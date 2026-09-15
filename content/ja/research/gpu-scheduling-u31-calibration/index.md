---
research_id: GPU-SCHED-EP-0017
title: 独立した較正でも、容量を決める二つの判定器は一致しなかった
date: 2026-09-16
lang: ja
domain: GPU Cluster Scheduling
type: Negative Result
status: 局所不一致・容量と閾値は未確定
evidence_level: 合成モデルの事前固定gridによる局所較正
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model-calibration
  source: 事前固定control 2点と独立grid、balanced/fcfsの16 simulation。公開再現物は集計値の検算まで
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 自作MSJ合成モデルのbalanced需要・FCFS・64サーバ・20k/40k窓・seed 111/222に限る局所比較
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0017
source_episode_sha256: 5fed9bdcc75af4d353f8bdc34180b6bda087b9fe1ca016208e58a413daa2a213
publication:
  status: publishable
tags: [negative-result, gpu-scheduling, capacity, calibration, japanese]
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>容量判定器を使う前に、その閾値を疑う</span><a href="/en/research/gpu-scheduling-u31-calibration/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Negative Result</span><span>合成モデルの局所較正</span><span>容量 UNKNOWN</span><span>査読なし</span><span>外部再現 0</span></div>

## 現在わかっていること

**alpha=0.5を使った容量境界と、別に較正したactive backlogの成長判定は、独立gridのrho=0.85で一致しませんでした。** alphaは0.762で成長側、backlog scoreは0.0385で事前閾値0.1187より低い側です。最初の局所不一致で停止したため、予定したrho=1.0は測っていません。

これは「alphaが間違い」「backlogが正しい」という結果ではありません。低負荷0.4と過負荷1.2の2点で作った中点閾値が、遷移域には粗すぎる可能性があります。**容量の値、alpha=0.5の物理的な意味、実クラスタへの移植はUNKNOWN**です。

[[ja/research/gpu-scheduling-one-job/index|EP-0013]]までの公開履歴の後、低頻度の直接測定を行い、飽和状態のthroughputを容量と呼ぶ計測には打ち切りと「全ジョブを同時に与える」欠陥があると分かりました。開放到着の二分法に移した既存結果も、alpha閾値を独立較正する前の記録です。直前の局所監査では別のbacklog信号との不一致を見つけましたが、runnerが封印した停止点を越えて12 runを続けました。今回のrunnerは最初の不一致で止まりました。これらの内部研究記録を丸ごと公開するものではありません。

## 何を調べたか

完了ジョブの平均応答時間から作るalphaと、到着窓内の未完了ジョブ数から作るbacklog scoreは、結果を見て選んだ境界点ではないgridでも同じラベルを出すか。

## なぜ重要か

二分法の数字は判定器の閾値に依存します。判定器が較正されていないのに、その数字を「検証済み容量」として使うと、測定法の不確かさを容量の確かさにすり替えてしまいます。

## 方法

自作の64サーバMSJ合成モデルでbalanced需要とFCFSを固定しました。20,000/40,000ジョブの2窓、seed 111/222を使い、低負荷rho=0.4と過負荷rho=1.2を先に実行しました。長い窓の各seedで、到着中のbacklogの最後と最初のdecile平均との差を40,000到着で割り、2 seed平均をscoreにしました。control scoreが事前の分離条件を満たすときだけ、その中点を閾値とします。alphaは2窓の平均応答時間の対数比で、比較線0.5は従来値のままです。

独立gridはrho=0.7、0.85、1.0の順に事前固定しました。各cellの4 run後、欠測・実行停止・最初の非曖昧な不一致で直ちに止める契約です。以前の保存境界点とseedは使っていません。ただし、この設計は以前の失敗を見てから作ったもので、外部独立再現や前向き容量予測ではありません。

## 結果

| 役割 | rho | alpha | backlog score | alpha / backlogのラベル |
|---|---:|---:|---:|---|
| 低負荷control | 0.40 | −0.0590 | −0.000004 | 較正に使用 |
| 過負荷control | 1.20 | 0.9267 | 0.237447 | 較正に使用 |
| 独立grid | 0.70 | −0.2291 | 0.000003 | 非成長 / 非成長 |
| 独立grid | 0.85 | 0.7622 | 0.038523 | **成長 / 非成長** |

control中点は0.118722でした。rho=0.85で**R2 局所不一致**となり、16/最大20 simulationで停止。全16 runの必要な値は有限で、backlog capによるabort、time limit、right censoringはありませんでした。これは観測条件の確認であり、安定性の証明ではありません。

## 何が変わったか

開放到着の容量値を検証済みとして採用する判断を保留し、次の仕事を「遷移域のcontrolとholdout gridを分け、閾値を再較正する」ことへ変えました。以前の数値は、合成モデルと未監査の判定線に条件付けられた履歴として残します。

## 何が失敗したか

二つの判定器は独立gridの1点で一致しませんでした。極端な負荷2点から取った中点が遷移域の物理的な閾値になる、という保証はありません。以前の停止条件逸脱は今回は繰り返していません。

## 証拠の範囲

**示すこと：** 固定した合成モデル・窓・seed・FCFSの局所比較で、alpha=0.5と今回のcontrol由来backlog閾値はrho=0.85を異なる側へ分類した。runnerは最初の不一致で停止した。

**示さないこと：** alphaの物理的反証、backlog判定器の妥当性、二分法の容量値、他policyや需要mix、実クラスタでの性能、独立再現。公開パッケージは集計値と停止分岐の算術検算だけで、raw runとsimulation sourceは含みません。

## まだ分からないこと

- 遷移域の安定・不安定controlを、有限窓backlog以外の根拠で確かめられるか。
- 閾値0.3/0.5/0.7、より長い窓、別seed、打ち切りを扱うdrift統計で不一致が残るか。
- 開放到着の容量値をどの証拠等級で扱えるか。

## この結論が崩れるとき

公開集計のcontrol中点やラベルが算術的に再計算できない場合、このNoteの局所不一致の記述は撤回します。新しく封印した遷移域較正で両統計が一致しても、今回の固定契約で観測した不一致そのものは消さず、その射程を狭めます。

## 自分で確かめる

公開集計の閾値と停止分岐だけを確認できます。**simulationの再実行ではありません。**

```bash
python reproduction/gpu-scheduling-u31/verify_summary.py
```

## 証拠とデータ

- [限定した公開集計と検算コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31)
- 内部EpisodeのSHA-256：`5fed9bdcc75af4d353f8bdc34180b6bda087b9fe1ca016208e58a413daa2a213`。これは原記録との対応を示し、科学的妥当性の封印ではありません。

## 外部からの検証

独立再現0、査読0。公開後の外部監査結果はまだありません。

## 次の実験

結果を見る前に、遷移域controlの独立根拠、calibrationとholdout grid、40k/80kを含む窓とseed、alpha=0.3/0.5/0.7、打ち切り時のdrift欠測、最初の不一致で止まるrunnerを新契約へ固定します。controlが分離しない場合はUNKNOWNで止めます。既存18セル全体の独立rerunと実クラスタでの検証は別のgateです。
