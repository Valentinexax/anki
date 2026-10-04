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
2. Then run **Tools → Empty Cards** and delete. The 35 notes that used to have c2/c3 keep
   their old extra cards as empty cards until you do. Deleting them removes the review
   history of those extra cards only; the c1 card keeps its history.
3. The old empty chapter decks (e.g. `HSK3::10 Supplement`, `Beyond HSK::…`) will be left
   empty; delete them by hand.
