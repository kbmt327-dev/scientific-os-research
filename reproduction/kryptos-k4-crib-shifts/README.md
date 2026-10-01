# Kryptos K4: key-position slips inside and between the cribs (EP-0149, 0151, 0165, 0166)

Check package for the Open Research Lab note
*Does the procedure enumerator fit K4 if the key position slips once inside a crib or between the cribs?*

```sh
python verify_crib_shifts.py          # standard library only, about 15 s
python verify_crib_shifts.py --full   # all 240 periodic cells with shuffles, about 8 min
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_crib_shifts.py` | The slip configurations (480 inside the cribs, 4 between them), the closed-form chance of a false pass, and EP-0151's table-free test for periodic arbitrary rows with crib 2 shifted (ported from the author's audit script) |
| `results/crib-shifts-20260930.json` | The author's recorded results: enumerator runs on K4, two shuffles and planted controls (EP-0149, EP-0165), EP-0151's full table (crib letters to drop and shuffle P for 240 cells), EP-0166's records check |
| `verify_crib_shifts.py` | Recomputes the configuration counts, the chance values, EP-0166's 79 origins, EP-0151's periodic test on K4 (all 240 cells, exact) and its shuffle P values with the author's generator and seed (periods 3-20, or all with `--full`), and 10 planted periodic controls; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The procedure enumerator builds selectors and chart rows from the K1-K3 texts and the carved
tableau, which this site does not publish, and the slip runs used a GPU (about 4 hours for
EP-0149). Their hit counts, shuffles and planted controls are recorded, not rerun. EP-0151's
enumerator part is an argument from an earlier per-crib run (EP-0134), not a computation.
A rerun of the author's code, not an independent replication.
