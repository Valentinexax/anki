"""Chapter plan: folds Supplement chapters into thematic chapters (German), inserts new
cards and assigns new sort IDs. Writes work/structure.json.

Each chapter lists items in order: an old group prefix ("HSK1-01-03" takes every
card in that group), a single old card ID ("HSK1-10b-05-03"), or "NEW:key".
"""
import json
import random
import string
from pathlib import Path

HERE = Path(__file__).parent
WORK = HERE / "work"

# Level name in the deck path -> (sort-ID code, tag segment)
LEVELS = {
    "A1": ("A1", "A1"), "A2": ("A2", "A2"), "B1": ("B1", "B1"), "B2": ("B2", "B2"),
    "C1": ("C1", "C1"), "C2": ("C2", "C2"),
    # "Z" sorts after "C2" in Anki's deck list.
    "Zusatz (über C2)": ("EX", "Extras"),
}
ROOT = "Cloze Grammar::German"

PLAN = {
    "A1": [
        ("sein, haben; du und Sie", ["A1-01-01", "A1-01-02", "A1-01-03"]),
        ("Präsens: regelmäßig, Vokalwechsel, wissen, möchte", ["A1-02-04", "A1-14-01", "A1-14-02", "A1-02-05", "A1-02-06", "A1-14-10"]),
        ("Artikel, Genus, Plural; kein und nicht", ["A1-03-07", "A1-14-07", "A1-14-08", "A1-03-08", "A1-03-09"]),
        ("Akkusativ", ["A1-04-10", "A1-04-11"]),
        ("Dativ und Präpositionen", ["A1-05-12", "A1-05-13", "A1-14-05"]),
        ("Possessivartikel", ["A1-06-14"]),
        ("Modalverben", ["A1-07-15"]),
        ("Trennbare Verben", ["A1-08-16", "A1-14-06"]),
        ("Verbzweitstellung und Fragen", ["A1-09-17", "A1-14-03"]),
        ("Zeit und Ort, Uhrzeit, Zahlen und Mengen", ["A1-10-18", "A1-14-04", "A1-14-09"]),
        ("Imperativ", ["A1-11-19"]),
        ("Vergangenheit: war, hatte und Perfekt", ["A1-12-20", "A1-12-21"]),
        ("es gibt, gern und lieber, man", ["A1-13-22"]),
    ],
    "A2": [
        ("Nebensätze: weil, dass, wenn, ob, als", ["A2-01-01"]),
        ("Wechselpräpositionen, Richtung und Ort; stellen, legen, setzen, hängen", ["A2-02-02", "NEW:hin-her", "A2-02-03", "A2-14-13", "A2-14-11", "A2-14-12"]),
        ("Dativverben, zwei Objekte, gefallen und mögen", ["A2-03-04", "A2-14-14", "A2-14-15", "A2-14-16"]),
        ("Adjektivendungen", ["A2-04-05", "NEW:grossem"]),
        ("Komparativ und Superlativ", ["A2-05-06"]),
        ("Reflexive Verben", ["A2-06-07"]),
        ("Perfekt: unregelmäßige Partizipien und untrennbare Präfixe", ["A2-07-08", "A2-14-17"]),
        ("Präteritum: Modalverben, es gab, wusste", ["A2-08-09"]),
        ("Höflicher Konjunktiv II: hätte, könnten, würde, wäre", ["A2-09-10"]),
        ("Zeitangaben: seit, vor, für, bis, ab; noch, erst; Datum", ["A2-10-11", "A2-14-08", "A2-14-09", "A2-14-10", "A2-14-06", "A2-14-07", "A2-14-18"]),
        ("einer, keiner, welcher; jemand, niemand; meiner, der da", ["A2-11-12", "A2-14-04", "A2-14-05"]),
        ("Besitz: Annas, von, wessen", ["A2-12-13"]),
        ("werden", ["A2-13-14"]),
        ("Genus nach Endung und Bedeutung; weitere Plurale", ["A2-14-01", "A2-14-02", "A2-14-03"]),
    ],
    "B1": [
        ("Verben mit Präposition; da- und wo-Wörter", ["B1-01-01", "B1-01-02"]),
        ("Infinitiv mit und ohne zu; um … zu und damit", ["B1-02-03", "B1-02-04", "B1-15-05"]),
        ("obwohl, trotzdem, trotz; weil und deshalb; aber und sondern; da, sonst, also", ["B1-03-05", "B1-03-06", "B1-15-14"]),
        ("Relativsätze", ["B1-04-07", "NEW:mit-denen"]),
        ("Präteritum: Erzählen und starke Verben", ["B1-05-08", "B1-15-01", "B1-15-02"]),
        ("haben oder sein; Doppelinfinitiv und Verbstellung", ["B1-15-03", "B1-15-04", "B1-15-06"]),
        ("Passiv", ["B1-06-09"]),
        ("Genitiv", ["B1-07-10"]),
        ("Konjunktiv II: Irreales, Vergangenheit, als ob", ["B1-08-11"]),
        ("n-Deklination", ["B1-09-12"]),
        ("Zweiteilige Konjunktionen", ["B1-10-13"]),
        ("Temporalsätze und Plusquamperfekt", ["B1-11-14", "NEW:vor-bevor"]),
        ("lassen", ["B1-12-15"]),
        ("Adjektive: Nominalisierung, Endungen nach dieser, Steigerung", ["B1-13-16", "B1-15-07", "B1-15-08", "B1-15-09", "B1-15-10"]),
        ("werden für Vermutungen und Versprechen", ["B1-14-17"]),
        ("selbst, einander, irgend-, jeder und alle; Bruchzahlen; Wortbildung", ["B1-15-11", "B1-15-12", "B1-15-13", "B1-15-15", "B1-15-16"]),
    ],
    "B2": [
        ("Konjunktiv I: indirekte Rede", ["B2-01-01"]),
        ("Passiv: Ersatzformen, Dativverben, Zustand und Vorgang", ["B2-02-02", "B2-16-07", "B2-16-08"]),
        ("Partizipien als Adjektive; Infinitiv Perfekt", ["B2-03-03", "B2-16-06"]),
        ("Subjektive Modalverben: soll, muss, dürfte, will, kann", ["B2-04-04"]),
        ("Modalpartikeln", ["B2-05-05", "B2-16-04"]),
        ("Konjunktionen: indem, sodass, falls, ohne dass, außer dass", ["B2-06-06", "B2-16-12"]),
        ("Nominalstil: beim Kochen, durch Üben", ["B2-07-07"]),
        ("Präpositionen der Schriftsprache", ["B2-08-08", "B2-16-05"]),
        ("Weitere Verben mit Präposition", ["B2-09-09"]),
        ("Funktionsverbgefüge", ["B2-10-10"]),
        ("Konjunktiv II: starke Formen, Doppelinfinitiv, Bedingung ohne wenn", ["B2-11-11", "B2-16-09", "B2-16-10"]),
        ("es als Platzhalter; man, einen, einem", ["B2-12-12", "B2-16-13"]),
        ("Futur II", ["B2-13-13"]),
        ("Adjektivendungen nach alle, beide, viele, einige", ["B2-14-14"]),
        ("haben und sein + zu; scheinen, drohen, pflegen", ["B2-15-15"]),
        ("Nomen: Name, Herz, derselbe; geschlechtergerechte Formen", ["B2-16-01", "B2-16-02", "B2-16-15"]),
        ("Präfixe trennbar oder untrennbar; starke und schwache Doppelformen", ["B2-16-03", "B2-16-14"]),
        ("Relativsätze mit wo(r)-, wer und was", ["B2-16-11"]),
    ],
    "C1": [
        ("Genitivobjekte: gedenken, bedürfen, sich bedienen; bewusst, würdig", ["C1-01-01"]),
        ("Feste Wendungen im Konjunktiv I", ["C1-02-02"]),
        ("Partizipialkonstruktionen", ["C1-03-03"]),
        ("Präpositionen der Amtssprache", ["C1-04-04"]),
        ("Verbpräfixe: ver-, zer-, er-, ent-, be-", ["C1-05-05"]),
        ("Adverbien auf -weise und -erweise", ["C1-06-06"]),
        ("Inversion: Bedingung ohne wenn, kaum … als", ["C1-07-07"]),
        ("Konjunktionen: zumal, wohingegen, geschweige denn, wo … doch", ["C1-08-08", "C1-14-04"]),
        ("Korrelate: darauf, dass; davon ausgehen, dass", ["C1-09-09"]),
        ("bekommen-Passiv, unpersönliches Passiv, Passiv im Konjunktiv II", ["C1-10-10", "C1-14-03"]),
        ("Fallen bei Genus und Plural", ["C1-11-11", "C1-14-05"]),
        ("als + Verb: als wäre nichts geschehen", ["C1-12-12"]),
        ("Adjektive mit Präposition", ["C1-13-13"]),
        ("Wortstellung und Bezug: Pronomen vor dem Subjekt, dessen, derer, manch, solch", ["C1-14-01", "C1-14-02", "C1-14-06"]),
    ],
    "C2": [
        ("Archaische und literarische Formen", ["C2-01-01"]),
        ("Adverbiale Genitive", ["C2-02-02"]),
        ("meinetwegen, um … willen, statt meiner", ["C2-03-03"]),
        ("Konjunktiv I: möge, solle, indirekte Fragen", ["C2-04-04"]),
        ("Konzessive Rahmen: so … auch, wie auch immer, mag … noch so", ["C2-05-05"]),
        ("Juristische Sprache", ["C2-06-06"]),
        ("Seltene Plurale", ["C2-07-07"]),
        ("Namen im Genitiv", ["C2-08-08"]),
        ("Vorfeld: Gesehen habe ich ihn nicht", ["C2-09-09"]),
        ("Literarischer Konjunktiv II: stürbe, hülfe", ["C2-11-01"]),
    ],
    "Zusatz (über C2)": [
        ("Rechtschreibung nach Grammatik", ["BC-01-01", "BC-01-02", "BC-01-03", "BC-01-04", "BC-01-05"]),
        ("Fallen für Englischsprachige", ["BC-02-01", "BC-02-02", "BC-02-03", "BC-02-04", "BC-02-05", "BC-02-06"]),
        ("Regional und umgangssprachlich", ["C2-10-10", "BC-03-01", "BC-03-02", "BC-03-03", "BC-03-04"]),
    ],
}

TOPICS = {}

NEW = {
    "hin-her": ("(Towards the speaker) Komm bitte {{c1::her::hin or her?}}!<br>(Away from the speaker) Geh doch {{c1::hin::hin or her?}} und frag ihn!",
                "Come here, please! / Go over there and ask him!", "hin-her"),
    "grossem": ("Ich habe den Artikel mit {{c1::großem::groß · dative (Interesse, n.; no article)}} Interesse gelesen.",
                "I read the article with great interest.", "adj-endings"),
    "mit-denen": ("Das sind die Freunde, mit {{c1::denen::who · dative plural (Freunde; mit …)}} ich in Urlaub fahre.",
                  "These are the friends I'm going on holiday with.", "relative"),
    "vor-bevor": ("{{c1::Vor::vor or bevor?}} dem Essen wasche ich mir die Hände.<br>{{c1::Bevor::vor or bevor?}} ich esse, wasche ich mir die Hände.",
                  "Before the meal I wash my hands. / Before I eat, I wash my hands.", "time-clauses"),
}

GUID_ALPHABET = string.ascii_letters + string.digits + "!#$%&()*+,-./:;<=>?@[]^_`{|}~"


def main():
    rows = json.loads((WORK / "original.json").read_text(encoding="utf-8"))
    by_old = {r["sort_id"][3:]: r for r in rows}
    guid_file = WORK / "new_guids.json"
    new_guids = json.loads(guid_file.read_text()) if guid_file.exists() else {}
    rng = random.SystemRandom()

    used, cards = set(), []
    for level, chapters in PLAN.items():
        code, tagseg = LEVELS[level]
        for ch_no, (ch_name, items) in enumerate(chapters, 1):
            deck = f"{ROOT}::{level}::{ch_no:02d} {ch_name}"
            members = []
            for item in items:
                if item.startswith("NEW:"):
                    key = item[4:]
                    text, tr, topic = NEW[key]
                    if key not in new_guids:
                        new_guids[key] = "".join(rng.choice(GUID_ALPHABET) for _ in range(10))
                    members.append({"guid": new_guids[key], "old_id": None, "new_key": key, "text": text,
                                    "tr": tr, "topic": f"German::{tagseg}::grammar::{topic}"})
                    continue
                ids = [k for k in by_old if k == item or k.startswith(item + "-")]
                assert ids, f"nothing matches {item}"
                for k in ids:
                    assert k not in used, f"{k} used twice"
                    used.add(k)
                    r = by_old[k]
                    # Re-point the level segment of the topic tag(s) at the new level.
                    raw = r["topic"]
                    topic = " ".join(
                        "::".join([t.split("::")[0], tagseg] + t.split("::")[2:])
                        if t.split("::")[2:3] == ["grammar"] else t
                        for t in raw.split())
                    members.append({"guid": r["guid"], "old_id": k, "new_key": None, "text": r["text"],
                                    "tr": r["tr"], "topic": topic})
            for n, m in enumerate(members, 1):
                m["sort_id"] = f"DE-{code}-{ch_no:02d}-{n:03d}"
                m["deck"] = deck
                m["level"] = level
                cards.append(m)

    missing = set(by_old) - used
    assert not missing, f"unplaced cards: {sorted(missing)}"
    guid_file.write_text(json.dumps(new_guids, indent=1))
    (WORK / "structure.json").write_text(json.dumps(cards, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(cards)} cards ({len(cards) - len(rows)} new) in "
          f"{sum(len(c) for c in PLAN.values())} chapters")


if __name__ == "__main__":
    main()
