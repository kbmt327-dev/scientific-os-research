# Kryptos K4: width 21 rechecked (EP-0146)

Rerun package for the Open Research Lab note
*Does anything in K4 besides one pair table point to width 21?*

```sh
python verify_width21.py   # needs numpy, a few seconds
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_width21.py` | Bean's count R_w of repeated vertical pair types, single-letter coincidence, plug-in mutual information and coinciding pair-pairs at a lag, R_21 without the types made by doubled letters; ported from the author's audit script |
| `results/width21-20260928.json` | The recorded numbers (20,000 permutations, seed 2109) |
| `results/PRED-013.json` | Predictions for K5's ciphertext and for K4's plaintext, sealed before either is public (sha256 81adb6ec…c98dc) |
| `results/t1-lags-20260930.json` | Later check (EP-0185): the T1 prediction at lags 21, 42 and 63, its power from planted English texts, and the general form over periods 2-48 (recorded; the plants need English text) |
| `verify_width21.py` | Reruns everything with the same generator and seed (exact match), checks the sealed prediction's hash, recomputes EP-0185's coincidences and closed-form expectations at lags 21, 42, 63, prints `PASS` |
| `make_figure.py` | The Note's figure |

Ciphertext only; the cribs are used only to list which revealed pieces start on a width-21 row.
A rerun of the author's code, not an independent replication.
