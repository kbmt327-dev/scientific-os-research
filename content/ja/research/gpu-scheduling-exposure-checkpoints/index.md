---
research_id: GPU-SCHED-EP-0025
title: 固定完了数の露出checkpointで、判定時点と棄権を比較する
date: '2026-09-19'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: Bounded synthetic benchmark; general claims UNKNOWN
evidence_level: Synthetic known-model control
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: Sealed scheduled checkpoint outcomes and same-design executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known two-block exponential FCFS; fixed reporting looks/checkpoints,
  not anytime; no general detector, real GPU effect or established novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0025
source_episode_sha256: eced65710973c1ca3517a81b333e680a10b9ab40f11b07884749240fed82bf8e
publication:
  status: publishable
tags:
- gpu-scheduling
- time-change
- scheduled-inference
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-exposure-checkpoints/" hreflang="en">English</a></p>

## 現在わかっていること

母パラメータを診断へ渡さない比較に、事前指定lookと固定完了数のサービス露出checkpointを追加しました。160 workload・2400判定、封印4/4、scheduled区間法の誤側0件。128万到着の境界近傍4cellで、随時有効法の棄権79/80に対しscheduled法は22/80でした。

## 図で見る

![随時有効法と事前指定lookの誤側/棄権](/assets/gpu-scheduling-exposure-checkpoints.png)

各cell20seed。赤=誤側、青=UNKNOWN、灰=正側、数字=誤側/棄権。3手法は同じ過去の情報を使いますが、scheduled法の保証範囲は狭くなります。

## この研究が示すこと

既知指数FCFS内で、並行実行中の未完了jobを含む露出を固定K番目完了まで記録し、既存χ²pivotを使えました。固定lookと随時有効な方法を、情報・予算・棄権費用とともに比較するartifactです。

## この研究が示さないこと

新しいtime-change/容量/推論定理、最適標本数、普遍的優越性、実GPU、一般U31/c12・非指数・独立外部replication・論文新規性・査読はUNKNOWN。scheduled法は任意停止時点では使えません。

## 何を調べたか

前回±1%負荷で全棄権だった区間を、自由なreporting時点の代わりに3つの時点へ制限するとどう変わるか。randomな観測完了数を固定数として扱わず、事前固定したmilestoneだけ使います。

## なぜ重要か

確定できない原因には観測量だけでなく保証範囲と区間の保守性が含まれます。報告契約と統計量・使用する観測subsetが同時に変わるので、改善を報告時点制限だけの因果効果とは言えません。

## 方法

64同質資源、need32/64、strict非preemptive FCFS、iid marked Poisson、独立クラス指数service、empty初期状態。baseline p=.5,μ1=1,μ2=.5,X=8/11、transfer p=.25,μ1=.5,μ2=2,X=16/13。[既知二クラス定理](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf)でλ<X/λ>Xを採点し等号を除外。seed9201–9220、z=.8/.99/1.01/1.2、H=20k/320k/1280k、K=256–1048576の2倍刻み13値を開始前に固定。

過去の到着/need/完了だけから開始とVj=∫Rjを復元。[既存時間変換定理](https://warwick.ac.uk/fac/sci/statistics/apts/students/resources-2010-2011/stochproc_notes.pdf)により固定K番目完了tKの2μjVj(tK)~χ²(2K)。露出は未完了jobを含み、完了job durationの合計ではありません。最大eligible Kを選ぶ失敗事象は全固定Kのunconditional union bound内です。availability条件付きcoverageではなく、randomなMをχ²自由度へ入れません。

joint scheduledα=.05を4parameterへ割り、λ/pはさらに3look、両μは各13checkpointへ配分。λはχ²、pはbinomial CP。容量rectangleは内部p極値と外向き変換を含む前回の実装です。[随時有効CS](https://arxiv.org/abs/1810.08240)は前回の4×.0125 mixture区間。真Xを持つKNOWN_SCHEDULED、同じarrivalαのALLOC_SCHEDULED、過去点推定PLUGIN_MLEも対照。

## 結果

| Model | z | H | Anytime wrong/UNKNOWN | Checkpoint | Known | Allocated | Plug-in |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.8 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 1280k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.99 | 20k | 0/20 | 0/20 | 0/20 | 0/20 | 5/0 |
| baseline | 0.99 | 320k | 0/20 | 0/20 | 0/0 | 0/1 | 0/0 |
| baseline | 0.99 | 1280k | 0/19 | 0/4 | 0/0 | 0/0 | 0/0 |
| baseline | 1.01 | 20k | 0/20 | 0/20 | 0/14 | 0/17 | 2/0 |
| baseline | 1.01 | 320k | 0/20 | 0/20 | 0/0 | 0/0 | 0/0 |
| baseline | 1.01 | 1280k | 0/20 | 0/2 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 1280k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 1280k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.99 | 20k | 0/20 | 0/20 | 0/20 | 0/20 | 7/0 |
| transfer | 0.99 | 320k | 0/20 | 0/20 | 0/0 | 0/1 | 0/0 |
| transfer | 0.99 | 1280k | 0/20 | 0/13 | 0/0 | 0/0 | 0/0 |
| transfer | 1.01 | 20k | 0/20 | 0/20 | 0/14 | 0/17 | 2/0 |
| transfer | 1.01 | 320k | 0/20 | 0/20 | 0/0 | 0/0 | 0/0 |
| transfer | 1.01 | 1280k | 0/20 | 0/3 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 1280k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |

各cell20seed。CPは族.05を240cell率/80anylook率へ配分。3窓は入れ子、cross-cell共通seedなので独立ではありません。0/20anylook誤側にも同時上限約.332があり、ゼロ件は無誤りの証明ではありません。損失e+a uはa=.1/.5/.9、truth条件付きです。

## 何が変わったか

母parameterなしの較正に、scheduled報告という別の契約を追加し草稿v0.5へ統合。構造/log宣言が未確認・scope外・欠落ならUNKNOWN、inferenceを実行しない入口を作りました。宣言gateはモデル仮定のデータ証明ではありません。

## 何が失敗したか

20seedの同時区間は広く、有限予算の結果から無誤り・任意時点保証・未知truthへの損失順位は言えません。全cellと封印予測のFAILもsummaryへ保存。前回の全棄権を情報理論的下限とは扱いません。

## 証拠の範囲

native4fixtureで24checkpoint露出を照合、最大差4.55e-13。並行実行hand fixtureは固定first-completion露出19.9と完了job duration10の違いを検査。7宣言gate対照、2指定外look、未来/extra情報拒否を確認。480row/24cell/8anylookの区間・件数・損失・予測を再計算。

## まだ分からないこと

時変parameter/構造、非指数、異質資源、実ログの仮定適合性、より鋭い方法、第三者の独立実行・用途・新規性はUNKNOWN。一般validated detector0。

## この結論が崩れるとき

完了ログ欠落、非FCFS、size lookahead、クラス内非指数、配置損失などはlikelihood/露出/容量条件を変えます。宣言が一致しても実データの真偽は証明されません。指定外lookではscheduled保証を出しません。

## 自分で確かめる

[コードと手順](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-exposure-checkpoints)の`python runner_checkpoint.py --verify-recorded`で記録算術と16小runを再生成。`--seeds 20 --horizons 20000 320000 1280000 --output full.json`で全grid。小runでも省略lookの誤差予算を再配分しません。

## 証拠とデータ

[summary・観測tape・scheduled/anytime実装・生成器・runner](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-exposure-checkpoints)。JSONはreviewed projectionで元sealの同一bytesではありません。hash/時計はローカル、外部timestamp認証なし。public verifierは連続値rel1e-9/abs1e-10、labels/counts厳密照合。

## 外部からの検証

独立外部replication0、scientific/domain/peer review未実施。公開版は同じ設計のFCFS oracleを再生成しprivate native engineを含みません。一次資料は既存方法の根拠であり本artifactの査読ではありません。

## 次の実験

時変parameter/構造の適用拒否と独立known labelを別契約で監査。構造未確認runを指数FCFSとみなさず、一般C042とscheduler順位を復帰させません。

[[ja/research/gpu-scheduling-past-only-learning/index|EP-0024]] → EP-0025
