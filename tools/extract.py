"""Convert an exported .apkg into the editable text format under decks/<slug>/.

Usage: python tools/extract.py inbox/MyDeck.apkg [--slug my-deck] [--force]

Reads any .apkg version (legacy and the newer zstd format) via the official
Anki library. Scheduling/review history is never extracted.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

from anki.collection import Collection, ImportAnkiPackageOptions, ImportAnkiPackageRequest

sys.path.insert(0, str(Path(__file__).parent))
from deckfile import dump  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "deck"


def notetype_to_dict(nt: dict) -> dict:
    return {
        "name": nt["name"],
        "id": nt["id"],
        "type": "cloze" if nt["type"] == 1 else "normal",
        "sort_field": nt["sortf"],
        "fields": [f["name"] for f in nt["flds"]],
        "templates": [
            {"name": t["name"], "qfmt": t["qfmt"], "afmt": t["afmt"]} for t in nt["tmpls"]
        ],
        "css": nt["css"],
    }


def extract(apkg: Path, slug: str | None, force: bool) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        col = Collection(str(Path(tmp) / "collection.anki2"))
        try:
            # A fresh collection ships stock note types ("Basic", "Cloze", ...).
            # Rename them so imported note types keep their names instead of
            # being renamed to "Basic+" on conflict.
            for entry in col.models.all_names_and_ids():
                nt = col.models.get(entry.id)
                nt["name"] = f"__stock_{entry.id}"
                col.models.update_dict(nt)

            col.import_anki_package(
                ImportAnkiPackageRequest(
                    package_path=str(apkg.resolve()),
                    options=ImportAnkiPackageOptions(with_scheduling=False),
                )
            )

            notes, used_nts, deck_ids = [], {}, {}
            for nid in col.find_notes(""):
                note = col.get_note(nid)
                nt = note.note_type()
                used_nts[nt["id"]] = nt
                cards = sorted(note.cards(), key=lambda c: c.ord)
                deck = col.decks.get(cards[0].did)
                deck_ids[deck["name"]] = deck["id"]
                notes.append(
                    {
                        "guid": note.guid,
                        "notetype": nt["name"],
                        "deck": deck["name"],
                        "tags": list(note.tags),
                        "fields": dict(note.items()),
                    }
                )
            if not notes:
                sys.exit(f"{apkg}: no notes found")

            root = Counter(n["deck"].split("::")[0] for n in notes).most_common(1)[0][0]
            out = REPO / "decks" / (slug or slugify(root))
            if out.exists():
                if not force:
                    sys.exit(f"{out} already exists; pass --force to overwrite")
                shutil.rmtree(out)
            (out / "media").mkdir(parents=True)

            # Only keep the subdeck key when it differs from the main deck.
            for n in notes:
                if n["deck"] == root:
                    del n["deck"]
            deck_ids.setdefault(root, col.decks.id(root))

            dump(
                {
                    "name": root,
                    "decks": dict(sorted(deck_ids.items())),
                    "notetypes": [notetype_to_dict(nt) for nt in used_nts.values()],
                },
                out / "deck.yaml",
            )
            dump(notes, out / "notes.yaml")

            media_dir = Path(col.media.dir())
            for f in sorted(media_dir.iterdir()):
                if f.is_file():
                    shutil.copy2(f, out / "media" / f.name)
            (out / "media" / ".gitkeep").touch()
        finally:
            col.close()

    print(f"extracted {len(notes)} notes into {out.relative_to(REPO)}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("apkg", type=Path)
    ap.add_argument("--slug", help="directory name under decks/ (default: from deck name)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing deck directory")
    args = ap.parse_args()
    extract(args.apkg, args.slug, args.force)


if __name__ == "__main__":
    main()
