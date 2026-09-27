---
research_id: KRYPTOS-K4-EP-0072
title: If a fixed substitution masks the English, which keys can still be tested?
date: '2026-09-26'
lang: en
domain: Kryptos K4
type: Negative Result
status: With a free mask on one side, text stride keys, World Clock keys, distance keys, M-94 with fixed orders, autokeys and linear keys give 0; periodic keys pass only at 19 and 38 by one crib coincidence; with masks on both sides no running key reads as English; free-order M-94, Hagelin and hand-chosen English keys are not decidable
evidence_level: Exact tests with free masks, and an English stage with measured power for double masks, on public ciphertext and cribs; planted controls and shuffle nulls
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; free substitutions solved exactly; English scoring with planted controls and shuffle nulls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: K1–K3-form ciphers with a completely free substitution before, after, or on both sides of the key, for the key families listed; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0072
source_episode_sha256: bae495dc6bc7472dc504d81bc15f1e65ca8d3f3183938ad70a66f971694f035c
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-masks/" hreflang="ja">日本語</a></p>

## Research question

Ed Scheidt, who taught Sanborn the cryptographic techniques used in Kryptos, said the English was masked. If a fixed substitution hides the English before the key is applied, after it, or on both sides, the chart no longer has to be a standard one. Which key families can still be tested, and what do they give?

## Why this matters

A free substitution is 26! (about 88 bits) of freedom. Families rejected without a mask might come back under one. Knowing which key families survive a mask, and which become untestable, is what separates "rejected" from "rejected unless masked".

## Method

- **One free mask (EP-0072–0075).** C = σ(P) + k (mask before) or C = τ(P + k) (mask after), σ and τ completely free and solved exactly. Keys: stride keys over the Kryptos texts and World Clock tapes, distance keys, the M-94 cylinder with fixed disk orders, plaintext and ciphertext autokeys, keys linear in position, periodic keys.
- **Two masks (EP-0076, 0077, 0084, 0086).** With masks on both sides the crib keeps only two equations on the key, so an English stage decides: each crib survivor is solved for its masks by annealing and scored against English, with the power measured on planted keys.
- **Capacity (EP-0074, 0085, 0088).** Families whose freedom exceeds what the crib and English can pin down are marked not decidable rather than searched.
- **Controls.** Planted masks and keys for every family; shuffled K4 as nulls.

## Results

| Family | Mask | K4 | Controls / shuffles |
|---|---|---|---|
| Keys linear in position | before or after | 0 | plants 40/40; shuffles 0 of 200 |
| Periodic keys | before or after | passes only at 19 and 38 where decidable (R→P at 27 and 65) | at other periods most shuffles pass too |
| Kryptos-text stride and World Clock keys, distance keys | before or after | 0 of 61.7 million and 0 of 0.93 million | controls recovered |
| M-94 with fixed disk orders; autokeys | before or after | 0 | — |
| M-94 with a free disk order | one mask | not decidable (about 79 bits against about 52) | — |
| Stride running keys (15.4 million) | both | 6,889 crib survivors, none reads as English (best −238.8, shuffles −243.1) | power about 0.65 |
| Carter & Mace vol. 1 running key | none or one; both | 0 with up to 2 crib errors; 291 survivors, none English | controls 60/60; power about 0.85 |
| ROLL keys and aperture windows (4,081 keys) | none or one; both | 0; no English | controls 20/20, 30/30 |
| Hagelin M-209 / CX-52 | with a mask | not decidable (freedom exceeds crib and English by tens to 200 bits) | — |
| Hand-chosen English running key | one mask | not decidable with the present search (0 of 8 plants recovered with the mask unknown) | not refuted |

## Current finding

A mask does not rescue the K1–K3 form for any short-description key tested. With one free mask, text stride keys, World Clock keys, distance keys, fixed-order M-94, autokeys and linear keys give nothing, and periodic keys pass only at 19 and 38 because of one coincidence in the crib. With masks on both sides no running-key survivor reads as English. What stays open is stated as undecidable, not rejected: M-94 with a free disk order, Hagelin machines under a mask, and a hand-chosen English key under one mask.

## Key figure

![Two panels over periods 1 to 48 for a mask before and after the key: grey bars show the share of shuffles that fit, and dots mark where K4 fits; where the test decides, K4 fits only at 19 and 38](/assets/kryptos-k4-masks.svg)

## What this research shows

- Keys linear in position fail under any mask on either side.
- Periodic keys are decidable under a mask only at some periods; there K4 fits only at 19 and 38, both explained by the crib's R→P at 27 and 65.
- The listed text, clock, distance and cylinder keys stay rejected under a mask.
- With masks on both sides, no running-key candidate reaches English, with measured power of about 0.65–0.85.

## What this research does not show

It does not reject a hand-chosen English key under a mask, M-94 with a free disk order, or Hagelin machines under a mask; those exceed what K4 can decide. The double-mask negatives have power below 1: passages resembling K2 would score below the threshold about a quarter of the time.

## What changed

Rejections of the K1–K3 form are now stated "with or without a mask" for the listed keys, and the families a mask makes undecidable are named.

## What failed

The search for a hand-chosen English key with an unknown mask recovered none of eight planted keys, so that family was closed for now as not decidable, at the owner's decision, rather than reported as rejected.

## Evidence boundary

Public K4 ciphertext and cribs. The linear-key and periodic-key tests are rerun in the public package. The text-based keys (Kryptos texts, Carter), the double-mask English stage and the capacity arguments are recorded, not rerun.

## UNKNOWN

Whether K4 uses a mask at all. Whether a stronger search would decide the hand-chosen English key. External independent replications: zero.

## Falsification targets

A listed key and a mask that reproduce all 24 crib letters and read as English would overturn the corresponding row.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-masks): `python verify_masks.py` reruns the linear-key and periodic-key tests with free masks on either side, with planted controls and a 200-shuffle power check per period, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including the searches not rerun here, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-masks). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None for the listed keys. A search that can recover planted hand-chosen English keys under an unknown mask would make that family decidable.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Scheidt on masking the English: [WIRED 2005](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/).
- Running-key text: Howard Carter and A. C. Mace, *The Tomb of Tut.ankh.Amen*, vol. 1 (1923).
