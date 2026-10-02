# Kryptos K4: one phase break in machines already closed (EP-0168, EP-0176 with the 2026-10-02 controls)

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
| `results/hagelin-controls-under-20261002.json` | The 2026-10-02 addendum: the registered size rule and why it accepted nothing, the amended construction (controls planted under K4's own crib stage), engine v5, the K4 rerun on v5, and the five controls with their planted keys, ciphertexts and English scores |
| `verify_machine_phase_break.py` | Recomputes the counts, capacities and chance expectation; runs the single-rotor break test (A-Z or KRYPTOS numbering, step 0..25) on K4 and 200 shuffles, against brute force and with 100 planted breaks. For the addendum: checks that each recorded control equals K4 at the 24 crib positions, decrypts under its recorded key to the cribs (the text is not printed), shares K4's crib-position key values k_i = (C_i - 25 + P_i) mod 26, and that the acceptance arithmetic (5/5 >= 4/5; P(>= 4 of 5) = 0.34 at 0.6 and 0.92 at 0.9) and the threshold comparisons (every E_true >= 40.4, K4's 38.64 < 40.4) hold; prints `PASS` |
| `make_figure.py` | The Note's figure (the Hagelin row and the five controls' E_true are read from the two results files) |

## What is not rerun here

The full R-a (1,951,976 settings) and R-b (90,246,284 settings) sweeps use 274 keyword
alphabets and 329,366 position keys from earlier Notes and a compiled kernel; the Enigma +
sigma sweep (1.11 × 10¹⁰ settings) takes 14–23 minutes per ciphertext. The Hagelin-type run
(EP-0176) needed a GPU and an English 4-gram table, and so did the 2026-10-02 addendum: the five
control runs (one K4-size English stage each, about 45 min on a GPU) and the K4 rerun on engine v5.
They are recorded, not rerun. The single-rotor test here is the subset of R-a with the same wiring
numbering on both sides (the setting of EP-0083). A rerun of the author's code, not an independent
replication.
