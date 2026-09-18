---
research_id: GPU-SCHED-EP-0022
title: The price of abstention and the critical-load definition
date: '2026-09-18'
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
source_episode: GPU-SCHEDULING/EP-0022
source_episode_sha256: f54e91a65b31f402c98be348e731ed115c1854b99da369a65092b66d60d3f5e4
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- en
aliases:
- /research/gpu-scheduling-critical-loss/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-critical-loss/" hreflang="ja">日本語</a></p>

## Current finding

Using unused seeds 6001-6100, five loads, three windows and seven methods, we measured 10,500 decisions with pre-fixed loss L(a)=wrong_rate+a UNKNOWN_rate. Five of eight sealed predictions passed. The per-cell superiority prediction against constant baselines was ill-posed and failed; two other predictions also failed and remain recorded.

## Key figure

![EP-0022 conditional loss curves and critical-load declarations. Crossovers are point estimates, not online recommendations or equivalence tests.](/assets/gpu-scheduling-critical-loss.png)

EP-0022 conditional loss curves and critical-load declarations. Crossovers are point estimates, not online recommendations or equivalence tests.

## What this research shows

Finite-window wrong-side and UNKNOWN rates can be measured separately against independent known-model labels, with information costs stated.

## What this research does not show

No general GPU guarantee, new capacity theorem, real-cluster effect, universal ranking or peer-reviewed paper is established.

## Research question

How do information contracts and abstention prices affect diagnostics under a common arrival window?

## Why this matters

A finite-window declaration needs explicit information and error/abstention costs before it can support a long-term stability claim.

## Method

[Executable reproduction](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u 31-tier-benchmark) includes critical-load declaration counts. Interpret loss with prices, target distributions and information costs stated.

## Results

The O/W crossover price was .152 at load.99/20k and .739 at 1.01/20k; at 320k it was 1.250/4.000. These are cell-specific point estimates. A price above one supports a point-estimate comparison within 0<=a<=1, not arbitrary prices or universal advantage with enough data. Truth-conditioned crossover prices cannot directly recommend an online decision for unknown truth.

At critical M/M/4, positive recurrence differs from positive linear queue growth: the chain is null recurrent with zero asymptotic linear growth. O declared subcritical in 80/78/81 runs at 20k/80k/320k; W returned UNKNOWN in 96/93/91. D's declaration proportions were close to a coin, but equivalence was not tested. Lack of improvement across these windows is not an infinite-horizon impossibility result.

## What changed

Information tiers and conditional loss were integrated into the draft; later corrections to estimands, price scope and coin comparisons are reflected here.

## What failed

Three of eight predictions failed, including an ill-posed per-cell superiority claim against constant baselines.

## Evidence boundary

Synthetic known models, local seals and same-design/generator execution only. Recorded native alignment differs from public oracle re-execution.

## UNKNOWN

General U-31/c 12 capacity, real clusters, operational benefit, external independent replication, novelty and acceptance. Validated general detectors=0.

## Falsification targets

Invalid theorem mapping, source hashes, population assumptions, individual departure alignment or arithmetic aggregation invalidate these control claims; return UNKNOWN.

## Reproduce

[Re-execution instructions and code](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u 31-tier-benchmark) regenerate inputs from seeds and compare with records.

## Evidence / Artifacts

[Public artifacts](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u 31-tier-benchmark); source Episode hashes appear in frontmatter. Private sources and personal paths are excluded.

## External audit

Independent replications=0. Scientific, domain-expert and peer review are unperformed. Editorial and arithmetic checks are not independent scientific audits.

## Next experiment

Narrow the useful contribution against prior work and assess another environment/reader execution. Broader models need another contract; original scheduler rankings/capacities remain suspended.

[[en/research/gpu-scheduling-information-tiers/index|EP-0021]] · [[en/research/gpu-scheduling-critical-loss/index|EP-0022]] · [[en/research/gpu-scheduling-two-class-control/index|EP-0023]]
