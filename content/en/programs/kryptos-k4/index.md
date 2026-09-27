---
title: Kryptos K4
description: An audit-first program on the unsolved fourth section of Jim Sanborn's Kryptos sculpture.
lang: en
---

K4 is the 97-letter fourth section of *Kryptos*, the sculpture Jim Sanborn installed at CIA headquarters in 1990. Twenty-four plaintext letters are public (`EASTNORTHEAST` and `BERLINCLOCK`). In 2025 the plaintext was found in archival papers, but it has not been published and the method has not been disclosed, so the ground truth exists and is withheld.

This program does not claim to have solved K4. It records which cipher families the public evidence rules out, how much each claimed pattern is really worth once the searcher's own freedom is paid for, and which questions the cribs cannot answer at all.

## The question

Which mechanisms can the 97 ciphertext letters and 24 crib letters rule out, and which apparent patterns survive once the freedom used to find them is counted?

## Evidence class

Public ciphertext and cribs only. Every test is exploratory unless a Note says it was sealed in advance. A rejected family means that no member within the stated range reproduces the cribs, with planted positive controls showing that the test would have found one. A "not distinguishable" family has more freedom than 24 letters can constrain; it is not rejected.

## Families examined so far (as of 2026-09-27)

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
| One rotor with free wiring; a chart built from powers of one permutation | Incompatible with the cribs (positive controls 200/200) |
| A running key from the text of Carter & Mace, *The Tomb of Tut.ankh.Amen*, vol. 1 (1923), with text and preprocessing frozen before running | Rejected with no mask or a one-sided mask (up to two crib errors, positive controls 60/60); no English with masks on both sides |
| Hagelin machines (M-209, CX-52) with a mask | Their freedom exceeds what English can constrain by tens to 200 bits; not decidable from K4 alone |
| `ROLL` as a key that turns the chart (three readings); the cut-out holes read as windows onto a key (96 readings, 4,081 keys, listed before running) | Rejected with no mask or a one-sided mask; no English with masks on both sides |
| A hand-chosen English running key with a one-sided mask | Not decidable with the current search (with an unknown substitution it does not recover positive controls); not a rejection |
| The sculpture's own text used as the coding chart (18,624 settings, fixed before running) | Rejected: K4 scores at most 6/24, and all 1,000 shuffles score 6 or more; positive controls 12/12 |
| Maps that do not depend on position (windows of four letters or fewer, a word-level alphabet, fixed homophonic substitution) | Impossible without errors: `EAST` occurs twice in the crib `EASTNORTHEAST` and enciphers differently |
| Key sources named by the hints, combined through a hand-made Latin-square chart: the tableau at K4's place, carved column numbers, keyword and digit-string phases, text offsets, clock hands, the carved geometry, positions of T, short texts | No source supported: pass rates at or below the chart-shape null |
| Clock-type keys (linear in position, clock hands) and autokeys (plaintext lags 1–4, ciphertext lags 1–21) | Excluded wherever the cribs decide; the structures that stay feasible are feasible for random ciphertext just as often |
| Chaocipher starting from hint and English-word alphabets; a cursor walking over the carved texts | No candidate (0 of 20.6 million and 0 of 5,832) |
| Letters written in base 2 (Vernam type) or base 3 (arithmetic Trifid type) | Base 2 would print a non-letter somewhere with probability ≥ 1 − 2.3 × 10⁻⁷; base 3 gives key fragments that are not English |
| Chart rows chosen by position: alphabets keyed by successive words (K1–K3, the World Clock places, the hint words), carved panel lines, the M-94 cylinder with any disk order, mixed alphabets from matrices | No candidate (0 of 386,048; 0 for every M-94 disk order; 0 of 190 million) |
| Any system that keeps a fixed partition of the alphabet into blocks under 21 letters (cube positions, Morse-length classes, keyboard rows, halves, Polybius lines) | Impossible: all 21 crib letters form one connected component of the plaintext–ciphertext graph |
| A key made of two texts (K1–K3 plaintexts, the carved panel) | No candidate (0 of 66.4 million) |
| Occurrence-count ciphers; switching between Vigenère and Beaufort | Impossible / no candidate (0 of 16.5 million switching patterns) |
| 25-letter squares with W as separator: Four-square, Two-square, Bifid (keyword and free squares), CM-Bifid, also with a shift mask before or after; Playfair followed by a shift mask | No candidate: keyword squares 0 of 925,600, free squares logically inconsistent with the cribs |
| 2-D shifts, rotations and mirrors on a 5 × 5 grid | No candidate where decidable; long periods with free squares are not decidable |
| Slidefair, Portax, Doppelkasten | Slidefair and Portax never encipher a letter to itself, so S→S and K→K exclude them; single-pass Doppelkasten is inconsistent in all 96 settings; double-pass is not decidable |
| Affine maps that change with position; Hill with periodically changing matrices, also with matrices taken from texts | No candidate where decidable (text matrices 0 of 2.38 million); long periods with free matrices are not decidable |
| Rotor machines: one free rotor with entry and exit alphabets or stepped by position keys; two moving rotors with a free slow rotor (7.9 × 10¹⁰); reflector machines (commercial Enigma and others, no plugboard) behind a free substitution (1.11 × 10¹⁰) | No candidate |
| An enumerator of fully specified procedures (274 alphabets × 16.6 million row selections × 10 chart forms, 4.7 × 10¹⁵ procedures), also with a stacked shift mask, per crib, and with up to three crib errors | No procedure fits K4 |
| Carving errors against the closed different methods | One or two errors would reopen several closed families, but just as often for random ciphertext; the errors do not single out a family |

Every negative in the rows added on 2026-09-27 (from "Key sources named by the hints" down) is logical: the family cannot reproduce the cribs. In none of them is K4 rarer than random ciphertext, which usually fails too.

The reading of the W gaps as `TOKIO` (the German spelling of Tokyo, which appears on Berlin's World Clock) passed a frozen external target list at p ≤ 1.5 × 10⁻³ ([Note](/en/research/kryptos-k4-tokio-price/)). A later check (2026-09-27) also paid for choosing the list: against the union of six lists frozen before looking at K4 (3,036 words), the expected number of chance hits for K4's reading family is 0.054, of which the World Clock contributes 3.7%; counting the other markers in K1–K4 as well, there is one hit against 0.211 expected (p = 0.19). The reading is compatible with chance and is no longer a pattern that stands out. Mechanisms that treat the Ws as markers inserted or overwritten after encryption also gave no candidate.

The program began by auditing a claim that K4 is a reversed Gromark cipher with primer 57973. Its numbers reproduce, but the public cribs cannot tell it from chance ([Note](/en/research/kryptos-k4-57973-audit/)).

## Where things stand (2026-09-27)

- **What has been tested**: only whether a procedure short enough to write down is compatible with the 24 crib letters. Every answer so far is no. These are logical refutations; none shows K4 to be rarer than random. No new plaintext letters.
- **A lower bound on the key**: K4's letter frequencies are flat, which needs at least 3 bits of key per position. That is more than the redundancy of English (about 2.86 bits), so a key chosen freely letter by letter cannot be determined from K4 alone. A solvable K4 must pair a short technique with a key source that has a short description. This points the same way as Scheidt's remark that once the technique is known the rest is a puzzle.
- **What cannot be decided**: hand-made charts, homophones, digraph charts, codebooks and multi-rotor machines with free wiring have more freedom than the cribs constrain. Deciding them needs an outside source for the chart, the device or K5. One hypothesis is that the key or chart was chosen by hand position by position; it would account for every observed feature and predicts that public data cannot decide K4. It is a hypothesis, not a conclusion.
- **Key sources**: the test that separates the key source from the chart (planned on 2026-09-26) found no supported source for a Latin-square chart.
- **In progress**: further hypotheses developed with the program's owner (within-word reordering, digraphs, an enumerator allowing four to seven crib errors) are being computed.
## Physical record and 3D model of the sculpture (2026-09-25)

To test whether the key might come from the sculpture's physical form rather than from letters, we estimated the sculpture's physical layout from public photographs and aerial imagery and built a 3D model (v0.5). It includes how the copper is assembled (four plates in a 2 × 2 arrangement, with the horizontal seam falling exactly at the K2/K3 boundary), the S-shaped plan, its orientation (the cipher side faces roughly south), the thickness of the petrified-wood trunk, and the layout of the three stones at the entrance that carry the Morse code (K0). Choosing a date and time at Langley places the sun and shows the light cast through the cut-out letters.

In v0.5 the column pitch was re-measured by fitting a camera and a cylinder to letters in a photograph, and the radius set so the two ends are 20 ft (6.1 m) apart, the published width. The entrance Morse holes follow proportions measured in photographs, and the compass rose's bearing was re-measured. In v0.5.1 all seven Morse phrases were checked dot by dash against photographs (they match the transcription), and the gaps between letters and between words were set to values measured in three photographs. The interface switches between Japanese and English, and the model can be saved as glTF (.glb) and the physical features of the 97 K4 letters as CSV.

Most dimensions and bearings are estimates (grade C) and should be read as approximate. The shape was fixed from photographs alone, without looking at the cribs. Research computations run over the whole plausible range of the shape (radius 1.4–2.4 m and so on). The public version withholds every carved letter except the 97 letters of K4 and the seven Morse phrases, showing only where each letter is cut.

**[Open the 3D model →](https://kbmt327-dev.github.io/scientific-os-research/static/kryptos-k4-model.html)** (Japanese / English)

<!-- GENERATED: program-current:START -->
## Current public state

No decryption and no new plaintext letter (as of 2026-09-27). What has been tested is only whether a procedure short enough to write down is compatible with the 24 crib letters, and every answer is no. Besides the K1–K3 form (one chart, shifted), methods outside it (digraph squares, Hill, Slidefair, Portax and Doppelkasten, rotor machines, an Enigma-type machine behind a free substitution) and an enumerator of 4.7 × 10¹⁵ procedures built from a grammar of parts gave no candidate wherever the cribs decide. These are logical refutations; none shows K4 to be rarer than random. K4's flat letter frequencies need at least 3 bits of key per position, and hand-made charts, homophones and codebooks cannot be decided without an outside source for the chart, the device or K5. The TOKIO reading of the W gaps is compatible with chance once the choice of target list is paid (expected 0.054). The latest Research Note is EP-0057.

**Evidence boundary:** Exploratory computation on the public ciphertext and 24 crib letters. Not preregistered; no external independent replication and no review by a cryptographer. The ground truth exists but is withheld.

**[Read the current Research Note (EP-0057) →](/en/research/kryptos-k4-w-brackets/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## Published Research Notes

1. [[en/research/kryptos-k4-57973-audit/index|EP-0001 — Does primer 57973 stand out once the model's freedom is counted?]]
2. [[en/research/kryptos-k4-tokio-price/index|EP-0011 — How much is the TOKIO reading of K4's Ws worth?]]
3. **[[en/research/kryptos-k4-w-brackets/index|EP-0057 — Do the Ws that bracket both K4 cribs carry structure?]] (latest)**
<!-- GENERATED: program-history:END -->

## Sources

Jim Sanborn, *Kryptos* (1990); ciphertext as transcribed on [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) and by [Elonka Dunin](https://elonka.com/kryptos/). Crib releases: [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020 ([transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)), [Elonka Dunin's archive](https://elonka.com/kryptos/) for `EAST`. Scheidt on masking the English and solving the technique first: [WIRED 2005](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/). Sanborn's 2025 clues: [Scientific American](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/). The 2025 archival discovery: [RR Auction](https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/). The ciphertext and cribs are quoted for research and commentary and are not licensed by this site.
