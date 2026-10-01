---
research_id: KRYPTOS-K4-EP-0167
title: Do the fold lines on the K3 worksheet tell where K4's key restarts?
date: '2026-09-30'
lang: en
domain: Kryptos K4
type: Negative Result
status: The public chart #3 image is a typeset reconstruction; the only marks inside K4's cells are two fold lines through the whole sheet (columns 6 and 25), which cross 6 K4 cells and 22 K3 cells, so no other layer of the sheet gives K4 an operator (STOP). The 2025 materials describe no worksheet shape. A key restarting at the fold lines with a shift table disagrees at all 5 same-phase crib pairs, for any key generator (logical refutation, not rarer than random); arbitrary rows chosen by phase are undecidable (83-93% of shuffles also fit)
evidence_level: Records check of public images and 2025 materials (no computation), and an exact generator-free test on the public ciphertext and cribs with a 100,000-shuffle null; the inventory's decision rule and the test's code were committed before use; the restart idea came from the fold positions after the inventory (post hoc)
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; The Kryptos Project's chart #3 reconstruction and NOVA stills; the 2025 auction catalogue and press reports (form only)
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: The marks on the public chart #3 reconstruction, what the 2025 materials say about the worksheet's form, and one family - the same key sequence restarting at the fold crossings (EP-0148, EP-0154, EP-0167); no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0167
source_episode_sha256: 00452341e521be3accf4484ab70e5b3d67a9af992b30d8aec8e18e4d9f112e08
publication:
  status: publishable
tags:
- kryptos-k4
- worksheet
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-chart3-folds/" hreflang="ja">日本語</a></p>

## Research question

K3 was built on paper worksheets, and a public reconstruction of one of them, chart #3, ends with K4 copied after K3. Does anything drawn on that sheet, or on a layer laid over it, pick out K4's cells? And the two fold lines that do cross K4: could the key restart where they cross?

## Why this matters

The production papers are the one outside source that could fix K4's operator ([EP-0140](/en/research/kryptos-k4-construction-ledger/)). The K4 coding papers themselves are private, so the public worksheet images are all that can be checked. A key that restarts at physical marks would be a short-description key, the kind K4 can decide.

## Method

- **Mark inventory (EP-0148).** The chart #3 image on The Kryptos Project's "K3 Method" page: a 14 × 31 grid (K3 in rows 1–11, the "?" at row 11 column 27, K4 from row 11 column 28 to row 14). Every mark was listed with its cell, its probable layer (paper, a plastic sleeve, or the reconstructor) and whether it lies on a K4 cell. The decision rule was fixed before looking: no mark on K4 cells means the public sheet gives no K4 operator; marks that form a set of K4 cells are recorded and reported, without inventing an operation to score on the cribs.
- **2025 materials (EP-0154).** The 2025 auction catalogue, auction-house blog, and AFP and AP reports, read for the form of the working papers only (hand-drawn or typed, number of sheets, folds, sleeves, sheet numbers). Pages that print plaintext were not read.
- **Original footage (EP-0167).** The NOVA scienceNOW stills (2007-07-01) on The Kryptos Project's media page, checked for whether the folds exist on the original sheet.
- **Restart test (EP-0167).** If one key sequence restarts at every fold crossing (segments 0–8, 9–27, 28–39, 40–58, 59–70, 71–89, 90–96), crib letters at the same distance from their segment start must share a key value, whatever generated the key (constant, periodic, a position formula, a recurrence or a text). Five crib pairs share a phase: 28/71, 29/72, 30/73, 32/63, 33/64 (two of them for one fold line alone). Shift table (A–Z or KRYPTOS × Vigenère, Beaufort, variant): the key values must agree. Arbitrary rows chosen by phase (a different method): the pairs must form a partial one-to-one map. Null: 100,000 shuffled ciphertexts.

## Results

**The sheet.** The public image is a typeset reconstruction, not a photograph; the page neither shows nor links the original NOVA and New York Times images. Inside K4's 97 cells the only marks other than labels are two red fold lines through all 14 rows, at columns 6 and 25. They cross K4 positions 9, 28, 40, 59, 71 and 90, and 22 K3 cells in the same way. Every other mark (labels, a marker scrawl, staple notes, margin marks) lies outside the grid. The page's remark that the marker writing seems to be on a plastic sleeve is an impression with no visual basis given, and the layer of no mark can be judged from a reconstruction.

**2025 materials.** No source describes the form of the K4 working papers. The catalogue calls the K1–K3 and K5 items coding charts but the K4 item "the original coding system for K4", with no photos. What was found in the archive in 2025 is five pieces of cut and taped plaintext, not coding charts; their content is not discussed here.

**Original footage.** One crease is visible on the back of a tractor-feed sheet, about 19% along its long side, which matches column 6 (6 of 31). Which sheet it is, the second fold (hidden by a hand), and whether either crosses K4's rows cannot be seen in the stills.

**Restart test.**

| Form | K4 | Shuffles (100,000) |
|---|---|---|
| Shift table, all six crossings | all 5 pairs disagree, in all 6 conventions | all ≤ K4 (K4 has the worst possible value); 45% also disagree at all 5 |
| Shift table, column 6 or column 25 alone | both pairs disagree | all ≤ K4; 72% also disagree at both |
| Arbitrary rows, all six crossings | 0 conflicts | 83% also 0 |
| Arbitrary rows, one fold line | 0 conflicts | 93% also 0 |

The share of shuffles that disagree at every pair (45% and 72%) was computed for this Note with 20,000 shuffles.

## Current finding

The public chart #3 gives no operator for K4: the only marks on K4's cells are two folds through the whole sheet, which cross K3 just as often. A key that restarts at those folds and is read through a shift table is refuted for every key generator, since all five same-phase crib pairs disagree; rescuing it would take five carving errors (two for one fold line). Shuffled ciphertexts often fail just as completely, so this is a logical refutation, not evidence that K4 is further from the family than random. Arbitrary rows chosen by phase are not decided: only five pairs test them, and most shuffles pass.

## Key figure

![Grid of 14 rows by 31 columns: K3 cells in grey (rows 1 to 11), the question mark at row 11 column 27, K4 cells in orange from row 11 column 28 to row 14; red dashed fold lines at columns 6 and 25 run through every row, and six K4 cells on them are outlined in red with positions 9, 28, 40, 59, 71 and 90. Text below: the five same-phase crib pairs, the shift table disagreeing in all five, and arbitrary rows with 0 conflicts but 83% of shuffles also 0](/assets/kryptos-k4-chart3-folds.svg)

## What this research shows

- In the public chart #3 reconstruction, nothing on or over the sheet marks out K4's cells; the two fold lines cross the whole sheet.
- The 2025 materials say nothing about the worksheet's form.
- A key restarting at the fold crossings cannot be read through one shifted chart, whatever the key.

## What this research does not show

It does not show that K4 is rarer than random under the restart: shuffles often fail at every pair too. It does not decide arbitrary rows chosen by phase. It does not say what the original sheet looks like: the stills show one fold, but not whether it crosses K4's rows, and a reconstruction cannot show which marks sit on a sleeve. The private K4 coding papers were not read.

## What changed

The public worksheet is closed as a source of K4's operator. The fold-restart idea is closed for shift tables.

## What failed

The test was meant to run only if the folds were on the original sheet; that condition was half met (one fold seen, its relation to K4's rows unknown). It was run anyway because it was cheap, and it found nothing.

## Evidence boundary

Public K4 ciphertext and cribs, the public reconstruction and stills (viewed, not saved; no image is published here), and the 2025 catalogue and press reports. The public package reruns the fold crossings from the cell geometry and the whole restart test with its null; the inventory and the reading of the materials are records.

## UNKNOWN

What the original sheet's folds cross, and which marks were on a sleeve (the original NOVA and New York Times images would be needed; they were not sought, since every mark said to be on a sleeve lies outside the grid). What the private K4 coding papers contain. External independent replications: zero.

## Falsification targets

An original image showing marks on K4's cells that the reconstruction omitted would reopen the inventory. A shift-table key that agrees at the five same-phase pairs, or a defect in the phase computation, would overturn the restart result.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-chart3-folds): `python verify_chart3_folds.py` recomputes the K4 and K3 cells on the fold columns, the same-phase crib pairs, the shift-table disagreements and the arbitrary-row conflicts with the 100,000-shuffle null (in the author's random order, so the rates match exactly), and prints `PASS`. Standard library only, about 15 seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-chart3-folds). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None from the public worksheet. A new public image of the K4 working papers would be needed.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Chart #3 reconstruction and NOVA stills: The Kryptos Project (thekryptosproject.com), "K3 Method" and media pages; NOVA scienceNOW, PBS, 2007-07-01.
- 2025 materials: RR Auction lot description and blog (October–November 2025); AFP (2025-11-19); AP (2025-11-24).
- Production facts: [EP-0140](/en/research/kryptos-k4-construction-ledger/); physical keys from the sculpture's shape: [EP-0066](/en/research/kryptos-k4-physical-keys/).
