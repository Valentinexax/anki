# Working on this repo

Anki decks as text sources (`decks/<slug>/deck.yaml`, `notes.yaml`, `media/`),
built into `.apkg` with `tools/build.py`. See README.md for the workflow.

Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

Rules:
- New `.apkg` in `inbox/`: run `tools/extract.py`, commit the resulting `decks/<slug>/`,
  and delete the `.apkg` from `inbox/` in the same commit.
- Never modify existing `guid`s or note type `id`s; that breaks in-place updates of
  the user's collection. New notes get a fresh random guid.
- Keep each note's `fields` keys in the exact order of its note type's `fields`.
- Run `tools/check.py` and `tools/build.py` before committing; both must pass.
- When improving cards, prefer one fact per card, keep the original meaning, and
  don't silently drop content. Explain notable content changes in the commit message.
