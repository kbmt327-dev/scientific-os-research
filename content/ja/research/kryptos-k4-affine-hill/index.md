---
research_id: KRYPTOS-K4-EP-0117
title: 文に沿って変わるアフィンやHillの行列は、K4に合うか
date: '2026-09-27'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 位置で変わるアフィンは0件。周期で変わるHillは判定できる91設定すべてで矛盾し、文章から作る行列では0件。自由な行列の69設定は判定できない
evidence_level: 公開暗号文とcribでの厳密な判定。陽性対照とシャッフルのnullつき。スクリプトは回す前にコミット
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開K4暗号文と公開crib 24文字。行列の行と多項式の係数の厳密な列挙、植え込みの陽性対照、並べ替えた暗号文のnull
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 乗数とずれ幅が述べた位置の規則に従うアフィン、2×2・3×3の行列が周期で変わるHill（自由な行列、または一覧の文章から作る行列）。復号はなく、新しい平文文字もない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0117
source_episode_sha256: a144b37aabc5f6703259d27b056e2365f74b91003c8daffcc10d87273192f622
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-affine-hill/" hreflang="en">English</a></p>

## 何を調べたか

算術のままで表のずらしの形から出る方法は2つあります。足すだけでなく掛ける（C＝a·P＋bで、aが文に沿って変わる）か、塊を行列で暗号化し（Hill）、その行列を塊ごとに変えるかです。どちらかがK4のcribに合うか。

## なぜ重要か

乗数が一定なら、アフィンは1枚の表のずらしのままで、K1〜K3変種です。乗数が位置で変わるときだけ別方式になります。行列の変わるHillは塊の中で文字を混ぜ、これはどんなずらしの表もしません。どちらも、規則を決めればcribで判定できます。

## 方法

- **アフィン（EP-0117）。** 乗数とずれ幅を位置の2次以下の多項式（mod 26）にします。乗数は97位置すべてで可逆（1,896通り）、ずれ幅は17,576通り。数はA–ZかKRYPTOSのalphabetで、暗号化の向き（C＝aP＋b）と復号の向き（P＝aC＋b）。ほかに指数の乗数 a₀·gⁱ と、乗数が一定で走り鍵のずれ幅。
- **周期で変わるHill（EP-0117）。** 各起点から2文字か3文字の塊に切り、塊tは行列 M(t mod p) を使います。p＝1〜8、定数ベクトルの有無、2つの番号。各行列の各行をcribの塊に対してすべて列挙し、可逆な組み合わせを探します。標本をとらない厳密な判定です。シャッフル100本のうち両立か未決が5本以下の設定を「判定できる」としました。
- **文章から作る行列のHill（EP-0122）。** 同じ160設定で、一覧の文章のあらゆる開始位置から行列を作りました。2,378,384設定×開始位置。
- **対照。** 植え込みのアフィンとHillの暗号文、並べ替えたK4。

## 結果

| 族 | K4 | 対照 | シャッフル |
|---|---|---|---|
| アフィン、多項式の乗数とずれ幅（両方の番号、両方の向き） | 0件 | 20/20 | 20本中0 |
| アフィン、指数の乗数 | 0件 | 20/20 | 20本中0 |
| 乗数が一定、走り鍵のずれ幅（K1〜K3変種） | 最良9/24 | 6/6 | 最良9〜10/24 |
| 周期で変わるHill、判定できる91設定 | 91すべてで矛盾 | 40/40 | 設定ごとに100本中5以下 |
| 周期で変わるHill、残りの69設定 | シャッフルと同じ（両立24、未決13） | — | 100本中6〜100 |
| 文章から作る行列のHill（160設定） | 2,378,384中0（偶然の期待8×10⁻²¹） | 30/30 | 0、0、0 |

鍵の候補として挙げられることのある彫刻のtableauの余分なLは、表として引く30列の外にあり、表の升を1つも変えません。

## 現在わかっていること

乗数が多項式や指数の規則で文に沿って変わるアフィンは、K4に合いません。周期で変わるHillの行列は、判定できるどの設定でもcribと矛盾し、行列を一覧の文章から作ると何も出ません。開いたまま残るのは、1つの行列がcribの塊を1つか2つしか受け持たない場合の、自由な行列のHillです。

## 図で見る

![周期で変わるHillの160設定の積み上げ棒。91がK4で判定でき矛盾、69が判定できない。下に、文章から作る行列では2,378,384中0件、多項式のアフィンは0件という説明](/assets/kryptos-k4-affine-hill.svg)

## この研究が示すこと

- 乗数が多項式（2次以下）か指数のアフィンは、どちらの向き・番号でも、cribを再現しません。
- ベクトルなしの2×2の周期Hillは、周期1〜8、両方の起点、両方の番号のすべてで矛盾します。3×3やベクトルつきでも、行列ごとのcribの塊が足りる所では同じです。
- 行列を一覧の文章から取ると、自由な行列では判定できなかった設定も閉じます。

## この研究が示さないこと

K4がでたらめより起きにくいことは示しません。判定できる所では、シャッフルも落ちます。周期の長い自由な行列のHill、走り鍵から取る乗数、一覧にない文章から作る行列は判定していません。

## 何が変わったか

カタログの3項目（位置で変わるアフィン、周期で変わるHill、tableauの欠陥）が、判定できる範囲で閉じました。tableauの欠陥は「数升に影響する」としていた記述を「影響する升はない」に直しました。

## 何が失敗したか

Hillの69設定では、1つの行列が受け持つcribの塊が少なすぎ、どの検定でも判定できません。そこではK4はシャッフルとまったく同じに振る舞います。

## 証拠の範囲

公開K4暗号文とcribです。多項式のアフィンとベクトルなしの2×2 HillはK4だけを使い、公開パッケージで再実行します。3×3やベクトルつきの形、指数と走り鍵のアフィン、文章の行列の探索は結果を記録しており、再実行していません。

## まだ分からないこと

cribが長ければ、周期の長い自由な行列のHillが判定できるか。外部の独立replicationは0件です。

## この結論が崩れるとき

24のcrib文字をすべて再現する多項式のアフィンの規則か、周期のHillの行列の組が見つかれば、対応する行は覆ります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-affine-hill)：`python verify_affine_hill.py` は、多項式のアフィンの判定（1,896×17,576の規則、4つの形）と2×2の周期Hillの判定（32設定）を、植え込みと並べ替えた文とともにK4でやり直し、`PASS` を出します。標準ライブラリだけで約40秒です。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[コード、記録した結果、図のスクリプト](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-affine-hill)。MITライセンスです。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

これらの族の中ではありません。周期の長い自由な行列のHillは、行列を作る規則を決めないと判定できません。

## 出典

- K4の暗号文とcrib：Jim Sanborn, *Kryptos*（1990）。[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)、[Elonka Dunin](https://elonka.com/kryptos/)、[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020。
- Hill暗号：Lester S. Hill, "Cryptography in an Algebraic Alphabet", *The American Mathematical Monthly* 36（1929）。
