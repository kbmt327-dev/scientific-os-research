---
research_id: KRYPTOS-K4-EP-0121
title: Can a rotor machine with a free wiring produce K4's cribs?
date: '2026-09-27'
lang: en
domain: Kryptos K4
type: Negative Result
status: One free rotor (any step, with keyed entry and exit alphabets or position keys), two moving rotors with a free slow rotor, and reflector machines behind a free substitution give 0 settings; logical refutations, not rarer than random
evidence_level: Exact existence tests for the free wiring over enumerated settings, on public ciphertext and cribs; scripts committed before running
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; exact wiring tests, planted positive controls, shuffled-ciphertext nulls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: The rotor families as specified (one free wiring, or moving rotors from 274 keyword alphabets with one free rotor, or public Enigma-type wirings behind a free substitution); no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0121
source_episode_sha256: ef45787aa9e0ecbea92f3db22340029ba4856590f7b2aad108d2cedcf3d3934c
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-rotors/" hreflang="ja">日本語</a></p>

## Research question

A rotor changes the substitution at every letter without being a shifted chart, so it is a genuine different method. If one rotor's wiring is left completely free, can any rotor machine of the kinds listed below produce the 24 crib letters?

## Why this matters

A free wiring has about 88 bits of freedom, far more than any search could enumerate. It can still be tested exactly: the cribs give 24 equations for the wiring, and a wiring exists only if they do not contradict each other. That turns a hopeless search into a yes-or-no check per setting.

## Method

- **One free rotor (EP-0083).** At position i the rotor is shifted by s + d·i, in A–Z or KRYPTOS contact numbering, d = 0–25. Each crib letter gives R(u) = v; a wiring exists exactly when equal u always go with equal v and different u with different v.
- **Extensions (EP-0121).** One free rotor behind keyed entry and exit alphabets (274 alphabets from Kryptos, clue and 2025 theme words; 1,951,976 settings). One free rotor stepped by keys that depend only on position: periodic keywords, quadratics, carry-over from a faster rotor, W segments, carved rows, Berlin clock lamp counts (90,246,284 settings). An odometer: two moving rotors from the 274 alphabets and a free slow rotor anywhere in the path, which covers every two- and three-rotor machine whose moving wirings are in the list (7.9 × 10¹⁰ settings, on a GPU).
- **Reflector machines (EP-0132).** A reflector machine alone never enciphers a letter to itself, which K4 does at 32 and 73. With a free substitution in front, that argument no longer applies, so commercial Enigma D and K, Swiss-K and Railway wirings (no plugboard) were tested behind a free substitution: 1.11 × 10¹⁰ settings, the simulator checked against published Enigma test vectors.
- **Controls.** Planted machines for every family; shuffled K4 as nulls. Scripts committed before running on K4.

## Results

| Family | Settings | K4 | Shuffles | Controls |
|---|---|---|---|---|
| One free rotor, step d, A–Z or KRYPTOS | 52 | **0** | 0 of 2,000 | 200/200 |
| Chart of powers of one permutation, exponent a·i + b | 676 | **0** | 0 of 2,000 | 200/200 |
| Free rotor with keyed entry and exit alphabets | 1,951,976 | **0** | 0 of 10 | 30/30 |
| Free rotor stepped by position keys | 90,246,284 | **0** | 0 of 10 | 30/30 |
| Two moving rotors + free slow rotor | 7.9 × 10¹⁰ | **0** | 1 of 10 | 30/30 |
| Reflector machine behind a free substitution | 1.11 × 10¹⁰ | **0** | 0 of 50 | 30/30 |

The fewest crib errors that would let a wiring exist: 4 for keyed entry and exit alphabets (shuffles 3–4), 3 for position keys (shuffles 3–5).

## Current finding

No rotor family tested can produce K4's cribs: a single free rotor under any step, keyed alphabets or position-only stepping, two or three rotors whose moving wirings come from 274 keyword alphabets with the slow rotor free, and reflector machines with public wirings behind a free substitution. Each is a logical refutation. Random ciphertext also fails (the odometer passed once in ten shuffles, since that family nears the crib's capacity), so K4 is not shown to be rarer than random.

## Key figure

![Horizontal bars of log2 settings searched for five rotor families, from 5.7 bits for one free rotor to 36.2 bits for the odometer, each marked 0 fit, with a red line at 112.8 bits for what the cribs pin down](/assets/kryptos-k4-rotors.svg)

The free wiring or free substitution in each family is solved, not searched, so each bar understates the family's freedom by about 88 bits.

## What this research shows

- A single rotor with any wiring cannot produce the cribs for any constant step, and neither can it with keyed entry and exit alphabets or with stepping driven by position.
- Two- and three-rotor machines are closed as long as the moving rotors are wired from the listed alphabets; the slow rotor can be anything.
- Putting a free substitution in front of a commercial Enigma-type reflector machine does not rescue it.
- The number of crib errors a single rotor would need is within the range of random ciphertext, so "a few carving errors" does not favour this family.

## What this research does not show

It does not show that K4 is rarer than random. Machines with two or more free wirings, moving wirings outside the 274 alphabets, plugboards on the reflector machines, or stepping that depends on the plaintext are outside what was tested; with two free wirings the family is larger than the cribs can decide.

## What changed

The rotor entries in the catalogue changed from "two or more rotors: not decidable" to "closed when the moving rotors are from the list, whatever the slow rotor". The one decidable different method found in the catalogue audit, a reflector machine behind a free substitution, is closed.

## What failed

The odometer family is close to the crib's capacity (36 bits of settings plus a free rotor): one shuffle in ten passed by chance. A pass on K4 would therefore have been hard to tell from chance.

## Evidence boundary

Public K4 ciphertext and cribs. The single-rotor test uses only K4 and is rerun in the public package. The larger searches use keyword alphabets and GPU batch code that are not published; their outcomes are recorded.

## UNKNOWN

Whether any machine of the 1980s with a free or unlisted wiring was used. External independent replications: zero.

## Falsification targets

A setting in any listed family for which a wiring (or substitution) consistent with all 24 crib letters exists would overturn the corresponding row.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-rotors): `python verify_rotor.py` reruns the free-wiring single-rotor test on K4 for every step and both numberings, finds 200 planted rotors and checks 2,000 shuffles, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including the GPU searches, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-rotors). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None within these families. Machines with two free wirings cannot be decided from the cribs.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Enigma wirings: [Crypto Museum, Enigma wiring](https://www.cryptomuseum.com/crypto/enigma/wiring.htm).
