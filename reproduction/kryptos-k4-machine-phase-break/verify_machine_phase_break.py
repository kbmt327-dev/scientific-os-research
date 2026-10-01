"""Recompute the break counts and a single-rotor break test of the machine phase-break Note
(EP-0168, EP-0176) and compare with the record.

    python verify_machine_phase_break.py

Rerun here: the 23 crib splits, 575 classes and 1,300 (b, t); the setting counts and capacities of
R-a, R-b and Enigma + sigma; the Enigma chance expectation in closed form; the exact single-rotor test
(EP-0083 subset of R-a: one free wiring, A-Z or KRYPTOS numbering, step d = 0..25) with a break on K4
and 200 shuffles, its agreement with brute force, and 100 planted breaks.  The full R-a / R-b / Enigma
sweeps (numba) and the Hagelin run (GPU) are recorded, not rerun.  Standard library only, about a second.
A rerun of the author's code, not an independent replication.
"""
import json
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
    check("recorded Hagelin: no climb at E >= 40.4, controls not run",
          h["K4"]["n_E_ge_40.4"] == 0 and h["K4"]["E_max"] < h["threshold_E"] and "not run" in h["planted_controls"])
    print(f"  recorded Hagelin climbs: K4 {h['climbs_b_weighted']:,} vs shuffles "
          f"{[s['climbs'] for s in h['shuffles']]} (ratio about {h['climbs_b_weighted'] / 2.0e6:.0f})")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: break counts, capacities and the single-rotor break test reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
