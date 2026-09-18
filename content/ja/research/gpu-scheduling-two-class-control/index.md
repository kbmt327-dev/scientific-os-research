---
research_id: GPU-SCHED-EP-0023
title: 二クラスFCFSでは、名目負荷1未満でも過負荷を見逃す
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
source_episode: GPU-SCHEDULING/EP-0023
source_episode_sha256: e22560bf6d10d8488984a3fb6bde48acf42e76df2975558f4745c4fb5cd3c218
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-two-class-control/" hreflang="en">English</a></p>

## 現在わかっていること

**要求資源数が混在する小さなFCFS対照で、診断と独立に容量を計算しました。** 64同質資源、need32/64各1/2、クラス別指数service rate1/.5、Poisson到着、strict非preemptive FCFSです。32資源を1blockとし、5状態CTMCを有理数で解くと、到着容量X=8/11 job/time、平均block work=5/2、名目負荷境界=10/11でした。

known labelは[Grosofらの二クラス安定性定理](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf)4.2/4.3の仮定に写像して得ます。λ<Xとλ>Xのみ採点し、等号は除外しました。定常balance・埋込chainの時間重み・work flowを照合しています。新しい定理や一般mixed-need容量ではありません。

100独立seed8001-8100 × 5実効負荷 × 2窓 × 4手法の**4,000判定（500 workload）**、事前予測5/5。実効負荷z=λ/Xに対し、名目負荷は(10/11)zです。z1.01/1.05は名目負荷1未満の過負荷です。

## 図で見る

![二クラス対照の誤側率（20k）とKの棄権率（20k/80k）。各cell100seed、80率へ誤り.05を配分した同時CP区間。既知母パラメータ・未来観測の違いを含むため情報能力の順位は示しません。](/assets/gpu-scheduling-two-class-control.png)

二クラス対照の誤側率（20k）とKの棄権率（20k/80k）。各cell100seed、80率へ誤り.05を配分した同時CP区間。既知母パラメータ・未来観測の違いを含むため情報能力の順位は示しません。

## この研究が示すこと

独立known-model labelの下で、有限窓・情報契約・誤側と棄権を分けて測れること。

## この研究が示さないこと

一般GPU系の判定保証、新しい容量定理、実クラスタ性能、単一の普遍順位、査読済み論文を示しません。

## 何を調べたか

二クラスmixed-needに診断から独立な容量を置けるか、名目work判定と有限窓診断がどう誤るか。

## なぜ重要か

有限窓の確定値を長期安定性の証明として扱う前に、情報と誤り・保留の費用を区別する必要があります。

## 方法

O_ABはcutoffまでの到着/退去、D_ALPHAは未来drain後のH/2対H JCT弾性（20%warmup、閾値.5）、K_EXACTは既知の母クラス確率・母service rate・厳密Xに加え到着記録を使います。Kは到着率のχ²95%区間をXと比較します。混合workへF-CIを移していません。NOMINAL_WORKはHOLを無視する二分対照です。既知母パラメータを持つKの優越性を出力のみの診断へ主張しません。

損失L(a)=e+a uは価格.1/.5/.9で測定。z.99/20kのO/K交差は.125、保守的同時範囲[-.066,.413]、z1.01/20kは1.014、範囲[.562,1.576]です。点交差だけで順位は確定しません。未知truthへの期待損失推薦には適用可能な校正分布が必要で、なければUNKNOWN。

## 結果

| z | H | O wrong/UNKNOWN | D wrong/UNKNOWN | K wrong/UNKNOWN | Nominal wrong/UNKNOWN |
|---:|---:|---:|---:|---:|---:|
| 0.8 | 20k | 1/0 | 0/0 | 0/0 | 0/0 |
| 0.8 | 80k | 2/0 | 0/0 | 0/0 | 0/0 |
| 0.99 | 20k | 9/0 | 34/0 | 0/72 | 0/0 |
| 0.99 | 80k | 11/0 | 37/0 | 0/17 | 0/0 |
| 1.01 | 20k | 73/0 | 44/0 | 0/72 | 100/0 |
| 1.01 | 80k | 54/0 | 24/0 | 0/21 | 100/0 |
| 1.05 | 20k | 9/0 | 1/0 | 0/0 | 100/0 |
| 1.05 | 80k | 0/0 | 0/0 | 0/0 | 100/0 |
| 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 |
| 1.2 | 80k | 0/0 | 0/0 | 0/0 | 0/0 |

各cell100seed。棄権を正解に数えません。名目work対照はz1.01/1.05全4cellで100/100見逃し。Kは全cell0誤側ですが、20kの近傍2cellで72/100棄権。0/100のwrong率にも、80率の同時CP区間では上限.07754があります。

## 何が変わったか

[公開コード・1000 seed-look記録・手順](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-two-class-control)。seedから入力とFCFSを再生成し、厳密容量・診断・区間・損失を実行できます。記録されたnative照合4fixtureはdeparture差0ですが、公開版はprivate native engineを含みません。同じ設計/コードの再実行であり外部独立replicationではありません。

v10は観測前にtuple/list表現照合で停止し、v11は表現のみ修正して再封印。モデル・seed・予測は変更なし。封印はローカルhash/時計で外部timestamp認証ではありません。

技術報告草稿v0.3へ統合し、旧版の推定対象・棄権価格・coin比較の解釈を訂正しました。**一般U-31/c12、実クラスタ、査読論文の新規性・受理可能性はUNKNOWN、validated general detector=0**。次は主張の新規性と用途を絞り、別環境/第三者による実行を検討します。

## 何が失敗したか

v10は観測前の表現照合で失敗。v11で表現のみ修正し再封印。

## 証拠の範囲

合成known-model、ローカル封印、同じ設計・generatorの再実行。native照合の記録と公開oracle再実行を区別します。

## まだ分からないこと

一般U-31/c12容量、実クラスタ、運用効果、外部独立再現、新規性と受理可能性。validated general detector=0。

## この結論が崩れるとき

定理への機構写像、hash、母分布仮定、個体departure整合、算術集計が成立しなければこの対照の主張を撤回/UNKNOWNにします。

## 自分で確かめる

[再実行手順とコード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-two-class-control)。seedから入力を生成し、記録との一致を検査します。

## 証拠とデータ

[公開artifact](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-two-class-control)。元Episodeのhashをfrontmatterに記録。私的source全文・個人パスは公開しません。

## 外部からの検証

外部独立replication=0、scientific/domain-expert/peer reviewは未実施。編集点検と算術検査は独立科学監査ではありません。

## 次の実験

報告の新規性・用途を先行研究に対して絞り、別環境/第三者実行を検討。広いモデルは別契約にし、原RQ-1の順位や容量値を復帰させません。

[[ja/research/gpu-scheduling-information-tiers/index|EP-0021]] · [[ja/research/gpu-scheduling-critical-loss/index|EP-0022]] · [[ja/research/gpu-scheduling-two-class-control/index|EP-0023]]
