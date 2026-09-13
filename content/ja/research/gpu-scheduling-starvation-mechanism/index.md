---
id: GPU-SCHED-EP-0003-JA
title: size-based schedulingが壊れる条件は平均gang sizeではなく全クラスタjobの有無
date: 2026-09-13
lang: ja
translation_of: GPU-SCHED-EP-0003
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 合成simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: 公開simulator、平均を一致させた対照mix、優先度×充填の要因計画、sealed prediction、E4出力
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: 全クラスタjob比率0〜0.03の合成需要mixと平均を一致させた対照群1つ、64 server、指数service、rho 0.7と0.85、preemption cost 0
source_episode: GPU-SCHEDULING/EP-0003
source_episode_sha256: ca6a566b0396730d61e2ec33a48c5cfd1a12b6246dcd2a43e5e03f067b0ff3de
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification, starvation, japanese]
---

<p class="language-switch">English: <a href="/scientific-os-research/research/gpu-scheduling-starvation-mechanism/">Original Research Note</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成simulation</span><span>探索的</span><span>peer reviewなし</span><span>外部再現 0</span></div>

[[ja/research/gpu-scheduling-phase-diagram/index|需要mixの相図と、失敗した3つの安定性判定器]]の続きです。

> **このnoteの実務的含意は降格されました。** [[ja/research/gpu-scheduling-real-traces/index|EP-0004]]が2つの公開traceの需要分布を測定し、Phillyのどのvirtual clusterにもpoolを占め切るjobが来ていないことを示しました。このnoteが要求する前提は、実測されたデータでは満たされていません。「全クラスタjobが来るか確認せよ」という規則は撤回し、pool容量に対する比の判定に置き換えます。EP-0004は本noteが自ら挙げた反証条件も満たしました。以下の機構そのものは変わらずmodel内では成立します。狭まったのはその射程です。本noteは2026-09-13時点で何を主張したかの記録として保持し、改変しません。

## 要約

先行する2つの研究が食い違っていました。EP-0001では、平均gang sizeが3.26で最大jobがクラスタの半分を要するmixで、greedy SRPTが勝ちました。EP-0002では、平均gang sizeが**より小さい**2.37でありながら全クラスタjobを含むmixで、greedy SRPTが需要classを飢餓させました。平均は逆を指していたので、平均を固定してsupportだけを動かしました。

平均gang sizeを4.076に一致させると、クラスタの半分で頭打ちのmixはgreedy SRPTで安定し（最悪classの平均JCT 3.31）、全クラスタjobを3%含むmixは飢餓します（最悪classの平均JCT 655.7）。閾値は3%よりはるかに低く、30,000本中15本で十分で、rho 0.85と同様にrho 0.7でも起きます。優先度規則と充填規則の2×2は、原因がsize優先度とgreedyな仕事保存の**組み合わせ**にあることを示します。どちらか単独では起きません。preemptionは原因ではなく、むしろ緩和します。封印した10本の予測は7/10でした。

## 研究質問

全クラスタjobの飢餓を引き起こすのは、平均gang sizeではなく、need分布のsupportがクラスタサイズNを含むことか。またその飢餓はsize優先度によるのか、greedyな仕事保存によるのか、両者が揃ったときだけか。

## なぜ重要か

「大gang workloadは素朴なschedulerを壊す」は比率についての言明であり、容量計画上の対応を促します。大jobの比率を監視せよ、と。しかし真の引き金が**クラスタ全体を要求するjob classの存在**であるなら、運用上の規則は別物で、はるかに鋭くなります。問われるのは何本あるかではなく、1本でもあるかどうかです。

監視すべき対象も変わります。集約平均が盲目になるのは、まさに全クラスタjobが希少な領域であり、そこは見落としが最も起きやすい領域でもあります。

## 方法

need 1〜32への重みは`theta = 0.4`の形を保ったまま`1 - p64`へ正規化し、残りの質量`p64`を64 serverクラスタのneed 64へ置きます。変わるのはsupportだけです。

| mix | 平均gang size | 最大need | 全クラスタjob比率 |
|---|---|---|---|
| p64 = 0 | 2.223 | 32 | 0 |
| p64 = 0.0005 | 2.254 | 64 | 0.0005 |
| p64 = 0.002 | 2.346 | 64 | 0.002 |
| p64 = 0.008 | 2.717 | 64 | 0.008 |
| p64 = 0.03 | 4.076 | 64 | 0.03 |
| **対照群** | **4.076** | **32** | **0** |

対照群の形状parameterは数値解で求め、平均gang sizeが`p64 = 0.03`のmixと一致するようにしました。飢餓が平均を追うなら、対照群も飢餓しなければなりません。

機構の要因計画は優先度規則と充填規則を交差させます。greedy SRPT（size優先度・greedy充填）、ServerFilling-SRPT（size・厳密充填）、FCFS（到着順・greedy）、ServerFilling-FCFS（到着順・厳密）、加えてEASY backfill（到着順＋予約）と非preemptiveなgreedy SRPT。負荷2点、seed 5本、30,000 job、全セルに120,000 jobのhorizon確認。432 run。

予測はSHA-256 `2f3b1808d806e9af888acaa77a7e00f7e9af86a13d58e42ac75e514a91157d05`で封印し、結果ファイルが存在しない状態でcommitしました。前研究の教訓を踏まえ、安定性の判定器そのものをsealed fileの`detector`に書き込んでいます。

## 結果

**平均を一致させた対照群が決着をつけます。** 平均gang sizeは同じ、結果は逆です。

| | 判定 | 平均JCT | 最悪classの平均JCT |
|---|---|---|---|
| 対照群、最大need 32、平均4.076 | 安定、最小flow balance 0.997 | 1.167 | 3.31 |
| p64 = 0.03、最大need 64、平均4.076 | class飢餓 | 20.55 | 655.7 |

**閾値は非常に低い。** `p64 = 0.0005`、すなわち30,000本中15本の全クラスタjobで、greedy SRPTは両負荷で既にそのclassを飢餓させます。64GPU classの平均JCTは312.5、EASY backfillは5.40、ServerFillingは1.21です。

**壊れるのは組み合わせだけ。** rho 0.85での64GPU classのflow balance。1.0は到着と同じ速さで完了していることを意味します。

| mix | FCFS | EASY backfill | greedy SRPT | greedy SRPT（preemptionなし） | ServerFilling-SRPT | ServerFilling-FCFS |
|---|---|---|---|---|---|---|
| p64 = 0.0005 | 0.989 | 0.989 | **0.397** | **0.000** | 1.000 | 1.000 |
| p64 = 0.002 | 0.962 | 0.992 | **0.308** | **0.000** | 0.996 | 0.996 |
| p64 = 0.008 | 0.677 | 0.987 | **0.386** | **0.000** | 0.997 | 0.995 |
| p64 = 0.03 | 0.395 | 0.987 | **0.443** | **0.000** | 0.998 | 0.996 |

size優先度だけでは飢餓せず、greedy充填だけでも飢餓しません。両方揃うと飢餓します。想定される機構は次のとおりです。クラスタ全体を要する jobは残り時間が全体最小になったときにしか開始できませんが、その残り時間は決して減りません。走らないからです。到着順優先度はhead-of-line blockingがクラスタを空けるためこの罠を逃れ、厳密充填は降順充填が最大jobに枠を確保するため逃れます。

**遅延は大きいのではなく有界でない。** 4倍のhorizonで飢餓classの平均JCTは2.83倍になり、1GPU classは1.02倍にとどまります。

**preemptionは原因ではない。** 非preemptive版のほうが悪く、flow balanceはちょうど0.000です。到着が続く間、全クラスタjobは1本も完了しません。preemptionは、先頭に到達しさえすればクラスタを掌握できるため、緩和側に働きます。

**集約指標の盲目性には境界がある。** greedy SRPTとEASY backfillの平均JCT比は、`p64`が0、0.0005、0.002、0.008と進むにつれ0.756、0.800、0.982、1.695と動きます。`p64 = 0.002`では比0.982で健全なpolicyと区別がつきませんが、全クラスタclassは63倍悪化しています。`p64 = 0.008`になると集約にも現れます。この指標は、希少なclassが希少であるうちだけ盲目です。

## 何が変わったか

EP-0002は「supportがNを含むこと」を仮説として提示しました。平均を一致させた対照群により、これは分離された結果になります。運用上の読み方も比率から述語へ変わります。問うべきは、クラスタ全体を要するjobが何本あるかではなく、1本でもあるかどうかです。

さらに2点。preemptionは悪化要因の疑いから緩和要因の実証へ移り、「集約指標はclass飢餓を見ない」という主張には条件が付きます。そのclassが希少である間に限る、という条件です。

## 何が失敗したか

封印した10本のうち3本が外れました。

| 予測 | 判定基準 | 結果 |
|---|---|---|
| R1 | p64が正の全点でgreedy SRPTがneed 64を飢餓させる | 4点すべてで支持 |
| R2 | p64 = 0では飢餓せずServerFillingに勝つ | 支持。1.084 対 1.210、対比0.896でEP-0001を再現 |
| R3 | 平均を一致させた対照群は飢餓しない | 支持。安定、最小flow balance 0.997 |
| R4 | ServerFillingの平均JCTはp64 0→0.008で25%未満しか動かない | **外れ。** 38%動いた（1.210→1.674）。厳密充填は飢餓を防ぐがコストは吸収しない |
| R5 | EASY backfillはどこでも飢餓しない | 支持。12/12セルが安定 |
| R6 | 飢餓するのはgreedy＋size優先度の組だけ | 支持 |
| R7 | 飢餓classは4倍horizonで2倍以上、小classは1.2倍未満 | 支持。2.83倍と1.02倍 |
| R8 | 集約比はp64 = 0.008まで30%以内に収まる | **外れ。** 0.008で1.695。盲目性には上記の希少性条件が必要 |
| R9 | 最悪class JCTは単調増加しp64 0.002以上で100を超える | 支持。4.4、312.5、394.4、425.7、655.7 |
| R10 | ServerFilling-FCFSはどこでも安定で平均JCTではServerFilling-SRPTに劣る | **外れ。** 平均JCTの側は6 mix全部で成立。ただし1セルが閾値1.30に対し1.31倍成長し裁定不能 |

R10は際どい側で落ちました。完了率は1.000、abortなし、flow balanceはhorizonとともに改善しています。閾値を事後に動かさなかったので、外れとして残します。

解析上の欠陥を1つ、結果を見た後に修正しました。採点が厳しくなる方向です。horizon比較が当初、単一seedの長時間実行を5 seedの短時間平均で割っており、seed間変動が成長率に混入していました。現在は同一seed対で比較します。R10の判定は変わりませんでした。

## 証拠境界

**支持されること:** このsimulatorとこれらのmixの下で、greedyなsize-based schedulingにおける全クラスタjobの飢餓が、需要分布の平均ではなくsupportを追うこと。全クラスタjob比率0.0005で現れること。size優先度とgreedyな仕事保存の両方を要すること。preemptionが原因ではなく緩和側に働くこと。

**支持されないこと:** production clusterについての主張。need格子は2の冪なので、「クラスタの半分」と「クラスタ全体」の間（33〜63）は未検証です。preemption costは0、service時間は指数分布。実traceは未実行であり、そもそも実際のGPU clusterに全クラスタjob classが存在するのか——この発見が実務上意味を持つための前提——は、ここでは検証されていません。

## UNKNOWN

- 閾値がちょうどneed = Nなのか、N/2より上のどこかから始まるのか。格子上には32と64しかありません。
- preemption costが非ゼロのとき緩和が消えるか。
- 重尾service時間が、集約指標が気づき始める比率を変えるか。
- 非preemptive版が同じ理由で飢餓するのか、単にpreemptできないためか。
- 実traceの需要分布。最優先の未解決項目であり、PhillyやAlibaba PAIにおける全クラスタjobの比率は0.0005という閾値と直接比較できます。

## 反証条件

- 独立のsimulatorで、平均を一致させた対照群が飢餓する。その場合、平均gang sizeが駆動要因として復活します。
- 全クラスタjobを含むmixが、いずれかの負荷でgreedy SRPTのもと安定に動く。
- より長いhorizonで飢餓classのJCTが収束する。
- ServerFilling-FCFSまたはFCFSが全クラスタclassを飢餓させる。その場合、優先度と充填の分離が崩れます。
- 公開traceに全クラスタjob classが存在しない。その場合、この発見はmodelについては真であるが実務には無関係ということになります。

## 再現

### artifactと採点の簡易確認

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-phase
```

### 完全な再走

```bash
cd reproduction/gpu-scheduling-phase
python run_e4.py
python analyze_e4.py
```

`run_e4.py`は全セルに120,000 jobのhorizon確認を含むため、裁定されていない仮定に依存する判定はありません。

## 証拠 / Artifacts

- [公開再現package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-phase)
- [封印済みPRED-003、判定器を含む](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-003.json)
- [E4の採点](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E4_grading.json)
- [E4 report、平均を一致させた対照群を含む](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E4_report.txt)

## 外部監査

- 独立再現: 0
- 失敗した再現: 0
- 確認されたbug: 0
- 未解決の批判: 0

## 次の実験

公開production traceにおける全クラスタjobの比率を測ります。Blox経由のPhilly、Kubernetes scheduler simulator経由のAlibaba PAIで、0.0005という閾値と比較します。それが済むまで、この発見はmodelを記述しているのであって、実在するclusterを記述してはいません。副次的な実験として、2の冪の制約を外し、クラスタの半分と全体の間のどこに飢餓の境界があるかを特定します。
