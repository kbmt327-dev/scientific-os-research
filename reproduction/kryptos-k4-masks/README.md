# Kryptos K4: a substitution that masks the English (EP-0072-0077, EP-0084-0088)

Rerun package for the Open Research Lab note
*If a fixed substitution masks the English, which keys can still be tested?*

```sh
python verify_masks.py          # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_masks.py` | A completely free substitution before or after a shift key; exact tests for keys linear in position and for periodic keys (weighted union-find), with planted controls and a shuffle null giving the test's power per period |
| `results/masks-20260927.json` | Recorded results (written by `record.py`), including the searches not rerun here |
| `verify_masks.py` | Recomputes the above and prints `PASS` |
| `make_figure.py` | The Note's figure |

The periodic check requires consistent key and mask values and that no two letters are forced to the
same mask value; it does not also check that a full permutation completes, so it can only pass more
often than an exact test. A rerun of the author's code, not an independent replication.

## Not rerun here

Stride keys over the Kryptos texts, World Clock keys, anchor distances, M-94, autokeys, masks on both
sides with running keys and the English stage, the Carter & Mace running key, Hagelin capacity, ROLL
and aperture keys, and the hand-chosen English running key. Their outcomes are in `results/`.
