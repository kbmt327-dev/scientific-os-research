---
title: 人体運動モデルのデータ接続
description: 計測データと人体運動モデルの接続条件を機械検査する研究の概要です。
lang: ja
---

人体運動の計測値をモデルへ渡すとき、座標系や単位、時刻の対応を取り違えると、計算が動いても意味の違う答えになります。この研究では、その接続条件を人の注意ではなく機械検査で守る方法を扱います。

## 問い

どの入力契約、dataset境界、失敗条件を固定すれば、座標の取り違え、対象変数の漏えい、見かけだけの外部検証をmodel実行前に止められるのか。

<!-- GENERATED: program-current:START -->
## 現在の公開結論

接続契約は意図的に壊した7つの変種を拒否します。dataset gateはCarterをdevelopment 30人、validation 10人、test 10人に分け、OpenCapの実験室dataを外部検証、Knee Grand Challengeを内部荷重のstress testに限定しました。B3Dはsource adapter形式で、内部表現はNumPy配列と明示的な意味情報です。Nimbleは必須ではありません。

**証拠の境界：** model fittingもholdout読込もまだ実施していません。

**[現在のResearch Note（EP-0005）を読む →](/ja/research/human-model-dataset-portfolio/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## 公開中のResearch Note

1. [[ja/research/human-model/index|EP-0004 — 人体データとモデルの接続を、曖昧なまま先へ進ませない検査の仕組み]]
2. **[[ja/research/human-model-dataset-portfolio/index|EP-0005 — 開発・外部検証・内部荷重の検査を混ぜないためのデータセット構成]]（最新）**
<!-- GENERATED: program-history:END -->
