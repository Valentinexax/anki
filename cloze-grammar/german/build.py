"""Build german_grammar_cloze.txt from work/structure.json + work/content/*.json.

Applies OVERRIDES (corrections from the final read-through), renumbers every
cloze to c1, recomputes Type from the hints, writes the Anki TSV and runs the
final checks. Never hand-edit the output; fix the inputs or OVERRIDES instead.
"""
import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dupscan import scan  # noqa: E402
from validate import load_all  # noqa: E402

HERE = Path(__file__).parent
OUT = HERE / "german_grammar_cloze.txt"
HEADER = ["#separator:tab", "#html:true", "#guid column:1", "#notetype column:2",
          "#deck column:3", "#tags column:13"]
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::([^}]*))?\}\}")

# Corrections from the final read-through: sort ID -> {field: new value}.
OVERRIDES: dict[str, dict[str, str]] = {
    # Final read-through corrections.
    "DE-A1-02-018": {"notes": "sprechen changes e → i in the du and er forms: du sprichst, er spricht. With a language, gut Deutsch sprechen needs no article; Deutsch is the name of the language and so takes a capital."},
    "DE-A1-04-011": {"notes": "ich in the accusative is mich. anrufen takes a direct object, like English 'ring someone': Er ruft mich an. The prefix an goes to the end. In Switzerland the dative is used instead: Er ruft mir an."},
    "DE-A2-03-009": {"notes": "fragen takes the accusative of the person asked: Ich frage den Lehrer. What you ask about follows with nach + dative (nach dem Weg fragen); asking for something is bitten um + accusative."},
    "DE-A2-03-012": {"notes": "anrufen takes the accusative of the person called: Ruf mich an! In a du imperative, the prefix an still goes to the end, and bitte usually sits between the object and the prefix."},
    "DE-A2-07-014": {"notes": "mitbringen is separable and mixed: mit-ge-bracht. bringen changes both its vowel and its consonants in the past (brachte, gebracht) but still takes the weak -t ending."},
    "DE-A2-10-005": {"notes": "Dates use the ordinal with an adjective ending: der dritte Mai. Ordinals add -te up to 19 and -ste from 20; erste, dritte, siebte and achte are irregular."},
    "DE-A2-10-018": {"notes": "noch nichts means 'nothing yet', and noch nicht 'not yet'. The positive counterpart is schon etwas (something already). Without an object it's noch nicht: Ich habe noch nicht gegessen."},
    "DE-A2-11-005": {"notes": "jemand (somebody) takes the er form of the verb: Jemand hat angerufen. Its accusative and dative are jemanden and jemandem; in speech the endings are often dropped."},
    "DE-B1-02-012": {"notes": "With sehen and hören, the Perfekt traditionally uses the double infinitive: habe ihn kommen sehen, not gesehen. The participle form (kommen gesehen) is also accepted and common in speech."},
    "DE-B1-05-009": {"notes": "anrufen → rief … an. rufen and all its compounds share the Präteritum stem rief: aufrufen, zurückrufen. In a subordinate clause the prefix rejoins: als ich ihn anrief."},
    "DE-B1-05-011": {"notes": "regnen → regnete: regular, with an extra -e- after the gn cluster for pronunciation. den ganzen Tag gives the duration. Weather verbs take es as the subject."},
    "DE-B1-05-034": {"notes": "singen → sang → gesungen: i → a → u, the same pattern as trinken, finden and springen. The Perfekt uses haben, as singen is an activity, not a movement."},
    "DE-B1-14-009": {"notes": "manche (some) usually works like a der-word, so the plural adjective takes -en: manche jungen Leute. The strong form manche junge Leute is also accepted. It implies 'some, but not all'."},
    "DE-B2-08-012": {"notes": "zuliebe (for someone's sake) takes the dative and always follows its noun: dir zuliebe, der Umwelt zuliebe. Unlike gegenüber or entlang, it never stands before the noun."},
    "DE-B2-08-013": {"notes": "samt (together with) takes the dative: samt seiner Familie. It's more formal than mit and often suggests 'and all'. It also appears in the idiom samt und sonders (each and every one)."},
    "DE-B2-11-004": {"tr": "It would go faster if you helped me.", "flag": "tr: the Text was changed to wenn du mir helfen würdest, so the translation now includes 'me'"},
    "DE-C1-03-005": {"notes": "vorausgesetzt, (dass) = provided (that). mitspielen here means 'play along, cooperate'. Without dass, a main clause follows: vorausgesetzt, das Wetter spielt mit."},
    "DE-C1-06-005": {"notes": "beispielsweise = for example. It's more formal than zum Beispiel and is set off by commas. Its synonym zum Beispiel is the one abbreviated z. B. in writing."},
    "DE-C1-14-004": {"notes": "derer is the demonstrative genitive plural that points forward to a relative clause: die Zahl derer, die zustimmen. Using deren here is a common error; deren points back."},
    "DE-C2-07-002": {"notes": "Kaktus has the learned plural Kakteen; Kaktusse is colloquial. The singular is der Kaktus, a Greek word that came into German via Latin."},
    "DE-EX-01-006": {"notes": "muss has a short u, so ss. The infinitive müssen keeps ss, as its vowel is also short. Compare the noun Muße (leisure), which has a long u and so takes ß."},
    "DE-EX-01-017": {"notes": "A zu-infinitive depending on a noun (die Absicht) needs a comma. A comma is also required before infinitives introduced by um, ohne or statt: Er ging, ohne zu grüßen."},
}


def card_type(text: str) -> str:
    hints = [m.group(3) or "" for m in CLOZE.finditer(text)]
    choice = any("?" in h and (" or " in h or "/" in h) for h in hints)
    return "Choice" if choice else "Form"


def to_c1(text: str) -> str:
    return re.sub(r"\{\{c\d+::", "{{c1::", text)


def guid_field(guid: str) -> str:
    if any(ch in guid for ch in '#"\t'):
        return '"' + guid.replace('"', '""') + '"'
    return guid


def main() -> int:
    original = json.loads((HERE / "work" / "original.json").read_text(encoding="utf-8"))
    cards = json.loads((HERE / "work" / "structure.json").read_text(encoding="utf-8"))
    content = load_all()
    unknown = set(OVERRIDES) - {c["sort_id"] for c in cards}
    assert not unknown, f"overrides for unknown IDs: {unknown}"

    rows, built = [], []
    for c in cards:
        e = dict(content[c["sort_id"]])
        e.update(OVERRIDES.get(c["sort_id"], {}))
        text = to_c1(e.get("text", c["text"]))
        tr = e.get("tr", c["tr"])
        row = [c["guid"], "Typecloze", c["deck"], text, tr, card_type(text), e["notes"],
               e.get("tip", ""), e["register"], e.get("compare", ""), c["sort_id"],
               c["topic"], c["topic"]]
        rows.append(row)
        built.append({"sort_id": c["sort_id"], "text": text, "level": c["level"]})

    errors = []
    for row in rows:
        if len(row) != 13:
            errors.append(f"{row[10]}: {len(row)} fields")
        for i, f in enumerate(row[1:], 2):
            if any(ch in f for ch in '\t\n"'):
                errors.append(f"{row[10]}: column {i} contains tab, newline or quote")
        if re.search(r"\{\{c(?!1::)\d+::", row[3]):
            errors.append(f"{row[10]}: cloze number other than c1")
        if row[5] == "Form":
            for m in CLOZE.finditer(row[3]):
                # Whole-word match: Russian infinitives contain their own forms
                # (тащить / тащит) and short prepositions occur inside words.
                if m.group(3) and re.search(r"(?<!\w)" + re.escape(m.group(2)) + r"(?!\w)",
                                            m.group(3), re.I):
                    errors.append(f"{row[10]}: answer {m.group(2)!r} inside hint {m.group(3)!r}")
        if not 100 <= len(row[6]) <= 300:
            errors.append(f"{row[10]}: notes length {len(row[6])}")
        if len(row[7]) > 160:
            errors.append(f"{row[10]}: tip longer than 160")
        if not row[3].count("{{c1::"):
            errors.append(f"{row[10]}: no cloze")

    ids = [r[10] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate sort IDs")
    guids = [r[0] for r in rows]
    if len(guids) != len(set(guids)):
        errors.append("duplicate GUIDs")
    missing = {r["guid"] for r in original} - set(guids)
    if missing:
        errors.append(f"original GUIDs missing: {sorted(missing)}")

    hits = scan(built)
    for h in hits:
        errors.append(f"near-duplicate: {h}")

    with OUT.open("w", encoding="utf-8", newline="") as f:
        f.write("\n".join(HEADER) + "\n")
        for row in rows:
            f.write("\t".join([guid_field(row[0])] + row[1:]) + "\n")

    # Round-trip: parse the written file with a real TSV reader and compare GUIDs.
    body = [l for l in OUT.read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    parsed = list(csv.reader(body, delimiter="\t", quotechar='"'))
    if [p[0] for p in parsed] != guids or any(len(p) != 13 for p in parsed):
        errors.append("round-trip parse mismatch")

    counts = collections.Counter(c["level"] for c in cards)
    new = sum(1 for c in cards if c["old_id"] is None)
    types = collections.Counter(r[5] for r in rows)
    for e in errors:
        print("error:", e)
    print(f"wrote {OUT.name}: {len(rows)} cards ({len(original)} original + {new} new); "
          f"{dict(types)}; {len(errors)} error(s)")
    for level, n in counts.items():
        print(f"  {level}: {n}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
