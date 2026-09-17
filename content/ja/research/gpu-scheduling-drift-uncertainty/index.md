---
research_id: GPU-SCHED-EP-0019
title: 小さな過負荷を、有限窓では確定できなかった
date: '2026-09-17'
lang: ja
domain: GPU Cluster Scheduling
type: Negative Result
status: 有限窓UNKNOWN・一般判定器未検証
evidence_level: 合成の既知model対照
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: 51 input/oracle workloads, 17 CI comparisons; public sufficient-statistic CI arithmetic only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known full-gang M/M/1; homogeneous FCFS; independent exponential inputs; true required work accessible; no mixed-need or real-cluster capacity claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0019
source_episode_sha256: 772e57cdb1532f4aa047b32cda13fb04fe9e7d36d3272360ddd1106f34daf320
publication:
  status: publishable
tags:
- negative-result
- gpu-scheduling
- known-controls
- uncertainty
- ja
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>既知対照と有限窓の不確かさ</span><a href="/en/research/gpu-scheduling-drift-uncertainty/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Negative Result</span><span>Synthetic known model</span><span>Capacity UNKNOWN</span><span>No peer review</span><span>Independent replications 0</span></div>

## 現在わかっていること

**入力driftの信頼区間は3つのholdoutを正しい側へ確定し、より小さい過負荷はUNKNOWNとして残しました。** rho=1.005は320k job×3 seedでも負荷CIが[0.998880,1.008229]となり、境界1を含みました。最初の最大窓UNKNOWNで停止しました。

これは過負荷を検出できたという結果ではありません。確定できないものを安定側へ押し込まなかった結果です。指数入力、全jobのtrue required work、機構から分かる容量1を使うknown-model検査であり、一般MSJ判定器のvalidationではありません。

## 何を調べたか

[[ja/research/gpu-scheduling-known-controls/index|EP-0018]]の中点queue閾値に代わり、有限窓の不確かさを含めた入力drift判定が、境界近傍のknown labelを区別し、区別できないときUNKNOWNを返せるか。

## なぜ重要か

有限窓で成長が小さい場合、成長がない場合との区別にはデータが足りません。UNKNOWNを非成長と数えると、判定器の不確かさが安定性の主張に化けます。

## 方法

全gangの既知M/M/1を保持しました。calibrationはrho=0.97/1.03・seed 601/602/603、holdoutは0.99/1.01/0.995/1.005/0.999/1.001の順・別seed 701/702/703。各cellのH=20k/40k/80k/160k/320kを事前固定。calibrationは受入用で、閾値を結果からfitしません。

全jobのservice work Bとarrival gap時間Tを3 seedでpoolし、R=B/Tを負荷estimateにしました。n=3H。独立iid指数入力の下、R/rhoはF(2n,2n)に従うため、CI=[R/q_high,R/q_low]としました。[F分布の定義と実装](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html)を本モデルの十分統計へ適用した推論で、新しい定理ではありません。

最大8cell×5窓の40比較にdelta=0.05/40を割り当てます。union boundによる「誤った側を1つでも確定する確率5%以下」は仮定したmodelに条件付けられた理論上限。実クラスタの誤り率、UNKNOWNの頻度、本runの誤り0件からの経験的保証ではありません。

CI上限<1をsubcritical、下限>1をoverloaded、それ以外をUNKNOWN。中間窓UNKNOWNは次の固定窓へ、確定後はそのcellを終了。最初のwrong labelはR2、最大窓UNKNOWN・欠測はR3で全体を停止。封印はローカルhash/時計に限ります。

## 結果

| rho | H | load CI | label |
|---:|---:|---|---|
| 0.970 | 20,000 | [0.956913, 0.993245] | subcritical |
| 1.030 | 20,000 | [1.016103, 1.054683] | overloaded |
| 0.990 | 40,000 | [0.972746, 0.998718] | subcritical |
| 1.010 | 160,000 | [1.001040, 1.014316] | overloaded |
| 0.995 | 160,000 | [0.986173, 0.999252] | subcritical |
| 1.005 | 320,000 | [0.998880, 1.008229] | UNKNOWN |

control2点は20kで確定。holdout0.99は40k、1.01/0.995は160kで確定。1.005は5窓すべてUNKNOWNで、51 workload・17比較にR3停止。0.999/1.001は未実行・未採点です。1.005のnet-input drift CIは[-0.001120,0.008229]。実行範囲の確定誤ラベルは0件でした。

## 何が変わったか

正の成長量を任意の中点と比べる代わりに、既知modelの入力CIで確定可能な側だけ返しました。不確かさを明示する表現は改善しましたが、既知過負荷1.005を最大窓内に確定する受入条件は満たしていません。

## 何が失敗したか

小さい過負荷を、上限32万job×3 seedでも確定できませんでした。追加seedや緩い誤りbudgetを結果後に足していません。subcritical labelはknown full-gang容量の意味で、mixed-needの安定性labelではありません。

## 証拠の範囲

合成full-gang M/M/1、独立指数入力、true service workの可観測性、既知容量1に条件付けられます。未完了jobを含む全入力workを使います。反射されたremaining-workload driftと入力drift R-1は別量です。実データで到着時にtrue workを知れるかは未確認。mixed-need、alpha=0.5、二分法容量、実クラスタ、独立再現をvalidateしません。

公開verifierは集計された十分統計からF quantileとCI/停止分岐を再計算します。job生成、simulator再実行、指数性・独立性・繰り返し標本でのcoverage検証は含みません。

## まだ分からないこと

既知容量がないmixed-needで独立labelをどう定めるか。非指数・依存入力でどの不確かさモデルを使うか。実運用で入力workを観測できるか。一般容量・U-31の閾値はUNKNOWNです。

## この結論が崩れるとき

十分統計、F quantile、CIとlabel、停止位置が再計算できない場合は記述を撤回します。指数/独立性やknown capacityを満たさない入力にはCIの誤り上限を主張しません。新契約で確定しても今回のUNKNOWNを後から解決済みに変更しません。

## 自分で確かめる

```bash
python reproduction/gpu-scheduling-u31-controls/verify_summary.py
```

SciPyが必要です。公開十分統計のCI算術を検査する限定的再現で、simulationや独立科学再現ではありません。

## 証拠とデータ

[公開十分統計と検算コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-controls)。内部Episode SHA-256: `772e57cdb1532f4aa047b32cda13fb04fe9e7d36d3272360ddd1106f34daf320`。raw job列、simulator source、private Work Stateは含みません。

## 外部からの検証

独立再現0、査読0。内部で封印順、source hash、quantile-CDF roundtrip、全17CI算術、停止位置、改変protocol拒否を確認。編集・privacy reviewは科学レビューやdomain expert reviewではありません。

## 次の実験

fixed-needがpool容量を割り切る既知M/M/c対照へ移すための機構・入力work観測・指数/独立性・native engine整合を先に固定します。新しいcontrol/holdout、窓上限、誤りbudget、最初のR2/R3停止を封印し、独立known labelを得られないmixed-needには適用しません。既存18cell二分法の全rerunと実クラスタは別gateです。


後続の固定need M/M/4検査と論文準備：[[ja/research/gpu-scheduling-mmc-transfer/index|EP-0020]]。
