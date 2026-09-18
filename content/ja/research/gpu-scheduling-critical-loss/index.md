---
research_id: GPU-SCHED-EP-0022
title: 棄権の価格と、臨界負荷での定義
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
source_episode: GPU-SCHEDULING/EP-0022
source_episode_sha256: f54e91a65b31f402c98be348e731ed115c1854b99da369a65092b66d60d3f5e4
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-critical-loss/" hreflang="en">English</a></p>

## 現在わかっていること

未使用seed6001-6100、5負荷 × 100 seed、3窓、7手法の10,500判定で、損失 `L(a)=誤側率+a×棄権率` を事前固定して測りました。封印予測5/8。定数baselineとのper-cell優越を要求した予測は設計上不適切で外れ、他2件も外れたまま記録しています。

## 図で見る

![EP-0022の条件付き損失曲線と臨界負荷宣言。価格交差は点推定で、同等性検定やオンライン推薦ではありません。](/assets/gpu-scheduling-critical-loss.png)

EP-0022の条件付き損失曲線と臨界負荷宣言。価格交差は点推定で、同等性検定やオンライン推薦ではありません。

## この研究が示すこと

独立known-model labelの下で、有限窓・情報契約・誤側と棄権を分けて測れること。

## この研究が示さないこと

一般GPU系の判定保証、新しい容量定理、実クラスタ性能、単一の普遍順位、査読済み論文を示しません。

## 何を調べたか

共通窓でも情報の違いと棄権価格が判定の解釈をどう変えるか。

## なぜ重要か

有限窓の確定値を長期安定性の証明として扱う前に、情報と誤り・保留の費用を区別する必要があります。

## 方法

[公開再実行コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-tier-benchmark)は臨界宣言集計も含みます。損失順位は価格・対象分布・情報費用を併記して解釈します。

## 結果

O/Wの交差価格は負荷.99・20kで.152、1.01・20kで.739。320kでは1.250/4.000でした。これは特定cellの点推定です。a*>1は0≤a≤1の価格範囲での点推定損失を意味し、任意価格・十分なデータ一般の優越性は示しません。未知truthの新runにこの交差価格をそのままオンライン推薦として使えません。

臨界M/M/4ではpositive recurrenceと在系数の正の線形成長を区別します。負荷1はnull recurrentで、有限平均在系数の条件を満たさず、漸近線形成長率は0です。20k/80k/320kでOは80/78/81件をsubcritical、Wは96/93/91件をUNKNOWNと宣言。Dの宣言割合はcoinに近かったですが、同等性検定は未実施です。16倍窓で改善しなかった観測から無限窓の不可能性は主張しません。

## 何が変わったか

情報tierと条件付き損失を草稿へ統合。後日の推定対象・価格範囲・coin解釈訂正を反映しています。

## 何が失敗したか

事前予測3/8が外れ、定数baselineとのper-cell比較設計も不適切でした。

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
