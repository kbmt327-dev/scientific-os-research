---
research_id: KRYPTOS-K4-EP-0110
title: Wを区切りとみれば、5×5の方陣の暗号でK4を作れるか
date: '2026-09-27'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 鍵語の方陣と自由な方陣（Four-square、Two-square、Bifid、CM-Bifid）、どちらの順のPlayfair＋mask、方陣＋mask、5×5格子のずらしは、判定できる範囲でcribと両立しない
evidence_level: 公開暗号文とcribでの厳密な整合判定と、陽性対照つきの焼きなまし
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Wを除いた公開K4暗号文と公開crib 24文字。厳密な解き手、焼きなまし、並べ替えた暗号文のnull、植え込みの陽性対照
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: W以外の92文字に25文字の方陣の2文字・塊の暗号をかける形。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0110
source_episode_sha256: 1ea5f657fc2a3ff2bb4cb9d60a56956a98e2d40ed3696c20639cbecbf207bc1b
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-w-squares/" hreflang="en">English</a></p>

## 何を調べたか

K4は26文字すべてを使うので、出力が25記号の暗号は除外されます。しかし5つのWが暗号化の後に加えた区切りなら、残り92文字はちょうど25種類で、方陣の暗号がまた候補になります。Wを除いたとき、5×5の方陣の暗号でcribを作れるか。

## なぜ重要か

このProgramが見落としを点検したとき、判定できて未検定の別方式として残っていたのがこれでした。方陣の暗号は、表のずらしに代わる古典的な方式で、Wの観察がそれを試す具体的な理由になっていました。

## 方法

- **文。** 5つのWを除いたK4：92文字、cribは縮めた位置の20〜32と59〜69。2文字の組み方は3通り：1文字目から、2文字目から、Wの区間ごとにやり直す。
- **鍵語の方陣（EP-0110）。** Four-square、Two-square（角の取り方4通り、そのまま出す規則の有無）、Bifid（周期2〜12、全文、区間ごと）。鍵はヒントの語、Kryptosの語、標準の方陣、英単語2,540語。計925,600設定。
- **自由な方陣。** 暗号側の方陣2枚が自由なFour-square：cribの2文字ごとに各方陣の升が1つ決まるので、整合を直接判定できます。自由な方陣のTwo-square：行と列の等式を厳密に解きました（72設定）。方陣1枚が自由なBifid：cribを強い制約にした焼きなまし。方陣2枚が自由なCM-Bifid：方陣の座標についての厳密な充足判定（EP-0120）。
- **ずらしのmaskつき。** Playfairの後にずらしのmask（方陣5,012、maskの族4つ、EP-0125）。鍵語の方陣の前か後にずらしのmask（EP-0126）。
- **格子のずらし。** 自由な5×5格子上の平行移動・回転・鏡映を、鍵の文字、文章の配置、周期鍵で決める形（EP-0115、EP-0128）。
- **対照。** すべての族で植え込みの暗号文、nullは並べ替えた暗号文。

## 結果

| 族 | K4 | 対照 | シャッフル |
|---|---|---|---|
| 鍵語の方陣（925,600設定） | 0 | 30/30 | 0、0、0 |
| Four-square、暗号側の方陣が自由 | どの組み方でも矛盾（平文側を鍵語の方陣40通りにしても） | 200/200 | 2,000本中0 |
| Two-square、自由な方陣（72設定） | 72すべてで矛盾 | 30/30 | 設定ごとに200本中0〜2 |
| Bifid、方陣1枚が自由 | どの周期でもスコアはシャッフルの水準 | 植え込みの英文を96〜100%回収 | — |
| CM-Bifid、方陣2枚が自由（塊の設定79） | 79すべてで矛盾 | 26/26 | 100本中14も全設定で矛盾 |
| Playfairの後にずらしのmask | 0 | 40/40 | 0 |
| ずらしのmaskの後にPlayfair | 不可能：同じ文字が並んだ暗号文の対（組み方ごとに5、2、3） | — | — |
| 鍵語の方陣＋ずらしのmask | 0（偶然の期待0.00015） | 36/36 | 0、0、0 |
| 格子のずらし：鍵の文字／文章の配置 | 26,964中0／234中0 | 120/120、60/60 | 2,000本中0 |
| 格子の周期鍵 | 381中114が通過、シャッフル平均128.5 | — | 濃縮なし |

## 現在わかっていること

Wを区切りとみても、方陣の暗号は開きません。Four-square、Two-square、Bifid、CM-Bifidの鍵語の方陣と自由な方陣、どちらの順のPlayfair＋ずらしのmask、鍵語の方陣＋mask、5×5格子上のずらし・回転・鏡映は、判定できる範囲ではすべてcribと両立しません。どれも論理的な反証で、でたらめな暗号文もたいてい同じく落ちます。

## 図で見る

![Wを除いたK4での方陣の族10個の状態。8つは論理的に閉、方陣1枚のBifidは検出力つきで閉、長い周期の自由な方陣2枚は判定できない](/assets/kryptos-k4-w-squares.svg)

## この研究が示すこと

- 暗号側の方陣がどんなものでも、Four-squareではcribを作れません。どこかの升に2文字が入るか、どこかの文字が2つの升に入るからです。
- Two-squareは形そのもので落ちます。標準の角の取り方では、出力の文字が平文の文字と同じになるのは、もう一方も同じになるときだけですが、K4には片方だけ同じ対があります（AS→KS、CK→PK、ST→SS）。入れ替え型では2つの入れ替えが同時に起きるはずですが、RT→PRは片方だけです。
- Playfairは同じ文字が並んだ対を出力しないので、最後の段にはなれません。K4にはどの組み方でもそういう対があります。Playfairの後にずらしのmaskをかける形も成り立ちません。
- 焼きなましで判定できなかったCM-Bifidは、cribだけで厳密に判定できました。

## この研究が示さないこと

これらの族の下で、K4がでたらめより起きにくいことは示しません。未決のまま残るのは、長い周期の自由な方陣2枚、位置ごとに自由に選ぶ対称、2回がけのDoppelkasten（[別のNote](/ja/research/kryptos-k4-consistency/)で扱った）です。

## 何が変わったか

見落としの一覧に残っていた最後の判定できる別方式、Wを区切りとみた方陣の族が閉じました。CM-Bifidは、焼きなましを厳密な解き手に替えて、「判定できない」から「閉」になりました。

## 何が失敗したか

焼きなましではCM-Bifidを判定できませんでした（植え込みの英文を35〜75%しか戻せない）。厳密な解き手が必要でした。自由なFour-squareのスクリプトはコミットより先に実行しており、内部記録に手順の抜けとして残しています。判定は決定的で、ここで再実行しています。

## 証拠の範囲

公開K4暗号文とcribです。自由なFour-squareの判定、Two-squareの反例、同じ文字の対はK4だけを使い、再実行できます。鍵語の探索、Two-squareとCM-Bifidの厳密な解き手、焼きなまし、maskの探索は結果を記録していますが、公開パッケージには入っていません。

## まだ分からないこと

そもそもWが区切りなのか。長い周期の自由な方陣2枚を判定できる解き手があるか。外部の独立replicationは0件です。

## この結論が崩れるとき

閉じた族のどれかで、24のcrib文字を再現する方陣と組み方が見つかれば、対応する行は覆ります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-squares)：`python verify_w_squares.py` はWを除き、自由なFour-squareの判定（植え込み200本とシャッフル2,000本つき）をやり直し、各組み方でTwo-squareの反例と同じ文字の対を見つけて、`PASS` を出します。標準ライブラリだけで約1秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、ここで再実行しない探索を含む記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-squares)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

鍵語の方陣と自由な方陣1枚については計画はありません。長い周期の自由な方陣2枚は、扱える厳密な解き手ができれば試します。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
- 方陣の暗号：American Cryptogram Associationの暗号の種類の説明（[ACA](https://www.cryptogram.org/resource-area/cipher-types/)）。
