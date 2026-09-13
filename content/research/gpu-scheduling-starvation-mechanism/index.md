---
id: GPU-SCHED-EP-0003
title: Whole-cluster jobs, not mean gang size, decide when size-based scheduling breaks
date: 2026-09-13
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Synthetic simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: Public simulator, mean-matched control mix, priority-by-filling factorial, sealed prediction, and E4 outputs
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Synthetic demand mixes with whole-cluster job share from 0 to 0.03 plus one mean-matched control, 64 servers, exponential service, rho 0.7 and 0.85, zero preemption cost
source_episode: GPU-SCHEDULING/EP-0003
source_episode_sha256: ca6a566b0396730d61e2ec33a48c5cfd1a12b6246dcd2a43e5e03f067b0ff3de
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification, starvation]
---

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

Follows [[research/gpu-scheduling-phase-diagram/index|A demand-mix phase diagram, and three stability detectors that failed]].

## Summary

Two earlier studies disagreed. EP-0001 found greedy SRPT winning on a mix whose mean gang size was 3.26 and whose largest job needed half the cluster. EP-0002 found greedy SRPT starving a demand class on a mix whose mean gang size was *smaller*, 2.37, but which included jobs needing the whole cluster. The mean pointed the wrong way, so we held it fixed and moved only the support.

With mean gang size matched at 4.076, a mix capped at half the cluster is stable under greedy SRPT — worst-class mean JCT 3.31 — while a mix containing 3 percent whole-cluster jobs starves, at worst-class mean JCT 655.7. The threshold is far lower than 3 percent: 15 whole-cluster jobs in 30,000 are enough, and it happens at rho 0.7 as readily as at 0.85. A two-by-two over priority rule and filling rule locates the cause in the *combination* of size-based priority with greedy work conservation; neither alone produces it. Preemption is not the cause and mildly mitigates it. Ten sealed predictions graded 7/10.

## Research question

Is the trigger for whole-cluster starvation the support of the demand distribution containing the cluster size N, rather than the mean gang size? And is the starvation produced by size-based priority, by greedy work conservation, or only by the two together?

## Why this matters

"Large-gang workloads break naive schedulers" is a statement about proportions, and it invites a capacity-planning response: watch the share of big jobs. If the real trigger is the *presence* of a job class that requires the entire cluster, the operational rule is different and much sharper — the question is not how many, but whether any.

It also changes what to monitor. The aggregate mean is blind exactly in the regime where whole-cluster jobs are rare, which is the regime in which they are easiest to overlook.

## Method

Weights over needs 1 to 32 keep the `theta = 0.4` shape and are renormalized to `1 - p64`; the remaining mass `p64` is placed on need 64 on a 64-server cluster. Only the support changes.

| Mix | Mean gang size | Largest need | Whole-cluster share |
|---|---|---|---|
| p64 = 0 | 2.223 | 32 | 0 |
| p64 = 0.0005 | 2.254 | 64 | 0.0005 |
| p64 = 0.002 | 2.346 | 64 | 0.002 |
| p64 = 0.008 | 2.717 | 64 | 0.008 |
| p64 = 0.03 | 4.076 | 64 | 0.03 |
| **matched control** | **4.076** | **32** | **0** |

The control's shape parameter was solved numerically so its mean gang size equals the `p64 = 0.03` mix. If starvation tracked the mean, the control would starve too.

The mechanism factorial crosses priority rule against filling rule: greedy SRPT (size priority, greedy fill), ServerFilling-SRPT (size, exact fill), FCFS (arrival, greedy), ServerFilling-FCFS (arrival, exact), plus EASY backfill (arrival with reservation) and non-preemptive greedy SRPT. Two loads, five seeds, 30,000 jobs, and a 120,000-job horizon check on every cell. 432 runs.

Predictions were sealed with SHA-256 `2f3b1808d806e9af888acaa77a7e00f7e9af86a13d58e42ac75e514a91157d05` and committed before any result file existed. Acting on the previous study's lesson, the stability detector itself is written into the sealed file under `detector`.

## Results

**The mean-matched control settles it.** Same mean gang size, opposite outcome.

| | Verdict | Mean JCT | Worst-class mean JCT |
|---|---|---|---|
| Control, largest need 32, mean 4.076 | Stable, min flow balance 0.997 | 1.167 | 3.31 |
| p64 = 0.03, largest need 64, mean 4.076 | Class-starved | 20.55 | 655.7 |

**The threshold is very low.** At `p64 = 0.0005` — 15 whole-cluster jobs among 30,000 — greedy SRPT already starves that class at both loads, with 64-GPU mean JCT of 312.5 against EASY backfill's 5.40 and ServerFilling's 1.21.

**Only the combination breaks.** Flow balance of the 64-GPU class at rho 0.85, where 1.0 means the class completes as fast as it arrives:

| Mix | FCFS | EASY backfill | greedy SRPT | greedy SRPT, no preemption | ServerFilling-SRPT | ServerFilling-FCFS |
|---|---|---|---|---|---|---|
| p64 = 0.0005 | 0.989 | 0.989 | **0.397** | **0.000** | 1.000 | 1.000 |
| p64 = 0.002 | 0.962 | 0.992 | **0.308** | **0.000** | 0.996 | 0.996 |
| p64 = 0.008 | 0.677 | 0.987 | **0.386** | **0.000** | 0.997 | 0.995 |
| p64 = 0.03 | 0.395 | 0.987 | **0.443** | **0.000** | 0.998 | 0.996 |

Size priority alone does not starve; greedy filling alone does not starve. Both together do. The proposed mechanism: a job needing the whole cluster can start only when it is the global minimum of remaining time, but its remaining time never decreases, because it never runs. Arrival-order priority escapes the trap because head-of-line blocking drains the cluster; exact filling escapes it because descending-need fill reserves a slot for the largest job.

**The delay is unbounded, not merely large.** Over a 4x horizon the starved class's mean JCT grows 2.83x while the 1-GPU class grows 1.02x.

**Preemption is not the cause.** The non-preemptive variant is worse, with flow balance of exactly 0.000: while arrivals continue, not one whole-cluster job completes. Preemption lets such a job seize the cluster if it ever reaches the head, so it mitigates.

**The blindness of the aggregate has a boundary.** Greedy SRPT's mean JCT against EASY backfill's runs 0.756, 0.800, 0.982, 1.695 as `p64` goes 0, 0.0005, 0.002, 0.008. At `p64 = 0.002` the ratio is 0.982 — indistinguishable from a healthy policy — while the whole-cluster class is 63x worse. By `p64 = 0.008` the aggregate does notice. The metric is blind precisely where the rare class is rare.

## What changed

EP-0002 offered "the support contains N" as a hypothesis. With the mean-matched control it becomes a separated result, and the operational reading changes from a proportion to a predicate: the question is whether any job requires the whole cluster, not how many do.

Two further revisions: preemption moves from suspected aggravator to demonstrated mitigator, and the claim "the aggregate metric cannot see class starvation" acquires a condition — it holds while the class is rare.

## What failed

Three of ten sealed predictions failed.

| Prediction | Criterion | Result |
|---|---|---|
| R1 | Greedy SRPT starves need 64 at every positive p64 | Supported at all four |
| R2 | At p64 = 0 it starves nothing and beats ServerFilling | Supported. 1.084 against 1.210, paired ratio 0.896, reproducing EP-0001 |
| R3 | The mean-matched control does not starve | Supported. Stable, min flow balance 0.997 |
| R4 | ServerFilling's mean JCT moves less than 25 percent from p64 0 to 0.008 | **Failed.** It moved 38 percent, 1.210 to 1.674. Exact filling prevents the starvation but does not absorb the cost |
| R5 | EASY backfill starves nothing anywhere | Supported. 12 of 12 cells stable |
| R6 | Exactly the greedy plus size-priority policies starve | Supported |
| R7 | The starved class grows at least 2x over a 4x horizon, the small class under 1.2x | Supported. 2.83x and 1.02x |
| R8 | The aggregate ratio stays within 30 percent up to p64 = 0.008 | **Failed.** 1.695 at 0.008. The blindness needs the rarity condition stated above |
| R9 | Worst-class JCT rises monotonically and exceeds 100 above p64 = 0.002 | Supported. 4.4, 312.5, 394.4, 425.7, 655.7 |
| R10 | ServerFilling-FCFS is stable everywhere and loses to ServerFilling-SRPT on mean JCT | **Failed.** The mean-JCT half holds in all six mixes, but one cell grew 1.31x against a 1.30x threshold and is undetermined |

R10 failed on a hairline: completion was 1.000, nothing aborted, and flow balance improved with the horizon. The threshold was not moved after the fact, so it stands as a failure.

One analysis defect was corrected after seeing results, in the direction that makes grading harder: the horizon comparison originally divided a single-seed long run by a five-seed short-run mean, letting seed variation leak into the growth ratio. It is now seed-paired. R10's verdict did not change.

## Evidence boundary

**Supported:** Under this simulator and these mixes, whole-cluster starvation under greedy size-based scheduling tracks the support of the demand distribution rather than its mean; it appears at a whole-cluster share of 0.0005; it requires both size priority and greedy work conservation; and preemption mitigates rather than causes it.

**Not supported:** No production-cluster claim. The needs grid is powers of two, so the boundary between "half the cluster" and "the whole cluster" is untested between 33 and 63. Preemption cost was zero. Service times were exponential. No real trace has been run, so whether real GPU clusters contain a whole-cluster job class at all — the precondition for this entire finding to matter in practice — is unverified here.

## UNKNOWN

- Whether the threshold is exactly need = N or begins somewhere above N/2. Only 32 and 64 are on the grid.
- Whether non-zero preemption cost removes the mitigation.
- Whether heavy-tailed service times change the share at which the aggregate metric starts to notice.
- Whether the non-preemptive variant starves for the same reason or merely because it cannot preempt.
- Real-trace demand distributions, the highest-priority open item: the share of whole-cluster jobs in Philly or Alibaba PAI can be compared directly against the 0.0005 threshold.

## Falsification targets

- An independent simulator finds the mean-matched control starving, which would restore mean gang size as the driver.
- A mix containing whole-cluster jobs runs stably under greedy SRPT at any load.
- The starved class's JCT converges under a longer horizon.
- ServerFilling-FCFS or FCFS starves the whole-cluster class, which would break the priority-by-filling separation.
- Public traces show no whole-cluster job class, which would leave the finding true of the model and irrelevant to practice.

## Reproduce

### Quick artifact and grading check

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-phase
```

### Full rerun

```bash
cd reproduction/gpu-scheduling-phase
python run_e4.py
python analyze_e4.py
```

`run_e4.py` carries its own 120,000-job horizon check on every cell, so no verdict depends on an unadjudicated assumption.

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-phase)
- [Sealed PRED-003, including the stability detector](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-003.json)
- [E4 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E4_grading.json)
- [E4 report, with the mean-matched control](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E4_report.txt)

## External audit

- Independent replications: 0
- Failed replications: 0
- Confirmed bugs: 0
- Open critiques: 0

## Next experiment

Measure the whole-cluster job share in public production traces — Philly via Blox, Alibaba PAI via the Kubernetes scheduler simulator — and compare it against the 0.0005 threshold. Until that is done, this finding describes the model and not any real cluster. A secondary experiment drops the power-of-two constraint to locate the starvation boundary between half and full cluster size.
