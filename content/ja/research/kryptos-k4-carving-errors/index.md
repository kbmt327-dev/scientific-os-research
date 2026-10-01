---
research_id: KRYPTOS-K4-EP-0071
title: 彫り間違いが数文字あれば、否定した暗号は開くか
date: '2026-09-26'
lang: ja
domain: Kryptos K4
type: Finding
status: 誤り1文字では何も開かない。5文字までなら、制約の多い族は閉じたままで、少ない族は判定できなくなる。どの族でも、K4に要る誤りの数はでたらめな暗号文と同じ
evidence_level: 公開暗号文とcribでの、最小の誤り数の厳密な計算と、陽性対照とシャッフルのnullつきの緩めたcrib検定
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文と公開crib 24文字。緩めたcrib検定、植え込みの陽性対照、並べ替えた暗号文のnull
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: cribや彫りの誤りを1〜5文字許したとき、K1〜K3の形の族と後に調べた別方式で、このProgramの主な否定がどう変わるか。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0071
source_episode_sha256: be936dda3db3eaf7e377804574770f736fb55d789ceb29963f39737d09fae908
publication:
  status: publishable
tags:
- kryptos-k4
- robustness
- carving-errors
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-carving-errors/" hreflang="en">English</a></p>

## 現在わかっていること

KryptosのK1〜K3には知られた彫り間違いがあるので、K4にもあるかもしれません。cribの誤りを1文字許しても、否定した族は1つも開きません。5文字まで許すと、cribが強く拘束する族（周期22〜23までの周期鍵、Trifid、2×2のHill）は閉じたままで、拘束の弱い族（剰余ごとに自由なalphabet、3×3のHill、英語の走り鍵）は判定できなくなります。どの族でも、K4に要る誤りの数は並べ替えた暗号文とほぼ同じで、「彫り間違いが数文字ある」ことは、どの族も特に支持しません。

## その後の点検（2026-09-30）

97の暗号字そのものを、彫刻の写真と照合しました（EP-0147）。判定の規則は、見る前にcommitしました。写真（見ただけで保存していない）は、Library of Congressにある Carol M. Highsmith の裏からの写真（item 2011631531）と、Jim Gillogly の写真3枚（1999-10-27）です。97の位置すべてが少なくとも1枚ではっきり読め、すべてがこのプログラムで使ってきた転記と一致しました。**食い違いは0**です。3か所の行区切り（最初の4文字の後と、その後31文字ごと）も、継ぎ目と左端で確かめました。1枚ではあいまいだった3文字は、別の写真ではっきり読めました。限界：読み手は基準の転記を知ったうえで読んだので、見落としの可能性はゼロではありません。これは転記の点検で、彫りの点検ではありません。彫られた文字が作者の意図どおりかは分からないので、上の数は変わりません。ただし、crib以外の文字を読む結果が転記の誤りに乗っていないことは言えます。要約は `results/transcription-check-20260930.json` にあり、写真は載せていません。

## 図で見る

![周期1〜48について、周期鍵に要るcribの誤りの最小数。K4は点、シャッフル100本の範囲は棒。K4は周期23まで5より多く、ほぼどこでもシャッフルの範囲の中](/assets/kryptos-k4-carving-errors.svg)

## この研究が示すこと

- 誤り1文字では、このProgramの主な否定はそのまま保たれ、新しく開くものはありません（Quagmire、Trifid、Hillは候補なし）。
- 周期鍵は、このパッケージの規約で周期23まで少なくとも7文字の誤りが要ります（内部ではcribのずれを許して18〜22で6〜10）。数文字の彫り間違いでは救えません。
- 後に調べた別方式では、外すcribの文字の最小数が小さいもの（Two-square 1、CM-Bifid 1、Four-square 2）もありますが、でたらめな暗号文も同じくらい少なくてすむので、誤りから族は選べません。

## この研究が示さないこと

K4に実際に何文字の誤りがあるかは推定しません。拘束の弱い族を救ってもいません。誤りを十分許すと、どちらにも判定できなくなる、と示しただけです。

## 何を調べたか

cribの文字のいくつかが違っていたら（彫り間違い、または公開cribのわずかなずれ）、このProgramの否定のうちどれが残るか。誤りを許すと、でたらめな暗号文よりK4がどれかの族に近づくか。

## なぜ重要か

このProgramの否定は、どれも24のcrib文字が正確だと仮定しています。KryptosのK1〜K3には記録された綴りの誤りがあるので、この仮定に値段を付ける必要があります。それぞれの結論が何文字の誤りまで耐えるかです。

## 方法

- **最小の誤り、周期鍵。** 周期と規約（Vigenère、Beaufort、変形Beaufort、A–ZかKRYPTOS）ごとに、違っていなければならないcribの文字の最小数を、剰余類ごとに厳密に計算しました。内部ではcribを前後2文字までずらした形も。
- **緩めたcrib検定（EP-0070、EP-0071）。** 主な否定した族（周期鍵、剰余ごとに自由なalphabet＋列の一致指数、Quagmire、Trifid、Hill、Kryptosの文の歩幅鍵、世界時計の鍵、英語の走り鍵）を、誤り1文字、次に5文字までで回し直しました。
- **別方式の誤りの距離（EP-0123）。** 後に調べた族ごとに、両立するまでに外すcribの文字の最小数。
- **対照。** 植え込みの暗号文に誤りを植え込み、すべての数で並べ替えたK4をnullにしました。

## 結果

| 族 | K4に要る誤り | でたらめな暗号文 | 5文字まで許すと |
|---|---|---|---|
| 周期鍵、p≦16 | 7以上 | 同じ範囲 | 閉 |
| 周期鍵、p＝18〜22 | 6〜10 | 同じ範囲 | 閉 |
| 周期鍵、p＝17と23以上 | 5以下 | 同じ | 判定できない |
| 周期Trifid | 10以上 | 9〜22 | 閉 |
| Hill 2×2 | 6ブロック以上 | 同じ | 閉 |
| Hill 3×3 | 3〜4ブロック | 同じ | 判定できない |
| Kryptosの文の歩幅鍵、世界時計の鍵 | 14 | 14〜15 | 閉 |
| 剰余ごとに自由なalphabet、p≧10 | — | シャッフルの45〜100%が通る | 判定できない |
| 英語の走り鍵 | — | シャッフルもほぼ通る | 検出力を失う |

| 別方式（EP-0123） | 外すcribの文字の最小数 | 同じ以下のシャッフル |
|---|---|---|
| Two-square | 1 | 200本中75 |
| Four-square | 2 | 200本中26 |
| CM-Bifid | 1 | 50本中50 |
| 周期のHill（判定できる設定） | 1 | 10本中10 |
| 自由なロータ1枚 | 7 | 200本中159 |
| 固定の同音換字 | 9 | 91.7% |

このパッケージの再計算では、48の周期のうち1つ（p＝39）でK4がシャッフル100本すべてより少なくてすみますが、これは偶然でありうる程度です。

## 何が変わったか

このProgramの否定を、それぞれが耐える誤りの数と一緒に述べるようになりました。誤りを許すと判定できなくなる族は、否定ではなく「判定できない」と記しました。

## 何が失敗したか

5文字の誤りで生まれる大量のQuagmireの通過（545万行）の採点は、計算量の上で無理で、途中で止めました。その周期は「判定できない」としています。

## 証拠の範囲

公開K4暗号文とcribです。周期鍵の最小誤りの表は公開パッケージで再実行します。ほかの族の緩めた検定は、ここで公開しない文章と解き手を使っており、結果を記録しています。

## まだ分からないこと

K4の彫りや公開cribに何文字の誤りがあるか。外部の独立replicationは0件です。

## この結論が崩れるとき

K4のcribの範囲に5文字を超える誤りがある証拠が出れば、閉とした周期の族が再び開きます。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-carving-errors)：`python verify_carving_errors.py` は、周期1〜48の周期鍵に要るcribの誤りの最小数を、K4とシャッフル100本について計算し直し、`PASS` を出します。標準ライブラリだけで数秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、ここで再実行しない族を含む記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-carving-errors)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

手順の列挙器で、cribの誤りを4〜7文字まで許す判定（この記事の時点で計算中）。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
