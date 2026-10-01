"""Recompute the crib-only parts of the crib-slip Note (EP-0149, EP-0151, EP-0165, EP-0166) and
compare with the record.

    python verify_crib_shifts.py          # about 15 s: P values for periods 3-20
    python verify_crib_shifts.py --full   # about 8 min: P values for all 240 cells

The enumerator runs (EP-0149, EP-0165) build selectors from the K1-K3 texts and the carved
tableau and ran on a GPU; their hit counts are recorded in results/ and not rerun here.
What is rerun: the 480 slip configurations and 4 shift configurations, the closed-form chance
values, the 79 origins of EP-0166, EP-0151's periodic test on K4 (all 240 cells, exact), its
shuffle P values with the author's generator and seed (periods 3-20 by default, all with --full),
and planted periodic controls.  Standard library only.
A rerun of the author's code, not an independent replication.
"""
import json
import sys
from math import isclose, log2
from pathlib import Path

import k4_crib_shifts as K

HERE = Path(__file__).resolve().parent


def main():
    full = "--full" in sys.argv
    rec = json.loads((HERE / "results" / "crib-shifts-20260930.json").read_text(encoding="utf-8"))
    n = rec["enumerator_procedures"]
    bad = []

    def check(name, got, want, rel=0.06):
        ok = isclose(got, want, rel_tol=rel)
        print(f"  {name:<52} {got:.3g}  (recorded {want:.3g})  {'ok' if ok else 'MISMATCH'}")
        if not ok:
            bad.append(name)

    r49 = rec["EP-0149 slips inside both cribs"]
    conf = K.inside_slip_configurations()
    print(f"  EP-0149 configurations: {len(conf)} ({log2(len(conf)):.1f} bit)")
    if len(conf) != r49["configurations"]:
        bad.append("EP-0149 configurations")
    check("EP-0149 chance, 480 configurations, e = 0", K.chance(n, 480, 0), r49["chance"]["e0"])
    check("EP-0149 chance, 480 configurations, e <= 4", K.chance(n, 480, 4), r49["chance"]["e4"])
    # recorded as 0.6 in the episode's plan; the formula gives 0.53 (not run, so no claim depends on it)
    check("EP-0149 chance, e <= 7 (not run)", K.chance(n, 480, 7), r49["chance"]["e7_not_run"], rel=0.15)

    r65 = rec["EP-0165 shift between the cribs with crib errors"]
    sh = K.between_shift_configurations()
    print(f"  EP-0165 shifts: {sh}")
    if sh != r65["shifts"]:
        bad.append("EP-0165 shifts")
    check("EP-0165 chance per configuration, e <= 2", K.chance(n, 1, 2), r65["chance_per_configuration"])
    check("EP-0165 chance, 4 configurations, e <= 2", K.chance(n, 4, 2), r65["chance"])

    r66 = rec["EP-0166 origins of i div m"]
    print(f"  EP-0166 origins (sum of m over {r66['m']}): {sum(r66['m'])}")
    if sum(r66["m"]) != r66["origins"]:
        bad.append("EP-0166 origins")

    per = rec["EP-0151 shift between the cribs"]["periodic_arbitrary_rows"]
    tab = K.periodic_table()
    diff = [c for c in tab if tab[c] != per["drops"][f"{c[0]},{c[1]}"]]
    print(f"  EP-0151 periodic test on K4: {len(tab)} cells, {len(diff)} differ from the record")
    if diff:
        bad.append("EP-0151 drops")
    for d in K.SHIFTS:
        z = [p for p in K.PERIODS if tab[(p, d)] == 0]
        print(f"    d = {d:+d}: {len(z)} of 48 periods fit with no crib letter dropped (smallest {min(z)})")
    lo, hi = (1, 48) if full else (3, 20)
    cells = [(p, d) for p in range(lo, hi + 1) for d in K.SHIFTS]
    P = K.shuffle_p(tab, cells, shuffles=per["shuffles"], seed=per["seed"])
    pdiff = [c for c in cells if f"{P[c]:.3f}" != f"{per['P'][f'{c[0]},{c[1]}']:.3f}"]
    best = min(P, key=P.get)
    print(f"  shuffle P for periods {lo}-{hi} ({len(cells)} cells, 2,000 shuffles, seed {per['seed']}): "
          f"{len(pdiff)} differ; smallest {P[best]:.3f} at p {best[0]}, d {best[1]:+d}")
    if pdiff:
        bad.append("EP-0151 P")
    allP = sorted(per["P"].values())
    m = len(allP)
    print(f"  smallest recorded P over all {m} cells: {allP[0]}; expected minimum of {m} independent "
          f"uniform P values 1/(m+1) = {1 / (m + 1):.4f}; cells at or below 0.05: {sum(x <= 0.05 for x in allP)} "
          f"(expected about {0.05 * m:.0f} if independent)")
    if allP[0] != per["min_P"] or allP[0] < 1 / (m + 1):
        bad.append("EP-0151 min P")

    found = 0
    for k, (p, d) in enumerate([(6, 1), (8, 2), (8, -1), (11, -2), (5, 2), (7, -1), (13, 1), (4, 0), (10, 2), (9, -2)]):
        ct = K.planted(p, d, 151 + k)
        found += K.drops(ct, p, d) == 0
    print(f"  planted periodic ciphertexts consistent at their own (p, d): {found}/10")
    if found != 10:
        bad.append("planted")

    if r49["K4_other_hits"] or r49["K4_identity_hits"] or r65["K4_other_hits"] or r65["K4_identity_hits"]:
        bad.append("recorded enumerator hits")
    print(f"  recorded: EP-0149 K4 hits {r49['K4_other_hits']} (controls {r49['controls']['slips_only_e4']}, "
          f"{r49['controls']['slips_plus_1_to_4_carving_errors_e4']}); EP-0165 K4 hits {r65['K4_other_hits']} "
          f"(controls {r65['controls']['shift_only']}, {r65['controls']['shift_plus_1_to_2_carving_errors']})")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: configuration counts, chance values and the periodic test reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
