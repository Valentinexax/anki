"""Validate deck sources. Exits non-zero on errors; warnings are informational.

Usage: python tools/check.py [slug ...]
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deckfile import Deck, all_decks  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
MEDIA_RE = re.compile(r"""<img[^>]+src=["']?([^"'>\s]+)|\[sound:([^\]]+)\]""", re.I)
CLOZE_RE = re.compile(r"\{\{c\d+::")
TAG_RE = re.compile(r"<[^>]+>")


def check_deck(deck: Deck) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    where = deck.slug

    for name, count in Counter(nt["name"] for nt in deck.notetypes).items():
        if count > 1:
            errors.append(f"{where}: duplicate notetype name {name!r}")
    if deck.name not in deck.decks:
        errors.append(f"{where}: main deck {deck.name!r} missing from decks")

    guids = Counter(n.get("guid") for n in deck.notes)
    for guid, count in guids.items():
        if not guid:
            errors.append(f"{where}: note without guid")
        elif count > 1:
            errors.append(f"{where}: guid {guid} used by {count} notes")

    media = {p.name for p in deck.media_dir.glob("*") if p.is_file() and p.name != ".gitkeep"}
    referenced: set[str] = set()
    fronts: Counter[str] = Counter()

    for i, note in enumerate(deck.notes):
        tag = f"{where}: note {note.get('guid', f'#{i}')}"
        nt = deck.notetype(note.get("notetype", ""))
        if nt is None:
            errors.append(f"{tag}: unknown notetype {note.get('notetype')!r}")
            continue
        fields = note.get("fields") or {}
        if list(fields) != nt["fields"]:
            errors.append(f"{tag}: fields {list(fields)} != notetype fields {nt['fields']}")
            continue
        sub = note.get("deck")
        if sub is not None and sub not in deck.decks:
            errors.append(f"{tag}: subdeck {sub!r} missing from deck.yaml decks")
        for t in note.get("tags") or []:
            if not t or any(c.isspace() for c in t):
                errors.append(f"{tag}: invalid tag {t!r}")

        values = [str(v or "") for v in fields.values()]
        if not values[0].strip():
            errors.append(f"{tag}: first field is empty")
        if nt["type"] == "cloze" and not CLOZE_RE.search(values[0]):
            errors.append(f"{tag}: cloze note has no {{{{c1::...}}}} deletion")
        fronts[TAG_RE.sub("", values[nt.get("sort_field", 0)]).strip().lower()] += 1

        for v in values:
            for img, sound in MEDIA_RE.findall(v):
                referenced.add(img or sound)

    for name in sorted(referenced - media):
        errors.append(f"{where}: missing media file {name!r}")
    for name in sorted(media - referenced):
        warnings.append(f"{where}: unused media file {name!r}")
    for front, count in fronts.items():
        if front and count > 1:
            warnings.append(f"{where}: {count} notes share sort field {front[:60]!r}")
    return errors, warnings


def main() -> int:
    decks = all_decks(REPO / "decks", sys.argv[1:] or None)
    errors, warnings = [], []
    for deck in decks:
        e, w = check_deck(deck)
        errors += e
        warnings += w
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"checked {len(decks)} deck(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
