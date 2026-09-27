# Kryptos K4: charts whose rows are chosen by position (EP-0098, EP-0099, EP-0114)

Rerun package for the Open Research Lab note
*Can K4 come from a list of keyed rows chosen letter by letter?*

```sh
python verify_chosen_rows.py    # standard library only, about 10 seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_chosen_rows.py` | Keyed alphabets from a word list, 29 reading conventions, and the selection-free cover: how many crib letters at least one row could explain; shuffle null |
| `data/worldclock-places.json` | World Clock place names (from the EP-0011 package) |
| `results/chosen-rows-20260927.json` | Recorded results, including the searches not rerun here |
| `verify_chosen_rows.py` | Recomputes the cover for three public lists and prints `PASS` |
| `make_figure.py` | The Note's figure |

A rerun of the author's code, not an independent replication.

## Not rerun here

Lists built from the K1–K3 texts and the carved panel, the M-94 cylinder over every disk order,
matrix-mixed alphabets and the sequential searches (190 million settings). Their outcomes are in
`results/`.
