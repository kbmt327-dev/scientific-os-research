---
title: 研究を再現する
description: 各noteの正確な公開reproduction packageから始める。
lang: ja
---

各noteの**再現**sectionから始めてください。public commit、環境、command、input、output digest、公開手順との差分を記録します。全projectの最短検査は次です。

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick all
```

Quick checkはartifactと小さな決定論的経路を検査します。simulation全体のrerunや独立実験の代わりではありません。
