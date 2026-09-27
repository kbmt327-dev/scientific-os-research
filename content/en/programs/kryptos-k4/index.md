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

## Progress so far

The program began by pricing claims brought in from outside. The claim that K4 is a reversed Gromark cipher with primer 57973 reproduces numerically but cannot be told from chance with the public cribs (EP-0001). Reading the W gaps as `TOKIO` passed the World Clock place list at p ≤ 1.5 × 10⁻³ (EP-0011); once six target lists conceivable before looking at K4 were paid for, the expected number of chance hits became 0.054, compatible with chance ([EP-0135](/en/research/kryptos-k4-list-price/)).

It then examined the K1–K3 form (one chart, shifted) broadly: periodic and running keys, masks, carving errors, physical keys. Every decidable family either gave no candidate or cannot be decided by the cribs. K4's flat letter frequencies need at least 3 bits of key per position.

From 2026-09-26 it turned to methods outside that form: digraph squares, Hill, Slidefair, Portax and Doppelkasten, rotor machines, Enigma-type machines, and, instead of choosing families by hand, an enumerator of 4.7 × 10¹⁵ procedures built from a grammar of parts ([EP-0119](/en/research/kryptos-k4-procedure-enumerator/)). Wherever the cribs decide, none is compatible. Random ciphertext usually fails the same way, so K4 is not shown to be rarer than random.

Family-by-family results are in **[Families examined](/en/programs/kryptos-k4/families)**.

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

No decryption and no new plaintext letter (as of 2026-09-27). What has been tested is only whether a procedure short enough to write down is compatible with the 24 crib letters, and every answer is no. Besides the K1–K3 form (one chart, shifted), methods outside it (digraph squares, Hill, Slidefair, Portax and Doppelkasten, rotor machines, an Enigma-type machine behind a free substitution) and an enumerator of 4.7 × 10¹⁵ procedures built from a grammar of parts gave no candidate wherever the cribs decide. These are logical refutations; none shows K4 to be rarer than random. K4's flat letter frequencies need at least 3 bits of key per position, and hand-made charts, homophones and codebooks cannot be decided without an outside source for the chart, the device or K5. The TOKIO reading of the W gaps is compatible with chance once the choice of target list is paid (expected 0.054, EP-0135).

**Evidence boundary:** Exploratory computation on the public ciphertext and 24 crib letters. Not preregistered; no external independent replication and no review by a cryptographer. The ground truth exists but is withheld.

**[Read the current Research Note (EP-0135) →](/en/research/kryptos-k4-list-price/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## Published Research Notes

1. [[en/research/kryptos-k4-57973-audit/index|EP-0001 — Does primer 57973 stand out once the model's freedom is counted?]]
2. [[en/research/kryptos-k4-tokio-price/index|EP-0011 — How much is the TOKIO reading of K4's Ws worth?]]
3. [[en/research/kryptos-k4-w-brackets/index|EP-0057 — Do the Ws that bracket both K4 cribs carry structure?]]
4. [[en/research/kryptos-k4-letter-graph/index|EP-0101 — Which ciphers does the crib's letter graph rule out without choosing a key?]]
5. [[en/research/kryptos-k4-consistency/index|EP-0113 — Which ciphers do K4's cribs refute by consistency alone?]]
6. [[en/research/kryptos-k4-procedure-enumerator/index|EP-0119 — Does any fully specified procedure built from a grammar of parts fit K4?]]
7. **[[en/research/kryptos-k4-list-price/index|EP-0135 — What is the TOKIO reading worth once the choice of target list is paid?]] (latest)**
<!-- GENERATED: program-history:END -->

## Sources

Jim Sanborn, *Kryptos* (1990); ciphertext as transcribed on [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) and by [Elonka Dunin](https://elonka.com/kryptos/). Crib releases: [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020 ([transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)), [Elonka Dunin's archive](https://elonka.com/kryptos/) for `EAST`. Scheidt on masking the English and solving the technique first: [WIRED 2005](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/). Sanborn's 2025 clues: [Scientific American](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/). The 2025 archival discovery: [RR Auction](https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/). The ciphertext and cribs are quoted for research and commentary and are not licensed by this site.
