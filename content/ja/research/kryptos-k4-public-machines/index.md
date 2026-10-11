---
research_id: KRYPTOS-K4-EP-0206
title: 公開機械族でのK4一致は有限設定の記録に限る
date: '2026-10-11'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 複数の登録有限族で完全一致0件。全探索とnullはsource recordのみ
evidence_level: 機械実装と小規模部分チェックの公開再実行、および記録済み大規模探索
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開機械モデル、小規模検査、EP-0193からEP-0215の集計記録
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: EP-0193 T2、EP-0203、EP-0206、EP-0207、EP-0209、EP-0215で明記した有限設定
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0206
source_episode_sha256: 91d9dd2ac17c054b8bae47719c13f152edf0fca3f2be151eff67ebd38a287984
publication:
  status: publishable
tags:
- kryptos-k4
- public-machines
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-public-machines/" hreflang="en">English</a></p>

## 何を調べたか

公開仕様で定義した複数のローター機械族について、cribに一致する有限設定が記録されたかを整理した。対象はEP-0193 T2、EP-0203、EP-0206、EP-0207、EP-0209、EP-0215である。

## なぜ重要か

機械の状態数が大きくても、結果は選んだ配線、入口読取り、配置、評価基準の範囲に限られる。登録条件と再実行範囲を分けて示すことで、0件を機械暗号全般の否定に広げずに済む。

## 方法

公開パッケージは機械のテストベクトル、ステッピング類、配線不変条件、入口読取り、小規模な植え込み・K4部分検査、設定数と確率式を確認する。フルCPU/GPU探索、null、EP-0207の確認統計はsource recordのままで、再生成していない。

## 結果

| 記録 | source recordの有限結果 |
|---|---|
| EP-0193 T2 | 111,209,679,360設定、K4 pass 0 |
| EP-0203 | 主設定487,118,136,960、h≤2のK4設定0、null 10本 |
| EP-0206 | 38,167,161,956,352設定、h≤2のK4設定0。より緩いh≤12の集まりは記録 |
| EP-0207 | 事後感度観察は未確認、記録p=0.415 |
| EP-0209 | 61,165,323,648設定、K4 pass 0、記録E=4.35×10⁻⁷ |
| EP-0215 | 733,983,883,776設定、登録pass 0、記録E=0.0331、最小のnull比較P=0.07 |

これらは同じ基準の一つの総合検定ではなく、それぞれの登録条件で得た記録値である。

## 現在わかっていること

いくつかの指定有限族で、source recordは登録された一致基準の通過を報告していない。EP-0206には緩い基準での集まりがあり、EP-0207の事後観察は確認されていない。

## 図で見る

| 検査 | 範囲 | 記録結果 | 公開verify |
|---|---:|---|---|
| EP-0203 | 約4.87×10¹¹設定 | h≤2は0 | 設定数・小規模検査 |
| EP-0206 | 約3.82×10¹³設定 | h≤2は0、h≤12は集まりあり | 部分検査 |
| EP-0209 | 約6.12×10¹⁰設定 | pass 0 | 記録のみ |
| EP-0215 | 約7.34×10¹¹設定 | 登録pass 0 | 記録のみ |

## この研究が示すこと

- 記録された結果は、記載された有限設定と基準に対する陰性である。
- 公開verifyは機械部品と小さな検査の一部を再実行する。
- 全探索やnullの全面再実行は公開verifyの範囲外である。

## この研究が示さないこと

他の配線・機械・crib配置が失敗するとは示さない。K4の解法全体、統計的な有意性、または独立replicationも主張しない。EP-0207の事後観察を確認済みの検出として扱わない。

## 何が変わったか

大規模な記録結果と公開側で確認した小規模な部品検査を別々に記述した。全面再計算したかのような表現を避けられるようにした。

## 何が失敗したか

フル探索、null生成、確認統計はこの公開パッケージで再実行していない。EP-0207の事後感度観察は確認されなかった。

## 証拠の範囲

公開verifyはテストベクトル、機械不変条件、設定数、確率式、小規模スライスを検査する。大規模なCPU/GPU走査、null、確認統計はsource recordに依存する。新しい平文0、独立replication 0。

## まだ分からないこと

未実行の全探索を別実装で再現したときに記録結果が維持されるかは未確認である。指定族の外にある方法の適合性もこの作業からは分からない。

## この結論が崩れるとき

同じ登録条件を満たす完全一致設定が見つかるか、実装・設定数・crib評価の誤りが示されれば、対応する有限族の陰性を更新する。

## 自分で確かめる

パッケージのディレクトリで python -B verify_public_machines.py を実行する。約10秒の部分チェックであり、全探索を回さない。

## 証拠とデータ

公開パッケージ（reproduction/kryptos-k4-public-machines）に検査コードと数値結果を置く。平文や植え込み文字列は含まれない。

## 外部からの検証

独立replicationは0件。専門家レビューと査読も受けていない。

## 次の実験

必要なら登録条件を固定した小さな独立実装で、公開verifyの機械部品と設定数を照合する。未実行の大規模走査へ結論を拡張しない。

## 出典

- K4公開情報：[CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- source record: KRYPTOS-K4/EP-0193 T2、EP-0203、EP-0206、EP-0207、EP-0209、EP-0215