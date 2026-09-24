---
research_id: GPU-SCHED-EP-0029
title: Does node fragmentation reorder size-first policies against FCFS and backfill?
date: '2026-09-25'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Sealed prediction failed (1/6); low power; post-hoc pattern unconfirmed
evidence_level: Sealed synthetic sweep, single model
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: 768-run MSJ simulation sweep graded by a sealed script (PRED-017)
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic MSJ model, 64 GPUs in 8-GPU nodes, loads 0.6 and 0.7,
  multiplicative fragmentation penalty; no real cluster claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0029
source_episode_sha256: 88e85fe7c39894030467205bc28b547382a841a13153f050bc477821522dc8cd
publication:
  status: publishable
tags:
- gpu-scheduling
- locality
- sealed-prediction
- en
aliases:
- /research/gpu-scheduling-locality/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-locality/" hreflang="ja">日本語</a></p>

## Current finding

In a model where a gang slows down when it spans extra nodes, we tested whether the ranking of four policies changes. Only one of six sealed predictions held, and the decision prediction (a ranking reversal occurs) failed: zero reversals. The test had little power. In one of the two job mixes fragmentation cannot occur by construction, and at the strongest penalty nearly every cell diverged.

## Key figure

![Mean-JCT degradation factor on trace_like, by policy, log scale](/assets/gpu-scheduling-locality.svg)

Mean JCT relative to pi = 0. The figure was made after seeing the results and is not a sealed test.

## What this research shows

- In this model at loads 0.6 and 0.7, no case was found where fragmentation reorders the policies. As committed in advance, locality is recorded as a level effect, not a ranking friction.
- The gang_heavy mix (needs 8/16/32/64) never fragments. Every need is a multiple of the node size, so under first-fit the free servers are always whole nodes and every gang lands on the minimum number of nodes. All 384 runs spanned zero excess nodes, and the eight pi x placement variants of each run gave bit-identical mean JCT.
- Post hoc, on the trace_like mix, degradation ordered srpt < sf_srpt < easy_backfill < fcfs in all eight rows. Size-first policies were more robust to fragmentation; the ranking widened rather than reversed.

## What this research does not show

The degradation order was noticed after seeing the results, on the same seeds; it is not confirmed. Nothing here speaks to real clusters, real communication costs, network topology, migration or locality-aware admission. That fragmentation hurts and consolidation helps is known (Tiresias, the Philly analysis, Gandiva) and is not claimed as new.

## Research question

RQ-1 asks where size-first scheduling is overtaken by FCFS plus backfill under estimation error, preemption cost, server heterogeneity and gang/locality constraints. Gang/locality was the one friction never measured. Does fragmentation reorder the policies, and does best-fit compact placement remove the effect?

## Why this matters

GPU schedulers often decide order and placement separately. If bad placement can overturn the merit of an ordering, comparisons of ordering alone do not carry over to practice.

## Method

MSJ simulator with 64 GPUs in eight 8-GPU nodes. A gang progresses at rate 1/(1 + pi * excess), where excess is the number of nodes spanned beyond ceil(need/8). Grid: fcfs, easy_backfill, srpt, sf_srpt; first_fit and compact (best-fit) placement; trace_like and gang_heavy mixes; rho {0.6, 0.7}; pi {0, 0.1, 0.3, 0.6}; three seeds; horizons 40k and 80k; 768 runs. Stability was labelled three-way from the 40k/80k JCT slope alpha (STABLE at or below 0.2, DIVERGING at or above 0.8 or on abort, UNKNOWN between; a cell is labelled only if all three seeds agree). Predictions, runner and grading script were sealed in a local commit before the first run (no external timestamp).

## Results

| Prediction | Content | Grade |
|---|---|---|
| P0 | At pi = 0, first_fit and compact give identical JCT (instrument check) | PASS |
| P1 | At pi = 0.3, compact spans fewer excess nodes than first_fit | FAIL (gang_heavy both 0) |
| P2 | Degradation larger on gang_heavy | FAIL (none scorable; gang_heavy 1.00) |
| P3 | Decision: reversal under first_fit, none under compact | FAIL (none under either) |
| P4 | easy_backfill degrades least on trace_like | FAIL (no policy STABLE at both ends) |
| P5 | On gang_heavy, sf_srpt degrades more than easy_backfill | FAIL (both 1.00) |

Cell labels: 100 STABLE, 21 DIVERGING, 7 UNKNOWN of 128. At pi = 0.6, 15 of 16 trace_like cells diverged. Compact placement lowered JCT relative to first_fit in all nine pairs where both were STABLE (0.47 to 0.96x).

## What changed

Hypothesis H10 (topology does not change the ranking) moved from unmeasured to weakly supported with low power. The pre-seal checklist now asks whether the friction can occur at all in the chosen mix and placement.

## What failed

Three of the five misses were decided by gang_heavy never fragmenting: the outcome was fixed before measuring. One run at pi = 0.1 showing `excess_nodes_per_placement` would have revealed it before sealing. pi = 0.6 was too strong and removed the material for the reversal test. The grades stand unchanged.

## Evidence boundary

One synthetic model, N = 64, exponential service, sigma 0, sticky placement, no migration. pi is a setting, not a measured cost. The author who wrote the runner also graded it.

## UNKNOWN

Whether the same order holds for gang mixes that are not node multiples or at smaller pi; the mechanism behind the order (a candidate: slowed gangs hold servers longer, fragmentation reinforces itself, and policies that clear short jobs first hold fragments for less time); behaviour on real clusters.

## Falsification targets

If, on fresh seeds, smaller pi and non-multiple needs, easy_backfill or fcfs degrades less than srpt, the post-hoc observation fails. If a reversal appears at higher load or under another penalty shape, "no reordering" is limited to these loads.

## Reproduce

In the [public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-locality), run `python verify_locality.py`. It checks the sealed digest, reruns the sealed grading script, checks the gang_heavy null, and re-simulates eight runs, in about a minute. The full 768 runs take about 20 minutes on 15 workers with `python run_e18.py`.

## Evidence / Artifacts

[Predictions, runner, grading, simulator and results](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-locality). Predictions, runner and grading script are published as sealed.

## External audit

Zero independent external replications. The seal is a local commit only.

## Next experiment

Seal the post-hoc order srpt < sf_srpt < easy_backfill < fcfs as the decision prediction and test it on fresh seeds, pi {0.05, 0.1, 0.2}, and a gang mix with needs that are not node multiples (e.g. 4/12/24/40).

[[en/research/gpu-scheduling-cold-reader/index|EP-0028]] → EP-0029
