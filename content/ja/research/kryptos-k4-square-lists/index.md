---
research_id: KRYPTOS-K4-EP-0200
title: 正方形リストを使う有限族の記録結果と検証範囲
date: '2026-10-11'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 記録済みの指定有限族で一致0件。公開verifyは入力件数とnull集計のみ確認
evidence_level: source recordの数値集計とinventory・ヒストグラムの軽量検算
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 公開入力inventoryとEP-0193 T1、EP-0199、EP-0200、EP-0201、EP-0205、EP-0228の数値記録
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 記録された有限リスト族と各EPで定義した不一致基準。候補走査の公開再実行ではない
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0200
source_episode_sha256: 49b73d5dc511003122bff8d840cda15b61563d25fb07c0c9eecdf3c840a08305
publication:
  status: publishable
tags:
- kryptos-k4
- square-lists
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-square-lists/" hreflang="en">English</a></p>

## 何を調べたか

正方形リスト、ペアリング、区間開始点、Bifid設定を組み合わせた有限族の記録結果を、公開可能な集計値として整理した。対象はEP-0193 T1、EP-0199、EP-0200、EP-0201、EP-0205、EP-0228である。

## なぜ重要か

これらの探索では候補族やnullの大きさが異なる。記録結果と公開パッケージで実際に再検算した項目を分ければ、小さなnull標本や未完成のパッケージを過大評価せずに済む。

## 方法

source recordから最小不一致数、登録pass数、null標本数とヒストグラムを数値だけ抽出した。公開verifyは場所・seed・square・pairing・mode・start・settingの件数、および記録済みヒストグラムの合計と割合を確認する。候補走査やnull生成は実行しない。

## 結果

| 記録 | source recordの結果 | null標本 |
|---|---|---|
| EP-0193 T1 | exact pass 0。公開走査なし | — |
| EP-0199 | 最小不一致13、exact pass 0 | n=200、観測値以下0.975 |
| EP-0200 | 最小不一致11、exact pass 0 | n=10、観測値以下0.10 |
| EP-0201 | 合同最小不一致8、h≤2 pass 0 | n=2,000、観測値以下0.189 |
| EP-0205 | 最小不一致14、exact pass 0 | n=20、観測値以下1.00 |
| EP-0228 | 48,608,736設定、最小不一致15、pass 0 | n=20、観測値以下1.00、記録P=1.00 |

割合は各source recordの有限null標本で観測値以下となった割合であり、独立したp値ではない。特にn=10やn=20の比較は精度が限られる。

## 現在わかっていること

source recordは指定された有限族で登録pass 0を報告している。null標本の分布はEPごとに異なり、いくつかは小さい。公開verifyはこの探索結果を再現していない。

## 図で見る

| 公開入力inventory | 件数 |
|---|---:|
| 場所 | 146 |
| keyword seed | 40 |
| unique square | 185 |
| pairing | 48 |
| 隣接mode | 3 |
| segment start | 6 |
| Bifid setting | 2,765 |

## この研究が示すこと

- source recordに残る有限探索の結果とnull集計を数値として確認できる。
- 指定記録には完全一致または登録passがない。
- 公開パッケージの軽量検算はinventoryと集計算術に限られる。

## この研究が示さないこと

正方形暗号全般、未登録のリストや規則、K4全体についての否定ではない。nullの割合は独立replicationや一般的な有意性を示さない。EP-0193 T1を含め候補走査は再実行していない。

## 何が変わったか

途中だったパッケージに記録結果の数値projectionと、inventory・nullヒストグラムの軽量検算を追加した。source recordの陰性をUNKNOWNへ置き換えず、公開検証の未実施を別に示した。

## 何が失敗したか

候補走査とnull再生成は公開パッケージにない。EP-0193 T1は結果記録だけで、対応する公開スキャンも未完成である。

## 証拠の範囲

source recordの記録済み数値、公開入力の件数、ヒストグラムの内部算術に限る。新しい平文0、独立replication 0。null shareは記述的な有限標本の割合である。

## まだ分からないこと

別実装で候補走査やnull生成を再現した場合に記録値が維持されるかは未確認である。小さなnull標本はその分布を詳しく推定するには足りない。

## この結論が崩れるとき

同じ登録規則の再走査で一致候補が見つかるか、記録した最小値・null集計・設定数に誤りが判明すれば該当結果を更新する。

## 自分で確かめる

パッケージのディレクトリで python -B verify_square_lists.py を実行する。inventory数と5つのヒストグラムの合計・割合を検算するだけで、候補探索は回さない。

## 証拠とデータ

公開パッケージ（reproduction/kryptos-k4-square-lists）にinventory、数値結果、軽量verifyを置く。解読文字列や盤面は含めない。

## 外部からの検証

独立replicationは0件。専門家レビューと査読は受けていない。

## 次の実験

登録条件のまま独立実装で小さい範囲を検算し、必要な場合だけ全走査とnullの再実行を計画する。nullが小さい記録から一般的な確率を主張しない。

## 出典

- K4公開情報：[CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- source record: KRYPTOS-K4/EP-0193 T1、EP-0199、EP-0200、EP-0201、EP-0205、EP-0228