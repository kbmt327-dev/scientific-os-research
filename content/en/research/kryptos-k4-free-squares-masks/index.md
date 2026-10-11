---
research_id: KRYPTOS-K4-EP-0195
title: Do registered free-square mask families fit the public K4 cribs?
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: Registered finite criteria have no accepted pass; compatible logic-only classes remain
evidence_level: Recorded finite searches with bounded projection checks
peer_reviewed: false
independent_replications: 0
evidence:
  class: finite registered search records and public-input checks
  source: Public K4 ciphertext, 24 public crib letters, and the cited registered episode records
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Finite registered free-square and mask families; compatible logic-only classes remain outside a plaintext claim
source_episode: KRYPTOS-K4/EP-0195
source_episode_sha256: 7ee86b1668f64ee244a9fece8170dda626fc77086e2e32b3770c61b1016829fc
publication:
  status: publishable
tags:
- kryptos-k4
- finite-search
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-free-squares-masks/" hreflang="ja">日本語</a></p>

## Current finding

The registered decision rules in the seven earlier finite records produced zero accepted passes. Their logic-only columns still contain compatible cases: EP-0213 retained 24 compatible two-square labels in 12 equivalence classes, and EP-0229 rejected one of four surviving non-bijective classes while three remained compatible. The EP-0224 follow-up also records zero passes and zero UNKNOWN across four PH and six SPF columns. These outcomes do not yield a K4 plaintext. This remains a bounded result about the listed masks, square conventions, and thresholds, not a closure of free-square models.

## Key figure

| Episode | Registered scope | Recorded outcome |
|---|---|---|
| EP-0195 | 324 settings; d*=0 and registered d*≤1 groups | 0 registered passes; 20,000 shuffle nulls |
| EP-0204 | 321,368 settings; d*≤1 | 0 passes; minima 3 and 2; 20,000 nulls |
| EP-0212 | 47,328 settings; h≤1 | 0 passes; h=0 nulls 0/20, h≤1 nulls 0/3 |
| EP-0213 | 6,048 labels; one-square d*≤2 | 0 one-square passes; minimum d*=6. Separate two-square logic column: 24 labels / 12 classes remain compatible |
| EP-0223 | 219,896 settings; registered family cutoffs | 0 passes; minima d*≥2, d*=2, and h≥3 |
| EP-0224 | 4 PH columns and 6 SPF columns; SP2-D0 screened out 287,934 settings and decided 62,256 | 0 K4 passes; 0 UNKNOWN. PH nulls: 200 per column; SPF nulls: 2 per column; conditional nulls: 8 periods × 20 samples |
| EP-0229 | Four surviving non-bijective classes | One refuted; three still compatible; null removal rate 22% |
| EP-0235 | 14,913,936 settings; d*≤2 | 0 passes; minimum d*=6 / 3 by order |

Here d* is the minimum number of crib positions that must be dropped to make a model consistent; h counts crib mismatches. The table reports source-record outcomes. The package verifier checks the projection and public-input dimensions only.

## What this research shows

- None of the decisionable registered criteria in these records produced a pass.
- The two-square result in EP-0213 is a compatibility result, not an accepted model or a plaintext.
- EP-0229 narrows four classes to one refuted and three compatible; it does not eliminate the remaining classes.
- EP-0224 found zero registered passes and zero UNKNOWN in its four PH and six SPF columns. The reported P=1.0 values are PH-main P0/P1, PH-sensitivity P0, and SPF P0.
- The results support only the stated finite tests and their recorded controls.

## What this research does not show

It does not identify the K4 cipher, recover any K4 plaintext, or rule out every free-square or mask construction. It does not turn the compatible classes into negative results. EP-0224's P=1.0 and approximate capacity-E estimates do not establish K4-specific rarity or close the full model family. No new plaintext characters are published.

## Research question

Do the specifically registered free-square and mask combinations satisfy their crib-consistency criteria on the public K4 ciphertext?

## Why this matters

Flexible square ciphers can absorb constraints in more than one way. Keeping exact acceptance rules separate from logic-only compatibility prevents a finite negative result from being overstated and preserves candidates that the records did not refute.

## Method

The source records apply their fixed finite settings to the public K4 ciphertext and the 24 public crib letters. They use mismatch or dropped-crib measures and recorded shuffled controls. The listed search sizes, thresholds, and null counts are copied as reported; EP-0224's aggregate completion record is projected in the same way. This package does not rerun those searches or nulls.

## What changed

The public summary states both sides of the result: zero passes in decisionable registered columns, and the compatible classes that remain in logic-only columns. The EP-0224 PH/SPF result and completed null scopes are added as a bounded follow-up. It adds no plaintext and makes no family-wide closure claim.

## What failed

Some two-square columns could not be decided by the chosen capacity criterion. In EP-0213 the logic-only column still has 24 compatible labels in 12 classes. The later EP-0229 test removed only one of four non-bijective classes; three remain compatible.

## Evidence boundary

Evidence is limited to the finite registrations in EP-0195, EP-0204, EP-0212, EP-0213, EP-0223, EP-0224, EP-0229, and EP-0235, plus the public ciphertext and crib. A zero pass means the stated cutoff was not reached in that recorded scope. It does not imply that every square, mask, or composition was tested.

## UNKNOWN

The cipher family and plaintext remain unknown. The compatibility of the three EP-0229 classes remains unresolved. No independent replication is recorded.

## Falsification targets

A pre-specified model outside these finite lists that predicts additional, independently checkable K4 plaintext positions would extend or overturn this bounded assessment. A completed test of a retained compatible class could also change its status.

## Reproduce

From the repository root, run:

    python reproduction/kryptos-k4-free-squares-masks/verify_free_squares_masks.py

This lightweight check validates input dimensions and key result boundaries. It does not reproduce the source searches or null runs. The existing implementation and projected records are in reproduction/kryptos-k4-free-squares-masks/.

## Evidence / Artifacts

The package contains the existing free-square implementation, a privacy-safe results projection, and the bounded verifier. Source record identifiers: KRYPTOS-K4/EP-0195, EP-0204, EP-0212, EP-0213, EP-0223, EP-0224, EP-0229, and EP-0235. The EP-0224 follow-up source SHA-256 is `f91c1f43e6ffaaab900d71fbc37a0040f1763513d46174f3afac47f3c3274099`.

## External audit

Independent replications: 0. Peer review and domain-expert review have not been recorded.

## Next experiment

If pursued, test a retained compatible class under a fixed, pre-registered rule and report it separately from already decided columns.

## Results

Across the decisionable registered criteria, accepted passes: 0. EP-0213 retains 24 compatible labels in 12 two-square classes; EP-0229 retains three of four examined classes. The EP-0224 follow-up adds zero passes and zero UNKNOWN across four PH and six SPF columns. New plaintext characters: 0.

## EP-0224 follow-up (2026-10-11)

The two PH main columns each covered 23,346 settings at h≤1; the two sensitivity columns each covered 606,996 settings at h=0. Six SPF columns each registered 350,190 settings. SP2-D0 screened out 287,934 settings and classified the remaining 62,256. K4 registered passes and UNKNOWN were zero in every column.

PH nulls completed 200 seeds per column, and SPF nulls completed two per column. In the PH main columns, which used the h≤1 cutoff, h=0 occurred zero times; h=1 occurred 0/200 in PH1-main and 1/200 in PH2-main. PH sensitivity nulls also completed 200 seeds per column, but their registered cutoff was h=0 only, so h=1 was not evaluated. SPF nulls had zero SAT and zero UNKNOWN. The conditional SP2-D0 null completed 20 accepted samples for each of P_open={10,15,25,32,36,38,43,44}; all had zero SAT and zero UNKNOWN. Reported P=1.0 values are PH-main P0/P1, PH-sensitivity P0, and SPF P0.

The preregistered capacity-E values are approximations: PH main E0=4.7×10⁻⁵ and E1(h≤1)=0.028 are combined across the two main columns; PH sensitivity E0≈1.3×10⁻³; the 45 SPF periods have E0≤6.5×10⁻⁴, with SP2-D0 about 1×10⁻⁴; the column-sum E0 is about 5×10⁻³ as an upper bound that ignores overlap. These use the registered independent-uniform approximation and are separate from empirical null outcomes. The recorded SPF control detection was 25/60; it is not generalized as K4 detection power.

This follow-up is bounded to the registered scope and controls. The verifier checks saved aggregates and input dimensions only; it does not rerun searches or nulls and is not an independent replication. Source episode SHA-256: `f91c1f43e6ffaaab900d71fbc37a0040f1763513d46174f3afac47f3c3274099`.
