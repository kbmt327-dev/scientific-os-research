---
research_id: KRYPTOS-K4-EP-0186
title: Does a transposition fixed by K4's layout, followed by the procedure enumerator, fit K4?
date: '2026-10-01'
lang: en
domain: Kryptos K4
type: Negative Result
status: 0 confirmed hits in 208 settings (104 layout transpositions x 2 orders, 7.70 bit). Up to 4 crib errors in all 208, 0 hits (chance 4.5e-7); up to 7 errors, 0 hits in 160 settings and one hit in 48 that the pre-set stop rule caught and the confirmation statistic did not confirm (p = 0.81). Closed within the grammar and the transposition set only; logical refutation, not rarer than random
evidence_level: Exact enumeration with closed-form chance, construction-matched shuffles and planted controls; the transposition set, stages, stop rule and confirmation statistic were committed before any run on K4
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; 104 route transpositions fixed in advance from K4's carved shape and its length; the procedure enumerator of an earlier Note (GPU); shuffles and planted controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only the 104 listed route transpositions, in two orders, followed by a procedure of the enumerator's grammar with up to 7 crib errors; no other transposition and no form outside the grammar; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0186
source_episode_sha256: 244810b6aabaedd456b3f2e44944a682c28a21f60856d8eddcf9c633a13de94f
publication:
  status: publishable
tags:
- kryptos-k4
- transposition
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-layout-transposition/" hreflang="ja">日本語</a></p>

## Research question

K3 was a transposition on a grid. The [procedure enumerator](/en/research/kryptos-k4-procedure-enumerator/) assumed that each letter keeps its position. If K4's letters were first rearranged by a route that the sculpture's layout itself suggests, and then enciphered by one of the enumerator's procedures, would some setting fit the cribs?

## Why this matters

The enumerator's 0 hits say nothing about K4 if the text was transposed: then the crib letters sit at other positions. Allowing any transposition would make the cribs meaningless (97! orders). A small set fixed in advance from the layout keeps the test sharp.

## Method

- **The transposition set Π.** Route transpositions on grids fixed before any run on K4: write in rows and read in columns or the reverse, with four column-reading variants (8 routes per grid).
  - 24 on K4's carved shape (4 letters, then 3 rows of 31): the first 4 letters kept at the head, moved to the tail, or routed with the rest.
  - 16 at width 21 (97 = 4 × 21 + 13, the short row last or first); width 21 is where [an earlier Note](/en/research/kryptos-k4-width21/) found an excess of repeated vertical pairs.
  - 64 on rectangles of 96 cells (one letter outside, first or last) or 98 cells (one null cell at the start or end).
  - 176 items, 104 distinct after removing duplicates and the identity (6.70 bit).
- **Two orders.** A: substitute, then transpose (undo Π, crib at its plaintext positions). B: transpose, then substitute by carved position (crib moved to its carved positions). 208 settings, 7.70 bit.
- **Stages and chance.** S1: all 208 settings, up to 4 crib errors (closed-form chance 4.5 × 10⁻⁷). S2: the 48 settings of the 3 × 31 family, up to 7 errors (0.053). S3: the other 160, up to 7 errors (0.18).
- **Stop rule and confirmation.** On a hit that is not a self-reference identity, record only its metadata and stop; no candidate text is displayed or written. A hit counts as confirmed only if the English single-letter score of the 73 letters outside the cribs beats 10,000 shuffles at p ≤ 0.001/m.
- **Pre-registration.** Π, the stages, chance values, stop rule and confirmation statistic were committed before any run on K4. The order of the stages was changed before running (S1 first); the rules were not.

## Results

| Stage | Settings | Crib errors | Chance (closed form) | K4 hits (non-identity) | Confirmed |
|---|---|---|---|---|---|
| S1 | 208 | ≤ 4 | 4.5 × 10⁻⁷ | **0** | 0 |
| S2 | 48 | ≤ 7 | 0.053 | **1** | 0 (p = 0.81) |
| S3 | 160 | ≤ 7 | 0.18 | **0** | 0 |

- Self-reference identities: 0 in every stage.
- The one S2 hit was caught by the pre-set stop rule and failed the confirmation statistic (p = 0.81). After the stop, the researcher decided to record it as unconfirmed and continue. One hit is within the chance expectation (0.23 over S2 and S3; probability of at least one about 0.21).
- Planted controls: up to 4 errors, 7/9 (order A; the two misses are ciphertext autokey spreading the errors) and 9/9 (order B); up to 7 errors, 9/9 and 9/9. A wrong Π found none.
- Shuffles built the same way: 16 runs at up to 4 errors and 8 at up to 7 errors, all 0 hits.

## Current finding

No transposition in this layout-fixed set, followed by any procedure of the enumerator's grammar, fits K4 with up to 7 crib errors in a confirmed way. Shuffles also give 0 and the one unconfirmed hit is within chance, so this is a logical refutation of the family, not evidence that K4 is further from it than random.

## Key figure

![Three horizontal bars on a log scale show the closed-form chance expectation of each stage: S1, all 208 settings with up to 4 crib errors, 4.5e-7 with 0 K4 hits; S2, the 48 settings of the 3 x 31 family with up to 7 errors, 0.053 with one hit that the stop rule caught and that was not confirmed (p = 0.81); S3, the other 160 settings with up to 7 errors, 0.18 with 0 hits. Notes below give the makeup of the 104 transpositions and say shuffles gave 0 hits](/assets/kryptos-k4-layout-transposition.svg)

## What this research shows

- The 104 route transpositions fixed from K4's layout and length, in either order, do not open a fitting procedure of the enumerator with up to 4 crib errors, and give no confirmed hit with up to 7.
- The single unconfirmed hit is what chance predicts for this many settings at 7 errors.

## What this research does not show

It does not show that K4 is rarer than random. It does not cover other transpositions (other grids, other routes, keyed columnar orders, several passes), or a transposition followed by a method outside the enumerator's grammar. Those remain open.

## What changed

The enumerator's negative result now also holds after a small, fixed set of layout transpositions. A test of a prediction about the 3 × 31 family is added to the [width-21 Note](/en/research/kryptos-k4-width21/) (it did not remove any transposition from this set).

## What failed

No setting fit in a confirmed way. The stop rule fired once; the hit failed confirmation.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. The enumerator runs (GPU) and the confirmation statistic are recorded results; the public package rebuilds Π and its digest and recomputes the chance values. Nothing about the content of the unconfirmed hit is published.

## UNKNOWN

Whether some transposition outside this set, or a method outside the grammar after one of these transpositions, fits K4. External independent replications: zero.

## Falsification targets

A procedure of the enumerator that, after one of the 104 transpositions, fits all but at most 7 crib letters and passes the confirmation statistic would overturn this; so would an error in how Π is applied that keeps planted controls findable but misses real ones.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-layout-transposition): `python verify_layout_transposition.py` rebuilds Π (176 items, 104 distinct, the same sha256 as the set committed before any run on K4), the 7.70-bit capacity, the chance values of the three stages and a round-trip control for every Π, and prints `PASS`. Standard library only, under a second. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-layout-transposition). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None planned inside this grammar. A transposition family would need an outside reason to be fixed before it is tested.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
