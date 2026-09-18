---
research_id: GPU-SCHED-EP-0024
title: 母パラメータを知らずに、過去の完了から容量を学習する
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
  source: Sealed past-only parameter-learning outcomes and same-model executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known two-block exponential FCFS structure only; no population parameters
  in learned inference; no general detector, real GPU effect or established novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0024
source_episode_sha256: 0bfc36ace20590a5498f92698f439e4685053b53b9dded31c2762220f6f4b7cc
publication:
  status: publishable
tags:
- gpu-scheduling
- past-only
- confidence-sequences
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-past-only-learning/" hreflang="en">English</a></p>

## 現在わかっていること

母パラメータを診断へ渡さず、過去の到着・need・完了から容量区間を学習しました。2つの既知指数FCFSモデル、400 workload・6,000判定、事前予測4/4。区間法は誤側0件でしたが、境界±1%では320k到着でも全50seedが棄権しました。ゼロ件は無誤りの証明ではありません。

## 図で見る

![既知容量と過去情報からの容量学習](/assets/gpu-scheduling-past-only-learning.png)

各cell50seed。赤=誤側、青=UNKNOWN、灰=正側。数字は誤側/棄権です。モデル行と窓列を分け、情報と誤差配分が異なる5手法を表示しています。

## この研究が示すこと

この構造に限り、未来の完了時刻やtrue serviceを使わずサービス露出を復元し、母λ/p/μの不確かさを容量区間へ渡せました。20%離れた負荷は20k時点で全seedを正しい側へ確定しました。

## この研究が示さないこと

一般U-31/c12、非指数、異質資源、実GPU、独立外部replication、新規定理、論文新規性・査読・運用効果はUNKNOWN。構造は既知のままで、実験設計者のblind化でもありません。

## 何を調べたか

EP-0023の母パラメータ既知という有利さを外すと、正側/誤側/棄権はどう変わるか。誤差予算を4分割するだけの影響と、パラメータ学習による影響を分離しました。

## なぜ重要か

真のサービス率が未知の観測で、known-capacity区間法の較正結果をそのまま適用できません。また、確定を急ぐ点推定と、誤側を避ける棄権には異なる費用があります。

## 方法

64同質資源、need32/64、strict非preemptive FCFS、iid marked Poisson、独立クラス指数service。baseline p=.5,μsmall=1,μbig=.5,X=8/11。transfer p=.25,μsmall=.5,μbig=2,X=16/13。未使用seed9101–9150、z=.8/.99/1.01/1.2、入れ子窓20k/80k/320kをv12で事前固定。known labelは[二クラス容量定理](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf)、[confidence sequences](https://arxiv.org/abs/1810.08240)、[counting-process anytime testing](https://proceedings.mlr.press/v258/lindon25a.html)の既存理論を再利用します。

診断入力はcutoffまでの到着/need/完了id・時刻だけ。FCFS開始時刻を復元し、running job数の積分Vjと完了数Mjを使います。稼働中は右打切り、待機中は露出0。Gamma(1,rate1) likelihood-mixture CSを到着率と両service rate、Beta(1,1) CSをclass確率へ適用。各δ=.0125、Ville/union boundによりモデル条件付きjoint anytime名目.05。新しい推論定理ではありません。

容量は1/X=(1-p)/μbig+p(2-p)/(2μsmall)。下容量ではpの内部極値も評価。固定numeric log slack1e-6と外向きroot拡張を使い、厳密な機械検証はしていません。

PAST_ABは標本分散によるWSC2003復元（名目αは保証なし）。KNOWN_CSは真X＋到着CS .05、ALLOCATED_CSは真X＋到着CS .0125、LEARNED_CSは4parameter区間、PLUGIN_MLEは同じ過去情報の点推定です。

## 結果

| Model | z | H | AB wrong/UNKNOWN | Known | Allocated | Learned | Plug-in |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.8 | 20k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 80k | 3/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 320k | 1/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.99 | 20k | 3/0 | 0/50 | 0/50 | 0/50 | 13/0 |
| baseline | 0.99 | 80k | 2/0 | 0/48 | 0/49 | 0/50 | 2/0 |
| baseline | 0.99 | 320k | 4/0 | 0/5 | 0/8 | 0/50 | 0/0 |
| baseline | 1.01 | 20k | 32/0 | 0/50 | 0/50 | 0/50 | 9/0 |
| baseline | 1.01 | 80k | 18/0 | 0/43 | 0/47 | 0/50 | 4/0 |
| baseline | 1.01 | 320k | 4/0 | 0/3 | 0/6 | 0/50 | 0/0 |
| baseline | 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 80k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 20k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 80k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 320k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.99 | 20k | 7/0 | 0/50 | 0/50 | 0/50 | 11/0 |
| transfer | 0.99 | 80k | 3/0 | 0/48 | 0/49 | 0/50 | 0/0 |
| transfer | 0.99 | 320k | 1/0 | 0/5 | 0/8 | 0/50 | 0/0 |
| transfer | 1.01 | 20k | 31/0 | 0/50 | 0/50 | 0/50 | 11/0 |
| transfer | 1.01 | 80k | 23/0 | 0/43 | 0/47 | 0/50 | 1/0 |
| transfer | 1.01 | 320k | 9/0 | 0/3 | 0/6 | 0/50 | 0/0 |
| transfer | 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 80k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |

各cell50seed。seed率CPは族.05を240誤側/棄権率へ配分。3窓のanylookはseedを一度だけ数え80率へ配分、LEARNED_CSはいずれかの窓が誤側となるseedも全8cellで0/50。同時上限は約.149であり無誤り保証ではありません。母parameter coverage監査も全1200 seed-lookで非coverage0件でしたが全時刻coverageを経験的に証明しません。

## 何が変わったか

母パラメータoracleを外し、past-only学習を草稿v0.4へ統合。320k近傍のknown容量棄権は5/3件、誤差配分対照8/6件、学習法50/50件でした（両モデル共通）。学習の隔たりを誤差予算配分だけでは説明できません。

## 何が失敗したか

区間法は±1%負荷を320kでも確定できませんでした。plug-inは20k近傍で9–13/50件誤側、320kでは0誤側/0棄権。この320k cellでは正の棄権価格で学習区間法の点損失が高く、普遍的優越性はありません。保守的rectangle法の限界であり最良手法の標本数下限ではありません。

## 証拠の範囲

20 exact CTMC parameterケース、内部極値fixture、過去露出hand fixture、未来入力拒否を検査。native4fixtureで個体departure/startとクラス露出を照合。全6000判定の件数・CP・損失・anylook・予測採点を再計算。公開版は同じ設計のoracleを再生成しprivate native engineを含みません。

## まだ分からないこと

構造の誤指定下でのcoverage、より鋭い区間法、真の負荷が未知のrunでの期待損失順位、第三者の独立実行と用途、新規性はUNKNOWN。一般validated detector=0。

## この結論が崩れるとき

FCFSでない、need/完了ログ欠落、クラス内非指数、serviceに依存するsize lookahead、異質資源や配置損失があれば露出復元・likelihood・容量定理の適用条件を再監査する必要があります。条件未確認なら長期安定性はUNKNOWN。

## 自分で確かめる

[コードと手順](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-past-only-learning)：`python rerun_past_learning.py --verify-recorded`は記録算術と16小runを再生成。`--seeds 50 --horizons 20000 80000 320000 --output full.json`で全gridを再実行。OS間実行は移植性であり独立replicationとは区別します。

## 証拠とデータ

[summary.json・推論実装・FCFS生成器](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-past-only-learning)。1200 seed-look、24 cell、8 anylook、四予測とnative fixture記録。JSONはreviewed projectionで元封印protocolの同一bytesではありません。hash/時計はローカル由来、外部timestamp認証はありません。損失e+a u、a=.1/.5/.9はtruth条件付き記述でオンライン推薦ではありません。

## 外部からの検証

独立外部replication=0、scientific/domain/peer reviewは未実施。一次資料は既存方法の根拠であり、本artifactの科学的査読ではありません。

## 次の実験

既知構造と観測記録の適合性を明示するgateを監査し、構造が未確認のrunに指数FCFS区間を黙って適用しない。非指数/c12へ精度主張を移す前に、独立known labelと別封印が必要です。

[[ja/research/gpu-scheduling-two-class-control/index|EP-0023]] → EP-0024
