---
research_id: GPU-SCHED-EP-0021
title: 同じ窓でも、情報が違えば誤り方が違う
date: '2026-09-18'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: Bounded synthetic benchmark; general claims UNKNOWN
evidence_level: Synthetic known-model control
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: Sealed aggregate seed-level outcomes and same-model executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known synthetic FCFS models only; information tiers differ; no general
  detector, real-cluster effect or established manuscript novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0021
source_episode_sha256: f69184188fbb7a793ffc81d9c1fb25a7c4e652c2585f9304923f72c22e0f5c4d
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-information-tiers/" hreflang="en">English</a></p>

## 現在わかっていること

同じ到着窓を渡した3診断を既知M/M/4対照で採点しました。600 workload、100独立seed × 6負荷、3入れ子窓、5,400判定。封印予測7/8。

## 図で見る

![EP-0021の誤側/棄権と将来情報費用。cell100seed、20k/80k/320kの入れ子窓。](/assets/gpu-scheduling-information-tiers.png)

EP-0021の誤側/棄権と将来情報費用。cell100seed、20k/80k/320kの入れ子窓。

## この研究が示すこと

独立known-model labelの下で、有限窓・情報契約・誤側と棄権を分けて測れること。

## この研究が示さないこと

一般GPU系の判定保証、新しい容量定理、実クラスタ性能、単一の普遍順位、査読済み論文を示しません。

## 何を調べたか

共通窓でも情報の違いと棄権価格が判定の解釈をどう変えるか。

## なぜ重要か

有限窓の確定値を長期安定性の証明として扱う前に、情報と誤り・保留の費用を区別する必要があります。

## 方法

Wは指数iid入力の母負荷ρを推定するF区間です。実現work比は推定統計量です。per-decision名目誤り.05で誤側区間1件を観測しました。過去の0件は無誤り保証ではありません。ABはWSC2003 Algorithm ABを標本分散として復元した解釈であり、原著の印刷式を忠実に走らせた保証はありません。Dの閾値には誤り.05の保証はありません。

[公開再実行コードと手順](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-tier-benchmark)。入力をseedから生成します。同じ設計の再実行で、外部独立replicationではありません。

## 結果

負荷1.01・20k到着窓でO（出力のみ）は40正/60誤、W（全true workと既知容量）は17正/1誤/82棄権、D（未来drain後JCT）は61正/39誤でした。安定負荷.99ではD閾値.5が31/100件を過負荷と誤確定しました。棄権を正解に数えず、同じ窓と同じ利用情報を区別します。

## 何が変わったか

情報tierと条件付き損失を草稿へ統合。後日の推定対象・価格範囲・coin解釈訂正を反映しています。

## 何が失敗したか

予測1/8が外れ、F区間で誤側1件。AB印刷式の解釈を開示。

## 証拠の範囲

合成known-model、ローカル封印、同じ設計・generatorの再実行。native照合の記録と公開oracle再実行を区別します。

## まだ分からないこと

一般U-31/c12容量、実クラスタ、運用効果、外部独立再現、新規性と受理可能性。validated general detector=0。

## この結論が崩れるとき

定理への機構写像、hash、母分布仮定、個体departure整合、算術集計が成立しなければこの対照の主張を撤回/UNKNOWNにします。

## 自分で確かめる

[再実行手順とコード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-tier-benchmark)。seedから入力を生成し、記録との一致を検査します。

## 証拠とデータ

[公開artifact](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-tier-benchmark)。元Episodeのhashをfrontmatterに記録。私的source全文・個人パスは公開しません。

## 外部からの検証

外部独立replication=0、scientific/domain-expert/peer reviewは未実施。編集点検と算術検査は独立科学監査ではありません。

## 次の実験

報告の新規性・用途を先行研究に対して絞り、別環境/第三者実行を検討。広いモデルは別契約にし、原RQ-1の順位や容量値を復帰させません。

[[ja/research/gpu-scheduling-information-tiers/index|EP-0021]] · [[ja/research/gpu-scheduling-critical-loss/index|EP-0022]] · [[ja/research/gpu-scheduling-two-class-control/index|EP-0023]]
