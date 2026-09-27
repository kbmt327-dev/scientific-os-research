---
research_id: KRYPTOS-K4-EP-0093
title: Can a key source be tested without knowing the chart it drives?
date: '2026-09-26'
lang: en
domain: Kryptos K4
type: Negative Result
status: No key source named by the hints is supported; with a Latin-square chart the hint keywords, digit strings, the tableau at K4's place, column numbers and most periods are logically excluded; the width-21 repeats remain unexplained
evidence_level: Chart-free consistency tests with decoy-source nulls and synthetic positive controls on public ciphertext and cribs; source families committed before running
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; hint keywords and digit strings; decoy sources; permutations of K4
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Key sources (which object, which position) tested against the cribs under chart types defined only by their structure; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0093
source_episode_sha256: 986147b6b6876e39a500aa1e9fd3ca469d39096ac12c8fbf9bdcd80a727dc897
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-key-sources/" hreflang="ja">日本語</a></p>

## Research question

If K4's chart was made by hand, its contents cannot be searched. But the key that picks a row at each position has to come from somewhere: a keyword, a date, a text, the sculpture's layout. Can such a source be tested against the cribs without knowing what is in the chart?

## Why this matters

A [separate Note](/en/research/kryptos-k4-key-bound/) shows that a solvable K4 needs a key with a short description. The hints name several candidate sources. Testing them one chart at a time would be endless; testing them against every chart of a given structure at once is possible.

## Method

- **Chart-free test.** A source gives each position a symbol X. Under a Latin-square chart (each row a permutation, and different rows send the same plaintext letter to different ciphertext letters), the crib requires: same X and same plaintext → same ciphertext; same X and different plaintext → different ciphertext; same plaintext and same ciphertext → same X; same ciphertext and different plaintext → different X. A source that breaks any rule is impossible for every such chart. Under arbitrary rows only the first two rules apply.
- **Power (EP-0092).** Wrong sources pass 26–42% of the time with arbitrary rows but only 1.7–1.9% with a Latin chart, so the test has power only with that structure. With English keyed by another English text, the true source passes every time and ranks first 47% of the time.
- **Sources (EP-0093, committed before running; 3,420 sources).** K1–K3 plaintext positions, carved panel positions, the tableau at K4's place, carved column numbers, periods 2–48, hint keywords at every phase (390), dates and coordinates as digit strings at every phase (78). Later: clock hands, carved geometry, positions of T, short texts (EP-0100, EP-0124).
- **Null.** Decoy sources of the same shape: random words of the same lengths, random digit strings, English text positions. Shuffling K4 itself was dropped after the first run, because it destroys the crib's own repeat (R→P at 27 and 65) and so inflates pass rates.
- **The width-21 phenomenon (Bean 2021).** Writing K4 in rows of width w and counting vertical letter pairs that occur at least twice; width 21 gives 11. Priced over the widths 2–48 scanned, against permutations of K4.

## Results

| Source (Latin chart, no crib error) | K4 passes | Decoys |
|---|---|---|
| Hint keywords, every phase | **0 / 390** | median 1; 18% of decoy lists also 0 |
| Dates and coordinates as digits | **0 / 78** | median 0; 53% of decoy lists also 0 |
| Periods 2–48 | only 19 and 38 | 38 = 65 − 27, the crib's own repeat |
| Tableau at K4's place; carved column numbers | 0 / 21; 0 / 2 | — |
| K1–K3 plaintext positions | 25 / 1,344 | median 25; best z P = 0.53 |
| Carved panel positions | 25 / 1,538 | median 29; best z P = 0.58 |
| Clock hands (EP-0100) | 1,352 / 144,527 = 0.009 | shape null 0.014 |
| Carved geometry (EP-0100) | 6 / 390 = 0.015 | shape null 0.012 |
| Positions of T, short texts (EP-0124) | 2/308, 0/266, 44/3,423 | shape null 0.012–0.018 |

| Width-21 vertical repeats | Value |
|---|---|
| K4's count at width 21 | 11 (the most of any width) |
| Permutations reaching 11 at width 21 | 1 of 20,000 |
| After paying for widths 2–48 | P ≈ 0.001 (internal run 0.003) |
| Keys from texts that reach 11 | 0 of 600 |
| A period-21 key | breaks 3 crib pairs |

## Current finding

None of the key sources the hints point to is supported. Under a Latin-square chart without crib errors the hint keywords, the date and coordinate digit strings, the tableau at K4's place, the carved column numbers and every period except 19 and 38 are logically excluded; those two pass only because of the crib's own R→P repeat 38 letters apart. Text positions and the other sources pass at the rate of decoys. The one strong regularity, vertical repeats at width 21, is not produced by any of these sources and remains unexplained.

## Key figure

![Bar chart of repeated vertical letter pairs when K4 is written in rows of width 2 to 48; the bar at width 21 reaches 11, well above the others](/assets/kryptos-k4-key-sources.svg)

## What this research shows

- A key source can be tested against every Latin-square chart at once; the named hint sources fail that test.
- The exclusions are logical but weak as evidence: many decoy lists also pass nothing, so K4's zero is not unusual.
- The width-21 regularity is real after paying for the scan, and neither text keys nor a period-21 key make it.

## What this research does not show

With arbitrary chart rows the test has little power, so sources are not excluded for hand-made charts without structure. Text-position sources are not excluded (the true source ranks first only 47% of the time). Nothing here explains the width-21 repeats.

## What changed

The key-source-first plan was run. Its answer for the named sources is negative, and it left one phenomenon (width 21) that no tested source accounts for. A later closeness pattern (cipher letters for the same plaintext letter lie near each other in A–Z order, P ≈ 0.01–0.02 after the choices) points toward shift-like rows and is recorded as data, not a lead.

## What failed

The planned null (shuffling K4) had to be replaced after the first run, because it broke the crib's own repeat; the direction of the result did not change.

## Evidence boundary

Public K4 ciphertext and cribs, the hint keywords and digit strings. Text-position sources read the K1–K3 texts and carved panel, and the tableau and column sources read the carved layout; this site does not publish those, so those rows are recorded, not rerun.

## UNKNOWN

What produces the width-21 repeats. Whether K4's chart has any structure. External independent replications: zero.

## Falsification targets

A named source that passes the Latin test and then reads English outside the cribs would overturn the negative. A mechanism that yields 11 or more vertical repeats at width 21 in a large share of simulations would explain the phenomenon.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-key-sources): `python verify_key_sources.py` reruns the Latin-chart test on the keywords, digit strings and periods with decoy nulls, and the width scan over 20,000 permutations, and prints `PASS`. Standard library only, about 20 seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including sources not rerun here, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-key-sources). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Search simulated mechanisms for ones that reproduce K4's fingerprint (flat letter counts, the width-21 repeats, the crib pattern) together, before searching keys.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Width-21 repeats and crib distances: Richard Bean, ["Cryptodiagnosis of Kryptos K4"](https://ecp.ep.liu.se/index.php/histocrypt/article/view/153), HistoCrypt 2021.
