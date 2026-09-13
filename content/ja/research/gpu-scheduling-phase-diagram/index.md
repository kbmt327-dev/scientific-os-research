---
id: GPU-SCHED-EP-0002-JA
title: 需要mixの相図と、失敗した3つの安定性判定器
date: 2026-09-13
lang: ja
translation_of: GPU-SCHED-EP-0002
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 合成simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: 公開simulator、計測器の較正、2 horizonの裁定、sealed prediction、E2/E3出力
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: 1パラメータの合成需要mix族、64 server、指数service、rho 0.7〜0.95、preemption cost 0、sigmaは3.0まで
source_episode: GPU-SCHEDULING/EP-0002
source_episode_sha256: 656775b68fee9214ef5490de02441111ac1451b4f24cab4d00556716c52649f4
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification, instrument, japanese]
---

<p class="language-switch">English: <a href="/scientific-os-research/research/gpu-scheduling-phase-diagram/">Original Research Note</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成simulation</span><span>探索的</span><span>peer reviewなし</span><span>外部再現 0</span></div>

[[ja/research/gpu-scheduling/index|摩擦とworkload mixでGPU schedulingの原理が逆転する]]の続きで、そのnoteが公開の場で宣言した「次の実験」を実施したものです。

## 要約

GPU需要mixを連続軸として掃き、ServerFilling-SRPTがgreedy SRPTを上回る閾値を探すとともに、推定誤差の軸を補正したnoise modelで再測しました。封印した予想は2つとも外れ、外れ方に情報がありました。低mix側に交点は存在しません。rho 0.85以上ではgreedy SRPTがどこでも安定しないからです。順位の逆転は**逆側**、gang sizeが等質な領域にあり、そこではgreedy SRPTが7〜17%上回ります。補正したnoise modelは、容量を予約する唯一のpolicyについてEP-0001の推定誤差の結論を覆しました。

より大きな結果はschedulingではなく計測にあります。「安定か発散か」を単一horizonで判定する検出器が3回続けて失敗し、2回目は本プロジェクトが既に無効と記録した検出器を、次の解析scriptの中で復活させたものでした。10本の予測は、補正後の計測器で5/10、実際に走らせた時点の計測器で4/10でした。

## 研究質問

連続的な需要mix軸上で、ServerFilling-SRPTはどこでgreedy SRPTを上回るか。その閾値は負荷で動くか。また、EP-0001の「size推定誤差はほとんど効かない」という結果は、sigmaが大きいほど中位推定値が縮む平均不偏lognormal error modelの産物ではなかったか。

## なぜ重要か

scheduling研究は通常、平均job完了時間で順位を付けます。ある需要classが永久に終わらないまま平均が健全に見えるなら、その順位は運用者が気にする量を測っていません。各セルを平均応答時間ではなく**安定性**で標識する相図は速度向上表とは別の対象であり、原理を採用する前に実務家が必要とするのは前者です。

計測の側は、待ち行列系のsimulation研究全般に効きます。主張している量である安定性は無限horizonについての言明であり、試した有限窓の代理指標はすべて、沈黙するか誤るかのいずれかでした。

## 方法

需要mixを1パラメータ族として表現しました。64 serverのクラスタで、need 1〜64に対し`P(need = 2^i)`が`theta^i`に比例します。`theta = 0.4`は小job中心で平均gang size 2.37、約60%が1GPU job。production traceについて報告されている形状に似せて選びましたが、本研究のどこでも実trace dataは使っていません。`theta = 2.0`はgang支配で平均gang size 43です。

- **E2**: mix 7点 × 負荷3点（rho 0.7、0.85、0.95）× policy 4種 × seed 5本、各30,000 job。420 run。
- **E3**: 平均不偏と中位不偏のerror、sigma ∈ {0, 0.5, 1, 2, 3}、policy 3種、seed 5本、`theta = 0.4`・rho 0.85。150 run。
- **裁定**: 単一horizonの規則で判定が確定しなかった59セルを30,000 jobと120,000 jobで再走。236 run。

予測はSHA-256 `d726c5a701367f3be0bff47eba10267ee5fcd43bc4b830ec70c97a22477ed8a0`で封印し、結果ファイルが存在しない状態でcommitしました。

## 結果

相図21セル。`.`安定、`S`ある需要classが飢餓、`O`系全体の過負荷、`X`測定不能、`?`裁定不能。

| rho | theta | FCFS | EASY backfill | greedy SRPT | ServerFilling-SRPT |
|---|---|---|---|---|---|
| 0.70 | 0.4 | . | . | **S** | . |
| 0.70 | 0.8 | X | . | O | . |
| 0.70 | 1.25 | O | . | . | . |
| 0.70 | 2.0 | . | . | . | . |
| 0.85 | 0.4 | . | . | **S** | . |
| 0.85 | 0.8 | X | . | O | . |
| 0.85 | 1.6 | O | . | O | . |
| 0.85 | 2.0 | O | . | ? | . |
| 0.95 | 0.4 | X | . | **S** | . |
| 0.95 | 1.0 | X | . | O | . |
| 0.95 | 2.0 | O | . | O | . |

ServerFilling-SRPTとEASY backfillは21セル全部で安定。greedy SRPTは3セルのみで、いずれもrho 0.7かつ大gangが等質な領域です。全格子は`results/E2E3_report.txt`にあります。

**集約指標は破綻を隠します。** `theta = 0.4`・rho 0.85でgreedy SRPTの平均JCTは2.06、EASY backfillは2.11。比0.98で、わずかに良い普通のpolicyに見えます。同じ実行で64GPU classは366、backfillは7.1で、52倍の差です。

**逆転は逆向きでした。** rho 0.7でServerFilling/greedyの比は`theta = 1.25`で0.248、1.6で1.070、2.0で1.169。ServerFillingの優位は大gangが多いことではなく、gang sizeの**異質性**から来ます。すべてのjobが同じ大きさなら、厳密充填が利用できる詰め方の自由度がありません。

**不公平の向きはpolicyで反転します。** rho 0.85で、最悪classの平均JCTはgreedy SRPTではtheta軸に沿って366から84へ下がり、ServerFillingでは1.6から26.7へ上がります。EASY backfillは7.1〜13.6でほぼ平らで、最悪class JCTでは21セル中19セルで最良です。

**推定誤差、補正後のmodel。** sigmaが純粋なばらつきとなる中位不偏では、EASY backfillの平均JCTはsigma 0→3で2.107から7.019へ、3.3倍になります。最悪classは7.1から43.9です。同じ範囲でServerFilling-SRPTは18%、greedy SRPTは27%しか動きません。

平均不偏modelではbackfillの曲線が非単調で、sigma 1で9.602に達した後sigma 3で3.887へ**改善**します。これはschedulingではなく算術です。sigma 3では中位推定値が真の大きさの`exp(-4.5) = 0.011`となり、77%のjobがほぼ瞬時に見えます。head-of-lineの予約時刻が現在時刻へ潰れ、EASY backfillは「入るものは何でも動かす」policyへ退化します。小job中心のmixではその退化が偶然有利に働きます。

## 何が変わったか

EP-0001の主張3つを改訂します。

| EP-0001の主張 | 改訂 |
|---|---|
| 小job中心のmixではgreedy SRPTが優位 | 需要分布が全クラスタjobを含まない場合に限る。含む場合はServerFilling-SRPTが平均・最悪classの両指標で上回る |
| size推定誤差はほとんど効かない | 予約型policyについては誤り。EASY backfillは純粋なばらつきで3.3倍悪化する。鈍いのは優先度型のほう |
| 大gang比率が上がると順位が逆転する | 向きが逆。逆転は等質な側にあり、greedy SRPTに有利 |

本研究はEP-0001が宣言したUNKNOWNを2つ閉じ、EP-0001自身が挙げた反証条件の1つを実際に満たしました。補正した中位不偏error modelは、同じ範囲内で推定誤差についての推論を反転させました。

## 何が失敗したか

封印した10本のうち5本が外れました。

| 予測 | 判定基準 | 結果 |
|---|---|---|
| Q1 | theta 0.4と0.8の間に交点がある | **外れ。** 同条件での交点は存在しない。rho 0.85でgreedy SRPTは一度も安定しない |
| Q2 | 交点は負荷で1格子以内しか動かない | **外れ。** rho 0.7でしか定義されない |
| Q3 | 比はthetaで単調減少する | **外れ。** rho 0.85で比較可能セルが0個。空虚 |
| Q4 | greedy SRPTはtheta 0.8以下で安定 | **外れ。** theta 0.4から1つのclassが飢餓 |
| Q5 | EASY backfillは一度も不安定にならない | 支持。21/21が安定、最悪flow balance 0.984 |
| Q6 | FCFSはtheta 0.4で安定、1.0以上で不安定 | 支持。ただし0.4での平均JCTはbackfillの38倍 |
| Q7 | EASY backfillは一度も最良でない | 平均JCTでのみ支持。最悪class JCTでは21セル中19セルで最良 |
| Q8 | 中位不偏ならbackfillのJCTはsigmaで単調 | 支持 |
| Q9 | sigma 3でもgreedy SRPTがbackfillに勝つ | **外れ。** greedy SRPTがclass飢餓のため対比を保留 |
| Q10 | sigma 3でbackfillは中位不偏のほうが悪い | 支持。7.019 対 3.887 |

Q1からQ4は同一の原因で外れました。封印した枠組みが「両policyがどこかで安定し、順位を入れ替える」ことを前提にしていたためです。実際にはそうなりません。この枠組みはEP-0001の結果を一般化しすぎたものでした。

**3つの計測器が失敗し、うち1つは再発でした。**

| 判定器 | 壊れ方 | 検出 |
|---|---|---|
| 完了率が閾値未満 | 有限系は到着が止まれば必ずdrainするので決して発火しない | EP-0001 |
| 利用率が提供負荷を下回る | 安定系の長い過渡でも発火する。EP-0001で無効と記録したにもかかわらず、E2の解析script内で復活していた | EP-0002 |
| class別flow balanceの**水準** | horizon依存。FCFSのtheta 0.4は30k jobで0.80、120kで0.95に上がり、平均JCTは3分の1下がる（安定）。theta 2.0ではより高い0.87なのに平均JCTが3.22倍になる（発散） | EP-0002 |

較正に耐えたのはflow balanceの**class間spread**だけでした。飢餓classは0.4付近に座り、他のすべてのclassは1.00に座る。この符号はhorizon不変で、同時に飢餓class自身のJCTはhorizonに線形に伸びます。水準の判定は2 horizonでの再走に委ねます。

**開示。** 判定器は結果を見た後に変更しています。PRED-002は両セルが安定であることを条件としましたが、安定の判定式自体を固定していませんでした。実行時点の判定器では4/10、補正後は5/10で、Q1・Q2・Q3・Q9の採点はどちらを使うかに依存します。この4本は証拠としての重みを下げます。両方の採点は`results/E2E3_grading.json`の`pass`と`pass_asrun`に保存しています。再発を防ぐため、PRED-003では判定器をsealed fileの中に書き込みました。

## 証拠境界

**支持されること:** このsimulator、mix族、負荷格子、seedの下で、policyの**安定性**（順位だけでなく）が需要mixに依存すること。greedy SRPTが低mix領域全体で全クラスタclassを飢餓させること。集約平均がその飢餓を隠すこと。EP-0001の推定誤差の結論がnoiseのparameterisationに依存すること。

**支持されないこと:** production clusterについての主張、普遍的な閾値、非指数service時間での結果、公平性の許容判断、実trace。本研究ではpreemption costは全体を通じて0です。

## UNKNOWN

- sigma 3を超える領域の挙動。
- mix依存の交点がpreemption cost非ゼロでも残るか。
- 重尾service時間で逆転線が残るか。
- theta 2.0・rho 0.85のgreedy SRPTは裁定不能。4倍horizonで1.46倍成長し、安定と発散の帯の間にある。
- 実traceでの検証。最優先の未解決項目。

## 反証条件

- 独立のsimulatorが同じparameterで安定/飢餓/過負荷の標識を再現しない。
- より長い実行で、飢餓classのJCTがhorizonとともに伸びなくなる。
- 3つ目のhorizonが、現在安定と標識されたセルを過負荷側へ動かす。
- EASY backfill以外の予約型policyが中位不偏errorに鈍いと判明する。その場合、推定誤差の改訂は予約という機構ではなく1実装に限られる。

## 再現

### artifactと採点の簡易確認

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-phase
```

### 完全な再走

```bash
cd reproduction/gpu-scheduling-phase
python calib/c06_flow_balance.py
python run_e2e3.py
python adjudicate.py
python analyze_e2e3.py
```

先に計測器を較正してください。`c06`が失敗するなら、packageのどの判定も信頼できません。`adjudicate.py`は`analyze_e2e3.py`より前に実行する必要があります。後者は裁定されていないセルを安定として扱うことを拒否します。

## 証拠 / Artifacts

- [公開再現package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-phase)
- [封印済みPRED-002](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-002.json)
- [E2/E3の採点、実行時点の判定器も保存](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E2E3_grading.json)
- [59セルの2 horizon裁定](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/adjudication.json)
- [計測器の較正](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/calib/c06_flow_balance.py)

## 外部監査

- 独立再現: 0
- 失敗した再現: 0
- 確認されたbug: 0
- 未解決の批判: 0

## 次の実験

飢餓の2つの候補原因を分離します。原因はneed分布の**support**がクラスタ全体サイズを含むことか、それとも平均gang sizeか。それが[[ja/research/gpu-scheduling-starvation-mechanism/index|EP-0003]]で、平均gang sizeを固定してsupportだけを動かします。
