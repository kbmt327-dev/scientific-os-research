---
research_id: GPU-SCHED-EP-0018
title: 既知の過負荷を、中点のqueue閾値が見逃した
date: '2026-09-17'
lang: ja
domain: GPU Cluster Scheduling
type: Negative Result
status: 既知対照の見逃し・一般容量未確定
evidence_level: 合成の既知model対照
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: 36 oracle workloads + 4 engine fixtures; public aggregate arithmetic only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known full-gang M/M/1; homogeneous FCFS; independent exponential inputs; true required work accessible; no mixed-need or real-cluster capacity claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0018
source_episode_sha256: 766e176d6e0254b00e3494ecc8a8dff44deadb39b5a7d8795607f6f65c8846c0
publication:
  status: publishable
tags:
- negative-result
- gpu-scheduling
- known-controls
- uncertainty
- ja
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>既知対照と有限窓の不確かさ</span><a href="/en/research/gpu-scheduling-known-controls/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Negative Result</span><span>Synthetic known model</span><span>Capacity UNKNOWN</span><span>No peer review</span><span>Independent replications 0</span></div>

## 現在わかっていること

**過負荷を確実に知っている対照でも、遠い2点の中点queue閾値は成長を見逃しました。** rho=1.05でalphaは0.976505、queue scoreは0.033571。較正中点0.059412を下回り、queueだけが非成長と判定しました。最初の不一致で停止しました。

この対照では全jobが64台すべてを占有するため、同時に1 jobしか処理できません。homogeneous FCFSと独立指数入力からM/M/1に帰着すると推論でき、[既知の安定条件](https://homepages.ecs.vuw.ac.nz/~schukova/SCIE201/Lectures/Lecture9_10_final.html)でrho>1を過負荷と定められます。mixed-needのbalanced需要にこの境界を移すことはできません。

## 何を調べたか

[[ja/research/gpu-scheduling-u31-calibration/index|EP-0017]]で見つけた判定器の食い違いを、判定器から独立した既知対照で絞り込めるか。極端なstable/overloadの中点が、遷移域でも成長を分類できるか。

## なぜ重要か

二つの信号が違うとき、どちらかを正しいと選ぶだけでは較正になりません。既知labelを使うことで、少なくともこの対照でqueue側が見逃したと特定できます。

## 方法

全gang FCFS、指数gap・指数service・mean service 1、64サーバを固定。calibrationはrho=0.4/1.2、seed 301/302/303。holdoutは0.95/1.05/0.99/1.01の順、別seed 401/402/403。H=20k/40k/80k。後半40k/80kのseed平均JCTの対数比をalphaとし、0.5以上をgrowthとしました。

80k窓で、到着中のevent backlogの最初/最後decile平均差をjob数で割り、controlの中点をqueue閾値にしました。全gangのFCFS recurrenceでjob列を解き、同じjob列に対する既存engineとの4 fixtureで個別completion・JCT・queue scoreが差0になることを先に確認しました。各cell直後にknown labelと照合し、最初のR2/R3で止める事前契約です。封印はローカルhash/時計の記録で、外部timestampや第三者sealではありません。

## 結果

| rho | alpha | event queue score | known label |
|---:|---:|---:|---|
| 0.40 | -0.006956 | -0.000001 | stable |
| 1.20 | 1.008942 | 0.118824 | overloaded |
| 0.95 | -0.229628 | -0.000023 | stable |
| 1.05 | 0.976505 | 0.033571 | overloaded |

rho=0.95では両判定がknown labelと一致。rho=1.05ではqueueだけが過負荷を見逃し、36/最大54 oracle workloadでR2停止。0.99/1.01は未実行です。time-weighted queue scoreも0.033578と近く、event平均の重みだけを見逃しの原因とする根拠はありません。1.05のalphaは前半pairで0.988114、後半pairで0.976505。0.3/0.5/0.7の各lineでgrowthでした。

## 何が変わったか

遠いcontrolが分離することと、境界近傍の判定が較正されることを分けました。queue中点の一般採用を保留し、次を入力driftの不確かさとUNKNOWNの扱いへ変更。[[ja/research/gpu-scheduling-drift-uncertainty/index|EP-0019]]がその新しい試行です。

## 何が失敗したか

中点queue閾値は、成長が小さい既知過負荷を非成長へ押し込みました。結果後に閾値を下げて合格へ変更していません。見逃しの予測が当たったことは、判定器の受入成功を意味しません。

## 証拠の範囲

全gang、既知M/M/1、固定窓とseedの合成対照での見逃しです。alphaの一致もこの4cellまで。balanced/rho=0.85の真のlabel、一般alpha閾値、二分法容量、実クラスタ性能を確定しません。公開物は集計の算術と停止分岐までで、raw job列とsimulator sourceは含みません。

## まだ分からないこと

mixed-needでqueueとalphaのどちらが正しいか。一般の容量を独立に知るcontrolを作れるか。実データで未完了jobのtrue workを観測できるか。容量と一般判定器はUNKNOWNです。

## この結論が崩れるとき

control中点やknown labelへの算術照合が再計算できない場合、見逃しの記述を撤回します。新しい契約の改善でこの固定契約の失敗を消しません。

## 自分で確かめる

```bash
python reproduction/gpu-scheduling-u31-controls/verify_summary.py
```

simulationの再実行ではなく、公開集計とCI/停止分岐の検算です。

## 証拠とデータ

[公開集計と検算コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-controls)。内部Episode SHA-256: `766e176d6e0254b00e3494ecc8a8dff44deadb39b5a7d8795607f6f65c8846c0`。原記録との対応であり、科学的妥当性の証明ではありません。

## 外部からの検証

独立再現0、査読0。編集上の整合・privacy reviewを行いましたが、科学レビュー・domain expert reviewではありません。

## 次の実験

入力driftの不確かさを事前固定して、小さい正の成長を無理に分類しない方法を検査します。その結果は[[ja/research/gpu-scheduling-drift-uncertainty/index|EP-0019]]へ続きます。mixed-need容量と実クラスタは別の受入gateです。
