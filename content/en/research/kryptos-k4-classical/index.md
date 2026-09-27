---
research_id: KRYPTOS-K4-EP-0032
title: Which classical ciphers do K4's crib and letter counts rule out?
date: '2026-09-20'
lang: en
domain: Kryptos K4
type: Negative Result
status: Every periodic key fails at all 49 periods the crib can test, in all 8 alphabet and form settings; progressive and Gromark-type keys fail; transposition alone and 25-symbol ciphers are impossible; the other classical families give no candidate
evidence_level: Exact closures from the crib's keystream values and letter counts, with power checked on K1 and K2 first; fully rerunnable for the keystream part
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext, the 24 public crib letters and English letter frequencies; K1 and K2 as positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Periodic and difference-periodic keys in four alphabets and two forms, English-frequency running keys, transposition alone, and the classical families listed; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0032
source_episode_sha256: 4bb3749dad6b745ff5b57e50d535a78ff2111c8735d68071a3358fe613f041fe
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-classical/" hreflang="ja">日本語</a></p>

## Research question

K1–K3 were solved with a keyed Vigenère and a transposition. Before trying anything unusual, which classical ciphers of that kind can K4's 24 crib letters and its letter counts rule out, and for which periods can the crib not decide at all?

## Why this matters

Searching a family key by key only rules out what was searched. Treating the crib's keystream as data rules out whole classes at once, and makes explicit which periods are simply out of reach of 24 letters. The rest of the program builds on these exclusions.

## Method

- **Keystream values.** Fix an alphabet and a form and the 24 crib letters give 24 exact key values: Vigenère and variant both fix c − p, Beaufort fixes c + p. Four alphabets (A–Z and the keyed KRYPTOS, PALIMPSEST and ABSCISSA alphabets) × two forms = 8 settings.
- **Periodic keys.** A key with period p needs equal values at crib positions that are congruent mod p. Decided for p = 1–96 at once; a period is testable only if two crib positions share a residue.
- **Difference-periodic keys.** Progressive and Gromark-type keys make the first differences periodic; the same test on differences.
- **English running keys.** The 24 key values judged against English letter frequencies (a key taken from typical English text).
- **Transposition alone.** A rearrangement keeps K4's letter counts; 97-letter English samples compared with K4's index of coincidence.
- **Power first.** Run on K1 and K2, the test recovers their true periods (10 and 8) and alphabet; the first attempt failed because it used A–Z, which caught a bug.
- **Other families (EP-0018–0020, EP-0051–0056, EP-0059).** Searched with their own tests and controls; outcomes recorded.

## Results

| Family | Result |
|---|---|
| Any periodic key, p = 1–96 | Fails at all 49 testable periods in all 8 settings; 27–29 and 53–96 cannot be tested |
| Difference-periodic keys (progressive, Gromark type) | Fail in all 8 settings |
| Running key with English letter frequencies | K4's key values are less likely than 20,000 of 20,000 English draws in 7 settings (≤ 0.0002 in the eighth) |
| Any transposition alone | 0 of 20,000 English samples are as flat as K4 |
| Ciphers with 25 or fewer output symbols | Impossible: K4 uses all 26 letters |
| Devices with no fixed points (reflector Enigma, M-94, M-138-A, HC-9) | Impossible if positions line up: S→S at 32, K→K at 73 |
| Free alphabet per residue, p ≤ 24 | Rejected by the crib or the column letter statistics |
| Keyed columnar and K3-style rotation, each with a periodic key | No candidate |
| Hill n = 2–4 with transposition; Trifid with word cubes | No candidate |
| Two stacked keyword layers | No candidate in 1.4 × 10¹⁰ settings |
| Periodic key followed by two 7 × 7 turning grilles | No candidate in 2.09 × 10¹⁰ settings |
| Row transposition with a periodic key | Not distinguishable from shuffled controls |

## Current finding

The K1–K3 kind of cipher does not produce K4. Any periodic key fails at every period the crib can test, in every standard or Kryptos-keyed alphabet and form; keys with periodic differences fail too; a transposition alone cannot turn English into K4's flat letter counts; and the other classical families searched give no candidate. What the crib cannot decide is stated explicitly: periods 27–29 and 53 and above.

## Key figure

![Grid of periods 1 to 96: 49 testable periods in red, each failing in all 8 settings, and 47 untestable periods in grey (27 to 29 and 53 to 96)](/assets/kryptos-k4-classical.svg)

## What this research shows

- Periodic keys are closed as a class, not one period at a time, for every period the crib can reach.
- The crib cannot decide periods 27–29 or 53 and above; those are not rejected, they are out of reach.
- K4 is far too flat to be English rearranged, so some substitution must be involved.

## What this research does not show

The running-key result rejects keys that follow English letter frequencies; it does not reject every English text chosen by hand, especially with an extra substitution (a hand-chosen English key with a one-sided mask is not decidable). Periods the crib cannot test are open, not closed.

## What changed

An earlier summary had said "repeating keys are unconstrained above period 13"; the keystream view showed that most periods 30–52 are testable too, and all fail. The statement that every English running key was closed was later narrowed to keys following English letter frequencies.

## What failed

The first run could not recover K1's and K2's periods, because it used the A–Z alphabet; K1 and K2 use the KRYPTOS alphabet. Fixing it before running on K4 is why the power check comes first.

## Evidence boundary

Public K4 ciphertext and cribs and English letter frequencies. The keystream closures and the letter-count test are rerun in the public package. The other classical searches use texts and solvers not published here; their outcomes are recorded.

## UNKNOWN

Whether K4 uses a period of 53 or more, or 27–29. External independent replications: zero.

## Falsification targets

A periodic key at a testable period, in any of the eight settings, that matches all 24 crib letters would overturn the closure; so would an alphabet outside the four that is the real one (then the closure would need rerunning for it).

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-classical): `python verify_classical.py` recomputes the keystream table in all 8 settings, the periodic and difference-periodic closures for every period, the English-frequency test and the letter-count test, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including families not rerun here, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-classical). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Masks before or after encryption, and keys from the sculpture's physical form (reported in later Notes).

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- K1–K3 methods (keyed Vigenère with KRYPTOS alphabet, K3 transposition): [Wikipedia, "Kryptos"](https://en.wikipedia.org/wiki/Kryptos).
