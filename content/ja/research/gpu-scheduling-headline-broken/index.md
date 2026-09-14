---
research_id: GPU-SCHED-EP-0008
title: 背景の粒度を変えるだけで、この研究の看板結論が消えた
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
  source: 封印した予測1本（PRED-009、5/5的中）、看板結論の設定を背景の粒度だけ変えた30回実行
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 64サーバの合成マルチサーバジョブモデル、rho 0.7、指数サービス時間、再開コスト0。EP-0003の原設定を固定し、背景需要の粒度のみを変えた
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0008
source_episode_sha256: 5b305fc7b433ae222efcd035c2760a6f5640d24b4f7497097729b9b65a0c93d7
publication:
  status: publishable
tags: [finding, scheduling, simulation, retraction, japanese]
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>サイズ優先方式が壊れる条件を、実データで確かめる</span><a href="/en/research/gpu-scheduling-headline-broken/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成シミュレーション</span><span>探索的</span><span>査読なし</span><span>外部再現 0</span></div>

## 現在わかっていること

[[ja/research/gpu-scheduling-starvation-mechanism/index|EP-0003]]以来、この研究の中心にあった結論はこれでした。

> 需要分布のsupport（取りうるジョブ幅の集合）がプール全体を含むと、そのクラスは飢餓する。30,000本中15本（確率0.0005）で十分であり、負荷rho 0.7でも起きる。

**壊しにいって、壊れました。**

同じプール規模、同じ負荷、同じスケジューリング方式、同じ「プール全体ジョブの確率0.0005」のまま、**背景ジョブの粒度だけを粗くします。**プール全体ジョブの流量は 0.307 から **0.997** になりました。平均待ち時間は400.9から**39.9**へ落ちました。飢餓は消えます。

何が変わったのかというと、同時にプールを取り合っているジョブの本数です。EP-0003の原設定は同時本数23.2でした。背景を粗くすると4.3になります。5.37倍の差です。

つまり**support（プール全体ジョブが存在するか）は代理変数でした。**原因は「そのジョブが、その時点の競合数に対して大きすぎるか」です。看板結論は間違いではなく、**同時実行ジョブ数に条件付けられた主張**だったのです。

## 図で見る

<div class="ratio-figure" aria-label="背景の粒度と飢餓の有無"><div class="ratio-track"><i style="left:30.7%"></i><i style="left:99.7%"></i></div><div class="ratio-labels"><span style="left:30.7%"><b>0.307</b> 細かい背景<br>同時23.2本・飢餓</span><span style="left:99.7%"><b>0.997</b> 粗い背景<br>同時4.3本・健全</span></div></div>

横軸はプール全体ジョブのflow balance（そのクラスが自分の到着に追いついている度合い）です。1.0なら追いついています。変えたのは背景ジョブの粒度だけで、プール規模も負荷もプール全体ジョブの確率も同じです。

## この研究が示すこと

- 同じ確率・同じプール規模・同じ負荷・同じ方式でも、**背景需要の粒度だけで飢餓は現れも消えもする**。流量0.307と0.997。
- 飢餓は需要分布のsupportそのものではなく、同時に競合しているジョブの本数に条件付けられている。
- 予約型のEASY backfillは、この操作に対して不感である（全背景で流量1.000）。

## この研究が示さないこと

- 同時実行ジョブ数が唯一の第二変数であることは、この研究では示していません。背景の粒度を変えると他の量も動きます。次の研究以降で、頻度と背景分布族という別の要因が見つかります。
- 判定に使ったflow balanceという統計量は、後の研究で無効と判明しました。ただしここでの差（0.307対0.997）は極端なので、判定線の置き場所には依存しません。
- 実トレース上でスケジューリング方式を動かしていません。

## なぜ重要か

この研究が壊した結論は、**この分野で最も強く、最も引用してきた自分の成果**でした。「クラスタ全体を占めるジョブがあるかを見よ」という形で運用にも渡していました。

条件付けを外した主張は、条件の外で使われます。プール全体ジョブが存在するだけで危険だと読めば、そのようなジョブを禁止する運用が生まれます。実際には、同時に走っている本数が少なければ通ります。

**看板結論を、自分で壊しにいく実験を組む。**壊れなければ強くなり、壊れれば条件が見つかります。この場合は後者でした。

## 何を調べたか

このdomainの看板結論を、背景の粒度という一つの軸だけで壊せるか。

## 方法

EP-0003の原設定（64サーバ、rho 0.7、プール全体ジョブの確率0.0005、greedy SRPT）を完全に固定します。変えるのは背景ジョブ幅の分布の**粒度だけ**です。細かい背景（1、2、4…）、中間、粗い背景（8、16、32…）の3段階。各30,000ジョブ、計30回の実行です。

PRED-009として封印しています。digestは再現パッケージの `predictions/PRED-009.sha256` にあります。対応する結果ファイルが存在しない状態でコミットしました。

決定予測X2は「背景を粗くするだけで飢餓が消える」、つまり**自分の看板結論が条件付きであるという側**に指名してあります。当たれば看板が降格する、という帰結を封印文に書いてあります。

## 結果

| 背景の粒度 | 細かい | 中間 | 粗い |
|---|---|---|---|
| 同時実行ジョブ数 | 23.2 | — | 4.3 |
| プール全体ジョブの流量 | **0.307** | 0.868 | **0.997** |
| プール全体ジョブの平均待ち時間 | **400.9** | — | **39.9** |
| EASY backfillの流量 | 1.000 | 1.000 | 1.000 |

流量は粒度に対して単調です。同時実行ジョブ数の差は5.37倍でした。

## 何が変わったか

- 「supportがプール全体を含む ⇒ そのクラスは飢餓する」という看板結論を、**同時実行ジョブ数に条件付けられた主張**へ書き換えました。
- 「support」を原因から代理変数へ降格しました。原因は「そのジョブが、その時点の競合数に対して大きすぎるか」です。
- EP-0003の公開noteに訂正帯を付けました。

## 何が失敗したか

**PRED-009は5本中5本的中しました。**予測はすべて当たっています。

失敗は予測の側ではなく、**この結論を3本の研究にわたって条件付けずに載せ続けたこと**にあります。EP-0003の原設定が同時実行ジョブ数23.2という特定の点にいることは、EP-0006で軸が見つかるまで誰も測っていませんでした。

**新しい軸を見つけたら、過去の結論を全部その軸の上に置き直す必要があります。**EP-0006で駆動変数が判明した時点で、過去の各研究がその軸のどこにいたかは未確認でした。置き直したら看板結論が反転しました。

## 証拠の範囲

**言えること：** この合成モデルの中では、プール全体ジョブの飢餓は背景需要の粒度だけで現れも消えもし、EP-0003の看板結論は同時実行ジョブ数に条件付けられていた。

**言えないこと：** 同時実行ジョブ数が唯一の第二変数であること。判定に使った統計量の妥当性（後に無効と判明、ただしここでの差は極端なので結論は影響を受けません）。実トレース上での挙動。

## まだ分からないこと

- EP-0002の相図21セルも同じ形の交絡を持っているのではないか。θを動かすと同時実行ジョブ数も動くはずです。
- 同時実行ジョブ数と最大ジョブ比率の2つで、本当に十分なのか。
- 背景の粒度を変えたときに動いている他の量。

## この結論が崩れるとき

- 同時実行ジョブ数と最大ジョブ比率を揃えたまま背景の形を変えて、飢餓の有無が変わる。
- 判定に別の統計量を使うと、粗い背景でも飢餓が残る。

## 自分で確かめる

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

完全な再実行：

```bash
cd reproduction/gpu-scheduling-boundary
python run_e10.py
```

## 証拠とデータ

- [公開再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [封印済みPRED-009（決定予測と、それが起動する降格を含む）](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-009.json)
- [E10の採点](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E10_grading.json)
- 内部の元Episodeのハッシュ：`5b305fc7b433ae222efcd035c2760a6f5640d24b4f7497097729b9b65a0c93d7`

## 外部からの検証

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決の批判：0

## 次の実験

[[ja/research/gpu-scheduling-phase-diagram/index|EP-0002]]の相図21セルを、同じ軸の上に置き直します。この研究の代表成果であり、θを動かすと同時実行ジョブ数も動いているはずなので、軸そのものが交絡している可能性があります。

## ここに至るまで

<div class="revision-chain vertical" aria-label="GPUクラスタのスケジューリング研究の更新履歴">
  <a href="/ja/research/gpu-scheduling/"><b>EP-0001</b><span>推定誤差と再実行コストで、最良の方式が入れ替わる。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>平均は良いのに、一部のジョブクラスが終わらない。安定性の判定器も3回壊れた。</span></a>
  <a href="/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>飢餓を決めるのは平均ジョブ幅ではなく、クラスタ全体を要するジョブの有無。</span></a>
  <a href="/ja/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>実測したプールにその条件はなく、害は飢餓ではなく数倍の遅れだった。</span></a>
  <a href="/ja/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>安全境界はプールが大きいほど下がる。実規模の害は2倍過小評価だった。</span></a>
  <a href="/ja/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>実クラスタの位置で測り、4本ぶん載せてきた機構説明を訂正した。</span></a>
  <a class="current" href="/ja/research/gpu-scheduling-headline-broken/"><b>EP-0008 · 現在地</b><span>背景の粒度を変えるだけで、この研究の看板結論が消えた。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>代表成果だった相図の軸そのものが、18倍交絡していた。</span></a>
  <a href="/ja/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>「2つの数で決まる」を撤回した。頻度が第三の変数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった。</span></a>
  <a href="/ja/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>動かない境界を持つ統計量へ置き換え、運用数値を戻した。</span></a>
  <a href="/ja/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>実クラスタについての主張は、19,100本中1本のジョブに乗っていた。</span></a>
</div>
