---
research_id: KRYPTOS-K4-EP-0121
title: 配線が自由なロータ機で、K4のcribを作れるか
date: '2026-09-27'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 自由配線のロータ1枚（どの歩幅でも、入口・出口の鍵語alphabetや位置の鍵でも）、動く2枚＋自由な遅い1枚、自由な置換の後ろの反射板つきの機械は、どれも0設定。論理的な反証で、でたらめより起きにくいとは言えない
evidence_level: 列挙した設定ごとに自由配線の存在を厳密に判定。公開暗号文とcribを使用。スクリプトは回す前にコミット
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文と公開crib 24文字。配線の厳密な判定、植え込みの陽性対照、並べ替えた暗号文のnull
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 述べた形のロータの族（自由配線1枚、または274の鍵語alphabetの動くロータ＋自由なロータ1枚、または公開のEnigma型配線＋自由な置換）。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0121
source_episode_sha256: ef45787aa9e0ecbea92f3db22340029ba4856590f7b2aad108d2cedcf3d3934c
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-rotors/" hreflang="en">English</a></p>

## 何を調べたか

ロータは1文字ごとに換字を変えますが、表のずらしではないので、本当の意味での別方式です。1枚のロータの配線を完全に自由にしたとき、下に挙げる種類のロータ機で、24のcrib文字を作れるか。

## なぜ重要か

自由な配線には約88 bitの自由度があり、どんな探索でも列挙できません。それでも厳密に判定できます。cribは配線について24本の式を与え、それが互いに矛盾しないときに限って配線が存在するからです。絶望的な探索が、設定ごとの可否の判定に変わります。

## 方法

- **自由なロータ1枚（EP-0083）。** 位置iでロータを s＋d·i だけずらします。接点の番号はA–ZかKRYPTOS、d＝0〜25。cribの各文字が R(u)＝v を与え、同じuには必ず同じv、違うuには違うvが対応するときに限って配線が存在します。
- **拡張（EP-0121）。** 入口と出口に鍵語alphabetを付けた自由なロータ1枚（Kryptos・ヒント・2025年の主題語から作った274 alphabet、1,951,976設定）。位置だけで決まる鍵で進む自由なロータ1枚：周期の鍵語、二次式、速いロータからの桁上がり、Wの区間、彫刻の行、Berlin clockの灯の数（90,246,284設定）。odometer：274 alphabetから選んだ動く2枚と、信号の道のどこにでも置ける自由な遅い1枚。動く配線が一覧にある2枚・3枚の機械をすべて覆います（7.9×10¹⁰設定、GPU）。
- **反射板つきの機械（EP-0132）。** 反射板つきの機械は単独では文字を自分に暗号化せず、K4は位置32と73でそれをしています。前段に自由な置換があると、この議論は効きません。そこで商用Enigma D・K、Swiss-K、Railwayの配線（plugboardなし）を自由な置換の後ろに置いて判定しました。1.11×10¹⁰設定で、シミュレータは公開のEnigmaの試験値で確かめました。
- **対照。** すべての族で植え込みの機械、nullは並べ替えたK4。スクリプトはK4に回す前にコミットしました。

## 結果

| 族 | 設定 | K4 | シャッフル | 対照 |
|---|---|---|---|---|
| 自由なロータ1枚、歩幅d、A–ZかKRYPTOS | 52 | **0** | 2,000本中0 | 200/200 |
| 1つの置換の累乗の表、指数a·i＋b | 676 | **0** | 2,000本中0 | 200/200 |
| 入口・出口の鍵語alphabetつきの自由なロータ | 1,951,976 | **0** | 10本中0 | 30/30 |
| 位置の鍵で進む自由なロータ | 90,246,284 | **0** | 10本中0 | 30/30 |
| 動く2枚＋自由な遅い1枚 | 7.9×10¹⁰ | **0** | 10本中1 | 30/30 |
| 自由な置換の後ろの反射板つきの機械 | 1.11×10¹⁰ | **0** | 50本中0 | 30/30 |

配線が存在するのに要るcribの誤りの最小数は、鍵語alphabetつきで4（シャッフルは3〜4）、位置の鍵で3（シャッフルは3〜5）でした。

## 現在わかっていること

調べたロータの族は、どれもK4のcribを作れません。どの歩幅・鍵語alphabet・位置だけの進み方でも自由なロータ1枚はだめで、動く配線が274の鍵語alphabetにある2枚・3枚の機械も（遅いロータは自由でも）だめ、公開配線の反射板つき機械に自由な置換を前置してもだめでした。どれも論理的な反証です。でたらめな暗号文も落ちる（odometerはcribの容量に近いので10本中1本が偶然通った）ので、K4がでたらめより起きにくいとは言えません。

## 図で見る

![横棒グラフ：5つのロータの族で探した設定のlog2。自由なロータ1枚の5.7 bitからodometerの36.2 bitまで、どれも「0件」。赤い線の112.8 bitがcribで決められる量](/assets/kryptos-k4-rotors.svg)

各族の自由な配線や自由な置換は探索ではなく解いているので、棒はそれぞれ族の自由度を約88 bit小さく見せています。

## この研究が示すこと

- どんな配線でも、ロータ1枚は、一定の歩幅でも、鍵語alphabetつきでも、位置だけで進む形でも、cribを作れません。
- 動くロータの配線が一覧のalphabetにある限り、2枚・3枚の機械は閉じます。遅いロータは何でもかまいません。
- 商用Enigma型の反射板つき機械の前に自由な置換を置いても、救えません。
- ロータ1枚に要るcribの誤りの数は、でたらめな暗号文の範囲の中です。「彫り間違いが数文字あれば」という説明は、この族を特に支持しません。

## この研究が示さないこと

K4がでたらめより起きにくいことは示しません。自由な配線が2枚以上の機械、274 alphabetの外の動く配線、反射板つき機械のplugboard、平文に依る進み方は、調べた範囲の外です。自由な配線が2枚あると、族はcribで判定できる量より大きくなります。

## 何が変わったか

カタログのロータの項目は、「2枚以上は判定できない」から「動くロータが一覧にあれば、遅いロータが何でも閉」に変わりました。カタログの点検で見つかった唯一の判定できる別方式、自由な置換の後ろの反射板つき機械も閉じました。

## 何が失敗したか

odometerの族はcribの容量に近く（設定36 bit＋自由なロータ1枚）、シャッフル10本中1本が偶然に通りました。K4で通っていても、偶然と見分けにくかったことになります。

## 証拠の範囲

公開K4暗号文とcribです。ロータ1枚の判定はK4だけを使い、公開パッケージで再実行します。大きな探索は、公開していない鍵語alphabetとGPUのバッチのコードを使っており、結果を記録しています。

## まだ分からないこと

自由な、あるいは一覧にない配線の1980年代の機械が使われたか。外部の独立replicationは0件です。

## この結論が崩れるとき

一覧の族のどれかで、24のcrib文字すべてと両立する配線（または置換）が存在する設定が見つかれば、対応する行は覆ります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-rotors)：`python verify_rotor.py` は、どの歩幅・どちらの番号でも自由配線のロータ1枚の判定をK4でやり直し、植え込み200本を見つけ、シャッフル2,000本を確かめて、`PASS` を出します。標準ライブラリだけで数秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、GPUの探索を含む記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-rotors)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

これらの族の中ではありません。自由な配線が2枚の機械は、cribでは判定できません。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
- Enigmaの配線：[Crypto Museum, Enigma wiring](https://www.cryptomuseum.com/crypto/enigma/wiring.htm)。
