---
research_id: GPU-SCHED-EP-0017
title: Independent calibration still left two capacity detectors in disagreement
date: 2026-09-16
lang: en
aliases: [/research/gpu-scheduling-u31-calibration/index]
domain: GPU Cluster Scheduling
type: Negative Result
status: Local disagreement; capacity and threshold unresolved
evidence_level: Fixed-grid calibration in a synthetic model
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model-calibration
  source: two fixed controls and an independent grid, 16 balanced/FCFS simulations; the public artifact checks aggregate arithmetic only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: local comparison in a self-authored MSJ model with balanced demand, FCFS, 64 servers, 20k/40k windows, and seeds 111/222
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0017
source_episode_sha256: 5fed9bdcc75af4d353f8bdc34180b6bda087b9fe1ca016208e58a413daa2a213
publication:
  status: publishable
tags: [negative-result, gpu-scheduling, capacity, calibration]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Audit the threshold before calling a number capacity</span><a href="/ja/research/gpu-scheduling-u31-calibration/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Negative Result</span><span>Local synthetic calibration</span><span>Capacity UNKNOWN</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## Current finding

**The alpha=0.5 capacity label and a separately calibrated active-backlog label disagreed at rho=0.85 on a new fixed grid.** Alpha was 0.762, on its growth side; the backlog score was 0.0385, below its predeclared threshold of 0.1187. The runner stopped at that first local disagreement. The planned rho=1.0 grid point was not run.

This does not establish that alpha is wrong or backlog is right. A midpoint threshold drawn from only a low-load and an overloaded control may be too coarse near the transition. **The capacity value, physical meaning of alpha=0.5, and transfer to a real cluster remain UNKNOWN.**

After the last public [[en/research/gpu-scheduling-one-job/index|Research Note (EP-0013)]], internal work measured the low-frequency edge directly and found two defects in calling saturated throughput capacity: truncation and offering all jobs at once, which gives a reordering policy unlimited packing choices. The existing open-arrival bisection output predates independent calibration of its alpha threshold. A later local audit found a backlog-signal disagreement, but its runner continued 12 runs past the sealed stop point. This runner stopped at the first disagreement. These intervening internal records are context, not wholesale public copies.

## Research question

Do alpha, which uses completed-job mean response time, and a backlog score, which uses the number of active unfinished jobs during arrivals, give the same label away from previously saved boundary points?

## Why this matters

A bisection capacity number depends on its detector and threshold. Treating that number as validated before calibrating the detector would turn uncertainty about measurement into unwarranted certainty about capacity.

## Method

We fixed balanced demand, FCFS, and 64 servers in a self-authored synthetic MSJ model. With 20,000/40,000-job windows and seeds 111/222, we ran low-load rho=0.4 and overloaded rho=1.2 controls first. The queue score is the longer-window mean across seeds of the final minus initial backlog-decile means, divided by 40,000 arrivals. If the controls meet predeclared separation conditions, their score midpoint becomes the threshold. Alpha is the log ratio of mean response times across the two windows; its comparison line remains the historical 0.5.

The grid rho=0.7, 0.85, 1.0 was fixed in that order before this run. The contract stops after each four-run cell on missing observations, an abort, or the first nonambiguous label disagreement. It excludes the previously saved boundary points and seeds. The design was made after an earlier failure, however, so it is neither external independent replication nor a prospective capacity prediction.

## Results

| Role | rho | Alpha | Backlog score | Alpha / backlog labels |
|---|---:|---:|---:|---|
| Low-load control | 0.40 | −0.0590 | −0.000004 | Used for calibration |
| Overloaded control | 1.20 | 0.9267 | 0.237447 | Used for calibration |
| Independent grid | 0.70 | −0.2291 | 0.000003 | No growth / no growth |
| Independent grid | 0.85 | 0.7622 | 0.038523 | **Growth / no growth** |

The control midpoint was 0.118722. Rho=0.85 triggered **R2 local-disagreement** and the runner stopped after 16 of at most 20 simulations. All required measurements in those 16 runs were finite; there were no backlog-cap aborts, time-limit hits, or right-censoring flags. Those observations establish that the fixed audit ran as recorded, not physical stability.

## What changed

We held back any adoption of the open-arrival bisection value as validated capacity. The next task is to separate transition-region control calibration from a holdout grid. Earlier values remain dated, model-conditional results made with a threshold that has not passed this independent audit.

## What failed

The two detectors did not agree at one point on the independent grid. There is no guarantee that a midpoint between extreme-load controls is a physically meaningful threshold in the transition region. The earlier stop-rule breach did not recur in this run.

## Evidence boundary

**Shows:** under the fixed synthetic model, window, seeds, and FCFS policy, alpha=0.5 and this control-derived backlog threshold put rho=0.85 on opposite sides; execution stopped at the first disagreement.

**Does not show:** a physical refutation of alpha, validation of the backlog detector, a bisection capacity value, other policies or demand mixes, real-cluster performance, or independent replication. The public package contains aggregate arithmetic and the stop branch, not raw runs or simulator source.

## UNKNOWN

- Can stable and unstable controls near the transition be checked using evidence other than finite-window backlog itself?
- Does the disagreement survive alpha lines 0.3/0.5/0.7, longer windows, other seeds, and a censoring-aware drift statistic?
- What evidence grade, if any, can the open-arrival capacity value support?

## Falsification targets

If the public control midpoint or labels cannot be recalculated, withdraw this Note's arithmetic claim. A newly sealed transition calibration might reconcile the detectors; that would narrow the reach of this fixed audit without erasing what it observed.

## Reproduce

Only the public aggregates, threshold, labels, and stop branch can be checked. **This does not rerun the simulation.**

```bash
python reproduction/gpu-scheduling-u31/verify_summary.py
```

## Evidence / Artifacts

- [Bounded public aggregate and verifier](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31)
- Private source Episode SHA-256: `5fed9bdcc75af4d353f8bdc34180b6bda087b9fe1ca016208e58a413daa2a213`. It identifies a source record, not a seal of scientific validity.

## External audit

There are zero independent replications and no peer review. No post-publication external audit has yet been recorded.

## Next experiment

Before observing new results, fix independent grounds for transition-region controls, separate calibration from a holdout grid, include the 40k/80k windows and other seeds, test alpha lines 0.3/0.5/0.7, specify missingness under censoring, and statically check that the runner stops at the first R2/R3. Stop at UNKNOWN if the controls or observations do not qualify. A full independent rerun of the existing 18 bisection cells and real-cluster validation are separate gates.
