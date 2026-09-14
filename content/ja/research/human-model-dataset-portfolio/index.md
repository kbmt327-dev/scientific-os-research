---
research_id: HUMAN-MODEL-EP-0005
lang: ja
title: 開発・外部検証・内部荷重の検査を混ぜないためのデータセット構成
date: 2026-09-14
domain: Scientific Human Model
type: Dataset
status: データセットの役割とparticipant splitを固定、model結果はまだない
evidence_level: 一次資料に基づくdataset設計
peer_reviewed: false
independent_replications: 0
evidence:
  class: source-backed-dataset-design
  source: datasetの一次資料、50人の決定論的split、archive indexの限定調査
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: 最初のlocomotion benchmarkにおけるdatasetの役割、leakage境界、固定済みparticipant split
source_episode: HUMAN-MODEL/EP-0005
source_episode_sha256: d4e7e6e2a2cc0a98f789e396483b5d8c043fd8f6d8a2d2fd1bc6744b63d5f6d3
publication:
  status: publishable
tags: [dataset, human-model, biomechanics, validation, preregistration, japanese]
---

<p class="research-area"><b>人体運動モデルのデータ接続</b><span>開発用のデータと、モデルを疑うための検査を分ける</span><a href="/en/research/human-model-dataset-portfolio/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Dataset</span><span>一次資料に基づく設計</span><span>model fitting未実施</span><span>holdout未使用</span><span>外部再現 0</span></div>

[[ja/research/human-model/index|曖昧な入力を止める接続契約]]の続きです。

## データセットの結論

一つのdatasetを「一般人体モデルの正解」とは扱いません。最初のvertical sliceでは、役割を三つに分けます。

| 役割 | Dataset | 検査できること |
|---|---|---|
| 開発と内部holdout | [Carter et al. 2024](https://doi.org/10.15125/BATH-01341)。[AddBiomechanics](https://addbiomechanics.org/download_data.html)から配布 | motion captureとforce plateを伴う、参加者・速度・勾配をまたぐlocomotion |
| 外部検証 | [OpenCap laboratory validation](https://doi.org/10.1371/journal.pcbi.1011462) | 別に収集されたraw sourceのwalking、squat、sit-to-stand、drop jumpの実験室計測へ移せるか |
| 内部荷重のstress test | [Knee Grand Challenge](https://doi.org/10.1002/jor.22023) | 将来のmodelがinstrumented implantで測った膝接触力との比較に耐えるか |

[AMASS](https://arxiv.org/abs/1904.03278)はkinematicsの範囲確認だけに使い、force validationには使いません。[HuMoD](https://www.informatik.tu-darmstadt.de/sim/forschung_sim/datensaetze_sim/humod_sim/index.en.jsp)はEMGの診断用であり、一般化性能のbenchmarkにはしません。

## 何を調べたか

最初のlocomotion benchmarkで、開発用のdataとmodelを疑うためのdataを密かに使い回さないためには、どの公開datasetとholdout境界を選ぶべきか。

## なぜ重要か

同じraw sourceを別の処理で作り直し、開発と検証に分けても、収集条件や処理上の仮定は共通です。それを外部検証と呼ばないため、容量の大きな取得、特徴量設計、model fittingより先にdatasetの役割を固定する必要があります。

## 方法

datasetの一次資料から、参加者、動作、計測modalities、license、targetがどれほど直接計測に近いかを比較しました。最初のquantity of interestは、force plateで実測した三次元ground reaction forceを体重で正規化した系列とcontact stateに限定しました。関節torqueはinverse dynamicsとmodel parameterに依存するため、最初のground truthにはしていません。

Carterの50 participant IDはsource表にあるsex labelごとに分け、各label内でage、participant IDの順に並べました。決定論的なmodulo-five ruleでdevelopment 30、validation 10、test 10へ割り当てました。各partitionの二つのsource label数は同じで、upstream testのP010はtestに残しています。

B3Dはsourceを読むadapter形式の一つに限定します。内部表現はNumPy配列と、座標、単位、frame、processing、missingness、provenanceの明示的metadataです。したがってNimble APIはHuman Modelの定義や学習の必須依存ではありません。公式readerとの一致確認はadapterの任意の再現性検査として残します。

## 結果

development、validation、testのIDを公開のmachine-readable manifestに固定しました。元のparticipant表はコピーせず、URL、size、SHA-256で参照します。既に取得済みだった1 MiBのZIP64 central-directory tailから、空でないCarter B3Dが610件あり、development participantのWith_Arm候補ではP008_split2が最小と確認しました。このB3D本体はまだ取得していません。

## 何が変わったか

次の必須gateをNimbleとprotobufのreader一致確認から、dataset選定とleakage防止へ変更しました。Subject40は接続契約の反例として残し、prediction benchmarkには使いません。開発内ではparticipant holdoutを使い、外部検証には別raw sourceを要求します。

## 何が失敗したか

model fittingもholdout評価も実施していないため、このEpisodeでmodelやdataset処理の失敗はありません。Nimble parityを次の必須gateにする案は退けました。検査できるのはreader間の一致であり、Human Modelの科学的な有用性ではないためです。

## 証拠の範囲

**言えること：** 公開sourceを別々の役割へ割り当てたこと、Carter participant splitが決定論的で内部整合していること、取得境界とleakage ruleを機械検査できること。

**言えないこと：** B3Dの数値抽出、trialの利用可能性、入力channelの妥当性、model学習、metric threshold、holdout性能、外部妥当性、内部荷重の正確さ、一般人体モデルの成立。

## まだ分からないこと

- P008_split2に、実測GRFを利用できるframeが十分あるか。
- どのkinematics processing passがforce plateによる最適化から独立しているか。
- 選んだB3D memberの正確なtrial condition、channel shape、座標、単位、missingness。
- 数値threshold、resampling、event定義、最終的なbaseline実装。
- 学習するmodelがheld-out participantで二つの単純baselineを上回るか。

## この結論が崩れるとき

- validationまたはtest participantがnormalization、fitting、feature選択、threshold選択へ影響する。
- force plateで最適化したdynamics-pass featureを、同じtrialのforce target予測に使う。
- 同じraw sourceの再処理を独立した外部検証として数える。
- missingnessや性能を見た後にparticipantの割り当てを変える。
- 複雑なmodelが、封印したparticipant単位metricでdevelopment平均波形とregularized linear modelを上回らない。

## 自分で確かめる

~~~bash
python scripts/reproduce.py --quick human-dataset
~~~

公開manifest、split出力、件数、hash、未実施境界を検査します。元datasetはdownloadせず、計測値を独立再現するものでもありません。

## 証拠とデータ

- [Dataset portfolioのmanifestとvalidator](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/human-model-dataset-portfolio)
- [Carterのsource record](https://doi.org/10.15125/BATH-01341)
- 内部の元Episodeのhash：d4e7e6e2a2cc0a98f789e396483b5d8c043fd8f6d8a2d2fd1bc6744b63d5f6d3

## 外部からの検証

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決の批判：0

## 次の実験

P008_split2だけをrange downloadし、protobufとNumPyでtrial condition、timebase、channel shape、processing pass、利用可能なGRFの割合、座標、単位を確認します。限定調査でreader固有の曖昧さが見つからない限り、validation/test participantを読まず、model fittingをせず、Nimbleも導入しません。
