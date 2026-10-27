---
research_id: GPU-SCHED-EP-0034
title: "状態結合の77%は、配置時点の使用中GPU数の層を残すだけで戻った"
date: '2026-10-27'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 決定予測D PASS（採点できた決定行は1行）。封印6/6
evidence_level: Sealed synthetic experiment, single model; decision scored on one row
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: E23 results and sealed prediction PRED-022
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic MSJ model with 64 GPUs in 8-GPU nodes, trace_like mix, first-fit placement; decision scored on one load-penalty row; mechanism candidate within the model only
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0034
source_episode_sha256: 838a51fd85bd0ca4c26e4d6694fd1db23a4bb2b0fd5ada41942eefff29fa3830
publication:
  status: publishable
tags:
- gpu-scheduling
- fragmentation
- sealed-prediction
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-occupancy-strata/" hreflang="en">English</a></p>

## 現在わかっていること

[前のNote](/ja/research/gpu-scheduling-fcfs-residual/)で、fcfsが断片化で余分に遅くなる分のおよそ半分は状態結合 a でした。E23では、Fの減速を「同じneed class、かつ配置時点の使用中GPU数が同じ層」の中だけで並べ替えました（CO）。すると、aの**77%**が戻りました（(ρ, π) = (0.55, 0.2)、6 seedすべてで半分以上）。到着順の粗いblockの中で並べ替える（CT）と、戻ったのは6%でした。

このモデルの中では、状態結合の大部分は「**断片化は混んでいるときに集中し、fcfsはそのときに代価を払う**」ことで説明できます。これは機構の候補であり、確定ではありません。

## 図で見る

d_X = log(J_X / J_CS) は、層Xを残すことで戻った遅れ。割合 d_X / a が1なら、その層だけでFの遅れを再現できます。値は6 seedの平均（括弧はSE）。

| 行 (ρ, π) | a | CO 使用中GPU数 | CQ 待ち行列長 | CT 到着順block |
|---|---|---|---|---|
| (0.55, 0.2) 決定行 | 0.051 (0.005) | 0.039 (0.003) **0.77** | 0.032 (0.002) 0.62 | 0.003 (0.003) 0.06 |
| (0.6, 0.1) 決定行外 | 0.019 (0.002) | 0.014 (0.002) 0.74 | 0.011 (0.002) 0.59 | 0.000 (0.002) 0.01 |
| (0.6, 0.2) | 採点外（fcfsのF・CO・CQがUNKNOWN） | | | |

配置時点の状態とexcess（余分にまたいだnode数）の順位相関。(0.6, 0.2)、need 2/4/8/16、6 seedの範囲。

| | Spearman(excess, 使用中GPU数) |
|---|---|
| fcfs BASE（π=0、減速なし） | 0.09〜0.39 |
| fcfs F | 0.17〜0.52 |
| srpt F | 0.19〜0.42 |

## この研究が示すこと

- 状態結合を運んでいるのは、主に「配置されたときにクラスタがどれだけ埋まっていたか」でした。使用中GPU数の5層を残すと77%、待ち行列長の5層では62%戻ります。2つの量は相関しています。
- 到着順の粗いblockの中で並べ替えても、ほとんど戻りません（0.9 SE）。小さい群の中で並べ替えるだけでは遅れは戻らない、という対照の役も果たしています。
- 決定行ではない(0.6, 0.1)でも同じ形（CO 0.74、CQ 0.59、CT 0.01）でした。
- 減速のないπ=0でも、混んでいるほど断片化します（S2）。これは配置の幾何から来る既知の関係です。
- fcfsのFでは、1配置あたりのexcess nodeがπ=0より平均0.119多くなりました（SE 0.001、6 seedすべて、S4）。減速がクラスタを混ませ、後から来たjobがより断片化したクラスタに置かれる、という帰還の向きです。

## この研究が示さないこと

- EP-0032の主な行だった(0.6, 0.2)での割合。今回はseed 2306のαが0.246で閾値0.2を超え、UNKNOWNで採点外でした。決定は(0.55, 0.2)の1行だけで決まりました。
- busy periodの中の細かい到着順の効き目。CTは5等分の粗いblockで、細かい順序は分けていません。
- 残りの23%が層の幅の中に残る状態の差なのか、別のつながりなのか。
- 実クラスタ、他のmix・placement・penalty形状。混んでいるほど断片化すること自体は新しくありません（Tiresias、Gandiva、Phillyの分析、bin packing）。

## 何を調べたか

前のNoteの並べ替えCS（同じneed classの中で減速を並べ替える）は、2つのつながりを同時に壊します。減速と配置時点のクラスタ状態とのつながりと、到着順で隣り合うjobとのつながりです。どちらがaを運んでいるかを分けるため、配置ごとの状態を記録する計器を足し、層を細かくした並べ替えを3つ加えました。

- **CO**：class × Fでの配置時点の使用中GPU数（値の分位で5層、同じ値は同じ層）
- **CQ**：class × 配置時点の待ち行列長（5層）
- **CT**：class × 到着順のblock（5等分）。状態ではなく時間の粗い流れだけを残す

## なぜ重要か

もし状態結合が「混んでいるときに断片化する」ことで来ているなら、断片化の害を減らす手は、総量を減らすことに加えて、混んでいるときの配置にもあります（どちらが効くかは比べていません）。到着順の流れで来ているなら、話は別です。並べ替えの単位を変えた対照で、2つを分けられます。

## 方法

封印実験E23（PRED-022）。合成MSJ model（64 GPU、8 GPU/node、trace_like、指数サービス、sticky first_fit、migrationなし）。行は (ρ, π) = (0.55, 0.2)・(0.6, 0.2)・(0.6, 0.1)、新seed 2301〜2306、窓160k/320k、864 simulation、CPUのみ。安定ラベルと既存の腕は前のNoteと同じです。

計器は、配置のたびに使用中GPU数・待ち行列長・空きGPUの散らばりとexcessを記録します。状態を読むだけで書き換えません。封印前に、計器を入れてもE22の4 taskで既存の腕が全項目で同じ値になり、RP＝Fが保たれることを確かめました。

決定予測D：採点できる決定行のすべてで d_CO ≥ 0.5a（採点できる行が少なくとも1つ）。

## 結果

封印6/6（P0、D、S1〜S4）。36 cell中4がUNKNOWN（11%）で、すべて(0.6, 0.2)のfcfs（F・RP・CO・CQ）でした。

| | 内容 | 判定 | 値 |
|---|---|---|---|
| P0 | 計器：fcfsのRPがFと一致 | PASS | 相対差 ≤1e-9 |
| D | 決定：d_CO ≥ 0.5a | PASS | (0.55, 0.2) 0.77（採点できたのはこの1行） |
| S1 | d_CO > d_CT | PASS | 0.039 対 0.003 |
| S2 | BASEで Spearman(excess, 使用中) > 0 | PASS | 0.09〜0.39 |
| S3 | F（fcfs・srpt）で同じ | PASS | 0.17〜0.52 |
| S4 | fcfs Fのexcess/配置 > BASE | PASS | 差0.119（SE 0.001） |

並べ替えた腕の仕事量はFと完全には一致しません（sizeとの組み合わせが変わるため）。320kでは全腕・全行で最大0.131%のずれで、封印で宣言した±1%の内側でした。

## 何が変わったか

前のNoteで「状態結合」と名前だけ付けていた項に、このモデルの中での中身の候補が付きました。混んでいるときほど断片化した配置になり（幾何）、fcfsではその減速がクラスタをさらに混ませます（帰還）。

## 何が失敗したか

- 主な行(0.6, 0.2)を採点できませんでした。320k窓でも、この行のfcfsはseedによって落ち着ききっていません。
- 封印前の読み取り専用レビューで、封印文の誤り（並べ替えた腕の仕事量がCSと一致するという主張）など4件の欠陥が見つかり、封印前に直しました。

## 証拠の範囲

1つの合成モデル、trace_like、first_fitだけで、決定は1行で決まりました。層は5つで粗く、層はFでの状態で決めています（並べ替えた腕の中の状態はFと同じではありません）。封印前に、捨てseed・20k窓の試運転でCO/CQ/CTの値を見てから、COを決定の腕、CTを対抗の腕に選びました。採点コードの試験に使った捨てデータ（seed 9001〜9006、4k/8k窓）の判定（全PASS）も見ました。どちらも封印に書いてあります。封印はローカルのgit commitのみです。

## まだ分からないこと

- (0.6, 0.2)で同じ割合が出るか。
- busy periodの中の細かい到着順の寄与。
- 残り23%の中身。
- 他のmix、placement、penaltyの形、実クラスタ。

## この結論が崩れるとき

- (0.6, 0.2)をより長い窓で採点し、d_CO < 0.5a になる。
- CTを細かいblockにすると、COと同じかそれ以上に戻る。その場合、効いているのは時間的に近いことで、使用中GPU数はその代理にすぎないことになります。
- 層を細かくしても割合が増えず、層の選び方で結果が大きく変わる。

## 自分で確かめる

[再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling)で `python verify_state_coupling.py` を実行します。PRED-022のhashを照合し、封印した採点コードをE23の公開結果に再実行し、C-058 modeのfcfs 1 task（CO/CQ/CTと配置時点の状態の要約を含む）を160k窓で再シミュレーションして公開値と一致することを確かめます。全864 simulationは `python run_e23.py`（`results/E23.json` を退かしてから）。

## 証拠とデータ

[パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling)に、PRED-022（封印したbytes）、計器を足したsimulator、`run_e23.py`、`analyze_e23.py`、E23の全run記録と採点結果があります。PRED-022の非公開記録のhashは改行がCRLFの作業コピーから取ったもので、公開した改行LFのファイルとは改行コードだけが違います。検算器は両方のhashを確かめます。

## 外部からの検証

外部の独立追試は0件です。

## 次の実験

(0.6, 0.2)で同じ割合が出るかを、より長い窓（320k/640k）で確かめます。CTを細かいblockにして、busy periodの中の順序がどれだけ効くかを分けます。
