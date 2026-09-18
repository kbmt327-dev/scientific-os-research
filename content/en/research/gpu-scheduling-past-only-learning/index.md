---
research_id: GPU-SCHED-EP-0024
title: Learning capacity from past completions without population parameters
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
  source: Sealed past-only parameter-learning outcomes and same-model executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known two-block exponential FCFS structure only; no population parameters
  in learned inference; no general detector, real GPU effect or established novelty
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0024
source_episode_sha256: 0bfc36ace20590a5498f92698f439e4685053b53b9dded31c2762220f6f4b7cc
publication:
  status: publishable
tags:
- gpu-scheduling
- past-only
- confidence-sequences
- en
aliases:
- /research/gpu-scheduling-past-only-learning/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-past-only-learning/" hreflang="ja">日本語</a></p>

## Current finding

We learned a capacity interval from past arrivals, needs and completions without passing population parameters to the diagnostic. Two known exponential FCFS models, 400 workloads and 6,000 decisions; all four sealed predictions passed. LEARNED_CS had zero observed wrong-side labels, but all 50 seeds at +/-1% load remained UNKNOWN even after 320k arrivals. Zero observed errors do not prove zero risk.

## Key figure

![Known capacity versus learning from past telemetry](/assets/gpu-scheduling-past-only-learning.png)

Each cell has 50 seeds. Red: wrong side; blue: UNKNOWN; grey: correct. Labels are wrong/UNKNOWN. Rows are models, columns are horizons. The five methods have different information and error allocations.

## What this research shows

Under this structure, strict-FCFS starts and censored service exposure can be recovered without true service or future completions, and parameter uncertainty can be propagated into a capacity interval. Loads 20% from the boundary were correctly decided in all seeds at 20k arrivals.

## What this research does not show

General U31/c12, nonexponential inputs, heterogeneous resources, real GPU effects, external independent replication, new theory, peer review, manuscript novelty and operational benefit remain UNKNOWN. Model structure is still known; the experiment designer was not blinded.

## Research question

What changes when the known population-parameter privilege of EP-0023 is removed? We separate the cost of four-way error allocation from the additional uncertainty of learning parameters.

## Why this matters

A known-capacity calibration cannot be transferred unchanged to telemetry with unknown service rates. Point estimates that decide early and intervals that abstain have different measured costs.

## Method

64 fungible resources, needs 32/64, strict nonpreemptive FCFS, iid marked Poisson arrivals and independent hidden class-exponential service. Baseline p=.5, service rates 1/.5, X=8/11; transfer p=.25, rates .5/2, X=16/13. Fresh seeds 9101–9150, loads z=.8/.99/1.01/1.2 and nested 20k/80k/320k prefixes were fixed before execution. Labels use [known two-class stability theory](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf), excluding equality.

Inference receives only arrivals/needs and completed ids/times through cutoff. Starts are reconstructed from strict FCFS and observed resource releases; queued jobs add zero exposure and running jobs are right-censored. With completions M_j and risk exposure V_j=integral R_j, intensity is mu_j R_j. Fixed Gamma(1,rate1) mixtures give E(theta)=exp(theta V) Gamma(M+1)/((V+1)^(M+1) theta^M); marks use Beta(1,1). Existing [confidence-sequence](https://arxiv.org/abs/1810.08240) and [counting-process](https://proceedings.mlr.press/v258/lindon25a.html) methods support the model-conditioned argument. Four errors .0125 give nominal joint anytime .05 by Ville/union bound, without requiring independence between processes. This is not a new inference theorem.

Capacity satisfies 1/X=(1-p)/mu_big+p(2-p)/(2mu_small). Rectangle lower bounds include the interior p extremum. Numeric log slack 1e-6 and outward root padding are fixed; the floating-point implementation is not formally verified.

PAST_AB restores WSC2003 with disclosed sample variance, nominal alpha without a proven guarantee. KNOWN_CS knows X with arrival CS .05; ALLOCATED_CS knows X with CS .0125; LEARNED_CS learns four parameters; PLUGIN_MLE uses the same past telemetry as a point estimate.

## Results

| Model | z | H | AB wrong/UNKNOWN | Known | Allocated | Learned | Plug-in |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.8 | 20k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 80k | 3/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.8 | 320k | 1/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 0.99 | 20k | 3/0 | 0/50 | 0/50 | 0/50 | 13/0 |
| baseline | 0.99 | 80k | 2/0 | 0/48 | 0/49 | 0/50 | 2/0 |
| baseline | 0.99 | 320k | 4/0 | 0/5 | 0/8 | 0/50 | 0/0 |
| baseline | 1.01 | 20k | 32/0 | 0/50 | 0/50 | 0/50 | 9/0 |
| baseline | 1.01 | 80k | 18/0 | 0/43 | 0/47 | 0/50 | 4/0 |
| baseline | 1.01 | 320k | 4/0 | 0/3 | 0/6 | 0/50 | 0/0 |
| baseline | 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 80k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| baseline | 1.2 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 20k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 80k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.8 | 320k | 2/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 0.99 | 20k | 7/0 | 0/50 | 0/50 | 0/50 | 11/0 |
| transfer | 0.99 | 80k | 3/0 | 0/48 | 0/49 | 0/50 | 0/0 |
| transfer | 0.99 | 320k | 1/0 | 0/5 | 0/8 | 0/50 | 0/0 |
| transfer | 1.01 | 20k | 31/0 | 0/50 | 0/50 | 0/50 | 11/0 |
| transfer | 1.01 | 80k | 23/0 | 0/43 | 0/47 | 0/50 | 1/0 |
| transfer | 1.01 | 320k | 9/0 | 0/3 | 0/6 | 0/50 | 0/0 |
| transfer | 1.2 | 20k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 80k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| transfer | 1.2 | 320k | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |

Each cell has 50 seed repetitions. Simultaneous CP intervals split family .05 over 240 cell rates and 80 anylook rates. Anylook counts a seed once if any nested label is wrong; all eight LEARNED_CS anylook cells had zero/50 wrong, with simultaneous upper bound about .149. Joint parameter noncoverage was zero in the 1200 recorded looks; this does not empirically prove all-time coverage.

## What changed

Known population parameters are now learned from past telemetry and integrated into draft v0.4. At 320k near-boundary loads, KNOWN_CS abstained 5/3 times, ALLOCATED_CS 8/6 times and LEARNED_CS 50/50 times, in both models. The learning gap is not explained by splitting the arrival error budget alone.

## What failed

LEARNED_CS could not decide +/-1% loads even at 320k. Plug-in had 9–13 wrong labels out of 50 at 20k near the boundary, but zero wrong and zero UNKNOWN at 320k. In those 320k cells any positive abstention price gives higher point loss for LEARNED_CS. Universal superiority is not claimed; this conservative rectangle method does not establish a sample-complexity lower bound.

## Evidence boundary

Twenty exact CTMC parameter cases, an interior-extremum fixture, past-exposure reconstruction and future-input rejection were checked. Four native fixtures aligned individual departures/starts and class exposure. Counts, CP intervals, loss, anylook and predictions were recomputed for all 6000 decisions. Public code regenerates the same-design causal oracle, without the private native engine.

## UNKNOWN

Coverage under misspecified structure, sharper inference, online expected-loss rankings for unknown truth, third-party independent execution/use and novelty remain UNKNOWN. Validated general detectors: zero.

## Falsification targets

Non-FCFS execution, missing need/completion logs, nonexponential within-class service, size-aware lookahead, heterogeneous resources or placement loss break assumptions requiring a new audit. Unconfirmed applicability means long-term stability UNKNOWN.

## Reproduce

[Code and instructions](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-past-only-learning): `python rerun_past_learning.py --verify-recorded` checks recorded arithmetic and regenerates 16 small runs. Use `--seeds 50 --horizons 20000 80000 320000 --output full.json` for the full grid. OS portability is not independent replication.

## Evidence / Artifacts

[summary.json, inference code and generator](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-past-only-learning) include 1200 seed-look records, 24 cells, eight anylook aggregates, four predictions and recorded native fixtures. This is a reviewed projection, not the original sealed-protocol bytes. Digests and clocks are local provenance, not external authenticated timestamps. Loss e+a u at a=.1/.5/.9 is conditional on benchmark truth, not an online recommendation.

## External audit

External independent replications: zero. Scientific/domain/peer review has not been performed. Primary sources justify existing methods; they do not constitute scientific review of this artifact.

## Next experiment

Audit a gate for model/log applicability. Do not silently apply exponential FCFS inference to an unconfirmed structure. Nonexponential/c12 accuracy claims require an independent known label and a separately sealed design.

[[en/research/gpu-scheduling-two-class-control/index|EP-0023]] → EP-0024


[[en/research/gpu-scheduling-exposure-checkpoints/index|EP-0025]]：Later fixed-count checkpoint/scheduled-look comparison.
