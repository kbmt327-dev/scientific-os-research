---
research_id: KRYPTOS-K4-EP-0032
title: K4のcribと文字数で、どの古典暗号を否定できるか
date: '2026-09-20'
lang: ja
domain: Kryptos K4
type: Negative Result
status: どの周期鍵も、cribで検定できる49周期すべてで、8つのalphabetと形のすべてで落ちる。progressive・Gromark型も落ちる。転置だけ、25記号の暗号は不可能。ほかの古典の族も候補なし
evidence_level: cribの鍵の値と文字数からの厳密な閉鎖。検出力はK1・K2で先に確認。鍵の値の部分はすべて再実行できる
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文、公開crib 24文字、英語の文字頻度。K1とK2を陽性対照に使用
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 4つのalphabetと2つの形での周期鍵と差分が周期の鍵、英語の頻度の走り鍵、転置だけ、一覧の古典の族。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0032
source_episode_sha256: 4bb3749dad6b745ff5b57e50d535a78ff2111c8735d68071a3358fe613f041fe
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-classical/" hreflang="en">English</a></p>

## 何を調べたか

K1〜K3は、鍵語つきのVigenèreと転置で解かれました。珍しいものを試す前に、その種の古典暗号のうち、K4のcrib 24文字と文字数で否定できるのはどれか。cribでまったく判定できない周期はどれか。

## なぜ重要か

族を鍵ごとに探すと、探した分しか否定できません。cribの鍵の値そのものをデータとして扱うと、種類ごとまとめて否定でき、24文字では届かない周期もはっきりします。このProgramのほかの部分は、この除外の上に立っています。

## 方法

- **鍵の値。** alphabetと形を決めると、crib 24文字から24個の鍵の値がそのまま決まります。Vigenèreと変形Beaufortはどちらも c−p を、Beaufortは c＋p を決めます。4つのalphabet（A–Zと、KRYPTOS・PALIMPSEST・ABSCISSAの鍵語alphabet）×2つの形＝8設定。
- **周期鍵。** 周期pの鍵なら、pを法として合同なcrib位置は同じ値を持たねばなりません。p＝1〜96を一度に判定します。検定できるのは、同じ剰余に入るcrib位置の組がある周期だけです。
- **差分が周期の鍵。** progressiveやGromark型の鍵は1階の差分が周期的になるので、差分に同じ判定をします。
- **英語の走り鍵。** 24個の鍵の値を英語の文字頻度に照らします（ふつうの英文から取った鍵）。
- **転置だけ。** 並べ替えはK4の文字数を保つので、97文字の英語の標本とK4の一致指数を比べます。
- **検出力を先に。** K1とK2に回すと、この検定は本当の周期（10と8）とalphabetを当てます。最初はA–Zで計算して当てられず、それでバグが見つかりました。
- **ほかの族（EP-0018〜0020、EP-0051〜0056、EP-0059）。** それぞれの検定と対照で探し、結果を記録しました。

## 結果

| 族 | 結果 |
|---|---|
| どんな周期鍵でも、p＝1〜96 | 検定できる49周期すべてで、8設定すべてで落ちる。27〜29と53〜96は検定できない |
| 差分が周期の鍵（progressive、Gromark型） | 8設定すべてで落ちる |
| 英語の文字頻度の走り鍵 | 7設定で、K4の鍵の値は英語から抜いた20,000本すべてより起きにくい（残る1設定で0.0002以下） |
| どんな転置でも、転置だけ | 英語の標本20,000本のうちK4ほど平らなものは0 |
| 出力が25記号以下の暗号 | 不可能：K4は26文字すべてを使う |
| 固定点のない装置（反射板つきEnigma、M-94、M-138-A、HC-9） | 位置がそろうなら不可能：32でS→S、73でK→K |
| 剰余ごとに自由なalphabet、p≦24 | cribか列の文字統計で否定 |
| 鍵つき列転置とK3型の回転（それぞれ周期鍵と） | 候補なし |
| 転置つきのHill n＝2〜4、語のcubeのTrifid | 候補なし |
| 鍵語の二層重ね | 1.4×10¹⁰設定で候補なし |
| 周期鍵の後の7×7回転グリル2枚 | 2.09×10¹⁰設定で候補なし |
| 行転置＋周期鍵 | シャッフルの対照と区別できない |

## 現在わかっていること

K1〜K3の種類の暗号ではK4は作れません。どの周期鍵も、標準かKryptosの鍵語のどのalphabetと形でも、cribで検定できるすべての周期で落ちます。差分が周期の鍵も落ち、転置だけでは英語をK4の平らな文字数にできず、ほかに探した古典の族も候補を出しません。cribで判定できないものも明示しました。周期27〜29と53以上です。

## 図で見る

![周期1〜96の格子。赤の49周期は検定でき、8設定すべてで落ちる。灰色の47周期（27〜29と53〜96）は検定できない](/assets/kryptos-k4-classical.svg)

## この研究が示すこと

- 周期鍵は、1周期ずつではなく種類として、cribが届くすべての周期で閉じます。
- cribは周期27〜29と53以上を判定できません。それらは否定されたのではなく、届かないのです。
- K4は並べ替えた英語にしては平らすぎるので、何らかの換字が入っています。

## この研究が示さないこと

走り鍵の結果が否定するのは、英語の文字頻度に従う鍵です。手で選んだ英文すべてを否定してはいません。とくに換字を1段足すと（片側maskつきの手で選んだ英語の鍵）判定できません。cribで検定できない周期は、閉ではなく開いたままです。

## 何が変わったか

以前の要約は「繰り返す鍵は周期13以上で無拘束」としていましたが、鍵の値で見ると周期30〜52の多くも検定でき、すべて落ちました。「英語の走り鍵をすべて閉じた」という記述は、後に「英語の文字頻度に従う鍵」に狭めました。

## 何が失敗したか

最初の実行はA–Zのalphabetを使ったので、K1とK2の周期を当てられませんでした。K1とK2はKRYPTOSのalphabetを使います。K4に回す前にこれを直せたのが、検出力を先に確かめる理由です。

## 証拠の範囲

公開K4暗号文とcrib、英語の文字頻度です。鍵の値による閉鎖と文字数の検定は、公開パッケージで再実行します。ほかの古典の探索は、ここで公開しない文章と解き手を使っており、結果を記録しています。

## まだ分からないこと

K4が周期53以上、または27〜29を使っているか。外部の独立replicationは0件です。

## この結論が崩れるとき

8設定のどれかで、検定できる周期の周期鍵が24のcrib文字すべてに合えば、閉鎖は覆ります。4つの外のalphabetが本当のものなら、そのalphabetで閉鎖をやり直す必要があります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-classical)：`python verify_classical.py` は、8設定の鍵の値の表、すべての周期での周期鍵と差分の閉鎖、英語の頻度の検定、文字数の検定を計算し直し、`PASS` を出します。標準ライブラリだけで数秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、ここで再実行しない族を含む記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-classical)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

暗号化の前後のmaskと、彫刻の物理的な形からの鍵（後のNoteで報告）。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
- K1〜K3の方式（KRYPTOSのalphabetの鍵つきVigenère、K3の転置）：[Wikipedia「Kryptos」](https://en.wikipedia.org/wiki/Kryptos)。
