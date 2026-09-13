---
title: 証拠レベル
description: 証拠classがclaim scopeをどう制限するか。
lang: ja
aliases: [/ja/methodology/evidence-levels/]
---

証拠ラベルはtopicの重要性ではなく、実際に何を検査したかを表します。

| Class | 支持すること | それだけでは支持しないこと |
|---|---|---|
| 合成simulation | 指定model・parameter・実装での挙動 | 実世界での有効性、外的妥当性 |
| 合成blind benchmark | 開示済み仮説族内のhidden instance同定 | 未知の仮説空間の発見 |
| Contract validation | schema、参照、guard、negative control | 数値の正しさ、予測性能 |
| Design / power simulation | 明示した仮定下のprotocolと感度 | 実行可能性、倫理承認、観測効果、最終sample size |
| 独立再現 | 独立した個人・groupによる再現 | 再現条件外での一般的妥当性 |

証拠レベルは将来拡張できます。既存noteは公開時のラベルを保持します。
