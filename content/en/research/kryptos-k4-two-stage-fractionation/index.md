---
research_id: KRYPTOS-K4-EP-0221
title: Do the listed two-stage fractionation families fit the public K4 cribs?
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: No registered pass in tested decisionable columns; the full square bank remains untested
evidence_level: Recorded finite searches with bounded projection checks
peer_reviewed: false
independent_replications: 0
evidence:
  class: finite registered search records and public-input checks
  source: Public K4 ciphertext, 24 public crib letters, and the cited two-stage episode records
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Listed finite two-stage families; EP-0222 covers only its fixed 16-square subset and did not run R3-3
source_episode: KRYPTOS-K4/EP-0221
source_episode_sha256: c9e7a11e209556aca518fa45ae363b11765223321dc751af0d2773606ed0ec3a
publication:
  status: publishable
tags:
- kryptos-k4
- fractionation
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-two-stage-fractionation/" hreflang="ja">日本語</a></p>

## Current finding

The decisionable registered columns across these six records had no accepted pass at their stated thresholds. Their scopes differ: EP-0221 tested five two-stage columns, while EP-0222 tested only two families over a fixed 16-square subset. EP-0222's third family, R3-3, failed its specificity control before K4 or null evaluation and was not run. The full 2,622-square bank was not closed. No new K4 plaintext was produced.

## Key figure

| Episode | Finite scope | Recorded outcome |
|---|---|---|
| EP-0202 | 187,858,944 settings; h≤12 | 0 passes; minimum h=13; P=.045 among 9 registered P values |
| EP-0219 | About 280 million settings | 0 passes; minima h=17, 17, and 13 across columns |
| EP-0220 | Row Trifid and Bifid→Trifid families | 0 passes; minima h=19 and 15; 200 nulls |
| EP-0221 | 22,027,128,336 settings across five columns; h≤2 | 0 passes; minima 14, 14, 13, 13, 13 |
| EP-0222 | Fixed bank of 16 squares from U=2,622 | R2-4 and R1-6: 0 passes, 50 nulls each, P=1. R3-3 specificity failed; K4/null not run |
| EP-0239 | 13,137,903,324 settings; h≤2 | 0 passes; minimum h=12; 59 nulls; P=.20 / .22 |

h is the mismatch count at public crib positions. A no-pass result applies only to the registered family and completed decisionable column.

## What this research shows

- The listed decisionable columns did not meet their registered acceptance criteria.
- EP-0202's P=.045 is one of nine registered comparisons and is not a confirmatory result.
- EP-0222's negative result is limited to its fixed subset. Its failed-specificity R3-3 branch was not evaluated on K4 or nulls.
- EP-0239 completed its 59 recorded nulls, with a coarse P resolution.

## What this research does not show

It does not exclude all two-stage ciphers, all square pairs, or all possible transpositions and segmentations. It does not close the full U=2,622 square bank in EP-0222 and does not identify or publish K4 plaintext.

## Research question

Do the listed, finite two-stage fractionation compositions meet their registered K4 crib criteria?

## Why this matters

Two-stage constructions can have enormous parameter spaces. A finite search can reject only the exact scope and threshold it completed; an unrun family and an untested portion of a key bank must stay visibly unresolved.

## Method

The source records tested fixed compositions, square sets, routes, and transpositions against the public ciphertext and 24 public crib letters. They report mismatch counts and saved shuffled controls. This package projects those records and checks public input dimensions and scope flags; it does not rerun the large searches.

## What changed

The public result now distinguishes completed decisionable columns from unrun or limited work. EP-0222 is stated as a 16-square subset result; the failed-specificity R3-3 branch remains unrun.

## What failed

The tested decisionable columns did not pass. The EP-0222 specificity control failed for R3-3, so that branch was stopped before K4 and null searches. This is not evidence that R3-3 is negative.

## Evidence boundary

Evidence is limited to EP-0202, EP-0219, EP-0220, EP-0221, EP-0222, and EP-0239. EP-0222 uses a fixed bank of 16 squares selected before K4 evaluation, not the full U=2,622 bank. R3-3 was not evaluated. EP-0239's null set contains 59 completed shuffles; its P resolution is coarse.

## UNKNOWN

The full two-stage hypothesis space remains open. The unrun EP-0222 branch and the rest of its square bank are unknown. Independent replications: 0.

## Falsification targets

A fully specified two-stage model that predicts additional K4 plaintext positions under a preregistered rule would challenge these bounded results. Completing a specificity-valid version of EP-0222's omitted branch would resolve only that branch's registered scope.

## Reproduce

From the repository root, run:

    python reproduction/kryptos-k4-two-stage-fractionation/verify_two_stage_fractionation.py

This bounded check validates public input dimensions and the key subset/unrun boundaries. It does not run any candidate or null search. Package files are in reproduction/kryptos-k4-two-stage-fractionation/.

## Evidence / Artifacts

The package contains the existing two-stage implementation, a recorded-results projection, and the bounded verifier. Source record identifiers: KRYPTOS-K4/EP-0202, EP-0219, EP-0220, EP-0221, EP-0222, and EP-0239.

## External audit

Independent replications: 0. Peer review and domain-expert review have not been recorded.

## Next experiment

If continuing EP-0222, repair and validate the specificity control before evaluating any K4 or null data. Keep its subset result distinct from a full-bank claim.

## Results

No accepted pass was recorded in the tested decisionable columns. EP-0222 remains a 16-square subset result; R3-3 was not run and the full U=2,622 bank remains open. New plaintext characters: 0.