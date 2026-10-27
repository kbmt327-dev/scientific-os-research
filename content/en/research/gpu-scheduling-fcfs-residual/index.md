---
research_id: GPU-SCHED-EP-0032
title: "About half of FCFS's extra fragmentation delay comes from slowdowns tied to cluster state"
date: '2026-10-27'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Decision prediction P2 passed and replicated on new seeds (thin margin); composition prediction P3 failed
evidence_level: Sealed synthetic experiments, single model; sealed replication on new seeds
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: E20-E22 results and sealed predictions PRED-019, PRED-020, PRED-021
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic MSJ model with 64 GPUs in 8-GPU nodes, trace_like mix, first-fit placement, three load-penalty rows; no real-cluster generalization
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0032
source_episode_sha256: 96438ae02cbbb411074130c15c9270577cae0972e48c056c604bb46ff6f72e1a
publication:
  status: publishable
tags:
- gpu-scheduling
- fragmentation
- sealed-prediction
- replication
- en
aliases:
- /research/gpu-scheduling-fcfs-residual/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-fcfs-residual/" hreflang="ja">日本語</a></p>

## Current finding

In this synthetic model at (ρ, π) = (0.6, 0.2), about half (0.52–0.56) of the extra delay FCFS suffers under node fragmentation is **state coupling, a**: the part that disappears when each job's slowdown is shuffled within its need class. It contains both the link between a slowdown and the cluster state at placement and the link with neighbouring jobs in arrival order. The sealed decision prediction "a is at least half" passed in E21 and again in E22, a sealed replication on seeds never used before.

The margin is thin. In E22 alone, three of six seeds went the other way. Pooling both experiments (12 seeds), the one-sided 95% lower bound on the margin is 0.0006. This bound is a precision estimate that includes E21's six seeds, whose thin margin prompted the replication; it is not an independent test. What the data support is "a is about half", not "a dominates". That a > 0 holds in all 18 seeds of all three rows.

## Key figure

Decomposition of FCFS's extra delay T = log(J_F / J_U). Means over six seeds (SE in parentheses).

| Row (ρ, π) | Experiment | T (total) | a state coupling | b within-class spread | c between-class composition | share of a |
|---|---|---|---|---|---|---|
| (0.6, 0.2) | E21 | 0.181 (0.013) | 0.102 (0.011) | 0.022 (0.005) | 0.058 (0.005) | **0.56** |
| (0.6, 0.2) | E22 replication | 0.171 (0.007) | 0.089 (0.005) | 0.016 (0.004) | 0.066 (0.006) | **0.52** |
| (0.55, 0.2) | E21 | 0.035 (0.005) | 0.056 (0.005) | 0.008 (0.002) | −0.029 (0.002) | 1.59 |
| (0.55, 0.2) | E22 replication | 0.038 (0.007) | 0.051 (0.006) | 0.007 (0.002) | −0.020 (0.002) | 1.34 |
| (0.6, 0.1) | E21 | −0.006 (0.002) | 0.018 (0.001) | 0.003 (0.001) | −0.027 (0.001) | — |
| (0.6, 0.1) | E22 replication | −0.004 (0.003) | 0.017 (0.002) | 0.002 (0.001) | −0.024 (0.001) | — |

Per-seed margin a − 0.5T at (0.6, 0.2): E21 all six seeds ≥ 0 (minimum 0.0001); E22 −0.0077, −0.0105, 0.029, 0.0149, 0.0007, −0.0035.

## What this research shows

A ladder of work-matched controls splits FCFS's fragmentation cost into three parts (RP, CM and U match F's GPU work exactly; the shuffled CS arm is within ±0.2% because slowdowns pair with different sizes).

- **a, state coupling**: shuffling each job's slowdown from the fragmented run F within its need class (CS) lowers FCFS mean JCT by about 9–10% at (0.6, 0.2). Each class keeps the same set of slowdowns; what is broken is which job received which slowdown, and when.
- **b, within-class spread**: small and positive.
- **c, between-class composition**: the bias that larger gangs slow down more. Its sign depends on load: positive at (0.6, 0.2), negative at (0.55, 0.2) and (0.6, 0.1). At π = 0.1 state coupling and composition cancel and T is near zero.

This restates, under an exact control, the EP-0030 observation that a gap of about 0.50 remained for FCFS after load matching. The two are defined differently (EP-0030 interpolated load in unit service time; here the control has the same work), so the numbers are not compared.

## What this research does not show

- What state coupling consists of. CS breaks two links at once: the link to the cluster state at placement, and the link to neighbouring jobs in arrival order. a contains both. The [next Note](/en/research/gpu-scheduling-occupancy-strata/) separates them.
- That a dominates. The margin sits at the resolution limit.
- Behaviour on real clusters, other mixes, placements or penalty shapes. π is a knob, not a measured cost.
- Novelty.

## Research question

Is the one FCFS gap that survived EP-0030 specific to fragmentation, or is it explained by added work? We ran the fragmented system (F) beside work-matched π = 0 arms. RP applies F's per-job slowdowns as they were (an instrument check: for FCFS it must equal F); CS shuffles them within need class; CM uses each class's work-weighted mean; U uses the overall mean. a = log(J_F/J_CS), b = log(J_CS/J_CM), c = log(J_CM/J_U), and T = a + b + c.

## Why this matters

If fragmentation hurt only by adding work, placement could do no more than reduce the total. If the link to state matters, *when* a job lands on a fragmented cluster matters too. Only a same-work control separates the two.

## Method

Three sealed experiments in sequence, all in one synthetic MSJ model (64 GPUs, 8-GPU nodes, trace_like mix, exponential service, sticky first-fit, no migration, slowdown rate = 1/(1 + π·excess)). Rows (ρ, π) = (0.55, 0.2), (0.6, 0.2), (0.6, 0.1), six seeds each. A cell is labelled STABLE only when all six seeds agree, using α, the elasticity of mean JCT with respect to the observation window, between two windows.

1. **E20** (PRED-019): 40k/80k windows, 648 simulations. One post-seal fix: the first run finished all simulations, then crashed while writing JSON; only the writer's argument was changed and the run repeated (simulation and grading untouched, first-run values not read; the simulation is deterministic).
2. **E21** (PRED-020): same predictions and thresholds, windows lengthened to 160k/320k, new seeds 2101–2106. Before sealing, stability labels alone were checked on separate seeds with the production seed count (that pilot's JCT was not viewed). However, after grading E20, per-arm JCT at 40k/80k had been displayed as a diagnostic, from which the direction of the decomposition (F > CS ≈ CM > U) was roughly visible. PRED-019's predictions and thresholds were fixed before that display and were not changed for E21.
3. **E22** (PRED-021): E21's predictions, thresholds, cells and windows unchanged, new seeds 2201–2206. Decision R1: P2 passes on new seeds. The seal states that R1 passes about half the time even when the true margin is zero, so it is reported with R2, a positive one-sided 95% lower bound on the pooled 12-seed margin.

## Results

- **E20**: unscorable. 14 of 27 cells were UNKNOWN (14 of the 15 FCFS cells with π > 0; U at (0.6, 0.1) was STABLE). Only the instrument check P0 (RP = F) passed; P1–P5 could not be scored. α split across seeds from −0.48 to 0.97 in the same configuration, with the same seed pattern in every arm: near effective load 0.7–0.8, FCFS does not settle in those windows. At that point the EP-0030 gap of 0.50 was downgraded to "not established".
- **E21**: 5/6 sealed predictions, decision P2 passed, all 27 cells STABLE. P3 (c positive in every decision row) failed.
- **E22**: R1 passed (share 0.52 and 1.34), R2 passed (pooled lower bound 0.0006; mean 0.0075, SE 0.0039), R3 (E22 alone, reported only) failed (lower bound −0.0087). Re-grading with PRED-020's wording gave the same 5/6 as E21.

## What changed

- The FCFS-only gap from EP-0030 was downgraded to "not established" after E20, and restated after E21 as real under an exact control.
- E21's P2 pass replicated on new seeds. Because the share is 0.52–0.56, it is written as "a is about half".

## What failed

- E20's windows were too short to score. The cause was building on stability labels that agreed over a few seeds only. Since then, cells an experiment depends on are first labelled with the production seed count.
- P3 (composition term positive) failed; its sign changes with load.
- In E22 alone, half the seeds had a negative decision margin.

## Evidence boundary

One synthetic model, trace_like, first-fit, three rows. Seals are local git commits with no external timestamp. Predictions and grading code were written by the same author; independent replications: 0. SRPT's U arm uses the final rate of re-placed jobs and is approximate, so SRPT values are not interpreted.

## UNKNOWN

- How much of state coupling is occupancy at placement and how much is arrival-order adjacency (partly separated in [EP-0034](/en/research/gpu-scheduling-occupancy-strata/)).
- Where and why the composition term c changes sign.
- Other mixes, placements, penalty shapes; real clusters.

## Falsification targets

- With new seeds or longer windows, the share of a at (0.6, 0.2) falls clearly below 0.5 (a pooled upper bound below 0.5).
- A seed with a ≤ 0 appears. So far all 18 seeds are positive.
- Changing how the same-work control is built (for example, the shuffle unit) makes a vanish.

## Reproduce

Run `python verify_state_coupling.py` in the [reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling). It checks the four sealed prediction digests, reruns the sealed grading code on the published E20–E23 results, and re-simulates two tasks at the 160k window against the published values (about two minutes on one core). The full 2,808 simulations run with `run_e20.py` to `run_e23.py`.

## Evidence / Artifacts

The [package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling) contains sealed predictions PRED-019 to PRED-022, the simulator, runners, grading code, and every E20–E23 run record and grade. The simulator is the private working repository's version at the E23 seal. Before sealing, it reproduced every field of the existing arms on four E22 tasks; the verifier re-simulates one E21 FCFS task against the published values.

## External audit

No independent replication yet. Seals are local records; a third party cannot verify their timing.

## Next experiment

State coupling was split by placement-time state in [EP-0034](/en/research/gpu-scheduling-occupancy-strata/). Confirming the share at (0.6, 0.2) needs longer windows (320k/640k).
