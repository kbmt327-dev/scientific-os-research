---
research_id: GPU-SCHED-EP-0020
title: Input confidence intervals transferred to a fixed-need four-slot control
date: '2026-09-17'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Bounded transfer PASS; novelty unestablished
evidence_level: Synthetic known-model controls
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: 30 input/oracle workloads, 10 CI looks and 4 native alignment fixtures;
    public aggregate arithmetic only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Synthetic homogeneous 64-server FCFS; every job requires 16 servers;
  four fungible slots; independent iid exponential gaps and true service work; no
  mixed-need capacity, real-cluster performance, diagnostic-superiority or established
  manuscript novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0020
source_episode_sha256: b5ebff918c1d35c67298f7c8ef2c649a7227389dc4f7d89f0c5f0b1f5128209f
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- en
aliases:
- /research/gpu-scheduling-mmc-transfer/index
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Known controls and manuscript preparation</span><a href="/ja/research/gpu-scheduling-mmc-transfer/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic known model</span><span>General capacity UNKNOWN</span><span>Novelty unestablished</span><span>Independent replications 0</span></div>

## Current finding

**The input CI transferred to a fixed-need four-slot control and resolved two control cells and four holdout cells on the correct side.** Load 1.01 required 160k arrivals per seed across three seeds. Four native-engine alignment fixtures had a maximum individual departure difference of about 8.9e-16.

This is bounded known-model acceptance. U-31 and mixed-need capacity remain UNKNOWN; validated general detectors remain zero. A technical-report draft has been prepared, with novelty for a peer-reviewed paper still unestablished.

## Key figure

![Known-control input-load confidence intervals](/assets/gpu-scheduling-mmc-transfer-ci.png)

Left: final intervals for this M/M/4 study. Right: intervals at each look for M/M/1 load 1.005 from [[en/research/gpu-scheduling-drift-uncertainty/index|EP-0019]]. Points are estimates; the dashed line is load 1. Each H is arrivals per seed, with three seeds pooled. Seeds, error allocation and maximum windows differ between panels, so they do not compare the effects of parallelism.

## What this research shows

With homogeneous 64 resources and exactly 16 required by every job, nonpreemptive FCFS maps to four identical slots. This supplies analytic known labels and an implementation alignment path. The input CI uses explicit capacity four.

## What this research does not show

Mixed-need packing/HOL, heterogeneous servers, locality, estimated work and non-exponential inputs were not validated. M/M/c load conditions and the F interval are established results; no new statistical theorem or general stability detector is claimed.

## Research question

Do the mechanism, observation requirements and native-engine alignment permit transfer of the full-gang M/M/1 input CI to a fixed-need control running four jobs concurrently?

## Why this matters

Agreement between diagnostics does not supply ground truth. Analytic labels independent of the classifier and a distinct execution path constrain the interpretation.

## Method

Homogeneous 64 resources, speed one, need=16 for every job, nonpreemptive FCFS, independent iid exponential arrival gaps and service durations. With c=4, rho=lambda E[S]/4. Fixed need removes mixed-demand packing loss. Applying the established [M/M/c load condition](https://homepages.ecs.vuw.ac.nz/~schukova/SCIE201/Lectures/Lecture9_10_final.html) to this mechanism is an inference under these assumptions.

Controls were rho=0.8/1.2, seeds 901/902/903; holdouts were 0.95/1.05/0.99/1.01, seeds 1001/1002/1003. Fixed horizons were 20k/40k/80k/160k. A family error of .05 was allocated over 24 potential looks before execution.

Pool all offered true service B and full gap time T. R=B/(4T), n=3H. Under the independent exponential assumptions, R/rho follows F(2n,2n), giving CI=[R/q_high,R/q_low]; see the [official F distribution description](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html). Upper<1 declares subcritical, lower>1 overloaded, otherwise UNKNOWN. Intermediate UNKNOWN advances only to the next fixed look; resolved cells cease expansion. The first wrong side stops with R2; maximum-window UNKNOWN, missing data or engine misalignment stops with R3.

A heap-based FCFS slot recurrence and the native event engine were aligned on individual departures and JCT in four H1000 fixtures. They share the generator, so this is not independent replication.

## Results

| Role | rho | Resolving H/seed | Load CI | Label |
|---|---:|---:|---|---|
| calibration | 0.80 | 20,000 | [0.783941, 0.812306] | subcritical |
| calibration | 1.20 | 20,000 | [1.175912, 1.218459] | overloaded |
| holdout | 0.95 | 20,000 | [0.933258, 0.967025] | subcritical |
| holdout | 1.05 | 20,000 | [1.031495, 1.068817] | overloaded |
| holdout | 0.99 | 40,000 | [0.974896, 0.999708] | subcritical |
| holdout | 1.01 | 160,000 | [1.005608, 1.018324] | overloaded |


Six cells resolved correctly over 30 workloads and 10 looks, with zero wrong declarations in this run. This is an observed count, not empirical coverage validation. The model-conditional 5% family budget is not a real-cluster error rate.

## What changed

Known controls now include four slots as well as one slot. A technical-report draft, claim/evidence matrix and comparison design were prepared. This methodology branch is separate from the original scheduler-ranking question.

Future comparisons separate information and actual time cutoffs. Tier O uses arrivals/departures/system count available by cutoff; W adds all offered true work and known capacity; D uses cohort JCT after future draining. This CI uses W. Matching arrival counts alone does not equalize extra work information or later observation end times.

## What failed

The initial attempt stopped during controls because a result snapshot could not be saved. Its failure record was retained. Only bounded persistence retry was added, then the same grid, seeds, decision formula and error budget were resealed for recovery. Controls were previously observed; holdouts had not run in the initial attempt. This is a recovery rerun rather than a wholly untouched independent study.

## Evidence boundary

Synthetic fixed-need M/M/4 only: independent exponential inputs, true required service including unfinished jobs, and mechanism capacity four. The seal uses local hashes/time. Adaptive stopping leaves unequal windows for early-resolved cells; no systematic alpha comparison was performed.

The public artifact contains pooled sufficient statistics and CI/stopping/alignment summaries. Generator, simulator, private manuscript/work state and raw job sequences are excluded.

## UNKNOWN

Whether a comparison with existing stability checks under matching information and actual time cutoffs produces additional knowledge. How to obtain independent labels for mixed need or handle unknown true work. Novelty for a peer-reviewed paper remains unestablished.

## Falsification targets

Withdraw the transfer description if sufficient statistics, intervals or resolving horizons cannot be recomputed, or if native alignment evidence fails. Do not apply the error bound where fixed need, exponentiality, independence or capacity assumptions fail.

## Reproduce

```bash
python reproduction/gpu-scheduling-u31-controls/verify_mmc_summary.py
```

SciPy is required. The verifier checks projected arithmetic and recorded stopping/alignment summaries; it cannot execute or independently audit the omitted engine.

## Evidence / Artifacts

[Public sufficient statistics and verifier](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-controls). Internal Episode SHA-256: `b5ebff918c1d35c67298f7c8ef2c649a7227389dc4f7d89f0c5f0b1f5128209f`.

## External audit

Independent replications zero; peer reviews zero. Internal checks covered source/seal hashes, timestamp ordering, quantile-CDF roundtrips, all ten looks, stopping and rejection of modified/unsupported mechanisms. Editorial/privacy review is separate from scientific review.

## Next experiment

Fix primary-source algorithm specifications, O/W/D information tiers, a common actual time cutoff, independent known labels, repeated wrong-declaration/UNKNOWN/cost evaluation and an executable public artifact before a separate seal. Missing specifications or labels mean unexecuted/UNKNOWN. If comparisons provide no novelty gap, complete a technical report rather than continuing calibration indefinitely.


Later comparisons and the two-class control: [[en/research/gpu-scheduling-two-class-control/index|EP-0023]]。
