---
title: Research Noteの読み方
description: 結論から証拠境界、UNKNOWN、再現経路まで、必要な深さで読む。
lang: ja
aliases: [/ja/methodology/]
---

<p class="language-switch"><span aria-current="page">日本語</span> · <a href="/scientific-os-research/en/how-to-read/" hreflang="en">English</a></p>

すべてのsectionを読む必要はありません。自分の問いに答えられた深さで止められます。

<div class="depth-guide">
  <section><b>01 · 発見する</b><h3>何が分かったのか</h3><p>冒頭の主張、status、key figureを読む。約15秒。</p></section>
  <section><b>02 · 理解する</b><h3>なぜ、どの条件で起きるのか</h3><p>重要性、機構、「示すこと／示さないこと」を読む。</p></section>
  <section><b>03 · 検証する</b><h3>その証拠で考えは変わるか</h3><p>予測、失敗、証拠境界、artifact、`UNKNOWN`を調べる。</p></section>
  <section><b>04 · 再現する</b><h3>同じ観測を得られるか</h3><p>公開packageを実行し、commit、環境、差分を報告する。</p></section>
</div>

## Labelを文字どおり読む

- **Evidence class**は何を観測したかであり、topicの重要度ではありません。[[evidence-levels|証拠レベルの比較]]。
- **UNKNOWN**は証拠の境界と、次に必要な識別的観測です。空欄ではありません。
- **Editorial review**は公開表現とprivacy境界の確認です。scientific／domain-expert／peer reviewを意味しません。
- **Quick reproduction**は公開artifactと限定経路の検査です。独立再現ではありません。

## 訂正は前向きに読む

日付付きnoteは記録として残します。後続証拠が主張を狭めた場合、旧noteから目立つ形で前方linkを置き、research indexで現在のnoteを示します。失敗予測、analysis defect、降格した主張も消しません。

## 深く読む

- [[prediction-sealing|予測のseal]]
- [[falsification|反証と反例]]
- [[replication|再現と独立再現の違い]]
