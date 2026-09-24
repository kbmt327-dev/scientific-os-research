---
research_id: KRYPTOS-K4-EP-0001
title: Does primer 57973 stand out once the model's freedom is counted?
date: '2026-09-19'
lang: en
domain: Kryptos K4
type: Finding
status: Claimed numbers reproduced; the cribs do not single out 57973
evidence_level: Exact reproduction plus three controls on public ciphertext
peer_reviewed: false
independent_replications: 0
evidence:
  class: audit
  source: Public K4 ciphertext, the 24 public crib letters, and the numeric claims of a research handoff
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Whether the public cribs discriminate the reverse-Gromark-57973 hypothesis;
  not whether K4 is a Gromark-type cipher
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0001
source_episode_sha256: ba7dc182c8f4c5aadbb63686e21a4ebcf6e06ba349566086a8bea66e598dad13
publication:
  status: publishable
tags:
- kryptos-k4
- audit
- capacity
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-57973-audit/" hreflang="ja">日本語</a></p>

## Current finding

A research handoff argued that K4 is a Gromark cipher with primer 57973, keystream reversed, and two arbitrary 26-letter alphabets. Every number it cited reproduces exactly: 23 of 100,000 reversed primers fit the cribs, 57973 is among them, and it forces 13 plaintext letters. But the numbers do not single out 57973. Random digit masks fit the cribs just as often as Gromark, the 13 letters exist only for one route with no shift, and every randomly drawn primer fits once routes are allowed. The public cribs cannot tell this hypothesis apart from chance. This does not show that K4 is not a Gromark-type cipher.

## Key figure

![Crib-compatible rates: random masks 4.07e-4, forward Gromark 3.90e-4, reversed Gromark 2.30e-4; below, the letters forced by 57973 under the identity route (13) and under column route 28 with shift 50 (21)](/assets/kryptos-k4-57973-audit.svg)

Top: how often a keystream fits the 24 crib letters when both alphabets are free. Bottom: the forced letters change completely with the route.

## What this research shows

- The handoff's numbers are correct, including one definition it never states: "reversed" means generating 97 digits forward and then reversing the sequence. Only that reading matches all 13 mask digits the handoff lists; other readings match at most 3.
- Uniform random masks fit the cribs at 4.07 × 10⁻⁴ (813 of 2,000,000), against 3.90 × 10⁻⁴ for forward Gromark and 2.30 × 10⁻⁴ for reversed. The count of 23 measures how much two arbitrary alphabets can absorb, not a property of Gromark.
- The 13 forced letters require the identity route and no shift. Over 55,096 route, shift and direction choices, 482 fit and up to 21 letters are forced, a different set each time. The handoff also argued that a route is required, which removes the 13.
- All 40 randomly drawn primers admit a fitting route. On both counts 57973 sits below the median.

## What this research does not show

That K4 is not a Gromark or Gromark-like cipher; that 57973 is wrong; that any other primer is right. It rejects only the claim that the public cribs discriminate this hypothesis.

## Research question

Do the numbers offered for reverse-Gromark-57973 reproduce from public data alone, and do they discriminate the hypothesis from chance?

## Why this matters

A model with two free 26-letter alphabets has far more freedom than 24 known letters can pin down: roughly 113 bits of constraint against more than 210 bits of freedom. In that regime almost any keystream "fits", and a count of fitting primers says more about the model than about K4. The controls here are the checks that make that visible.

## Method

- Reimplemented from the public ciphertext and cribs only. Keystream d_i = (d_{i−5} + d_{i−4}) mod 10 from a 5-digit primer; relation CA(C_i) − PA(P_i) = d_i (mod 26) with both alphabets free. Compatibility is decided exactly with a union-find over 52 letters carrying mod-26 offsets.
- All 100,000 primers in both directions; forced letters for every compatible primer; the number of alphabet configurations for 57973.
- Control 1: 2,000,000 uniform random 97-digit masks through the same test.
- Control 2: 284 paper-executable routes × 97 cyclic shifts × 2 directions for 57973.
- Control 3: 40 random primers, each tried against the same route family.

## Results

| Claim | Handoff | Reproduced |
|---|---|---|
| Compatible primers, forward / reversed | 39 / 23 | 39 / 23 (same primers) |
| 57973 forward / reversed | incompatible / compatible | incompatible / compatible |
| Alphabet configurations for 57973 | 29,120 | 29,120 (5 components) |
| Most forced letters | 13, at 3 primers | 13, at 57928, 57973, 59346 |

| Control | Result |
|---|---|
| Random masks | 4.07 × 10⁻⁴, as high as Gromark |
| Routes for 57973 | 482 of 55,096 fit; up to 21 forced letters |
| Random primers | 40 of 40 admit a fitting route |

## What changed

The reverse-Gromark-57973 line was reclassified from "leading hypothesis" to "not discriminated by the public cribs". In the internal record, restricting the alphabets to keyword-derived ones did not help either: the shortest keyword that fits is 16 letters for the real configurations and also 16 for random ones, so the restriction kills real and random alike.

## What failed

A first attempt to restrict the alphabets used 1,300 keyword alphabets and found no survivor, which was briefly read as closing the line. It had no power: chance expected 0.053 survivors, so zero was the typical outcome. It was withdrawn and replaced by a structural test with a matched null.

## Evidence boundary

Public ciphertext, 24 crib letters and the handoff's numeric claims. The route family is a finite list of paper-executable routes chosen by the author, not every route. The controls are the author's own, not independent.

## UNKNOWN

Whether K4 uses a Gromark-type keystream at all. How the handoff's source derived 57973 from `TOKIO` (examined in a later internal episode, not published here). External independent replications: zero.

## Falsification targets

A rule fixed before seeing K4 that derives 57973 and a route, and then predicts unseen plaintext letters correctly, would restore the hypothesis. A sealed prediction from the rejected identity-route model (PRED-001, SHA-256 `daea50e3e4de55539d9e96c89577d2c7c45658776eaef9ebe2f7571bfb743c12`, sealed 2026-09-19) remains unscored until the plaintext is published.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-57973-audit): `python verify_57973_audit.py` reruns the primer scan, forced letters, configuration count and route sweep with the standard library in under a minute and prints `PASS` when they match the recorded result. `--full` also reruns the two random controls. It is a rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Audit script and recorded output](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-57973-audit). Code and results are MIT-licensed; the ciphertext and cribs are quoted, not licensed.

## External audit

External independent replications: zero. No cryptographer has reviewed this note.

## Next experiment

Any Gromark-type claim should first say which fixed rule, chosen before looking, gives the primer and the route, and which unseen letters it predicts.

## Sources

- K4 ciphertext: Jim Sanborn, *Kryptos* (1990). Public transcriptions: [Wikipedia, "Kryptos"](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin's Kryptos page](https://elonka.com/kryptos/).
- Cribs: [WIRED, 21 Nov 2010](https://www.wired.com/2010/11/clue-kryptos/); [WIRED, 20 Nov 2014](https://www.wired.com/2014/11/second-kryptos-clue/); NPR *All Things Considered*, 30 Jan 2020 ([transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)); `EAST` as recorded in [Elonka Dunin's archive](https://elonka.com/kryptos/).
- The hypothesis audited: a research handoff given to this project on 2026-09-18, which builds on [matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0). Only its numeric claims are restated.
