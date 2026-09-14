---
research_id: GPU-SCHED-EP-0005
title: The safe ratio falls as the pool grows
date: 2026-09-13
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Synthetic simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: one sealed prediction (PRED-006) and a 294-run ratio sweep across pool sizes 32 to 512
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: synthetic multiserver-job model at 32 to 512 servers, rho 0.85, exponential service, no restart cost, a single background demand shape
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0005
source_episode_sha256: 3e72377d2a441966354b8c935104108933c5db8f863c2f22d3c9596edc87a680
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-pool-size/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

> [!warning] The next study found this one had named the wrong variable
> The **observation** here — that the safe ratio falls as the pool grows — holds. The **causal attribution** does not. [[en/research/gpu-scheduling-concurrency/index|EP-0006]] separated the confound and showed the driver is not the pool's server count but the number of jobs concurrently competing for it. Read EP-0006 before quoting any number from this study. The way the boundary was measured was itself later invalidated in [[en/research/gpu-scheduling-blind-detector/index|EP-0011]] and replaced in [[en/research/gpu-scheduling-alpha-boundary/index|EP-0012]].

## Current finding

The previous study ([[en/research/gpu-scheduling-real-traces/index|EP-0004]]) produced a safe-side rule of thumb on a 64-server pool: the largest job may take up to 0.75 of pool capacity. That same study recorded that exactly one of its predictions failed, and the failure had a direction. The assumption that **equal ratios give equal outcomes** was only an approximation, and the error was systematically toward **larger pools being more dangerous**.

Real GPU virtual clusters run 217 to 603 servers, far above 64. Whether the 0.75 rule survives at that scale is not something you can reason your way to.

It does not. The safe boundary falls monotonically with pool size: 0.81 at 32 servers, 0.50 at 512. The harm the previous study estimated at the measured ratio of 0.59 — 7.4× the delay of a one-server job — is **16.3×** at realistic scale. Roughly a two-fold underestimate.

One more thing belongs in the record. **Changing pool size moved three quantities at once**: the server count, the number of background job classes, and the number of jobs concurrently competing for the pool. The sealed document declares that confound in advance. So what this study establishes is a **correlation** with pool size, not a cause. The next study does the separation.

## Key figure

<div class="ratio-figure" aria-label="safe ratio by pool size"><div class="ratio-track"><i style="left:50%"></i><i style="left:68.75%"></i><i style="left:81.25%"></i></div><div class="ratio-labels"><span style="left:50%"><b>0.50</b> 512 servers</span><span style="left:68.75%"><b>0.69</b> 128 servers</span><span style="left:81.25%"><b>0.81</b> 32 servers</span></div></div>

The axis is the largest job's server requirement divided by pool capacity. The larger the pool, the further left the permitted ratio moves. Real virtual clusters sit at 217 to 603 servers, toward the left of this figure.

## What this research shows

- In this synthetic model, the largest ratio at which the big-job class keeps up with its own arrivals falls monotonically with pool size: 0.8125 / 0.75 / 0.6875 / 0.625 / 0.50 at 32 / 64 / 128 / 256 / 512 servers.
- The harm multiplier the previous study measured at 64 servers was about a two-fold underestimate at a scale close to real virtual clusters.
- Reservation-based EASY backfill does not starve the large class on this axis either.

## What this research does not show

- **It does not identify a cause.** Changing pool size also changes the background class count and the number of concurrently running jobs. The confound was declared at sealing time and is separated in the next study.
- No scheduling policy was run on a real arrival stream. This is entirely inside the synthetic model.
- One load (rho 0.85), one service distribution (exponential), one background demand shape.

## Why this matters

The previous study produced a number in a form you can hand to an operator: the largest job may take up to 0.75 of capacity. The more a number looks ready to hand over, the more it gets used outside the conditions it was measured in.

64 servers is smaller than every real virtual cluster in the trace. **The conditions that produced the rule did not contain the conditions where the rule would be used.** This study went after that gap and found the rule is scale-dependent.

## Research question

1. Does the previous study's 0.75 boundary hold at real pool sizes (217 to 603 servers)?
2. If not, in which direction and by how much does it move?

## Method

To a background of small jobs, add one large class requiring `m` servers, arriving with probability 0.002. Vary pool size `N` over 32 / 64 / 128 / 256 / 512 and sweep the ratio `m/N` across seven points from 0.50 to 1.00. rho 0.85, five seeds at small scale and three at large, 294 runs.

Sealed as PRED-006 with SHA-256 `b78c62fd5f6db0c9032d5f0ce09da52e104919af20223578b194ff96ce9810f2`. Sealing means the prediction text and the grading rules are fixed and hashed before any result is seen; the commit was made while no corresponding result file existed.

The boundary was judged by whether the large class's flow balance — how well that class keeps up with its own arrivals — stayed at or above 0.9. **That detector was later shown to be invalid** ([[en/research/gpu-scheduling-blind-detector/index|EP-0011]]).

## Results

**The boundary falls monotonically with pool size.**

| Pool size N | 32 | 64 | 128 | 256 | 512 |
|---|---|---|---|---|---|
| Safe ratio (under this detector) | 0.8125 | 0.75 | 0.6875 | 0.625 | 0.50 |
| Flow balance of a whole-pool job | 0.53 | 0.39 | 0.24 | 0.16 | 0.10 |

**Harm at realistic scale.** The previous study reported, at 64 servers, that a job at the measured ratio of 0.59 runs 7.4× slower than a one-server job. At 256 servers and ratio 0.625 the figure is **16.3×**. Carrying the rule to realistic scale roughly doubles the expected harm.

**The ratio matters more than the pool size.** Moving the ratio from 0.5 to 1.0 changes flow balance by 0.872; moving the pool from 32 to 512 changes it by 0.475. Both matter; the ratio dominates.

**EASY backfill does not break on this axis.** Its lowest flow balance was 0.925, at 512 servers with a whole-pool job — above the starvation line. The sealed prediction said 0.99 or better, so that one failed.

## What changed

- The previous study's single rule of thumb, "up to 0.75 of pool capacity", was replaced by **a table indexed by pool size**.
- The harm estimate at realistic scale was revised from 7.4× to 16.3×.

## What failed

**PRED-006 scored 6 of 8.** Of the two failures, the EASY backfill floor (predicted 0.99 or better) came in at 0.925. This project has repeatedly written that the policy "has never broken", and had set the floor optimistically. It does not break, but it is not insensitive either.

**A fourth instrument defect was found.** Comparing across pool sizes, the length of the measurement window turned out to vary by condition. At a fixed job count the observation window is `jobs / arrival rate`, so it shrinks as the pool grows — 2,296 time units at 32 servers, 232 at 512. Absolute backlog was being capped by the window, making the trend read backwards. Rate-based metrics or window normalisation are required.

**The most important failure is in the conclusion itself.** The sealed document declares the confound, and then the conclusion was written in the indicative: pool size is what matters. When the next study separated the variables, the driver was something else. The declaration made it traceable — but in the meantime this study's conclusion named the wrong variable.

## Evidence boundary

**Supported:** inside this synthetic model, the largest ratio at which the big class keeps up falls monotonically with pool size, and the harm multiplier measured at 64 servers roughly doubles at realistic scale.

**Not supported:** any causal attribution. Pool size, background class count and concurrent job count move together. No policy was run on a real arrival stream. The statistic used to locate the boundary was later shown to be invalid.

## UNKNOWN

- Whether the boundary is set by server count, by the number of background classes, or by how many jobs are running at once.
- Whether the boundary saturates at 0.5 beyond N = 1024 or keeps falling.
- Behaviour at other loads.
- Interaction with a non-zero restart cost.

## Falsification targets

- Hold the concurrent job count fixed, vary only pool size, and find the boundary does not move. **This is what happened.**
- Hold the background class count fixed, vary pool size, and find the boundary does not move.
- Use a different statistic to locate the boundary and find the scale dependence disappears.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Full rerun:

```bash
cd reproduction/gpu-scheduling-boundary
python run_e7.py
python analyze_e7.py
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-006](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-006.json)
- [E7 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E7_grading.json)
- Internal source Episode hash: `3e72377d2a441966354b8c935104108933c5db8f863c2f22d3c9596edc87a680`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Separate the confound this study declared for itself. Vary pool size, background class count, and concurrent job count independently, and find out which one sets the boundary.

## How this was reached

<div class="revision-chain vertical" aria-label="revision history of the GPU cluster scheduling research">
  <a href="/en/research/gpu-scheduling/"><b>EP-0001</b><span>Estimate error and restart cost swap which policy is best.</span></a>
  <a href="/en/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>Good averages hide a job class that never finishes. Three stability detectors broke.</span></a>
  <a href="/en/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>Starvation is set by whether whole-cluster jobs exist, not by mean gang size.</span></a>
  <a href="/en/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>Measured pools never meet that condition; the harm is a multiple, not starvation.</span></a>
  <a class="current" href="/en/research/gpu-scheduling-pool-size/"><b>EP-0005 · current</b><span>The safe ratio falls as the pool grows; the harm at real scale was underestimated.</span></a>
  <a href="/en/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>The driver was never pool size. It is how many jobs compete at once.</span></a>
  <a href="/en/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>Measured at the real cluster's position, and corrected a mechanism claim carried for four studies.</span></a>
  <a href="/en/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>Changing only the granularity of the background made the headline result disappear.</span></a>
  <a href="/en/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>The axis of the flagship phase diagram was confounded by a factor of 18.</span></a>
  <a href="/en/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>Retracted \"two numbers decide this\". Frequency is a third variable.</span></a>
  <a href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
