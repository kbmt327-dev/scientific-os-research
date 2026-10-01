"""Recompute the cheap parts of the Portax / free-square Playfair Note (EP-0156) and compare with the record.

    python verify_portax_playfair_mask.py      # standard library only, about 10 s

Rerun here: the Portax table against the ACA worked example, its structure (reciprocal, never keeps a letter in
place), the vertical pairs touching the crib for every period P = 1..48, an exact backtracking decider for the
'before' layer (C = Portax(sigma(P))) on K4 at every period with 20 planted texts and 20 shuffles per period, and
for the Playfair part the W-reduced text, the crib pairs of each pairing and the number of m1 / m2 settings.
Recorded, not rerun: the CP-SAT proofs for the 'after' layer and for the free-square Playfair with masks.
A rerun of the author's method, not an independent replication.
"""
import json
import random
import sys
from pathlib import Path

import k4_portax as X

HERE = Path(__file__).resolve().parent


def t(s):
    return [X.AZ.index(c) for c in s.upper()]


def s(v):
    return "".join(X.AZ[x] for x in v)


def portax_part(rec, bad):
    r = rec["portax"]["per_period"]
    ex = s(X.encipher(t("EASY"), t("theearlybirdgetsthewormx"))) == "NIJAMPBGQCWKHQJEUIKYMPAT"
    recip = all(X.PX_ENC[x][X.PX_ENC[x][(a, b)]] == (a, b) for x in range(13) for a in range(26) for b in range(26))
    fixed = sum((c[0] == a) + (c[1] == b) for x in range(13) for (a, b), c in X.PX_ENC[x].items())
    print(f"Portax: ACA worked example reproduced {ex}; every slide reciprocal {recip}; "
          f"letters kept in place over 13 x 676 pairs: {fixed}")
    if not (ex and recip and fixed == 0):
        bad.append("Portax table")
    diff = []
    for P in range(1, 49):
        ps = X.crib_pairs(P)
        cols = len({c for _, _, c in ps})
        if (len(ps), cols) != (r["before"][str(P)]["pairs_touching_crib"], r["before"][str(P)]["key_columns"]):
            diff.append(P)
    print(f"  pairs touching the crib and key columns, P = 1..48: {48 - len(diff)}/48 match the record")
    if diff:
        bad.append(f"pair counts {diff}")
    ct = t(X.K4)
    k4 = [X.before_consistent(P, ct) for P in range(1, 49)]
    print(f"  'before' layer on K4, exact backtracking: consistent at {[P for P, v in zip(range(1, 49), k4) if v]} "
          f"(inconsistent at {k4.count(False)} of 48 periods)")
    if k4.count(False) != 48:
        bad.append("Portax before K4")
    rng = random.Random(1560)
    planted = sum(X.before_consistent(P, X.plant(rng, P, "before")) is True for P in range(1, 49) for _ in range(20))
    print(f"  planted texts (random letters with the cribs, random key and sigma) found consistent: {planted}/960")
    if planted != 960:
        bad.append("Portax plants")
    res = {True: 0, False: 0, None: 0}
    for P in range(1, 49):
        for _ in range(20):
            c = ct[:]
            rng.shuffle(c)
            res[X.before_consistent(P, c, 20000)] += 1
    print(f"  shuffles (20 per period): consistent {res[True]}, inconsistent {res[False]}, "
          f"over the node budget {res[None]}  (record with CP-SAT: "
          f"{sum(v['shuffles_SAT'] for v in r['before'].values())} of 9,600 consistent)")
    if res[True] > 5:
        bad.append("Portax null")
    after = sum(v["K4"] == "UNSAT" for v in r["after"].values())
    print(f"  recorded 'after' layer (CP-SAT): K4 inconsistent at {after}/48 periods; shuffles consistent at "
          f"P = 13..33: {min(r['after'][str(P)]['shuffles_SAT'] for P in range(13, 34))}.."
          f"{max(r['after'][str(P)]['shuffles_SAT'] for P in range(13, 34))} of 200")
    if after != 48 or rec["portax"]["K4_UNSAT"] != 96:
        bad.append("recorded Portax")


def playfair_part(rec, bad):
    keep = [i for i in range(97) if X.K4[i] != "W"]
    red = "".join(X.K4[i] for i in keep)
    ridx = {i: n for n, i in enumerate(keep)}
    cr = {ridx[i]: ch for i, ch in X.CRIB.items()}
    starts, st = [], 0
    for i in range(98):
        if i == 97 or X.K4[i] == "W":
            if i > st:
                starts.append(ridx[st])
            st = i + 1
    n = len(red)

    def pairs(mode):
        if mode in (0, 1):
            return [(i, i + 1) for i in range(mode, n - 1, 2)]
        b = starts + [n]
        return [(i, i + 1) for s0, e in zip(b[:-1], b[1:]) for i in range(s0, e - 1, 2)]
    print(f"Playfair part: W removed -> {n} letters, {len(set(red))} distinct (a 25-letter alphabet); "
          f"{len(starts)} W-segments")
    for mode in (0, 1, "seg"):
        ps = [(i, j) for i, j in pairs(mode) if i in cr or j in cr]
        full = sum(i in cr and j in cr for i, j in ps)
        print(f"  pairing {mode!s:>3}: pairs with both crib letters {full}, with one {len(ps) - full}")
    m1 = 3 * 2                     # pairings x mask alphabets (the key index does not matter for a constant)
    m2 = 3 * 2 * 2 * 5             # pairings x alphabets x key index (reduced / original) x p = 1..5
    m = rec["playfair_free_square_then_mask"]["masks"]
    print(f"  settings: m1 {m1}, m2 with p <= 5 {m2} (record {m['m1']['settings']}, {m['m2_p_le_5']['settings']})")
    if n != 92 or len(set(red)) != 25 or (m1, m2) != (m["m1"]["settings"], m["m2_p_le_5"]["settings"]):
        bad.append("Playfair counts")
    tot = {k: v for k, v in m.items() if "settings" in v}
    print("  recorded K4 results (CP-SAT, necessary-condition screen): " +
          "; ".join(f"{k} {v['settings']:,} {v['K4']}" for k, v in tot.items()))
    if any(v["K4"] != "all UNSAT" for v in tot.values()) or \
            m["m3"]["by_screen"] + m["m3"]["by_cp_sat"] != m["m3"]["settings"] or \
            m["m4"]["by_screen"] + m["m4"]["by_cp_sat"] != m["m4"]["settings"]:
        bad.append("recorded Playfair")


def main():
    rec = json.loads((HERE / "results" / "portax-playfair-mask-20260930.json").read_text(encoding="utf-8"))
    bad = []
    portax_part(rec, bad)
    playfair_part(rec, bad)
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: the Portax facts and the 'before' layer reproduce; the recorded results are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
