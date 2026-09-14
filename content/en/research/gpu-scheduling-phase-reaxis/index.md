---
research_id: GPU-SCHED-EP-0009
title: The axis of the flagship phase diagram was confounded by a factor of 18
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
  source: one sealed prediction (PRED-010, 7 of 7), an exact 210-run replay of the old phase diagram and a 90-run equal-summary control, 300 runs total
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 64-server synthetic multiserver-job model at rho 0.7 / 0.85 / 0.95, exponential service, no restart cost
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0009
source_episode_sha256: a2c4be8afc557a71ba447773163d0fcf512d15181a8b235720fc3048b629c6d2
publication:
  status: publishable
tags: [finding, scheduling, simulation, confounding]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-phase-reaxis/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## Current finding

The 21-cell phase diagram from [[en/research/gpu-scheduling-phase-diagram/index|EP-0002]] was this project's flagship result: a map, over demand-mix parameter θ and load rho, of which policy breaks where.

After the previous study broke the headline result, the same suspicion fell on the diagram. **Does varying θ also vary concurrency?**

It does. **Moving θ from 0.4 to 2.0 divides concurrency by about 18 at every load.** θ was not only changing the shape of the demand mix; it moved mean gang size from 2.37 to 43, and with it the arrival rate and the concurrency, by a factor of 18.

Under the sealed starvation detector, starved cells ran at concurrency 18.95 to 25.71 and non-starved cells at 1.05 to 11.33 — **no overlap**. Reading the old diagram's starvation boundary as a θ effect is therefore **retracted**.

The diagram is not discarded. It is **read in two layers**:

1. **A stability layer.** Which class starves is organised by maximum job ratio and concurrency. θ was a proxy here.
2. **A conditional ranking layer.** Among cells where every policy is healthy, the ranking of mean response times still carries gang-size heterogeneity. The result that greedy SRPT beats ServerFilling by 7–17% on homogeneous large-gang workloads (high θ, rho 0.7) stands as it was.

## Key figure

<div class="ratio-figure" aria-label="the old theta axis against concurrency"><div class="ratio-track"><i style="left:5%"></i><i style="left:95%"></i></div><div class="ratio-labels"><span style="left:5%"><b>θ=2.0</b><br>concurrency 1.05–1.42</span><span style="left:95%"><b>θ=0.4</b><br>concurrency 19.0–25.8</span></div></div>

The old diagram's horizontal axis was also, unlabelled, a concurrency axis — about 18× end to end. Starvation is concentrated at the high-concurrency end.

## What this research shows

- The old diagram's θ axis moved concurrency by 18.1–18.2× at every load.
- Starved and non-starved cells separate on concurrency with no overlap (18.95–25.71 against 1.05–11.33).
- Holding maximum job ratio, its frequency, mean gang size and load fixed, and changing **only the shape** of the background distribution across three forms, left the starvation verdict unchanged.
- The 210 runs of the old diagram reproduced with a maximum absolute difference of **0** on every retained metric.

## What this research does not show

- It does not show that two numbers settle the **ranking of mean response times** between policies. The claim is about the stability layer.
- The control groups hold the largest class's frequency fixed within each group, so this does not establish that frequency is not a third variable. The next study tests that, and **finds that it is**.
- The statistic used to judge starvation was later shown to be invalid. The separation here has zero overlap, so this conclusion does not depend on where the line is drawn.

## Why this matters

A phase diagram is read to decide which policy to use under which conditions. If the horizontal axis is understood as the shape of the demand mix, an operator who cannot change their demand mix sees no lever.

If the effective variable is concurrency, there is a lever: how many jobs run at once is something operations can adjust. **A mislabelled axis hides the action available to the reader.**

## Research question

1. Is the old diagram's θ axis confounded with concurrency?
2. If so, do starved and non-starved cells separate on the new axis?
3. With maximum job ratio and concurrency matched, is the starvation verdict invariant to the shape of the background distribution?

## Method

**Replay arm.** Rerun the greedy-SRPT and ServerFilling-SRPT half of the old diagram — 210 runs — at identical seeds and settings. Confirm the old metrics reproduce exactly before reading the newly retained concurrency.

**Equal-summary control arm.** At 64 servers and rho 0.85, hold the maximum job ratio, its probability, mean gang size and arrival rate fixed within a group, and vary only the background shape across narrow / geometric / wide. Two groups, at mean gang size 4 (expected concurrency 13.6) and 16 (3.4). 90 runs.

Sealed as PRED-010 with SHA-256 `c68cbf56b09da9dfe5a6c1493836979bda716c642dab8788834cbc54d7a741ea`, committed while no corresponding result file existed.

The deciding prediction Y4 — "matching two numbers keeps the verdict invariant across background shapes" — was named **on the side where the then-current working hypothesis could be falsified**.

## Results

**The old θ axis was confounded with concurrency by a factor of 18.**

| Load | θ=0.4 | 0.8 | 1.25 | 2.0 | End ratio |
|---|---|---|---|---|---|
| 0.70 | 19.00 | 4.14 | 1.67 | 1.05 | 18.1× |
| 0.85 | 23.03 | 5.02 | 2.03 | 1.27 | 18.1× |
| 0.95 | 25.84 | 5.62 | 2.27 | 1.42 | 18.2× |

Strictly monotone at every load.

**Starved and non-starved cells separate.** Starved cells run at concurrency 18.95–25.71, non-starved at 1.05–11.33. No overlap.

**Changing the background shape did not change the verdict.**

| Group | Background shape | Concurrency | Flow of the large class | Verdict |
|---|---|---|---|---|
| High concurrency | narrow / geometric / wide | 13.366 / 13.366 / 13.367 | 0.460 / 0.460 / 0.458 | all starved |
| Low concurrency | narrow / geometric / wide | 3.268 / 3.259 / 3.222 | 0.870 / 0.858 / 0.831 | all healthy |

The within-group flow range is at most 0.040, inside the sealed tolerance of 0.15.

**The old diagram reproduced at difference 0.** Across all 210 runs, the maximum absolute difference on mean response time, utilisation, empirical load and flow balance was zero.

## What changed

- Reading the diagram's **starvation boundary as a θ effect was retracted**, and the boundary was placed on the maximum-ratio and concurrency axes.
- The diagram was split from one picture into **two layers**: stability, and conditional ranking.
- The conditional-ranking result — greedy SRPT beating ServerFilling by 7–17% on homogeneous large-gang workloads — was **retained**.

## What failed

**PRED-010 scored 7 of 7.**

The failure worth recording is again in the past. **Nobody checked whether the flagship result's axis was confounded, across seven studies.** The parameter was named for the shape of the demand mix, so it was assumed to change only the shape. In fact it moved mean gang size by 18× and, to hold load constant, divided the arrival rate by 18 as well.

**The name of a parameter is not evidence about what that parameter moves.**

One observation is left exploratory: in the low-concurrency control group, greedy SRPT's mean response time varied from 55.1 to 79.7 with the background shape. No direction was sealed for it.

## Evidence boundary

**Supported:** the old diagram's θ axis is strongly confounded with concurrency, and the starvation boundary separates on that new axis. Within the range examined, matching maximum job ratio and concurrency gives the same starvation verdict regardless of background shape.

**Not supported:** that two numbers settle the ranking of mean response times; that the largest class's frequency is not a third variable (the next study finds it is); any behaviour on a real trace.

## UNKNOWN

- Whether the two-variable account survives when frequency, ratio and concurrency are varied fully independently.
- Why mean response time varied with background shape in the low-concurrency control group.
- The size of the heterogeneity effect that remains in the conditional ranking layer.

## Falsification targets

- With concurrency and maximum ratio matched, changing only the largest class's frequency flips the starvation verdict. **Something close to this happens in the next study.**
- A condition is found where starved and non-starved cells overlap on concurrency.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Full rerun:

```bash
cd reproduction/gpu-scheduling-boundary
python run_e11.py
python analyze_e11.py
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-010](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-010.json)
- [E11 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E11_grading.json)
- Internal source Episode hash: `a2c4be8afc557a71ba447773163d0fcf512d15181a8b235720fc3048b629c6d2`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Build an experiment that manipulates maximum job ratio, its frequency and concurrency fully independently. This study held frequency fixed within each group, so the sufficiency of the two-variable account is still untested.

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
  <a class="current" href="/en/research/gpu-scheduling-phase-reaxis/"><b>EP-0009 · current</b><span>The axis of the flagship phase diagram was confounded by a factor of 18.</span></a>
  <a href="/en/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>Retracted \"two numbers decide this\". Frequency is a third variable.</span></a>
  <a href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
