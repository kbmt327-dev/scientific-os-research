---
title: Research
description: Research areas, what each currently claims, and what kind of evidence backs it.
lang: en
aliases: [/research/index]
---

<p class="site-lede">Grouped by research area. Each entry says what can be claimed right now and what kind of evidence supports it. <a href="/ja/research/" hreflang="ja">日本語</a></p>

Notes are grouped by what they contribute, not by how confident they sound. A **Finding** reports an observed result, a **Method** defines a research interface, and a **Protocol** freezes a future test before confirmatory data exists.

## GPU cluster scheduling

**Question:** under what conditions does size-based scheduling — run the shortest job first — break?

**Current claim:** the breaking mechanism is real inside synthetic simulation. A single job that needs the entire cluster is enough: size priority combined with greedy packing leaves it waiting indefinitely. But measuring two public traces showed no such job in any pool actually in production. The quantity to watch is the largest job as a fraction of pool capacity; the safe boundary is 0.75 and the worst measured ratio is 0.59. The harm is a several-fold delay, not starvation.

**[Read the current claim (EP-0004) →](/en/research/gpu-scheduling-real-traces/)**

<details class="series-history" id="gpu-scheduling-program">
<summary>The four studies that led here</summary>

<div class="revision-chain vertical" aria-label="How the GPU scheduling claim changed">
  <a href="/en/research/gpu-scheduling/"><b>EP-0001 · synthetic</b><span>Estimation error and restart cost reverse which scheduler wins. Two claims were later made conditional.</span></a>
  <a href="/en/research/gpu-scheduling-phase-diagram/"><b>EP-0002 · synthetic</b><span>A good average hides a job class that never finishes; three stability detectors failed.</span></a>
  <a href="/en/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003 · mechanism</b><span>A mean-matched control isolated the cause — but the practical rule stated here was later withdrawn.</span></a>
  <a class="current" href="/en/research/gpu-scheduling-real-traces/"><b>EP-0004 · trace measurement + synthetic · current</b><span>No measured pool met the condition; degradation is continuous, with a provisional 0.75 boundary in the model.</span></a>
</div>

Read backward from EP-0004 when you want the claim history. This is the published revision sequence; it does not imply that every internal update is published.

</details>

## Queueing system identification

**Question:** given a queueing world whose mechanism is hidden, how much of that mechanism can external records alone recover?

**Current claim:** inside a disclosed family of candidate mechanisms, one hidden instance was identified correctly — all five structural components matched the withheld truth. This tests selection from given options, not discovery from an unknown hypothesis space.

**[Read this study →](/en/research/simulation-worlds/)** — Finding

## Human movement model interfaces

**Question:** before measured human motion reaches a model, can coordinate mix-ups, target leakage, and false external validation be blocked by explicit contracts and dataset boundaries?

**Current state:** the contract stops seven deliberately broken variants, and the first dataset gate is now fixed. Carter is split into 30 development, 10 validation, and 10 test participants; OpenCap laboratory data is reserved for external validation; Knee Grand Challenge is reserved for internal-load stress testing. B3D is only a source-adapter format, and Nimble is not mandatory. No model has been fitted and no holdout has been read.

**[Read the current dataset decision (EP-0005) →](/en/research/human-model-dataset-portfolio/)** — Dataset

Earlier method: **[the fail-closed interface contract (EP-0004) →](/en/research/human-model/)**

## Badminton biomechanics

**Question:** in the smash, can the effect of short preparation time be separated from the effect of backward centre of mass?

**Current state:** design and power sensitivity only. **No observations yet.** Detecting the interaction needs far more participants than the main effects, so the sample size is undecided. Instrument feasibility and ethics are unresolved, so the protocol is not sealed and data collection is not authorized.

**[Read this protocol →](/en/research/badminton-biomechanics/)** — Protocol

---

Future records may include Replication, Negative Result, Dataset, and Benchmark without changing existing research identities.
