# Kryptos K4: W as a null, reversed key, Morse mask, digit-wise addition (EP-0180 to EP-0183, with EP-0187)

Check package for the Open Research Lab note
*Does K4 fit W as a null, a reversed key, a Morse mask or digit-wise addition?*

```sh
python verify_w_morse_digits.py   # standard library only, a few seconds
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_w_morse_digits.py` | The W-skipping key index, the reversed-direction identity of the stride text keys, the Morse-mask logic on the crib, and the digit-wise addition mechanism with planted controls |
| `results/w-morse-digits-20260930.json` | The author's recorded results: enumerator and text-key runs under the W-skipping index, the reversed-direction counts, the Morse-mask search with a free substitution, the digit-addition run on the 22 fixed strings |
| `results/wskip-both-side-english-20261002.json` | EP-0187 (2026-10-01): the English stage of the two-sided masks under the W-skipping index; scorer, threshold, planted recovery, power, the K4 and shuffle-3 statistics and the verdict |
| `verify_w_morse_digits.py` | Recomputes the crib-only parts and compares them with the record; for EP-0187, recomputes the power product 0.875 × 0.641 = 0.56 and applies the candidate rule (score ≥ THETA and above the shuffle maximum) to the recorded statistics (0 candidates); prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

- The procedure enumerator under the W-skipping index (GPU, 3 alignments, up to 2 crib errors).
- The text-key runs (61.7 million settings per gate): they read K1–K3 cipher and plain text, the tableau and
  the World Clock place names, which this site does not publish. Their chance values are recomputed from the
  recorded setting counts.
- The English stage for the two-sided masks under the W-skipping index (EP-0187, 2026-10-01: all 5,970 K4
  survivors and shuffle 3 on a GPU, 14/16 planted controls) is recorded in
  `results/wskip-both-side-english-20261002.json`, not rerun; only its power and candidate arithmetic is recomputed.
- The Morse mask with a free substitution (22.4 million settings); only the logic that excludes the pure form
  is rerun.
- The digit-addition run on the 22 fixed digit strings. The strings are not listed here; the package checks the
  mechanism on random digit strings instead.

A rerun of the author's code, not an independent replication.
