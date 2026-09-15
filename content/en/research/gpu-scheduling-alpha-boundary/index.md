---
research_id: GPU-SCHED-EP-0012
title: Replaced it with a statistic whose boundary stays put, and restored the numbers
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
  source: one sealed prediction (PRED-013, 8 of 11, deciding prediction passed) and 1440 runs across four observation windows and eight seeds
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 256-server synthetic multiserver-job model, rho 0.85, exponential service, no restart cost, a single background distribution family, observation windows of 30,000 to 240,000 jobs
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0012
source_episode_sha256: 9f33d6cf645c7273f53984f13ce51ae2bc3b87aaba50ae1df822ed1756755ce6
publication:
  status: publishable
tags: [finding, scheduling, simulation, instrument]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-alpha-boundary/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

> [!warning] Later audit, 2026-09-16
> [[en/research/gpu-scheduling-u31-calibration/index|EP-0017]] found a local disagreement between alpha=0.5 and a separate backlog detector. Boundaries and margins in this dated Note depend on an unaudited threshold in the synthetic model; do not treat them as capacity guarantees.

## Current finding

The previous study demoted the detector and put this domain's operational numbers on hold. The replacement candidate is **alpha — the elasticity of mean response time with respect to the observation window**:

```
alpha = d log(mean response time) / d log(observation window)
        0 = converged,  1 = linear divergence
```

Unlike flow balance it is not normalised by the window, so divergence cannot cancel.

Measured under seal across four windows (30,000 to 240,000 jobs), eight seeds, 1440 runs. **The deciding prediction passed.**

Alpha has three properties:

| Property | Measured | Flow balance |
|---|---|---|
| Reads 0 where the system is plainly stable | −0.046 to +0.029 | ranges 0.88 to 1.00 by condition |
| Reads 1 where it plainly is not | 0.899 to 0.984 | 0.25 to 0.65 |
| Boundary unmoved when the window is multiplied by eight | −0.021 to +0.006 | unmoved, but because divergence cancels |
| Precise enough to quote | 90% interval half-width 0.013 to 0.021 | published margin was 0.10 of one job |

**The hold on operational numbers is lifted.**

This study also checked, with an independent detector, the most-cited claim in the domain: that EASY backfill has never broken a class. Even for a whole-pool class, alpha is about 0. **It was not an artifact of the blind detector.**

## Key figure

<div class="ratio-figure" aria-label="alpha against the job ratio"><div class="ratio-track"><i style="left:50%"></i><i style="left:87.5%"></i><i style="left:100%"></i></div><div class="ratio-labels"><span style="left:50%"><b>0.5</b><br>alpha ≈ 0<br>converged</span><span style="left:87.5%"><b>0.875</b><br>alpha 0.29–0.95</span><span style="left:100%"><b>1.0</b><br>alpha ≈ 0.96<br>linear divergence</span></div></div>

The axis is the largest job's share of pool capacity. Alpha reads 0 at the plainly stable left end and 1 at the plainly divergent right end — a calibration flow balance never had.

## Results

**Operational numbers, on the alpha basis**

256 servers, rho 0.85, exponential service, no restart cost, background geometric over {1…64}. Decision line alpha = 0.5, windows 30,000 to 240,000 jobs, eight seeds, 90% bootstrap interval.

| Concurrency | Frequency of the largest class | Safe maximum job ratio | 90% interval |
|---|---|---|---|
| 10 | 0.002 | **0.92** | [0.903, 0.932] |
| 10 | 0.02 | **0.72** | [0.706, 0.732] |
| 15 | 0.002 | **0.85** | [0.834, 0.863] |
| 15 | 0.02 | **0.68** | [0.667, 0.695] |
| 30 | 0.002 | **0.73** | [0.713, 0.749] |
| 30 | 0.02 | **0.66** | [0.640, 0.682] |

**Do not drop the frequency column.** Its absence is why the old table kept breaking across three studies.

**Against the old table — the errors did not share a direction.**

| Concurrency | Old published value | alpha (freq 0.002) | alpha (freq 0.02) |
|---|---|---|---|
| ~10 | 0.875 | **0.92** | **0.72** |
| ~15 | 0.8125 | **0.85** | **0.68** |
| ~30 | 0.625 | **0.73** | **0.66** |

The old table was **conservative for rare large jobs (0.04 to 0.11 low) and dangerous for frequent ones** (0.875 against 0.72 at concurrency 10). Grid rounding pushes the boundary down (conservative, mean 0.040); the censoring ratio's blindness pushes it up (dangerous). At low frequency the first wins, at high frequency the second. **Publishing a single number meant it could not even be wrong in a consistent direction.**

**Deciding prediction: the boundary stays put.** Alpha fitted on three windows against four differs by −0.021 to +0.006; all six cells are inside the sealed tolerance of 0.03.

**Bootstrap.** Over 2000 resamples of the eight seeds, the 90% interval half-width is 0.013 to 0.021 — a third of the sealed criterion of 0.06.

**EASY backfill.**

| Concurrency | ratio 0.875 | ratio 1.0 |
|---|---|---|
| 10 | 0.020 | 0.011 |
| 15 | 0.009 | −0.008 |
| 30 | −0.002 | −0.013 |

Against greedy SRPT's 0.90 to 0.98 in the same conditions, this is not a detector artifact.

## What this research shows

- Alpha reads 0 where stable and 1 where divergent, moves the boundary by at most 0.02 when the window is multiplied by eight, and is quotable to a 90% half-width of 0.02.
- The operational table on that basis, including a frequency column.
- The old table's errors did not share a direction; which way it erred flipped with frequency.
- EASY backfill's class health is confirmed by an independent detector.

## What this research does not show

- The decision line alpha = 0.5 is a convention — the midpoint between converged and linearly divergent — not a derived criterion. The observation that moving the line between 0.3 and 0.7 shifts the boundary by only ±0.04 while preserving the ordering is **unsealed**.
- Mean response time averages completed jobs only. The more severely a class diverges, the more its slow jobs are excluded, so alpha is biased **downward** at the divergent end. The alpha boundary therefore errs toward calling things stable.
- No scheduling policy was run on a real arrival stream. One load, one pool size, one service distribution, one background family.

## Why this matters

This domain reached a state where changing the detector changed every number. Getting out of it required sealing a prediction about **the detector itself, not about the numbers**.

The deciding prediction was whether adding one more observation window moves the boundary. Only once that is shown not to happen can the boundary be handed to an operator. Had it moved, the conclusion would have been that no finite-window statistic has a fixed point here, and the plan was to move to a test that does not depend on a window at all.

**The qualitative axis has not broken once across five detector changes and three retractions.** What broke was always the numbers.

## Research question

1. Does alpha give a boundary that stops moving when a window is added?
2. Is it precise enough to quote?
3. Was EASY backfill's health an artifact of the blind detector?

## Method

7 ratios × 3 concurrency levels × 2 frequencies × 4 windows (30,000 / 60,000 / 120,000 / 240,000 jobs) × 8 seeds — 1344 runs, plus 96 EASY backfill controls. 1440 runs, 57 minutes on eight workers.

Seeds 901–905 at 30,000 to 120,000 double as a replay gate against the previous study; **630 rows reproduced at difference 0**.

Sealed as PRED-013 with SHA-256 `803590cd3c15b5dd383e2f4a900c129e79c66ea7db786c54842b70ee87ba830c`, committed while no corresponding result file existed.

## What changed

- The **hold was lifted** and the operational table reissued on the alpha basis, now with a frequency column.
- The detector was replaced, from flow balance to alpha.
- A **correction band** was added to the previous study's exploratory claim that the old table erred optimistic. In fact the errors did not share a direction.

## What failed

**PRED-013 scored 8 of 11. The deciding prediction G1 passed.**

**G2 (monotonicity) failed.** At concurrency 10 and frequency 0.002, alpha goes from 0.01 to −0.06 between ratios 0.5 and 0.625. Both are effectively zero, and away from zero the sequence is monotone in every condition. The criterion that counts fluctuation around zero as a monotonicity violation is one I wrote. The failure is still recorded as a failure.

**G3 (uniform optimism) failed.** "The alpha boundary is at least 0.04 below the flow-balance boundary" held in only four of six cells; at frequency 0.002 the two nearly coincide. The previous study's exploratory claim, fitted on three windows and five seeds, overstated the gap in the rare-job conditions. A correction band was added as the sealed text required.

**G9 (the censoring coefficient) failed.** The median of 1.602 is inside the sealed band, but the distribution is wider than expected — only 70.7% of 157 cells fell inside. As pre-committed, **the route of converting past results to alpha without remeasuring is abandoned.**

**And two sealed consequences collided.** "If the deciding prediction passes, publish on the new basis" and "if G3 fails, restore the old table's numbers" fired together with opposite instructions.

The resolution: **when a validated statistic is in hand, restoring an unvalidated one is wrong.** The first was executed; from the second, only the correction band. The collision was not foreseen at sealing time because **consequences were written per prediction, without considering combinations.** They should be written per decision — what to publish, what to retract.

## Evidence boundary

**Supported:** inside this synthetic model alpha reads 0 when stable and 1 when divergent, moves the boundary by at most 0.02 over an eightfold window extension, and is precise enough to quote with eight seeds. The table above is the measurement on that basis. EASY backfill converges even for a whole-pool class.

**Not supported:** the validity of the alpha = 0.5 line (a convention); any behaviour on a real trace. One load, one pool size, one service distribution, one background family. `real_prospective_cycle_count` remains 0.

## UNKNOWN

- The sensitivity of the alpha = 0.5 line. Unsealed analysis puts it at ±0.04; it needs sealing and remeasurement.
- Which row of the table a real cluster falls on. **The next study measures it.**
- The U-shape of the frequency effect, and what the background family effect really is.

## Falsification targets

- Adding a still longer window moves the boundary by more than 0.03.
- Moving the decision line reverses the ordering of conditions.
- The truncation from averaging completed jobs only is large enough to change alpha's reading qualitatively.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Full rerun (about 57 minutes):

```bash
cd reproduction/gpu-scheduling-boundary
python run_e14.py
python analyze_e14.py
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-013, including the two consequences that collided](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-013.json)
- [E14 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E14_grading.json)
- Internal source Episode hash: `9f33d6cf645c7273f53984f13ce51ae2bc3b87aaba50ae1df822ed1756755ce6`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Measure the real cluster's frequency. The table splits the safe ratio between 0.92 and 0.72 across the 0.002 and 0.02 rows, so Philly's 11cb48 currently has a margin anywhere from 0.13 to 0.33 — a factor of 2.5. Frequency is measurable from the trace and needs **no new simulation**.

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
  <a class="current" href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012 · current</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
