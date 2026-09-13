---
id: IAA-EP-0008
title: A 2x2 preparation-time x backward-CoM protocol for badminton smash biomechanics
date: 2026-09-13
domain: IAA / Badminton biomechanics
type: Protocol
status: Draft; not sealed; data collection not authorized
evidence_level: Design and power simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: protocol-and-power-sensitivity
  source: Public preregistration draft and Monte Carlo sensitivity analysis
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Prospective design only; no confirmatory observations
source_episode: IAA/EP-0008
source_episode_sha256: 6c12a0f9f82a62cac5b36509d4901d10cb9ffec458bcd873cb801fe54a5f9308
publication:
  status: publishable
tags: [protocol, biomechanics, badminton, preregistration]
---

<div class="evidence-strip"><span>Protocol</span><span>Draft, not sealed</span><span>No confirmatory data</span><span>Power assumptions uncalibrated</span><span>0 external replications</span></div>

## Summary

This protocol proposes a within-subject 2×2 experiment that independently assigns preparation time and backward center-of-mass state during a badminton overhead smash. It freezes the primary racket-velocity outcome, coordinate system, synchronized events, exclusions, hierarchical model, and model fallback order before confirmatory data collection. A Monte Carlo sensitivity analysis shows that interaction effects require substantially more participants than comparable main effects under the stated assumptions. Equipment feasibility, ethics, manipulation levels, empirical variance, minimum important effect, missingness, and final sample size remain unresolved, so the protocol is not sealed and does not authorize data collection.

## Research question

When assigned preparation time and assigned backward-CoM state are separated within the same skilled participant, how do they affect pre-contact racket-head velocity toward a fixed target?

## Why this matters

Observed preparation time, backward movement, skill adaptation, and racket outcome are entangled in retrospective swings. Independent assignment is needed to distinguish time pressure from body-state effects and to test whether skilled reorganization can compensate for a backward state.

## Competing hypotheses

- **H1:** short assigned preparation time reduces the primary velocity projection (`beta_T < 0`).
- **H2:** high assigned backward-CoM state reduces it (`beta_B < 0`).
- **H6:** within a successful braking/reorganization regime, high backward state may yield `beta_B > 0` or a condition-dependent interaction with consistent mechanistic outcomes. `beta_B = 0` alone does not support H6.

## Predictions

No confirmatory prediction is sealed. Placeholder `PENDING-2X2-EP-0007` remains intentionally unsealed until feasibility and design blockers are resolved.

## Method

- Within-subject 2×2: assigned preparation time (`long/short`) × assigned backward-CoM state (`low/high`).
- Assignment, not achieved value, defines the primary contrast; trials are never relabeled by their observed time or CoM.
- Ground axes: `+X` toward net center, `+Z` up, `+Y = +Z cross +X`; backward CoM is velocity projected on `-X`.
- Primary outcome: mean ground-frame racket-head velocity projected on a fixed target vector during `[-10,-2] ms` before contact.
- Cue: synchronized TTL rising edge. Contact: first visible shuttle/stringbed contact at at least 1000 fps. Ground contact: vertical GRF above 20 N for at least 10 ms.
- Primary model: trial-level linear mixed model with fixed time, backward state, interaction, order, and block; participant intercept and time/backward/interaction slopes.
- Co-primary terms use two-sided Holm familywise alpha 0.05. A fixed simplification order handles non-convergence or singularity.

Technical missingness is outcome-specific. A force-plate miss invalidates force-dependent outcomes but does not remove an otherwise valid contact-based racket outcome. The primary window is not interpolated, and low or unexpected outcomes are never excluded because of their value.

## Power sensitivity

The simulation assumes residual SD 1.0, participant random-slope SD 0.20, balanced complete cells, and Bonferroni alpha `0.05/3` as a conservative approximation to the planned Holm procedure. With six trials per cell:

| Contrast | Effect | Smallest tested N with power >= .80 |
|---|---:|---:|
| Main effect | 0.30 SD | 30 |
| Main effect | 0.40 SD | 20 |
| Interaction | 0.30 SD | >48; power 0.4988 at N=48 |
| Interaction | 0.40 SD | >48; power 0.7905 at N=48 |
| Interaction | 0.50 SD | 36 |

These values are sensitivity results, not a final sample-size decision.

## What changed

- A vague pre-impact direction became a fixed target-vector projection and `[-10,-2] ms` primary window.
- Assigned factors and achieved manipulation values were separated to prevent post hoc relabeling.
- A single fixed sample size was rejected because interaction power differs sharply from main-effect power.

## What failed

No empirical pilot currently supports the assumed random-slope SD or manipulation levels. Availability of synchronized 1000-fps video, TTL, force plates, and racket markers has not been demonstrated. The protocol therefore fails its execution gate today and remains a draft.

## Evidence boundary

**Supported:** The design is specified enough to expose its event, coordinate, exclusion, model, and power assumptions; the public simulation reproduces the stated sensitivity grid.

**Not supported:** Feasibility, ethics approval, an observed biomechanical effect, causal interpretation, final sample size, or confirmatory readiness.

## UNKNOWN

- Ethical/safety criteria and eligible skill level.
- Feasible `T_long/T_short` and backward-state manipulation geometry.
- Minimum manipulation margins and shuttle-feed tolerance.
- Empirical random-slope variance, technical missingness, attrition, and minimum important effect.
- Whether the interaction is confirmatory enough to determine sample size.
- Final code/environment hashes and the confirmatory data cutoff.

## Falsification targets

- Assigned time fails to separate achieved preparation time by the preregistered margin.
- Assigned backward state fails to separate `v_CoM dot (-X)` while holding time assignment.
- Synchronization or calibration cannot support the frozen event/window definitions.
- Pilot variability or missingness makes the current power grid materially optimistic.
- In a new confirmatory sample, `beta_B < 0` replicates under a successful manipulation, weakening H6.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick iaa
```

This reproduces the power calculation under the published assumptions. It does not reproduce an experiment because no confirmatory data exist.

## Evidence / Artifacts

- [Preregistration draft, power script, and output](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/badminton-biomechanics)
- Internal source Episode digest: `6c12a0f9f82a62cac5b36509d4901d10cb9ffec458bcd873cb801fe54a5f9308`

## External audit

- Independent replications: 0
- Failed replications: 0
- Confirmed bugs after publication: 0
- Open critiques: 0

## Next experiment

Run a feasibility pilot separate from the confirmatory sample to verify synchronization and orthogonal manipulation, estimate variance and missingness, choose a minimum important effect, decide whether interaction is co-primary, and only then seal the final protocol and sample size.
