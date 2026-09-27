---
research_id: KRYPTOS-K4-EP-0066
title: Can the sculpture's physical form be K4's key?
date: '2026-09-25'
lang: en
domain: Kryptos K4
type: Negative Result
status: Keys that depend only on horizontal position, or on horizontal plus vertical position, are impossible without measuring the shape; K4's crib keys are as rough as random keys, unlike keys read off a smooth physical map; every 3D-model reading tested gives no candidate
evidence_level: A shape-free exact argument and a roughness statistic on public ciphertext and cribs, plus searches over a 3D model built from photographs; statistics fixed before running
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext, the 24 public crib letters, K4's row and column on the panel from photographs, and a 3D model of the sculpture estimated from public photographs and aerial imagery
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Keys derived from the sculpture's physical layout, light, shadow and viewpoint, with the chart one shift (pi = id) in six conventions; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0066
source_episode_sha256: 2cbc0c7b6e99a063f64d791681977e3f0d3c0a2dab2610de7354116cd039606e
publication:
  status: publishable
tags:
- kryptos-k4
- physical
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-physical-keys/" hreflang="ja">日本語</a></p>

## Research question

Perhaps the key is not a word at all but the sculpture itself: the direction each letter faces, the distance along the curved screen, when a shadow crosses it, what shows through the cut-out letters. Can such physical keys produce K4's cribs?

## Why this matters

Physical keys are hard to enumerate, because every one needs measurements the public does not have. Two tests avoid measuring the shape at all; the rest were run over a 3D model across its whole plausible range, so that no single guessed dimension drives the result.

## Method

- **Layout (photographs).** K4 sits at the end of the cipher panel: row 24 columns 27–30, then rows 25–27 with 31 letters each, right-aligned at the seam. So crib positions 32 and 63 share column 28, and 33 and 64 share column 29.
- **Shape-free test (EP-0066).** A key that depends only on horizontal position (surface direction, distance along the arc, anything that does not change with height) needs k(32) = k(63) and k(33) = k(64). A key that is a horizontal part plus a vertical part needs k(32) − k(63) = k(33) − k(64). Checked in six conventions (Vigenère, Beaufort, variant; A–Z or KRYPTOS).
- **Smoothness (EP-0068).** Keys read off a smooth map (the time a shadow edge crosses a letter, the tableau cell seen behind it from a standing point) change slowly from letter to letter. S is the largest second difference along the carved crib rows or the 2×2 cross difference, in units of the key's step, minimised over 12 step sizes, 6 conventions and 2 numberings; random keys get the same freedom. Calibrated on keys generated from the 3D model before K4 was scored.
- **3D model searches (EP-0059–0069).** A model estimated from public photographs and aerial imagery, run over its uncertainty range (radius 1.4–2.4 m and more; 27–81 shape variants): the letter behind each hole, sunlight through the holes, shadow timing, distance from a fixed point, the screen wrapped around the petrified-wood trunk, wave bands, Morse, Berlin clock, seam folds, reading from the back.

## Results

| Convention | k(32), k(63), k(33), k(64) | Horizontal only | Horizontal + vertical |
|---|---|---|---|
| Vigenère A–Z | 0, 12, 25, 20 | fails | fails |
| Beaufort A–Z | 10, 14, 11, 2 | fails | fails |
| Variant A–Z | 0, 14, 1, 6 | fails | fails |
| Vigenère KRYPTOS | 0, 11, 2, 17 | fails | fails |
| Beaufort KRYPTOS | 12, 1, 10, 13 | fails | fails |
| Variant KRYPTOS | 0, 15, 24, 9 | fails | fails |

| Roughness S | Value |
|---|---|
| K4 | 10 |
| 2,000 random crib keys | median 10; P(S ≤ 9) = 0.145 |
| Sight-line keys from the model (828 standing points) | S ≥ 10 in 0 |
| Shadow-edge clocks, gain ≤ 13 steps per letter | S ≥ 10 in at most 2.3% |

| 3D-model reading | Result |
|---|---|
| Sunlight through the cut-out letters | no moment in the year lights all 24 crib letters together (at most 14 and 16) |
| Letter behind each hole, shadow timing, distance from a fixed point (whole shape range) | no setting fits; best scores equal shuffles |
| Screen wrapped around the trunk (19–25 columns per turn) | no candidate |
| Wave bands, sine intensity, fractionated Morse, Berlin clock odometer, seam folds, reading from the back | no candidate |

## Current finding

K4's key does not come from the sculpture's shape in any of the ways tested. Keys that depend only on horizontal position, or on a horizontal plus a vertical part, are ruled out without measuring anything: two pairs of crib letters share a column but need different keys in every convention. Keys read off a smooth physical map would change slowly along the carved rows, and K4's crib keys are exactly as rough as random ones. Every reading of the 3D model tried, over the whole plausible shape, gives no candidate.

## Key figure

![Histogram of the roughness S of 2,000 random crib keys, peaking around 10, with K4's value 10 marked in red; a bar above marks that keys from the 3D model mostly have S of 4 or less](/assets/kryptos-k4-physical-keys.svg)

## What this research shows

- No key that is a function of horizontal position, or of horizontal plus vertical position, can produce the cribs; no dimension of the sculpture enters this argument.
- K4's crib keys are not smooth along the carved rows, which is what shadow, sunlight and sight-line keys would produce.
- The 3D model readings give nothing across the shape's uncertainty range.

## What this research does not show

The shape-free exclusion is logical but weak as evidence: a random key would pass "horizontal only" with probability 1/676 and "horizontal + vertical" with 1/26 per convention, so the family is small. Fast clocks (26 or more steps per letter) and smooth quantities looked up through a non-linear table are not decidable with a model of centimetre accuracy. All tests assume the chart is one shift of a standard or KRYPTOS alphabet.

## What changed

Physical keys moved from "untested because they need measurements" to "closed where decidable", and the model's uncertainty is carried through by running every reading over the shape range.

## What failed

The model is estimated from photographs (most dimensions grade C), so readings that need millimetre precision, such as a fast shadow clock, could not be tested.

## Evidence boundary

Public K4 ciphertext and cribs; K4's row and column on the panel from public photographs. The shape-free test and the roughness statistic are rerun in the public package. The 3D-model searches are recorded, not rerun here; the model is published separately.

## UNKNOWN

The sculpture's exact dimensions. Whether a physical quantity enters through a non-linear table. External independent replications: zero.

## Falsification targets

A physical quantity, measured independently, whose values at the crib positions reproduce all 24 crib letters would overturn the negative for that reading.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-physical-keys): `python verify_physical_keys.py` recomputes the shared-column table in six conventions and the roughness S for K4 and 2,000 random keys, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including the 3D-model searches, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-physical-keys). MIT-licensed. [The 3D model](https://kbmt327-dev.github.io/scientific-os-research/static/kryptos-k4-model.html).

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Only with better measurements (millimetre survey, or an outside record of the time unit) could fast clocks be tested.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Panel layout: public photographs of the sculpture, including those collected by [Elonka Dunin](https://elonka.com/kryptos/).
