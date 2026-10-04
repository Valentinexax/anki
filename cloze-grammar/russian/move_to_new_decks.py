# Paste into Anki's Debug Console (Tools > Debug Console, or Ctrl+Shift+;) and press Ctrl+Enter.
# Moves every Russian cloze-grammar card into the chapter deck its Sort ID belongs to,
# then removes Russian chapter decks (including the old English-named ones) left empty. Only touches Typecloze notes whose
# Sort ID starts with RU-; reviews and scheduling are untouched.
DECKS = {
 "RU-A1-01": "Cloze Grammar::Russian::A1::01 Род, множественное число, притяжательные местоимения",
 "RU-A1-02": "Cloze Grammar::Russian::A1::02 Прилагательные, «этот», «какой» и порядковые числительные",
 "RU-A1-03": "Cloze Grammar::Russian::A1::03 Настоящее время",
 "RU-A1-04": "Cloze Grammar::Russian::A1::04 Прошедшее и будущее время",
 "RU-A1-05": "Cloze Grammar::Russian::A1::05 Предложный падеж; «в» и «на»",
 "RU-A1-06": "Cloze Grammar::Russian::A1::06 Винительный падеж; «где» и «куда»",
 "RU-A1-07": "Cloze Grammar::Russian::A1::07 Родительный падеж: основы",
 "RU-A1-08": "Cloze Grammar::Russian::A1::08 Дательный и творительный падежи: основы",
 "RU-A1-09": "Cloze Grammar::Russian::A1::09 Глаголы движения, союзы и вопросительные слова",
 "RU-A2-01": "Cloze Grammar::Russian::A2::01 Вид глагола: образование и прошедшее время",
 "RU-A2-02": "Cloze Grammar::Russian::A2::02 Вид глагола: будущее время, инфинитив, повелительное наклонение",
 "RU-A2-03": "Cloze Grammar::Russian::A2::03 Спряжение: чередования и особые формы",
 "RU-A2-04": "Cloze Grammar::Russian::A2::04 Существительные: падежи множественного числа и чередования",
 "RU-A2-05": "Cloze Grammar::Russian::A2::05 Родительный падеж множественного числа и количество",
 "RU-A2-06": "Cloze Grammar::Russian::A2::06 Прилагательные и местоимения во всех падежах",
 "RU-A2-07": "Cloze Grammar::Russian::A2::07 Дательный падеж, безличные предложения, краткие прилагательные",
 "RU-A2-08": "Cloze Grammar::Russian::A2::08 Творительный падеж",
 "RU-A2-09": "Cloze Grammar::Russian::A2::09 Глаголы движения с приставками; положение в пространстве",
 "RU-A2-10": "Cloze Grammar::Russian::A2::10 Сложные предложения: «который», «что» / «чтобы», «если»",
 "RU-A2-11": "Cloze Grammar::Russian::A2::11 Сравнение и «свой»",
 "RU-A2-12": "Cloze Grammar::Russian::A2::12 Выражения времени",
 "RU-A2-13": "Cloze Grammar::Russian::A2::13 Трудные пары и речевые формулы",
 "RU-B1-01": "Cloze Grammar::Russian::B1::01 Условное наклонение: «бы»",
 "RU-B1-02": "Cloze Grammar::Russian::B1::02 Причастия",
 "RU-B1-03": "Cloze Grammar::Russian::B1::03 Деепричастия",
 "RU-B1-04": "Cloze Grammar::Russian::B1::04 Вид глагола: тонкости",
 "RU-B1-05": "Cloze Grammar::Russian::B1::05 Глаголы движения: пары и приставки",
 "RU-B1-06": "Cloze Grammar::Russian::B1::06 Падежи и предлоги",
 "RU-B1-07": "Cloze Grammar::Russian::B1::07 Глаголы на «-ся», неопределённо-личные и отрицательные конструкции",
 "RU-B1-08": "Cloze Grammar::Russian::B1::08 «-то» и «-нибудь», «ли», союзы",
 "RU-B1-09": "Cloze Grammar::Russian::B1::09 Местоимения: «друг друга», «сам», «каждый», неопределённые",
 "RU-B1-10": "Cloze Grammar::Russian::B1::10 Числительные",
 "RU-B1-11": "Cloze Grammar::Russian::B1::11 Существительные: трудные формы, имена и отчества",
 "RU-B1-12": "Cloze Grammar::Russian::B1::12 Степени сравнения",
 "RU-B1-13": "Cloze Grammar::Russian::B1::13 Управление глаголов и лексические пары",
 "RU-B2-01": "Cloze Grammar::Russian::B2::01 Глаголы движения: переносные и особые значения",
 "RU-B2-02": "Cloze Grammar::Russian::B2::02 Вид глагола: сложные случаи",
 "RU-B2-03": "Cloze Grammar::Russian::B2::03 «Удаться», «прийтись», «стоить», «следовать»",
 "RU-B2-04": "Cloze Grammar::Russian::B2::04 Причастия, деепричастия и страдательный залог",
 "RU-B2-05": "Cloze Grammar::Russian::B2::05 Книжные союзы и предлоги",
 "RU-B2-06": "Cloze Grammar::Russian::B2::06 Частицы: «же», «ведь», «именно», «даже»",
 "RU-B2-07": "Cloze Grammar::Russian::B2::07 Употребление падежей",
 "RU-B2-08": "Cloze Grammar::Russian::B2::08 Уступка и пожелания: «как бы ни», «хотя бы», «пусть»",
 "RU-B2-09": "Cloze Grammar::Russian::B2::09 Краткие прилагательные, притяжательные на «-ин», сравнение",
 "RU-B2-10": "Cloze Grammar::Russian::B2::10 «Себя», «тот, кто» и неопределённые местоимения",
 "RU-B2-11": "Cloze Grammar::Russian::B2::11 Числительные, проценты и фамилии в падежах",
 "RU-C1-01": "Cloze Grammar::Russian::C1::01 Вид глагола и способы действия",
 "RU-C1-02": "Cloze Grammar::Russian::C1::02 Глагольно-именные сочетания",
 "RU-C1-03": "Cloze Grammar::Russian::C1::03 Книжные предлоги",
 "RU-C1-04": "Cloze Grammar::Russian::C1::04 Управление существительных и глаголов",
 "RU-C1-05": "Cloze Grammar::Russian::C1::05 Причастия, деепричастия и относительные слова",
 "RU-C1-06": "Cloze Grammar::Russian::C1::06 Безличные конструкции",
 "RU-C1-07": "Cloze Grammar::Russian::C1::07 Условие, вероятность и сопоставление",
 "RU-C1-08": "Cloze Grammar::Russian::C1::08 Частицы и чужая речь",
 "RU-C1-09": "Cloze Grammar::Russian::C1::09 Собирательные числительные и приблизительность",
 "RU-C2-01": "Cloze Grammar::Russian::C2::01 Разговорная грамматика",
 "RU-C2-02": "Cloze Grammar::Russian::C2::02 Книжные и устаревшие формы",
 "RU-C2-03": "Cloze Grammar::Russian::C2::03 Уменьшительные и увеличительные формы",
 "RU-C2-04": "Cloze Grammar::Russian::C2::04 Тонкости согласования",
 "RU-C2-05": "Cloze Grammar::Russian::C2::05 Склонение числительных и имён",
 "RU-C2-06": "Cloze Grammar::Russian::C2::06 Типичные ошибки: формы глагола",
 "RU-C2-07": "Cloze Grammar::Russian::C2::07 Типичные ошибки: выбор слова и падежа",
 "RU-EX-01": "Cloze Grammar::Russian::Дополнительно (выше C2)::01 Церковнославянский пласт",
 "RU-EX-02": "Cloze Grammar::Russian::Дополнительно (выше C2)::02 Разговорный и интернет-русский",
 "RU-EX-03": "Cloze Grammar::Russian::Дополнительно (выше C2)::03 Региональные слова",
 "RU-EX-04": "Cloze Grammar::Russian::Дополнительно (выше C2)::04 Орфография: «-тся» / «-ться», «ъ», «не» / «ни»",
 "RU-EX-05": "Cloze Grammar::Russian::Дополнительно (выше C2)::05 Орфография: «н» / «нн», слитно и раздельно, дефис, «ь»",
 "RU-EX-06": "Cloze Grammar::Russian::Дополнительно (выше C2)::06 Частые ошибки"
}

nt = mw.col.models.by_name("Typecloze")
moved = 0
for nid in mw.col.find_notes('"note:Typecloze" "Sort ID:RU-*"'):
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
    if d.name.startswith("Cloze Grammar::Russian::") and d.name not in DECKS.values() \
            and not mw.col.decks.card_count(d.id, include_subdecks=True):
        mw.col.decks.remove([d.id])
        removed.append(d.name)
try:
    mw.reset()
except Exception:
    pass
print(f"moved {moved} cards; removed {len(removed)} empty decks")
