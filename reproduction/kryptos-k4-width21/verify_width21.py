"""Rerun the width-21 recheck (EP-0146) and compare with the record; check the sealed prediction.

    python verify_width21.py

Needs numpy; a few seconds.  Uses the same random generator and seed as the author's run, so
every number matches exactly.  A rerun of the author's code, not an independent replication.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

import k4_width21 as W

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "width21-20260928.json").read_text(encoding="utf-8"))
    bad = []
    reps = W.repeated_types(21)
    order = sorted(reps, key=lambda k: reps[k][0])
    dbl = [k for k, v in reps.items() if len(v) == 2 and v[1] - v[0] == 1]
    print(f"  width 21: {len(reps)} repeated vertical pair types {order}; from doubled letters {sorted(dbl)}")
    if order != rec["repeated_types_w21"] or sorted(dbl) != sorted(rec["double_induced_types"]):
        bad.append("types")
    if W.doubles() != rec["doubles"]:
        bad.append("doubles")
    K, P = W.permutations()
    print("  lag   R (expected, P)            kappa (expected, P)")
    for w in W.LAGS:
        rk, rp = int(W.R(K, w)[0]), W.R(P, w)
        kk, kp = int(W.kappa(K, w)[0]), W.kappa(P, w)
        got = {"R": rk, "E_R": round(float(rp.mean()), 1), "P_R": round(float((rp >= rk).mean()), 5),
               "kappa": kk, "E_kappa": round(float(kp.mean()), 1), "P_kappa": round(float((kp >= kk).mean()), 3)}
        print(f"  {w:>3}   {rk:>2} ({got['E_R']:.1f}, {got['P_R']:.4f})       {kk:>2} ({got['E_kappa']:.1f}, "
              f"{got['P_kappa']:.3f})")
        if got != rec["lags"][str(w)]:
            bad.append(f"lag {w}")
    sub = P[:5000]
    r21 = W.R(sub, 21)
    for name, f in (("MI_lag21", W.mi), ("pair_pairs_lag21", W.coincident_pairpairs)):
        v, vk = f(sub, 21), float(f(K, 21)[0])
        got = {"K4": round(vk, 3), "P": round(float((v >= vk).mean()), 4),
               "r_with_R21": round(float(np.corrcoef(v, r21)[0, 1]), 2)}
        print(f"  {name}: K4 {got['K4']}, P {got['P']}, correlation with R_21 {got['r_with_R21']} (forced)")
        if got != rec["forced"][name]:
            bad.append(name)
    rn_k, rn_p = int(W.R_nodouble(K, 21)[0]), W.R_nodouble(P, 21)
    got = {"K4": rn_k, "mean": round(float(rn_p.mean()), 2), "P": round(float((rn_p >= rn_k).mean()), 4)}
    print(f"  width 21 without the double-induced types: {got}")
    if got != rec["without_doubles"]:
        bad.append("without doubles")
    widths = [w for w in range(2, 49) if 21 % w == 0 and 63 % w == 0]
    print(f"  widths 2-48 where both crib phrases (21, 63) start a row: {widths}")
    if widths != rec["crib_start_widths"]:
        bad.append("crib widths")
    h = hashlib.sha256((HERE / "results" / "PRED-013.json").read_bytes()).hexdigest()
    print(f"  sealed prediction PRED-013 sha256 {h[:16]}...")
    if h != rec["pred013_sha256"]:
        bad.append("PRED-013 hash")
    # Later check (EP-0185): the T1 prediction at lags 21, 42, 63 with the closed-form expectation (97 - L) q
    t1 = json.loads((HERE / "results" / "t1-lags-20260930.json").read_text(encoding="utf-8"))
    from collections import Counter
    q = sum(c * (c - 1) for c in Counter(W.K4).values()) / (97 * 96)
    print(f"  EP-0185: flat coincidence rate q = {q:.5f}")
    if abs(q - t1["q"]) > 1e-12:
        bad.append("EP-0185 q")
    tot_k = tot_e = 0
    for L in (21, 42, 63):
        kk, e = int(W.kappa(K, L)[0]), (97 - L) * q
        tot_k, tot_e = tot_k + kk, tot_e + e
        r = t1["lags"][str(L)]
        print(f"    lag {L}: kappa {kk}, closed-form expectation {e:.2f} (recorded {r['kappa']}, {r['E']}, "
              f"shuffle p {r['p']})")
        if kk != r["kappa"] or round(e, 2) != r["E"]:
            bad.append(f"EP-0185 lag {L}")
    print(f"    sum over 21, 42, 63: {tot_k} against {tot_e:.2f}; literal prediction met: "
          f"{t1['literal_prediction_met']} (recorded power {t1['power']['all_three']}: cannot decide)")
    if tot_k != t1["sum_21_42_63"] or W.R(K, 21)[0] != t1["R"]["21"]:
        bad.append("EP-0185 sum or R_21")
    print(f"    recorded: T1 x periodic key dropped for p = {t1['general_form']['dropped_periods']}; "
          f"R_21 >= 11 under T1 + period 7 in {t1['power']['R21_ge_11_under_T1_period7']:.1%} of plants")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: only the lag-21 pair table points to 21; the statistics it does not imply are at chance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
