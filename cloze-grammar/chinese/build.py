"""Build chinese_grammar_cloze.txt from work/structure.json + work/content/*.json.

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
OUT = HERE / "chinese_grammar_cloze.txt"
HEADER = ["#separator:tab", "#html:true", "#guid column:1", "#notetype column:2",
          "#deck column:3", "#tags column:13"]
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::([^}]*))?\}\}")

# Corrections from the final read-through: sort ID -> {field: new value}.
OVERRIDES: dict[str, dict[str, str]] = {
    # Read-through corrections.
    "ZH-HSK1-03-015": {"notes": "Hours form a small, closed set, so the question is 几点. The answer needs no 是 (现在三点), and the polite way to ask a stranger is 请问，现在几点了?, with 了 because it asks how late it has got."},
    "ZH-HSK1-08-001": {"notes": "在 + place goes before the verb it locates: 在家 + 看电视. 我看电视在家 is ungrammatical; place phrases that come last in English usually move forward in Chinese."},
    "ZH-HSK1-08-006": {"notes": "包 is an object, so 在 can only take it once a location word turns it into a place: 包里, with 里 usually unstressed. Countries and cities never take 里: 在中国, not 在中国里."},
    "ZH-HSK2-01-007": {"notes": "开 + 着 describes the resulting state (open), not the act of opening, and 在 can't replace it here. A sentence-final 了 would report the change instead (see Compare)."},
    "ZH-HSK2-06-005": {"notes": "要…了 signals something imminent; 快, 快要 and 就要 are near-equivalents. 快 and 快要 can't take a specific time word, whereas 要 and 就要 can (明天就要走了)."},
    "ZH-HSK2-06-007": {"notes": "A definite time word (明天) rules out 快 and 快要, so 就要 is the usual choice; 就 adds a sense of 'as soon as that'. Plain 要…了 is also possible: 他明天要走了."},
    "ZH-HSK3-04-005": {"notes": "开心 is an adjective used adverbially before 唱歌, so 地. 开心 is close to 高兴 but more colloquial, and it reduplicates as 开开心心 for a vivid effect."},
    "ZH-HSK3-05-001": {"notes": "虽然 concedes a real fact, and 但是 / 可是 still introduces the main point. English uses only 'although'; Chinese normally keeps both halves of the pair."},
    "ZH-HSK3-07-001": {"compare": ""},
    "ZH-HSK3-04-006": {"compare": ""},
    "ZH-UX-02-006": {"compare": ""},
    "ZH-HSK4-07-009": {"tip": ""},
    "ZH-HSK4-04-004": {"notes": "说明 (the instructions) is something to follow, so 按照 (according to). 请按照说明使用 is a stock phrase on packaging; 按 alone is the shorter form (按说明使用)."},
    "ZH-HSK4-04-011": {"notes": "Self-reliance (靠自己) is the point, so 靠 (rely on), a verb here after the modal 要. Literally 靠 means 'lean against' (靠墙), and 依靠 is its formal two-syllable form."},
    "ZH-HSK6-04-008": {"tr": "There's no harm in saying it.",
                       "flag": "tr: aligned with the new hint 'no harm in' (was 'You might as well say it')"},
    "ZH-HSK79-12-003": {"notes": "枚 counts small flat or round objects: medals, coins, stamps, badges. It's formal and written; 块 or 个 replace it for coins in speech."},
    "ZH-UX-01-009": {"notes": "时间 is the topic and 别着急 the advice, so the predicate is 有的是 (there's plenty of). It also works before a noun: 他有的是钱 (he's got loads of money)."},
    "ZH-HSK3-09-009": {"text": "走{{c1::着::continuing (doubled verb + particle)}}走着就到了。",
                       "flag": "hint: answer 着 appeared inside the hint (V … V着)"},
    "ZH-HSK4-02-010": {"text": "他不但{{c1::不::negative (far from …; 反而 follows)}}帮忙，反而添乱。",
                       "flag": "hint: answer 不 appeared inside the hint (不但)"},
    "ZH-HSK1-02-014": {"text": "李明是我{{c1::的::possessive particle}}同事。", "tr": "Li Ming is my colleague.",
                       "flag": "dup: replaced 他是我的朋友; first replacement 她是我的同事 was still too close to HSK1-02-003"},
    "ZH-HSK2-11-011": {"text": "我爷爷今年八十{{c1::多::more than (… -odd)}}岁了。", "tr": "My grandad is over eighty.",
                       "notes": "多 after a round number gives 'more than': 八十多岁 = eighty-odd, anywhere from 81 to 89. With round numbers 多 comes before the measure word, here 岁.",
                       "flag": "dup: replaced 我们班有二十多个学生; first replacement 他已经四十多岁了 was close to HSK1-09-004"},
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
                if m.group(3) and m.group(2) in m.group(3):
                    errors.append(f"{row[10]}: answer {m.group(2)!r} inside hint {m.group(3)!r}")
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
