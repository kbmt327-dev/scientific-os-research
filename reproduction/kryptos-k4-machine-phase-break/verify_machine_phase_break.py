"""Recompute the break counts and a single-rotor break test of the machine phase-break Note
(EP-0168, EP-0176) and compare with the record.

    python verify_machine_phase_break.py

Rerun here: the 23 crib splits, 575 classes and 1,300 (b, t); the setting counts and capacities of
R-a, R-b and Enigma + sigma; the Enigma chance expectation in closed form; the exact single-rotor test
(EP-0083 subset of R-a: one free wiring, A-Z or KRYPTOS numbering, step d = 0..25) with a break on K4
and 200 shuffles, its agreement with brute force, and 100 planted breaks.  For the 2026-10-02 addendum
(five controls planted under K4's own crib stage, results/hagelin-controls-under-20261002.json): that each
recorded control equals K4 at the 24 crib positions, decrypts under its recorded key to the cribs (the text is
not printed), shares K4's crib-position key values, and the acceptance arithmetic and threshold comparisons.
The full R-a / R-b / Enigma sweeps (numba), the Hagelin run and the five control runs (GPU, about 45 min each)
are recorded, not rerun.  Standard library only, about a second.
A rerun of the author's code, not an independent replication.
"""
import json
import math
import random
import sys
from pathlib import Path

import k4_machine_phase_break as M

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "machine-phase-break-20260930.json").read_text(encoding="utf-8"))
    bad = []

    def check(name, ok):
        print(f"  {name:<66} {'ok' if ok else 'MISMATCH'}")
        if not ok:
            bad.append(name)

    c = M.counts()
    print(f"  splits {c['splits']}, b values {c['b_values']} (one split covers {c['b_in_largest_split']}), "
          f"classes {c['classes']}, (b, t) {c['bt']} = {c['bits_bt']:.2f} bit")
    br = rec["break"]
    check("23 splits, 575 classes, 1,300 (b, t), 10.3 bit",
          (c["splits"], c["classes"], c["bt"], round(c["bits_bt"], 1)) == (br["splits"], br["classes"], br["bt"], br["bits"]))
    for (k, v), (rk, rv) in zip(c["settings"].items(), rec["EP-0168"].items()):
        print(f"  {k:<13} settings {v:,}  with the break {c['bits_with_break'][k]:.1f} bit")
        check(f"{k} settings and capacity", v == rv["settings"] and round(c["bits_with_break"][k], 1) == rv["bits_with_break"])
    print(f"  Enigma: P(pass) per (setting, class) {c['enigma_p_pass']:.3g}; expected chance passes "
          f"{c['enigma_expected_false']:.2g} (no break {c['enigma_expected_false_no_break']:.2g})")
    check("Enigma expected chance passes 4.5e-5",
          round(c["enigma_expected_false"], 6) == rec["EP-0168"]["Enigma + free entry substitution (EP-0132 settings)"]["expected_false_passes"])

    # exact kernel against brute force: planted (often passing) and shuffled (rarely passing) cases
    rng = random.Random(1682)
    mism = with_pass = 0
    for i in range(300):
        name = rng.choice(list(M.ALPHABETS))
        al, d = M.ALPHABETS[name], rng.randrange(26)
        if i % 2:
            ct = M.shuffled(1000 + i)
        else:
            w = list(range(26))
            rng.shuffle(w)
            pt = "".join(M.CRIB.get(k, rng.choice(M.AZ)) for k in range(97))
            ct = M.encrypt(pt, al, w, rng.randrange(26), d, rng.choice(M.B_RANGE), rng.choice(M.T_RANGE))
        u, v = M.uv(ct, al, d)
        fast, ref = M.passing_classes(u, v), M.passing_classes_ref(u, v)
        mism += fast != ref
        with_pass += bool(ref)
    print(f"  single-rotor kernel vs brute force: mismatches {mism}/300 ({with_pass} cases with passes)")
    check("kernel agrees with brute force", mism == 0 and with_pass > 0)

    k4 = M.single_rotor_passes(M.K4)
    sh = sum(bool(M.single_rotor_passes(M.shuffled(s))) for s in range(1, 201))
    print(f"  single rotor (2 numberings x 26 steps) x 575 classes: K4 passes {len(k4)}; shuffles with a pass {sh}/200")
    check("single rotor with a break: K4 0, shuffles 0 (subset of R-a)", not k4 and sh == 0)
    pc = M.planted_controls(100)
    print(f"  planted single-rotor breaks recovered: {pc}/100")
    check("planted breaks 100/100", pc == 100)

    h = rec["EP-0176"]
    check("recorded Hagelin (2026-09-30): no climb at E >= 40.4, controls not run then",
          h["K4"]["n_E_ge_40.4"] == 0 and h["K4"]["E_max"] < h["threshold_E"] and "not run" in h["planted_controls"])
    print(f"  recorded Hagelin climbs: K4 {h['climbs_b_weighted']:,} vs shuffles "
          f"{[s['climbs'] for s in h['shuffles']]} (ratio about {h['climbs_b_weighted'] / 2.0e6:.0f})")

    # 2026-10-02 addendum: five controls planted under K4's own crib stage (recorded; the GPU runs are not repeated)
    rec2 = json.loads((HERE / "results" / "hagelin-controls-under-20261002.json").read_text(encoding="utf-8"))
    per, ctl, th = rec2["constants"]["PER"], rec2["controls_under"], h["threshold_E"]
    crib_pos = sorted(M.CRIB)
    k_k4 = {i: (M.AZ.index(M.K4[i]) - 25 + M.AZ.index(M.CRIB[i])) % 26 for i in crib_pos}
    same_ct = sum(all(c["ct"][i] == M.K4[i] for i in crib_pos) for c in ctl)
    print(f"  controls planted under K4's crib stage: {len(ctl)} recorded; equal to K4 at the 24 crib positions {same_ct}")
    check("five controls equal K4 at the 24 crib positions", len(ctl) == 5 and same_ct == 5)
    ok_dec = same_k = 0
    for c in ctl:
        cage, pins, b, t = c["cage"], c["pins"], c["b"], c["t"]

        def key(j):
            return sum(cage[w] * pins[w][(j + (t if j >= b else 0)) % per[w]] for w in range(6))

        # pt = 25 - ct + k (letters A = 0); compared only at the crib positions, never printed
        pt = [(25 - M.AZ.index(c["ct"][j]) + key(j)) % 26 for j in range(97)]
        ok_dec += [len(w) for w in pins] == per and all(pt[i] == M.AZ.index(M.CRIB[i]) for i in crib_pos)
        same_k += {i: (M.AZ.index(c["ct"][i]) - 25 + M.AZ.index(M.CRIB[i])) % 26 for i in crib_pos} == k_k4
    check("planted keys decrypt each control to the cribs at 21-33 and 63-73 (text not shown)", ok_dec == 5)
    check("crib-position key values k_i = (C_i - 25 + P_i) mod 26 equal K4's for every control", same_k == 5)

    def p_ge(n, k, p):
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))

    found = sum(bool(c["truth_found"]) for c in ctl)
    print(f"  controls recovered as the global maximum {found}/{len(ctl)} (rule: at least 4/5); "
          f"P(>= 4 of 5) = {p_ge(5, 4, 0.6):.2f} at p = 0.6, {p_ge(5, 4, 0.9):.2f} at p = 0.9")
    check("acceptance arithmetic: 5/5 >= 4/5; P(>= 4 of 5) 0.34 at 0.6, 0.92 at 0.9",
          found == 5 and found >= 4 and round(p_ge(5, 4, 0.6), 2) == 0.34 and round(p_ge(5, 4, 0.9), 2) == 0.92)
    k4v5 = rec2["k4_v5_reproduction"]
    print(f"  E_true of the controls {[c['E_true'] for c in ctl]} (threshold {th}; about "
          f"{sum(c['elapsed_s'] for c in ctl) / len(ctl) / 60:.0f} min each); K4 on engine v5: E_max {k4v5['E_max']}, "
          f"n(E >= {th}) {k4v5['n_E_ge_40.4']}, climbs {int(k4v5['leaves_b_weighted']):,}")
    check("every control E_true >= 40.4 and found; K4 v5 E_max 38.64 < 40.4 with none >= 40.4",
          all(c["E_true"] >= th and c["truth_found"] and c["top1_E"] == c["E_true"] for c in ctl)
          and k4v5["E_max"] == h["K4"]["E_max"] == 38.64 and k4v5["E_max"] < th and k4v5["n_E_ge_40.4"] == 0
          and int(k4v5["leaves_b_weighted"]) == h["climbs_b_weighted"] and k4v5["n_E_ge_20"] == h["K4"]["n_E_ge_20"])
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: break counts, capacities, the single-rotor break test and the planted-control record reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
