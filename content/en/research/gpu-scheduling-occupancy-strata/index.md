---
research_id: GPU-SCHED-EP-0034
title: "Keeping only the busy-GPU stratum at placement restores 77% of state coupling"
date: '2026-10-27'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Decision prediction D passed (one decision row scorable); 6/6 sealed predictions
evidence_level: Sealed synthetic experiment, single model; decision scored on one row
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-model
  source: E23 results and sealed prediction PRED-022
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One synthetic MSJ model with 64 GPUs in 8-GPU nodes, trace_like mix, first-fit placement; decision scored on one load-penalty row; mechanism candidate within the model only
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0034
source_episode_sha256: 838a51fd85bd0ca4c26e4d6694fd1db23a4bb2b0fd5ada41942eefff29fa3830
publication:
  status: publishable
tags:
- gpu-scheduling
- fragmentation
- sealed-prediction
- en
aliases:
- /research/gpu-scheduling-occupancy-strata/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-occupancy-strata/" hreflang="ja">日本語</a></p>

## Current finding

In the [previous Note](/en/research/gpu-scheduling-fcfs-residual/), about half of FCFS's extra fragmentation delay was state coupling a. In E23 we shuffled F's slowdowns only within "same need class and same stratum of busy GPUs at placement" (CO). That restored **77%** of a at (ρ, π) = (0.55, 0.2), at least half on every one of six seeds. Shuffling within coarse arrival-order blocks (CT) restored 6%.

Within this model, most of the state coupling is explained by "**fragmentation concentrates when the cluster is busy, and FCFS pays for it then**". This is a mechanism candidate, not an established mechanism.

## Key figure

d_X = log(J_X / J_CS) is the delay restored by keeping stratum X. A share d_X / a of 1 means that stratum alone reproduces F's delay. Means over six seeds (SE in parentheses).

| Row (ρ, π) | a | CO busy GPUs | CQ queue length | CT arrival block |
|---|---|---|---|---|
| (0.55, 0.2) decision row | 0.051 (0.005) | 0.039 (0.003) **0.77** | 0.032 (0.002) 0.62 | 0.003 (0.003) 0.06 |
| (0.6, 0.1) non-decision row | 0.019 (0.002) | 0.014 (0.002) 0.74 | 0.011 (0.002) 0.59 | 0.000 (0.002) 0.01 |
| (0.6, 0.2) | not scored (FCFS F, CO, CQ UNKNOWN) | | | |

Rank correlation of placement-time state with excess (extra nodes spanned). (0.6, 0.2), needs 2/4/8/16, range over six seeds.

| | Spearman(excess, busy GPUs) |
|---|---|
| FCFS BASE (π = 0, no slowdown) | 0.09–0.39 |
| FCFS F | 0.17–0.52 |
| SRPT F | 0.19–0.42 |

## What this research shows

- State coupling is carried mainly by how full the cluster was when a job was placed. Keeping five busy-GPU strata restores 77%; five queue-length strata restore 62%. The two quantities are correlated.
- Shuffling within coarse arrival-order blocks restores almost nothing (0.9 SE). This also serves as a control: shuffling within small groups does not by itself restore the delay.
- The non-decision row (0.6, 0.1) has the same shape (CO 0.74, CQ 0.59, CT 0.01).
- Fuller clusters fragment more even at π = 0 with no slowdown (S2). This is a known geometric relation.
- Under FCFS F, excess nodes per placement exceed π = 0 by 0.119 on average (SE 0.001, all six seeds; S4): slowdowns keep the cluster fuller, so later jobs land on a more fragmented cluster. This is the feedback direction.

## What this research does not show

- The share at (0.6, 0.2), the main row of EP-0032. Seed 2306 had α = 0.246, above the 0.2 threshold, so the row was UNKNOWN and not scored. The decision rests on (0.55, 0.2) alone.
- The effect of fine arrival order inside busy periods. CT uses five coarse blocks.
- Whether the remaining 23% is state variation inside strata or another link.
- Real clusters, other mixes, placements, penalty shapes. That fuller clusters fragment more is not new (Tiresias, Gandiva, Philly analyses, bin packing).

## Research question

The previous Note's shuffle CS (within need class) breaks two links at once: the link between a slowdown and the cluster state at placement, and the link with neighbouring jobs in arrival order. To see which carries a, we added an instrument that records the state at every placement, and three finer stratified shuffles.

- **CO**: class × busy GPUs at F's placement (five value-quantile strata, ties kept together)
- **CQ**: class × queue length at placement (five strata)
- **CT**: class × arrival-order block (five equal-count blocks); keeps only coarse drift in time, not state

## Why this matters

If state coupling comes from fragmenting when busy, placement under high occupancy is a lever against fragmentation cost in addition to less total work (the two were not compared). If it comes from arrival-order drift, the story differs. Controls that vary the shuffle unit separate the two.

## Method

Sealed experiment E23 (PRED-022). Synthetic MSJ model (64 GPUs, 8-GPU nodes, trace_like, exponential service, sticky first-fit, no migration). Rows (ρ, π) = (0.55, 0.2), (0.6, 0.2), (0.6, 0.1); new seeds 2301–2306; windows 160k/320k; 864 simulations, CPU only. Stability labels and existing arms are as in the previous Note.

The instrument records busy GPUs, queue length, free-GPU scatter and excess at every placement. It only reads state. Before sealing, with the instrument on, every field of the existing arms was reproduced exactly on four E22 tasks and RP = F held.

Decision prediction D: in every scorable decision row, d_CO ≥ 0.5a (at least one row scorable).

## Results

6/6 sealed predictions (P0, D, S1–S4). Four of 36 cells were UNKNOWN (11%), all FCFS at (0.6, 0.2) (F, RP, CO, CQ).

| | Prediction | Grade | Value |
|---|---|---|---|
| P0 | Instrument: FCFS RP equals F | PASS | relative difference ≤ 1e-9 |
| D | Decision: d_CO ≥ 0.5a | PASS | (0.55, 0.2) 0.77 (the only scorable row) |
| S1 | d_CO > d_CT | PASS | 0.039 vs 0.003 |
| S2 | BASE: Spearman(excess, busy) > 0 | PASS | 0.09–0.39 |
| S3 | Same under F (FCFS and SRPT) | PASS | 0.17–0.52 |
| S4 | FCFS F excess per placement > BASE | PASS | difference 0.119 (SE 0.001) |

The shuffled arms' work does not equal F's exactly, because slowdowns are paired with different sizes. At 320k the largest deviation over arms and rows is 0.131%, inside the ±1% declared in the seal.

## What changed

The term the previous Note only named "state coupling" now has a candidate content within this model: placements fragment more when the cluster is busier (geometry), and under FCFS those slowdowns keep the cluster fuller (feedback).

## What failed

- The main row (0.6, 0.2) could not be scored. Even at 320k, FCFS in that row does not fully settle on every seed.
- A read-only review before sealing found four defects, including a false statement in the seal text (that the shuffled arms have the same work as CS). All were fixed before sealing.

## Evidence boundary

One synthetic model, trace_like, first-fit; the decision rests on one row. Five strata are coarse, and strata are defined by F's state (the shuffled arm's own state differs). Before sealing, CO/CQ/CT values were viewed in a throwaway-seed 20k-window smoke run, after which CO was chosen as the decision arm and CT as its rival; grading-code test rows on throwaway data (seeds 9001–9006, 4k/8k windows; all PASS) were also viewed. The seal declares both. Seals are local git commits.

## UNKNOWN

- Whether the same share holds at (0.6, 0.2).
- The contribution of fine arrival order inside busy periods.
- What the remaining 23% is.
- Other mixes, placements, penalty shapes; real clusters.

## Falsification targets

- Scoring (0.6, 0.2) with longer windows gives d_CO < 0.5a.
- Finer CT blocks restore as much as CO or more. Then the active ingredient is closeness in time, and busy GPUs are only a proxy.
- Finer strata do not raise the share, or the result depends strongly on how strata are chosen.

## Reproduce

Run `python verify_state_coupling.py` in the [reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling). It checks PRED-022's digest, reruns the sealed grading code on the published E23 results, and re-simulates one FCFS task in C-058 mode (including CO/CQ/CT and the placement-state summaries) at the 160k window against the published values. The full 864 simulations run with `python run_e23.py` after moving `results/E23.json` aside.

## Evidence / Artifacts

The [package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-state-coupling) holds PRED-022 (sealed bytes), the instrumented simulator, `run_e23.py`, `analyze_e23.py`, and every E23 run record and grade. The private record's digest for PRED-022 was taken from a CRLF working copy; the published LF file differs from it only in line endings. The verifier checks both digests.

## External audit

No independent replication yet.

## Next experiment

Check whether the same share holds at (0.6, 0.2) with longer windows (320k/640k). Split CT into finer blocks to measure how much order inside busy periods matters.
