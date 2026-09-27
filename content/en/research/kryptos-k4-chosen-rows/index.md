---
research_id: KRYPTOS-K4-EP-0114
title: Can K4 come from a list of keyed rows chosen letter by letter?
date: '2026-09-27'
lang: en
domain: Kryptos K4
type: Negative Result
status: No rule for choosing rows from any tested list of up to 64 keyed or mixed alphabets can produce the crib; sequential choosing, the M-94 cylinder and panel lines give 0
evidence_level: Selection-free cover and exhaustive sequential searches on public ciphertext and cribs; families committed before running
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; keyed alphabets from word lists; the M-94 disks; shuffled-ciphertext nulls and planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Charts whose rows are keyed or matrix-mixed alphabets from stated lists, chosen by any rule (cover) or in order (sequential), and the M-94 cylinder; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0114
source_episode_sha256: 9dfefe285696135fa41f132c422bfd723302390a1417eda94622a109baa21ec2
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-chosen-rows/" hreflang="ja">日本語</a></p>

## Research question

A hand-made chart might be a stack of keyed alphabets, one per word of some text, with the row at each position chosen by a rule. If the list of rows is known but the rule is not, can K4's crib still be tested?

## Why this matters

The rule for choosing rows is the part that is hardest to guess. A test that does not need it covers every rule at once, including ones nobody would think to enumerate.

## Method

- **Selection-free cover (EP-0114).** For a list of rows and a reading convention, count the crib positions that at least one row could explain. If fewer than 24, no rule for choosing rows from that list can produce the crib, whatever the order. Conventions: the row used as a cipher alphabet over A–Z or KRYPTOS positions, the inverse, and a cylinder read g places on (29 in all).
- **Lists.** Hint keywords (40 rows), John 8:32 (9), World Clock places (146), and internally the words of K1–K3, K0's phrases, the 2025 theme words and grids of the K3 plaintext (44 lists with up to 64 rows), each with plain keyed and three matrix-mixed alphabets.
- **Sequential choosing (EP-0098, EP-0114).** Rows taken in order of the words with steps, directions, offsets and four conventions: 386,048 settings for plain keyed rows, 190,282,456 for matrix-mixed rows.
- **The M-94 cylinder (EP-0099).** The 25 published disks in any order, any line phase, one read-off per line, by exact matching. Rows keyed by the carved panel lines.
- **Controls.** Planted charts (30/30 and 30/30); shuffled K4 as nulls (200 for cover, 20 for sequential).

## Results

| List (plain keyed rows) | Rows | Best cover of 24 | Shuffles as high |
|---|---|---|---|
| Hint keywords | 40 | 18 | 89% |
| John 8:32 | 9 | 8 | 85% |
| World Clock places | 146 | 20 | 98% |
| 44 internal lists, ≤ 64 rows each | — | none reaches 24 | — |

| Search | Settings | K4 |
|---|---|---|
| Rows keyed by successive words, in order | 386,048 | 0 (best 5–7/24, shuffle level) |
| Matrix-mixed rows, in order | 190,282,456 | 0 reach 19/24 (best 5–10) |
| M-94, any disk order | 1,065,625 × every order | 0 (controls 20/20) |
| Rows keyed by carved panel lines | 60,320 | 0 (best 6/24 = null median) |
| Text lines as chart rows | — | forward: IC ≤ K4 in 0.2%; inverse cannot encipher English |

## Current finding

Choosing chart rows from a list of keyed alphabets cannot produce K4's crib for any of the lists tested: for every list of up to 64 rows (and for the 146 World Clock places) some crib letters cannot be explained by any row, so no rule of choice helps. Choosing rows in order, the M-94 cylinder and rows from the carved panel give nothing either. These are logical refutations; shuffled texts behave the same.

## Key figure

![Horizontal bars of the best cover out of 24 for three lists (hint keywords 18, John 8:32 words 8, World Clock places 20), each short of the red line at 24, with shuffle medians marked](/assets/kryptos-k4-chosen-rows.svg)

## What this research shows

- For each tested list, some crib letters are unreachable by any row under any convention, which rules out every way of choosing rows from it.
- Even the 146 World Clock places, a list larger than the cribs can usually constrain, leave four crib letters unexplained.
- The sequential and cylinder families give nothing.

## What this research does not show

It does not show that K4 is rarer than random: shuffled texts fall short in the same way. Lists with more than about 64 rows usually cover all 24 letters and cannot be decided this way; a truly hand-made chart without a source list is outside the test.

## What changed

Word-keyed and mixed-row charts moved from "undecidable by rule" to "closed for the listed sources, whatever the rule".

## What failed

Nothing in the tested lists reached 24. Larger lists could not be decided.

## Evidence boundary

Public K4 ciphertext and cribs. The cover for the hint keywords, John 8:32 and the World Clock places is rerun in the public package. Lists built from the K1–K3 texts and the panel, and the sequential and M-94 searches, are recorded, not rerun.

## UNKNOWN

Where a hand-made chart's rows would come from. External independent replications: zero.

## Falsification targets

A list of up to 64 rows with full cover and a choice rule that reproduces the crib would overturn the result for that list.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-chosen-rows): `python verify_chosen_rows.py` recomputes the cover under 29 conventions for the three public lists with a 200-shuffle null and prints `PASS`. Standard library only, about 10 seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, World Clock data, recorded results including searches not rerun here, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-chosen-rows). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None for the listed sources. A new source list can be tested by cover before any rule is proposed.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- World Clock places: [Erich John's official site](https://web.archive.org/web/20200812142431/https://weltzeituhr-berlin.de/en/places-worldtimeclock) (Internet Archive).
- M-94 disks: [Crypto Museum, M-94](https://www.cryptomuseum.com/crypto/usa/m94/index.htm).
