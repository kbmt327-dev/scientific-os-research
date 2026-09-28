---
research_id: KRYPTOS-K4-EP-0140
title: How far do the sculpture's production facts fix K4's operator?
date: '2026-09-28'
lang: en
domain: Kryptos K4
type: Negative Result
status: 6 of 13 facts fix no operator (STOP). Only the carved rows, columns and the two seams fix one; an arbitrary table per carved row fails at the first crib letter, while tables per column or per letter behind a fold fit but so do 74-96% of random ciphertexts, so they carry no information. No candidate
evidence_level: A ledger of facts from public photos and transcriptions, and exact consistency tests on the public ciphertext and cribs; ledger, code and decision rules committed before running on K4
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: 13 production and installation facts from public photos and transcriptions (grades A-C), public K4 ciphertext and 24 crib letters, 20,000 shuffled ciphertexts, planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only one arbitrary table per class of an operator the carved layout fixes to a finite set (carved row, column, letter behind a fold at the vertical, horizontal or both seams); the private production papers are not used; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0140
source_episode_sha256: 4293b03a646f94f71bda37bbd205de2d025b4b0c4426d15211d36e164539fed2
publication:
  status: publishable
tags:
- kryptos-k4
- physical
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-construction-ledger/" hreflang="ja">日本語</a></p>

## Research question

Physical keys for K4 have mostly been tested on the finished sculpture: sun, shadow, orientation, distance (installation physics). How K4 was made at the desk (paper, charts, layers, laying the letters out on copper) is almost untouched. We put the production and installation facts left on the sculpture in a ledger and asked, for each, whether it fixes a cipher operator to a finite set. Only those that do are tested on the cribs.

## Why this matters

One can believe the physical operations have been well tested while actually having tested a different kind of physics. An operator from the production process can be invented freely unless evidence narrows it to a finite set, so the rule was: if the evidence does not fix it, stop rather than invent one (STOP).

## Method

- **Ledger.** For each of 13 facts: content, grade (A–C), source, and whether it fixes an operator to a finite set. Committed before running on K4.
- **K4's coordinates.** Positions 0–3 are row 24, columns 27–30; positions 4–34, 35–65 and 66–96 are rows 25, 26 and 27 of 31 letters each.
- **Operators fixed to a finite set.** L1: one arbitrary table per carved row. L2: one per carved column. G1: close the screen like a book at the vertical seam; one table per tableau cell behind. G2: fold at the horizontal seam; one table per cipher letter behind (three roundings for rows of unequal length). G3: fold at both seams; one table per tableau cell behind. None is a shift of one chart; all are different methods.
- **Decision.** Consistent when, among crib positions in the same class, plaintext → ciphertext is a function and one-to-one. Second column: the share of 20,000 shuffles of K4's ciphertext that are consistent. Twenty planted texts with a random table per class must all be consistent.
- **Known at design time.** A table can only be broken by crib pairs in the same class: 109 for L1, 2 for L2, 1 for G1, 7–8 for G2, 3 for G3. L2, G1 and G3 were declared uninformative in advance if consistent.

## Results

| Facts | Fix an operator? |
|---|---|
| Cipher row lengths and justification, where K4 starts, the 31-letter rows, the row breaks, the top and bottom tableau rows, the two seams | yes (L1, L2, G1–G3) |
| The question marks, the tableau's extra L and the row-14 shift, hand-cut letters, the 1988 prototype plate, the hole in the entrance Morse, the private production papers | STOP (6) |

| Operator | Crib pairs in one class | K4 | Shuffles consistent | Plants |
|---|---|---|---|---|
| L1 row | 109 | **inconsistent** (21 E→F and 30 E→G in row 25) | 0% | 20/20 |
| L2 column | 2 | consistent | 93.1% | 20/20 |
| G1 vertical fold | 1 | consistent | 96.3% | 20/20 |
| G2 horizontal fold (3 roundings) | 7–8 | consistent | 74.3–77.0% | 20/20 |
| G3 both folds | 3 | consistent | 89.7% | 20/20 |

With 15 of the 28 cipher rows at 31 letters, the last four rows are all 31 with chance 0.067 (first counted as 14 rows and 0.049, corrected later).

## Current finding

The carved layout fixes operators only through its rows, columns and two seams. One arbitrary table per carved row fails: inside crib 1, E goes to both F and G. Tables per column or per letter behind a fold fit the cribs, but shuffled ciphertexts fit at almost the same rate; deciding them needs outside evidence that constrains the tables (the production papers), which are private, so the work stops there.

## Key figure

![Horizontal bars for seven operators: share of 20,000 shuffled ciphertexts consistent with the cribs. The row table is 0% and K4 also fails; the column table 93%, the vertical fold 96%, the horizontal folds 74-77%, both folds 90%, and K4 fits each](/assets/kryptos-k4-construction-ledger.svg)

## What this research shows

- One arbitrary table per carved row cannot produce the cribs.
- Tables per column or per letter behind a fold fit, but carry no information (too much capacity).
- Six of the thirteen facts fix no operator for K4.

## What this research does not show

The row-table rejection is logical and does not make K4 rarer than random (every shuffle fails too). The column and fold forms are not rejected. Steps recorded only in the production papers (paper layouts, coding charts) are outside the test. As later found, carved row lengths follow letter widths ([EP-0141](/en/research/kryptos-k4-production-traces/)), so a column number is not a fixed position on the plate and the column table is a weak production unit; the verdicts do not change.

## What changed

"Physical" is now split into three layers: installation physics (sun, shadow, orientation), production geometry (the desk work), and post-decryption physics (carrying out a plaintext instruction on site). Almost all earlier physical tests were layer one. This ledger is the first pass at layer two, and the decidable part turned out small.

## What failed

The ledger miscounted the 31-letter rows as 14 (it is 15). The chance value moved from 0.049 to 0.067; the verdicts did not change.

## Evidence boundary

Facts from public photos and transcriptions, and the public K4 ciphertext and cribs. The public package reruns the row and column tests, which need only K4's coordinates, in the same random order as the author's run. The fold forms (G1–G3) need carved text beyond K4 and are recorded only.

## UNKNOWN

The table types in the production papers. Whether the production process fixes other operators besides rows, columns and folds. External independent replications: zero.

## Falsification targets

An operator fixed to a finite set by production facts, not listed here, that fits the cribs and is rarer than shuffles would overturn "production geometry fixes nothing decidable". The row-table rejection falls if the crib or ciphertext letter at position 21 or 30 is wrong.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-construction-ledger): `python verify_construction_ledger.py` reruns the row (L1) and column (L2) tests with 20,000 shuffles and the plants (an exact match with the author's run), recomputes the row-length chance and prints `PASS`. Standard library only, about a second. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Ledger, recorded results, test and figure scripts](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-construction-ledger). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer or by anyone familiar with how the sculpture was made.

## Next experiment

Use K1–K3, whose methods are known, to calibrate whether production leaves traces in the layout (done in [EP-0141](/en/research/kryptos-k4-production-traces/)).

## Sources

- Jim Sanborn, *Kryptos* (1990). Ciphertext and cribs: [Wikipedia](https://en.wikipedia.org/wiki/Kryptos), [Elonka Dunin](https://elonka.com/kryptos/), [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Layout and seams: public photos by Jim Gillogly and Carol M. Highsmith (Library of Congress). Prototype plate: RR Auction's 2025 lot description and photos.
