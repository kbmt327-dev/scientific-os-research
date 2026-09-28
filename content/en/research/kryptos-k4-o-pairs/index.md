---
research_id: KRYPTOS-K4-EP-0138
title: Can the two O-segments of TOKIO, paired letter by letter, be a digraph cipher?
date: '2026-09-28'
lang: en
domain: Kryptos K4
type: Negative Result
status: Inconsistent with the cribs in all 56 free 5x5-square settings (Four-square, Two-square, Doppelkasten), 0 of 1,238,220 keyed-square settings, and no 2x2 Hill; logical refutation, not rarer than random; a fixed arbitrary digraph table cannot be decided
evidence_level: Exact consistency test on the public ciphertext and cribs (constraint-solver proofs), pre-registered before any run on K4; the pairing was thought of after seeing the W positions and the cribs (post hoc)
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; CP-SAT consistency for free squares, keyed squares, 1,000 shuffles keeping the W positions, planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only the pairing of the same offsets in positions 21-35 and 59-73; four square methods (56 settings) and the 2x2 Hill in four non-mixed alphabets; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0138
source_episode_sha256: 977ff42939472d9eb4b4f45abb1c4f5b554052e0f71a0999c794bb38bc9a2200
publication:
  status: publishable
tags:
- kryptos-k4
- digraph
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-o-pairs/" hreflang="ja">日本語</a></p>

## Research question

Split at its Ws, K4 has segments of 20, 15, 11, 9, 15 and 22 letters. The only two of equal length are the two O-segments of the TOKIO reading (positions 21–35 and 59–73), and both cribs lie exactly inside them; K4 also uses exactly 25 letters besides W. Could the letters at the same offset in the two O-segments be paired and enciphered two at a time in 5×5 squares without W?

## Why this matters

Pairing letters far apart leaves the K1–K3 form (one letter at a time, one shifted chart). Reading the W brackets as part of the method pairs letters differently from the squares of [EP-0110](/en/research/kryptos-k4-w-squares/). But this pairing was thought of after seeing the W positions and the cribs, so consistency alone would not be evidence.

## Method

- **Pairs.** (P[21+o], P[59+o]) → (C[21+o], C[59+o]) for o = 0–14; both plaintext letters are known from the cribs in 9 pairs, one in 6.
- **Methods.** Four-square (plaintext squares standard, or all four free), Two-square (one or two squares × four rectangle conventions × no pass-through, row or column), single-pass Doppelkasten (the two variants a receiver can decipher). With two directions, 56 settings.
- **Exact test.** One constraint model (CP-SAT) per setting: each letter's row and column in each square are variables, and each pair chooses exactly one case (rectangle, same row, pass-through). "No solution" is a proof. The six half-known pairs are used by giving the unknown letter a free cell.
- **Keyed squares.** The square combinations of EP-0110 (hint words, English words × base squares): 1,238,220 settings.
- **Controls and null.** 280 planted texts (English with the cribs written in, random squares; 30 keyed). Null: 1,000 shuffles of the non-W letters with the W positions and segments kept.

## Results

| Method | Settings | K4 | Shuffles consistent (of 1,000) |
|---|---|---|---|
| Four-square, standard plaintext squares | 2 | inconsistent | 0 |
| Four-square, all four free | 2 | inconsistent | 371 |
| Two-square, 24 variants | 48 | inconsistent | 0 each |
| Doppelkasten, single pass | 4 | inconsistent | 6 |
| Keyed squares | 1,238,220 | 0 | 0 in each of 3 |
| 2×2 Hill (A–Z, KRYPTOS, each without W; linear and affine; both directions) | 32 | no solution | — |

No timeouts; planted controls were found 280/280 and 30/30.

Some facts need only the cribs. The nine fully known pairs contain no repeated input, so a fixed arbitrary digraph table cannot be decided on this pairing. The input (R,R) occurs, which Playfair cannot encipher. In the mirror pairing (21+o with 73−o), the same (T,L) becomes both (V,Z) and (R,V), so every fixed digraph table contradicts.

The contradictions come from small sets. In 18 of the Two-square variants the single pair (S,L)→(S,Z) is enough: an unchanged first letter forces an unchanged second letter, but it became Z. For Four-square with free squares and for Doppelkasten, (T,L)→(R,V), (S,L)→(S,Z) and (T,O)→(S,F) contradict together.

## Current finding

A digraph cipher on the two O-segments paired at equal offsets is inconsistent with the cribs in every square method tested, and a 2×2 Hill on the same pairs has no solution. Random ciphertexts mostly fail as well, so this is a logical refutation of the families, not evidence that K4 is further from them than random.

## Key figure

![Horizontal bars for the four square methods: K4 inconsistent in every one; grey bars show the share of 1,000 shuffled ciphertexts that are consistent, 37.1% for Four-square with free squares, 0.6% for Doppelkasten, 0% otherwise](/assets/kryptos-k4-o-pairs.svg)

## What this research shows

- Enciphering the O-segment pairs with a 5×5-square digraph cipher (Four-square, Two-square, single-pass Doppelkasten) fails with free squares and with keyed squares.
- A 2×2 Hill on the same pairs has no solution in four non-mixed alphabets.
- Every contradiction comes from a handful of crib pairs.

## What this research does not show

It does not show that K4 is rarer than random: apart from Four-square with free squares, shuffled ciphertexts almost always contradict too. A fixed arbitrary digraph table cannot be decided on this pairing. Mixed-alphabet Hill, double-pass Doppelkasten, extra stages before or after the squares, and other pairings inside the O-segments were not tested.

## What changed

One way of reading the TOKIO brackets as part of the method is closed for squares. Reversing the direction only renames the squares and gives the same family (noticed after the runs, so not counted as two independent results).

## What failed

No setting fit. Because the pairing is post hoc, even a consistent result would have been weak evidence.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. The square results are recorded constraint-solver proofs, not rerun in the public package; the public check covers the pair facts and the 2×2 Hill.

## UNKNOWN

Whether a non-square digraph transform, such as a mixed-alphabet Hill, works on this pairing. Whether the TOKIO brackets mean anything at all ([EP-0135](/en/research/kryptos-k4-list-price/): compatible with chance once the target list is paid). External independent replications: zero.

## Falsification targets

A square in any of the stated methods that is consistent with all 24 crib letters would overturn this; so would an error in the constraint model that discards consistent squares (all 280 planted texts were judged consistent).

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-o-pairs): `python verify_o_pairs.py` recomputes the 15 pairs and their known letters, the absence of repeated inputs, Playfair's (R,R), the mirror contradiction and the 2×2 Hill in four alphabets (with 10 planted controls), and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-o-pairs). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Mixed-alphabet Hill on the same pairs (σ⁻¹(M·σ(P) + b) with σ free); other pairings inside the O-segments (neighbours, staggered).

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
