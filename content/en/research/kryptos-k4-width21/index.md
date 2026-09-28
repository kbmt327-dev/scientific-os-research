---
research_id: KRYPTOS-K4-EP-0146
title: Does anything besides one pair table point to width 21?
date: '2026-09-28'
lang: en
domain: Kryptos K4
type: Finding
status: The width-21 excess of repeated vertical pairs (11 types, P = 0.0001; about 0.001-0.003 once widths are paid for) survives removing the 2 types made by doubled letters. But only the lag-21 pair table points to 21; mutual information and similar statistics agree because they are computed from the same table. The column period, pairs two and three rows apart and the diagonals are at chance. "21 is a working grid" cannot be tested inside K4 until an operator on the grid is fixed; predictions for K5 and for the plaintext were sealed
evidence_level: Ciphertext-only descriptive statistics against 20,000 permutations of K4's letters; predictions for K5 and the plaintext sealed before either is public
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: The public K4 ciphertext; the cribs only to count which revealed pieces start on a row of a given width
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only which statistics in K4's ciphertext point to width 21, and the sealed predictions; no operator on the grid is fixed; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0146
source_episode_sha256: 420e42399f4361a96938d9d4968789d50a9c37219feb7859344b3bfe11bd1a79
publication:
  status: publishable
tags:
- kryptos-k4
- width-21
- sealed-prediction
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-width21/" hreflang="ja">日本語</a></p>

## Research question

Written at width 21, K4 has 11 types of vertical letter pairs that occur twice or more, against about 3.5 by chance. An outside analysis shared by the program's owner read 21 not as a key period but as the working grid of the encryption (a scaffold for its state), and proposed checking whether several crib-free statistics also single out 21. Does anything besides this one table point to 21?

## Why this matters

Few structures are visible in K4's ciphertext alone, and the width-21 excess is among the strongest (P ≈ 0.001 after paying for widths, see the [key-sources Note](/en/research/kryptos-k4-key-sources/)). Several independent statistics pointing to 21 would support the working-grid reading. Statistics computed from the same table agreeing with each other, however, are not independent evidence.

## Method

- **Forced statistics.** Mutual information at lag 21 and the number of coinciding pair-pairs are both functions of the lag-21 pair table; their correlation with the count R_21 was measured over 5,000 permutations.
- **Statistics not implied by that table.** Single-letter coincidence κ (a column period), pairs two and three rows apart (lags 42, 63), diagonals (lags 20, 22) and multiples of 7, against 20,000 permutations of K4's letters.
- **Doubled letters.** Where the same letter appears twice in a row (positions 18, 25, 32, 42, 46, 67), doubles 21 apart line up vertical pairs automatically; the count was redone without them.
- **Phrase starts.** The widths at which both public crib phrases (starting at 21 and 63) begin a row. Sanborn chose which pieces to reveal, so no P value is attached.
- **Sealing.** Predictions for when K5's ciphertext and when K4's plaintext become public were sealed before either is public (PRED-013).

## Results

| Lag | Repeated vertical pairs R (expected, P) | Single-letter coincidence κ (expected, P) |
|---|---|---|
| 7 | 9 (4.9, 0.039) | 9 (3.3, 0.005) |
| 14 | 7 (4.1, 0.098) | 2 (3.0, 0.81) |
| 20 | 3 (3.6, 0.73) | 4 (2.8, 0.30) |
| **21** | **11 (3.5, 0.0001)** | 3 (2.7, 0.52) |
| 22 | 3 (3.4, 0.69) | 2 (2.7, 0.76) |
| 42 | 3 (1.8, 0.28) | 3 (2.0, 0.32) |
| 63 | 0 (0.7, 1) | 0 (1.2, 1) |

| Forced statistic at lag 21 | K4 | P | Correlation with R_21 |
|---|---|---|---|
| Coinciding pair-pairs | 11 | 0.0016 | 0.94 |
| Mutual information | 2.99 bits | 0.015 | 0.57 |

- Two of the 11 types (QZ, ZT) follow automatically from the doubles QQ (25), ZZ (46) and TT (67) being 21 apart. Without them 9 remain (expected 3.4, P = 0.003).
- Widths 2–48 at which both 21 and 63 begin a row: 3, 7 and 21. Of the four revealed pieces only EAST (21) and BERLIN (63) start a row; NORTHEAST (25) and CLOCK (69) do not.
- The single-letter coincidence at lag 7 (P = 0.005) is post hoc: 7 was chosen after seeing that five of six doubles sit at positions ≡ 4 mod 7.

## Current finding

The width-21 excess looks real and survives removing the doubles. But inside K4 only the lag-21 pair table points to 21. Mutual information and the like point to 21 because they are computed from the same table; that was settled before measuring. The column period, pairs two and three rows apart and the diagonals are at chance. And 21 cannot be separated from 7: the doubles, the phrase starts and the common divisors fit both.

## Key figure

![Bar chart for lags 7 to 63: K4's repeated vertical pairs R and single-letter coincidences kappa beside the permutation means. R is large only at lag 21 (11 against 3.5); the other lags and kappa sit near the mean](/assets/kryptos-k4-width21.svg)

## What this research shows

- "Several statistics point to 21" cannot be a success criterion: every statistic computed from the lag-21 pair table says the same thing.
- Statistics the table does not imply do not single out 21. As states on a grid, a state set by the column, a state reaching two rows ahead, or an operation linking neighbouring cells do not fit these numbers.
- "21 is a working grid" does not fix any operation on the grid, so it cannot be tested inside K4; only outside targets (K5, the plaintext) can test it.

## What this research does not show

It says neither that a width-21 grid exists nor that it does not; without a fixed operation the hypothesis neither gains nor loses here. Chance also remains possible for the excess itself (about 0.001–0.003 once widths are paid for).

## What changed

The width-21 reading moved from tests inside K4 to waiting on a sealed prediction (PRED-013).

- **When K5's ciphertext is public**: a width-21 tail of 0.01 or less against permutations of K5's own letters (also with the stretches shared with K4 removed) counts as a hit; 0.20 or more reads 21 as not a feature of a shared production method. If K5 is said to use a different method, this condition does not apply.
- **When K4's plaintext is public**: a word (or an X separator) begins at both position 42 and position 84 (chance about 0.04). A miss weakens only the version in which grid rows are phrase units.
- Not predicted: the operation on the grid, any key, any plaintext letter.

## What failed

The shared analysis's first proposal (do several statistics single out 21) included forced statistics, so as written it could not serve as a success criterion. The statistics were split into forced and unforced ones and measured again.

## Evidence boundary

The public K4 ciphertext only; the cribs only to count which revealed pieces start a row. The public package reruns everything with the author's generator and seed and matches exactly.

## UNKNOWN

What operation, if any, works on such a grid. Whether width 21 shows up again in K5. External independent replications: zero.

## Falsification targets

A statistic not implied by the lag-21 pair table that independently singles out 21 would overturn "only one table points to 21". A hit on PRED-013's condition A with K5's ciphertext would add weight to 21 as a feature of a shared production method.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-width21): `python verify_width21.py` recomputes R and κ at each lag, the forced statistics and their correlation with R_21, the version without doubles and the phrase-start widths with the author's generator (exact match), checks the sealed prediction's hash, and prints `PASS`. Needs numpy; a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Rerun code, recorded numbers, the sealed prediction (PRED-013, sha256 `81adb6ec…c98dc`) and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-width21). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Judge PRED-013 as sealed when K5's ciphertext or K4's plaintext becomes public.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/).
- K5 uses a similar system and shares some words with K4 at the same positions: [Scientific American 2025-11-12](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/).
