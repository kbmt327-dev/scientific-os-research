---
research_id: GPU-SCHED-EP-0011
title: The detector was not measuring divergence. It divided by the window, so it never moved
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
  source: one sealed prediction (PRED-012, 9 of 11), a 648-run audit across three observation windows and three decision lines, and a continuous remeasurement of two past experiments
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 256-server synthetic multiserver-job model, rho 0.85, exponential service, no restart cost, a single background distribution family
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0011
source_episode_sha256: ce69ff0e09f54ff06c694be8bab700ee9faaedbe553ff53e3ff6a04facd944ca
publication:
  status: publishable
tags: [finding, scheduling, simulation, instrument-defect, retraction]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-blind-detector/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

> [!warning] Correction band (from the next study)
> The statement below that "the correct detector puts the boundary 0.054 to 0.157 lower" is **overstated**. [[en/research/gpu-scheduling-alpha-boundary/index|EP-0012]] measured it under seal across four observation windows and eight seeds: the gap varies sharply by condition. **At a frequency of 0.002 the two nearly coincide** (−0.003 at concurrency 10). The ~0.15 gaps appear only on the 0.02 side. "The operational table errs optimistic" was also one-sided: the old table was **conservative by 0.04–0.11 for rare large jobs and dangerous by up to 0.16 for frequent ones** — the errors did not share a direction. The body below is left unchanged.

## Current finding

The previous study established that every operational number in this domain is a function of one unvalidated detector: whether the large class's flow balance — completions inside the observation window divided by arrivals inside it — is at or above 0.9. That constant was placed seven studies earlier and carried forward unchanged.

We audited it. **The boundary turns out to be almost invariant to the observation window** — quadrupling it moves the boundary by only 0.006 to 0.021.

**And the reason for that invariance is the problem.**

Flow balance is not a stability indicator. It is a **right-censoring ratio**: mean response time divided by the observation window. With stationary arrivals it follows with no free parameter:

```
1 - flow balance = E[min(response time, W)] / W
```

`W` is proportional to the observation length. **So is the response time of a diverging class.** Numerator and denominator grow together, so the ratio does not move.

The measured values:

| Observation window | Mean response time of the large class | Flow balance |
|---|---|---|
| 30,000 jobs | 611 | 0.562 |
| 60,000 | 1,230 | 0.562 |
| 120,000 | 2,357 | 0.574 |

**While the response time grew 3.9×, the detector moved from 0.562 to 0.574.**

**A statistic normalised by the observation window being insensitive to the horizon is not evidence that it is robust.** It can equally be evidence that the divergence is being divided away.

And this domain had learned exactly that lesson seven studies earlier. In [[en/research/gpu-scheduling-phase-diagram/index|EP-0002]] three stability detectors failed in a row, and the conclusion was that stability cannot be judged from a single window with a single metric. The lesson was even moved into calibration code. **What it was moved into did not include this detector.**

## Key figure

<div class="ratio-figure" aria-label="two quantities as the observation window grows"><div class="ratio-track"><i style="left:15%"></i><i style="left:60%"></i></div><div class="ratio-labels"><span style="left:15%"><b>×1</b> window 30k<br>wait 611 / detector 0.562</span><span style="left:60%"><b>×3.9</b> window 120k<br>wait 2,357 / detector 0.574</span></div></div>

Quadruple the observation window and the response time rises 3.9×. The detector barely moves, because both quantities scale with the window.

## What this research shows

- Flow balance is a censoring ratio. `(1 − fb)` correlates with `mean response time / window length` at 0.974, with a near-constant factor of 1.76 across 36 cells.
- **It therefore cannot detect divergence.** While the response time grows 3.9×, its value moves only from 0.562 to 0.574.
- The qualitative structure survives changing the detector. The ordering "higher concurrency means a lower safe ratio" held across three windows × three decision lines × two frequencies.
- A boundary read off a grid is systematically conservative relative to the continuous one (all six past rows, mean 0.040).
- In the experiment that produced the operational table, **the large class had only 42 arrivals per run.** The detector's resolution, pooled over four seeds, is 0.0059. The published margin was +0.0006 — **a tenth of one job.**

## What this research does not show

- The validity of the replacement statistic is not tested under seal here. **The next study does that.**
- "How much lower the correct detector puts the boundary" is exploratory, unsealed analysis, and was overstated (see the correction band above).
- No scheduling policy was run on a real arrival stream.

## Why this matters

Completion rate, attainment rate, coverage, in-window success rate, SLA compliance — all have the form *numerator inside the window over denominator inside the window*. **A metric of that shape cancels the phenomenon you are trying to see whenever that phenomenon grows at the same rate as the window.** And the cancellation shows up in the reassuring form of a metric that stays stable when conditions change.

The value of this study is not in the queueing numbers but in the detection of that shape. **Before using a ratio-shaped metric, write one line about what its denominator is proportional to.** If it is proportional to the observation window, the observation period, or the size of the population observed, do not put a threshold on its level. What carries the signal is how it approaches its limit.

## Research question

1. Does the boundary depend on the observation window?
2. Does moving the decision line preserve the ordering of conditions?
3. How far off are the previously published boundaries when remeasured continuously?

## Method

**Window arm.** 7 ratios × 3 concurrency levels × 2 frequencies × 3 observation windows (30,000 / 60,000 / 120,000 jobs) × 5 seeds — 630 runs. The 30,000 rows double as an exact replay gate against the previous study; **210 rows reproduced at difference 0**.

**Decision-line and past-remeasurement arms** required no new runs: existing results are reread at lines 0.8 / 0.9 / 0.95 and by continuous interpolation.

648 runs. Sealed as PRED-012 with SHA-256 `9fc35c5b761923e7b9ff019df77e6145cf4d3e8561267b7be3b9196005efe8fa`, committed while no corresponding result file existed.

## Results

**The boundary is nearly invariant to the window.**

| Concurrency | Frequency | 30k | 60k | 120k | Change |
|---|---|---|---|---|---|
| 9.98 | 0.002 | 0.8994 | 0.9100 | 0.9148 | +0.0154 |
| 14.96 | 0.002 | 0.8766 | 0.8842 | 0.8880 | +0.0115 |
| 29.93 | 0.002 | 0.7814 | 0.7930 | 0.8019 | +0.0204 |

The direction was right in 6 of 6, but three of four cases fell short of the sealed +0.02 threshold, so the deciding prediction failed. **The observation window is the smallest of the nuisance factors measured so far.** The decision line moves the boundary by 0.05–0.14, the background family by 0.10, frequency by 0.05.

**All the qualitative structure survived.** The concurrency ordering held across three windows × two frequencies, and across three decision lines × two windows.

**Grid rounding is a real systematic bias.** All six rows of the past concurrency curve read higher on the continuous statistic, mean difference 0.040. The shape of that curve, and the past pool-size trend, both survive continuous remeasurement.

## What changed

- Flow balance was **demoted from being a stability indicator**. A threshold on its level was a threshold on a quantity whose level carries no meaning.
- The operational numbers were put on **hold**. No replacement figures were published from post-hoc evidence; they are remeasured under seal in the next study.
- A detector registry was implemented as a calibration test: every detector that turns a measurement into a verdict is enumerated with its threshold and audit status, and the build fails when a new threshold appears in a new analysis script.

## What failed

**PRED-012 scored 9 of 11. The deciding prediction D1 failed.**

**And part of the sealed consequence was not executed.** It contained the inference "if the boundary is invariant to the window, the detector is valid" — an inference the unsealed analysis refuted.

The sealed document's `measurand_validity` field had said that exceeding a threshold in a finite window is not proof of stability. **Having written that, the consequence was still tied to a test that cannot detect the danger.** The correct test — whether mean response time grows with the window — was never sealed.

**Writing down a concern and placing a bet on it are two different pieces of work.**

**The moment the detector was swapped can be dated.** Counting how many observation windows each experiment recorded, [[en/research/gpu-scheduling-real-traces/index|EP-0004]] is the branch point. That experiment recorded two windows and used the correct detector to confirm, and correctly predict, that a whole-pool class diverges. **And then drew the boundary itself, in the same experiment, from a single-window threshold.** From the next experiment onward, a second window was not recorded again for six studies.

The correct detector was used on one expensive point; the cheap threshold was used on everything; the cheap one became the headline.

**There is a fourth problem.** In the experiment that produced the operational table, the large class had only 42 arrivals per run. The detector's resolution is 1/42 = 0.024, or 0.0059 pooled over four seeds. Converted, the published margins were **0.10 of one job** at concurrency 9.8 and **1.08 jobs** at 14.6.

The published operational table had four independent causes stacked in it: **sample size, grid rounding, the decision line, and the statistic itself. Three of the four were detectable before publication.**

## Evidence boundary

**Supported:** flow balance is a censoring ratio and cannot detect divergence. The boundary's window dependence is small. The decision line and the grid matter a great deal. The qualitative ordering survives a change of detector.

**Not supported:** the validity of the replacement statistic (next study); the size of the boundary gap, per the correction band; any behaviour on a real trace.

## UNKNOWN

- Whether the replacement statistic gives a boundary that stops moving when a window is added.
- Whether the censoring coefficient of 1.76 can be derived. If so, past results could be converted without remeasurement.
- The U-shape of the frequency effect, and what the background family effect really is.

## Falsification targets

- The relation between `(1 − fb)` and `response time / window` breaks at a different load or pool size.
- The replacement statistic's boundary also keeps moving with the window. Then no finite-window statistic has a fixed point here.
- The ordering of conditions changes with the choice of detector.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Beyond verifying the sealed digests, this quick check re-derives from the stored results that **the detector stayed flat while the response time grew 3.9×**.

The detector registry:

```bash
cd reproduction/gpu-scheduling-boundary
python calib/c07_detector_registry.py
python calib/c07_detector_registry.py --selftest
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-012, including the consequence that was not executed](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-012.json)
- [E13 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E13_grading.json)
- [Detector registry](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/calib/c07_detector_registry.py)
- Internal source Episode hash: `ce69ff0e09f54ff06c694be8bab700ee9faaedbe553ff53e3ff6a04facd944ca`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Measure the replacement candidate — the elasticity of mean response time with respect to the observation window — as a sealed primary statistic. Four windows, eight seeds, and a deciding prediction on **whether adding one more window moves the boundary**. If it does not, the numbers come back; if it does, no finite-window statistic has a fixed point here.

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
  <a class="current" href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011 · current</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
