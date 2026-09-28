---
research_id: KRYPTOS-K4-EP-0137
title: Does reordering letters inside each word open a procedure that fits K4?
date: '2026-09-28'
lang: en
domain: Kryptos K4
type: Negative Result
status: With the letters reordered inside each word, before or after the substitution, 0 of the 4.7e15 procedures in the grammar fit K4, under three segmentations, for fixed rules and for any order; logical refutation, not rarer than random
evidence_level: Exhaustive exact crib test on the public ciphertext and cribs; scripts committed before any run on K4; planted controls 76/76, two shuffles
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; the EP-0119 procedure grammar, reordering inside words (8 fixed rules, any order), two shuffled ciphertexts, planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Procedures in the EP-0119 grammar with reordering confined to the crib words, under the three stated segmentations; nothing about families outside the grammar or reordering across words; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0137
source_episode_sha256: f40f91d61f9e2531d1892815157317269cd82294bc5d632bf9ea589bc3ed036e
publication:
  status: publishable
tags:
- kryptos-k4
- word-unit
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-word-reordering/" hreflang="ja">日本語</a></p>

## Research question

Sanborn's hints come in whole words (four letters become `EAST`, six become `BERLIN`, and so on). Reordering the letters inside a word before substituting position by position contradicts none of them, yet every exact test so far read each crib letter as enciphered at its own position. Does allowing reordering inside words open a procedure that fits?

## Why this matters

A word rather than a letter as the unit is one way out of the K1–K3 form (one letter at a time, one shifted chart). If reordering inside words were allowed, every exact rejection so far could fall. Whether it does had to be checked inside the same grammar.

## Method

- **Two orders.** J01: reorder inside words, then substitute (C_i = f(P_π(i), k_i)). J01′: substitute, then reorder (C_π(i) = f(P_i, k_i)). With a key that changes by position these are different hypotheses.
- **Three segmentations.** S1: the hint spans (EAST | NORTHEAST | BERLIN | CLOCK). S2: NORTH split off. S3: each crib one word ("this word is somewhere in this span").
- **Eight fixed rules.** Identity, reverse, rotate by one either way, swap neighbours, even-then-odd and its inverse, second half first. Combined with the segmentations they give 21 distinct crib assignments, each run through the exact EP-0119 test on a GPU.
- **Any order.** Matched by the multiset of letters in each word. The number of orders is 1.9 × 10¹¹ for S1 (37.5 bits), 3.0 × 10⁹ for S2 (31.5 bits) and 1.3 × 10¹⁵ for S3 (50.2 bits). Added to the procedures (52.1 bits), each stays below the crib's 112.8 bits, so a true procedure would stand out.
- **Controls and null.** Planted ciphertexts with random within-word orders and random procedures, for both J01 and J01′; two shuffled K4s as the null. Scripts were committed before any run on K4.

## Results

| Test | K4 | Shuffles | Planted controls | Expected chance passes |
|---|---|---|---|---|
| J01 fixed rules (21) | **0** | 0, 0 | 16/16 | 1.1 × 10⁻¹⁷ |
| J01 any order | **0** | 0, 0 | 22/22 | 7 × 10⁻⁶ in total |
| J01′ fixed rules | **0** | 0, 0 | 16/16 | at most the same |
| J01′ any order | **0** | 0, 0 | 22/22 | at most the same |

Two checks that need only the cribs (post hoc observations, not used in the test):

| Segmentation | Conflicts if the key restarts at every word (from word start, from word end) | A–Z shift keys within ±3 |
|---|---|---|
| no reordering | — | 12 of 24 |
| S1 | 2, 4 | 5 when reversed |
| S2 | 7, 5 | 7 when reversed |
| S3 | 2, 0 | 6 when reversed |
| EASTNORTHEAST one word, BERLIN \| CLOCK | 1, 0 | — |

## Current finding

Reordering the letters inside each word, before or after substituting, gives no procedure in the EP-0119 grammar that fits K4, whether the words follow the hint spans, split off NORTH, or take each crib as one word. So the families already closed by the exact crib test that lie inside this grammar stay closed when reordering inside words is allowed.

## Key figure

![Horizontal bars: procedures alone 52.1 bits, with the fixed rules 56.5, with any order 83.6 for S2, 89.6 for S1 and 102.3 for S3; a red line at 112.8 bits marks what the 24 crib letters can decide, and every test lies below it](/assets/kryptos-k4-word-reordering.svg)

## What this research shows

- Reordering at the word level does not reopen the rejections inside this grammar, before or after the substitution, for fixed rules or any order.
- Every test is smaller than the crib's information, so chance passes practically do not occur; planted controls were found 76/76.
- The observation that the first crib's keys sit close together in A–Z order (12 of 24 within ±3) drops to 5–7 when the words are read reversed; the closeness depends on reading each letter at its own position.

## What this research does not show

It does not show that K4 is rarer than random: the expected count is at most 7 × 10⁻⁶ and the shuffles also gave 0. Families outside the grammar (squares, Doppelkasten, periodic Hill, rotors, an Enigma-type machine behind a substitution) were not rerun with reordered cribs. Reordering across words and word boundaries outside the cribs are out of scope. The affine rows (`AFF`) under any order and the two-layer full-alphabet shapes (`TWO`, `TWOB`) under S3 are covered by the fixed rules only.

## What changed

The worry that "the hints are words, so letter-level tests miss the point" now has an answer inside the grammar. The conflict counts for restarting the key at every word (catalog J03) were rechecked on the way.

## What failed

No procedure fit. J01′ leaves out selectors that would read the intermediate text before reordering (ciphertext autokey and similar), so that corner is not covered.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. Part of the grammar is built from the K1–K3 texts and the carved tableau, so the search itself cannot be rerun from the public package; the public check covers the order counts, the chance values and the crib-only checks.

## UNKNOWN

How words are divided outside the cribs. Whether there is reordering across words. External independent replications: zero.

## Falsification targets

A procedure in the grammar that, with reordering inside the words of a stated segmentation, reproduces all 24 crib letters would overturn this; so would a bug that makes the multiset match miss a planted reordering.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-word-reordering): `python verify_word_reordering.py` recomputes the number of orders and bits for each segmentation, the margin against the crib, the 21 fixed-rule crib assignments and their chance value, the word-restart conflicts and the near-key counts, and prints `PASS`. Standard library only, under a second. It does not rerun the search and is not an independent replication.

## Evidence / Artifacts

[Recorded counts and results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-word-reordering). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Rerun the families closed outside the grammar (squares, Doppelkasten, periodic Hill, rotors) with reordered cribs.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
