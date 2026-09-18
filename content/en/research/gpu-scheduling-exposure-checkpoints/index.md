---
research_id: GPU-SCHED-EP-0025
title: 'Fixed completion-exposure checkpoints: reporting scope and abstention'
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
  source: Sealed scheduled checkpoint outcomes and same-design executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known two-block exponential FCFS; fixed reporting looks/checkpoints,
  not anytime; no general detector, real GPU effect or established novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0025
source_episode_sha256: eced65710973c1ca3517a81b333e680a10b9ab40f11b07884749240fed82bf8e
publication:
  status: publishable
tags:
- gpu-scheduling
- time-change
- scheduled-inference
- en
aliases:
- /research/gpu-scheduling-exposure-checkpoints/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-exposure-checkpoints/" hreflang="ja">日本語</a></p>

## Current finding

We added fixed completion-exposure checkpoints and predeclared arrival looks to inference without population parameters. 160 workloads, 2400 decisions; 4/4 sealed predictions passed and 0 observed scheduled wrong-side labels. Near-boundary 1280 k UNKNOWN totals were 79/80 for anytime rectangles and 22/80 for scheduled rectangles.

## Key figure

![Anytime versus scheduled wrong-side/UNKNOWN outcomes](/assets/gpu-scheduling-exposure-checkpoints.png)

Each cell has 20 seeds. Red: wrong; blue: UNKNOWN; grey: correct. Bar labels: wrong/UNKNOWN. The three methods see the same past information; scheduled guarantees have narrower scope.

## What this research shows

Under known exponential FCFS structure, fixed-K class completion exposure includes censored running jobs and supports the existing chi-square pivot. The artifact compares reporting scope, information, budgets and abstention costs.

## What this research does not show

No new time-change/capacity/inference theorem, optimal sample complexity, universal superiority, real GPU effect, general U 31/c 12, nonexponential transfer, external independent replication, established novelty or peer review. Scheduled inference is not valid at arbitrary stopping times.

## Research question

Can predeclared looks reduce abstention compared with the previous anytime rectangle? Only fixed completion milestones are used; random observed completion counts are not treated as fixed Gamma shapes.

## Why this matters

Unresolved decisions reflect reporting scope and conservative intervals as well as information. Both the reporting contract and statistic/data subset change; this comparison does not isolate a causal effect of reporting restriction alone.

## Method

64 fungible resources, needs 32/64, strict nonpreemptive FCFS, iid marked Poisson arrivals, independent class-exponential service and empty start. Baseline p=.5,rates 1/.5,X=8/11; transfer p=.25,rates.5/2,X=16/13. Labels follow [known two-class theory](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf), excluding equality. Fresh seeds 9201–9220, z=.8/.99/1.01/1.2, H=20 k/320 k/1280 k and 13 doubling K milestones 256–1048576 were sealed before execution.

Inference sees only arrivals/needs/completions through A_H. With V_j=integral R_j, the continuous unbounded compensator of the infinite model obeys the [existing random-time-change theorem](https://warwick.ac.uk/fac/sci/statistics/apts/students/resources-2010-2011/stochproc_notes.pdf). Therefore 2 mu_jV_j(t_K)~chi-square(2 K) at fixed K. Exposure includes running censored jobs, not merely completed durations. Unconditional union bounds over all fixed K cover failure of an eligible selected milestone; no conditional availability coverage or random-M Gamma pivot is claimed.

Joint scheduled alpha .05 splits four ways, then over 3 looks for arrival chi-square/mark binomial CP and 13 checkpoints for each service rate. Rectangle capacity includes the interior p extremum. ANYTIME_RECT retains [existing likelihood-mixture CS](https://arxiv.org/abs/1810.08240) with four errors.0125. KNOWN_SCHEDULED knows X; ALLOC_SCHEDULED knows X with the same arrival error; PLUGIN_MLE uses past point estimates. Scheduled guarantees cover only original planned looks.

## Results

| Model | z | H | Anytime wrong/UNKNOWN | Checkpoint | Known | Allocated | Plug-in |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.8 | 20 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 320 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 1280 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.99 | 20 k | 0/20 | 0/20 | 0/20 | 0/20 | 5/0 |
| baseline | 0.99 | 320 k | 0/20 | 0/20 | 0/0 | 0/1 | 0/0 |
| baseline | 0.99 | 1280 k | 0/19 | 0/4 | 0/0 | 0/0 | 0/0 |
| baseline | 1.01 | 20 k | 0/20 | 0/20 | 0/14 | 0/17 | 2/0 |
| baseline | 1.01 | 320 k | 0/20 | 0/20 | 0/0 | 0/0 | 0/0 |
| baseline | 1.01 | 1280 k | 0/20 | 0/2 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 20 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 320 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 1280 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 20 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 320 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 1280 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.99 | 20 k | 0/20 | 0/20 | 0/20 | 0/20 | 7/0 |
| transfer | 0.99 | 320 k | 0/20 | 0/20 | 0/0 | 0/1 | 0/0 |
| transfer | 0.99 | 1280 k | 0/20 | 0/13 | 0/0 | 0/0 | 0/0 |
| transfer | 1.01 | 20 k | 0/20 | 0/20 | 0/14 | 0/17 | 2/0 |
| transfer | 1.01 | 320 k | 0/20 | 0/20 | 0/0 | 0/0 | 0/0 |
| transfer | 1.01 | 1280 k | 0/20 | 0/3 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 20 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 320 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 1280 k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |

Each cell has 20 seed repetitions. CP family .05 splits over 240 cell and 80 anylook rates; windows are nested and common cross-cell seeds dependent. Zero/20 anylook wrong has simultaneous upper about.332. Loss e+a u at a=.1/.5/.9 is benchmark-truth conditional, not an online ranking.

## What changed

Scheduled reporting is a separate contract integrated into draftv 0.5. A declaration gate returns UNKNOWN without inference for unconfirmed, out-of-scope, missing or extra model/log statements. It checks declarations, not empirical truth of assumptions.

## What failed

Twenty-seed simultaneous intervals are wide. Finite results do not establish zero risk, arbitrary-time guarantees or expected-loss rankings for unknown truth. All cells and any failed sealed predictions remain in summary; prior all-UNKNOWN results are not an information-theoretic lower bound.

## Evidence boundary

Four native fixtures aligned 24 checkpoint exposures, maximum difference 4.55e-13. A concurrency hand fixture separates exposure 19.9 from completed duration 10. Seven declaration negatives, two unscheduled cases and future/extra input rejection were checked.480 rows/24 cells/eight anylook aggregates were recomputed.

## UNKNOWN

Time-varying parameters/structure, nonexponential or heterogeneous models, real-log applicability, sharper methods, third-party independent execution/use and novelty remain UNKNOWN. General validated detectors: zero.

## Falsification targets

Missing completions, non-FCFS execution, size lookahead, within-class nonexponential service or placement loss change assumptions. Matching declarations do not prove real-data validity. Scheduled inference is unavailable at unplanned looks.

## Reproduce

[Code and instructions](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-exposure-checkpoints): `python runner_checkpoint.py --verify-recorded` checks arithmetic and 16 regenerated small runs. Full grid: `--seeds 20 --horizons 20000 320000 1280000 --output full.json`. Partial runs keep the original error allocation without recycling omitted-look budgets.

## Evidence / Artifacts

[summary, past tape, scheduled/anytime inference, generator and runner](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-exposure-checkpoints). JSON is a reviewed projection, not original sealed bytes. Digests/clocks are local provenance, not authenticated timestamps. Continuous verifier tolerance: rel 1e-9/abs 1e-10; labels/counts exact.

## External audit

External independent replications: zero; scientific/domain/peer review not performed. Public code regenerates the same-design causal FCFS oracle without the private native engine. Primary sources justify existing methods, not scientific review of this artifact.

## Next experiment

Separately seal an audit of applicability rejection and independent labels for time-varying parameters/structure. Do not silently treat an unconfirmed system as exponential FCFS or restore general C 042/scheduler rankings.

[[en/research/gpu-scheduling-past-only-learning/index|EP-0024]] → EP-0025
