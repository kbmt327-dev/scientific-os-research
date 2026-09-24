---
research_id: GPU-SCHED-EP-0029
title: nodeの断片化は、サイズ優先とFCFS・backfillの順位を入れ替えるか
date: '2026-09-25'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: Sealed prediction failed (1/6); low power; post-hoc pattern unconfirmed
evidence_level: Sealed synthetic sweep, single model
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: 768-run MSJ simulation sweep graded by a sealed script (PRED-017)
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic MSJ model, 64 GPUs in 8-GPU nodes, loads 0.6 and 0.7,
  multiplicative fragmentation penalty; no real cluster claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0029
source_episode_sha256: 88e85fe7c39894030467205bc28b547382a841a13153f050bc477821522dc8cd
publication:
  status: publishable
tags:
- gpu-scheduling
- locality
- sealed-prediction
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-locality/" hreflang="en">English</a></p>

## 現在わかっていること

gangが複数nodeにまたがると遅くなるmodelで、4つのpolicyの順位が入れ替わるかを調べました。封印した予測は6本中1本しか当たらず、決定予測（順位の逆転が起きる）も外れました。逆転は0件です。ただしこの検定には検出力がほとんどありませんでした。片方のjob mixでは断片化がそもそも起きない設計になっており、強いpenaltyではほぼ全cellが発散しました。

## 図で見る

![trace_likeでの平均JCTの劣化倍率（policy別、対数軸）](/assets/gpu-scheduling-locality.svg)

π=0を基準にした平均JCTの倍率です。結果を見たあとに作った図で、封印した判定ではありません。

## この研究が示すこと

- このmodelとこの負荷（ρ 0.6/0.7）では、断片化がpolicyの順位を入れ替える例は見つかりませんでした。事前に決めたとおり、localityは「順位の摩擦」ではなく「水準の効果」と記録します。
- gang_heavy mix（needが8/16/32/64）では断片化が起きません。needがすべてnode size（8）の倍数なので、first-fitでも空きserverは常にnode単位で残り、どのgangも最小数のnodeに収まります。384 runすべてでexcess nodeは0、π×placementの8通りでJCTがbit単位で一致しました。
- 結果を見たあとの観察として、trace_like mixでは劣化の順がsrpt < sf_srpt < easy_backfill < fcfsで、8行すべてで同じでした。サイズ優先ほど断片化に強く、順位は入れ替わらずに差が広がっています。

## この研究が示さないこと

上の劣化の順は、同じseedの上で結果を見てから気づいたもので、確証ではありません。実クラスタでの挙動、実際の通信コスト、network topology、migrationやlocality-aware admissionの効果は示しません。断片化が害になり、集約配置が効くことは既知です（Tiresias、Phillyの解析、Gandiva）。新しい主張ではありません。

## 何を調べたか

RQ-1は「サイズ優先は、推定誤差・preemptionコスト・server不均質・gang/locality制約のもとで、どこでFCFS+backfillに逆転されるか」です。4つの摩擦のうち、gang/localityだけが一度も測られていませんでした。断片化は順位を入れ替えるか、best-fitのcompact配置はその効果を消すかを調べました。

## なぜ重要か

GPUクラスタのschedulerは、どのjobを先に走らせるかと、どこに置くかを別々に決めることが多いです。置き方の悪さが順番の良し悪しを覆すなら、順番だけを比較した結論は実運用に移りません。

## 方法

64 GPU（8-GPU node×8）のMSJ simulator。gangの進行速度は1/(1 + π × excess)で、excessはceil(need/8)を超えてまたいだnode数です。policyはfcfs、easy_backfill、srpt、sf_srptの4つ、配置はfirst_fitとcompact（best-fit）、mixはtrace_likeとgang_heavy、ρ {0.6, 0.7}、π {0, 0.1, 0.3, 0.6}、seed 3本、horizon 40k/80kで、計768 runです。安定性は40k/80kのJCT比の傾きαで三値に分けました（0.2以下STABLE、0.8以上か打ち切りでDIVERGING、間はUNKNOWN、3 seedが一致したときだけcellにlabelを付ける）。予測・runner・採点scriptは、最初のrunの前にlocal commitで封印しました（外部timestampなし）。

## 結果

| 予測 | 内容 | 判定 |
|---|---|---|
| P0 | π=0ではfirst_fitとcompactのJCTが完全一致（器具の確認） | 的中 |
| P1 | π=0.3でcompactのexcessがfirst_fitより小さい | 外れ（gang_heavyは両方0） |
| P2 | 劣化はgang_heavyのほうが大きい | 外れ（採点可能0件、gang_heavyは1.00） |
| P3 | 決定予測：first_fitで逆転あり、compactで逆転なし | 外れ（両方0件） |
| P4 | trace_likeでeasy_backfillの劣化が最小 | 外れ（両端STABLEのpolicyなし） |
| P5 | gang_heavyでsf_srptの劣化 > easy_backfill | 外れ（両方1.00） |

cellのlabelはSTABLE 100、DIVERGING 21、UNKNOWN 7（128 cell中）。trace_likeのπ=0.6は16 cell中15が発散しました。compact配置は、両方STABLEの9組すべてでfirst_fitよりJCTを下げました（0.47〜0.96倍）。

## 何が変わったか

仮説H10（topologyは順位を変えない）を「未測」から「弱く支持、検出力不足」に変えました。封印前の点検に「そのmix・配置で摩擦がそもそも発生するか」を加えました。

## 何が失敗したか

外れた5本のうち3本は、gang_heavyで断片化が起きないことで決まっていました。測る前から結果が決まっていたわけです。π=0.1の1 runで`excess_nodes_per_placement`を見れば封印前に気づけました。π=0.6は強すぎて、逆転の判定材料を消しました。採点は変えずに残します。

## 証拠の範囲

合成model1つ、N=64、指数サービス、sigma 0、sticky配置、migrationなし。πは設定値で、実測したコストではありません。runnerを書いた作者自身が採点しました。

## まだ分からないこと

nodeの倍数でないgang mixや小さいπでも同じ順序が出るか、劣化の順の機構（遅くなったgangがserverを長く握ることで断片化が自己強化し、短いjobを先に流すpolicyほど滞留が短い、という候補）、実クラスタでの挙動は、いずれもUNKNOWNです。

## この結論が崩れるとき

新しいseed・小さいπ・nodeの倍数でないneedで、easy_backfillやfcfsがsrptより劣化しにくければ、事後の観察は崩れます。より高い負荷や別のpenalty形状で逆転が見つかれば、「順位は入れ替わらない」はこの負荷に限った話になります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-locality)で`python verify_locality.py`を実行します。封印hashの照合、封印済み採点scriptの再実行、gang_heavyのnullの確認、8 runの再simulationを1分ほどで行います。全768 runは`python run_e18.py`で約20分です（15 worker）。

## 証拠とデータ

[予測・runner・採点・simulator・結果](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-locality)。予測・runner・採点scriptは封印時のまま載せています。

## 外部からの検証

独立外部replicationは0件です。封印はlocal commitのみです。

## 次の実験

事後に見えた「srpt < sf_srpt < easy_backfill < fcfs」を決定予測にして、新しいseed、π {0.05, 0.1, 0.2}、nodeの倍数でないneed（例：4/12/24/40）を含むgang mixで封印検定します。

[[ja/research/gpu-scheduling-cold-reader/index|EP-0028]] → EP-0029
