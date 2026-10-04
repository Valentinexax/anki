# Paste into Anki's Debug Console (Tools > Debug Console, or Ctrl+Shift+;) and press Ctrl+Enter.
# Moves every German cloze-grammar card into the chapter deck its Sort ID belongs to,
# then removes German chapter decks left empty. Only touches Typecloze notes whose
# Sort ID starts with DE-; reviews and scheduling are untouched.
DECKS = {
 "DE-A1-01": "Cloze Grammar::German::A1::01 sein, haben; du und Sie",
 "DE-A1-02": "Cloze Grammar::German::A1::02 Präsens: regelmäßig, Vokalwechsel, wissen, möchte",
 "DE-A1-03": "Cloze Grammar::German::A1::03 Artikel, Genus, Plural; kein und nicht",
 "DE-A1-04": "Cloze Grammar::German::A1::04 Akkusativ",
 "DE-A1-05": "Cloze Grammar::German::A1::05 Dativ und Präpositionen",
 "DE-A1-06": "Cloze Grammar::German::A1::06 Possessivartikel",
 "DE-A1-07": "Cloze Grammar::German::A1::07 Modalverben",
 "DE-A1-08": "Cloze Grammar::German::A1::08 Trennbare Verben",
 "DE-A1-09": "Cloze Grammar::German::A1::09 Verbzweitstellung und Fragen",
 "DE-A1-10": "Cloze Grammar::German::A1::10 Zeit und Ort, Uhrzeit, Zahlen und Mengen",
 "DE-A1-11": "Cloze Grammar::German::A1::11 Imperativ",
 "DE-A1-12": "Cloze Grammar::German::A1::12 Vergangenheit: war, hatte und Perfekt",
 "DE-A1-13": "Cloze Grammar::German::A1::13 es gibt, gern und lieber, man",
 "DE-A2-01": "Cloze Grammar::German::A2::01 Nebensätze: weil, dass, wenn, ob, als",
 "DE-A2-02": "Cloze Grammar::German::A2::02 Wechselpräpositionen, Richtung und Ort; stellen, legen, setzen, hängen",
 "DE-A2-03": "Cloze Grammar::German::A2::03 Dativverben, zwei Objekte, gefallen und mögen",
 "DE-A2-04": "Cloze Grammar::German::A2::04 Adjektivendungen",
 "DE-A2-05": "Cloze Grammar::German::A2::05 Komparativ und Superlativ",
 "DE-A2-06": "Cloze Grammar::German::A2::06 Reflexive Verben",
 "DE-A2-07": "Cloze Grammar::German::A2::07 Perfekt: unregelmäßige Partizipien und untrennbare Präfixe",
 "DE-A2-08": "Cloze Grammar::German::A2::08 Präteritum: Modalverben, es gab, wusste",
 "DE-A2-09": "Cloze Grammar::German::A2::09 Höflicher Konjunktiv II: hätte, könnten, würde, wäre",
 "DE-A2-10": "Cloze Grammar::German::A2::10 Zeitangaben: seit, vor, für, bis, ab; noch, erst; Datum",
 "DE-A2-11": "Cloze Grammar::German::A2::11 einer, keiner, welcher; jemand, niemand; meiner, der da",
 "DE-A2-12": "Cloze Grammar::German::A2::12 Besitz: Annas, von, wessen",
 "DE-A2-13": "Cloze Grammar::German::A2::13 werden",
 "DE-A2-14": "Cloze Grammar::German::A2::14 Genus nach Endung und Bedeutung; weitere Plurale",
 "DE-B1-01": "Cloze Grammar::German::B1::01 Verben mit Präposition; da- und wo-Wörter",
 "DE-B1-02": "Cloze Grammar::German::B1::02 Infinitiv mit und ohne zu; um … zu und damit",
 "DE-B1-03": "Cloze Grammar::German::B1::03 obwohl, trotzdem, trotz; weil und deshalb; aber und sondern; da, sonst, also",
 "DE-B1-04": "Cloze Grammar::German::B1::04 Relativsätze",
 "DE-B1-05": "Cloze Grammar::German::B1::05 Präteritum: Erzählen und starke Verben",
 "DE-B1-06": "Cloze Grammar::German::B1::06 haben oder sein; Doppelinfinitiv und Verbstellung",
 "DE-B1-07": "Cloze Grammar::German::B1::07 Passiv",
 "DE-B1-08": "Cloze Grammar::German::B1::08 Genitiv",
 "DE-B1-09": "Cloze Grammar::German::B1::09 Konjunktiv II: Irreales, Vergangenheit, als ob",
 "DE-B1-10": "Cloze Grammar::German::B1::10 n-Deklination",
 "DE-B1-11": "Cloze Grammar::German::B1::11 Zweiteilige Konjunktionen",
 "DE-B1-12": "Cloze Grammar::German::B1::12 Temporalsätze und Plusquamperfekt",
 "DE-B1-13": "Cloze Grammar::German::B1::13 lassen",
 "DE-B1-14": "Cloze Grammar::German::B1::14 Adjektive: Nominalisierung, Endungen nach dieser, Steigerung",
 "DE-B1-15": "Cloze Grammar::German::B1::15 werden für Vermutungen und Versprechen",
 "DE-B1-16": "Cloze Grammar::German::B1::16 selbst, einander, irgend-, jeder und alle; Bruchzahlen; Wortbildung",
 "DE-B2-01": "Cloze Grammar::German::B2::01 Konjunktiv I: indirekte Rede",
 "DE-B2-02": "Cloze Grammar::German::B2::02 Passiv: Ersatzformen, Dativverben, Zustand und Vorgang",
 "DE-B2-03": "Cloze Grammar::German::B2::03 Partizipien als Adjektive; Infinitiv Perfekt",
 "DE-B2-04": "Cloze Grammar::German::B2::04 Subjektive Modalverben: soll, muss, dürfte, will, kann",
 "DE-B2-05": "Cloze Grammar::German::B2::05 Modalpartikeln",
 "DE-B2-06": "Cloze Grammar::German::B2::06 Konjunktionen: indem, sodass, falls, ohne dass, außer dass",
 "DE-B2-07": "Cloze Grammar::German::B2::07 Nominalstil: beim Kochen, durch Üben",
 "DE-B2-08": "Cloze Grammar::German::B2::08 Präpositionen der Schriftsprache",
 "DE-B2-09": "Cloze Grammar::German::B2::09 Weitere Verben mit Präposition",
 "DE-B2-10": "Cloze Grammar::German::B2::10 Funktionsverbgefüge",
 "DE-B2-11": "Cloze Grammar::German::B2::11 Konjunktiv II: starke Formen, Doppelinfinitiv, Bedingung ohne wenn",
 "DE-B2-12": "Cloze Grammar::German::B2::12 es als Platzhalter; man, einen, einem",
 "DE-B2-13": "Cloze Grammar::German::B2::13 Futur II",
 "DE-B2-14": "Cloze Grammar::German::B2::14 Adjektivendungen nach alle, beide, viele, einige",
 "DE-B2-15": "Cloze Grammar::German::B2::15 haben und sein + zu; scheinen, drohen, pflegen",
 "DE-B2-16": "Cloze Grammar::German::B2::16 Nomen: Name, Herz, derselbe; geschlechtergerechte Formen",
 "DE-B2-17": "Cloze Grammar::German::B2::17 Präfixe trennbar oder untrennbar; starke und schwache Doppelformen",
 "DE-B2-18": "Cloze Grammar::German::B2::18 Relativsätze mit wo(r)-, wer und was",
 "DE-C1-01": "Cloze Grammar::German::C1::01 Genitivobjekte: gedenken, bedürfen, sich bedienen; bewusst, würdig",
 "DE-C1-02": "Cloze Grammar::German::C1::02 Feste Wendungen im Konjunktiv I",
 "DE-C1-03": "Cloze Grammar::German::C1::03 Partizipialkonstruktionen",
 "DE-C1-04": "Cloze Grammar::German::C1::04 Präpositionen der Amtssprache",
 "DE-C1-05": "Cloze Grammar::German::C1::05 Verbpräfixe: ver-, zer-, er-, ent-, be-",
 "DE-C1-06": "Cloze Grammar::German::C1::06 Adverbien auf -weise und -erweise",
 "DE-C1-07": "Cloze Grammar::German::C1::07 Inversion: Bedingung ohne wenn, kaum … als",
 "DE-C1-08": "Cloze Grammar::German::C1::08 Konjunktionen: zumal, wohingegen, geschweige denn, wo … doch",
 "DE-C1-09": "Cloze Grammar::German::C1::09 Korrelate: darauf, dass; davon ausgehen, dass",
 "DE-C1-10": "Cloze Grammar::German::C1::10 bekommen-Passiv, unpersönliches Passiv, Passiv im Konjunktiv II",
 "DE-C1-11": "Cloze Grammar::German::C1::11 Fallen bei Genus und Plural",
 "DE-C1-12": "Cloze Grammar::German::C1::12 als + Verb: als wäre nichts geschehen",
 "DE-C1-13": "Cloze Grammar::German::C1::13 Adjektive mit Präposition",
 "DE-C1-14": "Cloze Grammar::German::C1::14 Wortstellung und Bezug: Pronomen vor dem Subjekt, dessen, derer, manch, solch",
 "DE-C2-01": "Cloze Grammar::German::C2::01 Archaische und literarische Formen",
 "DE-C2-02": "Cloze Grammar::German::C2::02 Adverbiale Genitive",
 "DE-C2-03": "Cloze Grammar::German::C2::03 meinetwegen, um … willen, statt meiner",
 "DE-C2-04": "Cloze Grammar::German::C2::04 Konjunktiv I: möge, solle, indirekte Fragen",
 "DE-C2-05": "Cloze Grammar::German::C2::05 Konzessive Rahmen: so … auch, wie auch immer, mag … noch so",
 "DE-C2-06": "Cloze Grammar::German::C2::06 Juristische Sprache",
 "DE-C2-07": "Cloze Grammar::German::C2::07 Seltene Plurale",
 "DE-C2-08": "Cloze Grammar::German::C2::08 Namen im Genitiv",
 "DE-C2-09": "Cloze Grammar::German::C2::09 Vorfeld: Gesehen habe ich ihn nicht",
 "DE-C2-10": "Cloze Grammar::German::C2::10 Literarischer Konjunktiv II: stürbe, hülfe",
 "DE-EX-01": "Cloze Grammar::German::Zusatz (über C2)::01 Rechtschreibung nach Grammatik",
 "DE-EX-02": "Cloze Grammar::German::Zusatz (über C2)::02 Fallen für Englischsprachige",
 "DE-EX-03": "Cloze Grammar::German::Zusatz (über C2)::03 Regional und umgangssprachlich",
}

nt = mw.col.models.by_name("Typecloze")
moved = 0
for nid in mw.col.find_notes('"note:Typecloze" "Sort ID:DE-*"'):
    note = mw.col.get_note(nid)
    deck = DECKS.get(note["Sort ID"].rsplit("-", 1)[0])
    if not deck:
        continue
    did = mw.col.decks.id(deck)
    cids = [c.id for c in note.cards() if c.did != did]
    if cids:
        mw.col.set_deck(cids, did)
        moved += len(cids)
removed = []
for d in sorted(mw.col.decks.all_names_and_ids(), key=lambda d: -d.name.count("::")):
    if d.name.startswith("Cloze Grammar::German::") and d.name not in DECKS.values() \
            and not mw.col.decks.card_count(d.id, include_subdecks=True):
        mw.col.decks.remove([d.id])
        removed.append(d.name)
try:
    mw.reset()
except Exception:
    pass
print(f"moved {moved} cards; removed {len(removed)} empty decks")
