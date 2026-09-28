---
title: Kryptos K4
description: Jim Sanbornの彫刻Kryptosの未解読部分K4を、監査を優先して調べる研究の概要です。
lang: ja
---

K4は、Jim Sanbornが1990年にCIA本部へ設置した彫刻 *Kryptos* の第4部で、97文字の暗号文です。平文のうち24文字（`EASTNORTHEAST` と `BERLINCLOCK`）が公開されています。2025年に平文が資料の中から見つかりましたが、公開されておらず、暗号化の方法も明かされていません。正解は存在し、伏せられている状態です。

この研究はK4を解いたとは主張しません。公開された証拠でどの暗号の族を否定できるか、主張されたパターンが、探した側の自由度を払った後にどれだけの価値を持つか、そしてcribではそもそも答えられない問いはどれかを記録します。

## 問い

97文字の暗号文と24文字のcribで、どの仕組みを否定できるか。見つけるのに使った自由度を数えた後で、生き残るパターンはどれか。

## 証拠の種類

使うのは公開された暗号文とcribだけです。Noteで事前封印を明記していない検定は、すべて探索的です。「否定」は、述べた範囲のどの設定もcribを再現せず、しかも陽性対照（既知の鍵で作った暗号文）で検定が当たりを見つけられることを確かめた、という意味です。「区別できない」は、族の自由度が24文字で拘束できる量を超えているという意味で、否定ではありません。

## これまでの進展

最初は、外から持ち込まれた主張の値段を測りました。「K4はprimer 57973の反転Gromark暗号」という主張は、数値は再現しますが公開cribでは偶然と区別できません（EP-0001）。Wの間隔を `TOKIO` と読むパターンは、世界時計の地名リストに対して p ≤ 1.5×10⁻³ で通りましたが（EP-0011）、後にK4を見る前に考えられた6つの標的リストまで払うと、偶然の期待は0.054で、偶然と両立しました（[EP-0135](/ja/research/kryptos-k4-list-price/)）。

そのあと、K1〜K3と同じ「1枚の表のずらし」の形（周期鍵、running key、mask、彫り間違い、物理的な鍵）を広く調べ、判定できる族はすべて候補なしか、cribでは判定できないかのどちらかでした。K4の文字頻度は平らで、鍵は1位置あたり3 bit以上が要ります。

2026-09-26からは、その形を外した別方式を調べました。2文字の方陣、Hill、Slidefair・Portax・Doppelkasten、ロータ機、Enigma型の機械、そして族を人が1つずつ選ぶのをやめて部品の文法から作った4.7×10¹⁵手順の列挙器です（[EP-0119](/ja/research/kryptos-k4-procedure-enumerator/)）。判定できる範囲では、どれもcribと両立しませんでした。ただし、でたらめな暗号文もたいてい同じく通らないので、K4がでたらめより起きにくいとは言えません。

族ごとの結果は **[調べた族の一覧](/ja/programs/kryptos-k4/families)** にまとめています。

## 2026-09-28時点の整理

- **検証できたこと**：短く書ける手順がcrib 24文字と両立するか、だけです。答えはこれまですべて「両立しない」でした。どれも論理的な反証で、K4がでたらめより起きにくいと示したものはありません。新しい平文文字は0です。
- **鍵の大きさの下限**：K4の文字頻度は平らで、1位置あたり3 bit以上の鍵が要ります（[EP-0091](/ja/research/kryptos-k4-key-bound/)）。これは英語の冗長度（約2.86 bit）より大きいので、1文字ずつ自由に選んだ鍵はK4だけでは決まりません。K4が解ける形は「短い技法」と「短く書ける鍵の出どころ」の組に限られます。これは、技法が分かれば残りはpuzzleだ、というScheidtの発言とも同じ向きです。
- **判定できないもの**：手製の表、同音換字、2文字の表、符号帳、配線が自由な複数ロータは、cribで拘束できる量より自由度が大きく、判定には表・装置・K5の出どころが外から要ります。「鍵や表が位置ごとに手で選ばれた」という仮説は、観察されたすべての特徴を説明でき、公開データではK4を決められないと予測します。これは仮説で、結論ではありません。
- **鍵の出どころ**：2026-09-26に計画した「鍵の出どころと表を分ける」検定では、ラテン方格の表について、支持される出どころはありませんでした。
- **研究の担当者との検討で立てた案（2026-09-27）**：語の中で文字を並べ替えてから、または換字してから並べ替える形（[EP-0137](/ja/research/kryptos-k4-word-reordering/)）、2つのOの区間を対にした2文字暗号（[EP-0138](/ja/research/kryptos-k4-o-pairs/)）、しっかりした方式に手を加えた場合に要る、cribの誤りを7文字まで許す列挙器（[EP-0119](/ja/research/kryptos-k4-procedure-enumerator/)）。どれも0件で、論理的な反証です。
- **「物理」の3層**：設置の物理（完成した彫刻の太陽・影・向き）、制作の幾何（K4を机の上で作った工程）、復号後の物理（平文の指示を現地で行う）を分けて扱うようにしました。これまでの物理の検定は、ほとんどが1層目です。2層目では、制作・施工の事実が決める演算子は少なく、1つは否定、残りは判定できません（[EP-0140](/ja/research/kryptos-k4-construction-ledger/)）。K1〜K3の刻まれた配置は字幅で決まっていて、分かっている方式の痕跡を残していないので、K4の配置を手がかりに読む族は陽性対照が取れません（[EP-0141](/ja/research/kryptos-k4-production-traces/)）。行14の3文字のずれは、写真2枚で判定が食い違い、決まっていません（[EP-0139](/ja/research/kryptos-k4-yar-photo/)）。

## 彫刻の物理記録と3D模型（2026-09-25）

鍵が文字ではなく彫刻そのものの形から来る可能性を調べるため、公開写真と航空写真から、彫刻の物理的な情報を推定して3D模型にしました（v0.5）。銅板の組み方（4枚が2×2で、横の継ぎ目がK2とK3の境と一致）、S字の形、方位（暗号文側がおおむね南）、珪化木の太さ、入口のMorse（K0）が刻まれた3つの石の配置を含みます。ラングレーの日付と時刻を選ぶと、太陽の位置から、切り抜いた文字の光が床に落ちる様子を見られます。

v0.5では、写真の文字にカメラと円筒を当てはめて列の間隔を測り直し、両端の間が公表の幅20 ft（6.1 m）になるようにしました。入口のMorseの穴は写真で測った比率で描き、コンパス図の向きも写真から測り直しました。v0.5.1では、入口のMorseの7句すべてを写真と点・線ごとに照合し（転記と一致）、字の間と語の間を写真3枚から測った値にしました。画面は日本語と英語を切り替えられ、模型をglTF（.glb）で、K4の97文字の物理量をCSVで保存できます。

寸法と方位のほとんどは推定（確度C）で、目安です。模型の形はcribを見ずに写真だけで決めました。研究用の計算は、形の不確かさの範囲（半径1.4〜2.4 mなど）全体で回しています。公開版では、K4の97文字とMorseの7句のほかは彫刻の文字を伏せ、切り抜きの位置だけを示しています。

**[3D模型を開く →](https://kbmt327-dev.github.io/scientific-os-research/static/kryptos-k4-model.html)**（日本語／English）

<!-- GENERATED: program-current:START -->
## 現在の公開結論

復号はしていません。新しい平文文字は0です（2026-09-28時点）。検証できたのは「短く書ける手順がcrib 24文字と両立するか」だけで、答えはすべて「両立しない」でした。K1〜K3と同じ「1枚の表のずらし」の形に加え、それを外した別方式（2文字の方陣、Hill、Slidefair・Portax・Doppelkasten、ロータ機、Enigma型＋前段の置換）や、部品の文法から作った4.7×10¹⁵手順の列挙器も、判定できる範囲では候補なしでした。列挙器はcribの誤りを7文字まで許しても、語の中の並べ替えを許しても0件です。どれも論理的な反証で、でたらめより起きにくいとは言えません。K4の文字頻度は平らなので鍵は1位置あたり3 bit以上が要り、手製の表・同音・符号帳などは、表や装置、K5の出どころがなければ判定できません。W区間をTOKIOと読むパターンは、標的リストを選ぶ自由まで払うと偶然と両立します（期待0.054、EP-0135）。彫刻の制作・施工の事実から決まる演算子は、判定できないか否定され、K1〜K3の配置は字幅で決まっていて方式の痕跡を残していません（EP-0140、EP-0141）。

**証拠の境界：** 公開暗号文と24文字のcrib、彫刻の公開写真を使った探索的な計算です。後半の検定の多くはK4に回す前にコミットしましたが、外部の事前登録はなく、外部の独立replicationも暗号専門家のレビューもありません。正解は存在しますが公開されていません。

**[現在のResearch Note（EP-0141）を読む →](/ja/research/kryptos-k4-production-traces/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## 公開中のResearch Note

1. [[ja/research/kryptos-k4-57973-audit/index|EP-0001 — modelの自由度を数えても、primer 57973は際立つか]]
2. [[ja/research/kryptos-k4-tokio-price/index|EP-0011 — K4のWをTOKIOと読むことには、どれだけの価値があるか]]
3. [[ja/research/kryptos-k4-classical/index|EP-0032 — K4のcribと文字数で、どの古典暗号を否定できるか]]
4. [[ja/research/kryptos-k4-w-brackets/index|EP-0057 — K4の2つのcribを挟むWは、構造を持っているか]]
5. [[ja/research/kryptos-k4-physical-keys/index|EP-0066 — 彫刻の物理的な形が、K4の鍵になりうるか]]
6. [[ja/research/kryptos-k4-carving-errors/index|EP-0071 — 彫り間違いが数文字あれば、否定した暗号は開くか]]
7. [[ja/research/kryptos-k4-masks/index|EP-0072 — 固定の換字が英語を隠しているとき、どの鍵がまだ検定できるか]]
8. [[ja/research/kryptos-k4-key-bound/index|EP-0091 — K4にはどれだけの鍵が要り、それで何が判定できるものとして残るか]]
9. [[ja/research/kryptos-k4-key-sources/index|EP-0093 — 鍵の出どころを、それが動かす表を知らずに検定できるか]]
10. [[ja/research/kryptos-k4-letter-graph/index|EP-0101 — 鍵を選ばずに、cribの文字のつながりだけで除外できる暗号はどれか]]
11. [[ja/research/kryptos-k4-w-squares/index|EP-0110 — Wを区切りとみれば、5×5の方陣の暗号でK4を作れるか]]
12. [[ja/research/kryptos-k4-consistency/index|EP-0113 — 鍵を探さずに、cribとの整合だけで否定できる暗号はどれか]]
13. [[ja/research/kryptos-k4-chosen-rows/index|EP-0114 — 鍵語の行の一覧から1文字ずつ選ぶ表で、K4を作れるか]]
14. [[ja/research/kryptos-k4-affine-hill/index|EP-0117 — 文に沿って変わるアフィンやHillの行列は、K4に合うか]]
15. [[ja/research/kryptos-k4-procedure-enumerator/index|EP-0119 — 部品の文法から作った手順のうち、K4に合うものはあるか]]
16. [[ja/research/kryptos-k4-rotors/index|EP-0121 — 配線が自由なロータ機で、K4のcribを作れるか]]
17. [[ja/research/kryptos-k4-list-price/index|EP-0135 — 標的リストを選ぶ自由まで払うと、TOKIOの読みはいくらか]]
18. [[ja/research/kryptos-k4-word-reordering/index|EP-0137 — 語の中で文字を並べ替えれば、K4に合う手順は現れるか]]
19. [[ja/research/kryptos-k4-o-pairs/index|EP-0138 — TOKIOの2つのOの区間を対にした2文字暗号で、K4を作れるか]]
20. [[ja/research/kryptos-k4-yar-photo/index|EP-0139 — 上がって見える3文字と余分なLは、意図した印か、施工のずれか]]
21. [[ja/research/kryptos-k4-construction-ledger/index|EP-0140 — 彫刻の制作・施工の事実は、K4の演算子をどこまで決めるか]]
22. **[[ja/research/kryptos-k4-production-traces/index|EP-0141 — K1〜K3の制作は、刻まれた配置に痕跡を残したか]]（最新）**
<!-- GENERATED: program-history:END -->

## 出典

Jim Sanborn, *Kryptos*（1990）。暗号文は[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)と[Elonka Dunin](https://elonka.com/kryptos/)の転記による。cribの公開：[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020（[transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)）、`EAST` は[Elonka Duninのarchive](https://elonka.com/kryptos/)。Scheidtの発言（英語をmaskした、まず技法を解く）：[WIRED 2005](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/)。Sanbornの2025年のヒント：[Scientific American](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/)。2025年の資料での発見：[RR Auction](https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/)。暗号文とcribは研究と論評のための引用であり、このサイトのライセンスの対象外です。
