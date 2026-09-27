---
research_id: KRYPTOS-K4-EP-0114
title: 鍵語の行の一覧から1文字ずつ選ぶ表で、K4を作れるか
date: '2026-09-27'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 調べた64本以下の鍵語・混合alphabetのどの一覧からも、どんな選び方でもcribは作れない。順に選ぶ形、M-94の円筒、暗号面の行も0件
evidence_level: 選び方を問わない被覆と、網羅的な順の探索。公開暗号文とcribを使用。族は回す前にコミット
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文と公開crib 24文字。語の一覧からの鍵語alphabet、M-94の円盤、並べ替えた暗号文のnull、植え込みの陽性対照
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 述べた一覧の鍵語alphabet・matrixで混ぜたalphabetを行にし、どんな規則で（被覆）、または順に選ぶ表と、M-94の円筒。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0114
source_episode_sha256: 9dfefe285696135fa41f132c422bfd723302390a1417eda94622a109baa21ec2
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-chosen-rows/" hreflang="en">English</a></p>

## 何を調べたか

手製の表は、ある文章の語ごとの鍵語alphabetを積み重ね、各位置の行を何かの規則で選んだものかもしれません。行の一覧は分かっていて規則が分からないとき、それでもK4のcribで検定できるか。

## なぜ重要か

行の選び方の規則は、いちばん推測しにくい部分です。規則を要しない検定なら、誰も列挙しようと思わない規則まで、すべてを一度に覆えます。

## 方法

- **選び方を問わない被覆（EP-0114）。** 行の一覧と読み方の規約を決め、少なくとも1本の行で説明できるcribの位置を数えます。24未満なら、その一覧から行をどう選んでも（どの順でも）cribは作れません。規約は、行をA–ZかKRYPTOSの位置の暗号alphabetとして使う形、その逆、g個先を読む円筒の形で、全部で29。
- **一覧。** ヒントの鍵語（40行）、ヨハネ8:32（9）、世界時計の地名（146）。内部では、K1〜K3の語、K0の句、2025年の主題語、K3の平文の格子も（64行以下の一覧44個）。それぞれ、普通の鍵語alphabetとmatrixで混ぜた3種。
- **順に選ぶ（EP-0098、EP-0114）。** 語の順に行を取り、歩幅、向き、開始、4つの規約を変えます。普通の鍵語の行で386,048設定、混ぜた行で190,282,456設定。
- **M-94の円筒（EP-0099）。** 公開されている25枚の円盤を任意の順に、任意の行の位相、各行1つの読み出しで、厳密な照合で調べました。彫られた暗号面の行を鍵語にした行も。
- **対照。** 植え込みの表（30/30と30/30）。nullは並べ替えたK4（被覆で200本、順の探索で20本）。

## 結果

| 一覧（普通の鍵語の行） | 行 | 24中の最良の被覆 | 同じ以上のシャッフル |
|---|---|---|---|
| ヒントの鍵語 | 40 | 18 | 89% |
| ヨハネ8:32 | 9 | 8 | 85% |
| 世界時計の地名 | 146 | 20 | 98% |
| 内部の44一覧（各64行以下） | — | どれも24に届かない | — |

| 探索 | 設定 | K4 |
|---|---|---|
| 続く語の鍵語の行を順に | 386,048 | 0（最良5〜7/24、シャッフルの水準） |
| 混ぜた行を順に | 190,282,456 | 19/24に届くもの0（最良5〜10） |
| M-94、円盤の順は任意 | 1,065,625×すべての順 | 0（対照20/20） |
| 彫られた暗号面の行の鍵語の行 | 60,320 | 0（最良6/24＝nullの中央値） |
| 文章の行をそのまま表の行に | — | 順向き：一致指数がK4以下は0.2%。逆向き：英文を暗号化できない |

## 現在わかっていること

鍵語alphabetの一覧から表の行を選ぶ形では、調べたどの一覧でもK4のcribを作れません。64行以下のどの一覧（と世界時計の地名146）でも、どの行でも説明できないcribの文字があり、どんな選び方をしても救えません。順に選ぶ形、M-94の円筒、暗号面の行も何も出しませんでした。どれも論理的な反証で、並べ替えた文も同じように届きません。

## 図で見る

![3つの一覧の、24中の最良の被覆の横棒（ヒントの鍵語18、ヨハネ8:32の語8、世界時計の地名20）。どれも赤い線の24に届かない。シャッフルの中央値の印つき](/assets/kryptos-k4-chosen-rows.svg)

## この研究が示すこと

- 調べたどの一覧でも、どの規約のどの行でも届かないcribの文字があり、その一覧からの行の選び方はすべて除外されます。
- cribでふつうは拘束しきれない大きさの世界時計の地名146でも、説明できないcribの文字が4つ残ります。
- 順に選ぶ族と円筒の族は何も出しません。

## この研究が示さないこと

K4がでたらめより起きにくいことは示しません。並べ替えた文も同じように届きません。約64行を超える一覧はたいてい24文字すべてを覆うので、この方法では判定できません。出どころの一覧のない本当の手製の表は、この検定の外です。

## 何が変わったか

語の鍵語の表と混ぜた行の表は、「規則が分からないので判定できない」から「一覧にある出どころなら、規則によらず閉」に変わりました。

## 何が失敗したか

調べた一覧で24に届くものはありませんでした。もっと大きな一覧は判定できませんでした。

## 証拠の範囲

公開K4暗号文とcribです。ヒントの鍵語、ヨハネ8:32、世界時計の地名の被覆は、公開パッケージで再実行します。K1〜K3の文や暗号面から作った一覧、順の探索とM-94の探索は記録で、再実行していません。

## まだ分からないこと

手製の表の行がどこから来るか。外部の独立replicationは0件です。

## この結論が崩れるとき

24を覆い、cribを再現する選び方のある64行以下の一覧が見つかれば、その一覧について結果は覆ります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-chosen-rows)：`python verify_chosen_rows.py` は、3つの公開の一覧について29の規約での被覆を、シャッフル200本のnullとともに計算し直し、`PASS` を出します。標準ライブラリだけで約10秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、世界時計のデータ、ここで再実行しない探索を含む記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-chosen-rows)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

一覧にある出どころについてはありません。新しい出どころの一覧は、規則を提案する前に被覆で検定できます。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
- 世界時計の地名：[設計者Erich Johnの公式サイト](https://web.archive.org/web/20200812142431/https://weltzeituhr-berlin.de/en/places-worldtimeclock)（Internet Archive経由）。
- M-94の円盤：[Crypto Museum, M-94](https://www.cryptomuseum.com/crypto/usa/m94/index.htm)。
