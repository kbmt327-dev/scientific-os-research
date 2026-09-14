---
title: 人体運動モデルのデータ接続
description: 計測データと人体運動モデルの接続条件を機械検査する研究の概要です。
lang: ja
---

人体運動の計測値をモデルへ渡すとき、座標系や単位、時刻の対応を取り違えると、計算が動いても意味の違う答えになります。この研究では、その接続条件を人の注意ではなく機械検査で守る方法を扱います。

## 問い

どの入力契約、dataset境界、失敗条件を固定すれば、座標の取り違え、対象変数の漏えい、見かけだけの外部検証をmodel実行前に止められるのか。

## 現在の公開範囲

正しい接続bundleは九つの検査群を通過し、意図的に壊した七つのvariantはすべて拒否されました。次のdataset gateも固定しました。Carter 30人で開発し、validationとtestに各10人を未使用で残し、OpenCapの実験室dataは外部検証だけ、Knee Grand Challengeは内部荷重のstress testだけに使います。B3Dはsource adapter形式で、内部表現はNumPy配列と明示的な意味情報です。NimbleはHuman Modelの必須依存ではありません。model fittingもholdoutの読込もまだ実施していません。

**[[ja/research/human-model-dataset-portfolio/index|最新のResearch Noteを読む →]]**
