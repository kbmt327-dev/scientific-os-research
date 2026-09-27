# Kryptos K4: testing key sources without knowing the chart (EP-0092, 0093, 0100, 0124)

Rerun package for the Open Research Lab note
*Can a key source be tested without knowing the chart it drives?*

```sh
python verify_key_sources.py    # standard library only, about 20 seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_key_sources.py` | The chart-free consistency test for a key source under a Latin-square chart; hint keywords (390 phases), date and coordinate digit strings (78 phases), periods 2–48, decoy lists; the vertical-repeat count by width with a scan-corrected permutation null |
| `results/key-sources-20260927.json` | Recorded results, including the text-based sources not rerun here |
| `verify_key_sources.py` | Recomputes the above and prints `PASS` |
| `make_figure.py` | The Note's figure |

A rerun of the author's code, not an independent replication.

## Not rerun here

Sources taken from the K1–K3 plaintexts and the carved panel, the tableau at K4's place and
the carved column numbers read the sculpture's text or layout, which this site does not
publish. Clock-hand, carved-geometry and T-position sources (EP-0100, EP-0124) are recorded.

The width-21 phenomenon is at the resolution limit of 20,000 permutations (1 permutation reaches
K4's count at width 21). The internal run gave 0.0029 after the scan; this rerun gives 0.001.
