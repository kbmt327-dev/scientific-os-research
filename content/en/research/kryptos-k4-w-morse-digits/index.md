---
research_id: KRYPTOS-K4-EP-0182
title: Does K4 fit W as a null, a reversed key, a Morse mask or digit-wise addition?
date: '2026-09-30'
lang: en
domain: Kryptos K4
type: Negative Result
status: With W skipped in the key index, the procedure enumerator (up to 2 errors) and the text keys with a shift table, a mask on the plaintext or a mask on the ciphertext give 0 (closed); with masks on both sides, 5,970 settings pass the crib against about 5,390 by chance and the English stage was not run (undecidable). A reversed key direction is the forward family again (forced before testing). The pure Morse mask is excluded by logic, and with a free substitution it gives 0 of 22.4 million; digit-wise addition with 22 fixed digit strings gives 0. Logical refutations, not rarer than random
evidence_level: Exact crib tests with closed-form chance expectations, shuffles and planted controls on the public ciphertext and cribs; decision rules committed before each K4 run; the W-as-null reading was thought of after looking at K4 (post hoc)
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; the program's procedure enumerator and text-key runs (texts not published here), a Morse-mask search, a digit-addition search; shuffled ciphertexts and planted controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Four small families tested on 2026-09-30 (EP-0180 to EP-0183) - W as a null in the key index, the key read backwards, a per-position operation on Morse code, digit-wise addition of fixed digit strings; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0182
source_episode_sha256: daf1af88b7bd7730cc854324b2454b99977d779d48cdc80905b9dc3ef078bf29
publication:
  status: publishable
tags:
- kryptos-k4
- w-null
- morse
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-w-morse-digits/" hreflang="ja">日本語</a></p>

## Research question

Four small ideas, each tested on the cribs on 2026-09-30:

1. **W as a null (EP-0182).** K4's five Ws (0-based positions 20, 36, 48, 58, 74) are skipped by the key: carved letter i takes key position J = i − (number of Ws before i).
2. **Reversed key direction (EP-0183).** The key text is read from its end, or the index runs backwards along K4.
3. **Morse mask (EP-0180).** Each plaintext letter is written in Morse code, one of four operations is applied (none, swap dots and dashes, reverse, both), and the result is read back as a letter. The source is the Morse code at the sculpture's entrance.
4. **Digit-wise addition (EP-0181).** Each letter becomes two digits (A = 01 … Z = 26), a known digit string is added digit by digit without carry, and the result is folded back to a letter mod 26.

## Why this matters

Each idea changes one assumption of the K1–K3 form. The W reading comes from the observation that Ws bracket both cribs ([EP-0057](/en/research/kryptos-k4-w-brackets/)); if W is a null, every earlier test that counted W in the key position was misaligned. The reading was formed after looking at K4, so a fit alone would have been weak evidence.

## Method

- **W as a null, part (a).** The procedure enumerator of [EP-0119](/en/research/kryptos-k4-procedure-enumerator/), with up to 2 crib errors, under three alignments: the W-skipping shift (crib 2 moves by −3 relative to crib 1), the opposite shift, and the W-skipping index with its absolute origin (crib 1 at −1, crib 2 at −4). No W lies inside a crib, so neither crib is split.
- **W as a null, part (b).** The text keys k = S[(a·J + b) mod L] of the [masks Note](/en/research/kryptos-k4-masks/), with every stride a and start b, on K1–K3 cipher and plain text, K4 itself, the tableau and the World Clock place names, 8 conventions. Four gates: the shift table alone; a free substitution on the plaintext (σ); a free substitution on the ciphertext (τ); substitutions on both sides (crib sieve only). With the ordinary index the runs reproduce the earlier counts.
- **Reversed direction.** Four index types (index reversed, text reversed, each with and without skipping W). The decision rule stated before the run that, with every a and b free, a reversed index or text is a member of the forward family: a(96 − i) + b = (−a)i + const, and S read backwards at position x is S[L − 1 − x].
- **Morse mask.** First a logical check: which of the four operations maps each crib plaintext letter to its ciphertext letter. Then a variant with a free substitution after the mask, over 22,400,800 position rules (periodic up to 12, linear, block rules, and the enumerator's position features).
- **Digit-wise addition.** 22 digit strings fixed before running, from public sources (mathematical constants, the sculpture's coordinates, dates, a time difference); add or subtract; two directions; four digit conventions; start offsets 0–60. 21,472 settings, 5,600 distinct on the crib.
- **Nulls and controls.** Closed-form chance expectations; shuffled K4 (2 to 1,000 per test); planted ciphertexts for every test before the K4 run.

## Results

| Test | Settings | Chance expectation | K4 | Shuffles | Controls |
|---|---|---|---|---|---|
| W skipped: enumerator, ≤ 2 errors | 3 alignments × 52.1 bits | 2.7×10⁻¹³ | 0 | 0, 0 | 9/9 + 9/9 |
| W skipped: text key, shift table | 61,719,792 | 6.8×10⁻²⁷ | 0 | 0, 0, 0 | 80/80 over the four text-key gates |
| W skipped: text key, σ | 61,719,792 | 4.4×10⁻¹⁰ | 0 | 0, 0, 0 | (same) |
| W skipped: text key, τ | 61,719,792 | 5.7×10⁻⁹ | 0 | 0, 0, 0 | (same) |
| W skipped: masks on both sides (crib sieve) | 15,408,778 | about 5,390 (±40%) | **5,970** | 1.96 M, 1.85 M, 5,661 | (same) |
| Reversed direction (4 index types) | as above | as above | same counts as forward | same | (included) |
| Morse mask, pure form | — | — | impossible at 22 of 24 crib positions | — | — |
| Morse mask + free substitution | 22,400,800 | 8.9×10⁻¹¹ | 0 | 0 of 200 | 80/80 |
| Digit-wise addition, 22 fixed strings | 5,600 distinct | 1.3×10⁻³⁰ | 0 | 0 of 1,000 | 60/60 |

No setting other than an identity passed any gate. For the two-sided masks, 9 of K4's 5,970 passes use K4 itself as the key text. The first two shuffles pass far more often (their own chance expectation is 3.2–3.3 million), the third about as often as K4.

The reversed direction reproduced the forward counts exactly: 6,889 two-sided passes with the ordinary index and 5,970 with W skipped, and 5,869 and 5,661 on shuffle 3.

The pure Morse mask needs no search. None of the four operations changes the length of a Morse code, and at 22 of the 24 crib positions no operation maps the plaintext letter to the ciphertext letter (18 of them differ in Morse length). Only positions 32 (S → S) and 73 (K → K) admit one, by identity or reversal.

## Current finding

Skipping W in the key index does not rescue the enumerator or the text keys with a shift table or a one-sided mask: K4 gives 0 where chance gives far less than 1. With masks on both sides, the crib sieve passes about as many settings as chance, and the English stage that would decide them was not run, so that part is undecidable. Reading the key backwards adds nothing: the result was forced before testing. The Morse mask fails by logic in its pure form and gives 0 with a free substitution; digit-wise addition with the 22 fixed strings gives 0. Shuffled ciphertexts also give 0 in every closed test, so these are logical refutations of the families, not evidence that K4 is further from them than random.

## Key figure

![Dot chart on a log scale from 1e-32 to 1e4: expected chance passes for seven tests. The procedure enumerator with W skipped at 2.7e-13, text key with shift table at 6.8e-27, with a plaintext mask at 4.4e-10, with a ciphertext mask at 5.7e-9, Morse mask with free substitution at 8.9e-11 and digit-wise addition at 1.3e-30, each with K4 0 and closed; the text key with masks on both sides at about 5,390, right of the 1-expected-pass line, with K4 5,970 and undecidable](/assets/kryptos-k4-w-morse-digits.svg)

## What this research shows

- With W treated as a null in the key index, the procedure enumerator (up to 2 errors) and the text keys with a shift table, σ or τ give 0 on K4.
- A key read backwards is the same family as a key read forwards when the stride and start are free; the measured counts agree exactly.
- A per-position operation on Morse code cannot map the cribs in its pure form, at any position rule; with a free substitution after it, 0 of 22.4 million settings fit.
- Digit-wise addition of the 22 fixed digit strings gives 0 of 5,600 distinct settings.

## What this research does not show

It does not show that K4 is rarer than random: shuffled ciphertexts give 0 in every closed test. The text keys with masks on both sides are not decided: the crib sieve passes about as many settings as chance and the English stage was not run. Digit strings outside the 22, other operations on Morse code, other ways of treating W (for example as a separator that resets the key), and enumerator runs with more than 2 errors under W skipping were not tested.

## What changed

The W-as-null reading is closed for the enumerator and the one-sided text keys. The reversed key direction is recorded as identical to the forward family, not as a separate result.

## What failed

No setting fit. The reversed-direction test could not have given new information; it was run only to check the identity.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. The enumerator, the text-key runs (they read K1–K3 texts, the tableau and the World Clock names, which this site does not publish), the Morse-mask search with a free substitution and the digit-addition run on the 22 fixed strings (not listed here) are recorded, not rerun in the public package. The public check covers the W shifts, the chance values from the recorded setting counts, the direction identity, the Morse logic and the digit-addition mechanism with planted controls.

## UNKNOWN

Whether any of the 5,970 two-sided-mask passes reads as English. Running that stage needs a scorer that skips the five Ws and about 1.5 GPU hours; the researcher has not yet decided to run it. Whether W means anything in K4 ([EP-0135](/en/research/kryptos-k4-list-price/): compatible with chance once the target list is paid). External independent replications: zero.

## Falsification targets

A setting in any closed family that matches all 24 crib letters would overturn this; so would a defect that makes the search skip settings (every planted control was recovered). For the Morse mask, a Morse table different from the international one used here would reopen the pure form.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-morse-digits): `python verify_w_morse_digits.py` recomputes the W shifts of the cribs, the chance values of the text-key gates, the direction identity for text lengths 2–60 and 97, the Morse logic and the digit-addition mechanism with 30 planted controls on random digit strings, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-morse-digits). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

The English stage for the two-sided masks under the W-skipping index, if the researcher decides to run it (one run covers the reversed direction too).

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- International Morse code: ITU-R M.1677-1 (2009).
