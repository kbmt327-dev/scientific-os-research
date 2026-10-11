# Kryptos K4: key-position slips inside and between the cribs (EP-0149, 0151, 0165, 0166; with the 2026-10-10 check EP-0211, 0215)

Check package for the Open Research Lab note
*Does the procedure enumerator fit K4 if the key position slips once inside a crib or between the cribs?*

```sh
python verify_crib_shifts.py          # standard library only, about 15 s (the 2026-10-10 part adds about a second)
python verify_crib_shifts.py --full   # all 240 periodic cells with shuffles, about 8 min
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_crib_shifts.py` | The slip configurations (480 inside the cribs, 4 between them), the closed-form chance of a false pass, and EP-0151's table-free test for periodic arbitrary rows with crib 2 shifted (ported from the author's audit script). For the 2026-10-10 check: EP-0211's setting generator (one-square Bifid with cipher letters lost or junk letters carved between the cribs; periodic, full-text and W-segment blocks; the 12 edge systems for two-letter squares), ported from the author's `f3d.py` and using only crib and W positions, and EP-0215's setting count per column and closed-form chance per setting |
| `results/crib-shifts-20260930.json` | The author's recorded results: enumerator runs on K4, two shuffles and planted controls (EP-0149, EP-0165), EP-0151's full table (crib letters to drop and shuffle P for 240 cells), EP-0166's records check |
| `results/crib-gap-squares-machines-20261010.json` | The 2026-10-10 check, statistics only: EP-0211 (setting counts, the 200-shuffle null run before K4, controls, K4 per column, the post-hoc d* screen) and EP-0215 (families, thresholds by d, setting counts, chance per setting and E by d, controls, K4's minimum h in all 30 columns, the shuffle null) |
| `verify_crib_shifts.py` | Recomputes the configuration counts, the chance values, EP-0166's 79 origins, EP-0151's periodic test on K4 (all 240 cells, exact) and its shuffle P values with the author's generator and seed (periods 3-20, or all with `--full`), and 10 planted periodic controls. For the 2026-10-10 check: regenerates EP-0211's settings (8,316 raw / 8,085 valid / 5,797 covered by EP-0169's model / 2,288 residual periodic, 105 full text, 348 W segments, so 2,741 raw and 2,649 distinct crib-block structures; 12 edge systems with 7 distinct constraint sets; 12 x 40 and 12 x 298,090 edge settings) and checks the null gate and the recorded K4 counts; recomputes EP-0215's settings per column (30 and 3 machines x 6 x 26^6), the closed-form chance per setting (h = 0, h <= 1, h <= 2), the E allocation (Enigma I h <= 1 at every d: 0.00251; commercial h <= 2 at d = +-1: 0.01524 each, h <= 1 at d = +-2: 6.3e-5 each; total 0.0331; the unadjusted plan 0.0635), and checks that every recorded column minimum lies above its threshold; prints `PASS` |
| `make_figure.py` | The Note's figure (the original runs only) |

## What is not rerun here

The procedure enumerator builds selectors and chart rows from the K1-K3 texts and the carved
tableau, which this site does not publish, and the slip runs used a GPU (about 4 hours for
EP-0149). Their hit counts, shuffles and planted controls are recorded, not rerun. EP-0151's
enumerator part is an argument from an earlier per-crib run (EP-0134), not a computation.

For the 2026-10-10 check: EP-0211's exact one-square solver (with a CP-SAT fallback), its
200-shuffle null and its planted controls, and the edge column's keyword squares (built from word
lists of earlier Notes) are recorded, not rerun. EP-0215's machine scans (7.34 × 10¹¹ settings on a
GPU, about 21 minutes per Enigma I ciphertext), its planted controls and its shuffle null are
recorded, not rerun. A rerun of the author's code, not an independent replication.
