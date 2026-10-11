---
research_id: KRYPTOS-K4-EP-0196
title: A finite test of fixed row lists against the K4 cribs
date: '2026-10-11'
lang: en
domain: Kryptos K4
type: Negative Result
status: The specified checks on eight public lists match the record; the recorded bound across 12 lists is at least three mismatches
evidence_level: Partial rerun of three episodes on public data plus aggregate source records
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Aggregate record for 12 fixed lists and inputs for eight public lists
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Public-list checks for EP-0196, EP-0197, and EP-0208, plus the recorded cover bound for the registered 12-list family
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0196
source_episode_sha256: f2ff8d5e0fadb8370a84a2cf01f20da2408e9304ea2cc6b34277cf462917b85f
publication:
  status: publishable
tags:
- kryptos-k4
- fixed-row-lists
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-fixed-row-lists/" hreflang="ja">日本語</a></p>

## Research question

What do the recorded tests show for a finite family of fixed row lists when compared with the public K4 cribs? The registered family has 12 lists and 662 rows; the public package includes eight lists with 336 rows.

## Why this matters

A fixed list can reduce the freedom to select a favorable column after inspecting a result. Showing exactly which portion is rerun separates reproduced checks from values retained only in the source record.

## Method

The package tests the eight public lists against the cribs for EP-0196, EP-0197, and EP-0208, and recomputes counts derived from list sizes. The selection-free cover bound for all 12 lists, EP-0198, four omitted lists, nulls, planted controls, and IC analyses remain source-record results and are not rerun here.

## Results

| Scope | Result |
|---|---|
| Registered lists | 12 lists, 662 rows |
| Public subset | 8 lists, 336 rows |
| EP-0196, EP-0197, EP-0208 | Checks on the eight public lists are rerun and compared with the record |
| Cover bound for all 12 lists | The record gives a minimum mismatch count of at least 3 |
| EP-0198, nulls, controls, IC analyses | Source record only |

The bound means that, under the registered lists and rules, the recorded minimum cannot reach two or fewer mismatches. The verifier also found that EP-0208 prose says 11 qualifying list-period pairs, while the input sizes yield 9. The recorded excluded-setting count agrees with the recomputed count, but the prose discrepancy remains unresolved.

## Current finding

The specified checks on the eight public lists can be recalculated with the lightweight verifier. The bound for all 12 lists and results for omitted parts remain record values, not outputs of this public rerun.

## Key figure

| List set | Lists | Rows | Verification status |
|---|---:|---:|---|
| Registered family | 12 | 662 | Source record |
| Public subset | 8 | 336 | Three episode checks rerun |
| Cover bound | — | — | Recorded minimum mismatch count at least 3 |

## What this research shows

- The source-record cover bound excludes two or fewer mismatches within the specified lists and rules.
- The author code reruns the stated checks on eight public lists.
- The public verification does not reproduce the full registered search.

## What this research does not show

It makes no claim about every possible row list, selection rule, or K4 method. The public verifier does not validate the omitted lists, EP-0198, or the recorded null and control analyses.

## What changed

A reproduction package now exposes the eight public lists and their checks, while identifying which results remain record-only. It adds no new search finding or plaintext.

## What failed

Four lists and the EP-0198 analysis are absent from the public rerun. The all-list cover bound therefore depends on the source record. EP-0208 also has a remaining difference between 11 pairs in the prose and 9 from the inputs.

## Evidence boundary

Evidence consists of the eight public lists, the author's crib-check code, and recorded aggregates. Null generation and controls are not rerun. New plaintext: 0. Independent replications: 0.

## UNKNOWN

It is not independently verified here whether the recorded results for the four omitted lists and EP-0198 would hold under a separate recalculation.

## Falsification targets

A crib comparison at two or fewer mismatches on the public lists, or a change to the lists or rules defining the registered family, would require revisiting the relevant bound.

## Reproduce

From the package directory, run python -B verify_fixed_row_lists.py. It reruns the public-list checks and lightweight arithmetic in about 10 seconds. This is a partial author-code rerun, not an independent replication.

## Evidence / Artifacts

The public package at reproduction/kryptos-k4-fixed-row-lists contains the eight lists, code, and result aggregates. It omits the excluded list contents.

## External audit

There are zero external independent replications. The work has not been peer reviewed.

## Next experiment

Independently check the excluded aggregate results where a publishable projection is available, then compare them with the source record. Do not extend the conclusion to new methods.

## Sources

- Public K4 information: [CIA, “Kryptos” Sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- Source records: KRYPTOS-K4/EP-0196, EP-0197, EP-0198, and EP-0208