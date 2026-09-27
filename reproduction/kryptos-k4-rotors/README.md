# Kryptos K4: rotor machines (EP-0083, EP-0121, EP-0132)

Rerun package for the Open Research Lab note
*Can a rotor machine with a free wiring produce K4's cribs?*

```sh
python verify_rotor.py          # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_rotor.py` | One rotor with completely free wiring, stepped d positions per letter in A–Z or KRYPTOS contact numbering; the exact existence test for a wiring, planted controls and a shuffle null |
| `results/rotors-20260927.json` | Recorded results, including the larger searches not rerun here |
| `verify_rotor.py` | Reruns the single-rotor test on K4, 200 planted rotors and 2,000 shuffles, and prints `PASS` |
| `make_figure.py` | The Note's figure |

A rerun of the author's code, not an independent replication.

## Not rerun here

The chart of powers of one permutation (EP-0083), rotors with keyed entry and exit alphabets,
rotors stepped by position keys, the odometer with a free slow rotor (EP-0121, 7.9 × 10¹⁰
settings on a GPU) and the reflector machines behind a free substitution (EP-0132,
1.11 × 10¹⁰ settings on a GPU). They use keyword alphabets built from word lists and GPU batch
code; their outcomes are in `results/`.
