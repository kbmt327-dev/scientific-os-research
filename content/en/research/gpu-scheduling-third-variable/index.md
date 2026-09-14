---
research_id: GPU-SCHED-EP-0010
title: Retracting "this is decided by two numbers"
date: 2026-09-14
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Synthetic simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: one sealed prediction (PRED-011, 7 of 11) and a 496-run full factorial over maximum job ratio, frequency and concurrency
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 256-server synthetic multiserver-job model, rho 0.85, exponential service, no restart cost, a single background distribution family
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0010
source_episode_sha256: f23d5954db2632ef6d7c385817ebc06c44389bd1bd1e0c4f95a0cd478be8d17b
publication:
  status: publishable
tags: [finding, scheduling, simulation, retraction]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-third-variable/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## Current finding

For three studies this domain's headline read:

> This problem is decided by two numbers: what fraction of pool capacity a job requires, and how many jobs are competing for that pool at once.

**We are retracting it.**

A full factorial that sets maximum job ratio, its frequency and concurrency independently, 496 runs. Concurrency can be designed through Little's law: against targets of 9.98 / 14.96 / 29.93 the measured values were 9.98 / 14.97 / 29.94 — fixed to 0.1%.

On that footing, **multiplying the largest class's frequency by 25 moves the boundary by one grid step at all three concurrency levels.** And the direction is not consistent: it falls at concurrency 10, falls then returns at 15, and rises at 30.

The **background distribution family** mattered more still. With concurrency, ratio and frequency all matched, changing only the family moved flow by up to 0.164 — larger than the frequency effect of 0.151.

While reconciling the grading against earlier studies, this work also found **something heavier**. Two rows of the published operational table sat just **+0.0006** and **+0.0064** above the decision line. The same statistic has a seed-to-seed standard deviation of 0.012 to 0.105. **Two rows of the operational table were, in effect, decided by noise.**

## Key figure

<div class="ratio-figure" aria-label="how far each factor moves the boundary"><div class="ratio-track"><i style="left:20%"></i><i style="left:50%"></i><i style="left:80%"></i></div><div class="ratio-labels"><span style="left:20%"><b>0.02</b> seed noise</span><span style="left:50%"><b>0.15</b> frequency ×25</span><span style="left:80%"><b>0.16</b> background family</span></div></div>

The axis is how far each factor moves the large class's flow. The published table's margins (0.0006 to 0.0064) lie further left than the left end of this figure.

## What this research shows

- With concurrency and maximum job ratio matched, **the largest class's frequency still moves the boundary by one grid step**. On the continuous statistic that is 0.037 to 0.069 — three to fifty times the seed standard error.
- **The background distribution family matters more than frequency** (up to 0.164 in flow).
- Little's law designs concurrency to within 0.1%.
- At fixed load, **a world with frequent whole-pool jobs and a world with high concurrency cannot coexist.** That is workload algebra, not a gap in the design.
- Even inside the healthy region, making the large class more frequent slows that class down (13 of 14 groups).

## What this research does not show

- Whether the effect comes from frequency itself or from the **share of offered work** that class carries. With ratio and mean gang size fixed, the two are proportional and this design cannot separate them.
- A boundary read off a grid is systematically conservative. Remeasured continuously, the rule of thumb at concurrency 30 is not 0.625 but about 0.76.
- The validity of the statistic used to judge the boundary is not examined here. **The next study finds it invalid.**

## Why this matters

"Decided by two numbers" was exactly the right shape to hand to an operator. The better the shape, the further outside its conditions it travels.

There are at least **four**: ratio, concurrency, frequency, and the shape of the background. The first two dominate, but the last two each move the boundary by a grid step. A table without a frequency column hands a conservative number to clusters where big jobs are rare and a dangerous one to clusters where they are common.

The noise finding probably travels further than the scheduling result. **Print, next to any claimed difference, how many times larger it is than the statistic's own resolution and spread.** That one line would have stopped this in the first study.

## Research question

The previous study's top open question: is the largest class's frequency an independent third variable?

## Method

A construction that sets three factors independently. The maximum job ratio is the largest class's server requirement; the frequency is its probability; concurrency is set by pinning mean gang size, translated through Little's law. The background distribution's ratio is fitted by bisection so its mean lands exactly on the required value, leaving the three factors free of each other.

- **Factorial arm**: 7 ratios × 3 concurrency levels × 3 frequencies, fully crossed, 315 runs
- **Frequency extension arm**: frequency out to 0.05, 70 runs
- **Replay gate**: 84 runs reproducing the previous study, confirmed at difference 0
- **Control arm**: EASY backfill, 27 runs

496 runs. Sealed as PRED-011 with SHA-256 `8f0fbd64ff019671a58499aa552bcf5aaa2a24923cf1068705e543be924e3765`, committed while no corresponding result file existed.

The deciding prediction Z2 — "the boundary is invariant to frequency" — was named **on the side where the then-current headline could be falsified**, and the sealed text states what gets deleted if it fails.

## Results

**The boundary moves with frequency.**

| Concurrency | freq 0.002 | 0.005 | 0.02 | 0.05 |
|---|---|---|---|---|
| 9.98 | 0.875 | 0.875 | **0.8125** | **0.8125** |
| 14.97 | 0.875 | **0.8125** | **0.8125** | 0.875 |
| 29.94 | 0.75 | 0.75 | **0.8125** | structurally impossible |

One grid step at all three levels, with inconsistent direction. This is not seed noise: the seed standard error of the continuous boundary is 0.001 to 0.024, an order of magnitude below the 0.037–0.069 movement.

**The background family matters more.** At matched concurrency, ratio and frequency, changing only the family moved flow by up to 0.164.

**The published table's margins, remeasured.**

| Published row | Margin above the line |
|---|---|
| Concurrency 9.8 | **+0.0006** |
| Concurrency 14.6 | **+0.0064** |

The same statistic's seed-to-seed standard deviation is 0.012 to 0.105.

**Grid rounding is a systematic bias.** Remeasured continuously, the concurrency-30 rule of thumb is **0.677 to 0.817**, not 0.625. Calling the last grid point that passed "the boundary" lands you a grid width short.

## What changed

- "This problem is decided by two numbers" was **retracted**.
- The operational table needs a **frequency column**; its concurrency-30 row was corrected from 0.625 to about 0.76 ± 0.07.
- [[en/research/gpu-scheduling-real-cluster-position/index|EP-0007]]'s "reproduction at zero grid steps under a different construction" was narrowed to **within one background distribution family**.
- The grid-based boundary was demoted from being the primary statistic.

## What failed

**PRED-011 scored 7 of 11. The deciding prediction Z2 failed.**

What failed is not only the prediction's content. While grading, this study found that **numbers its own domain had published across three studies were decided inside the statistic's own spread.** That was found *because* the prediction failed; had it passed, it would not have been.

And the upward correction made here — "the grid rounds conservative, so raise the number" — turns out in the **next study to have been a correction in the wrong direction**, because that conservatism was cancelling a different error.

## Evidence boundary

**Supported:** inside this synthetic model the boundary depends on at least four quantities. Ratio and concurrency dominate; frequency and background family are each worth a grid step. Little's law designs concurrency to 0.1%.

**Not supported:** separating frequency from work share; the validity of the judging statistic; any behaviour on a real trace. One load, one pool size, one service distribution, one background family.

## UNKNOWN

- The observation that the frequency effect is U-shaped (worst at a work share of 0.2–0.3, recovering above 0.5) is exploratory and was not sealed.
- Whether the background family effect reduces to a few summary quantities.
- **Whether the 0.9 decision line is valid at all.** Every operational number in this domain is a function of it.

## Falsification targets

- Construct the same work share from different (frequency, ratio, mean width) combinations and find the boundaries coincide. Then the acting variable is work share, not frequency.
- Moving the decision line reverses the order of conditions.
- Extending the observation window moves the boundary substantially. **The next study tests this, and the answer arrives in an unexpected form.**

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Full rerun:

```bash
cd reproduction/gpu-scheduling-boundary
python run_e12.py
python analyze_e12.py
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-011, including the deciding prediction and what its failure deletes](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-011.json)
- [E12 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E12_grading.json)
- Internal source Episode hash: `f23d5954db2632ef6d7c385817ebc06c44389bd1bd1e0c4f95a0cd478be8d17b`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Put the decision line itself on trial. Sweep the observation window from 30,000 to 120,000 jobs, sweep the line across 0.8 / 0.9 / 0.95, and remeasure every past boundary continuously. **Every operational number in this domain is a function of that line, so if the line does not hold, all of them have to be redone.**

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
  <a class="current" href="/en/research/gpu-scheduling-third-variable/"><b>EP-0010 · current</b><span>Retracted \"two numbers decide this\". Frequency is a third variable.</span></a>
  <a href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
