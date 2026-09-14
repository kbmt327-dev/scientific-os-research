---
title: 研究
description: 分野ごとの研究テーマ、現在の結論、証拠の種類。
lang: ja
---

<p class="site-lede">分野ごとにまとめています。各項目には、いま何が言えているかと、証拠の種類を添えました。<a href="/en/research/" hreflang="en">English</a></p>

分類は自信の強さではなく、研究が何を足すかで決めています。**Finding** は観測から得た結果、**Method** は研究を進めるための仕組み、**Protocol** は確証データを取る前に固定した将来の検査です。

<!-- GENERATED: research-current:START -->
## GPUクラスタのスケジューリング

**テーマ：** 短いジョブを先に通す「サイズ優先」のスケジューリングは、どの条件で壊れるか。

**現在地：** 現在見る量は、**最大ジョブがプール容量に占める割合 × 同時実行ジョブ数 × 大ジョブの頻度**の3つです。256サーバ、rho 0.85の合成モデルでは、同時10本なら比率0.92（頻度0.002）／0.72（頻度0.02）、同時30本なら0.73／0.66が目安です。頻度を落とすと、希少な大ジョブには保守側、頻繁な大ジョブには危険側の数字になります。

自分のクラスタでは完了率ではなく、平均待ち時間が観測窓とともに伸びるかを見ます。窓を2倍にして平均が1.4倍以上になるなら、そのクラスは発散しています。実クラスタについて言える範囲は極端に狭く、Phillyの11仮想クラスタ中10個には容量の4分の1を超えるジョブがなく、唯一の例外でも容量の半分超は19,100本中1本でした。

**証拠の境界：** 実際の到着列を使ったスケジューラ比較ではなく、外部からの独立再現もまだありません。

**[現在のResearch Note（EP-0013）→](/ja/research/gpu-scheduling-one-job/)** — Finding

[研究の現在地と更新履歴を見る →](/ja/programs/gpu-scheduling/)

## 待ち行列のシステム同定

**テーマ：** 中身を隠した待ち行列の世界に対し、外から見える記録だけでどこまで仕組みを言い当てられるか。

**現在地：** あらかじめ開示された候補集合の中で、隠された1事例を正しく同定でき、5つの構造要素すべてが保留した正解と一致しました。

**証拠の境界：** これは与えられた選択肢から選ぶ検査であり、未知の仮説空間からの発見でも、実システムへの適用検証でもありません。

**[現在のResearch Note（EP-0001）→](/ja/research/simulation-worlds/)** — Finding

[研究の現在地と更新履歴を見る →](/ja/programs/queueing-system-identification/)

## 人体運動モデルのデータ接続

**テーマ：** 計測した人体の動きをmodelへ渡す前に、座標の取り違え、答えの漏れ、見かけだけの外部検証を止められるか。

**現在地：** 接続契約は意図的に壊した7つの変種を拒否します。dataset gateはCarterをdevelopment 30人、validation 10人、test 10人に分け、OpenCapの実験室dataを外部検証、Knee Grand Challengeを内部荷重のstress testに限定しました。B3Dはsource adapter形式で、内部表現はNumPy配列と明示的な意味情報です。Nimbleは必須ではありません。

**証拠の境界：** model fittingもholdout読込もまだ実施していません。

**[現在のResearch Note（EP-0005）→](/ja/research/human-model-dataset-portfolio/)** — Dataset

[研究の現在地と更新履歴を見る →](/ja/programs/human-model-interface/)

## バドミントンのバイオメカニクス

**テーマ：** スマッシュで、準備時間の短さと後方重心の効果を切り分けられるか。

**現在地：** 公開済みなのは実験計画と検出力の感度解析までで、観測はまだありません。交互作用の検出には主効果より多い参加者が必要と分かり、人数を決められていません。

**証拠の境界：** 機器の実行可能性と倫理審査が未解決なので、計画は封印されておらず、データ取得も承認されていません。

**[現在のResearch Note（EP-0008）→](/ja/research/badminton-biomechanics/)** — Protocol

[研究の現在地と更新履歴を見る →](/ja/programs/badminton-biomechanics/)

[公開中のResearch Noteを時系列で見る →](/ja/research-notes/)
<!-- GENERATED: research-current:END -->

---

将来は、既存の研究の識別子を変えないまま、Replication、Negative Result、Dataset、Benchmarkを追加できます。
