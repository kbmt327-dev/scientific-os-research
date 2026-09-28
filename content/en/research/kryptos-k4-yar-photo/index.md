---
research_id: KRYPTOS-K4-EP-0139
title: Are the raised letters and the extra L deliberate marks or construction offsets?
date: '2026-09-28'
lang: en
domain: Kryptos K4
type: Finding
status: Undecided. In the higher-resolution photo only Y, A and R are raised, by about 1.5-1.9 cm, with the H between them and the rows above and below unmoved (the pre-registered 'intended' pattern); the other photo shows the same direction below threshold, so the two photos disagree. No plate-bend or fitting pattern in either. The extra L cannot be measured on any public photo
evidence_level: Letter positions measured on two public photos; statistic and classes committed before measuring; two design errors in the pre-registration found after measuring and recorded
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Bounding boxes of cut-out letters read on two public photos (Jim Gillogly; Carol M. Highsmith, Library of Congress), pixel numbers only, no image stored
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only whether two anomalies of the sculpture (three raised letters in cipher row 14; one tableau row with 32 cells) are marks or construction offsets, judged on photos; not a cipher method; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0139
source_episode_sha256: 977c4095f1d922a5da0ae96eb4370a754032c0308484e04d493044ee3fae9df0
publication:
  status: publishable
tags:
- kryptos-k4
- physical
- measurement
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-yar-photo/" hreflang="ja">日本語</a></p>

## Research question

Two anomalies of the sculpture have long been known: in cipher row 14 (the top row of the lower plate, inside K3) the letters Y, A and R are reported to sit a few centimetres high, and one tableau row has 32 cells instead of 31, ending in an L. Are these marks the maker intended, or construction offsets?

## Why this matters

If they are marks, they support the reading that the maker switched charts with physical marks (catalog J09). If they are construction offsets, they can be set aside as clues to the method. Neither reading had been tested on photos.

## Method

- **What is measured.** The bounding box of each cut-out letter on public photos (left, right, top, bottom in pixels), rows 13, 14 and 15, columns 0–10. Photos from the back are mirrored and still usable. No image was stored, only pixel numbers.
- **Statistic (committed before measuring).** Each row's letter centres are fitted with a quadratic in horizontal position (tilt, curvature, perspective). Row 14 is fitted without columns 2–7, and residuals are measured in units of the row pitch P. Controls are rows 13 and 15 and row 14 outside columns 2–7. A letter is displaced when |residual| ≥ max(5σ, 0.08P, largest control).
- **Classes (fixed before measuring).** Intended: Y, A and R all displaced, while the H between them, the neighbours and the letters above and below are not. Local construction: the shift spreads to neighbours, or the rows above and below move the same way (plate bend, seam). Row offset: nothing displaced inside row 14, but the whole row sits off the grid. Two photos from different positions that agree settle a class; disagreement leaves it undecided.
- **Extra L.** A statistic comparing the letter spacing of that tableau row with the rows above and below was fixed in advance.

## Results

| Photo | Side | In-plate row pitch | Y, A, R residual (P) | H residual | Pre-registered class |
|---|---|---|---|---|---|
| Highsmith (LOC 2011631531) | back (mirrored) | about 100 px | −0.102, −0.129, −0.103 | −0.008 | **intended** |
| Gillogly (`ciphermidleft.jpg`) | front | about 47 px | −0.062, −0.059, −0.023 | +0.059 | row offset (forced by the seam; effectively "not seen") |

- Threshold 0.08P in both; control noise σ was 0.005P (Highsmith) and 0.012P (Gillogly).
- Size: in the Highsmith photo the three letters sit about 1.5–1.9 cm high (in-plate pitch about 11.7 cm); in the Gillogly photo about 1 cm or less, below threshold.
- Letters at the same horizontal position in the rows above and below do not move in either photo.
- **Combined verdict: undecided** (the classes disagree).
- **Extra L: undecided.** No public photo shows all 32 cells of that row at usable resolution.

Two design errors in the pre-registration showed up after measuring. A plate seam lies between rows 13 and 14, so the row-offset test (the difference between the 13→14 and 14→15 gaps) is always large; Gillogly's "row offset" is forced by the seam and carries no information. And P became a median that includes the gap across the seam, 1.25–1.34 times the in-plate pitch, so residuals in P are understated. Neither changes the combined verdict.

## Current finding

Under the pre-registered rules the YAR anomaly is undecided. The higher-resolution photo shows the "intended" pattern: only Y, A and R sit about 1.5–1.9 cm high, and neither the H between them nor the rows above and below move. The other photo points the same way but stays below threshold. Neither photo shows a plate-bend or fitting pattern. The extra L cannot be measured on any public photo.

## Key figure

![Dot plot of height residuals for the 11 letters of row 14 in two photos: in the Highsmith photo only Y, A and R cross the −0.08 threshold at −0.10 to −0.13; the Gillogly dots point the same way inside the threshold; the other letters sit near 0](/assets/kryptos-k4-yar-photo.svg)

## What this research shows

- In the higher-resolution public photo only Y, A and R are raised. If this were the scatter of cutting each letter by hand, it would be 8–20 times the control letters' scatter and would hit only these three.
- No plate-bend or fitting pattern appears in either photo.
- The row lies inside K3, not K4. Even as marks, they bear no relation to the positions where K4's chart must switch (25|26, 32|33, 67|68).

## What this research does not show

It does not show the letters are deliberate marks: the two photos give different classes and the rules leave it undecided. Nothing is said about the extra L. Neither result carries information about K4's method.

## What changed

The "YAR shift" moved from an untested report to a measured "undecided", with a statement of what would decide it.

## What failed

The pre-registration overlooked the seam twice. Automatic edge finding broke on the back-lit photo, so edges were taken from the brightness step inside hand-set windows, and weak edges were read by eye (a rule set after the YAR area had been seen, so observer bias is possible).

## Evidence boundary

Two public photos and the pixel coordinates read from them; the images are neither stored nor published. The public package recomputes residuals and classes from the recorded coordinates; it does not re-measure the photos.

## UNKNOWN

Whether a photo from another position, with a row pitch of 100 px or more, also shows the "intended" pattern. Whether the extra L was laid out as 32 cells from the start or added. External independent replications: zero.

## Falsification targets

One more photo from a different position at sufficient resolution, agreeing on "intended" or on a construction class under the pre-registered rules, would settle the question.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-yar-photo): `python verify_yar_photo.py` recomputes the row-14 residuals and each photo's class from the recorded pixel coordinates and prints `PASS`. Needs numpy; under a second. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Pixel coordinates, recorded results, statistic and figure scripts](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-yar-photo). MIT-licensed. No photos are included.

## External audit

No external independent replication. No survey of the sculpture and no review by a photo analyst.

## Next experiment

The same measurement on a high-resolution photo from another position (row pitch 100 px or more); a frontal photo of the tableau row and its neighbours (letter pitch 50 px or more).

## Sources

- Photos: Jim Gillogly, `ciphermidleft.jpg` (viewed only); Carol M. Highsmith, Library of Congress, [LOC 2011631531](https://www.loc.gov/pictures/item/2011631531/) (public domain).
- Reports of the anomalies: [Elonka Dunin](https://elonka.com/kryptos/).
- Jim Sanborn, *Kryptos* (1990).
