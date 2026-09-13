---
research_id: GPU-SCHED-EP-0004
lang: en
aliases: [/research/gpu-scheduling-real-traces/index]
title: Real GPU clusters never received a job that filled the pool
date: 2026-09-13
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Public trace measurement plus synthetic simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: public-trace-retrospective-and-synthetic-simulation
  source: Philly and Alibaba PAI public traces, per-virtual-cluster capacity measurement, two sealed predictions, and E6 threshold sweep
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Demand shape only from two public traces (194,202 GPU jobs), 11 Philly virtual clusters, plus a synthetic job-size-to-pool-ratio sweep at 64 servers, rho 0.7 and 0.85
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0004
source_episode_sha256: 6ec6a9dba06e28147c46effd2d7ca5d9867a55b9a0ff918f05649c40ab586653
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification, traces, retraction]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Testing the precondition against real data</span><a href="/ja/research/gpu-scheduling-real-traces/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Public trace + synthetic</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

Follows [[en/research/gpu-scheduling-starvation-mechanism/index|Whole-cluster jobs, not mean gang size, decide when size-based scheduling breaks]], whose practical claim this study demotes.

## Current finding

None of the 11 measured Philly virtual clusters received a job that filled its pool. Between half-pool and full-pool jobs, synthetic degradation was steep but continuous: at the observed worst ratio of 0.59 the large class completed, about 7.4× slower than single-GPU jobs. The model's provisional safety boundary was 0.75; larger real pool sizes remain an unfavorable unknown.

The previous study concluded that a demand distribution containing whole-cluster jobs breaks greedy size-based scheduling at a share as low as 0.0005, and gave the practical rule: check first whether jobs requiring the entire cluster arrive. This study put that rule in front of two public traces and, as promised in the sealed file beforehand, demoted it.

Across all 11 Philly virtual clusters — the units Philly actually schedules against — the probability that a job needs the whole pool is 0.00000. The largest job in the worst case needs 59 percent of its pool. So the condition the mechanism requires was not met anywhere in the measured data.

That put the entire practical relevance of the work on a band the previous study had never measured: jobs between half and all of the pool. Sweeping it shows no threshold. Degradation is continuous and steep, complete starvation occurs only at exactly the full pool size, and a usable safety boundary sits at 0.75. At the real measured ratio of 0.59 the class does not starve; it runs 7.4x slower than a single-GPU job. The harm is real but it is a delay, not an unbounded wait.

## Key figure

<div class="ratio-figure" aria-label="Largest-job to pool-capacity ratio"><div class="ratio-track"><i style="left:59%"></i><i style="left:75%"></i><i style="left:100%"></i></div><div class="ratio-labels"><span style="left:59%"><b>0.59</b> Philly max<br>delay, not starvation</span><span style="left:75%"><b>0.75</b> model r_safe</span><span style="left:100%"><b>1.00</b> model starvation</span></div></div>

## What this research shows

- Two public traces have thin, single-GPU-heavy demand tails; measured Philly pools contain no pool-filling job.
- In the 64-slot synthetic sweep, harm changes continuously with largest-job/pool ratio and crosses a provisional 0.75 flow-balance boundary.

## What this research does not show

- No policy was run on a real arrival stream; only demand shape came from traces.
- The 0.75 boundary is not yet validated at the 217–603 GPU scale of measured pools or beyond these two traces.

## Research question

Do the demand distributions of real GPU clusters contain the job class the mechanism requires? And between half the pool and the whole pool, is there a threshold or a continuous decline?

## Why this matters

A mechanism demonstrated inside a model earns attention only if its precondition occurs outside the model. Publishing the mechanism without testing that precondition would have left a practical-sounding rule — "check whether whole-cluster jobs arrive" — attached to a condition that the measured data does not contain.

The replacement rule is different in kind and is still actionable: what matters is the ratio of the largest job to the pool, and the failure it predicts is a multiple-factor slowdown rather than starvation.

## Method

**E5, demand shape.** Job GPU counts from Microsoft Philly (`cluster_job_log`, 112,018 GPU jobs) and Alibaba PAI v2020 (100K sample, 82,184 GPU jobs). Sealed as PRED-004, SHA-256 `7ef0f5b21d46318e6008a1be3021e9c1ffbefbe3fb23e959c3cffa7268048cbe`.

Philly schedules per virtual cluster, so per-VC peak concurrent GPU usage gives a *measured* pool capacity rather than an assumed one. Peak concurrency is a lower bound on capacity, so a larger true quota only makes the ratios smaller; the conclusion is robust in that direction.

**E6, the unmeasured band.** A background population of small jobs plus one large class at need `m`, arriving with probability 0.002, sweeping `m` from N/2 to N at N = 64, rho 0.7 and 0.85, five seeds, with a 120,000-job horizon check on every cell. 463 runs. Sealed as PRED-005, SHA-256 `fe3e27d68d27c5c8eb9fb6633d133e17fd6c4ba09158ab80d901dc4630ccb902`. ServerFilling requires powers of two, so it was run only at m in {32, 64}; reporting it at other sizes would misuse the algorithm.

Both seals were committed before their result files existed.

## Results

**Demand shape.** Single-GPU jobs dominate both traces, and the tails are thin.

| Trace | GPU jobs | E[k] | Median | Max k | P(k=1) | Power-of-two share | p(k ≥ 64) |
|---|---|---|---|---|---|---|---|
| Alibaba PAI v2020 | 82,184 | 2.736 | 1 | 150 | 0.788 | 0.876 | 0.00164 |
| Microsoft Philly | 112,018 | 1.744 | 1 | 128 | 0.866 | 0.9995 | 0.00035 |

Against a *hypothetical* 64-GPU pool, PAI's 0.00164 is 3.3x the previous study's threshold, and that sealed prediction passed. But a measurement added after sealing answered the question more directly.

**Measured pools contain no pool-filling job.**

| Virtual cluster | Jobs | Peak concurrent GPUs | Max k | Max k / capacity | p(k ≥ capacity) |
|---|---|---|---|---|---|
| 6214e9 | 51,980 | 603 | 16 | 0.03 | 0.00000 |
| **11cb48** | 19,401 | 217 | 128 | **0.59** | 0.00000 |
| 6c71a0 | 15,014 | 290 | 48 | 0.17 | 0.00000 |
| ee9e8c | 5,859 | 532 | 128 | 0.24 | 0.00000 |
| Other 7 VCs | 19,412 | 66–360 | 1–32 | 0.02–0.25 | 0.00000 |

Exactly one virtual cluster, 11cb48, landed in the band between half and full pool size — the band the previous study never measured, having tested only N/2 (does not starve) and N (starves).

**The band is continuous, with no threshold.** Greedy SRPT at rho 0.85, where flow balance 1.0 means the class keeps up with its own arrivals:

| m / N | 0.50 | 0.53 | 0.56 | 0.59 | 0.63 | 0.69 | 0.75 | 0.88 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|
| Class flow balance | 0.998 | 0.996 | 0.996 | **0.996** | 0.984 | 0.949 | 0.913 | 0.708 | **0.390** |
| Class mean JCT | 3.7 | 4.8 | 6.2 | **7.9** | 13.7 | 30.9 | 49.2 | 151.5 | **330.7** |
| Single-GPU mean JCT | 1.07 | 1.07 | 1.07 | 1.07 | 1.07 | 1.07 | 1.07 | 1.06 | 1.05 |

The sealed file also carried a mechanism-derived expectation: only `m = N` has the qualitatively distinct property of requiring rank 1 in the priority order to start at all, while `m < N` is a continuous competition for capacity, so the decline should be steep but smooth rather than stepping at N/2. That is what happened.

**Safety boundary `r_safe` = 0.75**, where the class still keeps flow balance at or above 0.9. At Philly's measured 0.59 the class does not starve, but it runs **7.4x** slower than a single-GPU job.

EASY backfill never starves the class at any ratio, with worst flow balance 0.999 and maximum JCT 6.7 — the only policy that has not broken anywhere across four studies. The non-preemptive variant is worse than greedy SRPT at every point, reaching flow balance 0.308 already at 0.75 and 0.000 at or above 0.875.

## What changed

The practical claim of the previous study is demoted, executing a commitment written into the sealed file before the data was seen:

> If the decisive prediction passes, demote the practical implication from "check whether a job filling the whole pool arrives" to a conditional on the largest job exceeding `r_safe` of pool capacity, and relabel the domain heading as *present in the model, unobserved as starvation in the two public traces examined*.

- **Withdrawn:** "check first whether jobs requiring the entire cluster arrive." No measured pool receives one.
- **Replacement:** check whether the largest job exceeds **0.75 of pool capacity**. Philly's worst virtual cluster is 0.59, under that boundary.
- **Revised harm model:** what real ratios produce is a several-fold delay, not an unbounded wait.

The mechanism itself is unchanged and still holds inside the model. What changed is its reach.

## What failed

**PRED-004 graded 5/10.** The informative failure is S8, which failed in the direction that weakens this project's own case: real-trace tails are *lighter* than the synthetic family used in earlier studies, not heavier. At matched E[k], synthetic p(k ≥ 64) was 0.00403 against PAI's 0.00164, and 0.00073 against Philly's 0.00035 — a factor of 2.1 to 2.5. **The synthetic setting had been favoring the starvation mechanism.** S3, S4, S7 and S10 also failed, all by overestimating the heaviness of real tails.

**The pre-registered retraction trigger did not fire, and should have.** It was conditioned on two predictions about *hypothetical* pool sizes, one of which passed. The per-VC measurement answered the same question more directly and pointed the other way. The seal's measurement was a poor proxy for the question it was meant to settle, so the commitment failed to bind — a way of being protected by one's own promise. Recorded as a method lesson: a seal should state in one line why its measurement is a valid proxy for the question.

**PRED-005 graded 9/10.** Only T6 failed: ratio invariance is an approximation, and the deviation is systematic in the direction that **larger pools are more dangerous** — at `m/N = 1.0`, flow balance is 0.390 at N = 64 but 0.236 at N = 128. Real virtual clusters run 217 to 603 GPUs, larger than anything measured here, so `r_safe` may be lower at real scale.

The decisive prediction T4 was deliberately named against this project's own claim — that at Philly's measured ratio the class would *not* starve. It passed, and the demotion followed automatically.

## Evidence boundary

**Supported:** In these two public traces, single-GPU jobs dominate, tails are thin, and no Philly virtual cluster receives a job requiring its full measured capacity. In the model, degradation across the half-to-full band is continuous with a usable boundary at 0.75, and at the measured ratio the class is delayed roughly sevenfold rather than starved.

**Not supported:** Only the *shape* of demand was taken from real traces. No policy was run on a real arrival stream, and the threshold experiment fed measured ratios into the synthetic model. Capacity was estimated from peak concurrency, not from published quotas. Two traces are not the population of GPU clusters. This measurement is retrospective on existing public data by an author holding prior expectations, so it is not a pre-registered forward evaluation and does not count as one.

## UNKNOWN

- How `r_safe` moves with load. At rho 0.7 the class still holds 0.856 flow balance at 0.875, so a heavier load lowers the boundary, but this was not measured finely.
- Whether the ratio-invariance deviation continues at N = 512 and 1024. Real virtual clusters sit in that region, and the deviation's direction is unfavorable.
- The same analysis on PAI quota groups, which needs the full trace rather than the 100K sample.
- Traces beyond Philly and PAI. Alibaba v2023 caps jobs at 8 GPUs per node and is not applicable.
- Interaction with non-zero preemption cost, still unmeasured.

## Falsification targets

- A published quota table for these virtual clusters shows capacities far below peak concurrency, which could put real jobs at or above their pool size after all.
- Another production trace contains a job class at or above its scheduling pool's capacity.
- A finer sweep finds a discontinuity inside the half-to-full band, which would restore a threshold reading.
- `r_safe` measured at 512 or 1024 servers falls below 0.59, which would put Philly's worst virtual cluster back inside the harmful region.

## Reproduce

### Quick artifact and grading check

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-phase
```

This verifies all four sealed digests, the gradings, and that no measured virtual cluster contains a pool-filling job.

### Full rerun

```bash
cd reproduction/gpu-scheduling-phase
python run_e6.py
python analyze_e6.py
```

The trace measurement itself requires the raw public traces, which are not redistributed here. `analyze_traces.py` is included, and `results/E5_traces.json` holds the derived per-trace and per-virtual-cluster measurements it produced. Obtain the traces from `msr-fiddle/philly-traces` and `alibaba/clusterdata`.

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-phase)
- [Sealed PRED-004, including the retraction condition that failed to bind](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-004.json)
- [Sealed PRED-005, including the decisive prediction and the demotion it triggers](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-005.json)
- [Derived trace measurements](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E5_traces.json)
- [E6 threshold sweep grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E6_grading.json)

## External audit

- Independent replications: 0
- Failed replications: 0
- Confirmed bugs: 0
- Open critiques: 0

## Next experiment

Measure `r_safe` at 64, 128, 256 and 512 servers. The one failed prediction of this study says ratio invariance does not hold and that the error runs toward larger pools being worse, while real virtual clusters are larger than anything measured so far. Whether Philly's 0.59 is genuinely on the safe side depends on that measurement.

## How this claim got here

<div class="revision-chain vertical" aria-label="How the GPU scheduling claim changed">
  <a href="/en/research/gpu-scheduling/"><b>EP-0001</b><span>Estimation error and restart cost reverse which scheduler wins.</span></a>
  <a href="/en/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>A good average hides a job class that never finishes; three stability detectors failed.</span></a>
  <a href="/en/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>Whole-cluster jobs, not mean gang size, decide when size-based scheduling breaks.</span></a>
  <a class="current" href="/en/research/gpu-scheduling-real-traces/"><b>EP-0004 &middot; current</b><span>Measured pools never met that condition; the harm is a several-fold delay, not starvation.</span></a>
</div>
