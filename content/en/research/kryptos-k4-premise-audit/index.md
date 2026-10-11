---
research_id: KRYPTOS-K4-EP-0188
title: Auditing K4 premise records while separating settled counts from unknowns
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Finding
status: Count and row discrepancies remain; search findings are limited to recorded finite families
evidence_level: Aggregate-record consistency check; no candidate search rerun
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Aggregate records from EP-0188 through EP-0194 and a public numeric projection
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Internal consistency of premise ledgers, classifications, and recorded finite searches; no K4 decryption
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0188
source_episode_sha256: b10d035bd88c2c8f8fd86191f75ac71664f600e10b376df3ec8bf891326f80e2
publication:
  status: publishable
tags:
- kryptos-k4
- audit
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-premise-audit/" hreflang="ja">日本語</a></p>

## Research question

Do the counts, classifications, and finite-search summaries in several K4 records agree with one another? This is an audit of existing aggregates, not a rerun of candidate searches.

## Why this matters

Search scope can only be interpreted when denominators and reported values are consistent. Leaving discrepancies visible helps keep a bounded negative result from becoming an unsupported general claim.

## Method

I projected numeric aggregates from EP-0188 through EP-0194 and checked classification totals, row counts, a recorded multiplier, and UNKNOWN counts. I did not rerun candidate searches, inspect plaintext, or regenerate nulls. The public projection excludes strings and individual candidates.

## Results

| Record | Source-record aggregate |
|---|---|
| EP-0188 | 100 ledger rows across 20 premises; mean Jaccard 0.80 across 14 double-coded rows |
| EP-0189 | 62 rows, six salvaged groups, threshold 7 |
| EP-0190 | Zero exact hits in five reported groups |
| EP-0191 | 72 coded rows versus 73 in the cited summary; recorded multiplier 172501 versus 173101 recomputed from the displayed rule |
| EP-0192 | Zero exact hits across six recorded finite groups; T6 has 1,898,208 settings and a best match of 8 letters |
| EP-0194 | One subfamily remains UNKNOWN |

The 600-point multiplier difference remains visible in the public aggregate rather than being silently corrected.

## Current finding

The audited records contain at least a row-count discrepancy and a multiplier discrepancy. The source records report no exact fit in the stated groups for EP-0190 and EP-0192. One EP-0194 item remains undecided.

## Key figure

| Check | Recorded value | Reading |
|---|---:|---|
| Premise ledger | 100 rows / 20 premises | Audit size |
| EP-0191 row count | 72 / 73 | Internal discrepancy |
| EP-0191 multiplier | 172501 / 173101 | Difference of 600 |
| EP-0192 | 0 in 6 groups | Recorded finite families only |

## What this research shows

- The audited records contain aggregate inconsistencies.
- The EP-0190 and EP-0192 results apply to their stated finite families.
- Discrepancies and UNKNOWN states should remain explicit.

## What this research does not show

It does not show that K4 as a whole is unsolvable, that any broad cipher class is impossible, or that the recorded searches have been independently reproduced. Zero exact hits are not generalized beyond the finite settings described.

## What changed

The numeric audit is now published with the 72-versus-73 row count and 172501-versus-173101 multiplier difference visible. The result scope can be reviewed without publishing plaintext or candidate details.

## What failed

The source records do not agree on the audited counts. One EP-0194 item remains UNKNOWN and is not resolved here.

## Evidence boundary

This note uses aggregate source-record values and a lightweight check of the public projection. No cipher search, null regeneration, or independent replication was performed. New plaintext: 0. External independent replications: 0.

## UNKNOWN

The cause of the row-count discrepancy, which multiplier was used downstream, and whether the UNKNOWN item can be decided from further evidence are not established by these aggregates.

## Falsification targets

If the original ledger and later summary establish that the 72/73 and multiplier differences arose from an identifiable transcription or calculation error, the corresponding audit finding should be revised. Finite-family results also require review if their recorded conditions or implementation are shown to be wrong.

## Reproduce

From the public package directory, run python -B verify_premise_audit.py. It checks aggregate values and differences only; it does not rerun the search.

## Evidence / Artifacts

The public package at reproduction/kryptos-k4-premise-audit contains the aggregate JSON and check script. It includes no candidate strings, ciphertext, or plaintext.

## External audit

There are zero independent replications of this audit and the underlying search records. It has not been peer reviewed.

## Next experiment

Reconcile the original ledger with the later summary row by row and record the source of each discrepancy. Until then, do not treat the differing figures as settled.

## Sources

- Public K4 information: [CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- Source records: KRYPTOS-K4/EP-0188, EP-0189, EP-0190, EP-0191, EP-0192, and EP-0194