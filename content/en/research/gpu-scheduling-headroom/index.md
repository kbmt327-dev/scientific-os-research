---
research_id: GPU-SCHED-EP-0030
title: "Gang mix reverses the fragmentation ranking; a load control explains much of the gap"
date: '2026-10-02'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Decision prediction P2 failed; approximate load control passed
evidence_level: Sealed synthetic experiment, single model; bounded saved-result projection
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: E19 saved grading projection and sealed prediction PRED-018
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic model with 64 GPUs in 8-GPU nodes; approximate load-matched comparison only; no real-cluster generalization
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0030
source_episode_sha256: 7e6375fa8addfdac5fbd3737b938bf0e4f4e6a61ed49732163813d36ab29a398
publication:
  status: publishable
tags:
- gpu-scheduling
- fragmentation
- sealed-prediction
- en
aliases:
- /research/gpu-scheduling-headroom/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-headroom/" hreflang="ja">日本語</a></p>

## Current finding

Three of six sealed predictions held; decision prediction P2 failed. Among scorable first_fit rows, trace_like held the preregistered order in 3/3 rows, while gang_odd reversed srpt versus sf_srpt in 4/4. We withdraw the EP-0029 post-hoc order as a cross-mix claim that size-first policies are more robust to fragmentation.

## Key figure

| Prediction | Result | Scope |
|---|---|---|
| P2: rank at pi = 0.1/0.2 | FAIL | trace_like held 3/3; gang_odd reversed srpt and sf_srpt in 4/4; 1 of 8 rows was unscorable |
| P3: rank at pi = 0.05 | FAIL | trace_like held 2/2; gang_odd reversed srpt and sf_srpt in 2/2 |
| P4: load increase at pi = 0 | FAIL | 3/4 rows held; gang_odd rho = 0.7 to 0.8 gave srpt 1.216 and sf_srpt 1.195 |
| P5: load-matched control | PASS | all 4/8 computable rows met the preregistered residual-gap threshold |

## What this research shows

In this synthetic model and configuration, gang_odd reversed the degradation order of srpt and sf_srpt. P1 confirmed fragmentation friction in all 8/8 rows: first_fit excess was 0.22 to 0.36, while compact was 0.05 to 0.09. Of 152 cells, 144 were STABLE and 8 were UNKNOWN.

The P5 load control met its preregistered condition in all four computable rows under an approximate comparison. Recomputing the explained share from the saved grading rows gives 63.8% to 100.0%. This is arithmetic over a compact projection, not an independent simulation rerun.

## What this research does not show

It does not establish rankings on real clusters, generality across schedulers or workloads, or a causal fragmentation effect. Fragmentation increases work only for gangs spanning nodes, while the load-control arm increases work uniformly for arrivals. P5 is therefore an approximate control, not a causal decomposition. About 0.50 of the gap remains for trace_like at rho = 0.6 and pi = 0.2 after load matching.

## Research question

Would the post-hoc EP-0029 order hold with new seeds and a gang mix whose sizes are not node multiples? A pi = 0 arm that raises arrival load alone also tested whether policy headroom could account for the degradation differences.

## Why this matters

A post-hoc order seen in one trace_like mix did not transfer across mixes: srpt and sf_srpt changed order. A ranking claim needs a sealed test across mixes. The load control shows that much of the gap is consistent with load headroom, but it does not identify the mechanism.

## Method

The sealed E19 prediction PRED-018 specified 768 main runs and 144 load-arm runs, 912 total. The model has 64 GPUs in 8-GPU nodes, exponential service, sigma = 0, sticky placement, and no migration. This public package builds a compact row-level projection from the saved grading and recomputes rank decisions and P5 arithmetic. It does not rerun the simulation.

## Results

P0 and P1 passed; P2, P3, and P4 failed; P5 passed, for three of six predictions. P2 had 7/8 scorable rows: trace_like passed 3/3, while gang_odd violated the srpt/sf_srpt order in 4/4. P3 held in 2/4 rows and P4 in 3/4. All eight UNKNOWN cells were concentrated in high-load fcfs or easy_backfill rows.

## What changed

The EP-0029 post-hoc ranking remains a historical observation from E18's trace_like mix. We withdraw the broader four-policy ranking and any implication that size-first policies are generally more robust to fragmentation. The EP-0030 results and correction are [here](/en/research/gpu-scheduling-headroom/).

## What failed

Decision prediction P2 did not support the preregistered four-policy order. The P2, P3, and P4 failures centered on srpt versus sf_srpt in gang_odd. The strict order was preregistered, so rows within per-seed variation were still graded as specified.

## Evidence boundary

Results come from one synthetic model under fixed settings. The seal is local, and there are zero independent external replications. The public reproduction package checks an aggregate projection of the saved grading; it does not contain raw E19 runs and is not a full rerun or independent replication.

## UNKNOWN

Rankings on other models, penalty shapes, real schedulers, or clusters remain UNKNOWN. The eight UNKNOWN cells are not failed evidence; they did not meet the preregistered reporting threshold.

## Falsification targets

A new sealed experiment in which srpt consistently has lower degradation than sf_srpt on gang_odd would fail to reproduce this reversal. A new load-control arm or real-cluster measurement that differs materially from P5 would also weaken the limited headroom interpretation.

## Reproduce

Run python verify_e19_projection.py in the [bounded verification package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-headroom). It recomputes P0-P5 counts and thresholds from projected saved-grading rows. It does not rerun the 912 simulations or provide an external replication.

## Evidence / Artifacts

[Verifier and aggregate projection](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-headroom). Included source-artifact hashes identify versions; raw run records and the prediction JSON are not included.

## External audit

There are zero independent external replications. PRED-018 was sealed in a local record. No independent implementation of the same model has been tested.

## Next experiment

Test srpt versus sf_srpt on a newly sealed seed set and gang mix, preserving the approximate boundary of the load-matched control. Do not claim real-cluster generalization until it is measured.
