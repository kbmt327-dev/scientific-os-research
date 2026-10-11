"""Recompute the cheap parts of the fixed-row-lists Note (EP-0196, EP-0197, EP-0198, EP-0208) and check the record.

    python verify_fixed_row_lists.py          # numpy, about 10 s

Recomputed: the setting counts N and their bits from the list sizes, the closed-form chance of a false pass
E(h <= 2) = N x sum_{j<=2} C(24, j) 25^j / 26^24, K4's index of coincidence, the EP-0208 duplicate pairs (|W| divides p)
from the list sizes alone, the null shares and P values from the recorded null histograms, the crib-free IC check's
group counts from the recorded group quantiles, and the selection-free cover bound.  On the 8 lists this site can
publish (336 of the 662 rows) it reruns the K4 crib test of EP-0196, EP-0197 and EP-0208 and compares the minimum h
of every (rule, list) group with the record; planted texts (random letters with the cribs) check the sweep.
    Recorded, not rerun: four omitted source-derived lists, EP-0198, null generation, planted controls, and IC checks.
A rerun of the author's method, not an independent replication.  No decryption is printed.
"""
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

import k4_fixed_rows as F

HERE = Path(__file__).resolve().parent
REC = json.loads((HERE / "results" / "fixed-row-lists-20261010.json").read_text(encoding="utf-8"))
DATA = json.loads((HERE / "data" / "public-row-lists.json").read_text(encoding="utf-8"))["lists"]
bad = []


def check(ok, what):
    if not ok:
        bad.append(what)
    return ok


def P_le(k, n=24):
    return sum(math.comb(n, j) * 25 ** j for j in range(k + 1)) / 26 ** n


def close(a, b, rel=0.05):
    return abs(a - b) <= rel * abs(b)


def share_le(hist, k):
    tot = sum(hist.values())
    return sum(v for h, v in hist.items() if int(h) <= k) / tot


def mean_of(hist):
    return sum(int(h) * v for h, v in hist.items()) / sum(hist.values())


def counts_part():
    L = REC["lists"]["sizes"]
    W = sum(L.values())
    print(f"Lists: 12, sum |W| = {W} (record {REC['lists']['sum']}); omitted source rows "
          f"{sum(L[k] for k in REC['lists']['withheld'])}, published here {sum(len(v['words']) for v in DATA.values())}")
    check(W == 662 and {k: len(v["words"]) for k, v in DATA.items()} == {k: L[k] for k in DATA}, "list sizes")
    r6, r7, r8, r9 = REC["ep0196"], REC["ep0197"], REC["ep0198"], REC["ep0208"]
    n6 = 2 * W * 29 * 2 * 6
    n7 = 6 * W * 29 * 2
    n8 = 33 * 2 * 2 * W * 29 * 2
    n8a = 2 * 2 * 2 * W * 29 * 2
    print(f"EP-0196  N = 2 x {W} x 29 x 2 x 6 = {n6:,}; x 16 outer offsets = {16 * n6:,} "
          f"({math.log2(16 * n6):.1f} bit); record {r6['N_main']:,} / {r6['N_all']:,}")
    print(f"EP-0197  N = 6 x {W} x 29 x 2 = {n7:,} ({math.log2(n7):.1f} bit); record {r7['N']:,}")
    print(f"EP-0198  N = 33 x 2 x 2 x {W} x 29 x 2 = {n8:,} ({math.log2(n8):.1f} bit); "
          f"wobble 2 x 2 x 2 x {W} x 29 x 2 = {n8a:,}; record {r8['N_main']:,} / {r8['N_aux']:,}")
    check((n6, 16 * n6, n7, n8, n8a) == (r6["N_main"], r6["N_all"], r7["N"], r8["N_main"], r8["N_aux"]), "N")
    # EP-0208: duplicates (|W| divides p) from the sizes alone
    dup = {k: [p for p in F.BAND if p % n == 0] for k, n in L.items()}
    dup = {k: v for k, v in dup.items() if v}
    pairs = sum(len(v) for v in dup.values())
    dset = sum(L[k] * 58 for k, v in dup.items() for p in v)
    d1 = sum(L[k] * 58 for k, v in dup.items() for p in v if p in F.LAYER1)
    nl1 = len(F.LAYER1) * W * 58 - d1
    nl2 = (len(F.BAND) - len(F.LAYER1)) * W * 58 - (dset - d1)
    print(f"EP-0208  band {len(F.BAND)} periods; |W| divides p in {pairs} (list, p) pairs: {dup}")
    print(f"         excluded settings {dset:,} (layer 1 {d1}, layer 2 {dset - d1:,}); "
          f"layer 1 N = {nl1:,} ({math.log2(nl1):.2f} bit), layer 2 N = {nl2:,} ({math.log2(nl2):.2f} bit); "
          f"record {r9['N']['L1']:,} / {r9['N']['L2']:,} / {r9['N']['dup_excluded']:,}")
    check((nl1, nl2, dset, d1) == (r9["N"]["L1"], r9["N"]["L2"], r9["N"]["dup_excluded"], r9["N"]["dup_L1"]), "EP-0208 N")
    check(dup == r9["dup_pairs_recorded_in_count_log"], "EP-0208 duplicate pairs")
    if pairs != r9["dup_pairs_stated_in_record"]:
        print(f"         note: the record's prose says {r9['dup_pairs_stated_in_record']} pairs; "
              f"the sizes give {pairs} (the excluded setting count {dset:,} agrees)")
    # closed-form E
    p2 = P_le(2)
    rows = [("EP-0196", 16 * n6, r6["E_recorded"]["h<=2"]), ("EP-0197", n7, r7["E_recorded"]["h<=2"]),
            ("EP-0198", n8, r8["E_recorded"]["h<=2"]), ("EP-0208 L1", nl1, r9["E_recorded"]["L1 h<=2"]),
            ("EP-0208 L2", nl2, r9["E_recorded"]["L2 h<=2"])]
    print(f"Closed form: P(h <= 2) per setting = sum_j<=2 C(24,j) 25^j / 26^24 = {p2:.3e}")
    for name, n, e in rows:
        print(f"  {name:<11} E(h <= 2) = {n * p2:.2e}  (record {e:.1e})")
        check(close(n * p2, e), f"E {name}")
    e3, e4 = 16 * n6 * P_le(3), 16 * n6 * P_le(4)
    print(f"  EP-0196     E(h <= 3) = {e3:.2e}, E(h <= 4) = {e4:.2e}  (record 2.6e-20, 3.4e-18)")
    check(close(e3, 2.6e-20) and close(e4, 3.4e-18), "E 0196 tails")
    # EP-0198: rule (a) drops blank crib positions (counted as matches), so those settings test fewer positions
    blanks = {"0": 33 - 15, "1": 13, "2": 2}
    per_geo = n8 // 33 // 2                                # settings per (geometry, blank rule)
    e8a = per_geo * (33 * p2 + blanks["0"] * p2 + blanks["1"] * P_le(2, 23) + blanks["2"] * P_le(2, 22))
    print(f"  EP-0198     with blank crib positions under rule (a) (18 geometries 0, 13 one, 2 two): "
          f"E(h <= 2) = {e8a:.1e}")
    check(sum(len(v) if "9 geometries" not in k else 9 for k, v in r8["blank_crib_positions"].items()) == 13 + 2 * 2,
          "EP-0198 blank positions")
    aux = n8a * sum(math.comb(24, t) * (23 / 26) ** t * (3 / 26) ** (24 - t) for t in range(3))
    print(f"  EP-0198     wobble upper bound E(h_w <= 2) <= {aux:.1e}  (record {r8['E_recorded']['aux_upper_h_w<=2']:.1e})")
    check(close(aux, r8["E_recorded"]["aux_upper_h_w<=2"]), "E 0198 aux")
    # m5 share in EP-0208
    m5 = {k: r9["N"][k] * 25 // 29 for k in ("L1", "L2")}
    print(f"EP-0208  m5 settings (25 of 29 readings, {25 / 29:.1%}): {m5['L1']:,} / {m5['L2']:,} "
          f"(record {r9['diagnostics_outside_rules']['m5_settings']})")
    check(m5 == r9["diagnostics_outside_rules"]["m5_settings"], "m5 share")


def ic(s):
    c = Counter(s)
    return sum(v * (v - 1) for v in c.values()) / (len(s) * (len(s) - 1))


def record_part():
    r6, r7, r8, r9 = REC["ep0196"], REC["ep0197"], REC["ep0198"], REC["ep0208"]
    k4ic = ic(F.K4)
    print(f"K4 index of coincidence {k4ic:.4f} (record {r6['ic_check']['k4_ic']:.4f})")
    check(abs(k4ic - r6["ic_check"]["k4_ic"]) < 1e-4, "K4 IC")
    for name, r, exp, sub in (("EP-0196", r6, 24, None), ("EP-0197", r7, 27, "excluded_by_line"),
                              ("EP-0198", r8, 17, "excluded_by_type")):
        g = r["ic_check"]["groups"]
        ex = [k for k, v in g.items() if k4ic < v["q01"]]
        med = [v["median"] for v in g.values()]
        line = f"  IC check {name}: K4 below the family's 1% quantile in {len(ex)}/{len(g)} groups (record {exp}); " \
               f"family median IC {min(med):.3f}-{max(med):.3f}"
        if sub:
            by = Counter(k.split("/")[0] for k in ex)
            line += f"; by {sub.split('_')[-1]} {dict(by)}"
            check(dict(by) == r["ic_check"][sub], f"IC {name} split")
        print(line)
        check(len(ex) == exp == r["ic_check"]["excluded"], f"IC {name}")
    # minima, counts, nulls
    k6, k7, k8 = r6["k4"], r7["k4"], r8["k4"]
    check(min(k6["per_group_min"].values()) == k6["min_all"] == 16 and k6["min_main"] == 17, "0196 minima")
    check(min(k7["per_group_min"].values()) == k7["min"] == 17, "0197 minima")
    check(min(k8["per_group_min"].values()) == k8["min"] == 14 and k8["min_aux"] == 12, "0198 minima")
    l1, l2 = r9["k4"]["L1"], r9["k4"]["L2"]
    check(sum(l1["hist"]) == r9["N"]["L1"] and sum(l2["hist"]) == r9["N"]["L2"], "0208 histogram totals")
    check(l1["min"] == 18 and l2["min"] == 16 and sum(l1["hist"][:3]) + sum(l2["hist"][:3]) == 0, "0208 minima")
    passes = sum(k6["count_h_le_k_all"][:3]) + sum(k7["count_h_le_k"][:3]) + sum(k8["count_h_le_k"][:3]) + \
        sum(k8["count_aux_h_le_k"][:3])
    print(f"Recorded K4 minima: EP-0196 {k6['min_all']} (o = (0,0): {k6['min_main']}), EP-0197 {k7['min']}, "
          f"EP-0198 {k8['min']} (wobble {k8['min_aux']}), EP-0208 layer 1 {l1['min']}, layer 2 {l2['min']}; "
          f"settings with h <= 2: {passes}")
    check(passes == 0, "passes")
    nl = [("EP-0196 all", r6["null"]["min_all_hist"], 16, r6["null"]["share_le_k4_all"]),
          ("EP-0196 o=(0,0)", r6["null"]["min_main_hist"], 17, r6["null"]["share_le_k4_main"]),
          ("EP-0197", r7["null"]["min_hist"], 17, r7["null"]["share_le_k4"]),
          ("EP-0198 main", r8["null"]["min_hist"], 14, r8["null"]["share_le_k4"]),
          ("EP-0198 wobble", r8["null"]["min_aux_hist"], 12, r8["null"]["share_le_k4_aux"])]
    for name, h, k, rec in nl:
        s = share_le(h, k)
        print(f"  null {name:<16} 2,000 shuffles, min h {min(map(int, h))}-{max(map(int, h))} "
              f"(mean {mean_of(h):.2f}); share <= K4's {k}: {s:.1%} (record {rec:.1%})")
        check(sum(h.values()) == 2000 and abs(s - rec) < 0.0006, f"null {name}")
    for lay, k in (("L1", 18), ("L2", 16)):
        mins = r9["null"]["shuffle_mins"][lay]
        P = sum(m <= k for m in mins) / len(mins)
        print(f"  null EP-0208 {lay}: 20 shuffles, min h {min(mins)}-{max(mins)}; P = #(<= {k})/20 = {P:.2f} "
              f"(record {r9['null']['P'][lay]:.2f})")
        check(abs(P - r9["null"]["P"][lay]) < 1e-9, f"P {lay}")
    self_enc = [int(p) for p in F.POS if F.K4[p] == F.CRIB[p]]
    print(f"Crib positions where K4's letter equals the crib letter: {self_enc} "
          f"(record {r9['diagnostics_outside_rules']['self_encrypted_crib_positions']})")
    check(self_enc == r9["diagnostics_outside_rules"]["self_encrypted_crib_positions"], "self-encryptions")


def rerun_part():
    TAB = {k: F.tables(v["words"]) for k, v in DATA.items()}
    rng = random.Random(1960)
    ok = True
    for _ in range(300):
        k = rng.choice(list(DATA))
        w = DATA[k]["words"]
        r, m, x = rng.randrange(len(w)), rng.randrange(29), rng.randrange(26)
        ok &= F.AZ[TAB[k][m, r, x]] == F.naive_letter(w[r], F.AZ[x], m)
    fixed = sum(int((T[4:, :, :] == np.arange(26)[None, None, :]).sum()) for T in TAB.values())
    print(f"Public lists ({sum(len(v['words']) for v in DATA.values())} rows): tables == string reference on 300 "
          f"random cells {ok}; m5 cells with C = P: {fixed}")
    check(ok and fixed == 0, "tables")
    C4 = F.crib_vec(F.K4)[None, :]
    cb = REC["cover_bound_computed_for_this_note"]
    cov = {k: F.cover_bound(T, C4[0]) for k, T in TAB.items()}
    cova = {k: min(F.cover_bound(T, C4[0], X) for X in ((66, 67), (66,), (65,))) for k, T in TAB.items()}
    print(f"Selection-free cover bound on K4 (crib letters no row can give, best reading): {cov}")
    print(f"  with EP-0198's blank positions dropped: min {min(cova.values())}; record includes {len(REC['lists']['withheld'])} omitted lists")
    check(all(cov[k] == cb["bound_per_list"][k] and cova[k] == cb["bound_per_list_with_ep0198_blank_rule_a"][k]
              for k in TAB), "cover bound")
    allb = list(cb["bound_per_list"].values())
    print(f"  -> over all 12 lists every setting of every row rule has h >= {min(allb)} "
          f"(EP-0198 rule (a): >= {min(cb['bound_per_list_with_ep0198_blank_rule_a'].values())}): "
          f"no pass (h <= 2) was possible on these lists")
    check(min(allb) >= 3 and min(cb["bound_per_list_with_ep0198_blank_rule_a"].values()) >= 3, "forced bound")

    def plants(fam, nplant=3):
        """random letters with the cribs, encrypted by the string reference under random settings"""
        out = []
        for _ in range(nplant):
            k = rng.choice(list(DATA))
            w = DATA[k]["words"]
            P = [rng.choice(F.AZ) for _ in range(97)]
            for i, ch in F.CRIB.items():
                P[i] = ch
            f = fam(k)
            out.append((k, F.crib_vec(F.naive_encrypt("".join(P), w, f, rng.randrange(len(w)),
                                                       rng.choice((1, -1)), rng.randrange(29)))))
        return out

    # EP-0196
    rec = REC["ep0196"]["k4"]["per_group_min"]
    vec = {m: [J for _, J in F.wordpos_vectors(m)] for m in ("head", "end")}
    got, diff = {}, []
    for mode in ("head", "end"):
        for k, T in TAB.items():
            got["%s/%s" % (mode, k)] = int(F.min_h(T, vec[mode], C4)[0])
            if got["%s/%s" % (mode, k)] != rec["%s/%s" % (mode, k)]:
                diff.append("%s/%s" % (mode, k))
    # a planted text needs the full 97-position j-vector; use word breaks of length 5 outside the cribs
    full = {}
    for mode in ("head", "end"):
        st = sorted({0, 5, 10, 15, 21, 25, 34, 39, 44, 49, 54, 59, 63, 69, 74, 79, 84, 89, 94})
        f = np.empty(97, dtype=int)
        for q, s in enumerate(st):
            e = st[q + 1] - 1 if q + 1 < len(st) else 96
            for i in range(s, e + 1):
                f[i] = i - s if mode == "head" else e - i
        full[mode] = f
    pl = [(k, c) for mode in ("head", "end") for k, c in plants(lambda k, m=mode: full[m], 2)]
    pmin = [int(F.min_h(TAB[k], vec[m], c[None, :])[0]) for (k, c), m in zip(pl, ("head", "head", "end", "end"))]
    print(f"EP-0196 rerun on the public lists ({len(got)} groups x 96 j-vectors x 2 dir x 29 x |W|): min h "
          f"{min(got.values())}; groups equal to the record {len(got) - len(diff)}/{len(got)}; "
          f"planted texts recovered with h = 0: {pmin.count(0)}/{len(pmin)}")
    check(not diff and pmin.count(0) == len(pmin), f"EP-0196 rerun {diff}")
    # EP-0197
    rec = REC["ep0197"]["k4"]["per_group_min"]
    got, diff = {}, []
    for rk, starts in F.RESTARTS.items():
        f = F.fold_phase(starts)
        for k, T in TAB.items():
            got["%s/%s" % (rk, k)] = int(F.min_h(T, [f[F.POS]], C4)[0])
            if got["%s/%s" % (rk, k)] != rec["%s/%s" % (rk, k)]:
                diff.append("%s/%s" % (rk, k))
    rk0 = list(F.RESTARTS)
    pl = []
    for t in range(4):
        f = F.fold_phase(F.RESTARTS[rk0[t]])
        pl += [(k, c, f) for k, c in plants(lambda k, f=f: f, 1)]
    pmin = [int(F.min_h(TAB[k], [f[F.POS]], c[None, :])[0]) for k, c, f in pl]
    print(f"EP-0197 rerun on the public lists ({len(got)} groups): min h {min(got.values())}; groups equal to the "
          f"record {len(got) - len(diff)}/{len(got)}; planted texts recovered with h = 0: {pmin.count(0)}/{len(pmin)}")
    check(not diff and pmin.count(0) == len(pmin), f"EP-0197 rerun {diff}")
    # EP-0208
    rec = REC["ep0208"]["k4_per_group_min"]
    got, diff = {}, []
    for k, T in TAB.items():
        n = T.shape[1]
        cols = {"L1": [p for p in F.LAYER1 if p % n], "L2": [p for p in F.BAND if p not in F.LAYER1 and p % n],
                "dup": [p for p in F.BAND if p % n == 0]}
        for lay, ps in cols.items():
            if ps:
                got["%s %s" % (lay, k)] = int(F.min_h(T, [F.POS % p for p in ps], C4)[0])
        got["ref %s" % k] = int(F.min_h(T, [F.POS], C4)[0])
    for key, v in got.items():
        if rec.get(key) != v:
            diff.append(key)
    pl = []
    for p in (28, 26, 58, 71):
        pl += [(k, c, p) for k, c in plants(lambda k, p=p: np.arange(97) % p, 1)]
    pmin = [int(F.min_h(TAB[k], [F.POS % p], c[None, :])[0]) for k, c, p in pl]
    l1 = min(v for key, v in got.items() if key.startswith("L1"))
    l2 = min(v for key, v in got.items() if key.startswith("L2"))
    print(f"EP-0208 rerun on the public lists ({len(got)} groups incl. duplicates and the period-free walk): "
          f"min h layer 1 {l1}, layer 2 {l2}; groups equal to the record {len(got) - len(diff)}/{len(got)}; "
          f"planted texts recovered with h = 0: {pmin.count(0)}/{len(pmin)}")
    check(not diff and pmin.count(0) == len(pmin), f"EP-0208 rerun {diff}")


def main():
    counts_part()
    record_part()
    rerun_part()
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: counts, closed forms and the record are consistent; the public-list rerun matches every recorded "
          "group minimum; no setting can reach h <= 2 on these lists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
