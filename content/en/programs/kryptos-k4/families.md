---
title: "Kryptos K4: families examined"
description: Every cipher family examined for K4 so far, with its result.
lang: en
---

Every family examined in the [Kryptos K4 program](/en/programs/kryptos-k4/), one row each (as of 2026-09-27). Results read as on the program page: "rejected" means no setting in the stated range reproduces the cribs while planted positive controls are found; "not distinguishable" and "not decidable" are not rejections.

This table summarizes the internal record. Only the rows marked with a public Note currently have a public rerun.

| Family | Result |
|---|---|
| Any single-alphabet periodic key, periods 1–96 | Rejected at all 49 testable periods; the rest have no two crib letters sharing a residue |
| Periodic key with a free alphabet per residue, period ≤ 24 | Rejected by the cribs or by column letter statistics |
| Any English running key | Rejected as a class |
| Progressive and Gromark-type difference keys | Rejected; Gromark with free alphabets is not distinguishable |
| Any rearrangement alone (transposition, route, folding) | Rejected: K4's letter counts cannot be English |
| Keyed columnar transposition and K3-style rotation, each with a periodic key | No candidate |
| Hill (n = 2–4) with transposition; Trifid with word cubes | No candidate |
| Any cipher whose output uses 25 symbols or fewer | Impossible, since K4 uses all 26 letters. Playfair is also impossible if W passes through ([Note](/en/research/kryptos-k4-w-brackets/)) |
| Two stacked keyword layers | No candidate in 1.4 × 10¹⁰ settings |
| Ws as nulls, key restarting at W, W-gaps as blocks, W pass-through with 25 letters | No candidate ([Note](/en/research/kryptos-k4-w-brackets/)) |
| Row transposition with a periodic key | Not distinguishable from shuffled controls |
| Periodic key followed by two 7 × 7 turning grilles | No candidate in 2.09 × 10¹⁰ settings |
| Reading along the bands of a wave; the intensity of a sine wave as the key | No candidate |
| Devices with no fixed points (Enigma with a reflector, M-94 and M-138-A disks and strips, HC-9) | Impossible if plaintext and ciphertext positions coincide: the cribs contain the self-encryptions S→S and K→K |
| Hagelin M-209 (lug cage without overlaps, standard constant) | Fits the cribs, but the other 73 letters never become English; the number of crib-fitting cages is not distinguishable from shuffled controls (p ≈ 0.06) |
| Hagelin CX-52 (regular stepping) | Not distinguishable by the cribs in the sampled range |
| Winding the copper screen around the petrified-wood trunk and keying each letter by the layer it overlaps | No candidate (circumference measured from photos as 19–25 columns) |
| Physical keys that do not depend on height (surface direction, distance along the arc, and similar) | Rejected without measuring the shape: two crib pairs share a column (positions 32 and 63, 33 and 64) and would need equal keys, which fails under every convention |
| Fractionated Morse; a Berlin Clock advanced one step per letter with its lit-lamp counts as the key; overlays by folding at the seam or mirroring; reading from the back | No candidate |
| The time a shadow edge crosses each letter; the tableau seen behind the screen from a standing point (judged by whether the key is smooth between neighbouring letters) | The crib keys are as rough as random keys and do not fit such smooth keys |
| Over the whole plausible range of the 3D model's shape: the letter seen behind each hole, the minute sunlight starts or stops on each letter, the distance from a fixed point | No setting fits the cribs; the best scores are indistinguishable from shuffled controls |
| Allowing one to five carving errors (rechecking the main rejections above) | With one error the main rejections hold and no family reopens. With up to five, tightly constrained families stay closed (periodic keys p ≤ 16 and 18–22, Trifid, Hill n = 2, and others) while loosely constrained ones become undecidable by the cribs (free-alphabet periodic keys p ≥ 10, Hill n = 3, English running keys, and others) |
| A fixed substitution that masks the English, placed before or after encryption: stride keys from the Kryptos text and the World Clock, distance keys, M-94 (12 disk orders), autokeys, keys linear in position | No candidate (positive controls recovered). M-94 with a free disk order is undecidable by the cribs |
| Masks on both sides with a stride running key (15.41 million settings) | Neither the number of crib-passing settings nor the best English score is distinguishable from shuffled controls |
| Preregistered follow-up of doubled letters lining up at i ≡ 4 (mod 7) | Indistinguishable from chance |
| A method that switches between segments (each crib judged separately): keyword, periodic and stride keys | No candidate in any segment |
| One rotor with free wiring; a chart built from powers of one permutation | Incompatible with the cribs (positive controls 200/200; [Note](/en/research/kryptos-k4-rotors/)) |
| A running key from the text of Carter & Mace, *The Tomb of Tut.ankh.Amen*, vol. 1 (1923), with text and preprocessing frozen before running | Rejected with no mask or a one-sided mask (up to two crib errors, positive controls 60/60); no English with masks on both sides |
| Hagelin machines (M-209, CX-52) with a mask | Their freedom exceeds what English can constrain by tens to 200 bits; not decidable from K4 alone |
| `ROLL` as a key that turns the chart (three readings); the cut-out holes read as windows onto a key (96 readings, 4,081 keys, listed before running) | Rejected with no mask or a one-sided mask; no English with masks on both sides |
| A hand-chosen English running key with a one-sided mask | Not decidable with the current search (with an unknown substitution it does not recover positive controls); not a rejection |
| The sculpture's own text used as the coding chart (18,624 settings, fixed before running) | Rejected: K4 scores at most 6/24, and all 1,000 shuffles score 6 or more; positive controls 12/12 ([Note](/en/research/kryptos-k4-key-bound/)) |
| Maps that do not depend on position (windows of four letters or fewer, a word-level alphabet, fixed homophonic substitution) | Impossible without errors: `EAST` occurs twice in the crib `EASTNORTHEAST` and enciphers differently ([Note](/en/research/kryptos-k4-key-bound/)) |
| Key sources named by the hints, combined through a hand-made Latin-square chart: the tableau at K4's place, carved column numbers, keyword and digit-string phases, text offsets, clock hands, the carved geometry, positions of T, short texts | No source supported: pass rates at or below the chart-shape null ([Note](/en/research/kryptos-k4-key-sources/)) |
| Clock-type keys (linear in position, clock hands) and autokeys (plaintext lags 1–4, ciphertext lags 1–21) | Excluded wherever the cribs decide; the structures that stay feasible are feasible for random ciphertext just as often |
| Chaocipher starting from hint and English-word alphabets; a cursor walking over the carved texts | No candidate (0 of 20.6 million and 0 of 5,832) |
| Letters written in base 2 (Vernam type) or base 3 (arithmetic Trifid type) | Base 2 would print a non-letter somewhere with probability ≥ 1 − 2.3 × 10⁻⁷; base 3 gives key fragments that are not English |
| Chart rows chosen by position: alphabets keyed by successive words (K1–K3, the World Clock places, the hint words), carved panel lines, the M-94 cylinder with any disk order, mixed alphabets from matrices | No candidate (0 of 386,048; 0 for every M-94 disk order; 0 of 190 million) |
| Any system that keeps a fixed partition of the alphabet into blocks under 21 letters (cube positions, Morse-length classes, keyboard rows, halves, Polybius lines) | Impossible: all 21 crib letters form one connected component of the plaintext–ciphertext graph ([Note](/en/research/kryptos-k4-letter-graph/)) |
| A key made of two texts (K1–K3 plaintexts, the carved panel) | No candidate (0 of 66.4 million) |
| Occurrence-count ciphers; switching between Vigenère and Beaufort | Impossible / no candidate (0 of 16.5 million switching patterns; [Note](/en/research/kryptos-k4-consistency/)) |
| 25-letter squares with W as separator: Four-square, Two-square, Bifid (keyword and free squares), CM-Bifid, also with a shift mask before or after; Playfair followed by a shift mask | No candidate: keyword squares 0 of 925,600, free squares logically inconsistent with the cribs ([Note](/en/research/kryptos-k4-w-squares/)) |
| 2-D shifts, rotations and mirrors on a 5 × 5 grid | No candidate where decidable; long periods with free squares are not decidable ([Note](/en/research/kryptos-k4-w-squares/)) |
| Slidefair, Portax, Doppelkasten | Slidefair and Portax never encipher a letter to itself, so S→S and K→K exclude them; single-pass Doppelkasten is inconsistent in all 96 settings; double-pass is not decidable ([Note](/en/research/kryptos-k4-consistency/)) |
| Affine maps that change with position; Hill with periodically changing matrices, also with matrices taken from texts | No candidate where decidable (text matrices 0 of 2.38 million); long periods with free matrices are not decidable ([Note](/en/research/kryptos-k4-affine-hill/)) |
| Rotor machines: one free rotor with entry and exit alphabets or stepped by position keys; two moving rotors with a free slow rotor (7.9 × 10¹⁰); reflector machines (commercial Enigma and others, no plugboard) behind a free substitution (1.11 × 10¹⁰) | No candidate ([Note](/en/research/kryptos-k4-rotors/)) |
| An enumerator of fully specified procedures (274 alphabets × 16.6 million row selections × 10 chart forms, 4.7 × 10¹⁵ procedures), also with a stacked shift mask, per crib, and with up to three crib errors | No procedure fits K4 ([Note](/en/research/kryptos-k4-procedure-enumerator/)) |
| Carving errors against the closed different methods | One or two errors would reopen several closed families, but just as often for random ciphertext; the errors do not single out a family |

Every negative in the rows added on 2026-09-27 (from "Key sources named by the hints" down) is logical: the family cannot reproduce the cribs. In none of them is K4 rarer than random ciphertext, which usually fails too.

The reading of the W gaps as `TOKIO` (the German spelling of Tokyo, which appears on Berlin's World Clock) passed a frozen external target list at p ≤ 1.5 × 10⁻³ ([Note](/en/research/kryptos-k4-tokio-price/)). A later check (2026-09-27) also paid for choosing the list: against the union of six lists frozen before looking at K4 (3,036 words), the expected number of chance hits for K4's reading family is 0.054, of which the World Clock contributes 3.7%; counting the other markers in K1–K4 as well, there is one hit against 0.211 expected (p = 0.19). The reading is compatible with chance and is no longer a pattern that stands out ([Note](/en/research/kryptos-k4-list-price/)). Mechanisms that treat the Ws as markers inserted or overwritten after encryption also gave no candidate.

The program began by auditing a claim that K4 is a reversed Gromark cipher with primer 57973. Its numbers reproduce, but the public cribs cannot tell it from chance ([Note](/en/research/kryptos-k4-57973-audit/)).
