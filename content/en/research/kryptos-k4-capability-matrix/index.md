---
research_id: KRYPTOS-K4-EP-0142
title: What have the tests covered, and where are the gaps?
date: '2026-09-28'
lang: en
domain: Kryptos K4
type: Finding
status: Coverage is concentrated on letter-unit ciphers whose state depends only on position (every synchronisation except two or more slips) and their neighbours. Eleven gap groups remain, almost all without a source that would fix an operator; the one with a source (fixed counting origins) was then tested and gave 0; a search for new evidence fixed no operator either
evidence_level: A re-reading of the records (a 92-row matrix) with no new K4 computation; the evidence search was reading only
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: The records of earlier tests (hypothesis catalogue, EP-0081, EP-0119, EP-0123, EP-0130, EP-0134 and the episodes they cite), public statements and press reports
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Bookkeeping of the abstract capabilities the recorded tests covered; no new refutation and no new candidate; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0142
source_episode_sha256: 13f2e24330fbaa62428f4f7c00eb6ccef2e9f192915f0e4365f6731f70cdbf59
publication:
  status: publishable
tags:
- kryptos-k4
- audit
- coverage
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-capability-matrix/" hreflang="ja">日本語</a></p>

## Research question

Most tests so far reduced K4 to "the key k_i at position i is a short formula G(i;θ) of the position". What procedures or states does that reduction lose? Without rerunning anything, we tabulated which abstract capabilities each test covered (unit, state, synchronisation, stages, alphabet, reordering, error spread, origin, chronology) and looked for cells that are really empty.

## Why this matters

Before searching further for an undiscovered key source, one should suspect the procedures and states that the current modelling erases. A pile of negatives says little about the outside if every one refutes something of the same shape. Knowing where the gaps are tells us what to test next, and what cannot be tested without new evidence.

## Method

- **Reduction audit (A–G).** Seven things the reduction can lose, checked against the records: A letters staying aligned by position; B three or more stages; C a single slip in the state (precedent: one ciphertext letter deleted at the end of K2); D the initial state at K4's head; E chronology of production; F procedures done by hand; G the origin of each stage (the method design by Scheidt, the actual encryption by Sanborn).
- **Matrix.** Catalogue families and episodes as rows, split where one row covered several capabilities: 92 rows. Error tolerance is written as the number of letters allowed. Hand-work weight is a prior only, never used to refute.
- **Gaps.** For each empty cell: (a) its source, (b) what would make it testable, (c) any way to close the whole family by logic without fixing an operator.
- **Rules.** No new computation on K4, and no inventing an operator to select with the cribs.
- **Two follow-ups.** The gap with a source (fixed counting origins, G11) was tested (EP-0143). New evidence that could fill gaps was searched for, reading only (EP-0144).

## Results

**Letter unit** (closed: at least one test closed or excluded it; gap: no test)

| State \ sync | Exact | Errors | One slip | Per crib | 2+ slips |
|---|---|---|---|---|---|
| none | closed | closed | closed | closed | closed |
| position | closed | closed | closed | closed | **gap** |
| plaintext history | closed | **gap** | **gap** | **gap** | **gap** |
| ciphertext history | closed | closed | closed | closed | **gap** |
| machine state | closed | partly | partly | partly | partly |

"Partly" for machine state means only devices without fixed points are closed there: each crib contains a letter enciphered to itself (positions 32 and 73), so they fail whatever the slips or switching. Digraph and block units are tested with no state and with position state, but not one test has a history or machine state. The word unit is almost entirely open.

| Gap | Content | Source |
|---|---|---|
| G1 | letter × position × two or more slips | none; mostly closed by logic (two slips land one inside each crib only about 2.6% of the time) |
| G2 | letter × plaintext history × errors, slips, per crib | none |
| G3 | letter × ciphertext history × two or more slips | none; partly inside the error allowance |
| G4 | machines with fixed points × errors, slips, per crib | none |
| G5 | digraph/block × slips, per crib | none |
| G6 | digraph/block × history or machine state | none |
| G7 | word unit with errors or slips; word × history or machine | weak (K5's "coded words"; the hints come as words) |
| G8 | a position-changing stage with history or machine state | none |
| G9 | arbitrary two-sided alphabets with history or machine state | none |
| G10 | three or more stages with a short description | weak ("LAYER TWO" in K2 and similar) |
| G11 | fixed counting origins (positions counted from the head of K3 or of the sculpture) | yes (K4 continues K3 on the same plate right after its question mark) |

Of the 92 rows, 64 are constructed operators (no source), 14 Sanborn's alterations, 8 installation, 4 Scheidt's design, 2 after decryption. By chronology, 74 use inputs that existed at encryption, 13 planned values, 9 quantities fixed only after installation (a row can carry several values).

**Afterwards.** G11 was added to the [enumerator](/en/research/kryptos-k4-procedure-enumerator/) grammar and tested: 1.06 × 10¹⁴ new procedures, 0 jointly, 0 per crib and 0 with up to seven crib errors (EP-0143). The evidence search (EP-0144) found K5's ciphertext still unpublished and only weak statements about the method since 2025 (method and key are separate; each section used a different method), none fixing an operator for any gap. It came across pages claiming a solution and images of handwritten notes about K4, and did not open them.

## Current finding

The tests so far cover letter-unit ciphers whose state depends only on position (every synchronisation except two or more slips), ciphertext history up to one slip, and families without fixed points (under any synchronisation). Of eleven gap groups only three had a source: the word unit (weak), three or more stages (weak), and fixed counting origins. The last has since given 0. For the rest, new evidence does not fix an operator, so testing them would mean inventing operators and selecting them with the cribs, which this study does not do.

## Key figure

![Grid for letter, block and word units: five states by five synchronisations; green cells were closed by a test, cells marked gap were never tested. For letters, position with two or more slips and most of plaintext history are gaps; for blocks and words, every history and machine state is a gap](/assets/kryptos-k4-capability-matrix.svg)

## What this research shows

- The negatives so far concentrate on letter-unit ciphers whose state is set by position.
- Almost every gap lacks a source that would fix an operator (UNDERDEFINED). With today's tools and no new material, only invented operators could be tested there.
- The audit also sorted out a chronology gate: quantities fixed only after installation (sun, shadow, measured dimensions) and the off-grid row breaks of rows 0–23 cannot be encryption inputs. K4's four rows coincide with the 31-column grid, so their rows and columns are planned values that could be fixed before encryption and pass the gate.
- The 3-bit-per-position [lower bound on the key](/en/research/kryptos-k4-key-bound/) was restated as a quantity inside a uniform-row model, not a general bound.

## What this research does not show

No new refutation and no candidate. The matrix is the author's reading of the records, and any row's classification can be wrong. A green cell can be closed by a single narrow family (for instance devices without fixed points). A gap does not mean the answer lies there.

## What changed

What to test next is now decided from empty cells and their sources. Gaps without a source are marked "not testable until evidence arrives" rather than filled with invented operators.

## What failed

An early assumption (row breaks follow letter widths, so operators built from the carved layout cannot be encryption inputs) was wrong for K4: its four rows match the 31-column grid and may be planned. The text reflects the correction. Two tallies in the episode text (72 rows existing at encryption, 62 without a source) come out as 74 and 64 when recounted from the table; the recounted values are used here.

## Evidence boundary

The records only; K4's ciphertext was not read. The evidence search read public pages only, with no download and no computation. Pages claiming a solution and images that may document K4's method were not opened, under this study's rules.

## UNKNOWN

K5's ciphertext. What the maker's handwritten notes on "encryption layers" say. Whether the answer lies in one of the gaps or outside the matrix. External independent replications: zero.

## Falsification targets

A misclassified row that makes a "closed" cell actually empty would change the gap list. A new primary source that fixes an operator to a finite set would make its gap testable.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-capability-matrix): `python verify_capability_matrix.py` recomputes, from the 92 recorded rows, the unit × state × sync coverage, the empty letter cells, the origin and chronology tallies and the two-slip share, and prints `PASS`. Standard library only, under a second. It checks the bookkeeping, not the underlying tests.

## Evidence / Artifacts

[The 92-row matrix (CSV), summary, check and figure scripts](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-capability-matrix). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Test a gap when evidence arrives that fixes its operator (K5's ciphertext, production papers). Until then, no invented operators for gaps without a source.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/).
- K5's release: [Scientific American 2025-11-12](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/).
- Sanborn did the encryption himself, with Scheidt helping to choose the methods: [WIRED 2005](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/) (confirmed by the program's owner; the wording has not yet been checked verbatim in this study).
