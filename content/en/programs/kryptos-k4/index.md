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

## Families examined so far (as of 2026-09-24)

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

The reading of the W gaps as `TOKIO` (the German spelling of Tokyo, which appears on Berlin's World Clock) remains the one pattern that passed a frozen external target list, at p ≤ 1.5 × 10⁻³. It is provisional and gives no plaintext.

<!-- GENERATED: program-current:START -->
## Current public state

No decryption and no new plaintext letter. EP-0057 reproduced the observation that two of the five Ws bracket the public cribs from outside, but without choosing the letter W the chance is 0.036, and it is not independent of the TOKIO reading of the W gaps. Reading the Ws as nulls, key restarts, block boundaries or pass-through symbols of a 25-letter cipher produced no candidate.

**Evidence boundary:** Exploratory computation on the public ciphertext and 24 crib letters. Not preregistered; no external independent replication and no review by a cryptographer. The ground truth exists but is withheld.

**[Read the current Research Note (EP-0057) →](/en/research/kryptos-k4-w-brackets/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## Published Research Notes

1. **[[en/research/kryptos-k4-w-brackets/index|EP-0057 — Do the Ws that bracket both K4 cribs carry structure?]] (latest)**
<!-- GENERATED: program-history:END -->

## Sources

Jim Sanborn, *Kryptos* (1990); ciphertext as transcribed on [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) and by [Elonka Dunin](https://elonka.com/kryptos/). Crib releases: [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020 ([transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)), [Elonka Dunin's archive](https://elonka.com/kryptos/) for `EAST`. Sanborn's 2025 clues: [Scientific American](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/). The 2025 archival discovery: [RR Auction](https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/). The ciphertext and cribs are quoted for research and commentary and are not licensed by this site.
