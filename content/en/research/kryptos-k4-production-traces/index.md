---
research_id: KRYPTOS-K4-EP-0141
title: Did making K1-K3 leave traces in the carved layout?
date: '2026-09-28'
lang: en
domain: Kryptos K4
type: Finding
status: Hardly any. Carved row lengths follow letter widths (rank correlation -0.74 to -0.76 in three fonts, P <= 1e-5); row breaks do not fall on plaintext word breaks (1 of 12, chance 2.0); even K3's known transposition grid is invisible in the layout. K4's four rows follow the same width rule. No K4 production operator can be fixed
evidence_level: The carved layout from public transcriptions, calibrated on K1-K3 whose methods are known; T1 and T2 committed before running; the comparison with a 31-column grid is labelled post hoc
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: The carved cipher-panel layout (28 rows) from public photos and transcriptions, the published K1-K3 methods, three fonts as stand-ins for letter widths (Arial, Arial Narrow, Calibri)
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only traces the K1-K3 production steps left in the carved layout (row lengths, breaks, section starts, symbols, known errors); no operator is fixed for K4 and no crib test is run; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0141
source_episode_sha256: f3419fdf329ede74c206c47d11302c83f3b10796044da969130981f11509c961
publication:
  status: publishable
tags:
- kryptos-k4
- physical
- calibration
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-production-traces/" hreflang="ja">日本語</a></p>

## Research question

For K1–K3 both method and plaintext are known. What traces did the production steps (plaintext → encipher with a chart → lay out and cut on copper) leave in the carved layout? If K4 shows the same kinds, the maker's production habits can be learned without touching K4's answer.

## Why this matters

Many hypotheses read K4's layout (row lengths, columns, breaks, seams) as a clue to its method. If such readings meant anything, K1–K3, whose methods are known, should show their method in the layout. If they do not, that kind of reading has no positive control and no power.

## Method

- **T1 (committed before running).** Do the 12 row breaks of K1 and K2 fall on plaintext word breaks? Nulls: a break equally likely anywhere in a ±2-letter window, or the overall word-break density (0.207).
- **T2 (committed before running).** Every cipher row is justified, so rows with many wide letters should hold fewer letters. Rank correlation between the letter count of the 28 rows and their mean letter width; the advance widths of three fonts stand in for hand-cut letters. Null: each plate's row lengths shuffled and the same text re-broken, 100,000 times.
- **Facts.** Where each section starts, how the question marks are handled, and at which step the known errors entered.
- **Post hoc (not pre-registered).** Whether the carved rows are a re-layout of a 31-column chart (offset of the row ends from a 31-column grid).

## Results

| Font | Rank correlation ρ | Null mean | P | ρ of a pure width layout |
|---|---|---|---|---|
| Arial | −0.738 | −0.021 | ≤ 10⁻⁵ | −0.81 |
| Arial Narrow | −0.738 | −0.019 | ≤ 10⁻⁵ | −0.81 |
| Calibri | −0.758 | −0.015 | ≤ 10⁻⁵ | −0.94 |

- K4's four rows (24–27) sit −0.6 to +0.4 letters from the line fitted to rows 0–23, inside those rows' scatter (SD 0.59).
- T1: 1 of 12 K1/K2 row breaks falls on a word break; chance expects 2.0 (P(≥1) = 0.89), so if anything slightly fewer. A control layout snapped to word breaks gives 11 of 12, P = 8 × 10⁻⁸.
- Post hoc: the range of the row ends' offset from a 31-column grid is 1.71 on the upper plate (null mean 2.13, P = 0.23) and 3.00 on the lower (3.53, P = 0.50), not tied to 31 columns. The last four lower rows (K4) all being 31 has chance 0.015, but the width model predicts about 31 for them, so it is not evidence.

| K1–K3 trace | Step | Same kind in K4? |
|---|---|---|
| Row lengths set by letter widths | laying out on copper | yes; uninformative |
| Row breaks not placed at word breaks | layout | same pattern; crib 2 splitting at a row end is an ordinary accident of it |
| Sections start at a row start | layout | no: K4 alone starts mid-row, right after K3's question mark |
| Question marks outside the cipher | plaintext → chart | K4 has no symbol |
| K3's transposition grid | — | invisible in the layout even for K3 |
| Errors at the plaintext, key and post-encryption steps | each step | on K4's side handled by the carving-error tests ([EP-0071](/en/research/kryptos-k4-carving-errors/)) |

## Current finding

Making K1–K3 left hardly any trace in the carved layout. Row lengths follow letter widths, row breaks carry no plaintext words, and even K3's known transposition grid does not show. K4's four rows follow the same width rule. Families that read K4's layout as a clue to the method therefore have no positive control in K1–K3, and no K4 production operator can be fixed from this material (STOP).

## Key figure

![Scatter plot of letters per row against the row's mean letter width for the 28 carved rows: rows with wider letters hold fewer letters, rho = -0.74; K4's four rows (red) sit on the same trend](/assets/kryptos-k4-production-traces.svg)

## What this research shows

- The carved cipher rows' lengths are set by the widths of the letters laid out on copper (the same in three fonts, P ≤ 10⁻⁵).
- Row breaks carry neither plaintext words nor a cipher grid.
- The traces that remain are section starts, question marks, the step at which errors entered, and one ciphertext letter deleted after layout. K4 shares only the width layout and "not starting at a row start", neither of which says anything about its method.
- K4 starting mid-row fits K3 and K4 having been written continuously on one chart.

## What this research does not show

It does not show that K4's layout has no method in it. A grid not showing in the layout is no evidence that K4 has no transposition (K3's does not show either, so the power is zero). Fonts stand in for the real hand-cut widths. The production papers (K4's charts and worksheets) count as solution material and are not read under this study's rules.

## What changed

The "one table per column" form tested in [EP-0140](/en/research/kryptos-k4-construction-ledger/) has a weak basis as a production unit, because column numbers drift with letter widths. Reading the 3 × 31 block as a matrix was restated as a typesetting outcome, not evidence of a designed matrix.

## What failed

T1 first ran once with the upper plate's count written as 432 (question marks not counted). The breaks and word boundaries do not depend on that number and the result was the same 1/12; it was fixed and rerun.

## Evidence boundary

The carved layout from public photos and transcriptions, and the published K1–K3 methods. This site does not publish the sculpture's text beyond K4, so the public package holds only per-row numbers (letter count and mean letter width) and recomputes the correlations, residuals, chance values and post hoc test from them. T2's re-breaking null and T1's word boundaries are recorded only.

## UNKNOWN

K4's production steps themselves. Whether "not starting at a row start" means more than K3 and K4 sharing one chart. External independent replications: zero.

## Falsification targets

If the real letter widths (measured on the sculpture) fail to explain the row lengths, T2 falls. If another reading finds the method's traces (a grid, word breaks) in K1–K3's layout, "no traces in the layout" is overturned.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-production-traces): `python verify_production_traces.py` recomputes, from the per-row numbers, the rank correlation in three fonts, the residuals of K4's four rows, T1's chance values, the permutation null of the offset from a 31-column grid and the chance that K4's rows are all 31, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Per-row numbers, recorded results, check and figure scripts](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-production-traces). MIT-licensed.

## External audit

No external independent replication. No review by anyone familiar with how the sculpture was made, or by a cryptographer.

## Next experiment

Measure the sculpture's real letter widths on photos and recheck T2 without font stand-ins.

## Sources

- Jim Sanborn, *Kryptos* (1990). Ciphertext and cribs: [Wikipedia](https://en.wikipedia.org/wiki/Kryptos), [Elonka Dunin](https://elonka.com/kryptos/).
- Layout: public photos by Jim Gillogly and Carol M. Highsmith (Library of Congress); transcriptions collected by [Elonka Dunin](https://elonka.com/kryptos/).
