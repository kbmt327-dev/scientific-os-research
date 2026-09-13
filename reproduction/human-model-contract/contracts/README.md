---
kind: human-model-contract
status: candidate
version: v0.2
as_of: 2026-09-13
---

# Human Model Commons：最小Contract v0.2

## 結論

EP-0002では最小単位を `HumanModelSpec`、`ObservationSpec`、`ValidationCase` の三つに固定した。実B3Dを調べたEP-0003で、37-DOF sourceと18-DOF IAAの写像を暗黙に置けない反例が出たため、変換自体を記録する `AdapterSpec` を追加した。目的は異なるsolverを同一化することではなく、**どの意味・単位・frame・processing pass・権利・評価境界を変換したか**を失わないことである。

EP-0004のv0.2では、実B3Dで見つかった反例を機械検証へ昇格した。`ObservationSpec.coordinate_spaces`、`ValidationCase.adapter_ref`、構造化したsource consistency check/warningを必須化し、`AdapterSpec`がsource coordinate space・target frame・warning処理を明示する。旧v0.1 filesはEP-0002/0003のhash付き証拠として変更しない。

| Contract | 責務 | 入れてはいけないもの |
|---|---|---|
| `HumanModelSpec` | model scope、component、frame、dynamics I/O、provenance、unsupported claim | 実測値そのもの、根拠のない解剖label |
| `ObservationSpec` | dataset/trial/timebase、channel、measured/derived区分、processing、rights | model validityの主張 |
| `ValidationCase` | context of use、input/target、split、baseline、metric、leakage、acceptance | 実行前の成功判定 |
| `AdapterSpec` | source→target mapping、transform、未写像field、invariant、fail-closed条件 | 配列位置だけの暗黙変換 |

## IAAで見つかった設計上の反例

IAAの18成分を単に `shape=[18,T]` として渡すと意味が壊れる。1–3はGCSでのlower-trunk COM並進加速度、4–18は各joint/tool basisにおける相対角速度微分である。一方、出力4–18はGCS torque成分で、historical plot labelを解剖学的軸と断定できない。したがってv0.1は、入出力を `block_id + source_indices + quantity_kind + unit + frame_id + axes + semantic_status` で表す。

## AddBiomechanicsで見つかったleakage境界

force / joint torqueを予測するtestで、force plateを使用したdynamics passを入力にするとtarget情報が混入する。`ObservationSpec.channels[].leakage_tags` と `processing_passes[].uses_target_measurement` を必須化し、`ValidationCase.leakage_rules` が入力をfail closedにする。

## v0.2のfail-closed gate

- channelが存在しないsource coordinate spaceを参照したらrejectする。
- ValidationCase、AdapterSpec、ObservationSpec、HumanModelSpecの参照が一致しなければrejectする。
- source内部の不一致に対応するstructured warningが無ければrejectする。
- adapterがwarningをreviewしていなければrejectする。
- unresolved mappingを残したadapterでValidationCaseを`ready`にできない。
- target由来のdynamics channelをinputへ入れたらrejectする。

実行：`python -B "tests/validate_contract_v0_2.py"`

## v0.2で意図的に扱わないもの

- muscle path、activation、controller objectiveの詳細schema
- solver固有XMLやB3D binaryそのもの
- anatomy ontologyの統一
- medical / injury prediction claim
- model promotion

これらは最初の実sampleでlossが観測された場合にのみ拡張する。

## Files

- `human-model-spec.schema.json`
- `observation-spec.schema.json`
- `validation-case.schema.json`
- `adapter-spec.schema.json`
- `observation-spec.v0.2.schema.json`
- `validation-case.v0.2.schema.json`
- `adapter-spec.v0.2.schema.json`
- `../examples/iaa-limited-human-model-spec.example.json`
- `../examples/addbiomechanics-observation-spec.definition.json`
- `../examples/addbiomechanics-b3d-adapter-validation-case.definition.json`
- `../tests/VC-0001 AddBiomechanics B3D Adapter Test.md`
- `../tests/validate_contract_v0_2.py`
