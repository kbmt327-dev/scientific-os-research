---
research_id: GPU-SCHED-EP-0013
title: The real-cluster claim rests on one job out of 19,100
date: 2026-09-14
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Public-trace measurement, no simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: public-trace-measurement
  source: one sealed prediction (PRED-014, 4 of 6) and measured arrival frequencies for 11 Philly virtual clusters. No new simulation
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: the public Microsoft Philly trace, 11 virtual clusters with at least 500 jobs. Capacity is taken as measured peak concurrent GPU usage
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0013
source_episode_sha256: 990cbc3e360d78ce5f7cd1cde10e7550a97c79bbd88d8cedf3e5417d5f4a32ea
publication:
  status: publishable
tags: [finding, scheduling, traces, scope]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-one-job/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Public-trace measurement</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## Current finding

The previous study restored the operational table, but the table has a frequency column — and the one claim this domain makes about a real cluster, that Philly's virtual cluster 11cb48 is on the safe side, had no measured frequency. On the table's 0.002 row the safe ratio is 0.92 (margin 0.33); on the 0.02 row it is 0.72 (margin 0.13). **A factor of 2.5.**

We measured it from the trace already on disk, with no simulation at all.

**In 11cb48, exactly one job out of 19,100 required at least half the pool's capacity.** A frequency of 5.2×10⁻⁵ — **38× rarer** than the table's lowest frequency row. Since the boundary rises as frequency falls, that row's 0.92 can be used directly as a lower bound.

**The margin is 0.33 (lower bound).**

But the clearest thing this study produced is not the margin. It is **how narrow the scope is.**

- **Ten of the eleven virtual clusters contain no job at all above a quarter of capacity.**
- In the one exception, 11cb48, six jobs exceed a quarter of capacity and **one** exceeds half.
- No cluster contains a job that fills its pool (confirmed on recount).

**Everything this domain has claimed about a real cluster rests on one job in the whole Philly trace.**

## Key figure

<div class="ratio-figure" aria-label="frequency of large jobs across the 11 Philly virtual clusters"><div class="ratio-track"><i style="left:59%"></i><i style="left:92%"></i></div><div class="ratio-labels"><span style="left:59%"><b>0.59</b> 11cb48's largest ratio<br>one job in 19,100</span><span style="left:92%"><b>0.92</b> alpha-basis boundary<br>margin 0.33</span></div></div>

11cb48's largest job is 128 GPUs against a capacity of 217. Excluding that one job, only five jobs in this cluster exceed a quarter of capacity.

## Results

| Virtual cluster | Jobs | Concurrency | Capacity | Max k | Ratio | P(≥0.25) | P(≥0.5) | P(≥1.0) |
|---|---|---|---|---|---|---|---|---|
| 6214e9 | 51,378 | 81.1 | 603 | 16 | 0.03 | 0 | 0 | 0 |
| **11cb48** | **19,100** | **10.2** | **217** | **128** | **0.59** | **0.000314** | **0.000052** | **0** |
| 6c71a0 | 14,833 | 46.2 | 290 | 48 | 0.17 | 0 | 0 | 0 |
| b436b2 | 9,159 | 22.8 | 340 | 32 | 0.09 | 0 | 0 | 0 |
| ee9e8c | 5,602 | 38.9 | 532 | 128 | 0.24 | 0 | 0 | 0 |
| 6 others | 10,983 | 4.9–27.6 | 66–360 | 1–32 | 0.02–0.25 | 0 | 0 | 0 |

The 0.000052 in `P(≥0.5)` is **one job** out of 19,100.

## What this research shows

- The arrival frequency of Philly 11cb48's largest-ratio class is 5.2×10⁻⁵ — 38× rarer than the lowest frequency row of the alpha-basis table.
- The margin over the ratio of 0.59 is therefore **0.33 (lower bound)**. The previous study's 0.13–0.33 range settles at the wide end.
- Ten of eleven virtual clusters contain no job above a quarter of capacity.
- No cluster contains a job that fills its pool — [[en/research/gpu-scheduling-real-traces/index|EP-0004]]'s headline survives its own recount.

## What this research does not show

- **Whether the two risk factors co-occur on the frequency axis is untestable here.** Only 11cb48 has any job above 40% of capacity; the other ten are tied at zero. With no variation, no direction of correlation can be claimed. It is neither supported nor refuted.
- Mapping a continuous distribution onto a single-class frequency is not unique. Mapping by share of offered work could land on a different row.
- The table was measured at 256 servers, rho 0.85 and exponential service, none of which Philly matches. **This places a real cluster on the model's axes; it is not the result of running a scheduling policy on the trace.**

## Why this matters

"Confirmed on a real trace" sounds strong. This study put a number on what that phrase actually covers. **One job.**

The practical implication lies in the procedure rather than the value. To assess your own cluster, first count how many jobs a year require at least half of capacity. If the answer is zero, this domain's boundary discussion does not concern you yet. Ten of eleven clusters were in that state.

## Research question

How often do large jobs actually arrive in the Philly virtual clusters, and which row of the alpha-basis table does 11cb48 fall on?

## Method

From Philly's `cluster_job_log`, for each virtual cluster with at least 500 jobs, recompute capacity (peak concurrent GPU usage), concurrency, the maximum gang size, and `P(need ≥ q × capacity)` for q = 0.25 / 0.40 / 0.50 / 0.59 / 0.75 / 1.00. **No new simulation.**

Sealed as PRED-014 with SHA-256 `9fedc330b067f8cc3616f1fcc896f55ba4bb3887ebf523dfcf4493ad539ee281`, committed while no corresponding result file existed.

The sealed text also records why the measurand was chosen. Mapping a continuous distribution onto a single-class frequency is not unique, so the chosen mapping is stated to fall on the **non-conservative (upper-bound) side**. Taking capacity as peak concurrent usage also makes ratios upper bounds. Both point the same way: the measured risk is not understated.

## What changed

- Philly's margin was fixed from a 0.13–0.33 range to **0.33 (lower bound)**.
- The content of "confirmed on a real trace" was stated at its real scale: **one job**.
- The previous claim that ratio and concurrency are negatively correlated in real traces was split into **valid on the concurrency axis, untestable on the frequency axis**.

## What failed

**PRED-014 scored 4 of 6. The deciding prediction K1 passed.**

**K2 failed, and it failed because of the threshold I sealed.**

11cb48's capacity is 217 GPUs and its largest job is 128, so the ratio is 128 ÷ 217 = **0.5899**. The sealed text specified a threshold of `q = 0.59`. That makes `0.59 × 217 = 128.03`, and **the very job that defines the ratio was excluded by 0.03 of a GPU.**

`P(≥0.59) = 0` is not physics; it is **a rounded measurement written back as a cut.** With the threshold at 0.5, one job qualifies and K2's criterion is met.

This is the **fifth instance** of a failure mode this domain keeps rediscovering: grid rounding, the decision line, sample size, window normalisation, and now threshold rounding. This time the sealed text required "the count must not be zero", so it was **caught at grading time.** Without that clause, a strong conclusion of "no such jobs" would very likely have been published as it stood.

**K4 failed, but it is not a refutation.** The correlation between ratio and frequency is +0.50 (p = 0.117), missing the sealed criterion of ≤ 0. But only 11cb48 has any job above 40% of capacity; the other ten are tied at zero. **The correlation was not "the other way"; the trace has no variation.** The pre-committed consequence was executed, but written as "untestable in this trace" rather than "does not extend to the frequency axis".

**A procedural lapse.** The grading script was not included in the sealing commit. The previous three studies put it in the same commit as the prediction file. The criteria are all in the sealed text so the grading is mechanical, but the discipline is a notch weaker. It is recorded in `results/E15_grading.json` as `grading_script_not_sealed: true`.

## Evidence boundary

**Supported:** the largest-ratio class in Philly 11cb48 arrives once in 19,100 jobs; ten of eleven virtual clusters contain no job above a quarter of capacity; no cluster contains a whole-pool job. All of these are trace measurements.

**Not supported:** any relation between the two risk factors on the frequency axis (untestable); any policy comparison on the trace. The margin of 0.33 is a measured frequency fed into a synthetic model's table.

## UNKNOWN

- Whether the two risk factors co-occur on the frequency axis. Philly has no variation; another trace is required.
- Real cluster frequencies do not land on the table's grid. 11cb48 sits below the lowest row, so it can only be **placed outside the table and read as a lower bound**.
- Sensitivity to the choice of mapping from a continuous distribution to a single-class frequency.

## Falsification targets

- Published allocation quotas show a capacity far below peak concurrent usage, which would raise the ratio and shrink the margin.
- Another production trace contains a pool with both a high ratio and a high frequency.
- Mapping frequency by share of offered work instead lands the cluster on a different row.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

This quick check re-derives the **one-in-19,100 measurement** from the stored results and confirms that no virtual cluster contains a whole-pool job.

A full rerun needs the raw Philly trace, which is not redistributed here. Fetch it from `msr-fiddle/philly-traces` and place it at `data/trace-data/`.

```bash
cd reproduction/gpu-scheduling-boundary
python run_e15.py
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-014, including the reasoning for the measurand](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-014.json)
- [E15 measurements](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E15.json)
- [E15 grading, including the record of the unsealed grading script](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E15_grading.json)
- Internal source Episode hash: `990cbc3e360d78ce5f7cd1cde10e7550a97c79bbd88d8cedf3e5417d5f4a32ea`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Refine the table's frequency axis. It currently has only two rows, 0.002 and 0.02, and the measured real-cluster value of 5.2×10⁻⁵ sits **outside** it. Extend the lower end to 10⁻⁴ and add intermediate points so a measured frequency can be read without rounding.

## How this was reached

<div class="revision-chain vertical" aria-label="revision history of the GPU cluster scheduling research">
  <a href="/en/research/gpu-scheduling/"><b>EP-0001</b><span>Estimate error and restart cost swap which policy is best.</span></a>
  <a href="/en/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>Good averages hide a job class that never finishes. Three stability detectors broke.</span></a>
  <a href="/en/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>Starvation is set by whether whole-cluster jobs exist, not by mean gang size.</span></a>
  <a href="/en/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>Measured pools never meet that condition; the harm is a multiple, not starvation.</span></a>
  <a href="/en/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>The safe ratio falls as the pool grows; the harm at real scale was underestimated.</span></a>
  <a href="/en/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>The driver was never pool size. It is how many jobs compete at once.</span></a>
  <a href="/en/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>Measured at the real cluster's position, and corrected a mechanism claim carried for four studies.</span></a>
  <a href="/en/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>Changing only the granularity of the background made the headline result disappear.</span></a>
  <a href="/en/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>The axis of the flagship phase diagram was confounded by a factor of 18.</span></a>
  <a href="/en/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>Retracted \"two numbers decide this\". Frequency is a third variable.</span></a>
  <a href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a class="current" href="/en/research/gpu-scheduling-one-job/"><b>EP-0013 · current</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
