---
research_id: GPU-SCHED-EP-0018
title: A midpoint queue threshold missed a known overload
date: '2026-09-17'
lang: en
domain: GPU Cluster Scheduling
type: Negative Result
status: Known-control miss; general capacity unresolved
evidence_level: Synthetic known-model controls
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: 36 oracle workloads + 4 engine fixtures; public aggregate arithmetic only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known full-gang M/M/1; homogeneous FCFS; independent exponential inputs; true required work accessible; no mixed-need or real-cluster capacity claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0018
source_episode_sha256: 766e176d6e0254b00e3494ecc8a8dff44deadb39b5a7d8795607f6f65c8846c0
publication:
  status: publishable
tags:
- negative-result
- gpu-scheduling
- known-controls
- uncertainty
- en
aliases:
- /research/gpu-scheduling-known-controls/index
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Known controls and finite-window uncertainty</span><a href="/ja/research/gpu-scheduling-known-controls/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Negative Result</span><span>Synthetic known model</span><span>Capacity UNKNOWN</span><span>No peer review</span><span>Independent replications 0</span></div>

## Current finding

**A queue threshold formed from two distant controls missed a known overload.** At rho=1.05, alpha was 0.976505 but the queue score was 0.033571, below the calibrated midpoint of 0.059412. Only the queue label missed the overload. Execution stopped at this first disagreement.

Every job occupies all 64 servers. Only one job can run, so homogeneous FCFS with independent exponential gaps and service sizes reduces to M/M/1. This is an inference from the implementation; the [known load criterion](https://homepages.ecs.vuw.ac.nz/~schukova/SCIE201/Lectures/Lecture9_10_final.html) supplies the independent label. This boundary does not transfer to the balanced mixed-need workload.

## Research question

Can known controls narrow the disagreement in [[en/research/gpu-scheduling-u31-calibration/index|EP-0017]]? Does the midpoint between distant stable and overload controls classify growth near the transition?

## Why this matters

Choosing the preferred signal when detectors disagree is not calibration. Independent known labels let us identify a miss on the queue side in this limited case.

## Method

Full-gang FCFS, 64 homogeneous servers, independent exponential gaps and mean-one exponential service were fixed. Calibration used rho=0.4/1.2 and seeds 301/302/303. Holdout loads were 0.95/1.05/0.99/1.01 in that order, with distinct seeds 401/402/403. Horizons were 20k/40k/80k jobs. Primary alpha was the log ratio of seed-averaged JCT at 40k/80k, with line 0.5.

The 80k queue score was the last-minus-first event backlog decile mean divided by job count. Its threshold was the control midpoint. A full-gang FCFS recurrence solved the generated job streams. Four same-job fixtures first matched the existing engine's individual completion times, JCT and event queue scores exactly. Each complete cell was checked against the known label, stopping at the first R2/R3. The seal was a local hash/time record, without an external timestamp or independent producer.

## Results

| rho | alpha | event queue score | known label |
|---:|---:|---:|---|
| 0.40 | -0.006956 | -0.000001 | stable |
| 1.20 | 1.008942 | 0.118824 | overloaded |
| 0.95 | -0.229628 | -0.000023 | stable |
| 1.05 | 0.976505 | 0.033571 | overloaded |

Both labels matched at rho=0.95. At 1.05 only the queue missed; execution stopped at R2 after 36 of at most 54 oracle workloads. Loads 0.99/1.01 were not executed. The time-weighted queue score was similarly 0.033578, so event weighting alone does not explain this miss. Alpha at 1.05 was 0.988114 on the earlier pair and 0.976505 on the later pair; lines 0.3/0.5/0.7 all indicated growth.

## What changed

Separation of distant controls is now distinct from calibration near the boundary. General adoption of the midpoint queue threshold is deferred. [[en/research/gpu-scheduling-drift-uncertainty/index|EP-0019]] tests uncertainty and abstention next.

## What failed

The midpoint threshold forced a small known overload into a no-growth label. It was not lowered after results to manufacture acceptance. Predicting the miss correctly does not make the detector pass.

## Evidence boundary

This is a synthetic, full-gang, known-M/M/1 control check at fixed horizons and seeds. Alpha agreement covers these four cells only. It does not identify the balanced rho=0.85 label, validate a general alpha threshold or bisection capacity, or demonstrate real-cluster performance. Public artifacts expose aggregate arithmetic and stop branches, without raw job sequences or simulator source.

## UNKNOWN

Which label is right under mixed needs; whether independent known-capacity controls exist there; whether unfinished jobs' true required work is observable in real data. General capacity and detector validity remain UNKNOWN.

## Falsification targets

Withdraw the miss description if the projected midpoint or known-label comparison cannot be recalculated. A future improved contract does not erase this fixed-contract failure.

## Reproduce

```bash
python reproduction/gpu-scheduling-u31-controls/verify_summary.py
```

This checks projected arithmetic and CI/stop branches; it does not rerun the simulator.

## Evidence / Artifacts

[Public aggregates and verifier](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-controls). Private Episode SHA-256: `766e176d6e0254b00e3494ecc8a8dff44deadb39b5a7d8795607f6f65c8846c0`. It identifies the source snapshot, not scientific validity.

## External audit

Zero independent replications and no peer review. Editorial consistency and privacy review are not scientific or domain-expert review.

## Next experiment

Fix input-drift uncertainty before observation and test a rule that can abstain on small growth. The outcome follows in [[en/research/gpu-scheduling-drift-uncertainty/index|EP-0019]]. Mixed-need capacity and real clusters remain separate gates.
