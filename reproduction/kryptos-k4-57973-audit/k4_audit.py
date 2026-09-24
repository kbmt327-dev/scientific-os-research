"""Independent audit of the reverse-Gromark-57973 hypothesis for Kryptos K4.

Reproduces every numeric claim in the 2026-09-18 handoff from the public
ciphertext and the 24 artist-confirmed crib letters only, then measures the
two controls the handoff omits:
  * the crib-compatibility rate of arbitrary digit masks (is 23/100000 special?)
  * the survival of the 13 forced letters under route freedom

Usage:  python k4_audit.py [--quick] [--json out.json]
"""
import argparse
import json
import random
import time

CT = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIA"
      "WINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
A = ord('A')
CRIBS = {}
for _j, _c in enumerate("EASTNORTHEAST"):
    CRIBS[21 + _j] = _c
for _j, _c in enumerate("BERLINCLOCK"):
    CRIBS[63 + _j] = _c
CP = sorted(CRIBS)
PLET = [ord(CRIBS[i]) - A for i in CP]
CT_CODES = [ord(ch) - A for ch in CT]


def gromark(primer, n=97):
    """Classic Gromark keystream: d_i = d_{i-5} + d_{i-4} mod 10."""
    d = list(primer)
    while len(d) < n:
        d.append((d[-5] + d[-4]) % 10)
    return d[:n]


def _solve(ctcodes, mask):
    """Constraint CA(ct[i]) - PA(crib[i]) = mask[i] (mod 26), with PA and CA
    arbitrary alphabet permutations.  Union-find over 26 plaintext + 26 cipher
    letters carrying a mod-26 offset.  Returns (find, comps, used_c) or None."""
    par = list(range(52))
    off = [0] * 52

    def find(x):
        r, o = x, 0
        while par[r] != r:
            o = (o + off[r]) % 26
            r = par[r]
        return r, o

    for k, i in enumerate(CP):
        p = PLET[k]
        c = 26 + ctcodes[i]
        d = mask[i] % 26
        rp, op = find(p)
        rc, oc = find(c)
        if rp == rc:
            if (oc - op - d) % 26:
                return None
        else:
            par[rc] = rp
            off[rc] = (op + d - oc) % 26

    used_c = set(26 + ctcodes[i] for i in CP)
    used_p = set(PLET)
    comps = {}
    for x in range(52):
        r, o = find(x)
        comps.setdefault(r, []).append((x, o))
    for mem in comps.values():
        pv = [o for x, o in mem if x < 26 and x in used_p]
        cv = [o for x, o in mem if x >= 26 and x in used_c]
        if len(set(pv)) != len(pv) or len(set(cv)) != len(cv):
            return None
    return find, comps, used_c


def sat(ctcodes, mask):
    return _solve(ctcodes, mask) is not None


def forced(ctcodes, mask):
    """Plaintext letters at non-crib positions fixed by same-component algebra."""
    s = _solve(ctcodes, mask)
    if s is None:
        return None
    find, comps, used_c = s
    used_p = set(PLET)
    out = {}
    for i in range(97):
        if i in CRIBS:
            continue
        c = 26 + ctcodes[i]
        if c not in used_c:
            continue
        rc, oc = find(c)
        target = (oc - mask[i]) % 26
        for x, o in comps[rc]:
            if x < 26 and x in used_p and o == target:
                out[i] = chr(A + x)
                break
    return out


def skeleton(forced_map):
    return "".join(CRIBS[i].lower() if i in CRIBS else forced_map.get(i, '.')
                   for i in range(97))


def config_count(ctcodes, mask):
    """Valid mod-26 offset assignments across the constrained components."""
    from itertools import product
    _find, comps, used_c = _solve(ctcodes, mask)
    used_p = set(PLET)
    groups = []
    for mem in comps.values():
        pv = [o for x, o in mem if x < 26 and x in used_p]
        cv = [o for x, o in mem if x >= 26 and x in used_c]
        if pv or cv:
            groups.append((pv, cv))
    n = 0
    for ts in product(range(26), repeat=len(groups)):
        pp, cc = [], []
        for t, (pv, cv) in zip(ts, groups):
            pp += [(v + t) % 26 for v in pv]
            cc += [(v + t) % 26 for v in cv]
        if len(set(pp)) == len(pp) and len(set(cc)) == len(cc):
            n += 1
    return n, len(groups)


def routes():
    """Paper-executable route family: columnar, boustrophedon, mirror."""
    r = {"identity": list(range(97)), "reverse": list(range(96, -1, -1))}
    for cols in range(2, 49):
        rows = (97 + cols - 1) // cols
        col = [x * cols + c for c in range(cols) for x in range(rows)
               if x * cols + c < 97]
        r["col%d" % cols] = col
        r["col%d-rev" % cols] = col[::-1]
        bou = []
        for x in range(rows):
            row = [x * cols + c for c in range(cols) if x * cols + c < 97]
            bou += row if x % 2 == 0 else row[::-1]
        r["bou%d" % cols] = bou
        r["bou%d-rev" % cols] = bou[::-1]
        cb = []
        for c in range(cols):
            cm = [x * cols + c for x in range(rows) if x * cols + c < 97]
            cb += cm if c % 2 == 0 else cm[::-1]
        r["colbou%d" % cols] = cb
        r["mirror%d" % cols] = [x * cols + (cols - 1 - c) for x in range(rows)
                                for c in range(cols) if x * cols + (cols - 1 - c) < 97]
    return {k: v for k, v in r.items()
            if len(v) == 97 and sorted(v) == list(range(97))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()
    null_n = 100000 if args.quick else 2000000
    nprim = 10 if args.quick else 40

    res = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "ciphertext_length": len(CT),
           "crib_letters": len(CRIBS)}

    # 1. what does "reverse" mean?  test against the handoff's 13 stated masks
    stated = {8: 9, 15: 0, 17: 0, 38: 8, 45: 1, 46: 2, 47: 4,
              60: 0, 75: 9, 77: 3, 78: 8, 80: 8, 85: 2}
    d = gromark([5, 7, 9, 7, 3])
    cand = {"forward": d,
            "sequence_reversed": d[::-1],
            "negated_forward": [(-x) % 10 for x in d],
            "negated_reversed": [(-x) % 10 for x in d[::-1]],
            "primer_reversed_forward": gromark([3, 7, 9, 7, 5])}
    res["mask_variant_match_out_of_13"] = {
        k: sum(1 for i in stated if v[i] == stated[i]) for k, v in cand.items()}

    # 2. full 100,000-primer scan, both directions
    fwd, rev = [], []
    for n in range(100000):
        p = [n // 10000 % 10, n // 1000 % 10, n // 100 % 10, n // 10 % 10, n % 10]
        dd = gromark(p)
        if sat(CT_CODES, dd):
            fwd.append("%05d" % n)
        if sat(CT_CODES, dd[::-1]):
            rev.append("%05d" % n)
    res["forward_compatible"] = {"count": len(fwd), "primers": fwd}
    res["reverse_compatible"] = {"count": len(rev), "primers": rev}
    res["p57973_forward_sat"] = "57973" in fwd
    res["p57973_reverse_sat"] = "57973" in rev

    # 3. forced letters for every reverse-compatible primer
    mask57973 = gromark([5, 7, 9, 7, 3])[::-1]
    tbl = {}
    for p in rev:
        f = forced(CT_CODES, gromark([int(x) for x in p])[::-1])
        tbl[p] = {"n": len(f), "skeleton": skeleton(f)}
    res["forced_by_primer"] = tbl
    res["max_forced"] = max(v["n"] for v in tbl.values())
    res["primers_at_max"] = sorted(k for k, v in tbl.items()
                                   if v["n"] == res["max_forced"])
    f57973 = forced(CT_CODES, mask57973)
    res["p57973_forced"] = {str(k): v for k, v in sorted(f57973.items())}
    res["p57973_skeleton"] = skeleton(f57973)
    cfg, ncomp = config_count(CT_CODES, mask57973)
    res["p57973_config_count"] = cfg
    res["p57973_components"] = ncomp

    # 4. CONTROL A -- crib-compatibility rate of arbitrary digit masks
    random.seed(0)
    hits = sum(1 for _ in range(null_n)
               if sat(CT_CODES, [random.randrange(10) for _ in range(97)]))
    res["null_random_mask"] = {"trials": null_n, "compatible": hits,
                               "rate": hits / null_n}

    # 5. CONTROL B -- do the 13 forced letters survive route freedom?
    rt = routes()
    rc_map = {k: [CT_CODES[i] for i in v] for k, v in rt.items()}
    res["route_family_size"] = len(rt)
    combos, best, best_at, best_skel = 0, 0, None, None
    for dname, base in (("reverse", mask57973), ("forward", gromark([5, 7, 9, 7, 3]))):
        for sh in range(97):
            mask = base[sh:] + base[:sh]
            for rname, rc in rc_map.items():
                f = forced(rc, mask)
                if f is not None:
                    combos += 1
                    if len(f) > best:
                        best = len(f)
                        best_at = "%s shift=%d %s" % (dname, sh, rname)
                        best_skel = skeleton(f)
    res["route_sweep_57973"] = {
        "combinations_tried": 2 * 97 * len(rt),
        "sat": combos,
        "max_forced_under_route_freedom": best,
        "max_forced_at": best_at,
        "max_forced_skeleton": best_skel,
        "max_forced_direct_identity_shift0": len(f57973)}

    # 6. CONTROL C -- do arbitrary primers also admit a crib-compatible route?
    random.seed(1)

    def any_sat(p):
        dd = gromark(p)
        for base in (dd[::-1], dd):
            for sh in range(97):
                mask = base[sh:] + base[:sh]
                for rc in rc_map.values():
                    if sat(rc, mask):
                        return True
        return False

    ok = sum(1 for _ in range(nprim)
             if any_sat([random.randrange(10) for _ in range(5)]))
    res["null_random_primer_admits_route"] = {"primers": nprim, "admitting": ok}

    out = json.dumps(res, ensure_ascii=False, indent=2, sort_keys=True)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
