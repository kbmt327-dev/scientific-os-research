---
research_id: GPU-SCHED-EP-0007
title: Measured at the real cluster's position, and withdrew an explanation carried for four studies
date: 2026-09-13
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Synthetic simulation with measured inputs
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation-with-measured-inputs
  source: one sealed prediction (PRED-008, 4 of 6) and a 168-run sweep extending concurrency down to the real cluster's position
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 256-server synthetic multiserver-job model, rho 0.85, exponential service, no restart cost. From the real cluster only the measured ratio and concurrency are used as inputs
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0007
source_episode_sha256: b821fb81d95ecfca2fef66f048b85812d98e15ddf39672b666170522b001d27f
publication:
  status: publishable
tags: [finding, scheduling, simulation, retraction]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-real-cluster-position/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation with measured inputs</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

> [!warning] The boundary numbers here were later replaced along with the detector
> The **shape** — lower concurrency permits a higher ratio — survives. The numbers (0.875, a margin of 0.285, a 5.1× harm) cannot be quoted: [[en/research/gpu-scheduling-blind-detector/index|EP-0011]] showed the detector was invalid. Current values are in [[en/research/gpu-scheduling-alpha-boundary/index|EP-0012]] and [[en/research/gpu-scheduling-one-job/index|EP-0013]]. The claim of "reproduction at zero grid steps under a different construction" was narrowed by [[en/research/gpu-scheduling-third-variable/index|EP-0010]] to **within the same background distribution family**.

## Current finding

The previous study ([[en/research/gpu-scheduling-concurrency/index|EP-0006]]) corrected the driver to concurrency, but measured only at 28.5 jobs and above. The most exposed real virtual cluster, 11cb48, runs at a concurrency of 10.2 — **outside the measured range**. The previous study called it safe by extrapolation.

The extrapolation is now a measurement. At a concurrency of 9.8 the safe boundary is 0.875, giving a margin of 0.285 over the measured ratio of 0.59. The direction does not change; the basis does.

This study also **withdraws an explanation it had carried across four studies.**

The withdrawn explanation read: a job requiring the whole pool cannot start unless it reaches rank 1 in the priority order; while it waits its remaining time does not fall, so it never reaches rank 1. This is a **structural trap**, independent of load.

Too strong. The flow of a whole-pool class varies **continuously** with concurrency, from 0.078 to 0.850. At a concurrency of 7.4 it does not starve at all. Whether a job reaches rank 1 is a question of how many competitors there are, not a categorically different condition.

## Key figure

<div class="ratio-figure" aria-label="safe boundary by concurrency with the real cluster marked"><div class="ratio-track"><i style="left:59%"></i><i style="left:87.5%"></i></div><div class="ratio-labels"><span style="left:59%"><b>0.59</b> measured on Philly<br>margin 0.285</span><span style="left:87.5%"><b>0.875</b> boundary at concurrency 9.8</span></div></div>

Real virtual clusters sit on the low-concurrency side, where a single job may take most of the pool and still get through. On the measured curve, the observed ratio of 0.59 falls to the left of the 0.875 boundary.

## What this research shows

- In this synthetic model the safe boundary is a decreasing function of concurrency: 0.875 / 0.875 / 0.8125 / 0.625 / 0.50 / 0.50 at concurrency 7.4 / 9.8 / 14.6 / 28.4 / 54.2 / 98.9.
- The position of the real virtual cluster 11cb48 (concurrency about 10) is on the safe side by measurement rather than extrapolation.
- Starvation of a whole-pool class is not a categorically distinct phenomenon. It is a continuous quantity along the concurrency axis.

## What this research does not show

- The boundary **numbers** come from a detector later shown to be invalid.
- No scheduling policy was run on a real arrival stream. From the real cluster only the measured ratio and concurrency were **fed in as inputs**.
- The "reproduction under a different construction" is within one background distribution family. Cross-family reproduction failed in a later study.

## Why this matters

The phrase "structural trap" sat in published documents across four studies. Qualitatively strong words change what readers do. If something is "structural and independent of load", then reducing load is pointless. In fact load — more precisely, how many jobs run at once — was the whole effect.

**Write a strong word only after sweeping the axis along which it claims no counterexample exists.** Writing "structural" from a single observation was the error.

## Research question

1. What is the safe boundary at the concurrency where real virtual clusters actually sit (about 10)?
2. Is starvation of a whole-pool job genuinely a categorically distinct phenomenon?

## Method

Fix the pool at 256 servers and sweep concurrency from 7.4 to 98.9 by changing the granularity of the background demand. At each point sweep the ratio across seven levels. 168 runs at rho 0.85.

Sealed as PRED-008; the digest is at `predictions/PRED-008.sha256` in the reproduction package, committed while no corresponding result file existed.

The previous study varied pool size while holding the background relatively fixed; this one fixes the pool and coarsens the background. **Two different constructions reaching the same concurrency should give the same boundary** — that check is built in.

## Results

**The boundary is a decreasing function of concurrency.**

| Concurrency | 7.4 | 9.8 | 14.6 | 28.4 | 54.2 | 98.9 |
|---|---|---|---|---|---|---|
| Safe boundary | 0.875 | 0.875 | 0.8125 | 0.625 | 0.50 | 0.50 |

**The two constructions agree.** EP-0006 (vary the pool, hold the background relative) and EP-0007 (fix the pool, coarsen the background) both give 0.625 near a concurrency of 28.5 — zero grid steps apart.

**Whole-pool starvation is continuous.**

| Concurrency | 98.9 | 54.2 | 28.4 | 14.6 | 9.8 | 7.4 |
|---|---|---|---|---|---|---|
| Flow of the whole-pool class | 0.078 | 0.178 | 0.265 | 0.519 | 0.693 | 0.850 |

From 0.078 to 0.850 with no step. At low concurrency even a whole-pool job gets through.

**Harm at the real cluster's position.** At ratio 0.625 and concurrency 9.8 the large class runs **5.1×** slower than the background class. Both earlier estimates — 7.4× and 16.3× — were measured on the wrong axis.

## What changed

- The explanation "whole-pool starvation is a structural trap independent of load" was **withdrawn** and replaced by a continuous quantity along the concurrency axis. It had been published across four studies.
- The real cluster's position was promoted from extrapolation to measurement.
- The harm estimate was revised for the second time as the axis was corrected: 7.4× (EP-0004) → 16.3× (EP-0005) → **5.1×** (here).

## What failed

**PRED-008 scored 4 of 6.** The informative failure is W5.

W5 predicted that a whole-pool job stays starved even as concurrency falls — a prediction that **must hold if the structural-trap explanation is right**. It failed; the flow rises to 0.850. The moment that prediction failed, four studies' worth of explanation became a retraction.

W6 predicted, against this project's own definition, that the harm at that position would be "under 5× and therefore mild". It came in at 5.1× — a narrow failure.

**Rewriting the harm multiplier three times is also recorded as a failure.** 7.4×, 16.3×, 5.1×. The numbers themselves are not the problem; the problem is that **numbers in a hand-to-an-operator form kept being published before the axis was settled.**

## Evidence boundary

**Supported:** inside this synthetic model the safe boundary decreases with concurrency, the real virtual cluster's position is inside the measured range and on the safe side, and whole-pool starvation has no qualitative threshold.

**Not supported:** the boundary numbers (the detector was later invalidated); any policy comparison on the trace; reproduction across background distribution families.

## UNKNOWN

- Whether 0.875 at both 7.4 and 9.8 is saturation or just the top of the grid.
- Behaviour above a concurrency of 98.9.
- Dependence on load.
- Whether the result reproduces when the background distribution's shape changes.

## Falsification targets

- Changing only the granularity of the background makes starvation appear or vanish at the same ratio, pool and load. **This is exactly what the next study does.**
- A finer grid separates the boundaries at concurrency 7.4 and 9.8.
- A different detector changes the shape of the curve. **This also happened later: the shape held, the values moved.**

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Full rerun:

```bash
cd reproduction/gpu-scheduling-boundary
python run_e9.py
python analyze_e9.py
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-008](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-008.json)
- [E9 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E9_grading.json)
- Internal source Episode hash: `b821fb81d95ecfca2fef66f048b85812d98e15ddf39672b666170522b001d27f`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Attack this project's own headline result — that a demand distribution whose support includes the whole pool starves that class. Hold the ratio, the pool and the load fixed, change only the granularity of the background, and see whether starvation disappears.

## How this was reached

<div class="revision-chain vertical" aria-label="revision history of the GPU cluster scheduling research">
  <a href="/en/research/gpu-scheduling/"><b>EP-0001</b><span>Estimate error and restart cost swap which policy is best.</span></a>
  <a href="/en/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>Good averages hide a job class that never finishes. Three stability detectors broke.</span></a>
  <a href="/en/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>Starvation is set by whether whole-cluster jobs exist, not by mean gang size.</span></a>
  <a href="/en/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>Measured pools never meet that condition; the harm is a multiple, not starvation.</span></a>
  <a href="/en/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>The safe ratio falls as the pool grows; the harm at real scale was underestimated.</span></a>
  <a href="/en/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>The driver was never pool size. It is how many jobs compete at once.</span></a>
  <a class="current" href="/en/research/gpu-scheduling-real-cluster-position/"><b>EP-0007 · current</b><span>Measured at the real cluster's position, and corrected a mechanism claim carried for four studies.</span></a>
  <a href="/en/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>Changing only the granularity of the background made the headline result disappear.</span></a>
  <a href="/en/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>The axis of the flagship phase diagram was confounded by a factor of 18.</span></a>
  <a href="/en/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>Retracted \"two numbers decide this\". Frequency is a third variable.</span></a>
  <a href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
