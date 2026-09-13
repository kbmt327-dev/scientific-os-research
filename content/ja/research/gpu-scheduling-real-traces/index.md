---
id: GPU-SCHED-EP-0004-JA
title: 実traceにpoolを占め切るjobは来ておらず、飢餓の境界は連続だった
date: 2026-09-13
lang: ja
translation_of: GPU-SCHED-EP-0004
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 公開trace測定＋合成simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: public-trace-retrospective-and-synthetic-simulation
  source: PhillyとAlibaba PAIの公開trace、virtual cluster単位の容量実測、封印予測2本、E6の閾値掃引
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 公開trace 2本（GPU job 194,202本）から取ったのは需要の形のみ、Philly virtual cluster 11個、加えて64 server・rho 0.7と0.85でのjob size対pool容量比の掃引
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0004
source_episode_sha256: 6ec6a9dba06e28147c46effd2d7ca5d9867a55b9a0ff918f05649c40ab586653
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification, traces, retraction, japanese]
---

<p class="language-switch">English: <a href="/scientific-os-research/research/gpu-scheduling-real-traces/">Original Research Note</a></p>

<div class="evidence-strip"><span>Finding</span><span>公開trace＋合成</span><span>探索的</span><span>peer reviewなし</span><span>外部再現 0</span></div>

[[ja/research/gpu-scheduling-starvation-mechanism/index|size-based schedulingが壊れる条件は平均gang sizeではなく全クラスタjobの有無]]の続きで、そのnoteの実務的含意を降格するものです。

## 要約

前研究は「全クラスタjobを含む需要分布は、比率0.0005でもgreedyなsize-based schedulingを壊す」と結論し、実務的含意として「クラスタ全体を要するjobが来るかを最初に確認せよ」と書きました。本研究はその規則を2つの公開traceに当て、**封印文で事前に約束したとおり降格しました**。

Phillyが実際にschedulingしている単位であるvirtual cluster 11個すべてで、pool全体を要するjobの確率は0.00000です。最悪でも最大jobはpoolの59%しか要しません。つまり機構が要求する条件は、実測されたデータのどこにも現れませんでした。

これにより、本研究全体の実務的な射程が、前研究が一度も測っていない帯——poolの半分から全体までのjob——にかかることになりました。掃いてみると閾値は存在せず、劣化は連続かつ急峻で、完全な飢餓はちょうどpool全体のサイズでのみ起きます。実用的な安全境界は0.75です。実測比0.59ではそのclassは飢えず、1GPU jobの7.4倍遅くなります。害は実在しますが、無限の待ちではなく遅延です。

## 研究質問

実在のGPU clusterの需要分布は、機構が要求するjob classを含むか。またpoolの半分から全体までの間に、閾値があるのか連続的な劣化があるのか。

## なぜ重要か

model内で示された機構が注目に値するのは、その前提条件がmodelの外で成立する場合だけです。前提を検査せずに機構だけを公開すれば、「全クラスタjobが来るか確認せよ」という実務的に聞こえる規則が、実測データに含まれない条件に紐づいたまま残ります。

置き換えた規則は種類が異なり、それでも行動可能です。重要なのは最大jobとpool容量の比であり、予測される失敗は飢餓ではなく数倍の遅延です。

## 方法

**E5、需要の形。** Microsoft Philly（`cluster_job_log`、GPU job 112,018本）とAlibaba PAI v2020（100K標本、82,184本）のjob GPU数。PRED-004としてSHA-256 `7ef0f5b21d46318e6008a1be3021e9c1ffbefbe3fb23e959c3cffa7268048cbe`で封印しました。

Phillyはvirtual cluster単位でschedulingするため、VCごとのピーク同時GPU使用数を取れば、poolの容量を仮定ではなく**実測**できます。ピーク同時使用は容量の下界なので、真のquotaがより大きければ比はさらに小さくなります。結論はこの向きに頑健です。

**E6、未測定の帯。** 小jobの背景群に、need `m`の大classを1つ加えて確率0.002で到着させ、`m`をN/2からNまで掃きます。N = 64、rho 0.7と0.85、seed 5本、全セルに120,000 jobのhorizon確認。463 run。PRED-005としてSHA-256 `fe3e27d68d27c5c8eb9fb6633d133e17fd6c4ba09158ab80d901dc4630ccb902`で封印しました。ServerFillingは2のべき乗を要求するため、m ∈ {32, 64}でのみ実行しています。他のサイズで報告するのはアルゴリズムの誤用になります。

どちらの封印も、対応する結果ファイルが存在しない状態でcommitしました。

## 結果

**需要の形。** どちらのtraceも1GPU jobが支配的で、裾は薄いです。

| trace | GPU job | E[k] | 中央値 | 最大k | P(k=1) | 2のべき乗の割合 | p(k ≥ 64) |
|---|---|---|---|---|---|---|---|
| Alibaba PAI v2020 | 82,184 | 2.736 | 1 | 150 | 0.788 | 0.876 | 0.00164 |
| Microsoft Philly | 112,018 | 1.744 | 1 | 128 | 0.866 | 0.9995 | 0.00035 |

**仮想的な**64 GPU poolに対して見れば、PAIの0.00164は前研究の閾値の3.3倍で、封印した予測は当たりました。しかし封印後に足した測定のほうが、問いにより直接答えていました。

**実測されたpoolに、poolを占め切るjobは来ていません。**

| virtual cluster | job | ピーク同時GPU | 最大k | 最大k / 容量 | p(k ≥ 容量) |
|---|---|---|---|---|---|
| 6214e9 | 51,980 | 603 | 16 | 0.03 | 0.00000 |
| **11cb48** | 19,401 | 217 | 128 | **0.59** | 0.00000 |
| 6c71a0 | 15,014 | 290 | 48 | 0.17 | 0.00000 |
| ee9e8c | 5,859 | 532 | 128 | 0.24 | 0.00000 |
| 他7 VC | 19,412 | 66–360 | 1–32 | 0.02–0.25 | 0.00000 |

ちょうど1つ、11cb48だけが、poolの半分から全体までの帯——前研究がN/2（飢えない）とN（飢える）しか測っていない帯——に落ちました。

**帯は連続で、閾値はありません。** rho 0.85のgreedy SRPT。flow balance 1.0はそのclassが自分の到着に追いついていることを意味します。

| m / N | 0.50 | 0.53 | 0.56 | 0.59 | 0.63 | 0.69 | 0.75 | 0.88 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|
| classのflow balance | 0.998 | 0.996 | 0.996 | **0.996** | 0.984 | 0.949 | 0.913 | 0.708 | **0.390** |
| classの平均JCT | 3.7 | 4.8 | 6.2 | **7.9** | 13.7 | 30.9 | 49.2 | 151.5 | **330.7** |
| 1GPU jobの平均JCT | 1.07 | 1.07 | 1.07 | 1.07 | 1.07 | 1.07 | 1.07 | 1.06 | 1.05 |

封印文には機構から導いた予想も書いてありました。`m = N`だけが「優先度順でrank 1でなければそもそも起動できない」という質的に異なる性質を持ち、`m < N`は容量をめぐる連続的な競争なので、劣化はN/2で段差を作るのではなく急峻だが滑らかになるはずだ、と。そのとおりになりました。

**安全境界 `r_safe` = 0.75。** ここまではclassのflow balanceが0.9以上に保たれます。Phillyの実測比0.59ではそのclassは飢えませんが、1GPU jobの**7.4倍**遅くなります。

EASY backfillはどの比でもclassを飢餓させず、最悪flow balance 0.999、最大JCT 6.7。4つの研究を通じて一度も破綻していない唯一のpolicyです。非preemptive版は全点でgreedy SRPTより悪く、0.75で既にflow balance 0.308、0.875以上で0.000です。

## 何が変わったか

前研究の実務的含意を降格します。データを見る前に封印文へ書いた約束の履行です。

> 決定予測が的中した場合、実務的含意を「pool全体を占めるjobが来るか確認せよ」から「最大jobが容量の`r_safe`を超えるか」という条件文へ降格し、domainの見出しを**modelでは実在するが、調べた2つの公開traceでは飢餓として未観測**に書き換える。

- **撤回:** 「クラスタ全体を要するjobが来るか最初に確認せよ」。実測poolにそのようなjobは来ていません。
- **置き換え:** 最大jobが**pool容量の0.75**を超えるかを見る。Phillyの最悪VCは0.59で、この境界の下にあります。
- **害の形の改訂:** 実際の比率が生むのは無限の待ちではなく数倍の遅延です。

機構そのものは変わっておらず、model内では依然として成立します。変わったのはその射程です。

## 何が失敗したか

**PRED-004は5/10。** 情報量が大きいのはS8の外れ方で、**本プロジェクト自身の主張を弱める向き**に外れました。実traceの裾は、先行研究で使った合成族より**軽い**のです。E[k]を揃えたとき、合成のp(k ≥ 64)は0.00403に対しPAIは0.00164、0.00073に対しPhillyは0.00035で、2.1〜2.5倍の差があります。**合成設定は飢餓機構に有利に働いていました。** S3・S4・S7・S10も外れ、いずれも実traceの裾を重く見積もりすぎたためです。

**事前登録した撤回trigger は発動しませんでしたが、発動すべきでした。** triggerは**仮想的な**pool sizeについての予測2本に紐づいており、うち1本が的中したためです。VC単位の実測は同じ問いにより直接答え、逆を指していました。封印時の測定量が、それが決着させるはずの問いの代理として不適切だった——**自分の約束に守られてしまう**形です。教訓として記録しました。封印時に「この測定は問いの代理として妥当か」を一行書くこと。

**PRED-005は9/10。** 外れたのはT6のみ。比率不変は近似にすぎず、ずれは**大きいpoolほど危険**という向きに系統的でした。`m/N = 1.0`でflow balanceはN = 64で0.390、N = 128で0.236です。実在のvirtual clusterは217〜603 GPUで、ここで測ったどれより大きいため、実規模では`r_safe`がさらに低い可能性があります。

決定予測T4は**本プロジェクト自身の主張に不利な側**、すなわちPhillyの実測比ではclassが飢え**ない**という側に指名してありました。的中したので、降格が自動的に実行されました。

## 証拠境界

**支持されること:** この2つの公開traceでは1GPU jobが支配的で裾は薄く、Phillyのどのvirtual clusterも実測容量の全体を要するjobを受け取っていないこと。model内では半分から全体までの帯の劣化が連続で、実用的な境界が0.75にあること。実測比ではそのclassは飢餓ではなくおよそ7倍の遅延を被ること。

**支持されないこと:** 実traceから取ったのは需要の**形だけ**です。実際の到着列でpolicyを走らせてはおらず、閾値実験は実測比率を合成modelに入力したものです。容量は公表quotaではなくピーク同時使用から推定しました。2本のtraceはGPU clusterの母集団ではありません。この測定は既存の公開データに対するretrospectiveであり、著者は事前の予想を持っているため、事前登録forward評価ではなく、そのようには数えません。

## UNKNOWN

- `r_safe`の負荷依存。rho 0.7では0.875でもflow balance 0.856を保つので、負荷が上がると境界は下がりますが、細かくは測っていません。
- 比率不変のずれがN = 512、1024でも続くか。実在のvirtual clusterはその領域にあり、ずれの向きは不利です。
- PAIのquota group構造での同じ分析。100K標本ではなく完全traceが必要です。
- PhillyとPAI以外のtrace。Alibaba v2023はnodeあたり8 GPU上限のため対象外です。
- preemption cost非ゼロとの相互作用。未測定のままです。

## 反証条件

- これらのvirtual clusterの公表quota表が、ピーク同時使用よりはるかに小さい容量を示す。その場合、実jobがpoolサイズに達していた可能性が戻ります。
- 別のproduction traceが、scheduling poolの容量以上のjob classを含む。
- より細かい掃引が半分から全体の帯の内側に不連続を見つける。その場合、閾値としての読みが復活します。
- 512または1024 serverで測った`r_safe`が0.59を下回る。その場合、Phillyの最悪VCは害のある領域に戻ります。

## 再現

### artifactと採点の簡易確認

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-phase
```

封印した4本のdigest、採点、そして実測されたどのvirtual clusterにもpoolを占め切るjobが存在しないことを検証します。

### 完全な再走

```bash
cd reproduction/gpu-scheduling-phase
python run_e6.py
python analyze_e6.py
```

trace測定そのものには生の公開traceが必要で、ここでは再配布していません。`analyze_traces.py`は同梱し、それが生成したtrace別・virtual cluster別の測定値を`results/E5_traces.json`に置いています。traceは`msr-fiddle/philly-traces`と`alibaba/clusterdata`から取得してください。

## 証拠 / Artifacts

- [公開再現package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-phase)
- [封印済みPRED-004、発動しなかった撤回条件を含む](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-004.json)
- [封印済みPRED-005、決定予測とそれが起動する降格を含む](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-005.json)
- [traceから導出した測定値](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E5_traces.json)
- [E6閾値掃引の採点](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E6_grading.json)

## 外部監査

- 独立再現: 0
- 失敗した再現: 0
- 確認されたbug: 0
- 未解決の批判: 0

## 次の実験

64、128、256、512 serverで`r_safe`を測ります。本研究で唯一外れた予測は、比率不変が成り立たず、ずれが「大きいpoolほど悪い」向きであることを示しており、実在のvirtual clusterはここまでに測ったどれよりも大きいためです。Phillyの0.59が本当に安全側かどうかは、その測定で決まります。
