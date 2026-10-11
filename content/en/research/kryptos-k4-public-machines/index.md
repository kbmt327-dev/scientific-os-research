---
research_id: KRYPTOS-K4-EP-0206
title: K4 matches in public machine families are bounded to finite recorded settings
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: Zero exact passes in several registered finite families; full sweeps and nulls remain source-record results
evidence_level: Public rerun of machine components and small slices plus recorded large searches
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public machine models, small checks, and aggregate records from EP-0193 through EP-0215
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Finite settings stated in EP-0193 T2, EP-0203, EP-0206, EP-0207, EP-0209, and EP-0215
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0206
source_episode_sha256: 91d9dd2ac17c054b8bae47719c13f152edf0fca3f2be151eff67ebd38a287984
publication:
  status: publishable
tags:
- kryptos-k4
- public-machines
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-public-machines/" hreflang="ja">日本語</a></p>

## Research question

Did the recorded finite settings in several publicly specified rotor-machine families produce a crib match? The records cover EP-0193 T2, EP-0203, EP-0206, EP-0207, EP-0209, and EP-0215.

## Why this matters

A large state space still depends on its wiring, entry reading, placement, and scoring rule. Separating registered conditions from what the public verifier reruns prevents a zero from becoming a claim about machine ciphers in general.

## Method

The public package checks machine test vectors, stepping classes, wiring invariants, entry readings, small planted and K4 slices, setting counts, and chance formulas. Full CPU/GPU searches, nulls, and the EP-0207 confirmation statistic remain in the source records and are not regenerated.

## Results

| Record | Finite source-record result |
|---|---|
| EP-0193 T2 | 111,209,679,360 settings; K4 passes 0 |
| EP-0203 | Main family 487,118,136,960; K4 settings with h≤2: 0; 10 nulls |
| EP-0206 | 38,167,161,956,352 settings; K4 settings with h≤2: 0; looser h≤12 clusters are recorded |
| EP-0207 | Post-hoc sensitivity observation unconfirmed; recorded p=0.415 |
| EP-0209 | 61,165,323,648 settings; K4 passes 0; recorded E=4.35×10⁻⁷ |
| EP-0215 | 733,983,883,776 settings; registered passes 0; recorded E=0.0331 and smallest null comparison P=0.07 |

These are results under separate registered conditions, not one combined test.

## Current finding

The source records report no registered pass in several stated finite families. EP-0206 also records clusters under a looser threshold, and the EP-0207 post-hoc observation was not confirmed.

## Key figure

| Check | Scope | Recorded result | Public verification |
|---|---:|---|---|
| EP-0203 | about 4.87×10¹¹ settings | h≤2: 0 | Counts and small checks |
| EP-0206 | about 3.82×10¹³ settings | h≤2: 0; looser clusters recorded | Partial checks |
| EP-0209 | about 6.12×10¹⁰ settings | 0 passes | Record only |
| EP-0215 | about 7.34×10¹¹ settings | 0 registered passes | Record only |

## What this research shows

- The recorded negatives apply to the stated finite settings and criteria.
- The public verifier reruns some machine components and small checks.
- Full searches and full null generation are outside the public verifier.

## What this research does not show

It does not show that other wirings, machines, or crib placements fail. It does not establish a solution to K4, statistical significance, or independent replication. The post-hoc EP-0207 observation is not treated as a confirmed detection.

## What changed

Large recorded outcomes and the small checks reproduced publicly are now reported separately. The note no longer implies that the full searches were rerun.

## What failed

The full searches, null generation, and confirmation statistic are not rerun in this package. The post-hoc EP-0207 sensitivity observation did not receive confirmation.

## Evidence boundary

The public verifier checks test vectors, machine invariants, setting counts, chance formulas, and small slices. Large CPU/GPU sweeps, nulls, and confirmation statistics remain source-record results. New plaintext: 0. Independent replications: 0.

## UNKNOWN

It is not verified here whether an independent implementation of the full searches would preserve their recorded outcomes. This work says nothing about methods outside the stated families.

## Falsification targets

A complete registered match, or a demonstrated error in the implementation, setting counts, or crib scoring, would require revising the relevant finite-family result.

## Reproduce

From the package directory, run python -B verify_public_machines.py. This roughly 10-second partial check does not rerun the full searches.

## Evidence / Artifacts

The public package at reproduction/kryptos-k4-public-machines contains check code and numeric results. It includes no plaintext or planted strings.

## External audit

There are zero independent replications. No expert review or peer review has occurred.

## Next experiment

If needed, use a small independent implementation to check the public machine components and setting counts under the registered conditions. Do not extend this result to unrun large searches.

## Sources

- Public K4 information: [CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- Source records: KRYPTOS-K4/EP-0193 T2, EP-0203, EP-0206, EP-0207, EP-0209, and EP-0215