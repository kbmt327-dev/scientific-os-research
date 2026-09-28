"""Recompute what the production-traces Note (EP-0141) derives from recorded per-row numbers
and compare with the record.

    python verify_production_traces.py

Standard library only, a few seconds.  Recomputed: the rank correlation between each carved
row's letter count and its mean letter width for three fonts, the width-model residuals of
K4's four rows, the chance values of the word-break test (T1), the post hoc offset from a
31-column grid with its permutation null, and the chance that K4's four rows are all 31.  Not
rerun: the re-breaking null of T2 and the word boundaries of T1, which need the K1-K3 text.
A rerun of the author's code, not an independent replication.
"""
import json
import random
import sys
from math import isclose
from pathlib import Path

import k4_production_traces as T

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "production-traces-20260928.json").read_text(encoding="utf-8"))
    bad = []
    n = rec["row_lengths"]
    print(f"  row lengths: top plate {sum(n[:14])} characters, bottom plate {sum(n[14:])} (= 14 x 31)")
    for font, t2 in rec["T2"].items():
        if not isinstance(t2, dict):
            continue
        m = rec["row_mean_advance_width"][font]
        rho = T.spearman(n, m)
        res = [round(x, 2) for x in T.ols_residuals(n, m, range(24), range(24, 28))]
        print(f"  T2 {font:<12} rho(letters per row, mean width) = {rho:+.3f}; K4 rows 24-27 residuals {res}")
        if round(rho, 3) != t2["rho"] or res != t2["k4_residuals"]:
            bad.append(f"T2 {font}")
    t1 = rec["T1"]
    pa = T.at_least_one(t1["local_fraction_per_break"])
    pb = T.at_least_one([t1["global_density"]] * t1["breaks_tested"])
    ea = sum(t1["local_fraction_per_break"])
    print(f"  T1 row breaks on word breaks {t1['on_word_boundary']}/{t1['breaks_tested']}: expected {ea:.2f} "
          f"(local), P(>=1) {pa:.3f}; global density: expected {t1['global_density'] * 12:.2f}, P(>=1) {pb:.3f}")
    if not (isclose(pa, t1["P_local"], abs_tol=0.001) and isclose(pb, t1["P_global"], abs_tol=0.001)
            and isclose(ea, t1["expected_local"])):
        bad.append("T1")
    rng = random.Random(1412)
    p = rec["P_posthoc"]
    for name, rows, key in (("top", n[:14], "top"), ("bottom", n[14:], "bottom")):
        obs, mean, pv = T.permutation_null(rows, 100_000, rng)
        print(f"  post hoc {name} plate: offset range {obs:.2f}, permutation null mean {mean:.2f}, P(<=) {pv:.3f}")
        if not (isclose(obs, p[f"{key}_range"], abs_tol=0.01) and isclose(pv, p[f"{key}_P"], abs_tol=0.01)):
            bad.append(f"P {name}")
    last = T.last_k_all(n[14:])
    print(f"  K4's four rows all 31 within the bottom plate: {last:.4f} (exact)")
    if not isclose(last, p["last_four_all_31"], abs_tol=0.0005):
        bad.append("last four")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: row lengths follow letter widths, K4's rows fit the same model, and the chance values reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
