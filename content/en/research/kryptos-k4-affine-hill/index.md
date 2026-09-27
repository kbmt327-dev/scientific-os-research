---
research_id: KRYPTOS-K4-EP-0117
title: Do affine maps or Hill matrices that change along the text fit K4?
date: '2026-09-27'
lang: en
domain: Kryptos K4
type: Negative Result
status: Position-varying affine maps give 0 fits; periodic Hill is inconsistent in all 91 decidable settings and gives 0 with matrices from texts; 69 settings with free matrices remain undecidable
evidence_level: Exact tests on public ciphertext and cribs with planted controls and shuffle nulls; scripts committed before running
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; exact enumeration of matrix rows and polynomial coefficients, planted positive controls, shuffled-ciphertext nulls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Affine maps whose multiplier and shift follow stated position rules, and Hill ciphers with 2×2 or 3×3 matrices that change periodically (free or taken from listed texts); no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0117
source_episode_sha256: a144b37aabc5f6703259d27b056e2365f74b91003c8daffcc10d87273192f622
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-affine-hill/" hreflang="ja">日本語</a></p>

## Research question

Two ways to leave the shifted-chart form while staying arithmetic: multiply as well as add (C = a·P + b with a changing along the text), or encipher blocks with a matrix (Hill) that changes from block to block. Does either fit K4's cribs?

## Why this matters

With a constant multiplier the affine map is still one chart shifted, a K1–K3 variant. Only a multiplier that changes with position is a different method, and Hill with changing matrices mixes letters inside a block, which no shifted chart does. Both are decidable from the cribs when their rules are fixed.

## Method

- **Affine (EP-0117).** Multiplier and shift are polynomials of degree ≤ 2 in the position (mod 26), the multiplier invertible at all 97 positions (1,896 polynomials), shift any of 17,576; numbers from A–Z or the KRYPTOS alphabet; enciphering (C = aP + b) or deciphering (P = aC + b) direction. Also exponential multipliers a₀·gⁱ, and a constant multiplier with a running-key shift.
- **Periodic Hill (EP-0117).** Blocks of 2 or 3 letters from each offset, block t using matrix M(t mod p), p = 1–8, with or without a constant vector, both numberings. Every row of every matrix is enumerated against the crib blocks and an invertible combination is sought: exact, no sampling. A setting counts as decidable if at most 5 of 100 shuffled texts come out consistent or unresolved.
- **Hill with matrices from texts (EP-0122).** The same 160 settings with matrices built from listed texts at every start: 2,378,384 settings × starts.
- **Controls.** Planted affine and Hill ciphertexts; shuffled K4.

## Results

| Family | K4 | Controls | Shuffles |
|---|---|---|---|
| Affine, polynomial multiplier and shift (both numberings, both directions) | 0 fits | 20/20 | 0 of 20 |
| Affine, exponential multiplier | 0 fits | 20/20 | 0 of 20 |
| Constant multiplier, running-key shift (K1–K3 variant) | best 9/24 | 6/6 | best 9–10/24 |
| Periodic Hill, 91 decidable settings | inconsistent in all 91 | 40/40 | ≤ 5 of 100 per setting |
| Periodic Hill, 69 other settings | like the shuffles (24 consistent, 13 unresolved) | — | 6–100 of 100 |
| Hill with matrices from texts (160 settings) | 0 of 2,378,384 (expected 8 × 10⁻²¹) | 30/30 | 0, 0, 0 |

The carved tableau's extra L, sometimes cited as a possible key, lies outside the 30 columns used for lookup, so it changes no cell of the chart.

## Current finding

Affine maps whose multiplier changes along the text by a polynomial or exponential rule do not fit K4. Hill matrices that change periodically are inconsistent with the cribs in every setting where the test can decide, and give nothing when the matrices come from listed texts. What stays open is Hill with free matrices when each matrix sees only one or two crib blocks.

## Key figure

![Stacked bar of 160 periodic Hill settings: 91 decidable and inconsistent on K4, 69 not decidable; text below notes that matrices from texts give 0 of 2,378,384 and polynomial affine maps give 0 fits](/assets/kryptos-k4-affine-hill.svg)

## What this research shows

- No affine map with a polynomial (degree ≤ 2) or exponential multiplier, in either direction or numbering, reproduces the cribs.
- Periodic Hill with 2×2 matrices and no vector is inconsistent for every period 1–8, both offsets and both numberings; the same holds wherever 3×3 or vector forms have enough crib blocks per matrix.
- Taking Hill matrices from listed texts closes the settings that are undecidable with free matrices.

## What this research does not show

It does not show that K4 is rarer than random: shuffles also fail wherever the test decides. Free Hill matrices with long periods, multipliers from running keys, and matrices from unlisted texts are not decided.

## What changed

Three catalogue entries (position-varying affine, periodic Hill, the tableau defect) are closed where decidable. The earlier note that the tableau defect "affects a few cells" was corrected to "no cell".

## What failed

In 69 Hill settings a matrix sees too few crib blocks for any test to decide; there K4 behaves exactly like the shuffles.

## Evidence boundary

Public K4 ciphertext and cribs. The polynomial affine test and the 2×2 Hill test without a vector use only K4 and are rerun in the public package. The 3×3 and vector forms, the exponential and running-key affine forms, and the text-matrix search are recorded, not rerun.

## UNKNOWN

Whether a longer crib would decide the free long-period Hill settings. External independent replications: zero.

## Falsification targets

A polynomial affine rule, or a set of periodic Hill matrices, that reproduces all 24 crib letters would overturn the corresponding row.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-affine-hill): `python verify_affine_hill.py` reruns the polynomial affine test (1,896 × 17,576 rules, four forms) and the 2×2 periodic Hill test (32 settings) on K4, with planted controls and shuffled texts, and prints `PASS`. Standard library only, about 40 seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-affine-hill). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None within these families. Free long-period Hill needs a fixed rule for making the matrices before it can be decided.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Hill cipher: Lester S. Hill, "Cryptography in an Algebraic Alphabet", *The American Mathematical Monthly* 36 (1929).
