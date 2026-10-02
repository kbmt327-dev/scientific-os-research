---
research_id: KRYPTOS-K4-EP-0168
title: Does one phase break reopen the rotor, Enigma or Hagelin machines?
date: '2026-09-30'
lang: en
domain: Kryptos K4
type: Negative Result
status: With one phase break (1,300 positions and sizes, 10.3 bit), one free-wiring rotor in two forms and Enigma behind a free substitution still give 0 settings (logical refutation, not rarer than random); a Hagelin-type machine with a break gave no English-like setting, but its controls were not run and its null was not size-matched, so it is undecidable; Chaocipher is out of scope. On 2026-10-02 the Hagelin-type row became closed within the family (controls planted under K4's own crib stage 5/5, K4's 38.64 reproduced)
evidence_level: Exact injectivity tests on the public ciphertext and cribs, decision rule committed before any run on K4, planted controls 100/100, 100/100, 20/20; the Hagelin-type run (EP-0176) used an English hill-climb with no planted controls and three shuffles of unmatched size; 2026-10-02, five controls planted under K4's own crib stage, 5/5
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; exact wiring and substitution tests, shuffled-ciphertext nulls, planted machines with planted breaks; for the Hagelin type, an exhaustive crib stage and an English 4-gram hill-climb (EP-0176)
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One break (b = 22–73, t = 1–25) added to the rotor families R-a and R-b, Enigma-type machines behind a free substitution (EP-0132 settings) and a no-overlap M-209-type machine without a mask; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0168
source_episode_sha256: 990614ffce8ad8a16d5c602486def2c50d15bdb25e6ebd50c0df821a4db5aeeb
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-machine-phase-break/" hreflang="ja">日本語</a></p>

> **Later check (2026-10-02).** The Hagelin-type-with-a-break row moved from undecidable to closed within the family: five controls planted under K4's own crib stage were all recovered as the global English maximum (E 126–156, all ≥ 40.4), while K4's maximum stays 38.64 (reproduced on engine v5). The text and numbers below are unchanged from 2026-09-30. Details are in the section "Later check (2026-10-02)" directly below.

## Later check (2026-10-02)

Of the two reasons that kept the Hagelin-type-with-a-break row undecidable, the planted controls were run on 2026-10-02.

**The registered size rule could accept nothing.** The registered rule accepted a planted control if the size L of its crib stage (the leaf count of that stage) was at most 5 × 10⁸, with 10 controls planned. Sizing seeds 0–4 all had L above 5 × 10⁸ and none was accepted (two sizing runs: the first ended after 75 min by a GPU driver event with rc −1, the second was stopped after seed 4 at 66 min). This is structural: a planted ciphertext agrees with its own true key at the 24 crib positions, so its crib stage counts that key's whole neighbourhood and cannot be small.

**The amended construction was committed before any control ran** (kryptos-k4-audit 1fae8ca; the engine in 3e0b3b2). Plant under K4's own crib stage: draw one row of K4's crib stage (cage, split m, t, pin-solution count ns) with probability proportional to ns × |b range(m)|, take one crib-consistent pin solution of that row, b uniform in its range, the unconstrained pins at random, and encrypt corpus English with the 24 cribs forced in by the same formula. The control equals K4 at the 24 crib positions and its allowed-bit set is K4's, so its crib stage (274,604 rows, 1,020,522,169 climbs) is K4's by construction; each English stage costs one K4 run. n = 5, adequate iff at least 4/5. The power of this check itself is P(≥ 4/5) = 0.34 at a true recovery rate of 0.6 and 0.92 at 0.9.

**Engine v5 (80d263d).** The free-pin structure is built once per (row, b) pair and shared (thread state 16 KB → 2.3 KB); same leaves, same RNG stream, same climb, float64 in the same order. On a 60-row check the CPU kernel, v4 and v5 agree bit for bit on the per-row counts, best E and best P. Speed × 1.76 (3,654 rows, 1.9 × 10⁶ leaves: v4 9.7 s, v5 5.5 s).

| Control | Cage | b | t | E_true | Truth is the global maximum | Leaves E ≥ 40.4 | Time |
|---|---|---|---|---|---|---|---|
| 0 | 2, 2, 3, 5, 10, 1 | 40 | 23 | 126.36 | yes | 2,071 | 46 min |
| 1 | 7, 3, 2, 1, 9, 2 | 60 | 23 | 139.16 | yes | 89 | 45 min |
| 2 | 5, 8, 3, 3, 2, 2 | 57 | 19 | 130.44 | yes | 265 | 45 min |
| 3 | 1, 1, 3, 3, 6, 8 | 67 | 15 | 156.44 | yes | 2,634 | 44 min |
| 4 | 3, 9, 1, 2, 7, 1 | 35 | 16 | 151.59 | yes | 91 | 44 min |

K4 rerun on v5: E_max 38.64, 29,578 leaves with E ≥ 20, 0 with E ≥ 40.4, 1,020,522,169 climbs, identical to the v4 record (crib stage 137 s, English stage 2,529 s).

**Verdict: undecidable → closed within the family** (M-209 type, six pinwheels 26/25/23/21/19/17, no-overlap cages, C = 25 − P + k, one break, no mask). In two columns: logical refutation, yes (no leaf of K4 reaches 40.4 while every planted truth reaches 126–156 and is the global maximum); rarer than random, not judged (no size-matched null). Two caveats. The planted class passes the crib stage by construction, so only the English stage's power on K4's own leaf set is tested. The control plaintexts are corpus English with the cribs, so a less English-like K4 plaintext could score lower.

**Record.** When the researcher tailed the K4 v5 log, the top-3 leaf strings (below the threshold, E ≤ 38.64; hill-climb outputs) were displayed; they were not used for anything.

**What the package now checks.** `verify_machine_phase_break.py` checks that the five recorded control ciphertexts equal K4 at the 24 crib positions, that each decrypts under its recorded key to the cribs at 21–33 and 63–73 (the text is not printed), that the crib-position key values k_i = (C_i − 25 + P_i) mod 26 of K4 and of every control agree (the identity behind "same crib stage"), the acceptance arithmetic (5/5 ≥ 4/5; the binomial 0.34 and 0.92), and that every control's E_true ≥ 40.4 while K4's 38.64 < 40.4. The five control runs (about 45 min each on a GPU) and the K4 v5 rerun are recorded, not rerun.

## Research question

The [rotor Note](/en/research/kryptos-k4-rotors/) closed one free-wiring rotor and Enigma-type machines behind a free substitution. A real machine can slip, or an operator can skip ahead. If the machine's step state jumps once, somewhere in the message, do those machines become consistent with the cribs? And does the same break let a Hagelin-type machine through?

## Why this matters

A single slip is a small, physically plausible change, and it costs little: 52 positions between the cribs times 25 sizes. If a family closed without a break reopened with one, the earlier closure would have been fragile. The only source pointing to machines is Scheidt's background, so this is a different method with no direct hint behind it; the 10.3 bit of the break is paid for in the tests.

## Method

- **The break.** From position b on, the machine's step state is displaced by t (t = 1–25). Only b = 22–73 matters: earlier or later it is no break or just a different starting point. The 24 crib letters fall into 23 distinct splits (every b from 34 to 63 gives the same split), so the test runs over 23 × 25 = 575 classes; counted by b, 1,300 (b, t), 10.3 bit.
- **Rotors.** One free wiring, displaced by t from b on. R-a: keyed entry and exit alphabets (274 each) and step d, 1,951,976 settings (it contains the single rotor of EP-0083). R-b: one alphabet and 329,366 position-only keys, 90,246,284 settings. A wiring exists exactly when equal inputs go with equal outputs, so each (setting, split, t) is a yes-or-no check.
- **Enigma + σ.** The 1.11 × 10¹⁰ settings of EP-0132 (commercial reflector machines behind a free substitution). The break is t extra machine steps at b, with the normal carries. The chance expectation is 4.5 × 10⁻⁵ passes in total.
- **Checks and controls.** The rotor kernel matched brute force on 3,000 cases; the Enigma tables matched an existing simulator on 3,960 letters and published Enigma I test vectors. Planted machines with planted breaks: 100 for R-a, 100 for R-b, 20 for Enigma. Nulls: 200 shuffles of K4 for the rotors, 10 for Enigma (fixed from the measured speed before the K4 run).
- **Hagelin type (EP-0176).** Six pinwheels (26, 25, 23, 21, 19, 17), free pins, all 1,107,567 no-overlap cages, C = 25 − P + k, plus one break. A crib stage enumerated every crib-consistent pin solution; an English stage then hill-climbed the remaining free pins of each one (6 random starts) on a 4-gram score E. The threshold E ≥ 40.4 was fixed before the K4 run.
- **Chaocipher.** Its state is two alphabets permuted by the text, with no step counter, so a phase break is not defined. Not run.

## Results

| Family | Settings × breaks | Capacity | K4 | Shuffles | Planted |
|---|---|---|---|---|---|
| Free-wiring rotor R-a | 1,951,976 × 1,300 | 31.2 bit | **0** | 0 of 200 | 100/100 |
| Free-wiring rotor R-b | 90,246,284 × 1,300 | 36.8 bit | **0** | 0 of 200 | 100/100 |
| Enigma + σ | 1.11 × 10¹⁰ × 1,300 | 43.7 bit | **0** (also 0 without a break) | 0 of 10 | 20/20 |
| Hagelin type (EP-0176) | 1.02 × 10⁹ climbs | search 52.6 bit | best E 38.64, none ≥ 40.4 | best E 24.4 / 28.2 / 28.5 (about 2 × 10⁶ climbs each) | not run |
| Chaocipher | — | — | not defined | — | — |

For the Hagelin type, K4 had 274,604 crib-consistent classes and 1.02 × 10⁹ (solution, b) climbs; 29,578 reached E ≥ 20. The three shuffles had about 500 times fewer climbs each. The best score grows with the number of climbs, so K4's 38.64 cannot be compared with the shuffles' values. No planted Hagelin machine was searched, so it is unknown whether a climb from the true pins reaches the true plaintext. The researcher deferred these controls as low priority; at this size a planted control would need on the order of 10¹⁰ climbs.

## Current finding

One phase break does not reopen the free-wiring rotors or Enigma behind a free substitution: 0 settings in every split and size, with every planted break found. Shuffled ciphertexts also give 0, so this is a logical refutation, not evidence that K4 is further from these machines than random. For the Hagelin type with a break, no setting reached the English threshold, but without planted controls and without a null of matched size this is **undecidable**, not a negative result.

## Key figure

![Upper panel: five rows. Free-wiring rotor R-a (31.2 bit) closed, K4 0, shuffles 0/200, planted 100/100; R-b (36.8 bit) closed, same; Enigma with a free substitution (43.7 bit) closed, K4 0, shuffles 0/10, planted 20/20; Hagelin M-209 type (search 52.6 bit) closed (controls 5/5), no score at least 40.4, controls under K4's crib stage 5/5 (2026-10-02); Chaocipher out of scope, no step counter. Lower panel: horizontal bars of the best English score for the Hagelin type on a 0–160 axis: K4 on engine v5 38.64 from 1,020,522,169 climbs, shuffles 24.43, 28.17 and 28.46 from about 1.9 to 2.2 million climbs each, all left of a dashed threshold line at 40.4; controls 0 to 4, each one K4-size run, reach their true plaintext at 126.36, 139.16, 130.44, 156.44 and 151.59, all right of the line. A note says the shuffles are still not comparable because they had about 500 times fewer climbs, that every control planted under K4's crib stage was recovered as the global maximum, and that K4's 38.64 stays below the threshold, so the row is closed within the family and not rarer than random](/assets/kryptos-k4-machine-phase-break.svg)

## What this research shows

- A single slip of the step state, at any position between the cribs and of any size, does not make one free-wiring rotor (R-a, R-b) or Enigma behind a free substitution consistent with the cribs.
- Every planted break was recovered (100/100, 100/100, 20/20), so the zero is not a blind test.
- The earlier closures of these families in the [rotor Note](/en/research/kryptos-k4-rotors/) are not fragile to one break.

## What this research does not show

It does not show that K4 is rarer than random for these machines: every shuffle also gives 0. It does not reject a Hagelin-type machine with a break: the run found no English-like setting, but its power is unknown and its null is about 500 times smaller. Two or more breaks, a slip of the fast Enigma rotor alone without carries, the overlapping-cage Hagelin, CX-52 variants and Hagelin with a mask were not tested. Chaocipher is outside this test.

## What changed

The rotor and Enigma closures now hold with one break as well. The Hagelin type with a break moved from "not run" to "run, undecidable", with the reasons stated: no planted controls and a null of unmatched size.

## What failed

No setting fit. The Hagelin run is the weak point: its negative cannot be used as a refutation until planted controls show that the climb finds a true key at this size.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. The full rotor and Enigma sweeps and the Hagelin run are recorded, not rerun in the public package. The public check recomputes the break counts, capacities, the Enigma chance expectation and the exact single-rotor test with a break.

## UNKNOWN

Whether the Hagelin-type climb would recover a planted key with a break at K4's size. How a size-matched null distributes the best score. External independent replications: zero.

## Falsification targets

A rotor or Enigma setting with one break that fits all 24 crib letters would overturn the logical part; so would an error in the injectivity test (the kernels matched brute force and test vectors, and every planted break was found). For the Hagelin type, planted controls showing that the climb reaches the true plaintext would turn the undecidable row into a real negative; a setting above 40.4 that survives a size-matched null would make it a candidate.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-machine-phase-break): `python verify_machine_phase_break.py` recomputes the 23 splits, 575 classes and 1,300 (b, t), the setting counts and capacities, and the Enigma chance expectation; it runs the exact single-rotor test with a break (A–Z or KRYPTOS numbering, step 0–25) on K4 and 200 shuffles, compares it with brute force, recovers 100 planted breaks, and prints `PASS`. Standard library only, about a second. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-machine-phase-break). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

(Done on 2026-10-02; see the later check above.) Planted controls for the Hagelin type with a break, accepted by the size of the crib-consistent set, and a null with as many climbs as K4. Two breaks for the rotors, if a source suggests them.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Enigma wirings: [Crypto Museum, Enigma wiring](https://www.cryptomuseum.com/crypto/enigma/wiring.htm).
