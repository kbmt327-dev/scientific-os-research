# Kryptos K4: the capability coverage matrix (EP-0142)

Check package for the Open Research Lab note
*What have the tests so far actually covered, and where are the gaps?*

```sh
python verify_capability_matrix.py   # standard library only, under a second
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `results/capability-matrix-20260928.csv` | 92 rows, one per catalogue family or episode: unit, state, synchronisation, stages, alphabet, reordering, error spread, origin, chronology, basis of the verdict, verdict, and a prior weight for hand work (never used to refute). Values are in Japanese, as recorded |
| `results/capability-matrix-summary-20260928.json` | The recorded summary: empty letter cells, tallies, the eleven gap groups G1-G11 |
| `k4_capability_matrix.py` | Builds the unit x state x sync coverage cube from the rows |
| `verify_capability_matrix.py` | Recomputes the cube, the empty cells, the tallies and the two-slip share; prints `PASS` |
| `make_figure.py` | The Note's figure |

No K4 data is read and no K4 test is run. The rows are the author's reading of the records,
so what this package checks is the bookkeeping, not the underlying tests. A rerun of the
author's code, not an independent replication.
