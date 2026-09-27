# Kryptos K4: keys from the sculpture's physical form (EP-0059-0069)

Rerun package for the Open Research Lab note
*Can the sculpture's physical form be K4's key?*

```sh
python verify_physical_keys.py  # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_physical_keys.py` | K4's place on the carved panel (from photographs), the shared-column test for keys that depend only on horizontal position (or horizontal plus vertical), and the roughness S of the crib keys against random keys |
| `results/physical-keys-20260927.json` | Recorded results (written by `record.py`), including the 3D-model searches not rerun here |
| `verify_physical_keys.py` | Recomputes the above and prints `PASS` |
| `make_figure.py` | The Note's figure |

The layout used is only which row and column each K4 letter occupies; no dimensions are needed. A
rerun of the author's code, not an independent replication.

## Not rerun here

Searches over the 3D model (sight lines, sunlight through the holes, shadow timing, distances),
the trunk wrap, wave bands, Morse and Berlin clock keys, turning grilles, and the Hagelin and
wheel devices. Their outcomes are in `results/`. The 3D model itself is published separately
(`static/kryptos-k4-model.html`).
