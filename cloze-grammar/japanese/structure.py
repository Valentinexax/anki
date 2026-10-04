"""Chapter plan: folds Supplement chapters into thematic chapters (Japanese names), inserts
new cards and assigns new sort IDs. Writes work/structure.json.

Each chapter lists items in order: an old chapter or group prefix ("N5-01" takes every card
in chapter 01, "N4-12-03" every card in that group), a single old card ID ("N4-12-03-01"),
or "NEW:key".
"""
import json
import random
import string
from pathlib import Path

HERE = Path(__file__).parent
WORK = HERE / "work"

# Level name in the deck path -> (sort-ID code, tag segment)
LEVELS = {
    "N5": ("N5", "N5"), "N4": ("N4", "N4"), "N3": ("N3", "N3"), "N2": ("N2", "N2"), "N1": ("N1", "N1"),
    # Kanji sort after Latin letters in Anki's deck list, so this comes after N5.
    "番外（JLPT範囲外）": ("EX", "Beyond-JLPT"),
}
ROOT = "Cloze Grammar::Japanese"

PLAN = {
    "N5": [
        ("「です」と基本の助詞", ["N5-01"]),
        ("指示詞と疑問詞", ["N5-02"]),
        ("丁寧形の動詞、「たい」「ほしい」、誘い", ["N5-03"]),
        ("助詞と存在（ある・いる）", ["N5-04"]),
        ("形容詞", ["N5-05"]),
        ("て形の文型", ["N5-06"]),
        ("普通形と目的の「に」", ["N5-07"]),
        ("接続・比較・その他", ["N5-08"]),
    ],
    "N4": [
        ("普通体・引用・説明・命令", ["N4-01", "N4-12-01", "N4-12-02"]),
        ("可能", ["N4-02"]),
        ("条件と助言", ["N4-03", "N4-12-06", "N4-12-07"]),
        ("意向・決定・変化", ["N4-04", "N4-12-04", "N4-12-05"]),
        ("て形の応用", ["N4-05"]),
        ("授受表現", ["N4-06"]),
        ("様子・伝聞・推量", ["N4-07", "N4-12-03"]),
        ("受身と使役", ["N4-08"]),
        ("理由・目的・時", ["N4-09", "NEW:noni-purpose"]),
        ("経験・連体修飾・複合動詞", ["N4-10", "N4-12-08"]),
        ("敬語の基本", ["N4-11"]),
    ],
    "N3": [
        ("使役受身と丁寧な依頼", ["N3-01"]),
        ("判断と推量", ["N3-02"]),
        ("時とタイミング", ["N3-03", "N3-11-03"]),
        ("条件と逆接", ["N3-04", "NEW:baai"]),
        ("関係を表す表現", ["N3-05", "N3-11-01", "N3-11-02", "NEW:kawarini"]),
        ("程度と強調", ["N3-06"]),
        ("意志・決まり・義務", ["N3-07"]),
        ("伝聞と願望", ["N3-08"]),
        ("原因と結果", ["N3-09"]),
        ("様子・状態・頻度", ["N3-10", "N3-11-04"]),
    ],
    "N2": [
        ("時・継起・変化", ["N2-01", "N2-11-01", "N2-11-06", "N2-11-08"]),
        ("原因・理由・根拠", ["N2-02"]),
        ("逆接と対比", ["N2-03", "NEW:hatomokaku"]),
        ("条件と限定", ["N2-04", "N2-11-04"]),
        ("関係を表す表現", ["N2-05", "N2-11-02", "N2-11-03", "N2-11-05", "N2-11-07"]),
        ("強調と程度", ["N2-06", "NEW:ueni"]),
        ("判断と感情", ["N2-07", "NEW:kotoni"]),
        ("複合動詞と接尾辞", ["N2-08"]),
        ("視点・様子・根拠", ["N2-09"]),
        ("談話と文末表現", ["N2-10"]),
    ],
    "N1": [
        ("時と継起", ["N1-01"]),
        ("原因・理由・根拠", ["N1-02", "N1-10-03", "N1-10-10"]),
        ("逆接と対比", ["N1-03", "N1-10-01", "N1-10-06", "N1-10-07", "N1-10-08", "N1-10-11"]),
        ("限定・条件・範囲", ["N1-04", "NEW:ni-itarumade"]),
        ("程度と強調", ["N1-05", "N1-10-14", "N1-10-15"]),
        ("判断と感情", ["N1-06", "N1-10-02", "N1-10-05", "N1-10-09", "N1-10-12", "N1-10-13", "NEW:toii"]),
        ("書き言葉の関係表現", ["N1-07"]),
        ("様子・状態", ["N1-08", "N1-10-04"]),
        ("文末表現と慣用句", ["N1-09"]),
    ],
    "番外（JLPT範囲外）": [
        ("自動詞と他動詞", ["BJ-01"]),
        ("アスペクト・名詞化・助詞", ["BJ-02"]),
        ("くだけた話し言葉と縮約形", ["BJ-03"]),
        ("終助詞と話し方", ["BJ-04"]),
        ("ビジネス敬語", ["BJ-05"]),
        ("書き言葉", ["BJ-06"]),
        ("古典語の名残", ["BJ-07"]),
        ("関西弁", ["BJ-08"]),
    ],
}

NEW = {
    "noni-purpose": ("このはさみは紙を切る{{c1::のに::for (purpose of use)}}使います。",
                     "These scissors are for cutting paper.", "Japanese::N4::grammar::noni-purpose"),
    "baai": ("雨の{{c1::場合::in the event of (formal)}}、試合は中止です。",
             "In the event of rain, the match will be cancelled.", "Japanese::N3::grammar::baai"),
    "kawarini": ("英語を教える{{c1::かわりに::in exchange for}}、日本語を教えてもらっています。",
                 "In exchange for teaching English, I'm being taught Japanese.", "Japanese::N3::grammar::kawarini"),
    "ueni": ("この店は安い{{c1::うえに::on top of being}}、店員も親切です。",
             "On top of being cheap, this shop has friendly staff.", "Japanese::N2::grammar::ueni"),
    "kotoni": ("{{c1::残念なことに::残念 · I'm sorry to say (feeling first)}}、旅行は中止になりました。",
               "Sadly, the trip has been cancelled.", "Japanese::N2::grammar::kotoni"),
    "hatomokaku": ("見た目{{c1::はともかく::leaving aside}}、味はとてもいいです。",
                   "Looks aside, it tastes very good.", "Japanese::N2::grammar::hatomokaku"),
    "ni-itarumade": ("子どもからお年寄り{{c1::に至るまで::right through to}}、この歌を知らない人はいません。",
                     "Everyone from children right through to the elderly knows this song.", "Japanese::N1::grammar::ni-itarumade"),
    "toii": ("味{{c1::といい::both … and (evaluating)}}、値段{{c1::といい::both … and (evaluating)}}、文句のない店です。",
             "In both taste and price, the restaurant can't be faulted.", "Japanese::N1::grammar::toii"),
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
                                    "tr": tr, "topic": topic})
                    continue
                ids = [k for k in by_old if k == item or k.startswith(item + "-")]
                assert ids, f"nothing matches {item}"
                for k in ids:
                    assert k not in used, f"{k} used twice"
                    used.add(k)
                    r = by_old[k]
                    # Cards keep their level, so the topic tag is unchanged.
                    topic = r["topic"]
                    members.append({"guid": r["guid"], "old_id": k, "new_key": None, "text": r["text"],
                                    "tr": r["tr"], "topic": topic})
            for n, m in enumerate(members, 1):
                m["sort_id"] = f"JP-{code}-{ch_no:02d}-{n:03d}"
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
