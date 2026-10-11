---
research_id: KRYPTOS-K4-EP-0196
title: 固定した行リストをcribで調べた有限範囲
date: '2026-10-11'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 公開された8リストの指定検査は記録と一致し、12リスト全体の記録上の下限は不一致3
evidence_level: 3 EPの公開部分再実行と、残りのsource record集計
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 12固定リストの集計記録と公開8リストの入力
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: EP-0196、EP-0197、EP-0208の公開8リスト検査と登録12リストの記録上のcover bound
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0196
source_episode_sha256: f2ff8d5e0fadb8370a84a2cf01f20da2408e9304ea2cc6b34277cf462917b85f
publication:
  status: publishable
tags:
- kryptos-k4
- fixed-row-lists
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-fixed-row-lists/" hreflang="en">English</a></p>

## 何を調べたか

固定規則で作られた行リストの有限族を、公開K4のcribに照らした記録を整理した。登録された一覧は12、合計662行で、そのうち8一覧・336行が公開パッケージに含まれる。

## なぜ重要か

事前に固定した一覧なら、候補選択後に都合のよい列を選ぶ余地を減らせる。公開できる範囲を限定して示すことで、再計算した部分と記録だけの部分を区別できる。

## 方法

公開データの8一覧に対して、EP-0196、EP-0197、EP-0208のcrib検査と一覧サイズから導く計数を実行する。12一覧全体についての選択自由なcover bound、EP-0198、非公開の4一覧、null、植え込み対照、IC解析はsource recordの記録として扱い、このパッケージでは再計算しない。

## 結果

| 範囲 | 結果 |
|---|---|
| 登録リスト | 12一覧、662行 |
| 公開データ | 8一覧、336行 |
| EP-0196、0197、0208 | 公開8一覧の検査を実行し、記録と照合 |
| 全12一覧のcover bound | 記録上、最小不一致数は3以上 |
| EP-0198、null、対照、IC解析 | source recordのみ |

この下限は、登録された一覧と規則の範囲内でcribの不一致が2以下にならないという意味に限る。加えてverifyは、EP-0208本文が11とする該当リスト・周期ペア数が、入力サイズからは9になる差も検出した。記録された除外設定数は再計算値と整合するが、本文の数え方は未解決である。

## 現在わかっていること

公開8一覧の指定検査は軽量verifyで再計算できる。全12一覧に関する下限や除外部分の探索は記録値であり、同じ公開チェックの再実行結果ではない。

## 図で見る

| 一覧集合 | 一覧数 | 行数 | 検証状態 |
|---|---:|---:|---|
| 登録全体 | 12 | 662 | source record |
| 公開部分 | 8 | 336 | 3 EPの検査を再実行 |
| cover bound | — | — | 記録上、最小不一致数3以上 |

## この研究が示すこと

- 指定された規則と登録一覧の範囲では、source recordのcover boundは2以下の不一致を除く。
- 公開8一覧に対する3 EPの検査は作者コードで再実行できる。
- 公開検証は登録探索全体を再現していない。

## この研究が示さないこと

K4の解法全般、別の行リスト、別の選択規則について結論しない。隠された一覧やEP-0198、null・対照の記録を、この公開検証が確認したとは扱わない。

## 何が変わったか

公開可能な8一覧だけを入力にした再現パッケージを整え、記録のみの結果を明示した。新しい探索結果や平文は追加していない。

## 何が失敗したか

4一覧とEP-0198の再実行は公開パッケージに含まれない。全12一覧のcover boundはsource recordに依存する。EP-0208の本文値11と入力からの再計算値9にも差が残る。

## 証拠の範囲

公開8一覧、作者コードのcrib検査、記録済み集計が証拠である。null生成と対照は再実行していない。新しい平文0、独立replication 0。

## まだ分からないこと

公開されていない4一覧とEP-0198を独立に再計算した場合に、記録値が維持されるかは未確認である。

## この結論が崩れるとき

公開8一覧の検査でcrib不一致が2以下となる場合、または登録全体を定義する一覧・規則が変わる場合、該当する下限を再評価する。

## 自分で確かめる

パッケージのディレクトリで python -B verify_fixed_row_lists.py を実行する。公開一覧の検査と軽い集計を行う。約10秒の作者側部分再実行であり、独立replicationではない。

## 証拠とデータ

公開パッケージ（reproduction/kryptos-k4-fixed-row-lists）には8一覧、コード、結果集計がある。除外リストの原文は含まれない。

## 外部からの検証

外部独立replicationは0件。査読は受けていない。

## 次の実験

公開可能な形で残る除外部分の集計を独立に検査し、source recordと照合する。新しい方法へ結論を広げない。

## 出典

- K4公開情報：[CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- source record: KRYPTOS-K4/EP-0196、EP-0197、EP-0198、EP-0208