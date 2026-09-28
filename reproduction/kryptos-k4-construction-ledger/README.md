# Kryptos K4: operators fixed by the carved layout (EP-0140)

Rerun package for the Open Research Lab note
*Which operators do the sculpture's production facts fix, and do they fit K4?*

```sh
python verify_construction_ledger.py   # standard library only, about a second
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_layout_ledger.py` | K4's rows and columns on the carved panel, the exact consistency test for one arbitrary table per class, the planted control, and the row-length chance |
| `results/construction-ledger-20260928.json` | The ledger of 13 production and installation facts (grade, which operator each fixes, or STOP) and the recorded results for all seven operator variants |
| `verify_construction_ledger.py` | Reruns the row (L1) and column (L2) operators with 20,000 shuffles in the author's random order (exact match) and the row-length chance; prints `PASS` |
| `make_figure.py` | The Note's figure |

Only K4's coordinates are used (row 24 columns 27-30, then rows 25-27 of 31 letters). The fold
operators (G1-G3) need the letters behind K4 on the tableau and the upper cipher plate; this site
does not publish the carved text beyond K4, so they are recorded, not rerun. A rerun of the
author's code, not an independent replication.
