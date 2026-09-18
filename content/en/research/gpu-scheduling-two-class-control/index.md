---
research_id: GPU-SCHED-EP-0023
title: Two-class FCFS overload below nominal resource load one
date: '2026-09-19'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Bounded synthetic benchmark; general claims UNKNOWN
evidence_level: Synthetic known-model control
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: Sealed aggregate seed-level outcomes and same-model executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known synthetic FCFS models only; information tiers differ; no general
  detector, real-cluster effect or established manuscript novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0023
source_episode_sha256: e22560bf6d10d8488984a3fb6bde48acf42e76df2975558f4745c4fb5cd3c218
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- en
aliases:
- /research/gpu-scheduling-two-class-control/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-two-class-control/" hreflang="ja">日本語</a></p>

## Current finding

**We constructed a small mixed-need control with capacity independent of the diagnostics.** The model has 64 homogeneous resources, needs 32/64 with probability 1/2 each, exponential class service rates 1/.5, Poisson arrivals and strict nonpreemptive FCFS. Normalizing 32 resources to one block, a five-state exact CTMC gives capacity X=8/11 jobs/time, mean block work 5/2 and nominal-load boundary 10/11.

Labels follow [Grosof et al.'s two-class stability theorem](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf), Theorems 4.2/4.3, under its assumptions. We score lambda<X and lambda>X, excluding equality. Exact stationary balance, embedded-chain time weights and work flow agree. This is a known-theorem small-instance construction, not new theory or general mixed-need capacity.

100 independent seeds 8001-8100, five effective loads, two nested windows and four methods produced **4,000 decisions from 500 workloads**. All five sealed predictions passed. Effective load z=lambda/X has nominal load(10/11)z; z 1.01/1.05 are overloaded below nominal load one.

## Key figure

![Wrong-side rates at 20k and K abstention at 20k/80k,100 seeds per cell, simultaneous CP intervals over 80 rates. Information contracts differ.](/assets/gpu-scheduling-two-class-control.png)

Wrong-side rates at 20k and K abstention at 20k/80k,100 seeds per cell, simultaneous CP intervals over 80 rates. Information contracts differ.

## What this research shows

Finite-window wrong-side and UNKNOWN rates can be measured separately against independent known-model labels, with information costs stated.

## What this research does not show

No general GPU guarantee, new capacity theorem, real-cluster effect, universal ranking or peer-reviewed paper is established.

## Research question

Can an independent two-class capacity expose nominal-work misses and finite-window diagnostic errors?

## Why this matters

A finite-window declaration needs explicit information and error/abstention costs before it can support a long-term stability claim.

## Method

O_AB sees arrivals/departures through cutoff. D_ALPHA uses future-drained JCT elasticity for H/2 versus H with 20% warmup and threshold.5. K_EXACT additionally knows population class probabilities, service rates and exact capacity; it compares a chi-square 95% arrival-rate interval to X. No F-work interval is transferred to the mixture. NOMINAL_WORK is a binary control ignoring HOL. Privileged known parameters prevent a cross-information superiority claim.

Loss L(a)=e+a u uses fixed prices.1/.5/.9. O/K crossover at z.99/20k is.125 with conservative simultaneous range[-.066,.413]; at 1.01/20k it is 1.014 with range[.562,1.576]. Point crossovers do not establish rankings. Online expected-loss recommendations for unknown truth require an applicable calibration distribution; otherwise UNKNOWN.

## Results

| z | H | O wrong/UNKNOWN | D wrong/UNKNOWN | K wrong/UNKNOWN | Nominal wrong/UNKNOWN |
|---:|---:|---:|---:|---:|---:|
| 0.8 | 20k | 1/0 | 0/0 | 0/0 | 0/0 |
| 0.8 | 80k | 2/0 | 0/0 | 0/0 | 0/0 |
| 0.99 | 20k | 9/0 | 34/0 | 0/72 | 0/0 |
| 0.99 | 80k | 11/0 | 37/0 | 0/17 | 0/0 |
| 1.01 | 20k | 73/0 | 44/0 | 0/72 | 100/0 |
| 1.01 | 80k | 54/0 | 24/0 | 0/21 | 100/0 |
| 1.05 | 20k | 9/0 | 1/0 | 0/0 | 100/0 |
| 1.05 | 80k | 0/0 | 0/0 | 0/0 | 100/0 |
| 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 |
| 1.2 | 80k | 0/0 | 0/0 | 0/0 | 0/0 |

Each cell has 100 seeds. UNKNOWN is not correct. NOMINAL_WORK missed overload in 100/100 runs in all four 1.01/1.05 cells. K had zero wrong-side decisions but 72 UNKNOWN in both near-boundary 20k cells. The simultaneous CP upper bound for 0/100 wrong is.07754 across 80 rate intervals.

## What changed

[Code,1000 seed-look records and instructions](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-two-class-control) regenerate inputs and FCFS and execute capacity, diagnostics, intervals and losses. Recorded native alignment had zero departure error in four fixtures, but the public package does not include the private native engine. Same-design/code execution is not external independent replication.

v 10 failed tuple/list representation preflight before fixture/grid observation; v 11 normalized representation and re-sealed unchanged model/seeds/predictions. Local clocks/hashes are not authenticated external timestamps.

The technical-report draft is version 0.3, with corrections to estimands, price scope and coin comparisons. **General U-31/c 12, real clusters, manuscript novelty and acceptance remain UNKNOWN; validated general detectors remain zero.** Next: narrow the useful contribution and assess execution by a separate environment/reader.

## What failed

v 10 failed representation preflight before observation; v 11 changed representation only and re-sealed.

## Evidence boundary

Synthetic known models, local seals and same-design/generator execution only. Recorded native alignment differs from public oracle re-execution.

## UNKNOWN

General U-31/c 12 capacity, real clusters, operational benefit, external independent replication, novelty and acceptance. Validated general detectors=0.

## Falsification targets

Invalid theorem mapping, source hashes, population assumptions, individual departure alignment or arithmetic aggregation invalidate these control claims; return UNKNOWN.

## Reproduce

[Re-execution instructions and code](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-two-class-control) regenerate inputs from seeds and compare with records.

## Evidence / Artifacts

[Public artifacts](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-two-class-control); source Episode hashes appear in frontmatter. Private sources and personal paths are excluded.

## External audit

Independent replications=0. Scientific, domain-expert and peer review are unperformed. Editorial and arithmetic checks are not independent scientific audits.

## Next experiment

Narrow the useful contribution against prior work and assess another environment/reader execution. Broader models need another contract; original scheduler rankings/capacities remain suspended.

[[en/research/gpu-scheduling-information-tiers/index|EP-0021]] · [[en/research/gpu-scheduling-critical-loss/index|EP-0022]] · [[en/research/gpu-scheduling-two-class-control/index|EP-0023]]
