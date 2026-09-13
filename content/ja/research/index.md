---
title: 研究
description: 証拠境界を明示したFinding、Method、Protocol。
lang: ja
---

<p class="language-switch"><span aria-current="page">日本語</span> · <a href="/scientific-os-research/en/research/" hreflang="en">English</a></p>

Research Noteは、自信の強さではなく、研究に何を追加するかで分類します。**Finding**は観測結果、**Method**は研究interface、**Protocol**は確証dataより前に固定する将来の検査です。

## Findings

### GPU scheduling研究系列

4本は一つの公開更新履歴です。最新の公開境界はEP-0004から、主張の変化を調べるときは逆向きに読んでください。この公開系列は、内部更新がすべて公開済みであることを意味しません。

<div class="revision-chain vertical" id="gpu-scheduling-program">
  <a href="/scientific-os-research/ja/research/gpu-scheduling/"><b>EP-0001 · SYNTHETIC</b><span>workload mixとpreemption frictionでscheduler順位が反転。二つの主張は後続で限定。</span></a>
  <a href="/scientific-os-research/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002 · SYNTHETIC</b><span>phase diagramがnoise軸の交絡と三つのstability detector失敗を露出。</span></a>
  <a href="/scientific-os-research/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003 · MECHANISM</b><span>mean-matched controlでwhole-pool supportを分離。ただし実務ruleは後に降格。</span></a>
  <a class="current" href="/scientific-os-research/ja/research/gpu-scheduling-real-traces/"><b>EP-0004 · TRACE MEASUREMENT + SYNTHETIC · LATEST PUBLIC</b><span>測定poolを満たすjobはゼロ。劣化は連続で、model上の暫定境界は0.75。</span></a>
</div>

### ほかのFinding

- **[[ja/research/simulation-worlds/index|batched arrivalとheterogeneous serverのblind identification]]** — 開示済み合成仮説族内の5つの構造的一致。open-world discoveryではありません。

## Methods

- **[[ja/research/human-model/index|Human Model Contract v0.2]]** — fail-closedなdata/model contractの検証。数値の正しさの証拠ではありません。

## Protocols

- **[[ja/research/badminton-biomechanics/index|準備時間 × 後方CoMの2×2 protocol]]** — 前向き設計とpower sensitivity。未sealでdata collection未承認です。

将来は既存のresearch identityを変えず、Replication、Negative Result、Dataset、Benchmarkを追加できます。
