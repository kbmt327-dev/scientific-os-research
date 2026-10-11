"""Recompute the cheap parts of the public-machines Note (EP-0193 T2, EP-0203, EP-0206, EP-0207, EP-0209, EP-0215)
and compare with the record.

    python verify_public_machines.py      # numpy + standard library, about 10 s

Rerun here: the devices (Enigma I test vectors through two stepping models, the 676 stepping classes, every machine
position a fixed-point-free involution, the QW / QWi entry readings), the exact sigma test on planted texts and on K4
in small slices (with the EP-0209 lesson: a plant made under one entry reading is invisible under the other), the
closed-form chance values and setting counts of every family, and on K4 the forced positions under the 104 layout
transpositions (R4 at Pi = id, the Pi that return S and K to 32 and 73, f >= 3, the five Pi that always fail on the
M-94, the sieve).  Recorded, not rerun: the full GPU / CPU sweeps, the nulls and the confirmation statistic.
Only counts and statistics are printed; no decryption of K4 and no planted text.
A rerun of the author's method, not an independent replication.
"""
import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

import k4_public_machines as M

HERE = Path(__file__).resolve().parent


def close(a, b, rel=0.006):
    return math.isclose(float(a), float(b), rel_tol=rel)


def sig(x, n=3):
    return float(f"{float(x):.{n}g}")


def p_of(k4, nulls):
    return sum(v <= k4 for v in nulls) / len(nulls)


def expand(d):
    return [int(k) for k, v in d.items() for _ in range(v)]


def devices(bad):
    tv = M.test_vectors()
    ok = tv == [("BDZGO", "BDZGO"), ("EQIB", "EQIB")]
    print(f"Enigma I (I-II-III, reflector B, rings A): AAA+AAAAA -> {tv[0][0]}, ADU+AAAA -> {tv[1][0]} "
          f"(abstract and real stepping agree: {ok})")
    if not ok:
        bad.append("test vectors")
    nR, nM = M.AZ.index("V"), M.AZ.index("E")
    agree = 0
    for phR in range(26):
        for phM in range(26):
            win = (7, (phM + nM) % 26, (phR + nR) % 26)
            real = M.real_steps(win, (nM, nR), 97)
            abst = [((win[0] + a) % 26, (win[1] + b) % 26, (win[2] + c) % 26) for a, b, c in M.steps(phR, phM, 97)]
            agree += real == abst
    print(f"  stepping: real lever/pawl machine == (offsets, phR, phM) model in {agree}/676 classes (97 letters each)")
    if agree != 676:
        bad.append("stepping classes")
    W = M.PUBLIC_WIRINGS
    refl = {m[3] for m in M.MACHINES.values()}
    inv_ok = all(all(u[M.AZ.index(u[x])] == M.AZ[x] and u[x] != M.AZ[x] for x in range(26)) for u in refl)
    print(f"  wirings: {len(set(W))} distinct public rotor wirings, {len(M.MACHINES)} machines "
          f"(3 commercial + 30 Enigma I), {len(refl)} distinct reflectors, all fixed-point-free involutions: {inv_ok}")
    if len(set(W)) != 14 or len(M.MACHINES) != 33 or len(refl) != 5 or not inv_ok:
        bad.append("wirings")
    rng = random.Random(2061)
    names = list(M.MACHINES)
    good = tot = 0
    x = np.arange(26)
    for name in names:
        for reading in M.READINGS:
            mach = M.Machine(name, M.ORDERS[rng.randrange(6)], reading)
            oL, oM, oR, uq, phR, phM = (rng.randrange(26) for _ in range(6))
            for sL, sM, sR in M.steps(phR, phM, 97):
                f = mach.letter(x, (oL + sL) % 26, (oM + sM) % 26, (oR + sR) % 26, uq)
                good += bool(np.all(f[f] == x) and np.all(f != x))
                tot += 1
    print(f"  every position a fixed-point-free involution: {good}/{tot} (33 machines x 3 readings x 97 letters)")
    if good != tot:
        bad.append("involutions")
    QW, QWi = M.READINGS["QW"], M.READINGS["QWi"]
    inverse = bool(np.all(QW[QWi] == np.arange(26)) and np.all(QWi[QW] == np.arange(26)))
    agree = int(np.sum(QW == QWi))
    shift = [c for c in range(26) if np.all((QWi + c) % 26 == QW)]
    keyq = QW[M.AZ.index("Q")] == 0 and np.array_equal(QWi, M.perm(M.QWERTZ))
    print(f"  entry readings: QW and QWi mutual inverses {inverse}; letters where they agree {agree} of 26; "
          f"contact shifts mapping QWi to QW: {len(shift)}; QW has key Q at contact A and QWi is EP-0132's table: {keyq}")
    if not (inverse and agree == 3 and not shift and keyq):
        bad.append("entry readings")


def plant(rng, reading):
    """random letters with the cribs written in, a random sigma and setting; returns ciphertext and setting.
    The planted text is never printed or stored."""
    P = [rng.randrange(26) for _ in range(97)]
    for i, ch in M.CRIB.items():
        P[i] = M.AZ.index(ch)
    sig_ = list(range(26))
    rng.shuffle(sig_)
    name = rng.choice(list(M.MACHINES))
    order = M.ORDERS[rng.randrange(6)]
    oL, oM, oR, uq, phR, phM = (rng.randrange(26) for _ in range(6))
    C = M.encipher(M.Machine(name, order, reading), [sig_[p] for p in P], oL, oM, oR, uq, phR, phM)
    return "".join(M.AZ[c] for c in C), (name, order, oL, oM, oR, uq, phR, phM)


def sigma_test(rec, bad):
    rng = random.Random(2091)
    n = 10
    same = cross = k4 = cross_n = 0
    for _ in range(n):
        for built in ("QW", "QWi"):
            ct, (name, order, oL, oM, oR, uq, phR, phM) = plant(rng, built)
            npass, hits = M.slice_scan(M.Machine(name, order, built), ct, phR, phM, oL0=oL)
            same += (oL, oM, oR, uq) in hits
            if built == "QW":
                npass2, _ = M.slice_scan(M.Machine(name, order, "QWi"), ct, phR, phM, oL0=oL)
                cross += npass2 == 0
                cross_n += 1
            for reading in M.READINGS:
                k4 += M.slice_scan(M.Machine(name, order, reading), M.K4, phR, phM, oL0=oL)[0]
    print(f"Exact sigma test (EP-0132 rule) in slices of 26^3 settings (oM, oR, uq) around each planted setting:")
    print(f"  plants scanned under the reading they were made with: true setting found {same}/{2 * n}")
    print(f"  plants made under QW, scanned under QWi: slices with no pass at all {cross}/{cross_n} "
          f"(EP-0209: the same code that plants and searches cannot see a wrong entry reading)")
    print(f"  K4 in the same {2 * n} slices x 3 readings ({2 * n * 3 * 26 ** 3:,} settings): passes {k4}")
    if same != 2 * n or cross != cross_n or k4 != 0:
        bad.append("sigma test")


def closed_forms(rec, bad):
    mult = M.crib_multiplicities()
    p0 = M.p_sigma_uniform()
    p1, p2 = M.p_sigma_le(1), M.p_sigma_le(2)
    print(f"Closed forms: crib letters {len(mult)} groups, multiplicities {dict(sorted(mult.items()))}")
    print(f"  P(sigma pass | random) per setting = 26^-11 x prod(1 - k/26, k < 13) = {float(p0):.4g}; "
          f"union bound P(d* <= 1) {float(p1):.4g}, P(d* <= 2) {float(p2):.4g}")
    if not (close(p0, 7.111780747846230e-18, 1e-9) and close(p1 - p0, 3.7509563601497546e-15, 1e-9)
            and close(p2 - p1, 9.097971066728866e-13, 1e-9)):
        bad.append("sigma closed form")
    r = rec["EP-0193_T2"]
    n193 = 30 * 6 * 2 * 26 ** 4 * 676
    e193 = n193 * p0
    print(f"  EP-0193 T2: N = 30 x 6 x 2 x 26^4 x 676 = {n193:,} ({math.log2(n193):.2f} bit), E = {float(e193):.2g} "
          f"(record {r['expected_chance_passes']:.2g})")
    if n193 != r["settings"]["N"] or sig(e193, 2) != r["expected_chance_passes"]:
        bad.append("EP-0193 T2 counts")
    r = rec["EP-0209"]
    n132q, n193q = 3 * 6 * 26 ** 4 * 676, 30 * 6 * 26 ** 4 * 676
    print(f"  EP-0209: QW rows N {n132q:,} + {n193q:,} = {n132q + n193q:,} ({math.log2(n132q + n193q):.2f} bit); "
          f"E {float(n132q * p0):.3g} + {float(n193q * p0):.3g} = {float((n132q + n193q) * p0):.3g}")
    if (n132q, n193q) != (r["settings"]["EP-0132_QW"], r["settings"]["EP-0193_T2_QW"]) or \
            (sig(n132q * p0), sig(n193q * p0), sig((n132q + n193q) * p0)) != (r["E"]["EP-0132_QW"], r["E"]["EP-0193_T2_QW"], r["E"]["total"]):
        bad.append("EP-0209 counts")
    r = rec["EP-0215"]
    eI = 12 * n193q * p1
    ec1 = 6 * n132q * p2
    ec2 = 6 * n132q * p1
    unadj = 12 * n193q * p1 + 12 * n132q * p2
    n215 = 12 * n193q + 12 * n132q
    print(f"  EP-0215: N = 12 x {n193q:,} + 12 x {n132q:,} = {n215:.3g} ({math.log2(n215):.2f} bit); "
          f"E Enigma I (d* <= 1) {float(eI):.3g} + commercial d = +-1 (d* <= 2) {float(ec1):.3g} + d = +-2 (d* <= 1) "
          f"{float(ec2):.3g} = {float(eI + ec1 + ec2):.4f} (unadjusted budgets {float(unadj):.4f})")
    if n215 != r["settings"]["N"] or not (close(eI, r["E"]["EnigmaI"], 0.01) and close(ec1, r["E"]["commercial_d_pm1"], 0.01)
                                          and close(ec2, r["E"]["commercial_d_pm2"], 0.01)
                                          and close(eI + ec1 + ec2, r["E"]["registered_total"], 0.01)
                                          and close(unadj, r["E"]["unadjusted_total"], 0.01)):
        bad.append("EP-0215 counts")
    r = rec["EP-0203"]["settings"]
    per3 = 14 * 13 * 12 * 6 * 26 ** 3 * (26 * 9 + 1)
    per2 = 14 * 13 * 2 * 26 ** 2 * (26 * 5 + 1)
    prop = 14 * 13 * 12 * 6 * 26 ** 3 * 26 * 10 * 9
    b2 = M.p_mismatch_le(2)
    print(f"  EP-0203: 3 rotors 2,184 triples x 6 paths x 26^3 x 235 (phase, case) = {per3:,} per entry/exit pair; "
          f"main 9 pairs {9 * per3:.3g} ({math.log2(9 * per3):.2f} bit), E(h <= 2) {float(9 * per3 * b2):.3g}; "
          f"2 rotors {9 * per2:,}")
    if (per3, 9 * per3, 16 * per3, prop, per2, 9 * per2) != (r["N3_per_pair"], r["N3_main9"], r["N3_supp16"],
                                                            r["N3_proposal"], r["N2_per_pair"], r["N2_main9"]) or \
            sig(9 * per3 * b2) != rec["EP-0203"]["E_h_le_2"]["N3_main9"] or sig(9 * per2 * b2) != rec["EP-0203"]["E_h_le_2"]["N2_main9"]:
        bad.append("EP-0203 counts")
    r = rec["EP-0206"]
    po = 33 * 6 * 3 * 26 ** 4 * 676
    e = {k: float(208 * po * M.p_mismatch_le(k)) for k in (2, 11, 12)}
    print(f"  EP-0206: per (Pi, order) 33 x 6 x 3 x 26^4 x 676 = {po:,}; x 208 = {208 * po:.4g} "
          f"({math.log2(208 * po):.2f} bit); E(h <= 2) {e[2]:.3g}, E(h <= 11) {e[11]:.3g}, E(h <= 12) {e[12]:.0f}")
    if po != r["settings"]["per_Pi_order"] or 208 * po != r["settings"]["N_208"] or \
            208 * 33 * 6 * 2 * 26 ** 4 * 676 != r["settings"]["N_proposal_id_QWi"] or \
            sig(e[2]) != r["E"]["h_le_2"] or sig(e[11]) != r["E"]["h_le_11"] or round(e[12]) != r["E"]["h_le_12"]:
        bad.append("EP-0206 counts")


def pi_facts(rec, bad):
    ps = M.pis()
    fam = Counter(f for _, f in ps)
    print(f"Layout transpositions: {len(ps)} Pi (sha256 {M.PI_DIGEST[:8]}...{M.PI_DIGEST[-4:]} as committed), "
          f"T1 {fam['T1']}, T2 {fam['T2']}, T4 {fam['T4']}")
    self_enc = [i for i in M.POS if M.K4[i] == M.CRIB[i]]
    fs = [M.forced(M.K4, s) for s, _ in ps]
    both = sum(32 in f and 73 in f for f in fs)
    dist = dict(sorted(Counter(len(f) for f in fs).items()))
    f3 = sum(len(f) >= 3 for f in fs)
    r = rec["EP-0206"]["forced"]
    print(f"  K4 at Pi = id: crib positions where the carved letter equals the crib letter {self_enc} "
          f"(R4: a reflector machine without sigma has h >= 2 there)")
    print(f"  EP-0206: Pi returning S and K to 32 and 73: {both}; 32 forced in {sum(32 in f for f in fs)}, "
          f"73 in {sum(73 in f for f in fs)}; forced-mismatch counts f {dist}; Pi with f >= 3 (cannot reach h <= 2): {f3}")
    if self_enc != r["pi_id"] or both != r["pi_returning_both_S_and_K"] or \
            sum(32 in f for f in fs) != r["pi_with_32_forced"] or sum(73 in f for f in fs) != r["pi_with_73_forced"] or \
            {str(k): v for k, v in dist.items()} != r["f_distribution"] or f3 != r["pi_with_f_ge_3"]:
        bad.append("EP-0206 forced")
    r = rec["EP-0207"]
    forced5 = [k for k, (s, _) in enumerate(ps) if s[32] == 32 or s[73] == 73]
    main = [k for k in range(104) if k not in forced5]
    dead = sum(len(fs[k]) >= 1 for k in main)
    print(f"  EP-0207: Pi that keep position 32 or 73 in place (always fail on the M-94): {forced5}; judged "
          f"{len(main)} x 2 orders = {2 * len(main)}; sieve on K4 (f >= 1): dead {dead}, survive {len(main) - dead} "
          f"per order (random text survival (25/26)^24 = {(25 / 26) ** 24:.3f})")
    if forced5 != r["forced_pi"]["indices"] or 2 * len(main) != r["forced_pi"]["judged_denominator"] or \
            any((c["sieve_dead"], c["survivors"]) != (dead, len(main) - dead) for c in r["K4"][:3]):
        bad.append("EP-0207 forced / sieve")
    W = 26 ** 24
    c = r["counts"]
    vals = {}
    for key, order, sl in (("A_s0", "A", [0]), ("B_s0", "B", [0]), ("A_s_free", "A", range(25)),
                           ("B_s_free_excluded", "B", range(25))):
        n104 = sum(M.m94_count(s, order, sl) for s, _ in ps)
        n99 = sum(M.m94_count(ps[k][0], order, sl) for k in main)
        vals[key] = (n104, n99)
        ok = close(n104, c[key]["N104"], 0.002) and close(n104 / W, c[key]["E0_104"], 0.002) and \
            close(n99 / W, c[key]["E0_99"], 0.002)
        if not ok:
            bad.append(f"EP-0207 {key}")
    mainN = vals["A_s0"][0] + vals["B_s0"][0]
    sensN = vals["A_s_free"][0] + vals["B_s0"][0]
    grid = [sum(sum(25 ** len({((i if o == "A" else M.LP.inverse(list(s))[i]) - q) // 25 for i in M.POS}) for q in sl)
                for s, _ in ps) for o, sl in (("A", [0]), ("B", [0]), ("A", range(25)))]
    print(f"  EP-0207 M-94 counts (N = sum 25^L x 25!/(25-R)!, E0 = N x 26^-24): main {math.log2(mainN):.2f} bit, "
          f"E0 {mainN / W:.3g} (99 Pi: {(vals['A_s0'][1] + vals['B_s0'][1]) / W:.3g}); main + sensitivity "
          f"{math.log2(sensN):.2f} bit, E0 {sensN / W:.3g} (99 Pi: {(vals['A_s_free'][1] + vals['B_s0'][1]) / W:.3g}); "
          f"order B with s free E0 {vals['B_s_free_excluded'][0] / W:.3f}; grids {grid}")
    if round(math.log2(mainN), 2) != c["main"]["log2_104"] or round(math.log2(sensN), 2) != c["main_plus_sensitivity"]["log2_104"] \
            or not close(mainN / W, c["main"]["E0_104"], 0.002) or not close(sensN / W, c["main_plus_sensitivity"]["E0_104"], 0.002) \
            or not close((vals["A_s0"][1] + vals["B_s0"][1]) / W, c["main"]["E0_99"], 0.002) \
            or not close((vals["A_s_free"][1] + vals["B_s0"][1]) / W, c["main_plus_sensitivity"]["E0_99"], 0.002) \
            or grid != [c["grid_A_s0"], c["grid_B_s0"], c["grid_A_s_free"]] \
            or (1 + 24 * 25, 1 + 24 * 25 + math.comb(24, 2) * 625) != (c["factor_e_le_1"], c["factor_e_le_2"]):
        bad.append("EP-0207 counts")
    s2 = r["stage2"]
    rate = s2["hits_e_le_1"] / s2["random_texts"]

    def pois_cdf(k, mu):
        return sum(math.exp(-mu) * mu ** j / math.factorial(j) for j in range(k + 1))

    def solve(f, lo, hi):
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return lo
    k = s2["hits_e_le_1"]
    lo = solve(lambda mu: 1 - pois_cdf(k - 1, mu) < 0.025, 0, 50)
    hi = solve(lambda mu: pois_cdf(k, mu) > 0.025, 0, 50)
    lo198, hi198 = lo / s2["random_texts"] * 198, hi / s2["random_texts"] * 198
    bound = 601 * (vals["A_s0"][1] + vals["B_s0"][1]) / W
    print(f"  EP-0207 stage 2: {k} hits in {s2['random_texts']:,} random texts -> {rate:.2g} per configuration, "
          f"x 198 = {rate * 198:.4f} < 0.05 (exact 95% interval {lo198:.3f}-{hi198:.3f}); closed-form bound "
          f"601 x E0 = {bound:.2f}")
    if not (close(rate * 198, s2["x198"], 0.01) and round(lo198, 3) == s2["interval_95_x198"][0]
            and round(hi198, 3) == s2["interval_95_x198"][1] and round(bound, 2) == s2["closed_form_bound_x198"]):
        bad.append("EP-0207 stage 2")


def record(rec, bad):
    print("Record consistency (P = share of null minima <= K4's minimum):")
    errs = []
    r = rec["EP-0203"]
    for c in r["columns"]:
        if round(p_of(c["K4_min_h"], c["null_min"]), 2) != c["P"]:
            errs.append("EP-0203 " + c["column"])
    print(f"  EP-0203: {len(r['columns'])} columns, P {sorted(c['P'] for c in r['columns'])}, K4 settings with h <= 2: "
          f"{r['K4_settings_h_le_2']}, smallest K4 minimum {min(c['K4_min_h'] for c in r['columns'])}")
    r = rec["EP-0206"]
    cols = r["null_t1id"]["columns"] + r["null_full"]["columns"]
    for c in cols:
        if round(p_of(c["K4_min_h"], c["null_min"]), 2) != c["P"]:
            errs.append("EP-0206 " + c["column"])
    ps = [c["P"] for c in cols]
    if [min(ps), max(ps)] != r["P_range_over_columns"] or r["K4_settings_h_le_2"] != 0 or \
            min(c["min_h"] for c in r["K4"]) != 12 or r["pi_id_check"]["with_32_and_73_mismatched"] != r["pi_id_check"]["settings_h_le_14"]:
        errs.append("EP-0206 summary")
    print(f"  EP-0206: K4 h <= 2: {r['K4_settings_h_le_2']}, smallest minimum {min(c['min_h'] for c in r['K4'])}, "
          f"P {min(ps)}-{max(ps)}; Pi = id: {r['pi_id_check']['with_32_and_73_mismatched']}/{r['pi_id_check']['settings_h_le_14']} "
          f"recorded settings mismatch at both 32 and 73")
    r = rec["EP-0207"]
    for c in r["null"]["columns"]:
        if round(p_of(c["K4_min_e"], c["null_min"]), 2) != c["P_shuffles"] or \
                round(p_of(c["K4_min_e"], expand(c["random_min"])), 2) != c["P_random"]:
            errs.append("EP-0207 " + c["column"])
    for c in r["K4"]:
        if c["sieve_dead"] + c["survivors"] != c["n"]:
            errs.append("EP-0207 sieve sum")
    h = r["sensitivity_hit_metadata"]
    z = (h["confirmation_S_bits"] - h["null_mean"]) / h["null_sd"]
    zen = (h["english_expectation"] - h["confirmation_S_bits"]) / h["null_sd"]
    if h["confirmed"] or h["p"] <= h["threshold"] or r["K4"][2]["passes"] != 1 or \
            any(c["passes"] for c in r["K4"][:2]) or any(c["stage2_hits"] for c in r["K4"][:2]):
        errs.append("EP-0207 verdicts")
    print(f"  EP-0207: main passes {r['K4'][0]['passes']} + {r['K4'][1]['passes']}, stage 2 hits 0; sensitivity: "
          f"{h['settings']} setting remains, confirmation statistic on {h['letters_decided']} letters "
          f"{z:+.1f} sd from the null mean and {zen:.1f} sd below the English expectation, p = {h['p']} -> unconfirmed")
    r = rec["EP-0209"]
    for c in r["diagnostic_d_star"]:
        if round(p_of(c["K4"], expand(c["null_min"])), 2) != c["P"] or sum(c["null_min"].values()) != c["n"]:
            errs.append("EP-0209 " + c["column"])
    if any(r["K4_passes"].values()):
        errs.append("EP-0209 passes")
    print(f"  EP-0209: K4 passes {sum(r['K4_passes'].values())} in 4 rows; minimum d* "
          f"{[c['K4'] for c in r['diagnostic_d_star']]}, P {[c['P'] for c in r['diagnostic_d_star']]}")
    r = rec["EP-0215"]
    cm = r["null"]["commercial"]
    if round(p_of(cm["K4_family_min"], cm["family_min"]), 2) != cm["P_family"] or \
            min(r["K4_min"]["commercial_columns"]) != cm["K4_family_min"] or r["K4_registered_passes"] != 0 or \
            r["K4_any_column_h_le_2"] != 0:
        errs.append("EP-0215 summary")
    ei = r["null"]["EnigmaI"]
    if round(p_of(3, ei["column_min"]), 2) != ei["P_h3_columns"] or p_of(4, ei["column_min"]) != ei["P_h4_columns"]:
        errs.append("EP-0215 Enigma I null")
    print(f"  EP-0215: registered passes 0; minimum d* Enigma I {min(r['K4_min']['EnigmaI_columns'])}-"
          f"{max(r['K4_min']['EnigmaI_columns'])}, commercial {min(r['K4_min']['commercial_columns'])}-"
          f"{max(r['K4_min']['commercial_columns'])}; null P (Enigma I d* = 3 columns) {ei['P_h3_columns']}, "
          f"(commercial family) {cm['P_family']}")
    r = rec["EP-0193_T2"]
    if r["K4_passes"] != 0 or any(r["null"]["passes"]) or r["plants"]["recovered"] != "5/5":
        errs.append("EP-0193 T2")
    print(f"  EP-0193 T2: K4 passes {r['K4_passes']}, plants {r['plants']['recovered']}, "
          f"shuffles with a pass {sum(map(bool, r['null']['passes']))}/{r['null']['n']}")
    if errs:
        bad.append("record: " + ", ".join(errs))


def main():
    rec = json.loads((HERE / "results" / "public-machines-20261010.json").read_text(encoding="utf-8"))
    bad = []
    devices(bad)
    sigma_test(rec, bad)
    closed_forms(rec, bad)
    pi_facts(rec, bad)
    record(rec, bad)
    if bad:
        print("FAIL:", "; ".join(bad))
        return 1
    print("PASS: the devices, the sigma test, the closed forms, the counts and the forced positions reproduce; "
          "the recorded results are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
