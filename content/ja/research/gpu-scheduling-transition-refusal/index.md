---
research_id: GPU-SCHED-EP-0026
title: 永久parameter遷移を、定常診断はいつ拒否すべきか
date: '2026-09-19'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: Bounded synthetic transition audit; general claims UNKNOWN
evidence_level: Synthetic known-model control
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: Sealed transition manifest and same-design executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One permanent parameter change with truthful provenance; eventual-tail
  label; no undeclared-drift detector or real-GPU claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0026
source_episode_sha256: 2485e3ee2146b9c93df5594c0d1dd5cd8ce0e2bb3dd0570777f20cfea02dcc1f
publication:
  status: publishable
tags:
- gpu-scheduling
- model-drift
- applicability-gate
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-transition-refusal/" hreflang="en">English</a></p>

## 現在わかっていること

永久的なparameter切替を正しく申告すると、既存の定常診断は240/240遷移lookを推論前にUNKNOWNとして拒否しました。同じデータを定常と偽ると、切替直後の100k lookでは80/80件が誤側でした。

## 図で見る

![虚偽定常宣言の誤側とUNKNOWN](/assets/gpu-scheduling-transition-refusal.svg)

2モデル×10seed。実線は誤側、破線はUNKNOWN。各系列の最大は20です。

## この研究が示すこと

正しいprovenance manifestがある合成一回遷移では、stationary診断の適用拒否が誤った長期側の宣言を遮断しました。

## この研究が示さないこと

未申告driftのデータ検知、時変安定性の新定理、一般U31、非指数・実GPU、新規性・査読・独立外部replicationは示しません。

## 何を調べたか

8万到着後にarrival rateまたは両class service rateが一度切り替わり、その後永久に固定する過程を、100k/160k/320kで報告しました。

## なぜ重要か

全履歴の累積統計は切替前のregimeを含みます。定常性が壊れたのに同じconfidence statementを使うと、区間が狭くても対象の長期側を誤ります。

## 方法

64同質資源、need32/64、strict nonpreemptive FCFS、二つの母モデル、seed9301–9310。有限回切替後に永久継続する定常尾部を既存二クラス容量定理で採点し、等号を除外。truthful gateはtransition manifestを受け取り、misuse armだけが虚偽のstationary attestationを受け取ります。

## 結果

| Scenario | Tail truth | H | False scheduled wrong/UNKNOWN/correct | False anytime wrong/UNKNOWN/correct |
|---|---|---:|---:|---:|
| arrival_up | overloaded | 100k | 20/0/0 | 20/0/0 |
| arrival_up | overloaded | 160k | 20/0/0 | 16/4/0 |
| arrival_up | overloaded | 320k | 0/0/20 | 0/0/20 |
| arrival_down | subcritical | 100k | 20/0/0 | 20/0/0 |
| arrival_down | subcritical | 160k | 0/0/20 | 0/2/18 |
| arrival_down | subcritical | 320k | 0/0/20 | 0/0/20 |
| service_degrade | overloaded | 100k | 20/0/0 | 20/0/0 |
| service_degrade | overloaded | 160k | 20/0/0 | 0/0/20 |
| service_degrade | overloaded | 320k | 0/0/20 | 0/0/20 |
| service_improve | subcritical | 100k | 20/0/0 | 20/0/0 |
| service_improve | subcritical | 160k | 20/0/0 | 20/0/0 |
| service_improve | subcritical | 320k | 20/0/0 | 0/20/0 |

定常対照120 lookはtruthful gateで全件正解。遷移240 lookは全件inferenceなし。100kの遷移80件はfalse scheduled/anytimeとも全件誤側。320kではservice improveのみscheduled20/20誤側、anytime20/20 UNKNOWN。

## 何が変わったか

草稿v0.6へ、診断精度より前にモデル適用可能性を確認する層を追加しました。

## 何が失敗したか

宣言gateは嘘や欠落したmanifestをデータから検出しません。service improveではscheduled法の累積履歴汚染が320kでも残りました。

## 証拠の範囲

120 workload、360固定look、1080 method outcomes、封印5/5。seal/source/chronology、post-regime exact label、gate状態、36cell集計を再計算。

## まだ分からないこと

漸進・反復・適応的変化、p変化、構造変化、実ログのprovenance、外部読者の理解と需要はUNKNOWN。general detector0。

## この結論が崩れるとき

manifestが真でないと拒否は働きません。eventual-tail labelは有限窓queue状態ではなく、別の時変定義には移せません。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-transition-refusal)で`python runner_transition.py --verify-recorded --seeds 2`。記録360 lookを再集計し、24 small lookを再生成します。

## 証拠とデータ

[summary、generator、gate、runner](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-transition-refusal)。reviewed projectionで元sealと同一bytesではありません。

## 外部からの検証

独立外部replication0。Linux CIは同じ設計の再実行で、第三者の独立研究ではありません。

## 次の実験

外部読者が作者の補助なしで、truthful/false declarationとeventual-tail labelの違いを説明・再実行できるかを評価できる仕様にします。

[[ja/research/gpu-scheduling-exposure-checkpoints/index|EP-0025]] → EP-0026
