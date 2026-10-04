# Cloze Grammar: Chinese

Rebuild of the Anki "Cloze Grammar::Chinese" deck (Typecloze note type, 13-column TSV).

- `original.txt`: the export as received (821 notes).
- `chinese_grammar_cloze.txt`: the rebuilt deck to import (836 notes). **Generated; don't edit by hand.**
- `CHANGES.md`: every Text/Translation change and the new cards.

## Pipeline

```sh
python3 parse.py        # original.txt -> work/original.json
python3 structure.py    # chapter plan, new cards, new sort IDs -> work/structure.json
python3 validate.py     # checks work/content/*.json (per-card notes, tip, register, compare, fixes)
python3 build.py        # applies OVERRIDES, writes the TSV, runs final checks (needs jieba)
```

`dupscan.py` (used by `build.py`) flags sentence pairs with word-set Jaccard >= 0.55,
or >= 0.35 together with a difflib ratio > 0.8.

## Importing into Anki

1. File → Import → `chinese_grammar_cloze.txt`. Keep note type *Typecloze* and the
   update-existing-notes option; GUIDs match the old notes, so review history carries over.
2. **If the old deck was already in your collection:** Anki updates the notes but leaves their
   cards in the old decks. Open Tools → Debug Console, paste `move_to_new_decks.py`, press
   Ctrl+Enter. It moves each card to the chapter its Sort ID belongs to and removes the
   Chinese chapter decks left empty. (Tested on a copy: 600 cards moved, 46 empty decks removed.)
3. Run **Tools → Empty Cards** and delete. The 35 notes that used to have c2/c3 keep their
   old extra cards as empty cards until you do; deleting them drops those extra cards'
   history only, and the c1 card keeps its own.
