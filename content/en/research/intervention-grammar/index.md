---
research_id: INTERVENTION-EP-0001
title: When the predictor also acts, the observational prediction contract breaks in five places
date: 2026-09-14
lang: en
domain: Research Instrument
type: Method
status: exploratory
evidence_level: contract validation only (zero scored predictions)
peer_reviewed: false
independent_replications: 0
evidence:
  class: contract-validation
  source: nine contract invariants and one refused counter-example each; no intervention prediction has been scored
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: the prediction contract of a seal-and-score research instrument, restricted to domains where the predictor is also the actor; no claim about any application field
replication:
  independent: 0
  failed: 0
source_episode: INTERVENTION-GRAMMAR/EP-0001
source_episode_sha256: 3b18a130f97481ccdd02226609c7d20a5a46a8397acb9a8771dfbff555496880
publication:
  status: publishable
tags: [method, contract, intervention, instrument]
---

<p class="research-area"><b>The instrument itself</b><span>Can a seal-and-score apparatus be carried into domains that require acting</span><a href="/ja/research/intervention-grammar/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Method</span><span>Contract validation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## What this method does

Sealing a prediction first and scoring it when the date arrives quietly assumes that **the observer does not move what is being observed**. Ours was built that way too. All four running domains are non-interventional, so the assumption had never been tested.

An external user tried to apply the instrument to a domain where the predictor is the one acting, and reported that **the assumptions break in five places**.

| # | Breach | What goes wrong |
|---|---|---|
| B1 | Attribution | A miss cannot be split into **"the model was wrong"** and **"nobody acted"** |
| B2 | Reflexivity | Predictor and actor are the same, so **you can go and make your own prediction false** |
| B3 | Exogenous due date | The scoring date is not yours to choose |
| B4 | Waiting | Under observation "wait" is a legitimate ending; under intervention it is a stall |
| B5 | Non-stationarity | Success moves the distribution. The quantity being measured responds to your own actions |

This method answers each with **a field and an invariant that refuses the record** — not a convention someone has to remember, but a form in which the violating record cannot be written.

## Key figure

<div class="ratio-figure" aria-label="Observational contract versus intervention contract"><div class="ratio-track"><i style="left:38%"></i><i style="left:100%"></i></div><div class="ratio-labels"><span style="left:38%"><b>Observational</b> target, unit, interval<br>when the outcome can be read, retraction rule</span><span style="left:100%"><b>plus intervention</b> action, actor, channel and direction<br>commitment stamp, expected time, baseline cross-section<br>whose the due date is, resume deadline, interference stance</span></div></div>

## Method

### Fixed on the action side

`action` / `actor` / `channel` and `direction` (which quantity moves, which way) / `decided_at` (**when we committed**) / `expected_at` (when the effect becomes readable) / `baseline_as_of` (**the cross-section the effect is measured against**) / `due_kind` (is the scoring date ours) / `resume_deadline` (an end to the waiting) / `stance` (below) / `side_effects` / `not_taken`.

### Required on the scoring side

A **four-point joint**: did the threshold cross, did a decision open, was the action executed, what was the result. An acting prediction cannot be scored without it. **"No decision was ever opened" is itself one of the recorded results.**

### How self-interference is handled

The stance is declared at seal time.

- **`commitment`** (predicting the result on the premise of acting): scored on the four-point joint. **If the action was never executed, that is not a refutation of the model.**
- **`non_interference`** (predicting while pledging not to act): a broken pledge forces an unresolved verdict. Being right does not earn a score.

We declined the option of **counting it as a success including the intervention**. Allowing that would make the ledger unable to separate a good model from a good operator, and the former is what the instrument is trying to measure.

## What changed

- The intervention spec and the four-point joint were added, with **one invariant per breach, B1 through B5**.
- "The scoring date never came" became a distinct outcome, excluded from the score count. It used to be absorbed into "insufficient evidence", so **"the date never came" and "the date came but we could not measure" looked identical** in the ledger. Rare enough to be harmless under observation; routine under intervention.
- Self-interference was settled by **a declaration made at seal time**.
- Predictions without an intervention are **byte-for-byte unchanged**. Not one existing sealed prediction hash moved.

## What failed

The first implementation put the gate — a prediction whose date never came cannot be scored — **only on the outcome**. But promotion reads the **evaluation record**, not the outcome. So the path "outcome: not due, evaluation: supported" walked straight past the gate and on into model promotion.

This is the exact weakness written down in our own documentation: **implement an isolation as one gate per condition you want to protect, and a path that grows later will not pass through it. Gates are needed per path that touches the condition, not per condition.** This was the third time we made the same shape of leak.

A second gate on the evaluation side closed it, and then **every path that could touch the condition was enumerated** and pinned in tests. The enumeration found that the instrument has two separate status universes with no converter between them; the outcome "never came due" is structurally unreachable in one of them, and an unrecognised value there fails closed at every gate.

## What this method establishes

- The contract actually refuses the nine counter-examples listed below.
- Sealed content of non-intervention predictions is unchanged.
- "Never came due" does not enter the score count.

## What this method does not establish

- **That five is the complete set of breaches.** The list was counted by the external user, not independently recounted here. Whether a sixth exists is unknown.
- **That the grammar suffices for real intervention research.** No prediction sealed in this form **has yet reached a scoring date**.
- Anything about any application field. None is included here.

## Research question

What is the **minimal addition** to an observational prediction contract that lets it carry intervention? Does adding one grammar suffice, or do the stopping conditions and the scoring format need to branch as well?

## Why this matters

Instruments that seal and score appear to accumulate records mainly where **outcomes are cheap and fast to observe**. Where observation is expensive — and especially where moving the project forward is itself the goal, so intervention is unavoidable — such instruments tend to decay into narrating after the fact. Separating "that decay is the instrument's limit" from "the grammar was simply missing" requires ruling out the grammar first.

## Results

| Breach | Records refused | Counter-examples |
|---|---|---|
| B1 | Scoring without the four-point joint; claiming supported/refuted when no decision opened; recording an execution with no decision | 3 |
| B2 | A commitment stamped after registration; a non-interference pledge by someone who cannot interfere; scoring after a broken pledge | 3 |
| B3 | An exogenous due date with no end to the waiting | 1 |
| B4 | A resume deadline that falls before the effect is expected | 1 |
| B5 | Calling a quantity measured after the decision a baseline | 1 |

All nine refused; all three positive checks hold.

## Evidence boundary

Contract validation only. **Zero scored predictions**, zero independent replications, no domain-expert review. No application-domain data entered this work at any point.

## UNKNOWN

- Whether a sixth breach exists.
- Whether **the not-due rate itself needs a sealed ceiling**. Under intervention the date failing to arrive can become routine, and an instrument whose predictions all end that way has not scored anything.
- Whether stopping conditions and the scoring format also need to branch. Only the grammar was added; both remain shared with the observational path.
- The instrument's other internal path — the one its domain adapters use — has nowhere to write an action at all. That side is untouched.

## Falsification targets

- Someone writing an intervention prediction in this grammar reports **even one breach with nowhere to write it**.
- Sealing still does not progress in an intervention domain after the grammar is added. That would place the rate limit elsewhere: on a predicate that exists in no data column, or on an organisational authority boundary. **We consider this the likelier of the two.**

## Reproduce

```bash
python scripts/reproduce.py --quick intervention
```

Or from that directory:

```bash
python tests/validate_intervention_grammar.py
```

What is published is an independent implementation running on the standard library alone. The internal research runtime is not public, so **agreement between the two is asserted here, not demonstrated.**

## Evidence / Artifacts

- [Contract implementation, validator, counter-examples](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/intervention-grammar)
- Internal source episode hash: `3b18a130f97481ccdd02226609c7d20a5a46a8397acb9a8771dfbff555496880`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

An intervention prediction written in this grammar reaching its first scoring date. Until then, all that stands here is that records which ought to be refused are refused.
