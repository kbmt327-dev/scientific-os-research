# Kryptos K4: layout transpositions before the procedure enumerator (EP-0186)

Check package for the Open Research Lab note
*Does a transposition fixed by K4's layout, followed by the procedure enumerator, fit K4?*

```sh
python verify_layout_transposition.py   # standard library only, under a second
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_layout_pi.py` | The set Pi of 104 layout transpositions (routes on K4's 3 x 31 carved shape, at width 21, and on 96- and 98-cell rectangles), ported from the author's script; pure geometry on 97 positions |
| `results/layout-transposition-20261001.json` | The author's recorded results: the three stages on K4, the stop-rule outcome and its confirmation p value, shuffles and planted controls |
| `verify_layout_transposition.py` | Rebuilds Pi (176 items, 104 distinct, sha256 equal to the set committed before any run on K4), the 7.70-bit capacity of 208 settings, the closed-form chance of each stage, where the crib positions go under order B, and a round-trip control for every Pi; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The procedure enumerator builds selectors and chart rows from the K1-K3 texts and the carved
tableau, which this site does not publish, and the 208 settings ran on a GPU over about 16
hours. The confirmation statistic uses English letter frequencies. Both are recorded, not
rerun. The one stop-rule hit is recorded only as "not confirmed (p = 0.81)"; no candidate text
was displayed or written, and nothing about it is in this package.
A rerun of the author's code, not an independent replication.
