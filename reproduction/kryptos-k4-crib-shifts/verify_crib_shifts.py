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

2026-10-10 addendum (EP-0211, EP-0215): the generator of EP-0211's settings (8,316 / 8,085 / 5,797 /
2,288 periodic, 105 full text, 348 W segments -> 2,741 raw, 2,649 distinct structures; 12 edge systems
with 7 distinct constraint sets), and EP-0215's setting counts, closed-form chance per setting and the
registered E allocation (total 0.0331); the recorded K4 and null values are checked for consistency.
The exact square solver and the GPU machine scans are recorded, not rerun.
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

    addendum(bad, check)
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: configuration counts, chance values and the periodic test reproduce; "
          "2026-10-10 addendum counts and chance allocation reproduce")
    return 0


def addendum(bad, check):
    """2026-10-10 addendum (EP-0211, EP-0215): recompute the setting counts and the chance allocation, and check
    the recorded results for internal consistency.  The square solver (CP-SAT) and the GPU machine scans are not
    rerun."""
    rec = json.loads((HERE / "results" / "crib-gap-squares-machines-20261010.json").read_text(encoding="utf-8"))

    def same(name, got, want):
        ok = got == want
        print(f"  {name:<52} {got}  (recorded {want})  {'ok' if ok else 'MISMATCH'}")
        if not ok:
            bad.append(name)

    print("  -- 2026-10-10 addendum: EP-0211 (one-square Bifid, deletion / insertion between the cribs)")
    r = rec["EP-0211 one-square Bifid with a deletion or insertion between the cribs"]
    c = r["counts"]
    S = K.f3d_settings()
    same("periodic settings, raw", S["per_raw"], c["periodic_raw_including_skipped"])
    same("periodic settings, valid", len(S["per_cov"]) + len(S["per_res"]), c["periodic_valid"])
    same("periodic, broken block touches no crib (EP-0169)", len(S["per_cov"]), c["periodic_covered_by_EP-0169_equivalence"])
    same("periodic residual", len(S["per_res"]), c["periodic_residual"])
    same("periodic residual by d", {f"{d:+d}": sum(1 for lab, _ in S["per_res"] if lab[3] == d) for d in K.F3D_DS},
         c["periodic_residual_by_d"])
    same("full text", len(S["full"]), c["full_text"])
    same("W segments", len(S["seg"]), c["W_segment"])
    raw = len(S["per_res"]) + len(S["full"]) + len(S["seg"])
    M = K.f3d_structures(S)
    same("main column, raw settings", raw, c["main_raw"])
    same("main column, distinct crib-block structures", len(M), c["main_distinct_structures"])
    first = {}
    for labs in M.values():
        first[labs[0][0]] = first.get(labs[0][0], 0) + 1
    same("distinct structures by first label", first, c["main_distinct_by_first_label"])
    same("W segments, distinct within the group", len({k for _, k in S["seg"]}), c["W_segment_distinct_within_group"])
    same("W segments, no lost / junk letter in a crib block",
         sum(1 for _, k in S["seg"] if all(K.contiguous(b) for b in k)),
         c["W_segment_with_no_lost_or_junk_letter_in_a_crib_block"])
    check("bits, raw", log2(raw), c["main_raw_bits"], rel=0.001)
    check("bits, distinct", log2(len(M)), c["main_distinct_bits"], rel=0.001)
    cons = [K.edge_constraints(s) for s in K.EDGE_SYSTEMS]
    same("edge systems", len(K.EDGE_SYSTEMS), c["edge_systems"])
    same("edge systems with distinct constraints", len(set(cons)), c["edge_systems_distinct_constraints"])
    same("crib-internal pairs per edge system", sorted({len(f) for f, _ in cons}), [c["edge_crib_internal_pairs_per_system"]])
    same("free Four-square edge settings (12 x 40)", 12 * c["edge_free_four_square_plain_squares"],
         c["edge_free_four_square_settings"])
    same("keyword edge settings (12 x 298,090)", 12 * c["edge_keyword_cipher_settings_per_system"],
         c["edge_keyword_settings"])
    nl = r["null_before_K4"]
    up = 1 - 0.05 ** (1 / nl["shuffles"])
    print(f"  null: main 0/{nl['shuffles']} -> E 0, one-sided 95% upper bound {up:.4f} (recorded {nl['main_E_upper95']}); "
          f"free Four-square edge {nl['fs_edge_shuffles_with_a_consistent_setting']}/{nl['shuffles']} = "
          f"{nl['fs_edge_shuffles_with_a_consistent_setting'] / nl['shuffles']}")
    if (nl["main_shuffles_with_a_consistent_structure"] != 0 or abs(up - nl["main_E_upper95"]) > 0.001
            or nl["fs_edge_shuffles_with_a_consistent_setting"] / nl["shuffles"] != nl["fs_edge_E"]
            or max(nl["main_E"], nl["fs_edge_E"], nl["kw_edge_E"]) > 0.05
            or set(nl["decision"].values()) != {"K4"}):
        bad.append("EP-0211 null gate")
    k4 = r["K4"]
    if (sum(k4["main_by_group_raw"].values()) != raw or k4["main_distinct"] != len(M)
            or k4["fs_edge_total"] != c["edge_free_four_square_settings"] or k4["kw_edge_total"] != c["edge_keyword_settings"]
            or k4["main_consistent"] or k4["main_undetermined"] or k4["fs_edge_consistent"] or k4["kw_edge_hits"]):
        bad.append("EP-0211 recorded K4")
    p_fs = 1 - nl["fs_edge_shuffles_with_a_consistent_setting"] / nl["shuffles"]
    if abs(p_fs - r["P_null_le_K4"]["fs_edge"]) > 1e-9:
        bad.append("EP-0211 P")
    print(f"  recorded K4: main {k4['main_consistent']}/{k4['main_distinct']} structures (groups sum to "
          f"{sum(k4['main_by_group_raw'].values())} raw), free Four-square edge {k4['fs_edge_consistent']}/"
          f"{k4['fs_edge_total']}, keyword edge {k4['kw_edge_hits']}/{k4['kw_edge_total']:,}; P(null <= K4) for the "
          f"free Four-square edge 1 - {nl['fs_edge_shuffles_with_a_consistent_setting']}/{nl['shuffles']} = {p_fs:.2f}")

    print("  -- 2026-10-10 addendum: EP-0215 (Enigma + sigma, machine-step shift d between the cribs)")
    r = rec["EP-0215 Enigma + sigma with a machine-step shift between the cribs"]
    print(f"  crib letter multiplicities: {K.crib_group_sizes()} (13 letters, 24 positions)")
    cp = r["chance_per_setting"]
    P = [K.chance_drop_le(h) for h in range(3)]
    check("chance per setting, h = 0", P[0], cp["h0"], rel=0.002)
    check("chance per setting, h <= 1", P[1], cp["h_le_1"], rel=0.002)
    check("chance per setting, h <= 2", P[2], cp["h_le_2"], rel=0.002)
    fam = r["families"]
    ncol = {f: K.enigma_settings_per_column(fam[f]["machine_count"]) for f in fam}
    for f in fam:
        same(f"settings per column, {f}", ncol[f], r["settings_per_column"][f])
    ntot = sum(r["readings"] * ncol[f] * len(fam[f]["threshold"]) for f in fam)
    same("registered columns", sum(r["readings"] * len(fam[f]["threshold"]) for f in fam), r["registered_columns"])
    same("registered N", ntot, r["N_registered"])
    check("registered N, bits", log2(ntot), r["N_bits"], rel=0.001)
    E = {}
    for f in fam:
        E[f] = {d: r["readings"] * ncol[f] * P[h] for d, h in fam[f]["threshold"].items()}
        for d in ("-2", "-1", "+1", "+2"):
            check(f"E {f} d {d} (h <= {fam[f]['threshold'][d]})", E[f][d], r["E_by_d"][f][d], rel=0.003)
        check(f"E {f} total", sum(E[f].values()), r["E_by_d"][f]["total"], rel=0.003)
    etot = sum(sum(v.values()) for v in E.values())
    check("E registered total", etot, r["E_registered_total"], rel=0.003)
    eun = sum(E["R1-1"].values()) + 4 * r["readings"] * ncol["R2-6"] * P[2]
    check("E of the unadjusted plan (R2-6 h <= 2 at every d)", eun, r["E_unadjusted_plan"], rel=0.003)
    if not (eun > 0.05 >= etot):
        bad.append("EP-0215 allocation rule")
    check("chance of 0 passes, exp(-E)", 2.718281828459045 ** -etot, r["chance_of_zero_passes"], rel=0.002)
    e2 = 4 * r["readings"] * ncol["R1-1"] * P[2]
    check("E of R1-1 at h <= 2 (not registered)", e2, r["E_R1-1_h_le_2_not_registered"]["value"], rel=0.01)
    k4 = r["K4"]
    ok = True
    for f in fam:
        mh = k4["min_h"][f]
        ok &= len(mh) == 15 and k4["registered_passes"][f] == 0
        ok &= all(mh[f"{rd}|{d}"] > fam[f]["threshold"][d] for rd in ("QW", "QWi", "id") for d in fam[f]["threshold"])
        ok &= min(mh[f"{rd}|{d}"] for rd in ("QW", "QWi", "id") for d in fam[f]["threshold"]) == \
            k4["family_min_h_registered_columns"][f]
    ok &= sum(len(k4["min_h"][f]) for f in fam) == r["all_columns_including_d0_regression"]
    ok &= (min(min(v.values()) for v in k4["min_h"].values()) > 2) == (k4["settings_with_h_le_2_in_any_of_30_columns"] == 0)
    nu = r["null"]
    pool = nu["R1-1"]["pooled_min_h"]
    p3 = pool["3"] / sum(pool.values())
    fm = nu["R2-6"]["family_min_h_null"]
    pf = sum(v for h, v in fm.items() if int(h) <= k4["family_min_h_registered_columns"]["R2-6"]) / nu["R2-6"]["shuffles"]
    ok &= abs(p3 - nu["R1-1"]["P_column_min_h"]["h=3 columns"]) < 0.005 and abs(pf - nu["R2-6"]["P_family_min_h"]) < 1e-9
    ok &= sum(fm.values()) == nu["R2-6"]["shuffles"] and nu["R1-1"]["registered_passes"] == nu["R2-6"]["registered_passes"] == 0
    if not ok:
        bad.append("EP-0215 recorded K4 / null")
    print(f"  null: registered passes 0 in {nu['R2-6']['shuffles']} + {nu['R1-1']['shuffles']} shuffles; Enigma I h = 3 "
          f"columns P = {pool['3']}/{sum(pool.values())} = {p3:.2f}; commercial family minimum P = {pf:.2f}")
    lo = min(min(v.values()) for v in k4["min_h"].values())
    hi = max(max(v.values()) for v in k4["min_h"].values())
    print(f"  recorded K4: registered passes {k4['registered_passes']}; every registered column's min h exceeds its "
          f"threshold; min h over all 30 columns {lo}-{hi} (none <= 2); family minima {k4['family_min_h_registered_columns']}")


if __name__ == "__main__":
    sys.exit(main())
