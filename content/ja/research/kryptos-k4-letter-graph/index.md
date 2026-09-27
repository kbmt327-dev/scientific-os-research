---
research_id: KRYPTOS-K4-EP-0101
title: 鍵を選ばずに、cribの文字のつながりだけで除外できる暗号はどれか
date: '2026-09-26'
lang: ja
domain: Kryptos K4
type: Finding
status: crib 21文字はすべて1つにつながる。alphabetの固定の区分け（ブロックが21文字未満）を保つ暗号は、cribに誤りがなければ不可能
evidence_level: 公開暗号文とcribについての厳密な組合せ論の議論。すべて再実行できる
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文と公開crib 24文字だけ
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 位置ごとの写像がそれぞれ1つの固定したalphabetの区分けを保つ暗号と、語ごとに鍵をやり直す純粋な形。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0101
source_episode_sha256: 19ae4896562c109279caadc34716d00d1afdbe0a9cf0bd02c2a38da43b28284f
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- structural
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-letter-graph/" hreflang="en">English</a></p>

## 現在わかっていること

K4のcrib 24組を、平文字から暗号字への辺として描くと、cribに出る21文字は**すべて1つにつながります**。したがって、どの位置の換字も「alphabetの固定した組分け（各組を自分自身に写す）」を保つ暗号なら、21文字以上の組が要ります。母音と子音、alphabetの前半と後半、キーボードの段、Morseの長さ、Polybiusの行、立方体の位置のような組分けは、鍵が何であれ、cribに誤りがなければ不可能です。名前のある組分けは、cribの誤りが7〜19文字要ります。

## 図で見る

![21文字を円に並べ、矢印で1つにつながったグラフ。SとKには自己暗号化のループ。横に、cribの誤りを1・2・3文字認めたときの最大のつながり（12、9、7文字）と、名前のある組分けに要る誤りの数](/assets/kryptos-k4-letter-graph.svg)

## この研究が示すこと

- cribの文字のグラフは21文字すべてでつながっており、S→S（位置32）とK→K（位置73）は自分に暗号化されます。
- 固定の区分けを保つ暗号は、このつながり全体を1つのブロックに入れなければなりません。最大のブロックが21文字未満の区分けは、cribの誤りがなければ不可能です。12文字未満なら誤り1文字でも、9文字未満なら2文字でも、7文字未満なら3文字でも不可能です。
- 特定の区分けについては、ブロックをまたぐcribの組の数が、その区分けに要るcribの誤りの数そのものです。母音（Yを含む）と子音7、A–Zの前半・後半8、A–Zの偶奇8、KRYPTOS順の前半・後半8、QWERTYの段12、Morseの長さ18、5×5のPolybiusの行19。
- 2つの固定した半分を毎回入れ替える方式（Porta型）は、2つの自己暗号化があるので不可能です。
- 語ごとに鍵をやり直す純粋な形（各位置の行は任意の全単射で、語の中の位置だけで決まる）は、語の先頭から数えると、cribのどの区切り方でも成り立ちません。

## この研究が示さないこと

位置ごとの写像がalphabet全体を混ぜる暗号（ほとんどの暗号）については何も言いません。cribに誤りが多ければ、区分けの暗号も除外できません。語ごとに鍵をやり直す形は、語の末尾から数えると `EASTNORTHEAST` を1語とする区切りで生き残り、語の位置と語の番号を組み合わせた形は、でたらめな区切りと同じ割合で通ります。どちらも、その形を支持する証拠ではありません。

## 何を調べたか

鍵もalphabetも表も選ばずに、「どのcrib文字がどの文字に暗号化されるか」の形だけで、何が除外できるか。

## なぜ重要か

このProgramのほとんどの検定は、族を決めてその鍵を探します。これは鍵をまったく要しません。24組のcribの性質だけから、列挙しにくい珍しい「立体」や組分けの設計まで、設計の種類ごと除外します。さらに、それぞれに要るcribの誤りの数を示すので、結論がcribの正確さにどれだけ依るかを読み手が判断できます。

## 方法

- **グラフ。** cribの組ごとに、平文字から暗号字へ1本の辺。つながりはunion–findで求めます。
- **誤り。** k＝1、2、3について、k組のcribの外し方をすべて試し、最大のつながりが最も小さくなる値を記録します。
- **名前のある区分け。** 2つの文字が別のブロックに入るcribの組の数。これが、その区分けに要るcribの誤りの数そのものです。
- **語ごとのやり直し。** cribの区切り方6通り（`EAST|NORTHEAST`、`EASTNORTHEAST`、`EAST|NORTH|EAST` と、`BERLIN|CLOCK` か `BERLINCLOCK`）。語の中の位置は先頭からか末尾から。同じ語内位置の2つの位置で、同じ平文字が別の暗号字に、または別の平文字が同じ暗号字になれば矛盾です。

## 結果

| cribの誤りとして外す組の数 k | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 最大のつながり（文字） | 21 | 12 | 9 | 7 |

| 区分け | 最大のブロック | 要るcribの誤り |
|---|---|---|
| 母音（AEIOUY）／子音 | 20 | 7 |
| A–Zの前半・後半、A–Zの偶奇、KRYPTOS順の前半・後半 | 13 | 各8 |
| QWERTYの段 | 10 | 12 |
| Morseの長さ | 12 | 18 |
| 5×5のPolybiusの行 | 5 | 19 |
| 3×3×3の立方体の種類（8／12／6） | 12 | どう割り当てても1以上 |

| 区切り方 | 語の先頭から | 末尾から |
|---|---|---|
| `EAST\|NORTHEAST` ＋どちらでも | 矛盾 | 矛盾 |
| `EASTNORTHEAST` ＋どちらでも | 矛盾 | **両立** |
| `EAST\|NORTH\|EAST` ＋どちらでも | 矛盾 | 矛盾 |

## 何が変わったか

組分けや「立体」の設計を1つずつ列挙する必要はなくなりました。内部記録では「語ごとに鍵をやり直す純粋な形は、どの区切り方でも成り立たない」としていましたが、このNoteのための再計算で、末尾から数える形は `EASTNORTHEAST` を1語とすると両立することが分かり、記録を訂正しました。

## 何が失敗したか

上に書いたとおり、語ごとのやり直しについての記録は、再計算でそのままは残りませんでした。

## 証拠の範囲

公開K4暗号文と公開crib 24文字です。議論は厳密で、仮定はcribが正しいことだけです。それぞれの結論がどれだけの誤りまで耐えるかは表に示しました。

## まだ分からないこと

当時の実際の設計で、固定の区分けを使ったものがあるか。cribに誤りがあるか。外部の独立replicationは0件です。

## この結論が崩れるとき

cribの訂正が公表されてつながりが分かれるか、cribに何文字も誤りがある証拠が出れば、小さなブロックの区分け暗号が再び開きます。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-letter-graph)：`python verify_letter_graph.py` は、K4とcribからグラフを作り直し、誤り1〜3文字でのつながりの大きさ、名前のある区分けに要る誤りの数、語ごとのやり直しの矛盾を計算し直して、`PASS` を出します。K4とcribだけを使い、数秒で終わります。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-letter-graph)。MITライセンスです。暗号文とcribは引用です。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

区分けの暗号については計画はありません。生き残った語ごとのやり直しの形は手製の表の族で、K4だけからは判定できません。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
