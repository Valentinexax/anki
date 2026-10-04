# Anki decks

Anki decks stored as editable text files, so every change is reviewable in a
pull request, then rebuilt into `.apkg` files you can import.

## Workflow

1. **Export** a deck from Anki: *File → Export → Anki Deck Package (.apkg)*.
   Untick *Include scheduling information*; it isn't used.
2. **Upload** the `.apkg` into [`inbox/`](inbox/) (on GitHub: *Add file → Upload files*).
3. **Extract** it into text sources:
   ```sh
   python tools/extract.py inbox/MyDeck.apkg      # → decks/my-deck/
   ```
4. **Edit** `decks/<slug>/notes.yaml` (and `deck.yaml` for templates/CSS).
5. **Check and build**:
   ```sh
   python tools/check.py      # errors: missing media, empty fields, bad cloze, duplicate GUIDs…
   python tools/build.py      # → dist/<slug>.apkg
   ```
   CI runs both on every push. The built decks can be downloaded from the
   *decks* artifact of the workflow run (Actions tab).
6. **Import** `dist/<slug>.apkg` into Anki. Existing notes are **updated in place**,
   so review history is kept and no duplicates are created, because note GUIDs and
   note type IDs are preserved from the original export.

Setup: `pip install -r requirements.txt` (Python 3.10+).

## Layout

```
inbox/            raw .apkg exports waiting to be extracted
decks/<slug>/
  deck.yaml       deck + subdeck names/IDs, note types (fields, card templates, CSS)
  notes.yaml      one entry per note: guid, notetype, optional subdeck, tags, fields
  media/          images/audio referenced from fields
tools/            extract.py, check.py, build.py
dist/             build output (git-ignored)
```

## Rules for editing

- Never change or reuse a note's `guid`. It is how Anki matches the note to your cards.
- New notes need a new unique `guid` (any random string, e.g. 10 characters).
- Changing a note type's fields or templates is fine, but depending on your import settings Anki may
  update the note type, and removing fields can drop data from your collection.
- Deleting a note here does **not** delete it from your Anki collection on import;
  delete it in Anki too (or tag it and suspend it).
