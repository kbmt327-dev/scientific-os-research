---
research_id: KRYPTOS-K4-EP-0165
title: Does the procedure enumerator fit K4 if the key position slips once inside or between the cribs?
date: '2026-09-30'
lang: en
domain: Kryptos K4
type: Negative Result
status: One slip inside each crib (480 settings, up to 4 crib errors) and a shift of ±1 or ±2 between the cribs (4 settings, up to 2 crib errors) give 0 procedures that fit K4; with no crib errors any shift between the cribs was already ruled out by an earlier per-crib run. Logical refutation within the grammar, not rarer than random. Periodic arbitrary rows with a shift cannot be decided
evidence_level: Exact enumeration with closed-form chance and two shuffles per run, planted controls; the slip runs were committed before running on K4; the periodic test was committed before its shuffle null but after one look at K4's consistency table
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; the procedure enumerator of an earlier Note (GPU); a table-free test for periodic arbitrary rows against 2,000 shuffles; planted controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only one key-position slip just before a crib letter inside each crib, or one shift of ±1 or ±2 between the cribs, within the grammar of the procedure enumerator and the stated crib-error tolerance; carved letters and crib letters stay at their carved positions; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0165
source_episode_sha256: e270f4d4a47bba1c4559aabec342ef51a7f0110cc7bfec4639e6f92ba01d0acf
publication:
  status: publishable
tags:
- kryptos-k4
- carving-errors
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-crib-shifts/" hreflang="ja">日本語</a></p>

## Research question

K2 has a precedent of one carved ciphertext letter removed. If, in K4, the count of positions slipped once (one key position skipped or used twice), does any procedure of the [procedure enumerator](/en/research/kryptos-k4-procedure-enumerator/) fit the cribs? Three places are checked: one slip inside each crib (EP-0149), one shift between the cribs in positions 34–62 (EP-0151), and the same shift together with crib errors (EP-0165).

## Why this matters

The enumerator judged both cribs at their carved positions. A single slip in between would change which key position each crib letter reads and so could hide a fitting procedure. The [coverage map](/en/research/kryptos-k4-capability-matrix/) listed this as an open gap.

## Method

- **Slip model.** Carved letters and crib letters stay where they are carved (Sanborn's hints match carved ciphertext letters to plaintext letters one to one). Only the key position read by selectors that count positions (linear in the position, periodic keyword, running text, position div or mod m) moves; selectors that read what is carved (ciphertext autokey, letter counts, the W brackets, carved rows and columns) do not.
- **Inside the cribs (EP-0149).** A slip of +1 or −1 just before a crib letter strictly inside each crib: 12 cuts × 2 × 10 cuts × 2 = 480 settings (8.9 bit). Up to 4 crib errors, using the error-tolerant index of the enumerator Note. Two shuffles on every tenth setting.
- **Between the cribs, no crib errors (EP-0151).** An argument, not a run: an earlier run judged crib 1 alone with every origin, and only 8 procedures pass crib 1, all of them self-reference identities (the second-layer key is the ciphertext itself). They depend on crib 1's words, so they do not carry to crib 2 (chance about 26⁻¹¹ each). Hence no shift between the cribs can make a procedure fit.
- **Between the cribs, with crib errors (EP-0165).** Crib 2 read at key position i + d, d = −2, −1, +1, +2 (4 settings), up to 2 crib errors. EP-0149's code imported unchanged.
- **Periodic arbitrary rows (EP-0151).** Outside the enumerator: the row at key position j is an arbitrary permutation chosen by j mod p (p = 1–48), crib 2 shifted by d = −2 to +2 (240 cells). For each cell, the fewest crib letters to drop so that every residue class is a partial one-to-one map; P = share of 2,000 shuffled ciphertexts that need no more drops.
- **Pre-registration.** The rules, settings and stop rule of EP-0149 and EP-0165 were committed before running on K4. The periodic test was committed before its shuffle null, but K4's consistency by p and d had been looked at once while timing, before the commit; its null is therefore not fully blind.

## Results

| Run | Settings | Crib errors | K4 hits | Two shuffles | Chance (closed form) | Planted controls |
|---|---|---|---|---|---|---|
| One slip inside each crib (EP-0149) | 480 | ≤ 4 | **0** (identities 0) | 0, 0 (48 settings each) | 1.0 × 10⁻⁶ | 18/18 slips; 18/18 slips + 1–4 carving errors |
| Shift between the cribs (EP-0151) | any | 0 | 0 (from the per-crib run) | — | — | — |
| Shift ±1, ±2 between the cribs (EP-0165) | 4 | ≤ 2 | **0** (identities 0) | 0, 0 | 3.6 × 10⁻¹³ | 9/9 shift only; 8/9 shift + carving errors |

- EP-0149 examined 5.7 × 10¹² candidate pairs in about 4 hours. Larger tolerances were not run: 69 s per setting at 5 errors and over 25 min at 7.
- In EP-0165 one planted text was missed: a two-layer plant with 2 ciphertext errors. Its first-layer selector was not logged, so the cause is unknown (perhaps ciphertext autokey spreading the errors, as seen in earlier runs; not verified).
- Periodic arbitrary rows: at every shift, 29–33 of the 48 periods fit with no crib letter dropped (the smallest such period is 6, at d = +1). The smallest P among the 240 cells is 0.015 (p 8, d +2). The expected smallest of 240 independent P values is about 0.004, and 11 cells are at or below 0.05 against about 12 expected. No cell is below shuffle level.
- EP-0166 needed no run: the 79 origins of i div m (m = 5, 7, 12, 24, 31) asked for are exactly the auxiliary features already tested in the [enumerator Note's](/en/research/kryptos-k4-procedure-enumerator/) fixed-origin addendum (EP-0143), with 0 new hits.

## Current finding

Within the enumerator's grammar, a single slip inside each crib (up to 4 crib errors) or a shift of up to two positions between the cribs (up to 2 crib errors) does not make any procedure fit K4. Shuffles give 0 as well and the chance expectations are tiny, so this is a logical refutation of the family, not evidence that K4 is further from it than random. For periodic arbitrary rows the capacity is too large: many periods fit at every shift, so the shift cannot be decided there.

## Key figure

![Left: horizontal bars on a log scale for the chance expectation of two enumerator runs with a slip, 1.0e-6 for one slip inside each crib (480 settings, up to 4 crib errors) and 3.6e-13 for a shift between the cribs (4 settings, up to 2 errors); K4 has 0 hits in both and two shuffles give 0 and 0. Right: the 240 shuffle P values of the periodic test, sorted and plotted against uniform quantiles; the points lie near or above the diagonal, the smallest being 0.015 at period 8, shift +2](/assets/kryptos-k4-crib-shifts.svg)

## What this research shows

- One key-position slip inside each crib, in either direction, gives 0 fitting procedures among 480 settings with up to 4 crib errors.
- A shift of ±1 or ±2 between the cribs gives 0 with up to 2 crib errors; with no errors any shift is excluded by the per-crib run.
- Planted slips are recovered (18/18, 18/18, 9/9; 8/9 with carving errors).

## What this research does not show

It does not show that K4 is rarer than random. It does not cover 5–7 crib errors together with slips inside the cribs, 3 or more errors with a shift between them, two or more slips in one crib, three or more slips, or families outside the enumerator tested on both cribs together (rotors, Enigma, squares) with a shift. For periodic arbitrary rows the answer is undecidable, not negative.

## What changed

The single-slip gap left by the enumerator is closed within the grammar and the stated tolerances. The question of extra origins for i div m turned out to be already answered by EP-0143.

## What failed

No setting fit. One planted control in EP-0165 was missed for a reason not established. The periodic test's null was committed after a first look at K4's table.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. The enumerator runs are recorded results (GPU), not rerun in the public package; the package reruns the counts, chance values and the periodic test.

## UNKNOWN

Whether larger error tolerances with a slip, several slips, or a slip in families outside the enumerator would fit. Why one EP-0165 control was missed. External independent replications: zero.

## Falsification targets

A procedure of the enumerator that fits all but at most 4 (inside) or 2 (between) crib letters under one of these slips would overturn this; so would an error in the slip model that keeps planted slips findable but misses real ones.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-crib-shifts): `python verify_crib_shifts.py` recomputes the 480 and 4 settings, the chance values, the 79 origins, EP-0151's periodic test on K4 (all 240 cells, exact match) and its shuffle P values for periods 3–20 with the author's generator and seed (exact match; `--full` does all 240 in about 8 minutes), and 10 planted periodic controls, and prints `PASS`. Standard library only, about 15 seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-crib-shifts). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Up to 7 crib errors together with a slip, if a faster index makes it affordable; a shift between the cribs in the rotor, Enigma and square families.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
