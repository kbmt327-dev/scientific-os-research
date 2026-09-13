---
title: Open Research Lab
description: 研究の現在の主張から、証拠・限界・再現まで辿れる公開研究インターフェース。
lang: ja
---

<p class="language-switch"><span aria-current="page">日本語</span> · <a href="/scientific-os-research/en/" hreflang="en">English</a></p>

<div class="gateway-kicker">SCIENTIFIC OS · PUBLIC RESEARCH INTERFACE</div>

> 短時間で意味がつかめ、主張が壊れるところまで深く検証できる研究公開。

Scientific OS が生み出した研究の一部を、人と機械が**理解・検証・再現・反証・再利用**できる形で公開します。結論は独立再現されるまで暫定です。

<div class="depth-rail" aria-label="読む深さ"><span><b>01</b> 発見する</span><span><b>02</b> 理解する</span><span><b>03</b> 検証する</span><span><b>04</b> 再現する</span></div>

## 注目の研究

<div class="feature-finding">
  <p class="eyebrow">GPU SCHEDULING · 4本で更新された研究系列</p>
  <h3>良い平均値の裏で、希少なjob classは待ち続け得る。ただし実trace検証で、その警告が届く範囲は狭まった。</h3>
  <p>合成simulationは、greedyなsize-based schedulingのstarvation機構を分離しました。その後のpublic trace測定では、必要な前提が測定pool内に存在しませんでした。現在の結論は、比率による境界と数倍の遅延であり、実trace上のstarvationではありません。</p>
  <p class="feature-actions"><a href="/scientific-os-research/ja/research/gpu-scheduling-real-traces/">最新の公開結果を読む →</a> <a href="/scientific-os-research/ja/research/#gpu-scheduling-program">4本の更新履歴を見る</a></p>
</div>

<div class="revision-chain" aria-label="GPU schedulingの主張がどう変わったか">
  <a href="/scientific-os-research/ja/research/gpu-scheduling/"><b>EP-0001</b><span>mixとfrictionで順位が反転</span></a>
  <a href="/scientific-os-research/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>noiseの交絡と検出器の失敗</span></a>
  <a href="/scientific-os-research/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>whole-pool supportが機構を分離</span></a>
  <a class="current" href="/scientific-os-research/ja/research/gpu-scheduling-real-traces/"><b>EP-0004 · LATEST PUBLIC</b><span>実traceが実務的な射程を降格</span></a>
</div>

<p class="public-scope">公開境界：このindexが現在扱う公開系列はEP-0004までです。すべての内部研究更新をmirrorしているとは主張しません。</p>

## ほかの研究

<div class="research-grid">
  <a href="/scientific-os-research/ja/research/simulation-worlds/"><span>Finding</span><b>Blind system identification</b><small>観測はhidden queueing mechanismをどこまで識別できるか。</small></a>
  <a href="/scientific-os-research/ja/research/human-model/"><span>Method</span><b>Human Model Contract v0.2</b><small>human dataとmodelの間をfail-closedに接続する境界。</small></a>
  <a href="/scientific-os-research/ja/research/badminton-biomechanics/"><span>Protocol</span><b>Badminton biomechanics 2×2</b><small>前向き実験設計。未sealで、data collectionは未承認。</small></a>
</div>

## このLabの読み方

各Research Noteは、結論と射程を分けます。何が変わり、何が失敗し、何が`UNKNOWN`で、どこから再現できるかを残します。まず **[[ja/how-to-read/index|Research Noteの読み方]]** を、必要なら背後の [[ja/about/scientific-os|Scientific OSの研究loop]] を見てください。

## 証拠で参加する

次に価値がある出来事はStarではなく、独立rerun、再現失敗、反例、より良い観測です。**[[ja/contribute/index|再現・反証・拡張・共同研究の入口へ →]]**

<p class="quiet-meta"><a href="/scientific-os-research/ja/about/open-research-lab/#誰がなぜ作っているか">このLabを作っている人について</a>。各noteに明記がない限り、editorial review済み、scientific／domain-expert／peer review未実施です。</p>
