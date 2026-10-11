---
research_id: KRYPTOS-K4-EP-0232
title: Do the listed printed procedures fit the public K4 cribs?
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: No accepted pass in the decisionable registered columns; diagnostic scopes remain separate
evidence_level: Recorded finite searches with bounded input checks
peer_reviewed: false
independent_replications: 0
evidence:
  class: finite registered search records and public-input checks
  source: Public K4 ciphertext, 24 public crib letters, and the cited printed-procedure episode records
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Listed finite historical-procedure families; EP-0234 free-square diagnostics are reported separately
source_episode: KRYPTOS-K4/EP-0232
source_episode_sha256: 1de3b47a3cb766c7b051d6344db1b204119449d70e3373b2714af225663d43af
publication:
  status: publishable
tags:
- kryptos-k4
- historical-procedures
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-printed-procedures/" hreflang="ja">日本語</a></p>

## Current finding

The decisionable registered columns in EP-0231, EP-0232, EP-0233, EP-0234, and EP-0237 had zero accepted passes. The outcomes are finite: minima vary by procedure, and several null comparisons do not distinguish K4 from shuffled controls. EP-0234's free-square diagnostic is kept separate; its one-square column has d*=7–8, while its two-square auxiliary is not decisionable. These results do not close all historical procedures or all free-square models.

## Key figure

| Episode | Registered or diagnostic scope | Recorded result |
|---|---|---|
| EP-0231 | Ohaver procedure followed by a fixed mask; 3,456 labels | 0 passes; primary minimum h=17; one-error auxiliary minimum 15; null P=.033 / .022 |
| EP-0232 | Delastelle printed procedures; 4,706,861 main settings | 0 passes; minima h=17 and 16; recorded null columns had no pass |
| EP-0233 | Helix damier with mask; main 989,605,728 settings | 0 passes; minimum h_dec=14 and h_enc=16; overall null P=.52 / 1.00 |
| EP-0234 | Separate free-square diagnostic | One-square d*=7–8; no d*≤2 pass. Two-square auxiliary is not decisionable; 50–91% of nulls meet d*≤2 |
| EP-0237 | Bigrammes rompus with registered mask; 52,119,235,008 settings | 0 passes at h≤2; minimum h=13; null P=1.00 |

h is crib mismatch count; d* is the minimum crib positions dropped for consistency. EP-0234 is a separate diagnostic row, not evidence that every square family was tested.

## What this research shows

- The listed decisionable columns did not meet their registered acceptance criteria.
- The historical procedures were represented by finite transcriptions, tables, settings, and masks.
- Several observed minima are ordinary under the corresponding recorded null comparisons; a small nominal tail value among multiple columns is not treated as a global result.
- The free-square diagnostic retains its own decision boundary and unresolved two-square auxiliary.

## What this research does not show

It does not rule out every historical cipher procedure, parameterization, free square, or composition. It does not identify the K4 method or publish K4 plaintext. New plaintext characters: 0.

## Research question

Do the specified historical procedures, as transcribed into finite registered families, meet their K4 crib criteria?

## Why this matters

A procedure described in a historical source may leave many choices open. A finite test can answer whether its stated implementation passed, while leaving untested choices and ambiguous families visible.

## Method

The source records evaluated fixed finite families against the public K4 ciphertext and 24 public crib letters, using mismatch or dropped-crib criteria and recorded shuffled controls. This package projects those saved outcomes and checks a few public input dimensions; it does not rerun the searches.

## What changed

The package now presents the recorded outcomes in one compact table and labels EP-0234 as a separate free-square diagnostic. It keeps compatible, undecidable, and untested scopes from being recast as decided negative rows.

## What failed

None of the listed decisionable columns reached its acceptance threshold. EP-0234's two-square auxiliary did not discriminate: many shuffled nulls also meet the cutoff. EP-0231's nominal P values are across multiple comparisons and do not establish specificity.

## Evidence boundary

Evidence is limited to the registered families and controls in EP-0231, EP-0232, EP-0233, EP-0234, and EP-0237. In particular, EP-0233's auxiliary unconstrained-square check was also mostly incompatible on nulls, and cannot establish K4-specific evidence. No family-wide closure follows.

## UNKNOWN

Whether any untested historical procedure or parameterization describes K4 remains unknown. EP-0234's two-square column remains unresolved. Independent replications: 0.

## Falsification targets

A fixed, independently checkable rule that predicts additional K4 plaintext positions from an untested procedure would challenge this bounded assessment. Any new procedure should be specified before it is scored.

## Reproduce

From the repository root, run:

    python reproduction/kryptos-k4-printed-procedures/verify_printed_procedures.py

The lightweight verifier checks public input dimensions, the transcribed symbol table size, and result boundaries. It does not rerun the searches or nulls. Package files are in reproduction/kryptos-k4-printed-procedures/.

## Evidence / Artifacts

The package contains the existing procedure implementation, a recorded-results projection, and the bounded verifier. Source record identifiers: KRYPTOS-K4/EP-0231, EP-0232, EP-0233, EP-0234, and EP-0237.

## External audit

Independent replications: 0. Peer review and domain-expert review have not been recorded.

## Next experiment

If a printed procedure is extended, define its open choices and finite parameter list first. Report any free-square diagnostic separately from other registered columns.

## Results

Decisionable registered pass count: 0 in the listed finite columns. EP-0234's diagnostic scope remains separate, and its two-square auxiliary is unresolved. New plaintext characters: 0.