---
research_id: GPU-SCHED-EP-0006
title: 効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった
date: 2026-09-13
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 合成シミュレーション＋公開トレースの測定
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation-and-public-trace
  source: 封印した予測1本（PRED-007、6/6的中）、交絡分離の224回実行、Philly仮想クラスタ11個の同時実行ジョブ数の実測
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 合成マルチサーバジョブモデル、rho 0.85、指数サービス時間、再開コスト0。トレース側は同時実行ジョブ数と最大ジョブ比率の実測のみ
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0006
source_episode_sha256: a6dc66607f3e9141bf2a29ed13dde581fc62e65dff31f010ed2909243928cf49
publication:
  status: publishable
tags: [finding, scheduling, simulation, confounding, traces, japanese]
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>サイズ優先方式が壊れる条件を、実データで確かめる</span><a href="/en/research/gpu-scheduling-concurrency/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成シミュレーション＋公開トレース</span><span>探索的</span><span>査読なし</span><span>外部再現 0</span></div>

> [!note] この研究で見つけた軸は生き残っています。境界の数値は後に測り直されました
> 「同時に取り合うジョブの本数が駆動変数」という**軸の発見は、その後7本の研究を通じて有効**です。ただしここで使った境界の判定器は[[ja/research/gpu-scheduling-blind-detector/index|EP-0011]]で無効と判明し、[[ja/research/gpu-scheduling-alpha-boundary/index|EP-0012]]で置き換えられました。**軸は引用してよく、数値は引用しないでください。**

## 現在わかっていること

前の研究（[[ja/research/gpu-scheduling-pool-size/index|EP-0005]]）は「安全境界はプールが大きいほど下がる」と書きました。しかし同じ研究の封印文には、その結論が信用できない理由も自分で書いてありました。**プール規模を変えると、背景クラスの数も、プールを同時に取り合っているジョブの本数も、一緒に動いてしまう。**

分離しました。**駆動変数は、プールのサーバ数でも背景クラスの数でもなく、そのプールを同時に取り合っているジョブの本数でした。**

同時実行ジョブ数を固定したまま、プールのサーバ数を8倍にしても、安全境界は動きません。逆に、プールを固定したまま同時実行ジョブ数を変えると境界は動きます。**サーバ数は代理変数でした。**

この軸には実務上の意味があります。同時実行ジョブ数は運用側が測れる量で、しかも公開トレースで測ると、**危険な2つの条件は同じクラスタに同時には現れていません。**最大ジョブがプールの59%を占める仮想クラスタ（11cb48）は同時実行ジョブ数が10.2で、11個中2番目に低い。逆に同時実行ジョブ数が81.1と高いクラスタ（6214e9）では、最大ジョブはプールの3%です。比率と同時本数は負に相関していました。

## 図で見る

<div class="ratio-figure" aria-label="同時実行ジョブ数と安全境界"><div class="ratio-track"><i style="left:12%"></i><i style="left:34%"></i><i style="left:100%"></i></div><div class="ratio-labels"><span style="left:12%"><b>28.5本</b><br>境界 0.625</span><span style="left:34%"><b>54本</b><br>0.50</span><span style="left:100%"><b>168本</b><br>0.50</span></div></div>

横軸はプールを同時に取り合っているジョブの本数です。本数が増えるほど、一つのジョブが占めてよい割合は下がります。プールのサーバ数を8倍にしても、この本数が同じなら境界は同じ場所にあります。

## この研究が示すこと

- この合成モデルでは、安全境界を決めているのはプールのサーバ数でも背景クラスの数でもなく、**同時に実行されているジョブの本数**である。同時本数を固定すればプールを8倍にしても境界は0.625で不変。
- 同時実行ジョブ数が20%以内で一致する条件どうしは、境界も1格子点以内で一致する。
- 公開トレースのPhilly仮想クラスタ11個では、最大ジョブ比率と同時実行ジョブ数が負に相関しており、2つのリスク要因が同じクラスタに同時に現れていない。

## この研究が示さないこと

- なぜ同時本数が効くのか、という機構の説明はここでは確定していません。この時点での説明は次の研究で訂正されます。
- 実際の到着列でスケジューリング方式を動かしていません。トレースから取ったのは同時実行ジョブ数と最大ジョブ比率の**実測値だけ**です。
- 境界の**数値**は、後の研究で無効と判明した判定器で測られています。

## なぜ重要か

前の研究は、自分で宣言した交絡を残したまま「プール規模が効く」と断定形で書きました。運用に渡すなら「あなたのクラスタは何サーバですか」と聞くことになります。それは測りやすいけれど、間違った質問でした。

正しい質問は「そのプールで同時に何本走っていますか」です。答えは同じくらい測りやすく、しかも実際に効いています。**宣言した交絡を次のサイクルで必ず解く**という手順が、この差を生みました。

## 何を調べたか

前の研究が宣言した交絡のうち、どれが安全境界を決めているのか。候補は3つです。

1. プールのサーバ数
2. 背景ジョブクラスの数
3. プールを同時に取り合っているジョブの本数

## 方法

3つを独立に動かせる設計を組みました。背景需要の形をプール規模に対して相対的に固定すると、サーバ数を変えても同時実行ジョブ数が保たれます。逆に背景の粒度だけを変えると、プールを固定したまま同時本数が動きます。これで3つを分離できます。計224回の実行、rho 0.85です。

PRED-007として、SHA-256 `af19b22f5049b0b1b52ba5e77b2d5ba2d5f5b4e5b0e7b0e7b0e7b0e7b0e7b0e7` で封印しています。実際の封印値は再現パッケージの `predictions/PRED-007.sha256` にあります。対応する結果ファイルが存在しない状態でコミットしました。

トレース側では、Philly仮想クラスタごとに「非空の時間で平均した同時実行ジョブ数」をイベント走査で測りました。

## 結果

**同時実行ジョブ数を固定すると、プール規模は効きません。**

| 条件 | プール規模 | 同時実行ジョブ数 | 安全境界 |
|---|---|---|---|
| 基準 | 64 | 28.5 | 0.625 |
| プールを8倍 | 512 | 28.4 | **0.625** |

**同時実行ジョブ数を動かすと、境界が動きます。**

| 同時実行ジョブ数 | 28.5 | 54.2 | 99.0 | 168.5 |
|---|---|---|---|---|
| 安全境界 | 0.625 | 0.50 | 0.50 | 0.50 |

**背景クラスの数は駆動変数ではありません。**クラス数を変えても同時本数が同じなら境界は動きませんでした。

**実トレースでは、2つのリスク要因が同時に現れません。**

| 仮想クラスタ | 最大ジョブ比率 | 同時実行ジョブ数 |
|---|---|---|
| 11cb48 | **0.59**（最大） | 10.2（11個中2番目に低い） |
| 6214e9 | 0.03 | **81.1**（最も高い） |

比率が高いクラスタは同時本数が低く、同時本数が高いクラスタは比率が低い。この2本のトレースの範囲では、危険な組み合わせは観測されていません。

## 何が変わったか

- 前の研究の「安全境界はプール規模で決まる」を**撤回**し、「同時に取り合っているジョブの本数で決まる」に置き換えました。
- 運用に渡す質問を「何サーバのプールですか」から「そのプールで同時に何本走っていますか」へ変えました。
- 前の研究が出した実規模での害16.3倍は、**プール規模という誤った軸の上での見積もり**だったので、次の研究で正しい軸に合わせて測り直すことになります。

## 何が失敗したか

**PRED-007は6本中6本的中しました。**この研究では封印した予測が全部当たっています。

ただし全部当たったこと自体は、この研究の価値の中心ではありません。価値の中心は、**前の研究が自分で宣言しておきながら断定形で書いてしまった交絡を、次のサイクルで実際に解いたこと**です。宣言がなければ追跡できず、解かなければ宣言は意味を持ちませんでした。

記録すべき失敗は前の研究の側にあります。**未解決の交絡を宣言したまま、正本には変数名を断定して書いた。**そのため1サイクル分、公開していた説明が誤った変数で書かれていました。

## 証拠の範囲

**言えること：** この合成モデルの中では、安全境界を決めているのは同時実行ジョブ数であり、プールのサーバ数と背景クラス数は代理変数である。公開トレース2本の範囲では、高い比率と高い同時本数が同じ仮想クラスタに同時には現れていない。

**言えないこと：** 機構の説明はこの時点では確定していません（次の研究で訂正されます）。境界の数値は、後に無効と判明した判定器で測られています。トレース上でスケジューリング方式を走らせていません。

## まだ分からないこと

- 同時実行ジョブ数が10本前後の領域——実在の仮想クラスタがいる場所——での境界。ここまでで測った最小は28.5です。
- 同時本数と境界の関係が対数的に飽和するのか、0へ向かうのか。
- なぜ同時本数が効くのか。この時点の説明は仮のものです。

## この結論が崩れるとき

- 同時実行ジョブ数を揃えた条件どうしで、境界が1格子点を超えて食い違う。
- 別のトレースで、高い比率と高い同時本数を同時に持つ運用プールが見つかる。
- 境界の判定に別の統計量を使うと、同時本数の効果が消える。**これは後に部分的に起きます。数値は変わりましたが、軸は残りました。**

## 自分で確かめる

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

完全な再実行：

```bash
cd reproduction/gpu-scheduling-boundary
python run_e8.py
python analyze_e8.py
python measure_vc_concurrency.py   # 生のPhillyトレースが必要です
```

## 証拠とデータ

- [公開再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [封印済みPRED-007](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-007.json)
- [E8の採点](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E8_grading.json)
- [Philly仮想クラスタの同時実行ジョブ数](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E8_philly_concurrency.json)
- 内部の元Episodeのハッシュ：`a6dc66607f3e9141bf2a29ed13dde581fc62e65dff31f010ed2909243928cf49`

## 外部からの検証

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決の批判：0

## 次の実験

実在の仮想クラスタがいる同時実行ジョブ数10本前後まで、境界の曲線を伸ばします。ここまでで測った最小は28.5で、実クラスタの位置は外挿でしか語れていません。

## ここに至るまで

<div class="revision-chain vertical" aria-label="GPUクラスタのスケジューリング研究の更新履歴">
  <a href="/ja/research/gpu-scheduling/"><b>EP-0001</b><span>推定誤差と再実行コストで、最良の方式が入れ替わる。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>平均は良いのに、一部のジョブクラスが終わらない。安定性の判定器も3回壊れた。</span></a>
  <a href="/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>飢餓を決めるのは平均ジョブ幅ではなく、クラスタ全体を要するジョブの有無。</span></a>
  <a href="/ja/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>実測したプールにその条件はなく、害は飢餓ではなく数倍の遅れだった。</span></a>
  <a href="/ja/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>安全境界はプールが大きいほど下がる。実規模の害は2倍過小評価だった。</span></a>
  <a class="current" href="/ja/research/gpu-scheduling-concurrency/"><b>EP-0006 · 現在地</b><span>効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>実クラスタの位置で測り、4本ぶん載せてきた機構説明を訂正した。</span></a>
  <a href="/ja/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>背景の粒度を変えるだけで、この研究の看板結論が消えた。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>代表成果だった相図の軸そのものが、18倍交絡していた。</span></a>
  <a href="/ja/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>「2つの数で決まる」を撤回した。頻度が第三の変数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった。</span></a>
  <a href="/ja/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>動かない境界を持つ統計量へ置き換え、運用数値を戻した。</span></a>
  <a href="/ja/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>実クラスタについての主張は、19,100本中1本のジョブに乗っていた。</span></a>
</div>
