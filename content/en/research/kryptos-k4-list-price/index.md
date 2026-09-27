---
research_id: KRYPTOS-K4-EP-0135
title: What is the TOKIO reading worth once the choice of target list is paid?
date: '2026-09-27'
lang: en
domain: Kryptos K4
type: Finding
status: Compatible with chance once six frozen target lists and other markers are paid (E = 0.054, p = 0.19); Ws as inserted or overwritten markers gave no candidate
evidence_level: Closed-form nulls on public ciphertext; lists, markers and decision rules committed before any run
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext, six target lists and a marker list frozen before any gap was read; closed-form nulls, shuffled-text controls and planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: The value of the W-gap reading of K4 against target lists conceivable before looking, and three cipher families built on the Ws being markers; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0135
source_episode_sha256: fb0f7a7b52033d795d3e06e98d302250e09179811e7edd71d682f3b396c0d3e6
publication:
  status: publishable
tags:
- kryptos-k4
- multiplicity
- exact-null
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-list-price/" hreflang="ja">日本語</a></p>

## Current finding

The gaps between K4's five Ws read `TOKIO`, a place on Berlin's World Clock. [An earlier Note](/en/research/kryptos-k4-tokio-price/) priced that reading at p ≤ 1.48 × 10⁻³ against the clock's place list, but did not pay for choosing that list. Here six target lists that were conceivable before looking at K4 were frozen first. Against their union (3,036 words) the same reading family is expected to hit **0.054** words by chance, and the World Clock contributes only 3.7% of that. Counting the gaps between every other marker in K1–K4 as well, the one hit (`TOKIO`) stands against **0.211** expected (p = 0.19). The reading is compatible with chance. Treating the Ws as marks added after encryption, inserted or overwriting a letter, gave no candidate in three different-method families.

## Key figure

![Horizontal bars of expected chance hits: World Clock 0.0020, English words 0.0176, K1–K3 words 0.0205, compass points 0.0111, theme words 0.0032, capitals 0.0008, union of the six lists 0.0539](/assets/kryptos-k4-list-price.svg)

Each bar is the expected number of list words that K4's reading family would produce if the letters sat at random positions. The cost of the reading sits mostly in short words (`ENE`, `ESE`, `THE`, `CIA`), not in place names.

## What this research shows

- Paying for "which object's list" makes the observation about 27 times less surprising than the World Clock price alone (0.054 against 0.0020).
- Over every marker checked in K1–K4 (each letter, the carved question marks, section boundaries, row heads, the X separators of K2, three misspellings, the extra L of the tableau), the cipher side has one hit against 0.211 expected. Without K4's letters, 0 against 0.156.
- If the Ws were inserted after encryption, the other 92 letters should form a working ciphertext. The procedure enumerator's six different-method shapes gave 0 fits on those 92 letters (shuffles 0, planted controls 6/6).
- If the Ws overwrote ciphertext letters, only families that read earlier ciphertext are affected. Ciphertext autokey, Chaocipher (536,138,304 settings) and a cursor walking the carved surface (5,832 settings) gave 0 with the five letters left unknown; controls were all found.

## What this research does not show

It does not show that the Ws were placed by chance, or that they were not. The lists were chosen after `TOKIO` was known; that is why their multiplicity is paid, but no finite set of lists covers every target a reader might have found meaningful. The zero counts for the marker families are logical refutations of the families as specified; random ciphertext also gives zero, so K4 is not shown to be rarer than random.

## Research question

Once the choice of target list and of marker is paid, is the `TOKIO` reading of the W gaps still more than chance? And if the Ws are an author's mark rather than part of the cipher, does any cipher appear under that assumption?

## Why this matters

The TOKIO reading was the one pattern in this program that had passed a frozen external list. A pattern that looks too explicit can be a clue or an artefact of looking; the two predict different things. The price was paid before anything else was built on it.

## Method

- **Three explanations, fixed in advance.** (i) Chance: the reading and the target were chosen after looking. (ii) An author's mark: the Ws were inserted after encryption, or overwrote ciphertext letters. (iii) A by-product of the method (such as separators). (iii) was already constrained elsewhere and was not rerun.
- **Frozen inputs.** Six lists, letters only, three letters or longer: World Clock places (146), common English words (2,541), words of the K1–K3 plaintexts (107), compass points (24), national capitals (207), Kryptos-related and 2025 theme words (135, with `TOKIO` removed because that list was written after the observation). The marker list covered the texts and features above. Both were committed before any gap was read.
- **Reading family.** As in EP-0011: gap definition (between / difference), four anchors, two directions, A = 1 or A = 0, generalised to a text of length n.
- **Closed-form null.** For letters or markers at uniform positions, the expected number of list words is a finite sum over words and marker counts (a union bound over conventions). For plaintext letters, whose positions are not uniform, the null was 200 windows of English of the same length.
- **Ws as marks.** (ii-a) The procedure enumerator was run unchanged on K4 with the Ws removed (cribs shift to 20–32 and 59–69). (ii-b) Families that read earlier ciphertext were judged with the five W letters unknown.
- **Pre-registered threshold** for any single hit: p < 0.01.

## Results

| List | Words | E[hits] |
|---|---|---|
| World Clock places | 146 | 0.0020 |
| English words | 2,541 | 0.0176 |
| K1–K3 plaintext words | 107 | 0.0205 |
| Compass points | 24 | 0.0111 |
| National capitals | 207 | 0.0008 |
| Theme words | 135 | 0.0032 |
| **Union** | 3,036 | **0.054** |

| Side | Hits | Expected | P(≥ hits) |
|---|---|---|---|
| Ciphertext and non-letter markers, all | 1 (`TOKIO`) | 0.211 | 0.19 |
| Same, without K4's letters | 0 | 0.156 | — |
| Plaintext letters (English-window null) | 1 | 0.045 | 0.044 (above 0.01) |

| Ws as marks | K4 | Shuffles | Controls |
|---|---|---|---|
| Inserted: enumerator on the 92 other letters | 0 | 0, 0 | 6/6 |
| Overwritten: ciphertext autokey | 0 | 0, 0 | 6/6 |
| Overwritten: Chaocipher (536,138,304 settings) | 0 | 0, 0 | 2/2 |
| Overwritten: walking cursor (5,832 settings) | 0 | 0, 0 | 2/2 |

## What changed

The `TOKIO` reading moves from "the one pattern that passed a frozen external list" to "compatible with chance once the list is paid". The earlier Note's arithmetic stands; what it did not count was the choice among lists.

## What failed

Nothing in the author's-mark branch produced a candidate. The plaintext-side hit (1 against 0.045) was below the pre-registered bar and is not reported as a finding.

## Evidence boundary

Public K4 ciphertext and published or author-typed word lists. The K1–K3 texts were used for the K1–K3 word list and the other markers; this site does not publish those texts, so that part is not rerunnable from the public package. The Chaocipher and enumerator runs were not rerun for this Note; their recorded counts are listed.

## UNKNOWN

Whether the Ws were placed on purpose. Whether a target list no one would have written down in advance explains the reading. The 1985–1997 edition of the World Clock list. External independent replications: zero.

## Falsification targets

A target list that is short, fixed by an outside source before K4 was examined, and still hit, would restore the reading's value. A cipher that works on the 92 non-W letters, or with the five W letters unknown, would support the author's-mark explanation.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-list-price): `python verify_list_price.py` checks the closed-form count against brute force, recomputes the expected hits for the five public lists, brackets the recorded union (0.0343 from public lists alone; with the withheld list the recorded 0.0539 must lie between 0.0343 and 0.0547), and confirms that the only list word K4 yields is `TOKIO` from W. It runs in a few seconds with the standard library and prints `PASS`. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Reading family, closed-form null, five public lists, recorded results and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-list-price). Code and results are MIT-licensed; the ciphertext is quoted and the lists are factual data.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None is planned for this reading. It is recorded as compatible with chance.

## Sources

- K4 ciphertext: Jim Sanborn, *Kryptos* (1990); public transcriptions on [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) and by [Elonka Dunin](https://elonka.com/kryptos/).
- The W-gap reading `20, 15, 11, 9, 15 → TOKIO`: [matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0).
- World Clock places: [Erich John's official site](https://web.archive.org/web/20200812142431/https://weltzeituhr-berlin.de/en/places-worldtimeclock) (Internet Archive).
- 2025 clue themes: [Scientific American, 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/).
