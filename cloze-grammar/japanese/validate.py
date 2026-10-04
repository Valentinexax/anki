"""Validate content chunks against work/structure.json.

Usage: python validate.py [LEVEL ...]   (file names under work/content/, e.g. HSK1 UX)
Checks: every sort ID of the level present and no strays; notes and register
filled; note length 100-300; tip <= 160; no duplicate notes or tips across
all chunks; cloze answers unchanged unless the flag says the answer changed;
every text/tr change carries a flag; no tab, newline or double quote.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).parent
CONTENT = HERE / "work" / "content"
ANSWERS = re.compile(r"\{\{c\d+::(.*?)(?:::[^}]*)?\}\}")
FILE_FOR = {"番外（JLPT範囲外）": "EX"}


def load_all():
    merged = {}
    for f in sorted(CONTENT.glob("*.json")):
        for k, v in json.loads(f.read_text(encoding="utf-8")).items():
            assert k not in merged, f"{k} in two chunks"
            merged[k] = v
    return merged


def main(levels):
    cards = json.loads((HERE / "work" / "structure.json").read_text(encoding="utf-8"))
    content = load_all()
    errors, warnings = [], []
    want = {FILE_FOR.get(c["level"], c["level"]) for c in cards} if not levels else set(levels)
    for c in cards:
        chunk = FILE_FOR.get(c["level"], c["level"])
        if chunk not in want:
            continue
        sid = c["sort_id"]
        e = content.get(sid)
        if e is None:
            errors.append(f"{sid}: missing")
            continue
        for key in ("notes", "register"):
            if not e.get(key, "").strip():
                errors.append(f"{sid}: empty {key}")
        n = len(e.get("notes", ""))
        if not 100 <= n <= 300:
            warnings.append(f"{sid}: notes length {n}")
        if len(e.get("tip", "")) > 160:
            errors.append(f"{sid}: tip length {len(e['tip'])}")
        for key, val in e.items():
            if any(ch in str(val) for ch in '\t\n"'):
                errors.append(f"{sid}: {key} contains tab, newline or double quote")
        if ("text" in e or "tr" in e) and not e.get("flag"):
            errors.append(f"{sid}: text/tr changed without flag")
        if "text" in e:
            old, new = ANSWERS.findall(c["text"]), ANSWERS.findall(e["text"])
            if old != new and "answer" not in e.get("flag", ""):
                errors.append(f"{sid}: answers {old} -> {new} without 'answer' in flag")
    ids = {c["sort_id"] for c in cards}
    for k in content:
        if k not in ids:
            errors.append(f"{k}: not in structure")

    # Duplicate / near-duplicate notes and tips across every chunk.
    items = sorted(content.items())
    for field, limit in (("notes", 0.85), ("tip", 0.85)):
        seen = [(k, v.get(field, "")) for k, v in items if v.get(field)]
        for i, (ka, a) in enumerate(seen):
            for kb, b in seen[i + 1:]:
                m = SequenceMatcher(None, a, b)
                if a == b or (m.real_quick_ratio() > limit and m.quick_ratio() > limit
                              and m.ratio() > limit):
                    errors.append(f"{field} too similar: {ka} / {kb}")
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
