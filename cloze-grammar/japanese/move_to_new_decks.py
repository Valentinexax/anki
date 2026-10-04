# Paste into Anki's Debug Console (Tools > Debug Console, or Ctrl+Shift+;) and press Ctrl+Enter.
# Moves every Japanese cloze-grammar card into the chapter deck its Sort ID belongs to,
# then removes Japanese chapter decks left empty. Only touches Typecloze notes whose
# Sort ID starts with JP-; reviews and scheduling are untouched.
DECKS = {
 "JP-N5-01": "Cloze Grammar::Japanese::N5::01 「です」と基本の助詞",
 "JP-N5-02": "Cloze Grammar::Japanese::N5::02 指示詞と疑問詞",
 "JP-N5-03": "Cloze Grammar::Japanese::N5::03 丁寧形の動詞、「たい」「ほしい」、誘い",
 "JP-N5-04": "Cloze Grammar::Japanese::N5::04 助詞と存在（ある・いる）",
 "JP-N5-05": "Cloze Grammar::Japanese::N5::05 形容詞",
 "JP-N5-06": "Cloze Grammar::Japanese::N5::06 て形の文型",
 "JP-N5-07": "Cloze Grammar::Japanese::N5::07 普通形と目的の「に」",
 "JP-N5-08": "Cloze Grammar::Japanese::N5::08 接続・比較・その他",
 "JP-N4-01": "Cloze Grammar::Japanese::N4::01 普通体・引用・説明・命令",
 "JP-N4-02": "Cloze Grammar::Japanese::N4::02 可能",
 "JP-N4-03": "Cloze Grammar::Japanese::N4::03 条件と助言",
 "JP-N4-04": "Cloze Grammar::Japanese::N4::04 意向・決定・変化",
 "JP-N4-05": "Cloze Grammar::Japanese::N4::05 て形の応用",
 "JP-N4-06": "Cloze Grammar::Japanese::N4::06 授受表現",
 "JP-N4-07": "Cloze Grammar::Japanese::N4::07 様子・伝聞・推量",
 "JP-N4-08": "Cloze Grammar::Japanese::N4::08 受身と使役",
 "JP-N4-09": "Cloze Grammar::Japanese::N4::09 理由・目的・時",
 "JP-N4-10": "Cloze Grammar::Japanese::N4::10 経験・連体修飾・複合動詞",
 "JP-N4-11": "Cloze Grammar::Japanese::N4::11 敬語の基本",
 "JP-N3-01": "Cloze Grammar::Japanese::N3::01 使役受身と丁寧な依頼",
 "JP-N3-02": "Cloze Grammar::Japanese::N3::02 判断と推量",
 "JP-N3-03": "Cloze Grammar::Japanese::N3::03 時とタイミング",
 "JP-N3-04": "Cloze Grammar::Japanese::N3::04 条件と逆接",
 "JP-N3-05": "Cloze Grammar::Japanese::N3::05 関係を表す表現",
 "JP-N3-06": "Cloze Grammar::Japanese::N3::06 程度と強調",
 "JP-N3-07": "Cloze Grammar::Japanese::N3::07 意志・決まり・義務",
 "JP-N3-08": "Cloze Grammar::Japanese::N3::08 伝聞と願望",
 "JP-N3-09": "Cloze Grammar::Japanese::N3::09 原因と結果",
 "JP-N3-10": "Cloze Grammar::Japanese::N3::10 様子・状態・頻度",
 "JP-N2-01": "Cloze Grammar::Japanese::N2::01 時・継起・変化",
 "JP-N2-02": "Cloze Grammar::Japanese::N2::02 原因・理由・根拠",
 "JP-N2-03": "Cloze Grammar::Japanese::N2::03 逆接と対比",
 "JP-N2-04": "Cloze Grammar::Japanese::N2::04 条件と限定",
 "JP-N2-05": "Cloze Grammar::Japanese::N2::05 関係を表す表現",
 "JP-N2-06": "Cloze Grammar::Japanese::N2::06 強調と程度",
 "JP-N2-07": "Cloze Grammar::Japanese::N2::07 判断と感情",
 "JP-N2-08": "Cloze Grammar::Japanese::N2::08 複合動詞と接尾辞",
 "JP-N2-09": "Cloze Grammar::Japanese::N2::09 視点・様子・根拠",
 "JP-N2-10": "Cloze Grammar::Japanese::N2::10 談話と文末表現",
 "JP-N1-01": "Cloze Grammar::Japanese::N1::01 時と継起",
 "JP-N1-02": "Cloze Grammar::Japanese::N1::02 原因・理由・根拠",
 "JP-N1-03": "Cloze Grammar::Japanese::N1::03 逆接と対比",
 "JP-N1-04": "Cloze Grammar::Japanese::N1::04 限定・条件・範囲",
 "JP-N1-05": "Cloze Grammar::Japanese::N1::05 程度と強調",
 "JP-N1-06": "Cloze Grammar::Japanese::N1::06 判断と感情",
 "JP-N1-07": "Cloze Grammar::Japanese::N1::07 書き言葉の関係表現",
 "JP-N1-08": "Cloze Grammar::Japanese::N1::08 様子・状態",
 "JP-N1-09": "Cloze Grammar::Japanese::N1::09 文末表現と慣用句",
 "JP-EX-01": "Cloze Grammar::Japanese::番外（JLPT範囲外）::01 自動詞と他動詞",
 "JP-EX-02": "Cloze Grammar::Japanese::番外（JLPT範囲外）::02 アスペクト・名詞化・助詞",
 "JP-EX-03": "Cloze Grammar::Japanese::番外（JLPT範囲外）::03 くだけた話し言葉と縮約形",
 "JP-EX-04": "Cloze Grammar::Japanese::番外（JLPT範囲外）::04 終助詞と話し方",
 "JP-EX-05": "Cloze Grammar::Japanese::番外（JLPT範囲外）::05 ビジネス敬語",
 "JP-EX-06": "Cloze Grammar::Japanese::番外（JLPT範囲外）::06 書き言葉",
 "JP-EX-07": "Cloze Grammar::Japanese::番外（JLPT範囲外）::07 古典語の名残",
 "JP-EX-08": "Cloze Grammar::Japanese::番外（JLPT範囲外）::08 関西弁",
}

nt = mw.col.models.by_name("Typecloze")
moved = 0
for nid in mw.col.find_notes('"note:Typecloze" "Sort ID:JP-*"'):
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
    if d.name.startswith("Cloze Grammar::Japanese::") and d.name not in DECKS.values() \
            and not mw.col.decks.card_count(d.id, include_subdecks=True):
        mw.col.decks.remove([d.id])
        removed.append(d.name)
try:
    mw.reset()
except Exception:
    pass
print(f"moved {moved} cards; removed {len(removed)} empty decks")
