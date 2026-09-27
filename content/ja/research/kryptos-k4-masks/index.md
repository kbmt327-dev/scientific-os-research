---
research_id: KRYPTOS-K4-EP-0072
title: 固定の換字が英語を隠しているとき、どの鍵がまだ検定できるか
date: '2026-09-26'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 片側に自由なmaskがあっても、文章の歩幅鍵、世界時計の鍵、距離の鍵、順の決まったM-94、自動鍵、一次式の鍵は0。周期鍵はcribの1つの偶然で19と38だけ通る。両側のmaskでは、どの走り鍵も英語にならない。順が自由なM-94、Hagelin、手で選んだ英語の鍵は判定できない
evidence_level: 自由なmaskの厳密な判定と、両側maskでの検出力を測った英語の段。公開暗号文とcribを使用。植え込みの対照とシャッフルのnull
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文と公開crib 24文字。自由な換字を厳密に解く判定、植え込みの対照とシャッフルのnullつきの英語の採点
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 鍵の前・後・両側に完全に自由な換字を置いたK1〜K3の形の暗号と、一覧の鍵の族。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0072
source_episode_sha256: bae495dc6bc7472dc504d81bc15f1e65ca8d3f3183938ad70a66f971694f035c
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-masks/" hreflang="en">English</a></p>

## 何を調べたか

Sanbornに暗号の技法を教えたEd Scheidtは、英語をmaskしたと語っています。鍵をかける前、後、または両側に固定の換字があって英語を隠しているなら、表は標準のものでなくてもよくなります。どの鍵の族がまだ検定でき、何が出るか。

## なぜ重要か

自由な換字は26!通り（約88 bit）の自由度です。maskなしで否定した族が、maskつきなら戻るかもしれません。maskの下で残る鍵の族と、検定できなくなる族を知ることが、「否定」と「maskがなければ否定」を分けます。

## 方法

- **片側に自由なmask（EP-0072〜0075）。** C＝σ(P)＋k（鍵の前のmask）か C＝τ(P＋k)（鍵の後のmask）。σとτは完全に自由で、厳密に解きます。鍵：Kryptosの文と世界時計の帯の歩幅鍵、距離の鍵、円盤の順が決まったM-94、平文と暗号文の自動鍵、位置の一次式の鍵、周期鍵。
- **両側のmask（EP-0076、0077、0084、0086）。** 両側にmaskがあるとcribは鍵に2本の式しか残さないので、英語の段で判定します。cribを通った候補ごとにmaskを焼きなましで解いて英語として採点し、検出力は植え込みの鍵で測りました。
- **容量（EP-0074、0085、0088）。** 自由度がcribと英語で決められる量を超える族は、探索せずに「判定できない」としました。
- **対照。** すべての族で植え込みのmaskと鍵、nullは並べ替えたK4。

## 結果

| 族 | mask | K4 | 対照／シャッフル |
|---|---|---|---|
| 位置の一次式の鍵 | 前か後 | 0 | 植え込み40/40、シャッフル200本中0 |
| 周期鍵 | 前か後 | 判定できる所では19と38だけ通る（27と65のR→P） | ほかの周期ではシャッフルの多くも通る |
| Kryptosの文の歩幅鍵・世界時計の鍵、距離の鍵 | 前か後 | 6,170万中0、93万中0 | 対照は回収 |
| 順の決まったM-94、自動鍵 | 前か後 | 0 | — |
| 円盤の順が自由なM-94 | 片側 | 判定できない（約79 bit対約52） | — |
| 歩幅つきの走り鍵（1,540万） | 両側 | cribを通る6,889件、英語になるものなし（最良−238.8、シャッフル−243.1） | 検出力約0.65 |
| Carter & Mace第1巻の走り鍵 | なしか片側／両側 | cribの誤り2文字まで0／通過291件、英語なし | 対照60/60、検出力約0.85 |
| ROLLの鍵と穴の窓（鍵4,081本） | なしか片側／両側 | 0／英語なし | 対照20/20、30/30 |
| Hagelin M-209／CX-52 | maskつき | 判定できない（自由度がcribと英語を数十〜200 bit超える） | — |
| 手で選んだ英語の走り鍵 | 片側 | 今の探索では判定できない（maskが未知だと植え込み8本中0を回収） | 反証ではない |

## 現在わかっていること

調べた短く書ける鍵では、maskを置いてもK1〜K3の形は救えません。片側に自由なmaskがあっても、文章の歩幅鍵、世界時計の鍵、距離の鍵、順の決まったM-94、自動鍵、一次式の鍵は何も出さず、周期鍵はcribの1つの偶然で19と38だけ通ります。両側にmaskがあっても、走り鍵の候補は英語になりません。開いたまま残るものは、否定ではなく判定できないものとして記しました。円盤の順が自由なM-94、maskつきのHagelin、片側maskの手で選んだ英語の鍵です。

## 図で見る

![鍵の前と後のmaskについて、周期1〜48の2段の図。灰色の棒は合うシャッフルの割合、点はK4が合う周期。判定できる所ではK4が合うのは19と38だけ](/assets/kryptos-k4-masks.svg)

## この研究が示すこと

- 位置の一次式の鍵は、どちら側のどんなmaskでも落ちます。
- maskの下で周期鍵が判定できるのは一部の周期だけで、そこでK4が合うのは19と38だけです。どちらもcribの27と65のR→Pで説明できます。
- 一覧の文章・時計・距離・円筒の鍵は、maskがあっても否定のままです。
- 両側のmaskでは、走り鍵の候補は英語に届かず、検出力は約0.65〜0.85と測りました。

## この研究が示さないこと

maskつきの手で選んだ英語の鍵、円盤の順が自由なM-94、maskつきのHagelinは否定していません。これらはK4で判定できる量を超えています。両側maskの陰性は検出力が1未満で、K2に似た文なら4回に1回ほどは閾値を下回ります。

## 何が変わったか

一覧の鍵について、K1〜K3の形の否定を「maskがあってもなくても」と述べるようになり、maskで判定できなくなる族に名前を付けました。

## 何が失敗したか

maskが未知のときの、手で選んだ英語の鍵の探索は、植え込み8本のどれも回収できませんでした。そのため、この族は否定ではなく、担当者の判断で「今は判定できない」として閉じました。

## 証拠の範囲

公開K4暗号文とcribです。一次式の鍵と周期鍵の判定は公開パッケージで再実行します。文章に基づく鍵（Kryptosの文、Carter）、両側maskの英語の段、容量の議論は記録で、再実行していません。

## まだ分からないこと

そもそもK4がmaskを使っているか。より強い探索なら、手で選んだ英語の鍵を判定できるか。外部の独立replicationは0件です。

## この結論が崩れるとき

24のcrib文字をすべて再現し、英語として読める一覧の鍵とmaskが見つかれば、対応する行は覆ります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-masks)：`python verify_masks.py` は、どちら側にも自由なmaskを置いた一次式の鍵と周期鍵の判定を、植え込みの対照と周期ごとのシャッフル200本の検出力とともにやり直し、`PASS` を出します。標準ライブラリだけで数秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、ここで再実行しない探索を含む記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-masks)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

一覧の鍵についてはありません。maskが未知でも植え込みの手で選んだ英語の鍵を回収できる探索ができれば、その族は判定できるようになります。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
- 英語をmaskしたというScheidtの発言：[WIRED 2005](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/)。
- 走り鍵の文章：Howard Carter and A. C. Mace, *The Tomb of Tut.ankh.Amen*, vol. 1（1923）。
