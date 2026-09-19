---
research_id: GPU-SCHED-EP-0026
title: When should a stationary diagnostic refuse a permanent parameter transition?
date: '2026-09-19'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Bounded synthetic transition audit; general claims UNKNOWN
evidence_level: Synthetic known-model control
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: Sealed transition manifest and same-design executable reproduction
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One permanent parameter change with truthful provenance; eventual-tail
  label; no undeclared-drift detector or real-GPU claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0026
source_episode_sha256: 2485e3ee2146b9c93df5594c0d1dd5cd8ce0e2bb3dd0570777f20cfea02dcc1f
publication:
  status: publishable
tags:
- gpu-scheduling
- model-drift
- applicability-gate
- en
aliases:
- /research/gpu-scheduling-transition-refusal/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-transition-refusal/" hreflang="ja">日本語</a></p>

## Current finding

With a truthful permanent-transition manifest, the stationary diagnostic refused all240 transition looks as UNKNOWN before inference. Falsely declaring the same data stationary produced80/80 wrong-side decisions at the first100k look.

## Key figure

![Wrong-side and UNKNOWN counts under a false stationary declaration](/assets/gpu-scheduling-transition-refusal.svg)

Two models times10seeds. Solid: wrong side; dashed: UNKNOWN; maximum20 per series.

## What this research shows

For a sealed synthetic one-change process with truthful provenance, applicability refusal blocks wrong eventual-tail declarations from a stationary diagnostic.

## What this research does not show

No data-driven detection of undeclared drift, new time-varying stability theorem, general U31, nonexponential/real-GPU transfer, established novelty, peer review or external independent replication.

## Research question

After arrival80000, arrival or service rates change once and remain fixed forever. Reports occur at100k,160k and320k arrivals.

## Why this matters

Cumulative full-history statistics mix pre- and post-change regimes. Narrow stationary intervals can target the wrong long-run side after stationarity has failed.

## Method

64 fungible resources, needs32/64, strict nonpreemptive FCFS, two parent models and seeds9301–9310. Existing exact two-class capacity labels the stationary regime that persists forever after the finite change; equality is excluded. The truthful gate sees a transition manifest. Only the misuse arm receives a false stationary attestation.

## Results

| Scenario | Tail truth | H | False scheduled wrong/UNKNOWN/correct | False anytime wrong/UNKNOWN/correct |
|---|---|---:|---:|---:|
| arrival_up | overloaded | 100k | 20/0/0 | 20/0/0 |
| arrival_up | overloaded | 160k | 20/0/0 | 16/4/0 |
| arrival_up | overloaded | 320k | 0/0/20 | 0/0/20 |
| arrival_down | subcritical | 100k | 20/0/0 | 20/0/0 |
| arrival_down | subcritical | 160k | 0/0/20 | 0/2/18 |
| arrival_down | subcritical | 320k | 0/0/20 | 0/0/20 |
| service_degrade | overloaded | 100k | 20/0/0 | 20/0/0 |
| service_degrade | overloaded | 160k | 20/0/0 | 0/0/20 |
| service_degrade | overloaded | 320k | 0/0/20 | 0/0/20 |
| service_improve | subcritical | 100k | 20/0/0 | 20/0/0 |
| service_improve | subcritical | 160k | 20/0/0 | 20/0/0 |
| service_improve | subcritical | 320k | 20/0/0 | 0/20/0 |

All120 stationary control looks were correct under the truthful gate. All240 transition looks were refused without inference. At100k, all80 drift records were wrong for both false-declaration methods. At320k, only service improvement remained: scheduled20/20 wrong, anytime20/20 UNKNOWN.

## What changed

Draftv0.6 adds model applicability before diagnostic accuracy.

## What failed

The declaration gate cannot detect a lying or missing manifest from data. Under service improvement, cumulative-history contamination remained for the scheduled method at320k.

## Evidence boundary

120 workloads,360 fixed looks,1080 method outcomes and5/5 sealed predictions. Seal/source chronology, post-regime exact labels, gate states and36cell aggregates were recomputed.

## UNKNOWN

Gradual/repeated/adaptive change, changing p, structural change, real-log provenance, external-reader comprehension and demand remain UNKNOWN. General detectors: zero.

## Falsification targets

Refusal depends on truthful provenance. Eventual-tail stability is not finite-window queue state and cannot be transferred to another time-varying definition.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-transition-refusal): `python runner_transition.py --verify-recorded --seeds 2` recomputes360 recorded looks and regenerates24 small looks.

## Evidence / Artifacts

[summary, generator, gate and runner](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-transition-refusal). This is a reviewed projection, not original sealed bytes.

## External audit

External independent replications: zero. Linux CI repeats the same design; it is not an independent study.

## Next experiment

Specify an external-reader test of whether truthful/false declarations and the eventual-tail label can be explained and rerun without author assistance.

[[en/research/gpu-scheduling-exposure-checkpoints/index|EP-0025]] → EP-0026
