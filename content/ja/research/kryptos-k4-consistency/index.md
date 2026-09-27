---
research_id: KRYPTOS-K4-EP-0113
title: 鍵を探さずに、cribとの整合だけで否定できる暗号はどれか
date: '2026-09-27'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 出現回数の暗号、周期鍵でのVigenère／Beaufortの自由な切り替え、Slidefair、Portax、1回がけのDoppelkastenはcribと両立しない。論理的な反証で、でたらめより起きにくいとは言えない
evidence_level: 公開暗号文とcribについての厳密な整合の議論。K4だけを使う部分はすべて再実行できる
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文と公開crib 24文字。厳密な整合の判定、並べ替えた暗号文のnull、植え込みの陽性対照
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 述べた形の5つの族（出現回数の鍵、Vigenère／Beaufortの切り替え、Slidefair、Portax、Doppelkasten）。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0113
source_episode_sha256: 89486e8a8e0fd05bc759a15136f5159e6170e843fd5ce644961c7842dda5d77c
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-consistency/" hreflang="en">English</a></p>

## 何を調べたか

暗号の族の中には、鍵をまったく選ばずにcribで判定できるものがあります。族がcribの文字どうしに関係を強制し、K4がそれを満たすかどうかで決まるからです。この種の族で、生き残るものはあるか。

## なぜ重要か

これらの族は、未検定の「別方式」（1枚の表のずらしではない方式）として登録されていました。整合の議論なら厳密に決着でき、どの結論が探索の運に依り、どれが依らないかも分かります。

## 方法

- **出現回数の暗号（EP-0112）。** 文字に使う行が、その平文字がそれまでに出た回数で決まる形。2つの形を調べました。任意のalphabetの下で、出るたびに共通の歩幅dだけ進むずらし（C＝τ(σ(x)＋d·n_x＋b)）と、どの時点でも復号できる任意の表です。
- **Vigenère／Beaufort／変形Beaufortの切り替え（EP-0113）。** 各位置で3つの型のどれかを使います（σ(C)＝s·σ(P)＋t·k、σはA–ZかKRYPTOS）。型の並びは完全に自由にし、鍵は周期p＝1〜52の周期鍵か、語・一次式・Gronsfeldの数字・一覧の文章の走り鍵で位置ごとに決まるものとしました。
- **Slidefair、Portax、Doppelkasten（EP-0116）。** 2文字単位の暗号です。規則はACAの説明に従い、まず例題を再現しました。Doppelkastenは完全に自由な方陣2枚、Wを区切り、同じ行の規則4通りと組み方48通りで、厳密に解きました。
- **nullと対照。** どの判定でも並べ替えたK4を、どの族でもcribを書き込んだ英文の植え込みを使いました。

## 結果

| 族 | K4 | でたらめな暗号文 |
|---|---|---|
| 出現回数によるずらし（σ、τ、dは任意） | 不可能：Vが、R（Tの24→28）とZ（Lの66→70）の両方へ進む | シャッフルの80%が同じ判定で落ちる |
| 復号できる出現回数の表（任意） | 不可能：9つの暗号字が、それぞれ2つの平文字から出る | — |
| 自由な切り替え＋周期鍵 | cribが拘束するどの周期（1〜26、30〜52）でも鍵がない。合うのは、同じ剰余に入るcrib位置の組がない27〜29だけ | p≦24で合うシャッフルは2,000本に1本。拘束のあるすべての周期で落ちるのは33% |
| 位置ごとに決まる鍵での切り替え（1,655万設定） | 0（期待0.011） | 10本中0 |
| 短い切り替え規則（彫刻の行、Wの区間、Tの位置、偶奇、切り替え点）×周期鍵 | どの周期も合わない | — |
| Slidefair、Portax | 文字を自分に暗号化しないので、S→S（32）とK→K（73）で除外 | — |
| Portax＋前段の自由な置換 | P＝1〜22と34〜48で矛盾。P＝23〜33は計算が終わらず | 各Pで200本中0 |
| 1回がけのDoppelkasten、自由な方陣 | 行長21を含む96設定すべてで矛盾 | 1,100本中10が両立 |
| 2回がけのDoppelkasten | 判定できない：解き手が植え込みの英文を27〜34%しか戻せない | — |

## 現在わかっていること

別方式として開いていた5つの族が、cribとの整合で閉じました。出現回数で行を変える暗号、周期鍵でのVigenère・Beaufort・変形Beaufortの自由な切り替え、Slidefair、Portax、1回がけのDoppelkastenです。どれも論理的な反証です。でたらめな暗号文もたいてい同じように落ちるので、K4がでたらめより起きにくいとは言えません。

## 図で見る

![周期1〜52について、型を自由に切り替える周期鍵が合うシャッフル2,000本の割合の棒グラフ。24以下はほぼ0、26・30・52で約3分の1、27〜29は全部。軸の下には、K4が拘束のあるどの周期でも合わないことの印](/assets/kryptos-k4-consistency.svg)

27〜29の薄い棒は、同じ剰余に入るcrib位置の組がない周期で、どんな文でも合います。それ以外ではK4は合いませんが、小さな周期ではでたらめな暗号文もほとんど合いません。

## この研究が示すこと

- 出現回数で進むずらしは、どのalphabetと歩幅でもK4のcribを作れません。
- どの時点でも復号できる出現回数の表は、固定の同音換字になります。cribでは9つの暗号字が2つの違う平文字から出ています。
- 3つの加法型を位置ごとに自由に切り替えても、cribが拘束するどの周期でも周期鍵は救えません。切り替えの短い規則（2つのcribの鍵の水準の違いを説明しえた彫刻の行を含む）でも同じです。
- SlidefairとPortaxは文字を自分に暗号化できませんが、K4は2回それをしています。
- 自由な方陣2枚の1回がけDoppelkastenは、調べたどの組み方でもcribと矛盾します。

## この研究が示さないこと

これらの族の下で、K4がでたらめより起きにくいことは示しません。未決のまま残るのは、2回がけのDoppelkasten、Portaxの前段置換で周期23〜33のものと後段置換でcribの対が少ない周期のもの、出現回数の形で文字ごとに歩幅を変えるもの、そして自由度の大きい鍵（一般の英文の走り鍵、長い周期）と切り替えの組み合わせです。

## 何が変わったか

カタログの5項目が「未検定」から「閉」になりました。彫刻の行で切り替える案の動機だった、2つのcribの鍵の水準の違いは、この形では説明できません。

## 何が失敗したか

2回がけのDoppelkastenは判定できませんでした。焼きなましが植え込みの英文を27〜34%しか戻せず、K4に回しても意味がないからです。PortaxのP＝23の探索は8時間半で終わりませんでした。

## 証拠の範囲

公開K4暗号文とcribです。出現回数、同音、自己暗号化、周期鍵の切り替えの判定はK4だけを使い、再実行できます。鍵つきの切り替えの探索はこのサイトが公開しないK1〜K3の文を読み、PortaxとDoppelkastenの解き手は公開パッケージに入っていません。それらは結果を記録しています。

## まだ分からないこと

より強い解き手なら2回がけのDoppelkastenを判定できるか（自由な方陣2枚は約167 bitで、92文字の英文の冗長度より小さいので、原理上は決まる量です）。外部の独立replicationは0件です。

## この結論が崩れるとき

24のcrib文字をすべて再現する、鍵と切り替え規則、Portaxの鍵と置換、またはDoppelkastenの方陣2枚が見つかれば、対応する行は覆ります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-consistency)：`python verify_consistency.py` は、出現回数の矛盾とそのシャッフル率、同音の衝突、自己暗号化、両方のalphabetでの自由な切り替えの周期を、シャッフル2,000本のnullとともに計算し直し、`PASS` を出します。標準ライブラリだけで数秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、ここで再実行しない探索を含む記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-consistency)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

あいだの文字を変数として扱う、2回がけDoppelkastenの厳密な解き手。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
- SlidefairとPortax：American Cryptogram Associationの暗号の種類の説明（[ACA](https://www.cryptogram.org/resource-area/cipher-types/)）。
