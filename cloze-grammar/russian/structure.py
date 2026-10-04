"""Chapter plan: folds Supplement chapters into thematic chapters, inserts new
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
    # Cyrillic sorts after Latin, so this follows C2 in Anki's deck list.
    "Дополнительно (выше C2)": ("EX", "Extras"),
}
ROOT = "Cloze Grammar::Russian"

PLAN = {
    "A1": [
        ("Род, множественное число, притяжательные местоимения", ["A1-01-01", "A1-10b-03", "A1-10b-04", "A1-10-01", "A1-01-02", "A1-10b-01"]),
        ("Прилагательные, «этот», «какой» и порядковые числительные", ["A1-02-03", "NEW:molodoy", "A1-02-04", "A1-02-05", "A1-10b-02", "A1-10-04", "A1-10-02"]),
        ("Настоящее время", ["A1-03-06", "A1-03-07", "A1-03-08", "A1-10-03", "A1-03-09"]),
        ("Прошедшее и будущее время", ["A1-04-10", "A1-04-11"]),
        ("Предложный падеж; «в» и «на»", ["A1-05-12", "A1-10b-05", "A1-05-13", "A1-05-14", "A1-10b-07"]),
        ("Винительный падеж; «где» и «куда»", ["A1-06-15", "NEW:avtobus", "A1-06-16", "A1-06-17", "A1-06-18", "A1-06-19"]),
        ("Родительный падеж: основы", ["A1-07-20", "NEW:u-brata", "A1-07-21", "A1-10-05", "A1-07-22", "A1-07-23"]),
        ("Дательный и творительный падежи: основы", ["A1-08-24", "A1-08-25", "A1-08-26", "NEW:k-v", "A1-08-27"]),
        ("Глаголы движения, союзы и вопросительные слова", ["A1-09-28", "A1-10b-06", "A1-09-29", "A1-09-30", "A1-09-31"]),
    ],
    "A2": [
        ("Вид глагола: образование и прошедшее время", ["A2-01-01", "A2-01-02"]),
        ("Вид глагола: будущее время, инфинитив, повелительное наклонение", ["A2-02-03", "NEW:smogu", "A2-02-04", "A2-02-05", "A2-02-06", "A2-11b-11", "A2-02-07", "A2-11b-12"]),
        ("Спряжение: чередования и особые формы", ["A2-11b-08", "A2-11b-09", "A2-11b-10"]),
        ("Существительные: падежи множественного числа и чередования", ["A2-11-01", "A2-11b-03", "A2-11b-02", "A2-11b-04", "A2-11b-05", "A2-11b-01"]),
        ("Родительный падеж множественного числа и количество", ["A2-03-08", "A2-03-09", "A2-11b-16"]),
        ("Прилагательные и местоимения во всех падежах", ["A2-04-10", "A2-11b-06", "A2-11b-07", "A2-04-11", "A2-11b-19"]),
        ("Дательный падеж, безличные предложения, краткие прилагательные", ["A2-05-12", "NEW:byla-nuzhna", "NEW:nado-budet", "A2-05-13", "A2-05-14", "A2-11b-14", "A2-05-15"]),
        ("Творительный падеж", ["A2-06-16", "A2-06-17", "A2-06-18"]),
        ("Глаголы движения с приставками; положение в пространстве", ["A2-07-19", "A2-07-20", "A2-07-21", "A2-11-02", "A2-11b-13"]),
        ("Сложные предложения: «который», «что» / «чтобы», «если»", ["A2-08-22", "NEW:u-kotorogo", "A2-08-23", "A2-08-24"]),
        ("Сравнение и «свой»", ["A2-09-25", "A2-09-26", "A2-09-27"]),
        ("Выражения времени", ["A2-10-28", "A2-11b-17", "A2-11b-18"]),
        ("Трудные пары и речевые формулы", ["A2-11-03", "A2-11-04", "A2-11b-15", "A2-11b-20", "A2-11b-21"]),
    ],
    "B1": [
        ("Условное наклонение: «бы»", ["B1-01-01", "B1-01-02"]),
        ("Причастия", ["B1-02-03", "B1-02-04", "B1-02-05", "B1-02-06"]),
        ("Деепричастия", ["B1-03-07", "B1-03-08"]),
        ("Вид глагола: тонкости", ["B1-04-09", "B1-04-10", "B1-04-11", "B1-04-12", "B1-10b-11"]),
        ("Глаголы движения: пары и приставки", ["B1-05-13", "B1-05-14", "B1-10b-14"]),
        ("Падежи и предлоги", ["B1-06-15", "B1-10b-15", "B1-06-16", "B1-06-17", "B1-06-18", "B1-10b-16", "B1-10-03", "NEW:pro-o", "B1-06-19"]),
        ("Глаголы на «-ся», неопределённо-личные и отрицательные конструкции", ["B1-07-20", "B1-10b-10", "B1-10b-12", "B1-10b-13", "B1-07-21"]),
        ("«-то» и «-нибудь», «ли», союзы", ["B1-08-22", "B1-08-23", "B1-08-24", "B1-10b-18", "B1-10b-19"]),
        ("Местоимения: «друг друга», «сам», «каждый», неопределённые", ["B1-09-25", "B1-09-26", "B1-10-04", "B1-10b-09"]),
        ("Числительные", ["B1-09-27", "B1-10b-05", "B1-10b-06"]),
        ("Существительные: трудные формы, имена и отчества", ["B1-10b-01", "B1-10b-02", "B1-10b-03", "B1-10b-04", "B1-10b-20"]),
        ("Степени сравнения", ["B1-10b-07", "B1-10b-08"]),
        ("Управление глаголов и лексические пары", ["B1-10-01", "B1-10-02", "B1-10b-17"]),
    ],
    "B2": [
        ("Глаголы движения: переносные и особые значения", ["B2-01-01", "B2-01-02", "B2-11b-05"]),
        ("Вид глагола: сложные случаи", ["B2-02-03", "B2-02-04", "B2-02-05", "B2-11-01"]),
        ("«Удаться», «прийтись», «стоить», «следовать»", ["B2-03-07"]),
        ("Причастия, деепричастия и страдательный залог", ["B2-04-08", "B2-04-09", "B2-04-10"]),
        ("Книжные союзы и предлоги", ["B2-05-11", "B2-11b-06", "B2-05-12", "B2-11-03", "B2-11-04"]),
        ("Частицы: «же», «ведь», «именно», «даже»", ["B2-06-13"]),
        ("Употребление падежей", ["B2-07-06", "B2-07-14", "B2-07-15", "B2-07-16", "B2-07-17", "B2-11b-07"]),
        ("Уступка и пожелания: «как бы ни», «хотя бы», «пусть»", ["B2-08-18", "B2-08-19"]),
        ("Краткие прилагательные, притяжательные на «-ин», сравнение", ["B2-09-20", "B2-11b-04", "B2-11b-03", "B2-09-21"]),
        ("«Себя», «тот, кто» и неопределённые местоимения", ["B2-10-22", "B2-11-02", "B2-10-23"]),
        ("Числительные, проценты и фамилии в падежах", ["B2-11b-01", "B2-11b-02", "B2-11b-08"]),
    ],
    "C1": [
        ("Вид глагола и способы действия", ["C1-01-01", "C1-01-02", "C1-10b-01"]),
        ("Глагольно-именные сочетания", ["C1-02-03"]),
        ("Книжные предлоги", ["C1-03-04"]),
        ("Управление существительных и глаголов", ["C1-04-05"]),
        ("Причастия, деепричастия и относительные слова", ["C1-05-06", "C1-05-07", "C1-10b-03"]),
        ("Безличные конструкции", ["C1-06-08"]),
        ("Условие, вероятность и сопоставление", ["C1-07-09", "C1-10b-04"]),
        ("Частицы и чужая речь", ["C1-08-10", "C1-08-11", "C1-10-01"]),
        ("Собирательные числительные и приблизительность", ["C1-09-12", "C1-09-13", "C1-09-14", "C1-10b-02"]),
    ],
    "C2": [
        ("Разговорная грамматика", ["C2-01-01", "C2-01-02", "C2-01-03"]),
        ("Книжные и устаревшие формы", ["C2-02-04", "C2-02-05", "C2-02-06"]),
        ("Уменьшительные и увеличительные формы", ["C2-03-07"]),
        ("Тонкости согласования", ["C2-04-08", "C2-08-01-01", "C2-08-01-02"]),
        ("Склонение числительных и имён", ["C2-05-09", "C2-08-01-05", "C2-08-01-03"]),
        ("Типичные ошибки: формы глагола", ["C2-06-10"]),
        ("Типичные ошибки: выбор слова и падежа", ["C2-07-11", "C2-08-01-04", "C2-08-01-06"]),
    ],
    "Дополнительно (выше C2)": [
        ("Церковнославянский пласт", ["BC-01-01", "BC-01-02"]),
        ("Разговорный и интернет-русский", ["BC-02-01", "BC-02-02"]),
        ("Региональные слова", ["BC-03-01", "BC-03-02"]),
        ("Орфография: «-тся» / «-ться», «ъ», «не» / «ни»", ["BC-04-01", "BC-04-02", "BC-04-03", "BC-04b-02", "BC-04b-04"]),
        ("Орфография: «н» / «нн», слитно и раздельно, дефис, «ь»", ["BC-04b-01", "BC-04b-03", "BC-04b-05", "BC-04b-06"]),
        ("Частые ошибки", ["BC-05-01", "NEW:na-russkom"]),
    ],
}

# Topic tags for the A1 groups, which had none.
TOPICS = {
    "A1-01-01": "possessives", "A1-01-02": "plurals", "A1-02-03": "adj-agreement", "A1-02-04": "kakoy",
    "A1-02-05": "etot-eto", "A1-03-06": "conj-1", "A1-03-07": "conj-2", "A1-03-08": "stem-changes-a1",
    "A1-03-09": "sya-present", "A1-04-10": "past", "A1-04-11": "future-budu", "A1-05-12": "prep-endings",
    "A1-05-13": "v-na", "A1-05-14": "prep-pronouns-adj", "A1-06-15": "acc-fem", "A1-06-16": "acc-animate",
    "A1-06-17": "acc-pronouns", "A1-06-18": "acc-adj", "A1-06-19": "gde-kuda", "A1-07-20": "u-menya",
    "A1-07-21": "net-gen", "A1-07-22": "gen-possession", "A1-07-23": "numbers-gen", "A1-08-24": "dat-pronouns",
    "A1-08-25": "nravitsya", "A1-08-26": "dat-nouns", "A1-08-27": "instr-s", "A1-09-28": "motion-basic",
    "A1-09-29": "i-a-no", "A1-09-30": "potomu-poetomu", "A1-09-31": "qwords",
}

NEW = {
    "molodoy": ("Это {{c1::молодой::молодой · agreement (stressed ending)}} человек.", "This is a young man.", "adj-agreement"),
    "avtobus": ("(A man speaking) Я купил {{c1::стол::стол · accusative (inanimate)}}.", "I've bought a table.", "acc-inanimate"),
    "u-brata": ("У {{c1::сестры::сестра · у + genitive}} две кошки.", "My sister has two cats.", "u-menya"),
    "k-v": ("(Going to a person) Дети пошли {{c1::к::в or к?}} другу.", "The children have gone round to a friend's.", "dat-nouns"),
    "smogu": ("Извини, я не {{c1::смогу::мочь · perfective future}} помочь тебе в субботу.",
              "Sorry, I won't be able to help you on Saturday.", "perf-future"),
    "byla-nuzhna": ("(Last year) Мне {{c1::была нужна::нужна · past}} помощь.", "I needed help.", "nuzhen"),
    "nado-budet": ("Завтра мне {{c1::надо будет::надо · future}} рано встать.",
                   "I'll have to get up early tomorrow.", "impersonal-past"),
    "u-kotorogo": ("Это мой друг, у {{c1::которого::who · agreement, after у}} есть машина.",
                   "This is my friend who has a car.", "kotoryy"),
    "pro-o": ("(Colloquial, + accusative) Расскажи мне {{c1::про::о or про?}} свою поездку.",
              "Tell me about your trip.", "pro-o"),
    "na-russkom": ("Книга написана {{c1::на русском::по-русски or на русском?}} языке.",
                   "The book is written in Russian.", "errors-2"),
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
                                    "tr": tr, "topic": f"Russian::{tagseg}::grammar::{topic}"})
                    continue
                ids = [k for k in by_old if k == item or k.startswith(item + "-")]
                assert ids, f"nothing matches {item}"
                for k in ids:
                    assert k not in used, f"{k} used twice"
                    used.add(k)
                    r = by_old[k]
                    # Re-point the level segment of the topic tag(s) at the new level.
                    raw = r["topic"] or f"Russian::{tagseg}::grammar::{TOPICS[k.rsplit('-', 1)[0]]}"
                    topic = " ".join(
                        "::".join([t.split("::")[0], tagseg] + t.split("::")[2:])
                        if t.split("::")[2:3] == ["grammar"] else t
                        for t in raw.split())
                    members.append({"guid": r["guid"], "old_id": k, "new_key": None, "text": r["text"],
                                    "tr": r["tr"], "topic": topic})
            for n, m in enumerate(members, 1):
                m["sort_id"] = f"RU-{code}-{ch_no:02d}-{n:03d}"
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
