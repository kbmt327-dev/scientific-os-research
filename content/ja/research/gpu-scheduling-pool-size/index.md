---
research_id: GPU-SCHED-EP-0005
title: 安全境界はプールが大きいほど下がる
date: 2026-09-13
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 合成シミュレーション
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: 封印した予測1本（PRED-006）、プール規模32〜512サーバでの比率掃引294回
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 32〜512サーバの合成マルチサーバジョブモデル、rho 0.85、指数サービス時間、再開コスト0、背景需要は1種類の形のみ
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0005
source_episode_sha256: 3e72377d2a441966354b8c935104108933c5db8f863c2f22d3c9596edc87a680
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification, japanese]
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>サイズ優先方式が壊れる条件を、実データで確かめる</span><a href="/en/research/gpu-scheduling-pool-size/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成シミュレーション</span><span>探索的</span><span>査読なし</span><span>外部再現 0</span></div>

> [!warning] この研究の結論は、次の研究で変数を取り違えていたと判明しました
> ここで測った「プールが大きいほど安全境界が下がる」という**観測そのものは有効**ですが、**原因の指定が誤り**でした。[[ja/research/gpu-scheduling-concurrency/index|EP-0006]]が交絡を分離し、効いていたのはプールのサーバ数ではなく、そのプールを同時に取り合っているジョブの本数だと示しています。この研究の数値を引用する前にEP-0006を読んでください。さらに境界の測り方そのものが[[ja/research/gpu-scheduling-blind-detector/index|EP-0011]]で無効と判明し、[[ja/research/gpu-scheduling-alpha-boundary/index|EP-0012]]で置き換えられています。

## 現在わかっていること

前の研究（[[ja/research/gpu-scheduling-real-traces/index|EP-0004]]）は、64サーバのプールで「最大ジョブがプール容量の0.75まで」という安全側の目安を出しました。同時にその研究は、自分の予測が1本だけ外れたことも記録しています。外れ方には向きがありました。**比率が同じなら結果も同じ**という不変性は近似にすぎず、ずれは「**大きいプールほど危険**」という側に系統的だったのです。

実在のGPU仮想クラスタは217〜603サーバで、64よりずっと大きい。だから目安の0.75が実規模でも成り立つかは、測らないと分かりません。

測りました。**成り立ちません。**安全境界はプール規模とともに単調に下がり、32サーバで0.81、512サーバで0.50になります。前の研究が実測比率0.59で見積もった害「1GPUジョブの7.4倍」も、実規模では**16.3倍**でした。およそ2倍の過小評価です。

ただし、この研究にはもう一つ記録すべきことがあります。**プール規模を変えると、同時に3つの量が動いていました。**サーバ数、背景ジョブクラスの数、そしてプールを同時に取り合うジョブの本数です。封印した文書にはその交絡を自分で宣言してあります。したがってここで言えるのは「プール規模とともに境界が下がる」という**相関**であって、原因の指定ではありません。次の研究がその分離をします。

## 図で見る

<div class="ratio-figure" aria-label="プール規模ごとの安全境界"><div class="ratio-track"><i style="left:50%"></i><i style="left:68.75%"></i><i style="left:81.25%"></i></div><div class="ratio-labels"><span style="left:50%"><b>0.50</b> 512サーバ</span><span style="left:68.75%"><b>0.69</b> 128サーバ</span><span style="left:81.25%"><b>0.81</b> 32サーバ</span></div></div>

横軸は「最大ジョブが必要とするサーバ数 ÷ プール容量」です。プールが大きくなるほど、許される比率は左へ動きます。実在の仮想クラスタは217〜603サーバで、この図の左寄りの領域にあります。

## この研究が示すこと

- この合成モデルでは、大ジョブクラスが自分の到着に追いつける最大の比率は、プール規模とともに単調に下がる。32 / 64 / 128 / 256 / 512サーバに対し 0.8125 / 0.75 / 0.6875 / 0.625 / 0.50。
- 前の研究が64サーバで測った害の倍率は、実在の仮想クラスタに近い規模では約2倍の過小評価だった。
- 予約型のEASY backfillは、この軸でも大ジョブクラスを飢餓させない。

## この研究が示さないこと

- **原因を特定していません。**プール規模を変えると背景クラス数と同時実行ジョブ数も動きます。封印時にこの交絡を宣言してあり、次の研究で分離します。
- 実際の到着列でスケジューリング方式を動かしていません。合成モデルの中の話です。
- 負荷はrho 0.85のみ、サービス時間は指数分布のみ、背景需要の形は1種類のみです。

## なぜ重要か

前の研究は「最大ジョブがプール容量の0.75まで」という、そのまま運用に渡せる形の数字を出しました。数字が運用に渡せる形をしているほど、それが測られた条件の外で使われます。

64サーバは、実在の仮想クラスタのどれよりも小さい。**目安を出した条件が、その目安を使いたい条件を含んでいなかった**のです。この研究はその隙間を埋めにいき、目安が規模に依存することを見つけました。

## 何を調べたか

1. 前の研究が出した安全境界0.75は、実在のプール規模（217〜603サーバ）でも成り立つのか。
2. 成り立たないなら、境界はどちら向きに、どれだけ動くのか。

## 方法

小さいジョブの背景群に、`m` 個のサーバを要求する大きいジョブのクラスを1つ加え、確率0.002で到着させます。プール規模 `N` を 32 / 64 / 128 / 256 / 512 と変え、比率 `m/N` を0.50から1.00まで7点掃きます。rho 0.85、シードは小規模5本・大規模3本、計294回の実行です。

PRED-006として、SHA-256 `b78c62fd5f6db0c9032d5f0ce09da52e104919af20223578b194ff96ce9810f2` で封印しています。封印とは、結果を見る前に予測文と判定基準を確定し、ハッシュで固定することです。対応する結果ファイルが存在しない状態でコミットしました。

境界の判定には、大ジョブクラスの flow balance（そのクラスが自分の到着に追いついている度合い）が0.9以上かを使いました。**この判定器は後の研究で無効と判明しています**（[[ja/research/gpu-scheduling-blind-detector/index|EP-0011]]）。

## 結果

**境界はプール規模とともに単調に下がります。**

| プール規模 N | 32 | 64 | 128 | 256 | 512 |
|---|---|---|---|---|---|
| 安全境界（この判定器での） | 0.8125 | 0.75 | 0.6875 | 0.625 | 0.50 |
| プール全体ジョブのflow balance | 0.53 | 0.39 | 0.24 | 0.16 | 0.10 |

**実規模での害。** 前の研究は64サーバで、実測比率0.59のジョブが1サーバジョブの7.4倍遅くなると報告しました。256サーバで比率0.625を測ると**16.3倍**です。目安を実規模へ持ち出すと、害の見積もりは約2倍になります。

**比率の効果はプール規模の効果より大きい。** 比率を0.5から1.0へ動かしたときのflow balanceの変化幅は0.872、プール規模を32から512へ動かしたときは0.475でした。どちらも効きますが、比率が主です。

**EASY backfillはこの軸でも壊れません。** 最小のflow balanceは512サーバ・プール全体ジョブで0.925でした。飢餓の目安を割っていません。ただし封印文では「0.99以上」と予測しており、そこは外れています。

## 何が変わったか

- 前の研究の「最大ジョブがプール容量の0.75まで」という単一の目安を、**プール規模ごとの表**へ置き換えました。
- 実規模での害の見積もりを7.4倍から16.3倍へ改訂しました。

## 何が失敗したか

**PRED-006は8本中6本的中。** 外れた2本のうち、EASY backfillの下限予測（0.99以上）は0.925で外れました。この方式は「一度も破綻していない」と繰り返し書いてきたので、下限を楽観的に置きすぎていたことになります。破綻はしていませんが、鈍感でもありません。

**4件目の計測器の問題を検出しました。** プール規模を横断して比較しようとして、測定窓の長さが条件ごとに変わっていることに気づきました。固定ジョブ数で走らせると、観測窓は `ジョブ数 ÷ 到着率` なのでプールが大きいほど短くなります（32サーバで2,296、512サーバで232の時間単位）。滞留量の絶対値が窓に頭打ちされ、傾向が逆に見えていました。率で測るか窓長で正規化する必要があります。

**そして最も重要な失敗は、この研究の結論そのものにあります。** 封印文に交絡を自分で宣言しておきながら、結論は「プール規模が効く」という断定形で書きました。次の研究が分離すると、効いていたのは別の変数でした。宣言があったので追跡できましたが、その間この研究の結論は誤った変数で書かれていたことになります。

## 証拠の範囲

**言えること：** この合成モデルの中では、大ジョブクラスが追いつける最大比率はプール規模とともに単調に下がり、64サーバで測った害の倍率は実規模では約2倍になる。

**言えないこと：** 原因の特定。プール規模・背景クラス数・同時実行ジョブ数が一緒に動いています。また実トレース上でスケジューリング方式を走らせていません。境界の判定に使った統計量は、後の研究で無効と判明しています。

## まだ分からないこと

- 境界を決めているのは、サーバ数そのものか、背景クラスの数か、同時に走っているジョブの本数か。
- N = 1024以上で境界が0.5で飽和するのか、さらに下がるのか。
- 負荷rhoを変えたときの動き。
- 再開コストが0でないときとの相互作用。

## この結論が崩れるとき

- 同時実行ジョブ数を固定したままプール規模だけを変えて、境界が動かない。**この通りになりました。**
- 背景クラス数を固定したままプール規模を変えて、境界が動かない。
- 境界の判定に別の統計量を使うと、規模依存が消える。

## 自分で確かめる

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

完全な再実行：

```bash
cd reproduction/gpu-scheduling-boundary
python run_e7.py
python analyze_e7.py
```

## 証拠とデータ

- [公開再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [封印済みPRED-006](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-006.json)
- [E7の採点](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E7_grading.json)
- 内部の元Episodeのハッシュ：`3e72377d2a441966354b8c935104108933c5db8f863c2f22d3c9596edc87a680`

## 外部からの検証

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決の批判：0

## 次の実験

封印文で自分が宣言した交絡を解きます。プール規模・背景クラス数・同時実行ジョブ数のどれが境界を決めているのかを、それぞれ独立に動かして分離します。

## ここに至るまで

<div class="revision-chain vertical" aria-label="GPUクラスタのスケジューリング研究の更新履歴">
  <a href="/ja/research/gpu-scheduling/"><b>EP-0001</b><span>推定誤差と再実行コストで、最良の方式が入れ替わる。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>平均は良いのに、一部のジョブクラスが終わらない。安定性の判定器も3回壊れた。</span></a>
  <a href="/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>飢餓を決めるのは平均ジョブ幅ではなく、クラスタ全体を要するジョブの有無。</span></a>
  <a href="/ja/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>実測したプールにその条件はなく、害は飢餓ではなく数倍の遅れだった。</span></a>
  <a class="current" href="/ja/research/gpu-scheduling-pool-size/"><b>EP-0005 · 現在地</b><span>安全境界はプールが大きいほど下がる。実規模の害は2倍過小評価だった。</span></a>
  <a href="/ja/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>実クラスタの位置で測り、4本ぶん載せてきた機構説明を訂正した。</span></a>
  <a href="/ja/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>背景の粒度を変えるだけで、この研究の看板結論が消えた。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>代表成果だった相図の軸そのものが、18倍交絡していた。</span></a>
  <a href="/ja/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>「2つの数で決まる」を撤回した。頻度が第三の変数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった。</span></a>
  <a href="/ja/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>動かない境界を持つ統計量へ置き換え、運用数値を戻した。</span></a>
  <a href="/ja/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>実クラスタについての主張は、19,100本中1本のジョブに乗っていた。</span></a>
</div>
