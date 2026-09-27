---
research_id: KRYPTOS-K4-EP-0113
title: Which ciphers do K4's cribs refute by consistency alone?
date: '2026-09-27'
lang: en
domain: Kryptos K4
type: Negative Result
status: Occurrence-count ciphers, free Vigenère/Beaufort switching with a periodic key, Slidefair, Portax and single-pass Doppelkasten are inconsistent with the cribs; logical refutations, not rarer than random
evidence_level: Exact consistency arguments on public ciphertext and cribs; the K4-only parts are fully rerunnable
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; exact consistency checks, shuffled-ciphertext nulls, planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Five cipher families as specified (occurrence-count keying, Vigenère/Beaufort switching, Slidefair, Portax, Doppelkasten); no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0113
source_episode_sha256: 89486e8a8e0fd05bc759a15136f5159e6170e843fd5ce644961c7842dda5d77c
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-consistency/" hreflang="ja">日本語</a></p>

## Research question

Some cipher families can be tested against the cribs without choosing a key at all, because the family forces a relation between crib letters that K4 either satisfies or not. Which families of this kind survive?

## Why this matters

These families were listed as untested "different methods" (ones that are not a single shifted chart). Consistency arguments settle them exactly, and they show which conclusions depend on luck in a search and which do not.

## Method

- **Occurrence-count ciphers (EP-0112).** The row used for a letter depends on how many times that plaintext letter has occurred. Two forms: a shift that advances by a common step d at each occurrence under arbitrary alphabets (C = τ(σ(x) + d·n_x + b)), and any chart that stays decipherable at every point.
- **Vigenère / Beaufort / variant switching (EP-0113).** At each position one of the three types is used (σ(C) = s·σ(P) + t·k, σ = A–Z or KRYPTOS). The type pattern is left completely free; the key is periodic with period p = 1–52, or fixed at each position by a word, a linear rule, Gronsfeld digits, or a running key from listed texts.
- **Slidefair, Portax, Doppelkasten (EP-0116).** Digraph ciphers, rules from the ACA descriptions, checked on their worked examples first. Doppelkasten with two completely free squares and W as separator, four same-row rules and 48 pairings, solved exactly.
- **Nulls and controls.** Shuffled K4 for every check; planted English with the cribs for every family.

## Results

| Family | K4 | Random ciphertext |
|---|---|---|
| Shift by occurrence count, any σ, τ, d | Impossible: V steps to R (T at 24 → 28) and to Z (L at 66 → 70) | 80% of shuffles fail the same check |
| Any decipherable occurrence-count chart | Impossible: 9 ciphertext letters come from two plaintext letters each | — |
| Free switching, periodic key | No key at any constrained period (1–26, 30–52); fits only 27–29, where no two crib positions share a residue | Shuffles fit at p ≤ 24 in 1 of 2,000; 33% fail every constrained period |
| Switching with keys fixed at each position (16.5 million settings) | 0 (expected 0.011) | 0 of 10 |
| Short switching rules (carved row, W segment, T positions, parity, switch points) × periodic key | No period fits | — |
| Slidefair, Portax | Never encrypt a letter to itself, so S→S (32) and K→K (73) exclude them | — |
| Portax with a free substitution before | Inconsistent at P = 1–22 and 34–48; P = 23–33 unfinished | 0 of 200 per P |
| Single-pass Doppelkasten, free squares | Inconsistent in all 96 settings, including line length 21 | 10 of 1,100 consistent |
| Double-pass Doppelkasten | Not decidable: the solver recovers only 27–34% of planted English | — |

## Current finding

Five families that were open as different methods are closed by consistency with the cribs: ciphers that change row with the occurrence count, free switching between Vigenère, Beaufort and variant Beaufort with a periodic key, Slidefair, Portax, and single-pass Doppelkasten. All are logical refutations. Random ciphertext usually fails in the same way, so none of them shows K4 to be rarer than random.

## Key figure

![Bar chart over periods 1 to 52 of the share of 2,000 shuffled texts for which free type switching with a periodic key fits; bars near zero below 24, about one third at 26, 30 and 52, full at 27 to 29; under the axis K4 is marked as not fitting at every constrained period](/assets/kryptos-k4-consistency.svg)

The light bars at 27–29 are periods where no two crib positions share a residue, so any text fits. Everywhere else K4 fails, but so does most random ciphertext at small periods.

## What this research shows

- A shift that advances with the occurrence count cannot produce K4's cribs under any alphabets or step.
- Any occurrence-count chart that can be deciphered at every point would be a fixed homophonic substitution, and 9 ciphertext letters in the cribs come from two different plaintext letters.
- Switching freely between the three additive types at each position does not rescue a periodic key at any period the cribs constrain, and short rules for when to switch (including the carved rows, which would have explained the different key levels of the two cribs) do not either.
- Slidefair and Portax can never encipher a letter to itself, which K4 does twice.
- Single-pass Doppelkasten with two free squares is inconsistent with the cribs in every tested pairing.

## What this research does not show

It does not show that K4 is rarer than random under any of these families. It leaves open the double-pass Doppelkasten, Portax with a free substitution at periods 23–33 or after the cipher at periods with few crib pairs, a separate step for each letter in the occurrence-count form, and switching combined with keys that have much more freedom (general English running keys, long periods).

## What changed

Five catalogue entries moved from "untested" to "closed". The motivation for switching by carved row, the different key levels of the two cribs, is not explained by it.

## What failed

The double-pass Doppelkasten could not be decided: annealing recovered only 27–34% of planted English, so running it on K4 would not mean anything. The Portax search at P = 23 did not finish in 8.5 hours.

## Evidence boundary

Public K4 ciphertext and cribs. The occurrence-count, homophone, self-encryption and periodic-switching checks use only K4 and are rerunnable. The keyed switching search reads K1–K3 texts that this site does not publish, and the Portax and Doppelkasten solvers are not part of the public package; their outcomes are recorded.

## UNKNOWN

Whether a stronger solver would decide the double-pass Doppelkasten (two free squares are about 167 bits, less than the redundancy of 92 letters of English, so it is decidable in principle). External independent replications: zero.

## Falsification targets

A key and switching rule, a Portax key and substitution, or a pair of Doppelkasten squares that reproduce all 24 crib letters would overturn the corresponding row.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-consistency): `python verify_consistency.py` recomputes the occurrence-count conflict and its shuffle rate, the homophone collisions, the self-encryptions, and the feasible periods for free switching in both alphabets with a 2,000-shuffle null, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including the searches not rerun here, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-consistency). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

An exact solver for the double-pass Doppelkasten that treats the intermediate letters as variables.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Slidefair and Portax: American Cryptogram Association, cipher type descriptions ([ACA](https://www.cryptogram.org/resource-area/cipher-types/)).
