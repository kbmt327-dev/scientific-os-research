---
research_id: KRYPTOS-K4-EP-0188
title: K4の前提記録を監査し、確定と未判定を分ける
date: '2026-10-11'
lang: ja
domain: Kryptos K4
type: Finding
status: 記録の算術・行数に不一致が残り、探索結果は有限族の記録に限られる
evidence_level: 集計記録の整合性確認。候補探索の再実行ではない
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: EP-0188からEP-0194の集計記録と公開用数値projection
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 前提台帳、分類集計、記録済み有限探索の内部整合性。K4の復号ではない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0188
source_episode_sha256: b10d035bd88c2c8f8fd86191f75ac71664f600e10b376df3ec8bf891326f80e2
publication:
  status: publishable
tags:
- kryptos-k4
- audit
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-premise-audit/" hreflang="en">English</a></p>

## 何を調べたか

K4を扱った複数の記録について、前提台帳の集計、分類数、有限探索の報告値が互いに一致するかを監査した。これは解読候補を探す再実験ではなく、既存記録の集計監査である。

## なぜ重要か

探索結果の範囲を読むには、対象件数や記録値が整合している必要がある。不一致を残したまま明示すれば、限定的な負の結果を未検証の一般論へ広げずに済む。

## 方法

EP-0188〜EP-0194の数値集計だけを公開用projectionに移し、分類数、行数、記録された乗数、UNKNOWN件数を照合した。元の候補探索、平文の確認、nullの再生成は行っていない。公開用データには文字列や個別候補を含めない。

## 結果

| 記録 | source recordの数値 |
|---|---|
| EP-0188 | 台帳100行、前提20件。14行の二重分類で平均Jaccard 0.80 |
| EP-0189 | 62行、救済グループ6件、閾値7 |
| EP-0190 | 5つの報告対象グループで完全一致0件 |
| EP-0191 | 分類行72に対し参照要約は73。乗数172501に対し表示規則からの再計算は173101 |
| EP-0192 | 記録された有限6グループすべてで完全一致0件。T6は1,898,208設定、最良一致8文字 |
| EP-0194 | 1サブファミリーがUNKNOWN |

EP-0191の乗数差は600で、公開集計でも修正せず残した。

## 現在わかっていること

台帳の集計には少なくとも行数と乗数の不一致がある。EP-0190の5グループとEP-0192の6グループでは、source recordは指定された有限族の完全一致を報告していない。EP-0194には未判定が残る。

## 図で見る

| 確認軸 | 記録された値 | 読み方 |
|---|---:|---|
| 前提台帳 | 100行 / 20件 | 集計対象の規模 |
| EP-0191の行数 | 72 / 73 | 内部不一致 |
| EP-0191の乗数 | 172501 / 173101 | 差600 |
| EP-0192 | 6群中0件 | 記録された有限族のみ |

## この研究が示すこと

- 監査対象の記録には集計上の不一致がある。
- EP-0190とEP-0192の報告は、記述された有限族に対する結果として読める。
- 不一致とUNKNOWNを隠さず提示する必要がある。

## この研究が示さないこと

K4全体が解けないこと、特定方式全般が不可能であること、あるいは記録済み探索が独立に再現されたことは示さない。完全一致0件をK4の一般的な性質へ広げない。

## 何が変わったか

数値の集計監査を公開し、72対73行と172501対173101の差を明示した。平文や候補情報を公開せずに、記録結果の範囲を追えるようにした。

## 何が失敗したか

元記録どうしの一致は得られなかった。EP-0194の1項目はUNKNOWNのままであり、ここでは解消していない。

## 証拠の範囲

このノートはsource recordの集計値と、公開projectionの軽量チェックに基づく。暗号探索、null再生成、独立replicationは実施していない。新しい平文0、外部独立replication 0。

## まだ分からないこと

行数差の原因、乗数のどちらが後続計算に使われたか、UNKNOWN項目が追加の証拠で判定可能かは、この集計からは分からない。

## この結論が崩れるとき

元記録の根拠を再確認し、72対73および乗数の差が誤った転記や計算によるものと確定すれば、対応する監査所見を更新する。有限族の結果も、条件や実装の誤りが見つかれば再評価が必要になる。

## 自分で確かめる

公開パッケージのディレクトリで python -B verify_premise_audit.py を実行すると、集計値と差分だけを検算する。これは探索を回さない作者側チェックである。

## 証拠とデータ

公開パッケージ（reproduction/kryptos-k4-premise-audit）には集計JSONと検算コードがある。候補文字列、暗号文、平文は含めない。

## 外部からの検証

この監査と探索記録の独立replicationは0件。査読も受けていない。

## 次の実験

元の台帳と後続要約を行単位で再照合し、差異の由来を記録する。その照合が終わるまでは、該当する数値を確定値として統合しない。

## 出典

- K4公開情報：[CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- source record: KRYPTOS-K4/EP-0188、EP-0189、EP-0190、EP-0191、EP-0192、EP-0194