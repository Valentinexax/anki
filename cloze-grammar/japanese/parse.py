"""Parse the original Anki TSV export into work/original.json."""
import csv, json
from pathlib import Path

HERE = Path(__file__).parent
COLS = ["guid", "notetype", "deck", "text", "tr", "type", "notes", "tip",
        "register", "compare", "sort_id", "topic", "tags"]

lines = (HERE / "original.txt").read_text(encoding="utf-8").splitlines()
header = [l for l in lines if l.startswith("#")]
body = [l for l in lines if not l.startswith("#")]
rows = []
for rec in csv.reader(body, delimiter="\t", quotechar='"'):
    assert len(rec) == 13, rec
    rows.append(dict(zip(COLS, rec)))
(HERE / "work" / "original.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(header), "header lines;", len(rows), "rows")
