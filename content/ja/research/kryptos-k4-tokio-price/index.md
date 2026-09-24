---
research_id: KRYPTOS-K4-EP-0011
title: K4のWをTOKIOと読むことには、どれだけの価値があるか
date: '2026-09-19'
lang: ja
domain: Kryptos K4
type: Finding
status: Passed an exact null at p ≤ 1.5e-3; exploratory; gives no plaintext
evidence_level: Exact closed-form null against a place list frozen before testing
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the place names on Berlin's World Clock, frozen from the designer's site before the test was written
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: A statement about where the Ws fall in K4; not about the encryption method,
  and the choice of the World Clock as the target list is not paid for
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0011
source_episode_sha256: eb6a82b83152b062f74ae6456b075e7a0a526f4249852fcca701c3095adbcc3e
publication:
  status: publishable
tags:
- kryptos-k4
- multiplicity
- exact-null
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-tokio-price/" hreflang="en">English</a></p>

## 現在わかっていること

K4の5つのWの間隔を先頭から数えると20・15・11・9・15で、文字に直す（A=1）と `TOKIO` になります。これはTokyoのドイツ語綴りで、ベルリンの世界時計に刻まれている地名です。`BERLINCLOCK` はK4の公開cribの1つです。間隔の読み方の自由度をすべて払うと、「並べ替えたK4のどれかの読みが、時計のどれかの地名に当たる」確率は最大で **1.48×10⁻³** です。最初の見積もりより88倍弱い値です。差はまるごと「短い地名も当たりとして受け入れるか」から来ており、`ROM` の1件だけで値段の70%を占めます。この読みは、K4の暗号化の方法については何も語りません。

## 図で見る

![対数目盛の棒グラフ：名指しした1標的で1.11e-6、5文字の地名17件で1.68e-5、到達可能な全長の地名で1.48e-3。積み上げ棒：3文字69.7%、4文字29.1%、5文字1.1%](/assets/kryptos-k4-tokio-price.svg)

上の棒は、自由度を払うごとの値段の変化です。下の棒は、最終的な値段を受け入れた地名の長さで分けたものです。

## この研究が示すこと

- 標的のリストは有限で外部にあります。時計の設計者Erich Johnの公式サイトにある146件の地名で、検定コードを書く前に凍結しました。5文字の地名は17件です。
- nullは閉じた形で解けます。m回出る文字は97セルから一様に選ばれたm個の位置にあり、どの読みも逆算できるので、当たりの期待数は有限の和になります。シミュレーションも外挿も要りません。
- 最初の見積もりが選んで固定していた出現回数と標的の長さを払うと、値は1.68×10⁻⁵から1.48×10⁻³へ動きます。
- K2の暗号文とK3の平文の窓から出る約36,000本の文字列には、地名が1つも出ません。厳密なnullでの期待は0.76本なので、これは証拠の追加ではなく計算の検算です。

## この研究が示さないこと

確証的なp値ではありません。世界時計を標的のリストに選んだのはcribがそれを指した後であり、その選択は枚挙できません。鍵も経路も平文の1文字も出ません。同じ5つのW位置についての他の観察とは独立ではありません。

## 何を調べたか

`TOKIO` の読みは、「意味のある5文字列」を定義できないという理由で未検定のままでした。crib `BERLINCLOCK` が世界時計に結びついたことで、時計の地名リストを外部の標的集合として使えるようになりました。自由度をすべて払ったとき、この集合に対して読みの価値はどれだけか。

## なぜ重要か

目を引くパターンの価値は、見つけるのに使った自由度で決まります。ここでは最初の見積もりの算術は正しく、足りなかったのは枚挙の外に残っていた2つの選択でした。それを、結果の上に何かを積む前に見つけて払いました。

## 方法

- **標的集合。** 設計者サイトの146件（Internet Archive、2020年8月12日の取得）を、検定コードより前にhash付きで凍結。
- **読みの族。** K4にある出現回数すべて（1–6回と8回）、間隔の定義（間の文字数／差）、4つの起点（先頭・0・巡回・なし）、2つの向き、A=1とA=0。この族で届く長さは1–8文字で、146件中95件がその長さです。
- **厳密なnull。** 地名ごとに「その地名を生む位置集合の数 × その出現回数の文字数 ÷ C(97, m)」を足します。Markovの不等式で P(1件以上) ≤ E[当たり数] です。
- **検算。** 逆像を合成テキストに埋め込んで確認（580件中580件が再現）。5文字版を2,000,000回のシミュレーションで回し、期待33.7件に対して29件（−0.8σ）。

## 結果

K4からはこの族で69本の相異なる文字列が出て、そのうち1本 `TOKIO` がリストにあります。

| 受け入れる地名の長さ | 厳密な P(1件以上) |
|---|---|
| 到達可能な長さすべて | **1.48×10⁻³** |
| 5文字以上 | 1.75×10⁻⁵ |
| 5文字ちょうど | 1.68×10⁻⁵ |

長さ別の内訳は、3文字69.7%（`ROM` のみ）、4文字29.1%（12件）、5文字1.1%（17件）、6文字以上0.04%です。`OSLO` はKryptosより後の1997年に時計へ追加されたので、除くと1.44×10⁻³です。

## 何が変わったか

最初の見積もり（シャッフルのシミュレーションから、標的1つあたり1.11×10⁻⁶）を厳密値に置き換え、推測していた標的リストの大きさを出典から数えました。代表値は約1.7×10⁻⁵から1.48×10⁻³へ動きました。

## 何が失敗したか

最初の200,000回のシミュレーションは当たり0件で、そのまま書けば「p < 1.5×10⁻⁵」を支持していました。厳密値の予測は3.4件で、0件は運のいい引きでした（確率0.034）。回数を増やしたシミュレーションは厳密値と一致しました。

## 証拠の範囲

公開暗号文と公開された地名リストです。Kryptos（1988–1990年）に対応するのは1985–1997年の時計（134件）ですが、この版は列挙できておらず、1997年以降の146件を使いました。値段を決めているのは1969年から載っていたはずの主要都市の短い名前なので、結論は版に対して頑健なはずですが、これは論証であって測定ではありません。

## まだ分からないこと

1985–1997年版の正確なリスト。Wが意図して置かれたかどうか。この読みと暗号化の方法とのつながり。外部の独立replicationは0件です。

## この結論が崩れるとき

1985–1997年版に `TOKIO` がなければ、この読みは標的を失います。見る前に決めた根拠のある標的リストで、普通の文章でも同程度に当たるなら、この値にはほとんど意味がありません。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-tokio-null)：`python verify_tokio_null.py` は、文字だけの地名リストから厳密なnullを標準ライブラリで1秒以内に計算し直し、記録した結果と一致すれば `PASS` を出します。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[読みの族、閉じた形のnull、文字だけの地名リスト、記録した結果](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-tokio-null)。コードと結果はMITライセンスです。暗号文は引用であり、地名は出典から取った事実のデータで、どちらもライセンスの対象外です。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

当時の写真や記録から1985–1997年版の134件を列挙し、計算し直す。

## 出典

- K4暗号文：Jim Sanborn, *Kryptos*（1990）。公開された転記：[Wikipedia「Kryptos」](https://en.wikipedia.org/wiki/Kryptos)、[Elonka DuninのKryptosページ](https://elonka.com/kryptos/)。
- W区間の読み `20, 15, 11, 9, 15 → TOKIO`：[matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0)。
- `BERLINCLOCK` がベルリンの世界時計を指すこと：[Scientific American、2025年](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/)。
- 地名とリストの沿革（1969年に80件、1985年以降はドイツ語綴りで134件、1997年以降146件）：設計者Erich Johnの公式サイト [weltzeituhr-berlin.de](https://weltzeituhr-berlin.de/en/places-worldtimeclock)、[Internet Archive経由](https://web.archive.org/web/20200812142431/https://weltzeituhr-berlin.de/en/places-worldtimeclock)。
- `OSLO` の1997年追加：*Berliner Zeitung*、1997年12月12日。
