---
research_id: FRONTIER-METRICS-REVIEW-0001
title: Two ways a synthetic world flatters its author, and both headline results withdrawn
date: 2026-09-15
lang: en
domain: Measurement Design
type: Negative Result
status: retracted
evidence_level: synthetic; the withdrawn claims and the tests that withdrew them are both published
evidence:
  class: synthetic-retraction
  source: five sealed prediction families, and the two adversarial sweeps that took down two of the headline results
peer_reviewed: false
independent_replications: 0
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: measurement-design claims obtained on a generative world of our own construction; no real data of any kind was used and no claim about any application field is made
replication:
  independent: 0
  failed: 0
source_episode: FRONTIER-METRICS/REVIEW-0001
source_episode_sha256: f92531bdfbd2e510a7f401ea3b57860164ba84e344bb324baf6bbf79ef4ad4c4
publication:
  status: publishable
tags: [negative-result, measurement, retraction, simulation]
---

<p class="research-area"><b>Measurement design</b><span>How to doubt a result that came out of a world you built yourself</span><a href="/ja/research/retracted-frontier-metrics/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Negative Result</span><span>Synthetic</span><span>Retracted</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## Research question

We were testing, on a generative world, whether the rate at which work settles
into a machine can be read off a queue of undecided items. Five sealed
prediction families in, two results were on the banner:

1. **The settling rate is blind to the frontier** — to whether novel types keep
   arriving forever.
2. **Whether the frontier ever closes can be decided from ten thousand records.**

**Both are withdrawn.** This note is how they broke, and what broke them.

## Why this matters

Both had the same shape: a claim of ours, holding on a world of ours, on top of
a constant of ours. **A synthetic world flatters its author, and the flattery
has forms. Name the form and you can test for it.**

The two forms generalise well past this subject. One is **fixing the only thing
that drives the quantity you are measuring**. The other is **pinning an
unobservable nuisance at a single value and publishing the result as a function
of sample size alone**.

## Method

Each claim was turned into a sweep over a quantity that had been held at one
value when the claim was published. A robust claim survives its sweep.

## What failed

### One: the metric was pinned by a constant we chose

In this world there is exactly **one** route by which a judgement fails to
become a reusable rule: the probability that a person calls it a one-off. We had
it fixed at 0.05. Sweep it.

| constant `p` | `1 − p` | settling rate (frontier closes) | settling rate (frontier open) | gap |
|---|---|---|---|---|
| 0.02 | 0.98 | 0.9674 | 0.9781 | +0.0108 |
| 0.05 | 0.95 | 0.9530 | 0.9486 | −0.0044 |
| 0.15 | 0.85 | 0.8720 | 0.8584 | −0.0136 |
| 0.30 | 0.70 | 0.7587 | 0.7322 | −0.0265 |

**The constant we picked moves the settling rate by 0.209. The frontier moves it
by at most 0.027, and the sign does not hold. A factor of 7.9.**

> **We did not find that the settling rate is blind to the frontier. We built a
> world in which it cannot see anything, and reported the blindness.**

The first version of this test asked whether the settling rate stayed within an
absolute tolerance of `1 − p`. **That threshold was badly placed too** — the
offset grows with `p`, so a fixed tolerance hides the point. The right
comparison is **how far our own constant moves the metric against how far the
thing we claimed to measure moves it.**

### Two: the decision line belonged to an unobservable, not to sample size

Whether the frontier closes is read from the slope of the growth in distinct
types. We characterised the estimator's null **at a base novelty of 30** and
published a decision line of **0.283** as though it were a function of sample
size.

Sweep the base novelty. **Every world below has a frontier that fully closes,
and every one has ten thousand records.**

| base novelty | estimate on a closing frontier | clears the published line of 0.283? |
|---|---|---|
| 5 | 0.1564 ± 0.0325 | — |
| 15 | 0.1918 ± 0.0352 | — |
| **30** | **0.2065 ± 0.0202** | — ← the only value we looked at |
| 100 | **0.2884** ± 0.0121 | **clears it** |
| 300 | **0.3837** ± 0.0092 | **clears it** |

For reference, at a base novelty of 30 a genuinely open frontier estimates
**0.3947**.

**At 100, a frontier that fully closes clears the line we published. At 300 it is
indistinguishable from one that is genuinely open.** The base novelty is a
property of the subject and is not observable from outside.

⇒ **"Ten thousand records is enough" is not a usable recipe as it stands.** The
nuisance parameter has no place in it.

## What changed

- Both headline results withdrawn, **with the original wording kept in place and
  marked as withdrawn**.
- Only what survives is claimed again.

**What survives**: rule reuse is 431.5 where the frontier closes and 14.6 where
it does not — a factor of **0.034**. That is not one of our constants; it follows
from the type distribution. So the claim stands in this weaker form: **reuse and
the settling rate are different quantities, and only the former responds to the
frontier.** The stronger form — that the settling rate is *specially* blind — does
not stand.

**What fell**: "the settling rate is blind to the frontier", and "ten thousand
records decides it".

## Evidence boundary

Synthetic. The mechanism family is ours. No real data of any kind was used, and
no claim about any application field is made. **What this note demonstrates is
how two published claims were withdrawn — not that anything was learned about
the subject itself.**

This review is a self-review. **An attack we did not think of is, by
construction, not in it.**

## UNKNOWN

- Whether the claim survives in a world where the settling rate *can* move — one
  where a person's willingness to generalise depends on novelty. The withdrawn
  claim has not been rebuilt into a testable form.
- Whether the nuisance and the quantity of interest can be estimated jointly. The
  growth curve carries both in its shape and not only in its slope, so it should
  be possible; it is not implemented.
- How sensitive the estimator is to how a type is defined. **If that gives way,
  the whole of the second result goes with it.**

## Falsification targets

- If a world with several routes driving the settling rate still leaves it
  unresponsive to the frontier, the first retraction went too far.
- If the nuisance can be estimated jointly, the second is not a retraction but a
  missing step in the procedure.

## Reproduce

```bash
python scripts/reproduce.py --quick frontier
```

Or from that directory:

```bash
python tests/reproduce_retractions.py
```

What is published is a standalone implementation on the standard library alone,
and the two sweeps themselves.

## Evidence / Artifacts

- [The world, both attacks, and the surviving result](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/frontier-metrics)
- Internal source record hash: `f92531bdfbd2e510a7f401ea3b57860164ba84e344bb324baf6bbf79ef4ad4c4`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Rebuild the world so that the settling rate *can* move, and re-seal the withdrawn
claim in a form that can be tested. Then joint estimation of the nuisance and the
quantity of interest. Until both are done we will not recommend this measurement
design to anyone.
