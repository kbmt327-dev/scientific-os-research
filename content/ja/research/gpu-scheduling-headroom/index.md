---
research_id: GPU-SCHED-EP-0030
title: "gang mixで断片化順位が逆転し、負荷対照が大半を説明する"
date: '2026-10-02'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 決定予測P2失敗。負荷対照P5は近似条件下で通過
evidence_level: Sealed synthetic experiment, single model; bounded saved-result projection
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: E19 saved grading projection and sealed prediction PRED-018
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic model with 64 GPUs in 8-GPU nodes; approximate load-matched comparison only; no real-cluster generalization
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0030
source_episode_sha256: 7e6375fa8addfdac5fbd3737b938bf0e4f4e6a61ed49732163813d36ab29a398
publication:
  status: publishable
tags:
- gpu-scheduling
- fragmentation
- sealed-prediction
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-headroom/" hreflang="en">English</a></p>

## 現在わかっていること

E19の封印予測は6件中3件成立し、決定予測P2は失敗しました。first_fitで採点できた範囲では、trace_likeの3/3行が事前の順位を保つ一方、gang_oddの4/4行でsrptとsf_srptが逆転しました。EP-0029の事後順位を、複数mixに通用する「size優先ほど断片化に強い」という結論として扱うことは撤回します。

## 図で見る

| 予測 | 結果 | 範囲 |
|---|---|---|
| P2: π=0.1/0.2の順位 | FAIL | trace_like 3/3で維持、gang_odd 4/4でsrptとsf_srptが逆転。8行中1行は採点不能 |
| P3: π=0.05の順位 | FAIL | trace_like 2/2で維持、gang_odd 2/2でsrptとsf_srptが逆転 |
| P4: π=0の負荷上昇 | FAIL | 4行中3行で維持。gang_oddのρ=0.7→0.8でsrpt 1.216、sf_srpt 1.195 |
| P5: 負荷をそろえた対照 | PASS | 計算可能な4/8行すべてで、残差が元のfcfs−srpt差の半分以下 |

## この研究が示すこと

この合成モデルと設定では、gang_oddにおいてsrptとsf_srptの劣化順位が逆転しました。断片化の摩擦自体はP1で8/8行に確認され、first_fitのexcessは0.22〜0.36、compactは0.05〜0.09でした。152 cellのうち144はSTABLE、8はUNKNOWNです。

P5の負荷対照は近似条件下で4/4行が事前基準を満たしました。保存されたgrading行から説明率を再計算すると63.8〜100.0%です。これは行別数値の集計であり、独立したシミュレーション再実行ではありません。

## この研究が示さないこと

実クラスタでの順位、他のschedulerやworkloadへの一般化、断片化の因果効果は示しません。断片化は複数nodeにまたがるgangの仕事量を増やす一方、負荷対照は全到着の仕事量を一様に増やします。したがってP5は近似的な対照であり、因果的な分解とは解釈できません。trace_likeのρ=0.6、π=0.2には負荷対照後も約0.50の差が残ります。

## 何を調べたか

EP-0029の封印外観察だった順位が、新しいseedとnodeサイズの倍数でないgang mixでも成立するかを検定しました。加えて、π=0のまま到着負荷だけを上げる腕を設け、観察された劣化差が各policyの負荷余裕でも説明されるかを調べました。

## なぜ重要か

単一のtrace_like mixで見えた事後順位は、別のmixに移すとsrptとsf_srptの間で保たれませんでした。順位の主張を残すには、mixをまたいだ封印検定が必要です。負荷対照は差の多くが負荷余裕と整合することを示しますが、機構を確定しません。

## 方法

封印済み予測PRED-018のE19は、主実験768 runと負荷腕144 run、合計912 runを含みます。モデルは64 GPU、8 GPU/node、指数サービス、σ=0、sticky配置、migrationなしです。この公開パッケージは保存済みgradingから小さな行別投影を作り、順位判定とP5の算術を再計算します。シミュレーション全件は再実行しません。

## 結果

P0とP1はPASS、P2・P3・P4はFAIL、P5はPASSで、6件中3件成立しました。P2は採点可能7/8行で、trace_like 3/3が成立し、gang_odd 4/4がsrptとsf_srptの順で違反しました。P3は2/4行、P4は3/4行で予測順位を保ちました。8件のUNKNOWNは全て高負荷側のfcfsまたはeasy_backfillに集まりました。

## 何が変わったか

EP-0029で記録したtrace_likeの事後順位は、E18の観察として残します。ただし、一般化された四policy順位や「size優先ほど断片化に強い」という含意は撤回します。EP-0030の結果と訂正は[こちら](/ja/research/gpu-scheduling-headroom/)です。

## 何が失敗したか

決定予測P2は事前の四policy順序を支持しませんでした。P2・P3・P4の不一致は主にgang_oddでのsrpt対sf_srptに集中しました。厳密な順位条件を事前登録しているため、差がper-seed変動内にある行も採点を変更していません。

## 証拠の範囲

結果は1つの合成モデルと固定設定に限られます。封印はローカル記録で、外部の独立追試は0件です。公開再現パッケージは保存済みgradingの集計投影を検算し、raw E19 runを含まず、完全な再現や独立追試ではありません。

## まだ分からないこと

別モデル、別のpenalty形状、現実のschedulerやクラスタで順位がどうなるかはUNKNOWNです。UNKNOWNの8 cellは証拠のない失敗ではなく、事前の報告閾値に達しなかったセルです。

## この結論が崩れるとき

新しい封印実験でgang_oddのsrptが一貫してsf_srptより小さい劣化を示せば、今回の逆転は再現しません。別の負荷腕や実クラスタ計測でP5の説明率が大きく外れれば、負荷余裕が大半を説明するという限定的な読みも崩れます。

## 自分で確かめる

[検算パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-headroom)で python verify_e19_projection.py を実行します。保存gradingから投影した行別数値でP0〜P5の閾値と件数を再計算します。912 runの再実行や外部追試は行いません。

## 証拠とデータ

[検算器と集計投影](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-headroom)。含まれるsource artifact hashは版の識別子です。元のrun recordと予測JSONはこのpackageに含めていません。

## 外部からの検証

外部の独立replicationは0件です。PRED-018の封印はローカル記録です。新しい環境で同じモデルを実装した追試はまだありません。

## 次の実験

新しいseedと事前登録したgang mixでsrpt対sf_srptの順位を直接検定し、load-matched対照の近似境界も維持します。実クラスタへの一般化は、その計測が行われるまで主張しません。
