---
research_id: KRYPTOS-K4-EP-0110
title: If the Ws are separators, can a 5×5 square cipher produce K4?
date: '2026-09-27'
lang: en
domain: Kryptos K4
type: Negative Result
status: Keyword and free squares (Four-square, Two-square, Bifid, CM-Bifid), Playfair with a mask in either order, squares with a mask, and 5×5 grid shifts are inconsistent with the cribs where decidable
evidence_level: Exact consistency tests and annealing with planted controls on public ciphertext and cribs
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext with the Ws removed and the 24 public crib letters; exact solvers, annealing, shuffled-ciphertext nulls, planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Digraph and block ciphers on a 25-letter square applied to the 92 non-W letters; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0110
source_episode_sha256: 1ea5f657fc2a3ff2bb4cb9d60a56956a98e2d40ed3696c20639cbecbf207bc1b
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-w-squares/" hreflang="ja">日本語</a></p>

> **Later check (2026-09-30).** The closure of CM-Bifid (two free squares) in this Note holds only when the digraph grouping and the block alignment never shift. An internal follow-up (EP-0169) allowed one shift: 27 of 2,765 settings are then consistent with the cribs, so CM-Bifid is back to undecidable from the cribs alone. K4's 27 is not unusual among shuffled ciphertexts (post hoc null, P = 0.12). The other square families stayed closed with one shift. The text and numbers below are unchanged from 2026-09-27. Details are in the [EP-0169 Note](/en/research/kryptos-k4-block-phase-shift/).

## Research question

K4 uses all 26 letters, which rules out any cipher with 25 output symbols. But if the five Ws are separators added after encryption, the other 92 letters use exactly 25 types, and square ciphers come back into play. With the Ws removed, can a 5×5 square cipher produce the cribs?

## Why this matters

This was the one decidable different method still untested when the program reviewed its blind spots. Square ciphers are the classic alternative to a shifted chart, and the W observation gave a concrete reason to try them.

## Method

- **Text.** K4 without its five Ws: 92 letters, cribs at reduced positions 20–32 and 59–69. Three digraph pairings: from the first letter, from the second, and restarting in each W segment.
- **Keyword squares (EP-0110).** Four-square, Two-square (four corner conventions, with and without the pass-through rule) and Bifid (periods 2–12, whole text, per segment), keyed by hint words, Kryptos words, the standard square and 2,540 English words: 925,600 settings.
- **Free squares.** Four-square with two free cipher squares: each crib digraph fixes one cell of each, so consistency is a direct check. Two-square with free squares: equalities between rows and columns, solved exactly (72 settings). Bifid with one free square: annealing with the cribs as hard constraints. CM-Bifid with two free squares: exact satisfiability on square coordinates (EP-0120).
- **With a shift mask.** Playfair followed by a shift mask (5,012 squares, four mask families, EP-0125); keyword squares with a shift mask before or after (EP-0126).
- **Grid shifts.** Translations, rotations and mirrors on a free 5×5 grid, with key letters, text layouts or periodic keys (EP-0115, EP-0128).
- **Controls.** Planted ciphertexts for every family; shuffled ciphertexts as nulls.

## Results

| Family | K4 | Controls | Shuffles |
|---|---|---|---|
| Keyword squares (925,600 settings) | 0 | 30/30 | 0, 0, 0 |
| Four-square, free cipher squares | Inconsistent in every pairing (and with 40 keyed plain squares) | 200/200 | 0 of 2,000 |
| Two-square, free squares (72 settings) | Inconsistent in all 72 | 30/30 | 0–2 of 200 per setting |
| Bifid, one free square | Score at the shuffle level for every period | 96–100% of planted English recovered | — |
| CM-Bifid, two free squares (79 block settings) | Inconsistent in all 79 | 26/26 | 14 of 100 also inconsistent everywhere |
| Playfair then shift mask | 0 | 40/40 | 0 |
| Shift mask then Playfair | Impossible: doubled ciphertext pairs (5, 2, 3 by pairing) | — | — |
| Keyword squares with a shift mask | 0 (expected false hits 0.00015) | 36/36 | 0, 0, 0 |
| Grid shifts with key letters / text layouts | 0 of 26,964 / 0 of 234 | 120/120, 60/60 | 0 of 2,000 |
| Grid with periodic keys | 114 of 381 pass, shuffle mean 128.5 | — | no enrichment |

## Current finding

Treating the Ws as separators does not open a square cipher. Keyword and free squares in Four-square, Two-square, Bifid and CM-Bifid, Playfair with a shift mask in either order, keyword squares with a mask, and shifts, rotations and mirrors on a 5×5 grid are all inconsistent with the cribs wherever the test can decide. Each is a logical refutation; random ciphertext usually fails as well.

## Key figure

![Status chart of ten square-cipher families on K4 with the Ws removed: eight closed logically, one-square Bifid closed with power, and two free squares with long periods marked not decidable](/assets/kryptos-k4-w-squares.svg)

## What this research shows

- A Four-square with any cipher squares cannot produce the cribs: some cell would need two letters, or some letter two cells.
- Two-square fails for a structural reason. In the standard corner conventions an output letter equals its plaintext letter only when the other one does too, and K4 has digraphs where only one does (AS→KS, CK→PK, ST→SS). In the swapped conventions the two swaps must happen together, and RT→PR has only one.
- Playfair cannot be the last step, because it never outputs a doubled pair and K4 has them in every pairing. It cannot be followed by a shift mask either.
- CM-Bifid, which annealing could not decide, is decided exactly from the cribs alone.

## What this research does not show

It does not show that K4 is rarer than random under these families. It leaves open two free squares with long periods, symmetries chosen freely at each position, and the double-pass Doppelkasten (covered in a [separate Note](/en/research/kryptos-k4-consistency/)).

## What changed

The W-as-separator square family, the last decidable different method on the blind-spot list, is closed. CM-Bifid moved from "not decidable" to "closed" once an exact solver replaced annealing.

## What failed

Annealing could not decide CM-Bifid (planted English recovered only 35–75%); the exact solver was needed. The free Four-square script was run before it was committed, a procedural lapse recorded internally; the check is deterministic and is rerun here.

## Evidence boundary

Public K4 ciphertext and cribs. The free-Four-square test, the Two-square witnesses and the doubled pairs use only K4 and are rerunnable. The keyword search, exact Two-square and CM-Bifid solvers, annealing and mask searches are recorded but not part of the public package.

## UNKNOWN

Whether the Ws are separators at all. Whether a solver could decide two free squares with long periods. External independent replications: zero.

## Falsification targets

Squares and a pairing that reproduce the 24 crib letters in any of the closed families would overturn the corresponding row.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-squares): `python verify_w_squares.py` removes the Ws, reruns the free-Four-square test (with 200 planted controls and 2,000 shuffles), finds the Two-square witnesses and the doubled ciphertext pairs in each pairing, and prints `PASS`. Standard library only, about a second. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including searches not rerun here, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-squares). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None for keyword or single free squares. An exact solver for two free squares with long periods, if one becomes tractable.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Square ciphers: American Cryptogram Association, cipher type descriptions ([ACA](https://www.cryptogram.org/resource-area/cipher-types/)).
