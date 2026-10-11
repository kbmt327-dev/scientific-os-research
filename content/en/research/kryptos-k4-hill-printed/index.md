---
research_id: KRYPTOS-K4-EP-0218
title: Do Hill's printed transformations fit the public K4 cribs?
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: The listed printed transformations produced no registered pass
evidence_level: Recorded finite searches with bounded transcript checks
peer_reviewed: false
independent_replications: 0
evidence:
  class: finite registered search records and public transcription checks
  source: Public K4 ciphertext, 24 public crib letters, and the cited Hill-procedure episode records
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Listed Hill 1929 and 1931 printed transformations and specified finite extensions only
source_episode: KRYPTOS-K4/EP-0218
source_episode_sha256: 1f5afa09da4e12a3b63bcd1f56ebaf3566b4e543548701267ad2cf17b2945d57
publication:
  status: publishable
tags:
- kryptos-k4
- hill-cipher
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-hill-printed/" hreflang="ja">日本語</a></p>

## Current finding

The registered searches of four finite Hill-related families produced zero accepted passes. The printed 1931 transformations had minimum mismatch h=19 across 348 labels (null P=0.435); the two printed 1929 transformations had minimum h=21 across 42 labels, with an auxiliary one-cipher-error minimum of 19. Other fixed-stream extensions had minima 13, 16, and 13. These outcomes concern the listed transformations, tables, block conventions, and phases. They do not rule out arbitrary Hill matrices or unspecified procedures.

## Key figure

| Episode | Finite scope | Recorded outcome |
|---|---|---|
| EP-0216 | 32 labels, Hill mod 25 on the W-free stream | No registered pass; labels lie at or within one mismatch of the top of their decidable range |
| EP-0217 | 1,839,948 labels in three extensions | No pass; minimum h values 13 / 16 / 13 |
| EP-0218 | 348 labels from Hill 1931 printed transformations | No h≤2 pass; minimum h=19; 200 nulls; P=0.435 |
| EP-0230 | 42 labels from Hill 1929 C3/C4 transformations | No h≤2 pass; minimum h=21; auxiliary minimum h=19; 1,000 nulls |

Here h is the number of mismatches at the public crib positions. Results and null counts are transcribed from the source records. The verifier checks the public historical transcription and summary structure, not the K4 searches.

## What this research shows

- None of these finite registered families reached its stated acceptance threshold.
- The printed 1929 and 1931 examples and transformations were transcribed and checked against the recorded example counts.
- The observed minima are not by themselves evidence that K4 is random or that Hill methods are impossible.

## What this research does not show

It does not exclude every Hill cipher, arbitrary invertible matrix, block segmentation, or unreported transformation. It does not recover K4 plaintext. No new plaintext characters are published.

## Research question

Do the specifically printed Hill transformations and the listed finite extensions satisfy their registered crib criteria on K4?

## Why this matters

A historical cipher description can define only a small set of transformations, while later readers may expand it into an unrestricted family. Testing the printed, reproducible operators gives a bounded answer without treating unspecified choices as if they had been tested.

## Method

The source records evaluated fixed operator lists, number tables, directions, and phases against the public K4 ciphertext and 24 public crib letters. They report mismatch minima and shuffled controls. The existing historical data file retains the C3/C4 transcription. This package only checks that transcription's dimensions and the recorded result summary.

## What changed

The public projection separates the printed transformations from broader, unspecified Hill families. It reports the finite negative outcomes and keeps the untested choices explicit.

## What failed

The listed printed operators did not reach the registered thresholds. The records also leave transformations unspecified in the historical discussion and do not test all possible treatment of text outside the chosen blocks.

## Evidence boundary

The scope is EP-0216, EP-0217, EP-0218, and EP-0230: their listed transformations, tables, encodings, block rules, and phase sets. A zero pass applies only to those finite choices.

## UNKNOWN

Whether K4 uses any Hill-related construction remains unknown. Arbitrary matrices and unspecified operators are outside this projection. Independent replications: 0.

## Falsification targets

A pre-specified Hill-family construction that predicts additional K4 plaintext positions, followed by independent checks of those predictions, would extend this result. Newly specified operators would need a separate finite registration.

## Reproduce

From the repository root, run:

    python reproduction/kryptos-k4-hill-printed/verify_hill_printed.py

This bounded verifier checks the C3/C4 transcription dimensions and recorded projections. It does not rerun any registered search or shuffle null. Package files are in reproduction/kryptos-k4-hill-printed/.

## Evidence / Artifacts

The package contains the C3/C4 historical data, projected results, and a standard-library verifier. Source record identifiers: KRYPTOS-K4/EP-0216, EP-0217, EP-0218, and EP-0230.

## External audit

Independent replications: 0. Peer review and domain-expert review have not been recorded.

## Next experiment

Any continuation should define the operator family, block treatment, and number table before evaluating K4, then keep its result separate from the printed transformations tested here.

## Results

Registered accepted passes: 0 in the four cited records. The result is limited to those finite lists; the package performs bounded transcription checks only.