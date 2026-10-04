"""Build importable .apkg files from deck sources into dist/.

Usage: python tools/build.py [slug ...]

Note GUIDs and note type/deck IDs are taken from the sources, so importing a
rebuilt deck updates existing notes in Anki (keeping review history) instead
of creating duplicates.
"""

from __future__ import annotations

import sys
from pathlib import Path

import genanki

sys.path.insert(0, str(Path(__file__).parent))
from check import check_deck  # noqa: E402
from deckfile import Deck, all_decks  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def build(deck: Deck, out_dir: Path) -> Path:
    models = {
        nt["name"]: genanki.Model(
            nt["id"],
            nt["name"],
            fields=[{"name": f} for f in nt["fields"]],
            templates=nt["templates"],
            css=nt.get("css", ""),
            model_type=genanki.Model.CLOZE if nt["type"] == "cloze" else genanki.Model.FRONT_BACK,
            sort_field_index=nt.get("sort_field", 0),
        )
        for nt in deck.notetypes
    }
    decks = {name: genanki.Deck(did, name) for name, did in deck.decks.items()}

    for note in deck.notes:
        decks[note.get("deck", deck.name)].add_note(
            genanki.Note(
                model=models[note["notetype"]],
                fields=[str(v or "") for v in note["fields"].values()],
                guid=note["guid"],
                tags=note.get("tags") or [],
            )
        )

    media = sorted(str(p) for p in deck.media_dir.glob("*") if p.is_file() and p.name != ".gitkeep")
    out = out_dir / f"{deck.slug}.apkg"
    genanki.Package(list(decks.values()), media_files=media).write_to_file(str(out))
    return out


def main() -> int:
    decks = all_decks(REPO / "decks", sys.argv[1:] or None)
    out_dir = REPO / "dist"
    out_dir.mkdir(exist_ok=True)
    failed = False
    for deck in decks:
        errors, _ = check_deck(deck)
        if errors:
            failed = True
            print(f"skipping {deck.slug}: {len(errors)} error(s), run tools/check.py")
            continue
        out = build(deck, out_dir)
        print(f"built {out.relative_to(REPO)} ({len(deck.notes)} notes)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
