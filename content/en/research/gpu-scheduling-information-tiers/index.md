---
research_id: GPU-SCHED-EP-0021
title: One window, different information, different errors
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
source_episode: GPU-SCHEDULING/EP-0021
source_episode_sha256: f69184188fbb7a793ffc81d9c1fb25a7c4e652c2585f9304923f72c22e0f5c4d
publication:
  status: publishable
tags:
- gpu-scheduling
- known-controls
- uncertainty
- en
aliases:
- /research/gpu-scheduling-information-tiers/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-information-tiers/" hreflang="ja">日本語</a></p>

## Current finding

We scored three diagnostics against known M/M/4 labels: 600 workloads, 100 seeds per load, six loads, three nested arrival windows and 5,400 decisions. Seven of eight sealed predictions passed.

## Key figure

![EP-0021 wrong-side/UNKNOWN counts and future-information cost,100 seeds per cell and nested 20k/80k/320k windows.](/assets/gpu-scheduling-information-tiers.png)

EP-0021 wrong-side/UNKNOWN counts and future-information cost,100 seeds per cell and nested 20k/80k/320k windows.

## What this research shows

Finite-window wrong-side and UNKNOWN rates can be measured separately against independent known-model labels, with information costs stated.

## What this research does not show

No general GPU guarantee, new capacity theorem, real-cluster effect, universal ranking or peer-reviewed paper is established.

## Research question

How do information contracts and abstention prices affect diagnostics under a common arrival window?

## Why this matters

A finite-window declaration needs explicit information and error/abstention costs before it can support a long-term stability claim.

## Method

W's F interval estimates the generative population load under iid exponential assumptions; the realized work ratio is its statistic. One wrong-side interval occurred at nominal per-decision error .05. Earlier zero counts are not an error-free guarantee. AB uses a disclosed sample-variance interpretation of the printed WSC 2003 Algorithm AB; D's threshold has no .05 error guarantee.

[Executable code and instructions](https://github.com/kbmt 327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u 31-tier-benchmark) regenerate inputs from seeds. Same-design execution is not external independent replication.

## Results

At load 1.01 and 20k arrivals, output-only O returned 40 correct/60 wrong; W with all true work and known capacity returned 17 correct/1 wrong/82 UNKNOWN; future-drained JCT elasticity D returned 61 correct/39 wrong. At stable load.99, D's .5 threshold falsely declared overload in 31/100 runs. UNKNOWN is not a correct decision, and common arrival windows do not imply common information.

## What changed

Information tiers and conditional loss were integrated into the draft; later corrections to estimands, price scope and coin comparisons are reflected here.

## What failed

One of eight predictions failed and one F interval was wrong-side; AB specification interpretation is disclosed.

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
