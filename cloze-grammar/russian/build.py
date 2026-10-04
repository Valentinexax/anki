"""Build russian_grammar_cloze.txt from work/structure.json + work/content/*.json.

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
OUT = HERE / "russian_grammar_cloze.txt"
HEADER = ["#separator:tab", "#html:true", "#guid column:1", "#notetype column:2",
          "#deck column:3", "#tags column:13"]
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::([^}]*))?\}\}")

# Corrections from the final read-through: sort ID -> {field: new value}.
OVERRIDES: dict[str, dict[str, str]] = {
    # Final read-through corrections.
    "RU-A1-01-007": {"notes": "тетрадь is a feminine -ь noun, so the familiar 'your' is твоя. Nouns ending in -сть, -чь, -шь and -щь are reliably feminine (новость, ночь, мышь, вещь); for the rest the gender has to be learned."},
    "RU-A1-01-009": {"notes": "её (her) is invariable like его, so it stays её even though дом is masculine: её дом, её машина, её письмо. The agreeing form ейный is non-standard dialect."},
    "RU-A1-01-022": {"notes": "окно is neuter in -о, so the plural is -а: окна. The stress shifts in the plural, from окно́ to о́кна, as with many neuters."},
    "RU-A1-01-026": {"notes": "дом takes a stressed -а in the plural: дома́, not домы. The same pattern gives города, поезда, учителя."},
    "RU-A1-03-002": {"notes": "ты takes -ешь: знаешь. Russian has a single present tense, so знаешь covers both 'you know' and 'do you know?'; a yes/no question is marked by intonation alone."},
    "RU-A1-03-009": {"notes": "он with звонить takes -ит: звонит. The stress is on the ending (звони́т); зво́нит is a common but non-standard pronunciation.", "tip": "Standard stress is звони́т, not зво́нит."},
    "RU-A1-03-014": {"notes": "ты takes the stressed ending -ёшь: живёшь. Yes/no questions keep the word order of a statement and rely on rising intonation on the key word, here далеко."},
    "RU-A1-03-015": {"notes": "писать changes с → ш in every present form: пишу, пишешь, пишут. The stress moves back after the я form: пишу́ but пи́шешь."},
    "RU-A1-03-029": {"notes": "учиться is reflexive, and the я form учу ends in a vowel, so the particle is -сь: учусь. With an infinitive it means 'learn to': учусь играть."},
    "RU-A1-05-017": {"notes": "почта is a fixed на noun: на почте, like на вокзале, на заводе and на стадионе. No rule predicts these; they have to be learned as a list."},
    "RU-A1-05-028": {"notes": "в becomes во before в or ф followed by another consonant: во Франции (фр-), во Владимире (вл-). в Финляндии keeps plain в, because a vowel follows ф."},
    "RU-A1-06-002": {"notes": "вода is the object of пить, so -а → -у: воду. The accusative is stem-stressed, во́ду, against вода́ in the nominative."},
    "RU-A1-06-014": {"notes": "он in the accusative is его, pronounced with в: yevó. It looks like the possessive 'his', but here it's the object, and it normally comes before the verb."},
    "RU-A1-09-003": {"notes": "A round trip in the past (went and came back) uses the multidirectional ходил. Я шёл в кино would mean I was on my way there."},
    "RU-A2-01-008": {"notes": "открывать (imperfective) pairs with открыть (perfective), which drops the suffix -ыва-. Who opened it implies the window is still open: a result, so the perfective. Кто takes masculine agreement by default."},
    "RU-A2-01-010": {"notes": "решать pairs with решить; the switch from -ать to -ить is a common way to form a perfective (решать / решить, отвечать / ответить). A decision made is a single completed act, so решили."},
    "RU-A2-01-013": {"notes": "Asking whether something has ever happened, with no interest in a result, takes the imperfective: Ты читал…? English uses the present perfect here ('Have you ever read…?')."},
    "RU-A2-02-012": {"notes": "Forgetting to do a specific thing takes the perfective infinitive: забыл купить. The buying is a single act that didn't take place."},
    "RU-A2-02-017": {"notes": "писать keeps its ш in the imperative: пиши, пишите. The stress follows the я form (пишу́), so the imperative ending is stressed."},
    "RU-A2-04-011": {"notes": "сын has the plural сыновья, with an inserted -ов-. The genitive plural is сыновей. In elevated style сыны is also found, as in сыны Отечества."},
    "RU-A2-04-017": {"notes": "учитель has the plural учителя, with stressed -я. The older plural учители survives only for great teachers and mentors: учители человечества."},
    "RU-A2-07-006": {"notes": "по + dative marks movement around or through a space: гулять по городу. Movement into the city is в город, out of it из города."},
    "RU-A2-09-022": {"notes": "вставать (get up) drops -ва- in the present: встаёт. The perfective is встать, with a different present stem: встану, встанешь."},
    "RU-A2-11-011": {"notes": "улица is feminine, so самая красивая. Both words agree with the noun, and самая declines like any feminine adjective: самой, самую."},
    "RU-A2-11-014": {"notes": "She called her own mum: свой refers back to она, and declines like мой: своей маме. Её маме would mean another woman's mother."},
    "RU-A2-12-008": {"notes": "A plain accusative gives duration: неделю (for a week). No preposition is needed. Most perfectives can't take a plain duration; про- and по- verbs are the exception (проработал неделю)."},
    "RU-A2-13-001": {"notes": "тоже says the same thing applies to a new subject: Я тоже. также adds a further item about the same subject and is more formal: а также по-немецки. Я также on its own is wrong."},
    "RU-B1-02-007": {"notes": "The short passive participle forms the passive with быть: книга написана. It agrees in gender with the subject (feminine -а), and in the present быть is omitted."},
    "RU-B1-04-004": {"notes": "Не нужно, like не надо, takes the imperfective when it means 'no need to': there's no point calling him at all. A perfective would sound like a warning."},
    "RU-B1-05-020": {"notes": "уйти has the imperfective уходить: поезд уходит. Timetables use the present for scheduled departures, as in English."},
    "RU-B1-06-002": {"notes": "для + genitive: мама → мамы. для marks the person something is meant for. With подарить, the recipient takes the bare dative instead: подарить маме."},
    "RU-B1-08-011": {"notes": "несмотря на + accusative means 'despite' a noun: несмотря на дождь. It's written as one word. With a clause it becomes несмотря на то что."},
    "RU-B1-08-013": {"notes": "так как (since, as) gives a reason and often begins the sentence. It's more formal than потому что, which normally follows the main clause."},
    "RU-B1-11-004": {"notes": "сапоги has a zero genitive plural, сапог, which looks like the nominative singular. Likewise ботинок, чулок, глаз."},
    "RU-B1-11-009": {"tr": "Attention, passengers!", "flag": "tr: Граждане пассажиры is an announcement formula, not a greeting; was Dear passengers!"},
    "RU-B1-13-005": {"notes": "учить кого + dative means 'teach someone something': учит детей музыке. The pupil is accusative and the subject taught is dative."},
    "RU-B2-05-005": {"notes": "по сравнению с + instrumental means 'compared with'. It's neutral, used in speech and writing. The variant в сравнении с is more bookish."},
    "RU-B2-05-008": {"notes": "при + prepositional means 'in the time of' a ruler: при Петре Первом. Пётр loses its ё in the oblique cases: Петра, Петре."},
    "RU-B2-09-008": {"notes": "мал (too small) is a short form of малый: мал, мала, мало, малы. ботинки is plural. The neuter мало also means 'little, not much'."},
    "RU-B2-09-018": {"notes": "самый can mean 'the very': в самом начале. It declines with the noun. самый also forms the superlative with adjectives: самый интересный."},
    "RU-C1-01-001": {"notes": "чуть не + perfective past means something almost happened but didn't: чуть не упал. The не isn't a real negation; the sentence is affirmative. едва не is a more bookish synonym."},
    "RU-C1-02-004": {"notes": "произвести впечатление на + accusative means 'make an impression on'. The past произвёл comes from вести (вёл), with ё under stress."},
    "RU-C1-03-006": {"notes": "в ходе + genitive means 'in the course of': в ходе переговоров. It's typical of news reports. Likewise в ходе работы, в ходе визита."},
    "RU-C1-07-008": {"notes": "не столько…, сколько… means 'not so much… as…'. It corrects or refines a description, and can join any parallel words: не столько читает, сколько смотрит картинки."},
    "RU-C1-08-003": {"notes": "как раз means 'just, exactly': как раз вовремя (just in time). It also means 'the right size': как раз по размеру. It can't be replaced by just as in 'just arrived', which is только что."},
    "RU-C1-08-004": {"notes": "вот-вот means 'any moment now' and goes with the perfective future: вот-вот отправится. It's written with a hyphen. с минуты на минуту is a synonym."},
    "RU-C2-01-003": {"notes": "папа → пап in the new vocative. This form is never used for a formal address or in writing. The full form папа is used everywhere else."},
    "RU-C2-06-003": {"notes": "ехать borrows its standard imperative from поехать: поезжай, plural поезжайте. Ехай and едь are non-standard. The prefixed verbs follow suit: приезжай, уезжай."},
    "RU-C2-06-008": {"notes": "их (their) never declines: их дом, их машина. ихний is non-standard, though common in colloquial and regional speech."},
    "RU-EX-02-006": {"notes": "здрасте is a fast-speech form of здравствуйте. It's polite but casual, fine for neighbours or shop staff. It's also spelt здрасьте."},
    "RU-EX-05-008": {"notes": "что бы ни (whatever) is two words; чтобы (in order to) is one. Test: чтобы can be replaced by для того чтобы, что бы ни cannot.", "register": "Written (spelling point)"},
    "RU-EX-05-011": {"notes": "по- + adjective in -ому forms an adverb with a hyphen: по-новому. Likewise по-русски, по-моему, по-твоему.", "register": "Written (spelling point)"},
    "RU-EX-05-016": {"notes": "Genitive plurals of feminine nouns ending in a sibilant have no ь: задач, туч, рощ. The ь rule for feminine nouns applies only to the nominative singular.", "register": "Written (spelling point)"},
    "RU-EX-05-019": {"notes": "пребывать (stay, be present) has пре-. It's an official word, and the noun is пребывание: пребывание в Москве.", "register": "Written (spelling point)"},
    # Register: spelling cards are written-language points, not a register.
    "RU-EX-04-001": {"register": "Written (spelling point)"},
    "RU-EX-04-002": {"register": "Written (spelling point)"},
    "RU-EX-04-003": {"register": "Written (spelling point)"},
    "RU-EX-04-004": {"register": "Written (spelling point)"},
    "RU-EX-04-005": {"register": "Written (spelling point)"},
    "RU-EX-04-006": {"register": "Written (spelling point)"},
    "RU-EX-04-007": {"register": "Written (spelling point)"},
    "RU-EX-04-008": {"register": "Written (spelling point)"},
    "RU-EX-04-009": {"register": "Written (spelling point)"},
    "RU-EX-04-010": {"register": "Written (spelling point)"},
    "RU-EX-04-011": {"register": "Written (spelling point)"},
    "RU-EX-04-012": {"register": "Written (spelling point)"},
    "RU-EX-05-001": {"register": "Written (spelling point)"},
    "RU-EX-05-002": {"register": "Written (spelling point)"},
    "RU-EX-05-003": {"register": "Written (spelling point)"},
    "RU-EX-05-004": {"register": "Written (spelling point)"},
    "RU-EX-05-005": {"register": "Written (spelling point)"},
    "RU-EX-05-006": {"register": "Written (spelling point)"},
    "RU-EX-05-007": {"register": "Written (spelling point)"},
    "RU-EX-05-009": {"register": "Written (spelling point)"},
    "RU-EX-05-010": {"register": "Written (spelling point)"},
    "RU-EX-05-012": {"register": "Written (spelling point)"},
    "RU-EX-05-013": {"register": "Written (spelling point)"},
    "RU-EX-05-014": {"register": "Written (spelling point)"},
    "RU-EX-05-015": {"register": "Written (spelling point)"},
    "RU-EX-05-017": {"register": "Written (spelling point)"},
    "RU-EX-05-018": {"register": "Written (spelling point)"},
    "RU-EX-05-020": {"register": "Written (spelling point)"},
    "RU-EX-05-021": {"register": "Written (spelling point)"},
    # Hints that gave the answer away (dictionary form = required form).
    "RU-A1-02-009": {"text": "Это {{c1::молодой::young · agreement (stressed ending)}} человек."},
    "RU-A1-06-006": {"text": "(A man speaking) Я купил {{c1::стол::table · accusative (inanimate)}}."},
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
