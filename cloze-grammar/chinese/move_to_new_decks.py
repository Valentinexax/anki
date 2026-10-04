# Paste into Anki's Debug Console (Tools > Debug Console, or Ctrl+Shift+;) and press Ctrl+Enter.
# Moves every Chinese cloze-grammar card into the chapter deck its Sort ID belongs to,
# then removes Chinese chapter decks left empty. Only touches Typecloze notes whose
# Sort ID starts with ZH-; reviews and scheduling are untouched.
DECKS = {
 "ZH-HSK1-01": "Cloze Grammar::Chinese::HSK1::01 是, 有 and 在",
 "ZH-HSK1-02": "Cloze Grammar::Chinese::HSK1::02 Pronouns, 这 / 那, 的, 叫 / 姓",
 "ZH-HSK1-03": "Cloze Grammar::Chinese::HSK1::03 Questions",
 "ZH-HSK1-04": "Cloze Grammar::Chinese::HSK1::04 Numbers, money and measure words",
 "ZH-HSK1-05": "Cloze Grammar::Chinese::HSK1::05 Dates and time",
 "ZH-HSK1-06": "Cloze Grammar::Chinese::HSK1::06 Adverbs: 不 / 没, 很, 太…了, 也, 都, 一起",
 "ZH-HSK1-07": "Cloze Grammar::Chinese::HSK1::07 Modal verbs; 喜欢; 认识 vs 知道",
 "ZH-HSK1-08": "Cloze Grammar::Chinese::HSK1::08 Place: 在 + place, location words",
 "ZH-HSK1-09": "Cloze Grammar::Chinese::HSK1::09 Particles: 了, 吧, 呢",
 "ZH-HSK2-01": "Cloze Grammar::Chinese::HSK2::01 Aspect: 过, 着, 正在; negating 了",
 "ZH-HSK2-02": "Cloze Grammar::Chinese::HSK2::02 Complements: result, degree (得), direction",
 "ZH-HSK2-03": "Cloze Grammar::Chinese::HSK2::03 Duration, frequency, 一下 and reduplication",
 "ZH-HSK2-04": "Cloze Grammar::Chinese::HSK2::04 Comparison: 比, 没有, 一样, 更, 最",
 "ZH-HSK2-05": "Cloze Grammar::Chinese::HSK2::05 Questions: A-不-A, 还是 vs 或者, 为什么 / 怎么",
 "ZH-HSK2-06": "Cloze Grammar::Chinese::HSK2::06 Sentence patterns: 是…的, 要…了, serial verbs, 让",
 "ZH-HSK2-07": "Cloze Grammar::Chinese::HSK2::07 Modal verbs: 应该, 得, 敢, 愿意, 不用",
 "ZH-HSK2-08": "Cloze Grammar::Chinese::HSK2::08 Adverbs: 再 / 又, 就 / 才, 还, 已经, 别, 只",
 "ZH-HSK2-09": "Cloze Grammar::Chinese::HSK2::09 Prepositions: 从…到, 离, 往, 对, 跟, 给; verb + 在 / 给 / 到",
 "ZH-HSK2-10": "Cloze Grammar::Chinese::HSK2::10 Linking words: 因为…所以, 但是, 如果…就, 先…然后, 又…又, 以前 / 的时候",
 "ZH-HSK2-11": "Cloze Grammar::Chinese::HSK2::11 Quantity and determiners: 每, 别的, 自己, 第, 多, 半, 一点儿, measure words",
 "ZH-HSK3-01": "Cloze Grammar::Chinese::HSK3::01 把 and 被",
 "ZH-HSK3-02": "Cloze Grammar::Chinese::HSK3::02 Result and potential complements",
 "ZH-HSK3-03": "Cloze Grammar::Chinese::HSK3::03 Direction complements: compound, figurative, object position",
 "ZH-HSK3-04": "Cloze Grammar::Chinese::HSK3::04 的 / 得 / 地, degree complements and reduplication",
 "ZH-HSK3-05": "Cloze Grammar::Chinese::HSK3::05 Linking words: 虽然, 不但, 一边, 一…就, 只要 / 只有, 结果",
 "ZH-HSK3-06": "Cloze Grammar::Chinese::HSK3::06 Linking words: 除了, 连, 越…越, 要是 / …的话, 不是…就是",
 "ZH-HSK3-07": "Cloze Grammar::Chinese::HSK3::07 Comparison: 比…得, 多了, 像…一样, 不如",
 "ZH-HSK3-08": "Cloze Grammar::Chinese::HSK3::08 Adverbs and duration of not doing",
 "ZH-HSK3-09": "Cloze Grammar::Chinese::HSK3::09 Question words as indefinites, 不是…吗, 着 and existence sentences",
 "ZH-HSK3-10": "Cloze Grammar::Chinese::HSK3::10 Prepositions and verb frames: 向, 朝, 替, 用, 请, 好 / 难 + verb",
 "ZH-HSK3-11": "Cloze Grammar::Chinese::HSK3::11 Measure words and quantifiers",
 "ZH-HSK4-01": "Cloze Grammar::Chinese::HSK4::01 Concession and conditions: 不管, 即使, 既然, 尽管, 否则, 除非, 再…也",
 "ZH-HSK4-02": "Cloze Grammar::Chinese::HSK4::02 Contrast and attitude adverbs: 却, 并, 竟然, 难道, 反而, 可, 怪不得",
 "ZH-HSK4-03": "Cloze Grammar::Chinese::HSK4::03 More adverbs: 尤其, 原来, 恐怕, 果然, 渐渐, 尽量…; 往往 vs 常常",
 "ZH-HSK4-04": "Cloze Grammar::Chinese::HSK4::04 Prepositions: 关于 / 对于, 由于, 随着, 按照, 通过, 自从, 趁, 沿着",
 "ZH-HSK4-05": "Cloze Grammar::Chinese::HSK4::05 Causative, passive and purpose: 使 / 令, 叫 / 被…给, 由, 为了 vs 因为",
 "ZH-HSK4-06": "Cloze Grammar::Chinese::HSK4::06 Formal linking words: 以及, 而, 于是, 因此, 总之, 首先",
 "ZH-HSK4-07": "Cloze Grammar::Chinese::HSK4::07 Structures: 来 + purpose, 是否, 不得不, 不仅, 一方面, 要么, 像…似的",
 "ZH-HSK4-08": "Cloze Grammar::Chinese::HSK4::08 Quantity, measure words and time: 左右, 以上, 之一, 分之, 倍, 以来",
 "ZH-HSK4-09": "Cloze Grammar::Chinese::HSK4::09 Complements: 下去, 下来, 起来, 出来, 住, 上, 开, 过来 / 过去",
 "ZH-HSK5-01": "Cloze Grammar::Chinese::HSK5::01 Preference: 与其…不如, 宁可…也",
 "ZH-HSK5-02": "Cloze Grammar::Chinese::HSK5::02 Escalation: 何况, 更不用说, 况且, 乃至",
 "ZH-HSK5-03": "Cloze Grammar::Chinese::HSK5::03 Purpose and avoidance: 以便, 以免, 免得, 省得",
 "ZH-HSK5-04": "Cloze Grammar::Chinese::HSK5::04 Hypotheses and concession: 假如, 万一, 即便, 固然, 就算, 要不是",
 "ZH-HSK5-05": "Cloze Grammar::Chinese::HSK5::05 Adverbs: judgement, time and manner",
 "ZH-HSK5-06": "Cloze Grammar::Chinese::HSK5::06 Formal verb frames: 加以, 予以, 进行, 受到, 作为, 为…所",
 "ZH-HSK5-07": "Cloze Grammar::Chinese::HSK5::07 Written linking words: 便, 即, 从而, 此外, 再说, 一来…二来",
 "ZH-HSK5-08": "Cloze Grammar::Chinese::HSK5::08 Correlatives and frames: 一旦, 凡是, 不是…而是, 在…看来, 与…相比",
 "ZH-HSK5-09": "Cloze Grammar::Chinese::HSK5::09 Measure words and vivid reduplication",
 "ZH-HSK6-01": "Cloze Grammar::Chinese::HSK6::01 Literary questions and surprise: 岂, 何尝, 莫非, 何不, 何苦, 不料, 未免",
 "ZH-HSK6-02": "Cloze Grammar::Chinese::HSK6::02 Result and degree: 以至于, 以致, 毫无, 丝毫",
 "ZH-HSK6-03": "Cloze Grammar::Chinese::HSK6::03 Grounds: 鉴于, 基于, 本着, 出于, 凭",
 "ZH-HSK6-04": "Cloze Grammar::Chinese::HSK6::04 Attitude adverbs: 不惜, 务必, 姑且, 势必, 索性, 偏偏, 不妨, 顿时, 一律",
 "ZH-HSK6-05": "Cloze Grammar::Chinese::HSK6::05 Classical function words: 之, 其, 所, 者",
 "ZH-HSK6-06": "Cloze Grammar::Chinese::HSK6::06 Classical function words: 则, 亦, 皆, 乃, 与, 于, 以…为, 与否, 临",
 "ZH-HSK6-07": "Cloze Grammar::Chinese::HSK6::07 Set structures: 在于, 非…不可, 无不, 莫过于",
 "ZH-HSK6-08": "Cloze Grammar::Chinese::HSK6::08 Discourse markers: 与此同时, 总的来说",
 "ZH-HSK79-01": "Cloze Grammar::Chinese::HSK7-9::01 Literary negation: 勿, 毋庸, 未, 尚未, 并非, 无从, 不得而知",
 "ZH-HSK79-02": "Cloze Grammar::Chinese::HSK7-9::02 Literary pronouns and determiners: 此, 彼此, 该, 本, 某, 何",
 "ZH-HSK79-03": "Cloze Grammar::Chinese::HSK7-9::03 Literary conditions and concessions: 倘若, 若, 若非, 纵然, 唯有, 尚且, 岂止, 一经",
 "ZH-HSK79-04": "Cloze Grammar::Chinese::HSK7-9::04 而 and its frames: 因…而, 为…而, 对…而言, 就…而言",
 "ZH-HSK79-05": "Cloze Grammar::Chinese::HSK7-9::05 Four-character frames: 非此即彼, 时…时…, 时而, 或…或…, 自…至…, 不知不觉, 半信半疑",
 "ZH-HSK79-06": "Cloze Grammar::Chinese::HSK7-9::06 Literary adverbs of degree and scope: 颇, 甚为, 尤为, 略, 均, 仅, 唯独, 一概, 屡, 愈…愈, 亟待",
 "ZH-HSK79-07": "Cloze Grammar::Chinese::HSK7-9::07 Formal connectives: 进而, 继而, 随即, 加之, 故, 反之, 综上所述, 换言之, 简言之",
 "ZH-HSK79-08": "Cloze Grammar::Chinese::HSK7-9::08 Formal verbs: 取决于, 源于, 致力于, 旨在, 有待, 堪称, 可谓, 犹如, 不失为, 归功于, 归咎于, 致以",
 "ZH-HSK79-09": "Cloze Grammar::Chinese::HSK7-9::09 Involuntary reactions and impossibility: 不禁, 不由得, 毫不 vs 毫无, 无可, 难以",
 "ZH-HSK79-10": "Cloze Grammar::Chinese::HSK7-9::10 Classical particles in modern prose: 以, 于, 者, 何以, 而已",
 "ZH-HSK79-11": "Cloze Grammar::Chinese::HSK7-9::11 Essay framing: 诚然, 众所周知, 不言而喻, 显而易见, 毋宁说",
 "ZH-HSK79-12": "Cloze Grammar::Chinese::HSK7-9::12 Literary measure words: 盏, 栋, 枚, 股",
 "ZH-UX-01": "Cloze Grammar::Chinese::Usage extras (beyond HSK)::01 Colloquial and regional constructions",
 "ZH-UX-02": "Cloze Grammar::Chinese::Usage extras (beyond HSK)::02 Common learner errors"
}

nt = mw.col.models.by_name("Typecloze")
moved = 0
for nid in mw.col.find_notes('"note:Typecloze" "Sort ID:ZH-*"'):
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
    if d.name.startswith("Cloze Grammar::Chinese::") and d.name not in DECKS.values() \
            and not mw.col.decks.card_count(d.id, include_subdecks=True):
        mw.col.decks.remove([d.id])
        removed.append(d.name)
try:
    mw.reset()
except Exception:
    pass
print(f"moved {moved} cards; removed {len(removed)} empty decks")
