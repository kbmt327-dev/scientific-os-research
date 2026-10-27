---
research_id: GPU-SCHED-EP-0032
title: "fcfsが断片化で余分に遅くなる分の、およそ半分は減速と状態の結びつきだった"
date: '2026-10-27'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 決定予測P2 PASS、新seedで再現（余裕は薄い）。構成項の予測P3はFAIL
evidence_level: Sealed synthetic experiments, single model; sealed replication on new seeds
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: E20-E22 results and sealed predictions PRED-019, PRED-020, PRED-021
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic MSJ model with 64 GPUs in 8-GPU nodes, trace_like mix, first-fit placement, three load-penalty rows; no real-cluster generalization
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0032
source_episode_sha256: 96438ae02cbbb411074130c15c9270577cae0972e48c056c604bb46ff6f72e1a
publication:
  status: publishable
tags:
- gpu-scheduling
- fragmentation
- sealed-prediction
- replication
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-fcfs-residual/" hreflang="en">English</a></p>

## 現在わかっていること

この合成モデルの (ρ, π) = (0.6, 0.2) では、fcfsが断片化で余分に遅くなる分のおよそ半分（0.52〜0.56）が**状態結合 a** でした。aは、各jobの減速を同じneed classの中で並べ替えると消える部分で、減速と配置時点のクラスタ状態とのつながりと、到着順で隣り合うjobとのつながりの両方を含みます。封印した決定予測「aがその半分以上」はE21で通り、一度も使っていないseedでの封印再現E22でも通りました。

ただし「半分以上」の余裕は薄く、E22単独では6 seed中3つが逆向きでした。両方を合わせた12 seedで、余裕の片側95%下限は0.0006です。この下限は、余裕の薄さがこの再現のきっかけになったE21の6 seedを含む精度の推定で、独立の検定ではありません。言えるのは「aはおよそ半分」までで、「aが主」とは言えません。a > 0 そのものは3行・18 seedのすべてで成り立ちました。

## 図で見る

fcfsが断片化で余分に遅くなった分 T = log(J_F / J_U) の分解。値は6 seedの平均（括弧はSE）。

| 行 (ρ, π) | 実験 | T（全体） | a 状態結合 | b class内ばらつき | c class間構成 | aの割合 |
|---|---|---|---|---|---|---|
| (0.6, 0.2) | E21 | 0.181 (0.013) | 0.102 (0.011) | 0.022 (0.005) | 0.058 (0.005) | **0.56** |
| (0.6, 0.2) | E22 再現 | 0.171 (0.007) | 0.089 (0.005) | 0.016 (0.004) | 0.066 (0.006) | **0.52** |
| (0.55, 0.2) | E21 | 0.035 (0.005) | 0.056 (0.005) | 0.008 (0.002) | −0.029 (0.002) | 1.59 |
| (0.55, 0.2) | E22 再現 | 0.038 (0.007) | 0.051 (0.006) | 0.007 (0.002) | −0.020 (0.002) | 1.34 |
| (0.6, 0.1) | E21 | −0.006 (0.002) | 0.018 (0.001) | 0.003 (0.001) | −0.027 (0.001) | — |
| (0.6, 0.1) | E22 再現 | −0.004 (0.003) | 0.017 (0.002) | 0.002 (0.001) | −0.024 (0.001) | — |

(0.6, 0.2)でのseedごとの余裕 a − 0.5T：E21は6 seedすべて0以上（最小0.0001）、E22は −0.0077、−0.0105、0.029、0.0149、0.0007、−0.0035。

## この研究が示すこと

GPU仕事量をそろえた対照の梯子を使うと、fcfsの断片化の害を3つに分けられます（RP・CM・Uの仕事量はFと完全に一致し、並べ替えたCSはsizeとの組み合わせが変わるため±0.2%以内）。

- **a 状態結合**：Fで各jobが受けた減速を、同じneed classの中で並べ替えるだけ（CS）で、fcfsのJCTは(0.6, 0.2)で約9〜10%下がります。減速の顔ぶれはclassごとに変えず、どのjobがいつその減速を受けたかのつながりを壊した結果です。
- **b class内ばらつき**：小さく正。
- **c class間構成**：大きいgangほど遅くなる偏り。負荷によって符号が変わり、(0.6, 0.2)では正、(0.55, 0.2)と(0.6, 0.1)では負でした。π0.1では状態結合と構成が打ち消し合い、全体Tはほぼ0です。

この結果は、EP-0030で「負荷をそろえた後もfcfsに約0.50の差が残る」とした観察を、厳密な対照のもとで置き直したものです。2つは定義が違う（EP-0030は単位サービス時間での負荷補間、ここでは同じ仕事量の対照）ので、数値は比べません。

## この研究が示さないこと

- 状態結合の中身。CSは、減速と配置時点の状態との結びつきと、到着順で隣り合うjobとの結びつきを同時に壊します。aにはその両方が入ります。中身を分けたのは[次のNote](/ja/research/gpu-scheduling-occupancy-strata/)です。
- 「aが主である」こと。余裕は分解能の境目にあります。
- 実クラスタ、他のmix・placement・penalty形状への一般化。πは実測したコストではなく、つまみです。
- 新規性。

## 何を調べたか

EP-0030で唯一残ったfcfsの差が、断片化に固有の何かなのか、それとも仕事量の増加で説明できるのかを調べました。断片化した実行（F）と、GPU仕事量をそろえたπ=0の腕を並べました。RPはFの減速をそのまま掛ける腕（fcfsではFと一致するはずの計器確認）、CSはneed classの中で並べ替え、CMはclassごとの平均、Uは全体の平均です。a = log(J_F/J_CS)、b = log(J_CS/J_CM)、c = log(J_CM/J_U) で、T = a + b + c です。

## なぜ重要か

断片化の害が「仕事量が増えるから」だけなら、配置の工夫は総量を減らす以上のことをしません。状態との結びつきが効いているなら、いつ断片化した配置になるかが問題になります。この区別は、同じ仕事量の対照を作らないと付きません。

## 方法

3つの封印実験を順に行いました。いずれも合成MSJ model（64 GPU、8 GPU/node、trace_like mix、指数サービス、sticky first_fit、migrationなし、遅さは rate = 1/(1 + π·excess)）で、行は (ρ, π) = (0.55, 0.2)・(0.6, 0.2)・(0.6, 0.1)、各6 seedです。cellの安定ラベルは2つの窓の間のα（平均JCTの窓に対する弾性）で付け、6 seedすべてが一致したときだけSTABLEとします。

1. **E20**（PRED-019）：40k/80k窓。648 simulation。封印後に1件だけ修正しました。初回は全simulationを終えた後、JSON書き出しで落ちたため、書き出しの引数だけを直して再実行しました（simulationと採点には触れず、初回の結果値は読んでいません。simulationは決定的です）。
2. **E21**（PRED-020）：予測と閾値をそのまま、窓だけ160k/320kに伸ばし、新seed 2101〜2106。封印前に、本番と同じ6 seed数の別seedで安定ラベルだけを先に確かめました（このpilotのJCTは見ていません）。ただし、E20の採点後に診断として腕ごとの40k/80kのJCTを表示しており、そこから分解の向き（F > CS ≈ CM > U）が大まかに読めました。PRED-019の予測と閾値はその表示より前に決めたもので、E21では1つも動かしていません。
3. **E22**（PRED-021）：E21の予測・閾値・cell・窓を変えず、新seed 2201〜2206で再現。決定はR1「P2が新seedで通る」。R1は真の余裕が0でも約半分の確率で通る判定なので、12 seed合算の片側95%下限が正であること（R2）を併記すると封印に書きました。

## 結果

- **E20**：採点できませんでした。27 cell中14がUNKNOWN（fcfsのπ>0の15 cellのうち、(0.6, 0.1)のUを除く14）。計器のP0（RP＝F）だけPASSで、P1〜P5は採点不能でした。同じ構成でもseedによってαが −0.48〜0.97 に割れ、腕によらず同じseedの型で出ました。fcfsは実効負荷0.7〜0.8付近で、この窓では落ち着きません。この時点で、EP-0030の残差0.50は「確立していない」に下げました。
- **E21**：封印5/6、決定予測P2 PASS。27 cellすべてSTABLE。P3（構成cが決定行すべてで正）はFAIL。
- **E22**：R1 PASS（aの割合0.52・1.34）、R2 PASS（合算下限0.0006、平均0.0075、SE 0.0039）、R3（E22単独の下限、報告のみ）FAIL（下限 −0.0087）。PRED-020の文言で採点し直すとE21と同じ5/6でした。

## 何が変わったか

- EP-0030の「fcfsだけに残る差」は、E20で一度「確立していない」に下げ、E21で厳密な対照のもとで実在すると置き直しました。
- E21の決定予測P2のPASSは、新seedで再現しました。ただし割合は0.52〜0.56で、書き方を「aはおよそ半分」に留めます。

## 何が失敗したか

- E20は窓が短く、採点できませんでした。少数seedの一致ラベルを前提に次の実験を組んだことが原因です。以後、前提にするcellは本番と同じseed数で先にラベルだけ確かめています。
- P3（構成の項が正）は外れました。構成の項は負荷によって符号が変わります。
- E22単独では、決定の余裕が負のseedが半数ありました。

## 証拠の範囲

1つの合成モデル、trace_like mix、first_fit、3行だけです。封印はローカルのgit commitのみで、外部のタイムスタンプはありません。採点コードと予測は同じ作者が書き、独立の追試は0件です。srptのUの腕は再配置されたjobの最終rateを使う近似なので、srpt側の値は解釈を保留しています。

## まだ分からないこと

- 状態結合のうち、配置時点の混み具合と、到着順のつながりがそれぞれどれだけか（→ [EP-0034](/ja/research/gpu-scheduling-occupancy-strata/)で一部を分けました）。
- 構成の項cの符号が、どの負荷で、なぜ変わるのか。
- 他のmix、placement、penaltyの形、実クラスタ。

## この結論が崩れるとき

- 新しいseedや長い窓で、(0.6, 0.2)のaの割合が0.5を明らかに下回る（合算の上限が0.5未満になる）。
- a ≤ 0 のseedが現れる。今のところ18 seedすべてで正です。
- 同じ仕事量の対照の作り方（並べ替えの単位など）を変えると、aが消える。

## 自分で確かめる

[再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling)で `python verify_state_coupling.py` を実行します。封印した予測4本のhashを照合し、封印済みの採点コードをE20〜E23の公開結果に再実行し、2 taskを160k窓で再シミュレーションして公開値と一致することを確かめます（1コアで約2分）。全2,808 simulationの再実行は `run_e20.py`〜`run_e23.py` で行えます。

## 証拠とデータ

[パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling)には、封印した予測PRED-019〜022、simulator、runner、採点コード、E20〜E23の全run記録と採点結果が入っています。simulatorは非公開の作業repositoryのE23封印時点のものです。封印前にE22の4 taskで既存の腕の全項目が同じ値になることを確かめ、検算器はE21のfcfs 1 taskを再シミュレーションして公開値と照合します。

## 外部からの検証

外部の独立追試は0件です。封印はローカルの記録で、第三者が封印の時刻を確かめる手段はありません。

## 次の実験

状態結合の中身を、配置時点の状態で層に分けて確かめました（[EP-0034](/ja/research/gpu-scheduling-occupancy-strata/)）。(0.6, 0.2)の割合をさらに確かめるには、より長い窓（320k/640k）が要ります。
