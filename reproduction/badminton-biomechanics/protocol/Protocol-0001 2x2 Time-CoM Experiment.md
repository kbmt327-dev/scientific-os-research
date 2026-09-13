---
kind: iaa-preregistration-draft
schema_version: iaa-preregistration-draft.v1
protocol_id: IAA-2X2-TIME-COM-001
version: 0.1.0-draft
as_of: 2026-09-13
status: draft-not-sealed
prospective_data_authorized: false
---

# IAA 2×2実験 事前登録ドラフト

## 判定

`assigned preparation time × assigned backward-CoM state`を独立操作する被験者内2×2として、座標、主要window、除外、主解析モデル、失敗時の扱いを固定した。ただし、機器・倫理・feasibility pilotが未確認で、操作水準、最小重要効果、最終標本数を根拠付きで決められない。したがって本書は**実験開始を許可しないdraft**であり、`PENDING-2X2-EP-0007`はsealしない。

## Research question / hypotheses

同じ熟練者内で、準備時間の割付と後方CoM状態の割付を分離したとき、接触直前のracket-head velocityがどう変わるかを問う。

- H1：short timeの割付はprimary racket velocity projectionを低下させる（`βT < 0`）。
- H2：high backward-stateの割付はprimary outcomeを低下させる（`βB < 0`）。
- H6：high backward-stateでもbrakingと近位―遠位再編成が成立する範囲では、`βB > 0`または条件依存の`βTB ≠ 0`と対応するmechanistic outcomeが現れる。`βB = 0`だけではH6支持としない。

## Design

- 対象：badminton overhead smashを安全に行える成人熟練者。具体的な競技水準、年齢、安全除外は倫理申請前に固定する。
- 因子T：assigned preparation time = `long` / `short`。
- 因子B：assigned backward-CoM state = `low` / `high`。
- 4セルを各participant内で実施し、block内順序をbalanced randomizationする。割付順列とseedを取得前に保存する。
- 練習・pilotとconfirmatory sampleを分離する。操作量、閾値、最小重要効果の決定に使ったparticipantはconfirmatory解析へ含めない。
- 疲労尺度とblock/orderを記録し、休息規則を倫理・feasibility後に固定する。

### 割付と実現値を分ける

primary causal contrastは割付T/Bを用いる。actual cue-to-contact timeやactual CoM velocityでtrialをlong/short、low/highへ付け替えない。実現値はmanipulation checkとsecondary dose-responseに用いる。

現時点で未固定の操作パラメータは次の通り。

| item | status | seal前の決定方法 |
|---|---|---|
| `T_long`, `T_short` | UNKNOWN | confirmatory sampleと分離したfeasibility pilotで成功率・安全性・実現時間差を評価し、絶対msまたはparticipant別校正式を固定する。 |
| backward-state cue / start geometry | UNKNOWN | time操作を変えずにCoM `−X`成分を変えられる方法をpilotで選ぶ。単なるspeed tokenは採用しない。 |
| manipulation margin `ΔT_min`, `ΔV_min` | UNKNOWN | 計測誤差とpilot分布から、結果を見ずに固定する。 |

## Coordinate and event contract

### Ground coordinate system

- 原点：calibrated court plane上の標準初期位置。
- `+X`：標準初期位置からnet中央へ向かう水平軸。
- `+Z`：鉛直上向き。
- `+Y = +Z × +X`：右手系を完成する水平軸。
- 「後方CoM」は`v_CoM · (−X)`で表す。speed magnitudeの符号なし減算はしない。
- impact target unit vector `u_target`は、calibrated nominal impact centerから固定target centerへ向かうGCSベクトルとしてsession前に保存する。actual hit pointを使ってtrialごとに軸を回転しない。

### Synchronized events

- `cue_onset`：視聴覚cueを出す装置のTTL rising edgeを同期収録した時刻。動画上の見た目開始で置換しない。
- `GC`：合成鉛直GRFが20 Nを超え、その状態が10 ms以上持続する最初の時点。force plate miss時はGC/GRF outcomeだけ欠測とする。
- `contact = 0 ms`：1000 fps以上の同期high-speed videoでshuttleとstringbedの最初の接触が見えるframe。impact sensorがある場合もvideoとの対応を保存する。
- 上記同期、sampling rate、calibrationが実現できない場合はprotocolをsealせず、別versionとして変更理由を残す。

## Outcomes and windows

### Primary outcome

`Y = mean[v_racket_head(t) · u_target]` over `t ∈ [−10, −2] ms` relative to contact、単位m/s。接触後のshuttle interactionを含めず、固定target方向へのground-frame vector projectionを評価する。

Secondary outcomeは同windowの3軸成分、velocity norm、stringbed-normal projection、contact height、actual shuttle feed位置・速度とする。primaryを見た後に最も大きい成分へ差し替えない。

### Manipulation checks

- time：`actual preparation time = contact − cue_onset`。割付longとshortのparticipant内差と95% CIを報告する。
- backward state：`mean[v_CoM · (−X)]` over `[GC−20, GC+20] ms`。割付highとlowのparticipant内差と95% CIを報告する。
- manipulation margin未達でも実現値で再分類しない。ITTを報告した上で「操作失敗」と判定し、H1/H2/H6の因果識別はしない。

### Mechanistic outcomes

- braking impulse：`∫ max(F_GRF · +X, 0) dt / body mass` from GC to the earlier of first `v_CoM·X ≥ 0` crossing or contact。
- early phase：`[GC, GC + 0.5×(contact−GC))`。
- late phase：`[GC + 0.5×(contact−GC), contact−10 ms)`。
- early pelvis–thorax separation / trunk kinematics、late shoulder internal-rotation qdd、late elbow-extension qdd、target別IAA INTを候補として保存する。
- shoulder JFPはsecondary counter-path。JTPはEP-0003/0004で妥当性確認したstructured/recomputed definitionだけを使い、raw JTPを使わない。
- mediatorはmechanistic consistencyの評価であり、割付→mediator→outcomeの因果媒介は追加仮定なしに主張しない。

## Exclusion and missingness contract

### Trial-level

- 割付後のattemptはすべてtrial ledgerへ残す。
- contactが確認できない、primary window内にracket-head markerの欠測が1 frameでもある、同期/calibrationが失敗したtrialはprimary outcomeを欠測とする。primary windowを補間しない。
- force plate missはGRF/GC由来outcomeだけを欠測とし、contact基準primary outcomeが有効ならtrial全体を除外しない。
- shuttle feedが事前固定許容域外、誤ったstroke、機器故障は理由コードをblind QCで付ける。許容域はpilot後・confirmatory data取得前に固定する。
- 低い/高いracket speed、予測と逆の値、外れ値で除外しない。winsorizeしない。

### Participant-level

- primary ITT-like analysisは、4セルすべてに1件以上の有効primary outcomeがあるparticipantを含め、元の割付で解析する。
- 4セルが揃わないparticipantはcell contrastを同定できないためprimary contrastから除くが、理由・件数・割付後脱落を報告する。
- 各セル4件以上の有効trialがあるcomplete-dose subsetをsensitivity analysisとする。primaryと入れ替えない。
- 欠測値の単純補完はしない。セル別欠測率と理由を報告する。

## Confirmatory statistical model

codingは`T = −0.5 (long), +0.5 (short)`、`B = −0.5 (low), +0.5 (high)`とする。

`Y_trial = β0 + βT T + βB B + βTB(T×B) + βorder trial_order + βblock block + u0_participant + uT_participant T + uB_participant B + uTB_participant(T×B) + ε`

- participant random interceptとT/B/T×B random slopesを含むtrial-level linear mixed modelをprimaryとする。
- 収束・特異性への固定fallback順は、(1) correlated T/B/T×B slopes、(2) correlationを0にしたT/B/T×B slopes、(3) correlationを0にしたT/B slopes、(4) random intercept only。最初に収束し非特異となるmodelを主判定に使い、fallbackの発生を報告する。
- `βT`, `βB`, `βTB`をco-primary contrastとし、両側familywise α=.05のHolm補正を行う。方向仮説はestimateと95% CIで評価する。
- 分布診断、participant-level orthogonal contrast、actual time/CoMを用いるdose-response、cell-balanced complete-dose解析はsensitivity。primaryを都合のよい結果へ差し替えない。
- H6はnon-significantなH2から採択しない。正方向効果またはinteractionに加え、事前定義mechanistic outcomeとの整合を必要とする。

## Power sensitivity, not final sample size

再現scriptは `analysis/ep0008_power_simulation.py`、要約結果は `evidence/EP-0008-power-sensitivity.json`。

現段階ではtrial residual SD=1、participant random-slope SD=0.20、balanced complete cells、3 co-primary testにBonferroni α=.0167という仮定で10,000回simulateした。effectはtrial residual SD単位である。

| contrast | trials/cell | effect | grid内でpower≥.80となる最小N |
|---|---:|---:|---:|
| main effect | 6 | 0.30 SD | 30 |
| main effect | 6 | 0.40 SD | 20 |
| interaction | 6 | 0.30 SD | `>48`（N=48で0.4988） |
| interaction | 6 | 0.40 SD | `>48`（N=48で0.7905） |
| interaction | 6 | 0.50 SD | 36 |

これは標本数決定ではない。pilotまたは独立データからrandom-slope SD、技術欠測率、最小重要効果を固定し、interactionを検出対象にするかを決めた後に再simulateし、attritionを加えて最終Nをsealする。

## Seal blockers / execution gate

以下が全部埋まるまで取得を開始しない。

1. 倫理・安全・熟練度基準と機器利用可能性。
2. `T_long/T_short`、backward-state操作、`ΔT_min/ΔV_min`。
3. sampling/synchronization実機検証、shuttle feed許容域、休息規則。
4. 最小重要効果、random-slope SD、欠測率、interaction優先度、最終N。
5. 計測・QC・randomization codeのversion/hashと解析環境。
6. confirmatory data cutoff、公開/保存方針、sealed prediction hash。

どれかが未確認なら、結果を取得してから穴を埋めず、pilotまたはprotocol revisionへ戻る。
