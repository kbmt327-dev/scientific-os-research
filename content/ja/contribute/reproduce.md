---
title: 研究を再現する
description: 各記事の公開再現パッケージから始める。
lang: ja
---

各記事の**「自分で確かめる」**の節から始めてください。公開コミット、実行環境、コマンド、入力、出力のハッシュ、そして公開手順との差分を記録します。

全プロジェクトの最短の検査は次です。

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick all
```

この簡易確認は、公開データと小さな決定論的経路だけを検査します。シミュレーション全体の再実行や、独立した実験の代わりにはなりません。
