# Kryptos K4: what K1-K3 production left on the carved layout (EP-0141)

Rerun package for the Open Research Lab note
*Did making K1-K3 leave traces in the carved layout, and does K4 show the same kind?*

```sh
python verify_production_traces.py   # standard library only, a few seconds
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_production_traces.py` | Rank correlation, width-model residuals, the word-break chance, the offset from a 31-column grid with its permutation null, exact row-length chances |
| `results/production-traces-20260928.json` | Recorded per-row numbers (letters per carved row; mean letter width per row in three fonts) and the recorded results of every test |
| `verify_production_traces.py` | Recomputes the above from the per-row numbers and prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

T2's null re-breaks the same K1-K3 text with shuffled row lengths, and T1 needs the word
boundaries of the K1 and K2 plaintexts. This site does not publish the sculpture's text beyond
K4, so those parts are recorded only; the per-row mean widths are published as numbers, which
do not reveal the text. Fonts (Arial, Arial Narrow, Calibri) are stand-ins for hand-cut
letters. A rerun of the author's code, not an independent replication.
