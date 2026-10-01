# Kryptos K4: one phase break in machines already closed (EP-0168, EP-0176)

Check package for the Open Research Lab note
*Does one phase break reopen the rotor, Enigma or Hagelin machines?*

```sh
python verify_machine_phase_break.py   # standard library only, about a second
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_machine_phase_break.py` | The break model (b = 22..73, t = 1..25; 23 crib splits, 575 classes, 1,300 (b, t)), setting counts and capacities, the Enigma chance expectation, and the exact single-rotor test with a break (bitmask form and brute force) |
| `results/machine-phase-break-20260930.json` | The author's recorded results: R-a, R-b and Enigma + sigma sweeps with shuffles and controls; the Hagelin-type run (EP-0176) |
| `verify_machine_phase_break.py` | Recomputes the counts, capacities and chance expectation; runs the single-rotor break test (A-Z or KRYPTOS numbering, step 0..25) on K4 and 200 shuffles, against brute force and with 100 planted breaks; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The full R-a (1,951,976 settings) and R-b (90,246,284 settings) sweeps use 274 keyword
alphabets and 329,366 position keys from earlier Notes and a compiled kernel; the Enigma +
sigma sweep (1.11 × 10¹⁰ settings) takes 14–23 minutes per ciphertext. The Hagelin-type run
(EP-0176) needed a GPU and an English 4-gram table. They are recorded, not rerun. The
single-rotor test here is the subset of R-a with the same wiring numbering on both sides
(the setting of EP-0083). A rerun of the author's code, not an independent replication.
