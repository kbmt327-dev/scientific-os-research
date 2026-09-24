---
research_id: KRYPTOS-K4-EP-0011
title: How much is the TOKIO reading of K4's Ws worth?
date: '2026-09-19'
lang: en
domain: Kryptos K4
type: Finding
status: Passed an exact null at p ≤ 1.5e-3; exploratory; gives no plaintext
evidence_level: Exact closed-form null against a place list frozen before testing
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the place names on Berlin's World Clock, frozen from the designer's site before the test was written
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: A statement about where the Ws fall in K4; not about the encryption method,
  and the choice of the World Clock as the target list is not paid for
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0011
source_episode_sha256: eb6a82b83152b062f74ae6456b075e7a0a526f4249852fcca701c3095adbcc3e
publication:
  status: publishable
tags:
- kryptos-k4
- multiplicity
- exact-null
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-tokio-price/" hreflang="ja">日本語</a></p>

## Current finding

The five Ws in K4 are 20, 15, 11, 9 and 15 letters apart counting from the start, which read as letters (A=1) spell `TOKIO`, the German spelling of Tokyo engraved on Berlin's World Clock. `BERLINCLOCK` is one of K4's public cribs. Once every freedom in how the gaps can be read is paid, the chance that some reading of a shuffled K4 hits some place name on the clock is at most **1.48 × 10⁻³**. That is 88 times weaker than the first estimate. The whole difference comes from accepting short place names, and `ROM` alone carries 70% of the price. The reading says nothing about how K4 was enciphered.

## Key figure

![Log-scale bars: 1.11e-6 for one named target, 1.68e-5 for all 17 five-letter names, 1.48e-3 for names of any reachable length; a stacked bar shows 3-letter names 69.7%, 4-letter 29.1%, 5-letter 1.1%](/assets/kryptos-k4-tokio-price.svg)

The top bars show the price as each freedom is paid. The bottom bar splits the final price by the length of the accepted place name.

## What this research shows

- The target list is finite and external: 146 place names from the official site of the clock's designer, Erich John, frozen before the test was written. Seventeen of them have five letters.
- The null has a closed form. A letter that occurs m times sits on a uniform m-subset of the 97 cells, and every reading can be inverted, so the expected number of hits is a finite sum. It needs no simulation and no extrapolation.
- Paying for the occurrence count and the target length, which the first estimate had fixed by choice, moves the value from 1.68 × 10⁻⁵ to 1.48 × 10⁻³.
- Across about 36,000 strings from K2 ciphertext and K3 plaintext windows, no place name appears. The exact null expects 0.76, so this checks the calculation rather than adding evidence.

## What this research does not show

It is not a confirmatory p-value. The choice of the World Clock as the target list was made after the cribs pointed to it, and that choice cannot be enumerated. It gives no key, no route and no plaintext letter. It is not independent of other observations about the same five W positions.

## Research question

The `TOKIO` reading had been left untested because "a meaningful five-letter string" cannot be defined. Once the crib `BERLINCLOCK` was tied to the World Clock, the clock's place list could serve as an external target set. What is the reading worth against that set when every freedom is paid?

## Why this matters

A striking pattern is priced by the freedoms used to find it. Here the arithmetic of the first estimate was right; what it missed were two choices outside the enumeration. They were found and paid before the result was built on, not afterwards.

## Method

- **Target set.** The designer's list of 146 names (captured through the Internet Archive, 12 Aug 2020), frozen with a hash before the test code.
- **Reading family.** Every letter multiplicity that K4 has (1–6 and 8), gaps counted as letters between or as differences, four anchors (start, zero, cyclic, none), two directions, A=1 or A=0. Target lengths reachable under this family are 1–8, and 95 of the 146 names have such a length.
- **Exact null.** For each name, the number of position sets that yield it, times the number of letters with that multiplicity, over C(97, m), summed. Markov's inequality gives P(at least one hit) ≤ E[hits].
- **Checks.** The inverse images were verified by planting them into synthetic texts (580 of 580 reproduced). A 2,000,000-draw simulation gave 29 hits for the five-letter version against 33.7 expected (−0.8σ).

## Results

K4 produces 69 distinct strings under the family; one of them, `TOKIO`, is on the list.

| Accepted place-name length | Exact P(at least one hit) |
|---|---|
| Any reachable length | **1.48 × 10⁻³** |
| Five letters or more | 1.75 × 10⁻⁵ |
| Exactly five letters | 1.68 × 10⁻⁵ |

By length, 3-letter names contribute 69.7% (`ROM` only), 4-letter names 29.1% (12 names), 5-letter names 1.1% (17 names) and longer names 0.04%. `OSLO` was added to the clock in 1997, after Kryptos was made; dropping it gives 1.44 × 10⁻³.

## What changed

The first estimate (per named target 1.11 × 10⁻⁶, from a shuffle simulation) was replaced by an exact value, and the target-list size, previously guessed, was counted from the source. The representative value moved from about 1.7 × 10⁻⁵ to 1.48 × 10⁻³.

## What failed

The first 200,000-draw simulation returned zero hits, which would have supported "p < 1.5 × 10⁻⁵". The exact value predicted 3.4 hits; the zero was a lucky draw (probability 0.034). The larger simulation agreed with the exact value.

## Evidence boundary

Public ciphertext and a public place list. Kryptos (1988–1990) corresponds to the 1985–1997 state of the clock, 134 names, which has not been enumerated; the post-1997 list of 146 was used. The price is dominated by short names of major cities that were very likely on the clock from 1969, so the conclusion should be robust to the version, but that is an argument, not a measurement.

## UNKNOWN

The exact 1985–1997 list. Whether the Ws were placed on purpose. Any link between this reading and the encryption method. External independent replications: zero.

## Falsification targets

If the 1985–1997 list lacked `TOKIO`, the reading would lose its target. If a principled target list chosen before looking gave a comparable hit rate on ordinary texts, the value would mean little.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-tokio-null): `python verify_tokio_null.py` recomputes the exact null from the letters-only place list with the standard library in under a second and prints `PASS` when it matches the recorded result. It is a rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Reading family, closed-form null, letters-only place list and recorded result](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-tokio-null). Code and results are MIT-licensed. The ciphertext is quoted, and the place names are factual data from the cited source; neither is licensed here.

## External audit

External independent replications: zero. No cryptographer has reviewed this note.

## Next experiment

Enumerate the 1985–1997 list of 134 names from period photographs or records, and recompute.

## Sources

- K4 ciphertext: Jim Sanborn, *Kryptos* (1990). Public transcriptions: [Wikipedia, "Kryptos"](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin's Kryptos page](https://elonka.com/kryptos/).
- The W-gap reading `20, 15, 11, 9, 15 → TOKIO`: [matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0).
- `BERLINCLOCK` refers to Berlin's World Clock: [Scientific American, 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/).
- Place names and the history of the list (80 names in 1969, 134 after 1985 with German spellings, 146 after 1997): official site of the designer, Erich John, [weltzeituhr-berlin.de](https://weltzeituhr-berlin.de/en/places-worldtimeclock), via the [Internet Archive](https://web.archive.org/web/20200812142431/https://weltzeituhr-berlin.de/en/places-worldtimeclock).
- `OSLO` added in 1997: *Berliner Zeitung*, 12 Dec 1997.
