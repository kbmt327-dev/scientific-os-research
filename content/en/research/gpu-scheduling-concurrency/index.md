---
research_id: GPU-SCHED-EP-0006
title: The driver was never pool size. It is how many jobs compete at once
date: 2026-09-13
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Synthetic simulation and public-trace measurement
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation-and-public-trace
  source: one sealed prediction (PRED-007, 6 of 6), a 224-run confound separation, and measured concurrency for 11 Philly virtual clusters
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: synthetic multiserver-job model at rho 0.85, exponential service, no restart cost. The trace side contributes measured concurrency and maximum job ratio only
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0006
source_episode_sha256: a6dc66607f3e9141bf2a29ed13dde581fc62e65dff31f010ed2909243928cf49
publication:
  status: publishable
tags: [finding, scheduling, simulation, confounding, traces]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-concurrency/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation and public traces</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

> [!note] The axis found here survives. The numbers were later remeasured
> The **discovery of the axis** — that the number of jobs concurrently competing for the pool is the driver — has held across the seven studies since. The detector used here to locate the boundary was invalidated in [[en/research/gpu-scheduling-blind-detector/index|EP-0011]] and replaced in [[en/research/gpu-scheduling-alpha-boundary/index|EP-0012]]. **Quote the axis; do not quote the numbers.**

## Current finding

The previous study ([[en/research/gpu-scheduling-pool-size/index|EP-0005]]) reported that the safe boundary falls as the pool grows. Its own sealed document also recorded why that conclusion could not be trusted: **changing pool size also changes the number of background classes and the number of jobs concurrently competing for the pool.**

We separated them. **The driver is neither the pool's server count nor the number of background classes. It is how many jobs are competing for the pool at the same time.**

Hold concurrency fixed and multiply the pool by eight, and the boundary does not move. Hold the pool fixed and change concurrency, and it does. **Server count was a proxy.**

This axis has a practical consequence. Concurrency is something an operator can measure, and when measured on the public traces, **the two dangerous conditions never appear in the same cluster.** The virtual cluster whose largest job takes 59% of its pool (11cb48) runs at a concurrency of 10.2, the second lowest of eleven. The cluster with the highest concurrency, 81.1 (6214e9), has a largest job at 3% of its pool. Ratio and concurrency are negatively correlated.

## Key figure

<div class="ratio-figure" aria-label="concurrency against the safe boundary"><div class="ratio-track"><i style="left:12%"></i><i style="left:34%"></i><i style="left:100%"></i></div><div class="ratio-labels"><span style="left:12%"><b>28.5 jobs</b><br>boundary 0.625</span><span style="left:34%"><b>54</b><br>0.50</span><span style="left:100%"><b>168</b><br>0.50</span></div></div>

The axis is the number of jobs competing for the pool at once. The more there are, the smaller the share a single job may take. Multiply the pool's server count by eight and the boundary stays where it is, as long as that number is unchanged.

## What this research shows

- In this synthetic model the boundary is set by **how many jobs are running concurrently**, not by the pool's server count or by the number of background classes. Hold concurrency fixed and an eight-fold larger pool gives the same boundary, 0.625.
- Conditions whose concurrency agrees within 20% give boundaries that agree within one grid step.
- Across the 11 Philly virtual clusters, maximum job ratio and concurrency are negatively correlated, so the two risk factors do not co-occur in any measured cluster.

## What this research does not show

- It does not settle *why* concurrency matters. The mechanism story current at this point is corrected by the next study.
- No scheduling policy was run on a real arrival stream. From the trace we took only measured concurrency and maximum job ratio.
- The boundary **numbers** were produced by a detector later shown to be invalid.

## Why this matters

The previous study left a confound it had declared for itself, and then wrote its conclusion in the indicative: pool size is what matters. Handed to an operator, that becomes "how many servers is your pool?". Easy to measure, and the wrong question.

The right question is "how many jobs run on it at once?". Just as easy to measure, and actually load-bearing. The difference came from one procedural rule: **a confound you declare must be separated in the next cycle.**

## Research question

Which of the confounded variables sets the safe boundary?

1. the pool's server count
2. the number of background job classes
3. the number of jobs concurrently competing for the pool

## Method

A design that moves the three independently. Holding the background demand shape fixed *relative to* the pool preserves concurrency while the server count changes. Changing only the granularity of the background moves concurrency while the pool stays fixed. 224 runs at rho 0.85.

Sealed as PRED-007; the digest is committed at `predictions/PRED-007.sha256` in the reproduction package, and the commit was made while no corresponding result file existed.

On the trace side, per-virtual-cluster concurrency was measured by an event walk, time-averaged over the periods when the cluster is non-empty.

## Results

**With concurrency held fixed, pool size does nothing.**

| Condition | Pool size | Concurrency | Safe boundary |
|---|---|---|---|
| Baseline | 64 | 28.5 | 0.625 |
| Pool ×8 | 512 | 28.4 | **0.625** |

**Move concurrency and the boundary moves.**

| Concurrency | 28.5 | 54.2 | 99.0 | 168.5 |
|---|---|---|---|---|
| Safe boundary | 0.625 | 0.50 | 0.50 | 0.50 |

**The number of background classes is not the driver.** Changing it left the boundary unmoved as long as concurrency was unchanged.

**In the real traces the two risk factors do not co-occur.**

| Virtual cluster | Max job ratio | Concurrency |
|---|---|---|
| 11cb48 | **0.59** (highest) | 10.2 (second lowest of 11) |
| 6214e9 | 0.03 | **81.1** (highest) |

High-ratio clusters run at low concurrency and high-concurrency clusters have small jobs. Within these two traces, the dangerous combination is not observed.

## What changed

- The previous study's "the boundary is set by pool size" was **retracted** and replaced by "it is set by how many jobs compete for the pool at once".
- The operational question changed from "how many servers?" to "how many jobs run at once?".
- The previous study's 16.3× harm estimate at realistic scale was **an estimate on the wrong axis**, and has to be remeasured on the right one in the next study.

## What failed

**PRED-007 scored 6 of 6.** Every sealed prediction in this study passed.

That is not where the value is. The value is that **a confound the previous study declared for itself, and then wrote over in the indicative, was actually separated one cycle later.** Without the declaration it would not have been traceable; without the separation the declaration would have meant nothing.

The failure worth recording belongs to the previous study: **it declared an unresolved confound and still wrote a variable name into its conclusion as fact.** For one cycle, the published explanation named the wrong variable.

## Evidence boundary

**Supported:** inside this synthetic model the boundary is set by concurrency, with server count and background class count acting as proxies. Within these two public traces, high ratio and high concurrency do not appear in the same virtual cluster.

**Not supported:** the mechanism, which is corrected in the next study. The boundary numbers, which come from a detector later shown to be invalid. Any claim about running a policy on a real arrival stream.

## UNKNOWN

- The boundary around a concurrency of 10 — where the real virtual clusters actually sit. The lowest measured here is 28.5.
- Whether the concurrency-boundary relation saturates logarithmically or continues toward zero.
- Why concurrency matters. The explanation current at this point is provisional.

## Falsification targets

- Two conditions with matched concurrency give boundaries more than one grid step apart.
- Another trace contains a production pool with both a high ratio and high concurrency.
- Using a different statistic to locate the boundary makes the concurrency effect disappear. **This partly happened later: the numbers changed, the axis survived.**

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Full rerun:

```bash
cd reproduction/gpu-scheduling-boundary
python run_e8.py
python analyze_e8.py
python measure_vc_concurrency.py   # needs the raw Philly trace
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-007](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-007.json)
- [E8 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E8_grading.json)
- [Measured concurrency per Philly virtual cluster](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E8_philly_concurrency.json)
- Internal source Episode hash: `a6dc66607f3e9141bf2a29ed13dde581fc62e65dff31f010ed2909243928cf49`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Extend the boundary curve down to a concurrency of about 10, where the real virtual clusters sit. The lowest measured so far is 28.5, so the real cluster's position is currently reached only by extrapolation.

## How this was reached

<div class="revision-chain vertical" aria-label="revision history of the GPU cluster scheduling research">
  <a href="/en/research/gpu-scheduling/"><b>EP-0001</b><span>Estimate error and restart cost swap which policy is best.</span></a>
  <a href="/en/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>Good averages hide a job class that never finishes. Three stability detectors broke.</span></a>
  <a href="/en/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>Starvation is set by whether whole-cluster jobs exist, not by mean gang size.</span></a>
  <a href="/en/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>Measured pools never meet that condition; the harm is a multiple, not starvation.</span></a>
  <a href="/en/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>The safe ratio falls as the pool grows; the harm at real scale was underestimated.</span></a>
  <a class="current" href="/en/research/gpu-scheduling-concurrency/"><b>EP-0006 · current</b><span>The driver was never pool size. It is how many jobs compete at once.</span></a>
  <a href="/en/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>Measured at the real cluster's position, and corrected a mechanism claim carried for four studies.</span></a>
  <a href="/en/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>Changing only the granularity of the background made the headline result disappear.</span></a>
  <a href="/en/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>The axis of the flagship phase diagram was confounded by a factor of 18.</span></a>
  <a href="/en/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>Retracted \"two numbers decide this\". Frequency is a third variable.</span></a>
  <a href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
