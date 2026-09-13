---
id: HUMAN-MODEL-EP-0004-JA
title: Human Model Contract v0.2
date: 2026-09-13
lang: ja
translation_of: HUMAN-MODEL-EP-0004
domain: Scientific Human Model
type: Method
status: Contract検証済み、adapterはblocked
evidence_level: Contract validation
peer_reviewed: false
independent_replications: 0
evidence:
  class: contract-validation
  source: JSON Schema bundle、文書間validator、7つのnegative control
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: 公開v0.2 contract bundleのschemaと参照整合性
source_episode: HUMAN-MODEL/EP-0004
source_episode_sha256: 260f10d6b70d75420e9aa57945ca24cd7d0335eaed053cf5a0fe9f77008f90f8
publication:
  status: publishable
tags: [method, human-model, contract, fail-closed, japanese]
---

<p class="language-switch">English: <a href="/scientific-os-research/research/human-model/">Original Research Note</a></p>

<div class="evidence-strip"><span>Method</span><span>Contract validation</span><span>Adapter blocked</span><span>予測性能の証拠ではない</span><span>外部再現 0</span></div>

## 要約

Contract v0.2は、coordinate-system identity、adapter参照、source不整合、target leakageを、`ObservationSpec`、`AdapterSpec`、`ValidationCase`にまたがる機械検査可能な要件へ変換します。正しいbundleは9種類の検査に合格し、意図的に無効化した7 variantはすべて拒否されました。以前のv0.1 artifactは変更せず、過去のevidence hashを維持しました。これはfail-closedなcontract挙動だけを示し、数値変換の正しさやHuman Modelの予測性能を示しません。

## 研究質問

公開biomechanics sampleで既知の不一致を、未解決mapping、coordinate ambiguity、参照欠落、target leakageが文章上の注意だけでなく機械的にValidationCaseをblockする形で表現できるか。

## なぜ重要か

Human Model pipelineはcoordinate system、model basis、processing pass、outcome由来inputを混在させたまま動作しているように見えることがあります。数値性能を解釈する前に、contractがその境界違反を明示すべきです。

## 方法

公開bundleは次を定義します。

- **ObservationSpec:** coordinate space、channel、processing pass、source consistency check、構造化warning。
- **AdapterSpec:** source observation、target model、coordinate／frame参照、mapping status、review済みwarning。
- **ValidationCase:** observation／model／adapterの正確な参照、input、target、leakage rule、readiness state。

ValidatorはJSON Schema 2020-12適合、identifier一意性、文書間参照、adapter target、source warning、leakage rule、readiness gateを検査します。

## 結果

基準bundleは9つのcheck groupに合格しました。次の7つのnegative controlはすべて拒否されました。

1. `coordinate_spaces`の欠落。
2. 未知のchannel coordinate参照。
3. `adapter_ref`の欠落。
4. AdapterとValidationCaseのobservation不一致。
5. source-inconsistency warningの削除。
6. 未解決mappingがあるのに`ready`とする。
7. dynamics／force由来のtarget channelをinputへ入れる。

## 何が変わったか

v0.1 fileを上書きする方法から、versioned v0.2 schemaとexampleへ移行しました。これにより過去artifact hashを保ち、意味上の変更を監査できます。

## 何が失敗したか

source sampleではactive degree of freedom 37とembedded coordinate 39の不一致が見つかりました。Contractは不整合を記録できますが、どちらが正しいか決められません。そのためpublic exampleは曖昧さをadapter claimへ変換せずblockedのままです。

## 証拠境界

**支持されること：** 同梱したpublic schema、example、文書間validator、negative controlが、宣言したcontract-level ruleを強制する。

**支持されないこと：** Nimble/OpenSim実行、B3Dの数値frame変換、37から18 DOF mappingの正しさ、biomechanics prediction、科学的価値、model promotion。

## UNKNOWN

- 同じB3D内容をofficial Nimble APIと調査済みprotobuf pathで一貫して読めるか。
- active-DOF数とembedded-coordinate数の正しい解決。
- frame／basis変換の数値妥当性。
- racket stateを欠かさずtarget modelへ有効mappingを作れるか。

## 反証条件

- 下記negative controlのいずれかを受理する。
- `ready`なValidationCaseが未解決adapterを参照できる。
- target由来dynamics channelを拒否せずinputへ入れられる。
- Official API調査がpublic source metadataまたはcoordinate assumptionと矛盾する。

## 再現

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick human
```

公開bundleはprivacy sanitize済みです。内部exampleにあったmachine-local documentation pathをrepository-relative参照へ変換しました。Validatorと科学的境界は変えておらず、public artifact hashは別に記録しています。

## 証拠 / Artifacts

- [Schema、example、validator、evidence](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/human-model-contract)
- 内部source Episode digest：`260f10d6b70d75420e9aa57945ca24cd7d0335eaed053cf5a0fe9f77008f90f8`

## 外部監査

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決critique：0

## 次の実験

同一のpublic B3D artifactをofficial Linux/Nimble環境で読み、header、trial、pass、frame、missing-GRF metadataを現在の抽出と比較します。必要mappingが一つでも未解決ならadapterはblockedのままにします。
