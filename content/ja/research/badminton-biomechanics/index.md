---
id: IAA-EP-0008-JA
title: バドミントンスマッシュの準備時間×後方CoM 2×2 protocol
date: 2026-09-13
lang: ja
translation_of: IAA-EP-0008
domain: IAA / Badminton biomechanics
type: Protocol
status: Draft、未seal、data collection未承認
evidence_level: Design and power simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: protocol-and-power-sensitivity
  source: 公開事前登録draftとMonte Carlo感度analysis
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: 前向きdesignのみ、確証的観測なし
source_episode: IAA/EP-0008
source_episode_sha256: 6c12a0f9f82a62cac5b36509d4901d10cb9ffec458bcd873cb801fe54a5f9308
publication:
  status: publishable
tags: [protocol, biomechanics, badminton, preregistration, japanese]
---

<p class="language-switch">English: <a href="/scientific-os-research/research/badminton-biomechanics/">Original Research Note</a></p>

<div class="evidence-strip"><span>Protocol</span><span>Draft、未seal</span><span>確証dataなし</span><span>power仮定は未較正</span><span>外部再現 0</span></div>

## 要約

このprotocolは、同じ熟練participant内でバドミントンoverhead smashの準備時間と後方center-of-mass状態を独立に割り付ける2×2実験を提案します。確証data取得前にprimary racket-velocity outcome、座標系、同期event、除外、階層model、model fallback順を固定します。Monte Carlo感度analysisでは、明示した仮定下でinteraction effectは同程度のmain effectより大幅に多いparticipantを要しました。機器の実行可能性、倫理、操作水準、経験的分散、最小重要効果、欠測、最終sample sizeは未解決なので、protocolは未sealでdata collectionを承認しません。

## 研究質問

同じ熟練participant内でassigned preparation timeとassigned backward-CoM stateを分離すると、contact前の固定target方向racket-head velocityへどう影響するか。

## なぜ重要か

retrospectiveなswingでは、観測された準備時間、後方移動、skill adaptation、racket outcomeが絡み合います。時間圧とbody-state effectを分け、熟練した再編成が後方状態を補償できるか調べるには独立割付が必要です。

## 競合仮説

- **H1:** 短いassigned preparation timeはprimary velocity projectionを下げる（`beta_T < 0`）。
- **H2:** 高いassigned backward-CoM stateはそれを下げる（`beta_B < 0`）。
- **H6:** braking／reorganizationに成功するregimeでは、高いbackward stateが`beta_B > 0`またはmechanism outcomeと整合する条件依存interactionを生み得る。`beta_B = 0`だけではH6を支持しない。

## 予測

確証予測はsealしていません。Placeholder `PENDING-2X2-EP-0007`はfeasibilityとdesign blockerが解けるまで意図的に未sealです。

## 方法

- participant内2×2：assigned preparation time（`long/short`）× assigned backward-CoM state（`low/high`）。
- primary contrastは達成値でなくassignmentが定義し、観測時間やCoMでtrialを再labelしない。
- Ground axis：`+X`はnet center方向、`+Z`は上、`+Y = +Z cross +X`。backward CoMはvelocityの`-X`射影。
- Primary outcome：contact前`[-10,-2] ms`におけるground-frame racket-head velocityの固定target vector方向平均。
- Cue：同期TTL rising edge。Contact：1000 fps以上で最初に見えるshuttle／stringbed接触。Ground contact：vertical GRFが10 ms以上20 Nを超える最初の時点。
- Primary model：time、backward state、interaction、order、blockをfixed effect、participant interceptとtime／backward／interaction slopeをrandom effectとするtrial-level linear mixed model。
- Co-primary termは両側Holm familywise alpha 0.05。非収束／singularity時は固定simplification順を使う。

Technical missingnessはoutcome別です。Force-plate missはforce-dependent outcomeを無効にしますが、有効なcontact-based racket outcomeまでは除外しません。Primary windowは補間せず、値が低い／予想外という理由で除外しません。

## Power感度

Simulationはresidual SD 1.0、participant random-slope SD 0.20、balanced complete cell、planned Holmの保守的近似としてBonferroni alpha `0.05/3`を仮定します。各cell 6 trialです。

| Contrast | Effect | power >= .80となる最小tested N |
|---|---:|---:|
| Main effect | 0.30 SD | 30 |
| Main effect | 0.40 SD | 20 |
| Interaction | 0.30 SD | >48、N=48でpower 0.4988 |
| Interaction | 0.40 SD | >48、N=48でpower 0.7905 |
| Interaction | 0.50 SD | 36 |

これは感度結果であり、最終sample-size決定ではありません。

## 何が変わったか

- 曖昧だったimpact前方向を、固定target-vector projectionと`[-10,-2] ms` primary windowへ変えました。
- post hoc relabelを防ぐため、assigned factorとachieved manipulation valueを分離しました。
- interaction powerがmain-effect powerと大きく異なるため、単一の固定sample sizeを棄却しました。

## 何が失敗したか

仮定したrandom-slope SDやmanipulation levelを支持するempirical pilotはありません。同期1000-fps video、TTL、force plate、racket markerの利用可能性も未実証です。したがって現時点で実行gateを通らずdraftのままです。

## 証拠境界

**支持されること：** event、座標、除外、model、powerの仮定を外部から確認できる程度にdesignが定義され、公開simulationで感度gridを再現できる。

**支持されないこと：** 実行可能性、倫理承認、観測されたbiomechanics effect、因果解釈、最終sample size、確証研究を開始できる状態。

## UNKNOWN

- 倫理／安全基準と対象skill level。
- 実行可能な`T_long/T_short`とbackward-state manipulation geometry。
- 最小manipulation marginとshuttle-feed tolerance。
- 経験的random-slope variance、technical missingness、attrition、最小重要効果。
- interactionをsample size決定に使うco-primaryとするか。
- 最終code／environment hashとconfirmatory data cutoff。

## 反証条件

- assigned timeが事前登録margin以上にachieved preparation timeを分離しない。
- time assignmentを保ったままassigned backward stateが`v_CoM dot (-X)`を分離しない。
- 同期または較正が固定event／window定義を支えられない。
- pilotの分散・欠測により現在のpower gridが実質的に楽観的と分かる。
- manipulation成功下の新confirmatory sampleで`beta_B < 0`が再現され、H6が弱まる。

## 再現

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick iaa
```

公開仮定下のpower計算を再現します。確証dataが存在しないため、実験を再現するものではありません。

## 証拠 / Artifacts

- [事前登録draft、power script、output](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/badminton-biomechanics)
- 内部source Episode digest：`6c12a0f9f82a62cac5b36509d4901d10cb9ffec458bcd873cb801fe54a5f9308`

## 外部監査

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決critique：0

## 次の実験

confirmatory sampleとは別のfeasibility pilotで同期と直交manipulationを確認し、分散と欠測を推定し、最小重要効果を選び、interactionをco-primaryにするか決めます。その後にだけ最終protocolとsample sizeをsealします。
