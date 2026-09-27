# Kryptos K4: position-varying affine maps and periodic Hill matrices (EP-0117, EP-0122)

Rerun package for the Open Research Lab note
*Do affine maps or Hill matrices that change along the text fit K4?*

```sh
python verify_affine_hill.py    # standard library only, about 40 seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_affine_hill.py` | Exact tests on the cribs: affine maps whose multiplier and shift are polynomials of degree ≤ 2 in the position (both directions, A–Z or KRYPTOS numbers), and 2×2 Hill with a matrix per period class; planted controls and shuffle nulls |
| `results/affine-hill-20260927.json` | Recorded results, including the searches not rerun here |
| `verify_affine_hill.py` | Reruns the affine and 2×2 Hill tests and prints `PASS` |
| `make_figure.py` | The Note's figure |

A rerun of the author's code, not an independent replication.

## Not rerun here

Exponential multipliers, running-key shifts over an English corpus and the K1–K3 texts, 3×3
Hill and Hill with a constant vector (all 160 settings), Hill matrices taken from texts
(EP-0122), and the carved tableau with its defect. Their outcomes are in `results/`.
