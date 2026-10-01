---
research_id: KRYPTOS-K4-EP-0156
title: Can Portax with a free substitution, or a free-square Playfair followed by a mask, produce K4?
date: '2026-09-30'
lang: en
domain: Kryptos K4
type: Negative Result
status: Portax with a free substitution before or after is inconsistent with the cribs in all 96 problems (periods P = 1-48); a free-square Playfair followed by a shift mask is inconsistent in all 23,406 settings of m1, m2 (period <= 5), m3 and m4; logical refutation, not rarer than random; m2 with periods 6-12 is undecidable
evidence_level: Exact consistency test on the public ciphertext and cribs (constraint-solver proofs); decision rules fixed before any run on K4; the rule limiting m2 to periods <= 5 was added after seeing the controls and before running on K4
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; CP-SAT consistency, shuffled ciphertexts and planted positive controls per period; the Portax 'before' layer re-decided by a separate standard-library implementation
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only Portax (ACA rules, periods 1-48) with one free substitution layer before or after, and Playfair with a free square (W as separator) followed by shift masks of four families; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0156
source_episode_sha256: 3413b4000a5a4abf6edd9092f44f80bd47802e67661fb7fe354ed7ea8ffe31a3
publication:
  status: publishable
tags:
- kryptos-k4
- digraph
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-portax-playfair-mask/" hreflang="ja">日本語</a></p>

## Research question

Can the parts of two digraph families that earlier Notes left open be closed?

1. **Portax with a free substitution.** C = Portax(σ(P)) (substitution before) and C = τ(Portax(P)) (substitution after), with σ and τ free.
2. **Free-square Playfair followed by a mask.** W as a separator, Playfair with a free 5×5 square, then a shift mask: C = M_i(PF(P)).

## Why this matters

In the [EP-0113/0116 Note](/en/research/kryptos-k4-consistency/), Portax with a substitution before did not finish at periods P = 23–33, and Portax with a substitution after could not be decided at periods with few crib pairs. The Playfair-plus-mask test (EP-0125) in the [EP-0110 Note](/en/research/kryptos-k4-w-squares/) used keyed squares only; free squares were not run because the cribs were expected to be too short. Both were open gaps.

Plain Portax never enciphers a letter to itself, so K4's two self-encryptions exclude it. One substitution layer before or after removes that argument, so an exact test that solves for the key and the substitution together is needed.

## Method

- **Portax table.** ACA rules, checked against the worked example. The text is written in rows of the period P; letters i and i+P of each block of 2P form a vertical pair (the last partial block is split in half); each column's key gives one of 13 slides.
- **Portax test.** One CP-SAT model per problem: the slide of each column, the substitution (all different), and the plaintext of a partner outside the crib are variables. Every pair with at least one crib letter is used. "No solution" is a proof. P = 1–48 for both layers: 96 problems. Controls per period: 20 planted texts (English with the cribs written in, random key and substitution) and 200 shuffled ciphertexts.
- **Playfair plus mask.** Everything but the square is EP-0125's: W removed (92 letters, 25-letter alphabet); pairs from offset 0, from offset 1, or per W-segment; mask alphabet A–Z or KRYPTOS order (W dropped); key indexed by the reduced or the original position. Four mask families:
  - m1: a constant shift per W-segment;
  - m2: a periodic key with period p;
  - m3: keyword letters (EP-0125's word list, every phase);
  - m4: the K1–K3 plaintext as a running key (every offset, forward and reversed); this site does not publish that text.
- **Free-square test.** The 25 cells are all-different variables. A square gives the same cipher under cyclic row and column shifts, so one letter is fixed at cell 0. Pairs with both letters in the crib and pairs with one crib letter (the partner's plaintext is a variable) are used. For m3 and m4, necessary conditions screen first (Playfair never leaves a letter in its own position, equal inputs give equal outputs, and so on); survivors go to CP-SAT.
- **Rules fixed before running on K4.** (a) If K4 is consistent in some setting, record it and stop. (b) If every setting has no solution, close the family. (c) A setting with timeouts, or with half or more of the shuffles consistent, is undecidable.

**About m2's periods (a rule added later).** 24 m2 controls were planned; 11 were run, then stopped for lack of compute. Plants timed out at periods 7, 8 and 9, and shuffles were consistent at periods 9 and 10. At periods 5 and 6, both plants were consistent and one shuffle was inconsistent while one timed out. After seeing this, and before any run on K4, the rule became: run m2 on K4 for periods ≤ 5 only, and record periods 6–12 as undecidable. Periods 5 and 6 look almost the same in these controls, so the cut at 5 is a judgement from few controls, not a measurement.

## Results

**Portax with a free substitution**

| Form | Periods | K4 | Shuffles consistent (200 each) | Plants |
|---|---|---|---|---|
| Before: C = Portax(σ(P)) | 1–48 | inconsistent at all 48 | 1 at P = 46 only (1 of 9,600) | 20/20 at every period |
| After: C = τ(Portax(P)) | 1–48 | inconsistent at all 48 | 0 at P = 1–12 and 34–48; 2–74 (1–37%) at P = 13–33 | 20/20 at every period |

All 96 problems have no solution, each in under 0.1 s, with no timeouts. EP-0116's results are reproduced, and the open periods (before: P = 23–33; after: P = 7, 11–33, 48) are closed. EP-0116's backtracking ran 8.5 hours at P = 23 because exhaustive search blew up at periods where many columns touch the crib.

With the substitution after, up to 37% of shuffles are consistent at P = 13–33, so K4's failure is somewhat on the rare side there; the per-period comparison was not fixed in advance, so it is not counted as evidence.

**Free-square Playfair followed by a mask**

| Mask | Settings | K4 | How | Controls |
|---|---|---|---|---|
| m1 (constant per segment) | 6 | all inconsistent | solver 6 | plants 20/20 consistent; the shuffle under the same setting inconsistent 20/20 |
| m2 (periods 1–5) | 60 | all inconsistent | solver 60 (no timeouts, 1,228 s in total) | the 11 above |
| m2 (periods 6–12) | — | undecidable (not run) | — | plants time out, shuffles consistent |
| m3 (keywords) | 7,680 | all inconsistent | screen 6,035, solver 1,645 | plants 20/20; shuffles all inconsistent |
| m4 (K1–K3 plaintext running key) | 15,660 | all inconsistent | screen 11,779, solver 3,881 | plants 20/20; shuffles all inconsistent |

EP-0125's expectation that 22 crib letters cannot fix a free square was wrong for m1, m3, m4 and short-period m2, because pairs with one crib letter were used as well.

## Current finding

Portax with one free substitution layer before or after is inconsistent with the cribs at every period 1–48. A free-square Playfair followed by a shift mask is inconsistent for m1, m2 with periods ≤ 5, m3 and m4. These are logical refutations: shuffled ciphertexts mostly fail as well, so this is not evidence that K4 is further from these methods than random. m2 with periods 6–12 is undecidable.

## Key figure

![Bar chart: for each Portax period P = 1 to 48, the share of 200 shuffled ciphertexts that are consistent. With the substitution after (grey), 1 to 37% at P = 13 to 33, highest 37% at P = 26, 0% elsewhere. With the substitution before (orange), 0% everywhere except 0.5% at P = 46. K4 is inconsistent at all 48 periods in both forms. A note below says the free-square Playfair with a mask is inconsistent in all m1 (6), m2 periods up to 5 (60), m3 (7,680) and m4 (15,660) settings, and that m2 periods 6 to 12 are undecidable](/assets/kryptos-k4-portax-playfair-mask.svg)

## What this research shows

- Portax (ACA rules) with one free substitution layer before or after is inconsistent with the cribs at periods 1–48 (96 proofs).
- Playfair with a free square (W as separator) followed by a shift mask that is constant per segment, periodic with period ≤ 5, keyword-based, or a K1–K3 plaintext running key is inconsistent with the cribs (23,406 settings).
- Using pairs with only one crib letter widens what can be decided even for free squares.

## What this research does not show

It does not show that K4 is rarer than random: shuffled ciphertexts mostly fail too. m2 with periods 6–12, Portax with substitutions both before and after, Portax periods above 48, and other digraph ciphers were not tested. m3 and m4 are limited to fixed word lists and texts.

## What changed

EP-0116's open items (Portax with a substitution before, P = 23–33; Portax with a substitution after, undecided) are closed. The free squares that were outside EP-0125's range are closed except for long-period m2.

## What failed

No setting fit. The m2 controls stopped at under half the plan, and the period cut was decided from few controls.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. The constraint-solver results are recorded, not rerun in the public package. The public check covers the Portax table and its structure, the pairs at every period, an exact test of the substitution-before form by a separate implementation, and the counts on the Playfair side. The m3 word list and the m4 K1–K3 plaintext are not published on this site.

## UNKNOWN

m2 with periods 6–12. Portax with substitutions on both sides. External independent replications: zero.

## Falsification targets

A key, substitution or square in any stated form that is consistent with all 24 crib letters would overturn this; so would an error in a constraint model that discards consistent solutions (all plants were judged consistent: 20/20 per Portax period, 20/20 per Playfair mask family).

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-portax-playfair-mask): `python verify_portax_playfair_mask.py` recomputes the Portax table against the ACA worked example, that every slide is its own inverse, that no letter stays in place, and the crib pairs at P = 1–48. The substitution-before form is decided at all 48 periods by a standard-library backtracking search (dynamic column order): K4 inconsistent at all 48; 960 planted texts all consistent; of 960 shuffles, 957 inconsistent, 3 over the search budget, 0 consistent. On the Playfair side it recomputes the 92-letter W-reduced text, the 25-letter alphabet, the crib pairs and the m1 / m2 setting counts. It prints `PASS`, in about 10 s. A rerun of the author's method, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-portax-playfair-mask). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

First a control design under which long-period m2 can be decided (plants solved in time, most shuffles inconsistent); without it a run on K4 would not be a test.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Portax and Playfair: American Cryptogram Association cipher type descriptions ([ACA](https://www.cryptogram.org/resource-area/cipher-types/)).
