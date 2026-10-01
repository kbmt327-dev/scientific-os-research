# Kryptos K4: the fold lines of chart #3 (EP-0148, EP-0154, EP-0167)

Check package for the Open Research Lab note
*Do the fold lines on the K3 worksheet tell where K4's key restarts?*

```sh
python verify_chart3_folds.py   # standard library only, about 15 seconds
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_chart3_folds.py` | The 14 x 31 cell geometry of chart #3 (no letters), the K4 cells on the fold columns 6 and 25, and the restart test: same-phase crib pairs under a shift table and under arbitrary rows, with the 100,000-shuffle null |
| `results/chart3-folds-20260930.json` | The recorded inventory of the public chart #3 image, the 2025 materials (form only), the NOVA stills, and the restart test |
| `verify_chart3_folds.py` | Recomputes the crossings and the restart test (in the author's random order, so the shuffle rates match exactly), plus the share of shuffles that disagree at every pair; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The inventory of the marks on the chart #3 image, the reading of the 2025 auction and press materials and the
look at the NOVA stills are records of what was seen; they are not computations. No image is included.
A rerun of the author's code, not an independent replication.
