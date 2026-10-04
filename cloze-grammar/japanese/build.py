"""Build japanese_grammar_cloze.txt from work/structure.json + work/content/*.json.

Applies OVERRIDES (corrections from the final read-through), renumbers every
cloze to c1, recomputes Type from the hints, writes the Anki TSV and runs the
final checks. Never hand-edit the output; fix the inputs or OVERRIDES instead.
"""
import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dupscan import scan  # noqa: E402
from validate import load_all  # noqa: E402

HERE = Path(__file__).parent
OUT = HERE / "japanese_grammar_cloze.txt"
HEADER = ["#separator:tab", "#html:true", "#guid column:1", "#notetype column:2",
          "#deck column:3", "#tags column:13"]
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::([^}]*))?\}\}")

# Corrections from the final read-through: sort ID -> {field: new value}.
OVERRIDES: dict[str, dict[str, str]] = {
}


def card_type(text: str) -> str:
    hints = [m.group(3) or "" for m in CLOZE.finditer(text)]
    choice = any("?" in h and (" or " in h or "/" in h) for h in hints)
    return "Choice" if choice else "Form"


def to_c1(text: str) -> str:
    return re.sub(r"\{\{c\d+::", "{{c1::", text)


def guid_field(guid: str) -> str:
    if any(ch in guid for ch in '#"\t'):
        return '"' + guid.replace('"', '""') + '"'
    return guid


def main() -> int:
    original = json.loads((HERE / "work" / "original.json").read_text(encoding="utf-8"))
    cards = json.loads((HERE / "work" / "structure.json").read_text(encoding="utf-8"))
    content = load_all()
    unknown = set(OVERRIDES) - {c["sort_id"] for c in cards}
    assert not unknown, f"overrides for unknown IDs: {unknown}"

    rows, built = [], []
    for c in cards:
        e = dict(content[c["sort_id"]])
        e.update(OVERRIDES.get(c["sort_id"], {}))
        text = to_c1(e.get("text", c["text"]))
        tr = e.get("tr", c["tr"])
        row = [c["guid"], "Typecloze", c["deck"], text, tr, card_type(text), e["notes"],
               e.get("tip", ""), e["register"], e.get("compare", ""), c["sort_id"],
               c["topic"], c["topic"]]
        rows.append(row)
        built.append({"sort_id": c["sort_id"], "text": text, "level": c["level"]})

    errors = []
    for row in rows:
        if len(row) != 13:
            errors.append(f"{row[10]}: {len(row)} fields")
        for i, f in enumerate(row[1:], 2):
            if any(ch in f for ch in '\t\n"'):
                errors.append(f"{row[10]}: column {i} contains tab, newline or quote")
        if re.search(r"\{\{c(?!1::)\d+::", row[3]):
            errors.append(f"{row[10]}: cloze number other than c1")
        if row[5] == "Form":
            for m in CLOZE.finditer(row[3]):
                # Japanese has no spaces, so any occurrence counts; English
                # answers (rare) are matched as whole words.
                ans, hint = m.group(2), m.group(3) or ""
                pat = re.escape(ans) if re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", ans) \
                    else r"(?<!\w)" + re.escape(ans) + r"(?!\w)"
                if hint and re.search(pat, hint, re.I):
                    errors.append(f"{row[10]}: answer {m.group(2)!r} inside hint {m.group(3)!r}")
        if not 100 <= len(row[6]) <= 300:
            errors.append(f"{row[10]}: notes length {len(row[6])}")
        if len(row[7]) > 160:
            errors.append(f"{row[10]}: tip longer than 160")
        if not row[3].count("{{c1::"):
            errors.append(f"{row[10]}: no cloze")

    ids = [r[10] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate sort IDs")
    guids = [r[0] for r in rows]
    if len(guids) != len(set(guids)):
        errors.append("duplicate GUIDs")
    missing = {r["guid"] for r in original} - set(guids)
    if missing:
        errors.append(f"original GUIDs missing: {sorted(missing)}")

    hits = scan(built)
    for h in hits:
        errors.append(f"near-duplicate: {h}")

    with OUT.open("w", encoding="utf-8", newline="") as f:
        f.write("\n".join(HEADER) + "\n")
        for row in rows:
            f.write("\t".join([guid_field(row[0])] + row[1:]) + "\n")

    # Round-trip: parse the written file with a real TSV reader and compare GUIDs.
    body = [l for l in OUT.read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    parsed = list(csv.reader(body, delimiter="\t", quotechar='"'))
    if [p[0] for p in parsed] != guids or any(len(p) != 13 for p in parsed):
        errors.append("round-trip parse mismatch")

    counts = collections.Counter(c["level"] for c in cards)
    new = sum(1 for c in cards if c["old_id"] is None)
    types = collections.Counter(r[5] for r in rows)
    for e in errors:
        print("error:", e)
    print(f"wrote {OUT.name}: {len(rows)} cards ({len(original)} original + {new} new); "
          f"{dict(types)}; {len(errors)} error(s)")
    for level, n in counts.items():
        print(f"  {level}: {n}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
