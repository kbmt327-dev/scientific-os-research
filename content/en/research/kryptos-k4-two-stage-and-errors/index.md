---
research_id: KRYPTOS-K4-EP-0241
title: Two-stage and error-family records show no registered passes in tested scopes
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: No registered pass in the completed finite scopes; EP-0241 r27 covers a subset only
evidence_level: Recorded finite searches and aggregate consistency checks
peer_reviewed: false
independent_replications: 0
evidence:
  class: finite registered search records and saved aggregate summaries
  source: Public K4 crib constraints and records EP-0227, EP-0236, EP-0238, EP-0240, and EP-0241
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Completed registered scopes in EP-0227, EP-0236, EP-0238, and EP-0240, plus the registered families and 26-setting r27 subset in EP-0241
source_episode: KRYPTOS-K4/EP-0241
source_episode_sha256: 2bfb1fc591b586fe1323fee84a38d7174ea6ba5a7588a5349179b3cc67acdfc2
publication:
  status: publishable
tags:
- kryptos-k4
- two-stage
- finite-search
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-two-stage-and-errors/" hreflang="ja">日本語</a></p>

## Current finding

Across the completed registered scopes summarized here, the recorded registered-pass count is zero. EP-0227 has one diagnostic identity hit in its null records; the registered rule required a nonidentity hit, so this diagnostic is not an eligible pass. EP-0236 and EP-0241 disclose K4 exposure before registration and resulting candidate-family or metric/subset selection. EP-0240 has no defined rank fraction for columns B and C because the K4 minimum h is unavailable.

## Key figure

| Record | Completed scope | Recorded result |
|---|---|---|
| EP-0227 | 22 null targets, 88 rows | K4 and null registered passes: 0; one null identity diagnostic was ineligible |
| EP-0236 | 466 registered settings; 20 nulls | K4 passes: 0; min d*=4; null min d* histogram 3:6, 4:14; recorded fraction 20/20 = 1.00 |
| EP-0238 | 200 joint nulls | Joint min(max)=4, min(sum)=8; null fractions 0.14 and 0.505; registered passes: 0 |
| EP-0240 | 200 main null targets per column; 10 auxiliary targets | K4 and null registered passes: 0; A: min h=15, 0.85; AB: min h=15, 0.87; B/C fractions undefined |
| EP-0241 | r26, hb, bh, r21: 1,000 nulls each; r27: 26 settings and 100 nulls | No registered passes; r27 nulls: 0/100 for the registered 1% q1 subset; full-q1 K4 search and null evaluation are incomplete |

P is the observed fraction of the recorded null sample at or below the stated K4 threshold. These finite-sample proportions are descriptive, not confirmatory p-values.

## What this research shows

The listed finite searches did not meet their registered pass criteria. Null summaries and the EP-0227 identity diagnostic follow each record's eligibility rule. The EP-0241 r27 null evaluation covers only its registered 26-setting subset (1% of q1); no completed K4 search or null evaluation covers the full q1 space.

## What this research does not show

These records do not establish a K4 solution, uniqueness, or impossibility of untested families. They provide no independent replication. EP-0236 and EP-0241 are not independent confirmations because K4 exposure informed candidate-family or metric/subset selection. No new K4 plaintext was produced.

## Research question

What do these completed registered two-stage and crib-error-family searches establish about accepted fits to the public K4 constraints, and where do the recorded null comparisons stop being decisionable?

## Why this matters

A zero count has meaning only inside its registered scope and eligibility rule. Separating the ineligible EP-0227 identity diagnostic, undefined EP-0240 fractions, and partial EP-0241 q1 coverage prevents a finite result from being read as a general conclusion.

## Method

This projection reads five episode records and saved aggregate summaries. It reports registered-pass counters, sample sizes, histograms, and explicit missing-scope fields. The lightweight verifier recalculates aggregate counts and fractions; it does not rerun the original searches.

## What changed

The five records are assembled as one bilingual public note with a compact aggregate file and an arithmetic check. No new search or independent replication was performed.

## What failed

No registered pass was recorded in the scopes listed above. EP-0240 B/C has no decisionable rank fraction, and EP-0241 r27 does not cover the full q1 family.

## Evidence boundary

Claims apply only to the completed finite settings, null samples, and eligibility rules named above. EP-0236 had pre-registration K4 exposure that affected candidate-family and face selection. EP-0241 had pre-registration K4 exposure; metric and r27 subset selection followed, although the registered rules, thresholds, settings, and column split were recorded as unchanged afterward. The EP-0241 per-run code hash is unverified. No claim extends beyond these records.

## UNKNOWN

Independent replication is absent. No completed K4 search or null evaluation covers the full EP-0241 q1 space; only the null evaluation for the 26-setting subset is complete. The per-run code hash is unverified, and EP-0240 B/C rank fractions remain undefined. The effect of pre-registration K4 exposure on the rankings is unknown.

## Falsification targets

Revise the finite-scope findings if a row-level audit finds an eligible registered pass, if the preserved histograms fail to reproduce the stated fractions, or if a faithful independent replay changes a registered count. A registered null evaluation completed across the full q1 space could change the null-comparison scope. The full-q1 K4 search is separately incomplete and would require its own completed search.

## Reproduce

From the repository root, run:

    python reproduction/kryptos-k4-two-stage-and-errors/verify_two_stage_and_errors.py

This check verifies aggregate arithmetic and scope flags only; it does not rerun any candidate family or null search.

## Evidence / Artifacts

Source episode identifiers: EP-0227, EP-0236, EP-0238, EP-0240, and EP-0241. Package files:

- reproduction/kryptos-k4-two-stage-and-errors/README.md
- reproduction/kryptos-k4-two-stage-and-errors/results/two-stage-and-errors-20261011.json
- reproduction/kryptos-k4-two-stage-and-errors/verify_two_stage_and_errors.py

## External audit

Independent replications: 0. The packaged verifier is an author-maintained aggregate consistency check, not an independent audit or a rerun of the full searches.

## Next experiment

Preregister candidate families, metrics, thresholds, and subsets before any K4 exposure, then use an independent implementation with a per-run code hash. A claim about null comparisons across full q1 requires registering and completing the null evaluation across that full space. A full-q1 K4 result requires its own completed K4 search.
