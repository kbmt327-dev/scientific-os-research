---
research_id: KRYPTOS-K4-EP-0200
title: Recorded results and verification limits for finite square-list families
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: Zero matches in the recorded finite families; public verification checks only inventory and null arithmetic
evidence_level: Numeric source-record projection and lightweight inventory/histogram checks
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public input inventory and numeric records from EP-0193 T1, EP-0199, EP-0200, EP-0201, EP-0205, and EP-0228
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Recorded finite list families and mismatch criteria defined by each episode; no public rerun of candidate searches
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0200
source_episode_sha256: 49b73d5dc511003122bff8d840cda15b61563d25fb07c0c9eecdf3c840a08305
publication:
  status: publishable
tags:
- kryptos-k4
- square-lists
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-square-lists/" hreflang="ja">日本語</a></p>

## Research question

What do the recorded results show for finite families combining square lists, pairings, segment starts, and Bifid settings? The records cover EP-0193 T1, EP-0199, EP-0200, EP-0201, EP-0205, and EP-0228.

## Why this matters

The candidate families and null samples differ. Separating source-record results from what the public package actually checks keeps small samples and an incomplete package from being overstated.

## Method

I projected only numeric minima, registered pass counts, null sample sizes, and histograms from the source records. The public verifier checks counts of places, seeds, squares, pairings, modes, starts, settings, and arithmetic in the recorded histograms. It does not run candidate searches or generate nulls.

## Results

| Record | Source-record result | Null sample |
|---|---|---|
| EP-0193 T1 | Exact passes 0; no public scan | — |
| EP-0199 | Minimum mismatch 13; exact passes 0 | n=200; 0.975 at or below observed |
| EP-0200 | Minimum mismatch 11; exact passes 0 | n=10; 0.10 at or below observed |
| EP-0201 | Joint minimum mismatch 8; h≤2 passes 0 | n=2,000; 0.189 at or below observed |
| EP-0205 | Minimum mismatch 14; exact passes 0 | n=20; 1.00 at or below observed |
| EP-0228 | 48,608,736 settings; minimum mismatch 15; passes 0 | n=20; 1.00 at or below observed; recorded P=1.00 |

Each share is the fraction at or below the observed statistic in that source record's finite null sample, not an independent p-value. Samples of 10 or 20 provide limited precision.

## Current finding

The source records report no registered pass in the stated finite families. Null distributions vary by episode, and some samples are small. The public verifier does not reproduce these searches.

## Key figure

| Public input inventory | Count |
|---|---:|
| Places | 146 |
| Keyword seeds | 40 |
| Unique squares | 185 |
| Pairings | 48 |
| Adjacent modes | 3 |
| Segment starts | 6 |
| Bifid settings | 2,765 |

## What this research shows

- Numeric finite-search and null summaries can be checked against the source records.
- The stated records report no exact or registered pass.
- The lightweight public check covers inventory counts and aggregate arithmetic only.

## What this research does not show

It does not reject square ciphers generally, unregistered lists or rules, or K4 as a whole. The null shares do not establish independent replication or general significance. Candidate scans, including EP-0193 T1, are not rerun.

## What changed

The incomplete package now contains a numeric projection of the recorded results plus lightweight inventory and histogram checks. The source-record negatives remain intact, while the lack of public search reruns is stated separately.

## What failed

The package does not rerun candidate searches or regenerate nulls. EP-0193 T1 has only a result record; its corresponding public scan is absent.

## Evidence boundary

Evidence is limited to recorded numeric results, public input counts, and internal histogram arithmetic. New plaintext: 0. Independent replications: 0. Null shares are descriptive fractions from finite samples.

## UNKNOWN

It is unverified whether independent candidate scans or null generation would preserve the recorded values. Small null samples cannot characterize their distributions precisely.

## Falsification targets

A rerun under the same registered rules that finds a matching candidate, or an error in a recorded minimum, histogram, or setting count, would require updating the corresponding result.

## Reproduce

From the package directory, run python -B verify_square_lists.py. It checks inventory counts and five histogram totals and shares only; it does not run the candidate search.

## Evidence / Artifacts

The public package at reproduction/kryptos-k4-square-lists contains the inventory, numeric results, and lightweight verifier. It contains no decoded strings or grids.

## External audit

There are zero independent replications. No expert review or peer review has occurred.

## Next experiment

Use an independent implementation to check a small registered subset, then plan full scans and null reruns only if needed. Do not infer general probabilities from the small recorded null samples.

## Sources

- Public K4 information: [CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- Source records: KRYPTOS-K4/EP-0193 T1, EP-0199, EP-0200, EP-0201, EP-0205, and EP-0228