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
    "HSK1": ("HSK1", "HSK1"),
    "HSK2": ("HSK2", "HSK2"),
    "HSK3": ("HSK3", "HSK3"),
    "HSK4": ("HSK4", "HSK4"),
    "HSK5": ("HSK5", "HSK5"),
    "HSK6": ("HSK6", "HSK6"),
    "HSK7-9": ("HSK79", "HSK7-9"),
    # Anki sorts decks alphabetically: "Extras…" would sort before "HSK1".
    "Usage extras (beyond HSK)": ("UX", "Usage-extras"),
}

PLAN = {
    "HSK1": [
        ("是, 有 and 在", ["HSK1-01-01", "HSK1-01-02", "HSK1-01-03", "HSK1-01-04", "HSK1-01-05"]),
        ("Pronouns, 这 / 那, 的, 叫 / 姓", ["HSK1-02-06", "HSK1-02-07", "HSK1-02-08", "HSK1-10b-03", "HSK1-02-09"]),
        ("Questions", ["HSK1-03-10", "HSK1-03-11", "HSK1-10b-01", "HSK1-03-12", "HSK1-03-13", "HSK1-10b-05-01"]),
        ("Numbers, money and measure words", ["HSK1-04-14", "HSK1-04-15", "HSK1-04-16", "HSK1-10b-04-01",
                                              "HSK1-10b-04-02", "HSK1-10b-04-03", "HSK1-10b-04-04", "HSK1-10b-04-05"]),
        ("Dates and time", ["HSK1-05-17", "HSK1-10b-04-06", "HSK1-05-18", "NEW:liang-dian", "HSK1-05-19"]),
        ("Adverbs: 不 / 没, 很, 太…了, 也, 都, 一起", ["HSK1-06-20", "HSK1-10b-02", "HSK1-06-21", "HSK1-06-22", "HSK1-06-23"]),
        ("Modal verbs; 喜欢; 认识 vs 知道", ["HSK1-07-24", "NEW:yao-xiang", "NEW:xiang-miss", "HSK1-10b-05-03",
                                          "HSK1-07-25", "HSK1-10b-05-02"]),
        ("Place: 在 + place, location words", ["HSK1-08-26", "HSK1-08-27"]),
        ("Particles: 了, 吧, 呢", ["HSK1-09-28", "HSK1-09-29", "HSK1-09-30"]),
    ],
    "HSK2": [
        ("Aspect: 过, 着, 正在; negating 了", ["HSK2-01-01", "HSK2-01-02", "HSK2-11b-03-04", "HSK2-11b-03-05",
                                            "HSK2-01-03", "HSK2-01-04", "NEW:zai-zhe"]),
        ("Complements: result, degree (得), direction", ["HSK2-02-05", "HSK2-02-06", "HSK2-02-07", "HSK2-02-08"]),
        ("Duration, frequency, 一下 and reduplication", ["HSK2-03-09", "HSK2-11b-03-01", "HSK2-11b-03-02",
                                                       "HSK2-11b-03-03", "HSK2-03-10", "HSK2-11b-02", "HSK2-03-11",
                                                       "HSK2-11b-11-01", "HSK2-11b-11-02"]),
        ("Comparison: 比, 没有, 一样, 更, 最", ["HSK2-04-12", "HSK2-11b-05-05", "HSK2-04-13", "HSK2-11b-06-01",
                                           "HSK2-11b-06-03", "HSK2-04-14"]),
        ("Questions: A-不-A, 还是 vs 或者, 为什么 / 怎么", ["HSK2-05-15", "HSK2-11b-09-06", "HSK2-05-16", "HSK2-05-17",
                                                     "HSK2-11b-06-02", "HSK2-11b-08-03"]),
        ("Sentence patterns: 是…的, 要…了, serial verbs, 让", ["HSK2-06-18", "HSK2-06-19", "HSK2-06-20", "HSK2-06-21"]),
        ("Modal verbs: 应该, 得, 敢, 愿意, 不用", ["HSK2-11b-07", "NEW:buyong-dei", "NEW:mei-neng"]),
        ("Adverbs: 再 / 又, 就 / 才, 还, 已经, 别, 只", ["HSK2-07-22", "HSK2-11b-04-04", "HSK2-07-23", "HSK2-11b-05-01",
                                                  "HSK2-11b-05-02", "HSK2-11b-05-03", "HSK2-11b-05-04", "HSK2-07-24",
                                                  "HSK2-11b-05-06", "HSK2-07-25"]),
        ("Prepositions: 从…到, 离, 往, 对, 跟, 给; verb + 在 / 给 / 到", ["HSK2-08-26", "HSK2-08-27", "HSK2-08-28",
                                                                 "NEW:gen-dui", "HSK2-11b-09-01", "HSK2-11b-09-02",
                                                                 "HSK2-11b-09-03"]),
        ("Linking words: 因为…所以, 但是, 如果…就, 先…然后, 又…又, 以前 / 的时候", [
            "HSK2-09-29", "HSK2-09-30", "HSK2-09-31", "HSK2-09-32", "HSK2-11b-04-03", "HSK2-09-33",
            "HSK2-11b-04-01", "HSK2-11b-08-01", "HSK2-11b-08-02", "HSK2-11b-08-04"]),
        ("Quantity and determiners: 每, 别的, 自己, 第, 多, 半, 一点儿, measure words", [
            "HSK2-10-34", "HSK2-10-35", "HSK2-11b-09-04", "HSK2-11b-09-05", "HSK2-11b-11-03", "HSK2-10-36",
            "HSK2-11b-10", "HSK2-10-37", "HSK2-11b-01", "HSK2-11b-04-02"]),
    ],
    "HSK3": [
        ("把 and 被", ["HSK3-01-01", "HSK3-01-02", "HSK3-01-03"]),
        ("Result and potential complements", ["HSK3-10b-03", "HSK3-02-04", "HSK3-10b-05", "HSK3-02-05",
                                              "NEW:nabudong"]),
        ("Direction complements: compound, figurative, object position", ["HSK3-03-06", "HSK3-10b-04",
                                                                          "HSK3-03-07", "NEW:qilai-chulai"]),
        ("的 / 得 / 地, degree complements and reduplication", ["HSK3-04-08", "HSK3-04-09", "HSK3-10b-06",
                                                              "HSK3-04-10"]),
        ("Linking words: 虽然, 不但, 一边, 一…就, 只要 / 只有, 结果", ["HSK3-05-11", "HSK3-05-12", "HSK3-05-13",
                                                            "HSK3-05-14", "HSK3-05-15", "HSK3-10b-10-03",
                                                            "HSK3-10b-10-04"]),
        ("Linking words: 除了, 连, 越…越, 要是 / …的话, 不是…就是", ["HSK3-06-16", "HSK3-06-17", "HSK3-06-18",
                                                          "HSK3-06-19", "HSK3-10b-08-04", "HSK3-06-20"]),
        ("Comparison: 比…得, 多了, 像…一样, 不如", ["HSK3-07-21", "HSK3-07-22", "HSK3-10b-02-04", "HSK3-07-23",
                                            "NEW:buru"]),
        ("Adverbs and duration of not doing", ["HSK3-08-24", "HSK3-08-25", "HSK3-10b-07-05", "HSK3-10b-07-06",
                                               "HSK3-10b-07-07", "HSK3-10b-08-05", "HSK3-10b-08-06", "HSK3-08-26"]),
        ("Question words as indefinites, 不是…吗, 着 and existence sentences", [
            "HSK3-09-27", "HSK3-10b-08-02", "HSK3-09-28", "HSK3-10b-11"]),
        ("Prepositions and verb frames: 向, 朝, 替, 用, 请, 好 / 难 + verb", [
            "HSK3-10b-07-01", "HSK3-10b-07-02", "HSK3-10b-07-03", "HSK3-10b-07-04", "HSK3-10b-08-01",
            "HSK3-10b-10-01", "HSK3-10b-10-02"]),
        ("Measure words and quantifiers", ["HSK3-10b-01", "HSK3-10b-02-01", "HSK3-10b-02-02", "HSK3-10b-02-03",
                                           "HSK3-10b-09", "HSK3-10b-08-03"]),
    ],
    "HSK4": [
        ("Concession and conditions: 不管, 即使, 既然, 尽管, 否则, 除非, 再…也", [
            "HSK4-01-01", "HSK4-01-02", "NEW:suiran-jishi", "HSK4-01-03", "HSK4-01-04", "HSK4-01-05",
            "HSK4-10b-05-02"]),
        ("Contrast and attitude adverbs: 却, 并, 竟然, 难道, 反而, 可, 怪不得", [
            "HSK4-02-06", "HSK4-10b-05-03", "HSK4-10b-07-01", "HSK4-10b-07-02", "HSK4-10b-07-03"]),
        ("More adverbs: 尤其, 原来, 恐怕, 果然, 渐渐, 尽量…; 往往 vs 常常", [
            "HSK4-03-07", "HSK4-03-08", "NEW:changchang-future", "HSK4-10b-06", "HSK4-10b-05-05",
            "HSK4-10b-07-05"]),
        ("Prepositions: 关于 / 对于, 由于, 随着, 按照, 通过, 自从, 趁, 沿着", [
            "HSK4-04-09", "HSK4-04-10", "HSK4-10b-04"]),
        ("Causative, passive and purpose: 使 / 令, 叫 / 被…给, 由, 为了 vs 因为", [
            "HSK4-05-11", "HSK4-10b-03-02", "HSK4-10b-03-03", "HSK4-05-13", "HSK4-05-12"]),
        ("Formal linking words: 以及, 而, 于是, 因此, 总之, 首先", ["HSK4-06-14"]),
        ("Structures: 来 + purpose, 是否, 不得不, 不仅, 一方面, 要么, 像…似的", [
            "HSK4-07-15", "HSK4-10b-08-04", "HSK4-10b-08-05", "HSK4-10b-03-01", "HSK4-10b-05-01",
            "HSK4-10b-05-04", "HSK4-10b-07-04"]),
        ("Quantity, measure words and time: 左右, 以上, 之一, 分之, 倍, 以来", [
            "HSK4-08-16", "HSK4-10b-08-01", "HSK4-10b-08-02", "HSK4-10b-08-03", "HSK4-10b-01"]),
        ("Complements: 下去, 下来, 起来, 出来, 住, 上, 开, 过来 / 过去", ["HSK4-09-17", "HSK4-10b-02"]),
    ],
    "HSK5": [
        ("Preference: 与其…不如, 宁可…也", ["HSK5-01-01", "HSK5-01-02"]),
        ("Escalation: 何况, 更不用说, 况且, 乃至", ["HSK5-02-03"]),
        ("Purpose and avoidance: 以便, 以免, 免得, 省得", ["HSK5-03-04", "HSK6-09b-01-09"]),
        ("Hypotheses and concession: 假如, 万一, 即便, 固然, 就算, 要不是", ["HSK5-04-05", "HSK5-09b-02"]),
        ("Adverbs: judgement, time and manner", ["HSK5-05-06", "HSK5-09b-04"]),
        ("Formal verb frames: 加以, 予以, 进行, 受到, 作为, 为…所", ["HSK5-06-07"]),
        ("Written linking words: 便, 即, 从而, 此外, 再说, 一来…二来", ["HSK5-07-08", "HSK5-09b-05"]),
        ("Correlatives and frames: 一旦, 凡是, 不是…而是, 在…看来, 与…相比", ["HSK5-08-09", "HSK5-09b-03"]),
        ("Measure words and vivid reduplication", ["HSK5-09b-01", "HSK5-09b-06"]),
    ],
    "HSK6": [
        ("Literary questions and surprise: 岂, 何尝, 莫非, 何不, 何苦, 不料, 未免", [
            "HSK6-01-01", "HSK6-09b-01-02", "HSK6-09b-01-04", "HSK6-01-02"]),
        ("Result and degree: 以至于, 以致, 毫无, 丝毫", ["HSK6-02-03", "HSK6-02-04"]),
        ("Grounds: 鉴于, 基于, 本着, 出于, 凭", ["HSK6-03-05"]),
        ("Attitude adverbs: 不惜, 务必, 姑且, 势必, 索性, 偏偏, 不妨, 顿时, 一律", [
            "HSK6-04-06", "HSK6-09b-01-03", "HSK6-09b-01-07", "HSK6-09b-01-08", "HSK6-09b-01-10"]),
        ("Classical function words: 之, 其, 所, 者", ["HSK6-05-07", "HSK6-05-08", "HSK6-05-09", "HSK6-09b-01-01",
                                                   "HSK6-05-10"]),
        ("Classical function words: 则, 亦, 皆, 乃, 与, 于, 以…为, 与否, 临", [
            "HSK6-06-11", "HSK6-09b-01-05", "HSK6-06-12", "HSK6-09b-01-06"]),
        ("Set structures: 在于, 非…不可, 无不, 莫过于", ["HSK6-07-13"]),
        ("Discourse markers: 与此同时, 总的来说", ["HSK6-08-14"]),
    ],
    "HSK7-9": [
        ("Literary negation: 勿, 毋庸, 未, 尚未, 并非, 无从, 不得而知", ["HSK79-01-01"]),
        ("Literary pronouns and determiners: 此, 彼此, 该, 本, 某, 何", ["HSK79-02-02"]),
        ("Literary conditions and concessions: 倘若, 若, 若非, 纵然, 唯有, 尚且, 岂止, 一经", [
            "HSK79-03-03", "HSK79-12-01-02"]),
        ("而 and its frames: 因…而, 为…而, 对…而言, 就…而言", ["HSK79-04-04"]),
        ("Four-character frames: 非此即彼, 时…时…, 时而, 或…或…, 自…至…, 不知不觉, 半信半疑", [
            "HSK79-05-05-01", "HSK79-05-05-02", "HSK79-12-01-04", "HSK79-05-05-03", "HSK79-05-05-04",
            "HSK79-05-05-05", "HSK79-05-05-06", "HSK79-05-05-07"]),
        ("Literary adverbs of degree and scope: 颇, 甚为, 尤为, 略, 均, 仅, 唯独, 一概, 屡, 愈…愈, 亟待", [
            "HSK79-06-06-01", "HSK79-06-06-02", "HSK79-06-06-03", "HSK79-06-06-04", "HSK79-06-06-05",
            "HSK79-06-06-06", "HSK79-06-06-07", "HSK79-12-01-03", "HSK79-06-06-08", "HSK79-06-06-09",
            "HSK79-06-06-10"]),
        ("Formal connectives: 进而, 继而, 随即, 加之, 故, 反之, 综上所述, 换言之, 简言之", [
            "HSK79-07-07-01", "HSK79-07-07-02", "HSK79-12-01-06", "HSK79-12-01-01", "HSK79-07-07-03",
            "HSK79-07-07-04", "HSK79-07-07-05", "HSK79-07-07-06", "HSK79-07-07-07"]),
        ("Formal verbs: 取决于, 源于, 致力于, 旨在, 有待, 堪称, 可谓, 犹如, 不失为, 归功于, 归咎于, 致以", [
            "HSK79-08-08-01", "HSK79-08-08-02", "HSK79-08-08-03", "HSK79-08-08-04", "HSK79-08-08-05",
            "HSK79-08-08-06", "HSK79-08-08-07", "HSK79-12-01-05", "HSK79-08-08-08", "HSK79-08-08-09",
            "HSK79-08-08-10", "HSK79-08-08-11"]),
        ("Involuntary reactions and impossibility: 不禁, 不由得, 毫不 vs 毫无, 无可, 难以", ["HSK79-09-09"]),
        ("Classical particles in modern prose: 以, 于, 者, 何以, 而已", ["HSK79-10-10"]),
        ("Essay framing: 诚然, 众所周知, 不言而喻, 显而易见, 毋宁说", ["HSK79-11-11"]),
        ("Literary measure words: 盏, 栋, 枚, 股", ["HSK79-12-01-07", "HSK79-12-01-08", "HSK79-12-01-09",
                                               "HSK79-12-01-10"]),
    ],
    "Usage extras (beyond HSK)": [
        ("Colloquial and regional constructions", ["BH-02b-01", "BH-02b-02"]),
        ("Common learner errors", ["BH-05-01", "NEW:zai-zai", "NEW:he-ranhou", "NEW:ma-ne"]),
    ],
}

# New cards: text, translation, topic tag (level segment filled in automatically).
NEW = {
    "liang-dian": ("现在{{c1::两::二 or 两?}}点。", "It's two o'clock.", "clock"),
    "yao-xiang": ("我{{c1::要::想 or 要?}}这个，不要那个。", "I want this one, not that one.", "yao-xiang"),
    "xiang-miss": ("我很{{c1::想::想 or 要?}}妈妈。", "I really miss my mum.", "yao-xiang"),
    "zai-zhe": ("(An action in progress) 他{{c1::在::在 or 着?}}洗澡，现在不能接电话。",
                "He's in the shower, so he can't come to the phone.", "zai-zhe"),
    "buyong-dei": ("明天是周末，你{{c1::不用::得 (děi) · negative}}早起。",
                   "It's the weekend tomorrow, so you don't have to get up early.", "modals-2"),
    "mei-neng": ("昨天我有事，{{c1::没能::能 · past, negative}}去参加他的生日聚会。",
                 "Something came up yesterday, so I couldn't make it to his birthday party.", "modals-2"),
    "gen-dui": ("明天我{{c1::跟::跟 or 对?}}朋友见面。", "I'm meeting a friend tomorrow.", "preps"),
    "nabudong": ("(Too heavy) 这个箱子太重了，我{{c1::拿不动::拿不动 or 不能拿?}}。",
                 "This case is too heavy — I can't lift it.", "potential-neng"),
    "qilai-chulai": ("他叫什么来着？我一下子想不{{c1::起来::起来 or 出来?}}了。",
                     "What's his name again? It's gone right out of my head.", "figurative-dir"),
    "buru": ("这家饭馆的菜{{c1::不如::not as … as (A … B + adj)}}那家好吃。",
             "The food in this restaurant isn't as good as in that one.", "buru"),
    "suiran-jishi": ("(It really happened) {{c1::虽然::虽然 or 即使?}}他道了歉，我还是很生气。",
                     "Although he apologised, I'm still angry.", "jishi"),
    "changchang-future": ("(A promise about the future) 以后我会{{c1::常常::常常 or 往往?}}回来看你们。",
                          "I'll come back and see you all often.", "wangwang"),
    "zai-zai": ("(Writing a note) 你明天{{c1::再::在 or 再?}}来一次吧。",
                "Come back again tomorrow.", "errors"),
    "he-ranhou": ("我吃了饭，{{c1::然后::和 or 然后?}}看了一会儿电视。",
                  "I had dinner and then watched a bit of TV.", "errors"),
    "ma-ne": ("你周末去哪儿{{c1::呢::吗 or 呢?}}？", "Where are you off to at the weekend?", "errors"),
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
            deck = f"Cloze Grammar::Chinese::{level}::{ch_no:02d} {ch_name}"
            members = []
            for item in items:
                if item.startswith("NEW:"):
                    key = item[4:]
                    text, tr, topic = NEW[key]
                    if key not in new_guids:
                        new_guids[key] = "".join(rng.choice(GUID_ALPHABET) for _ in range(10))
                    members.append({"guid": new_guids[key], "old_id": None, "new_key": key, "text": text,
                                    "tr": tr, "topic": f"Chinese::{tagseg}::grammar::{topic}"})
                    continue
                ids = [k for k in by_old if k == item or k.startswith(item + "-")]
                assert ids, f"nothing matches {item}"
                for k in ids:
                    assert k not in used, f"{k} used twice"
                    used.add(k)
                    r = by_old[k]
                    # Re-point the level segment of the topic tag(s) at the new level.
                    topic = " ".join(
                        "::".join([t.split("::")[0], tagseg] + t.split("::")[2:])
                        if t.split("::")[2:3] == ["grammar"] else t
                        for t in r["topic"].split())
                    members.append({"guid": r["guid"], "old_id": k, "new_key": None, "text": r["text"],
                                    "tr": r["tr"], "topic": topic})
            for n, m in enumerate(members, 1):
                m["sort_id"] = f"ZH-{code}-{ch_no:02d}-{n:03d}"
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
