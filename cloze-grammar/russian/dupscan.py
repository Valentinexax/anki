"""Near-duplicate scan over card sentences.

A pair is flagged when Jaccard similarity of the word sets is >= 0.55, or
>= 0.35 together with a difflib ratio > 0.8. Words are lower-cased word
tokens of the sentence with cloze answers filled in and leading context cues
in brackets removed.
"""
import difflib
import itertools
import json
import re
import sys
from pathlib import Path

CLOZE = re.compile(r"\{\{c\d+::(.*?)(?:::[^}]*)?\}\}")
CUE = re.compile(r"\([^()]*\)\s*")
WORD = re.compile(r"\w+(?:-\w+)*")


def plain(text: str) -> str:
    text = CLOZE.sub(r"\1", text).replace("<br>", " ")
    return " ".join(WORD.findall(CUE.sub("", text).lower()))


def words(text: str) -> set[str]:
    return set(plain(text).split())


def scan(cards: list[dict]) -> list[tuple]:
    prepared = [(c["sort_id"], plain(c["text"]), words(c["text"])) for c in cards]
    hits = []
    for (ia, pa, wa), (ib, pb, wb) in itertools.combinations(prepared, 2):
        if not wa or not wb:
            continue
        j = len(wa & wb) / len(wa | wb)
        if j < 0.35:
            continue
        r = difflib.SequenceMatcher(None, pa, pb).ratio()
        if j >= 0.55 or r > 0.8:
            hits.append((round(j, 2), round(r, 2), ia, pa, ib, pb))
    return sorted(hits, reverse=True)


if __name__ == "__main__":
    path = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "work" / "structure.json")
    hits = scan(json.loads(path.read_text(encoding="utf-8")))
    for h in hits:
        print(*h)
    print(len(hits), "pairs flagged")
