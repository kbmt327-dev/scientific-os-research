---
research_id: GPU-SCHED-EP-0020
title: 固定needの4並列対照へ、入力CIを移せた
date: '2026-09-17'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 限定移行PASS・新規性未確立
evidence_level: 合成の既知model対照
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: 30 input/oracle workloads, 10 CI looks and 4 native alignment fixtures;
    public aggregate arithmetic only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Synthetic homogeneous 64-server FCFS; every job requires 16 servers;
  four fungible slots; independent iid exponential gaps and true service work; no
  mixed-need capacity, real-cluster performance, diagnostic-superiority or established
  manuscript novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0020
source_episode_sha256: b5ebff918c1d35c67298f7c8ef2c649a7227389dc4f7d89f0c5f0b1f5128209f
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- ja
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>Known controls and manuscript preparation</span><a href="/en/research/gpu-scheduling-mmc-transfer/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic known model</span><span>General capacity UNKNOWN</span><span>Novelty unestablished</span><span>Independent replications 0</span></div>

## 現在わかっていること

**固定needの4並列対照へ入力CIを移し、control 2点・holdout 4点をすべて正しい側へ確定しました。** 負荷1.01の確定には160k到着×3 seedが必要でした。4個の既存エンジン照合の完了時刻最大差は約8.9×10⁻¹⁶でした。

限定的な既知modelの受入結果です。一般GPUジョブ混在系の容量・U-31はUNKNOWN、validated general detectorは0件です。有限窓監査の技術報告草稿を作りましたが、査読論文としての新規性は未確立です。

## 図で見る

![既知対照の入力負荷信頼区間](/assets/gpu-scheduling-mmc-transfer-ci.png)

左は今回のM/M/4各cellの最終CI、右は[[ja/research/gpu-scheduling-drift-uncertainty/index|EP-0019]]のM/M/1・rho=1.005の各窓のCI。点は推定値、破線は負荷1。Hは各seedの到着件数、3 seedをpoolしています。両panelはseed・誤り配分・最大窓が異なり、並列度による優劣の比較には使いません。

## この研究が示すこと

全jobが同じ16資源を必要とし、64資源が同質である条件では、nonpreemptive FCFSを4同質slotへ写像して、独立known labelと実装照合を得られました。入力CIの式に容量4を明示して移行できました。

## この研究が示さないこと

mixed-needのpacking/HOL、異質server、locality、推定work、非指数入力への適用は検証していません。M/M/c負荷条件とF CIは既知で、新しい統計的定理や一般判定器の発見ではありません。

## 何を調べたか

全gang M/M/1で使った入力CIを、同時に4jobが走る固定needの既知対照へ移す機構・観測要件・既存エンジン整合が成立するか。

## なぜ重要か

診断器同士の一致では正解を保証できません。判定器から独立した理論上のlabelと、別の実行経路との照合を用いて、主張できる範囲を確認します。

## 方法

64資源、全need=16、homogeneous、速度1、nonpreemptive FCFS、独立iid指数gap/service。c=4でrho=lambda E[S]/4。固定needにより混在要求数のpacking lossを除きます。[M/M/cの大学講義](https://homepages.ecs.vuw.ac.nz/~schukova/SCIE201/Lectures/Lecture9_10_final.html)の負荷条件を、この機構へ適用した推論です。

control rho=0.8/1.2はseed 901/902/903、holdout 0.95/1.05/0.99/1.01はseed 1001/1002/1003。H=20k/40k/80k/160k、最大24比較にfamily error .05を配分して実行前に封印しました。

真のoffered service Bと全gap時間Tをpoolし、R=B/(4T)、n=3H。指数/独立性の仮定下でR/rhoはF(2n,2n)であり、CI=[R/q_high,R/q_low]です。[F分布の公式説明](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html)。上限<1をsubcritical、下限>1をoverloaded、それ以外をUNKNOWN。途中UNKNOWNは次の固定窓へ、確定後は拡大を止めます。最初のwrong-sideはR2、最大窓UNKNOWN・欠測・engine不整合はR3停止です。

heapによるFCFS slot再帰と既存event engineを、4個のH1000 fixtureでjob別departure/JCT照合しました。generatorは共有しており、独立再現ではありません。

## 結果

| role | rho | 確定H/seed | 負荷CI | 判定 |
|---|---:|---:|---|---|
| calibration | 0.80 | 20,000 | [0.783941, 0.812306] | subcritical |
| calibration | 1.20 | 20,000 | [1.175912, 1.218459] | overloaded |
| holdout | 0.95 | 20,000 | [0.933258, 0.967025] | subcritical |
| holdout | 1.05 | 20,000 | [1.031495, 1.068817] | overloaded |
| holdout | 0.99 | 40,000 | [0.974896, 0.999708] | subcritical |
| holdout | 1.01 | 160,000 | [1.005608, 1.018324] | overloaded |


30 workload・10 lookで6 cellが正しい側へ確定、確定誤ラベルは0件でした。これは本runの観測件数で、経験的coverageの保証ではありません。model条件付き5%family budgetも実クラスタの誤り率ではありません。

## 何が変わったか

既知対照を1slotから4slotへ追加できました。技術報告草稿・主張と証拠の対応表・比較設計を作成し、論文準備へ進みました。原RQのscheduler順位問題とは別の方法論branchです。

次の比較では情報と実時間cutoffを分けます。Oはcutoffまでのarrival/departure/system count、Wは全offered true workと既知容量、Dはdrain後の将来完了を使うcohort JCT。今回のCIはWです。到着件数だけを揃えても、追加work情報や将来の完了を使う診断との公平な比較にはなりません。

## 何が失敗したか

初回はcontrol実行中の結果snapshot保存エラーで停止しました。失敗記録を残し、保存のbounded retryだけを修正、同じgrid・seed・判定式・誤り配分を再封印して復旧しました。controlデータは既に観測済み、holdoutは初回未実行です。完全未観測の独立実験とは呼びません。

## 証拠の範囲

合成固定need M/M/4、指数/独立入力、未完了jobも含むtrue required service、機構capacity4に限定。local hash/時計のsealです。adaptive停止のため早期確定cellの窓は揃わず、alphaとの系統的比較はしていません。

公開artifactは集計された十分統計とCI/停止/engine照合の要約です。generator・simulator・private原稿やWork State・raw job列は含みません。

## まだ分からないこと

既存の安定性検査との同一情報・同一時間比較が、追加の知見を与えるか。true workが未知の場合、mixed-needで独立labelをどう得るか。技術報告から査読論文へ進める新規性は未確立です。

## この結論が崩れるとき

十分統計・CI・確定窓を再計算できない、またはnative照合の根拠が崩れる場合は移行記述を撤回します。固定need/指数性/独立性/容量が成立しない系には誤り上限を適用しません。

## 自分で確かめる

```bash
python reproduction/gpu-scheduling-u31-controls/verify_mmc_summary.py
```

SciPyが必要です。公開集計の算術・記録された停止/照合要約を検査します。省略されたengineの再実行や独立検証ではありません。

## 証拠とデータ

[公開十分統計・検算コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-controls)。内部Episode SHA-256: `b5ebff918c1d35c67298f7c8ef2c649a7227389dc4f7d89f0c5f0b1f5128209f`。

## 外部からの検証

独立再現0、査読0。内部でsource/seal hash、封印順、quantile-CDF、全10 look、停止位置、改変/unsupported need拒否を確認しました。編集・privacy reviewは科学レビューではありません。

## 次の実験

既存の安定性検査の一次algorithm仕様とO/W/D情報tier、共通実時間cutoff、独立known label、反復の誤確定/UNKNOWN/cost、公開実行artifactを先に固定して別封印します。仕様/label不足なら未実行・UNKNOWN。比較で新規性差分が得られなければ技術報告として区切り、校正だけを追加し続けません。


次の比較と二クラス対照：[[ja/research/gpu-scheduling-two-class-control/index|EP-0023]]。
