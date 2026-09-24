"""EP-0057: the five Ws bracket both cribs -- verification and the two readings it suggests.

Observation (external, post hoc): W at 20,36,48,58,74.  W@20 is just before EASTNORTHEAST
(21-33) and W@74 just after BERLINCLOCK (63-73).  Both cribs lie inside the two 15-letter
W-gaps, which are the two "O"s of the TOKIO reading (H-11).

Part A  verification: exact nulls for the stated statistic and for letter-free versions.
Part B  "W is an inserted null": drop the Ws (92 letters) and gate key families on the cribs.
Part C  "the key restarts at each W": both cribs sit in O-segments, so any key that depends
        only on (segment letter, offset in segment) gives the two cribs the SAME keystream.
        EASTNORTHEAST is at offsets 0-12 of its segment, BERLINCLOCK at 4-14 -> 9 shared
        offsets, a 26^-9 test per setting (additive) or an injectivity test (arbitrary
        substitution per offset).

Run:  python k4_w_brackets.py --plants      (positive controls only; K4 is not read)
      python k4_w_brackets.py --k4 --json w-brackets-20260924.json
"""
import json
import random
import sys
from collections import Counter
from math import comb

from k4_common import K4, CRIB, N, AZ, KA, key_of, plain_of, encrypt_plain

SETTINGS = [("vig", AZ), ("beau", AZ), ("vbeau", AZ), ("vig", KA), ("beau", KA), ("vbeau", KA)]


def kval(kind, A, c, p):
    if kind == "vbeau":
        return (-key_of("vig", A, c, p)) % 26
    return key_of(kind, A, c, p)


def enc(kind, A, p, k):
    if kind == "vbeau":
        return encrypt_plain("vig", A, p, (-k) % 26)
    return encrypt_plain(kind, A, p, k)


def dec(kind, A, c, k):
    if kind == "vbeau":
        return plain_of("vig", A, c, (-k) % 26)
    return plain_of(kind, A, c, k)


# ---------------------------------------------------------------- Part A
def part_a(ct):
    n = len(ct)
    W = [i for i, c in enumerate(ct) if c == "W"]
    m = len(W)
    gaps = [b - a - 1 for a, b in zip([-1] + W, W + [n])]
    p_both = m * (m - 1) / (n * (n - 1))
    p_ge2_of4 = sum(comb(4, k) * comb(n - 4, m - k) for k in range(2, 5)) / comb(n, m)
    cnt = Counter(ct)
    p_same_outer = sum(v * (v - 1) for v in cnt.values()) / (n * (n - 1))
    # exact: same letter at (20,74) OR same letter at (34,62)
    tot = n * (n - 1) * (n - 2) * (n - 3)
    both = sum(v * (v - 1) * (v - 2) * (v - 3) for v in cnt.values()) + sum(
        a * (a - 1) * b * (b - 1) for x, a in cnt.items() for y, b in cnt.items() if x != y)
    p_same_either = 2 * p_same_outer - both / tot
    return {"W": W, "gaps": gaps,
            "P_W_at_20_and_74": p_both,
            "P_W_at_20_74_or_34_62": 2 * p_both - (m * (m - 1) * (m - 2) * (m - 3)) / tot,
            "P_ge2_of_4_boundary_cells_W": p_ge2_of4,
            "P_same_letter_20_74_any_letter": p_same_outer,
            "P_same_letter_outer_or_inner_pair": p_same_either,
            "boundary_letters": {i: ct[i] for i in (20, 34, 62, 74)}}


# ---------------------------------------------------------------- Part B
def drop_w(ct, crib):
    out, cr, j = [], {}, 0
    for i, c in enumerate(ct):
        if c == "W":
            continue
        out.append(c)
        if i in crib:
            cr[j] = crib[i]
        j += 1
    return "".join(out), cr


def periodic_ok(ct, cr, kind, A, p):
    k = {}
    for i, pl in cr.items():
        v = kval(kind, A, ct[i], pl)
        if k.setdefault(i % p, v) != v:
            return False
    return True


def trivial_periods(cr, pmax):
    return [p for p in range(1, pmax + 1) if len({i % p for i in cr}) == len(cr)]


def progressive_ok(ct, cr, kind, A, p, s):
    k = {}
    for i, pl in cr.items():
        v = (kval(kind, A, ct[i], pl) - s * (i // p)) % 26
        if k.setdefault(i % p, v) != v:
            return False
    return True


def general_periodic_ok(ct, cr, p):
    """arbitrary substitution alphabet per residue: p->c must be a partial bijection."""
    f, g = {}, {}
    for i, pl in cr.items():
        r, c = i % p, ct[i]
        if f.setdefault((r, pl), c) != c or g.setdefault((r, c), pl) != pl:
            return False
    return True


def ct_autokey_ok(ct, cr, kind, A, L):
    for i, pl in cr.items():
        if i >= L and kval(kind, A, ct[i], pl) != A.index(ct[i - L]):
            return False
    return True


def pt_autokey_ok(ct, cr, kind, A, L):
    """k_i = index of p_{i-L}.  A crib letter fixes its whole residue chain mod L."""
    n = len(ct)
    known = {}
    for i0, pl0 in cr.items():
        chain = {i0: pl0}
        i = i0
        while i + L < n:  # forward
            chain[i + L] = dec(kind, A, ct[i + L], A.index(chain[i]))
            i += L
        i = i0
        while i - L >= 0:  # backward: key at i is p_{i-L}
            chain[i - L] = A[kval(kind, A, ct[i], chain[i])]
            i -= L
        for j, x in chain.items():
            if known.setdefault(j, x) != x:
                return False
    return True


def part_b(ct, crib):
    out = {}
    for label, (t, cr) in {"with_W_97": (ct, crib), "drop_W_92": drop_w(ct, crib)}.items():
        n = len(t)
        pmax = n // 2
        triv = trivial_periods(cr, pmax)
        row = {"len": n, "crib_index_range": [min(cr), max(cr)], "trivial_periods": triv}
        for kind, A in SETTINGS:
            name = f"{kind}-{'AZ' if A == AZ else 'KA'}"
            row[f"periodic {name}"] = [p for p in range(1, pmax + 1)
                                       if periodic_ok(t, cr, kind, A, p) and p not in triv]
            row[f"progressive {name}"] = [(p, s) for p in range(1, 27) for s in range(1, 26)
                                          if progressive_ok(t, cr, kind, A, p, s) and p not in triv]
            row[f"ct-autokey {name}"] = [L for L in range(1, 31) if ct_autokey_ok(t, cr, kind, A, L)]
            row[f"pt-autokey {name}"] = [L for L in range(1, 31) if pt_autokey_ok(t, cr, kind, A, L)]
        row["general periodic (any alphabet per residue), nontrivial p"] = [
            p for p in range(1, pmax + 1) if general_periodic_ok(t, cr, p) and p not in triv]
        out[label] = row
    return out


# ---------------------------------------------------------------- Part C
def segments(ct):
    W = [i for i, c in enumerate(ct) if c == "W"]
    return list(zip([0] + [w + 1 for w in W], W + [len(ct)])), W


def crib_offsets(ct, crib, from_end=False, include_w=False):
    """offset of each crib position inside its W-segment."""
    segs, W = segments(ct)
    res = {}
    for i, pl in crib.items():
        for s, e in segs:
            if s <= i < e:
                start = s - 1 if (include_w and s > 0) else s
                res[i] = (e - 1 - i) if from_end else (i - start)
    return res


def shared_key_test(ct, crib, from_end, include_w):
    off = crib_offsets(ct, crib, from_end, include_w)
    g1 = {off[i]: i for i in range(21, 34)}
    g2 = {off[i]: i for i in range(63, 74)}
    shared = sorted(set(g1) & set(g2))
    res = {"shared_offsets": shared}
    for kind, A in SETTINGS:
        name = f"{kind}-{'AZ' if A == AZ else 'KA'}"
        agree = sum(kval(kind, A, ct[g1[o]], crib[g1[o]]) == kval(kind, A, ct[g2[o]], crib[g2[o]])
                    for o in shared)
        res[name] = f"{agree}/{len(shared)}"
    # arbitrary substitution per offset: same plaintext letter <-> same ciphertext letter
    viol = [o for o in shared
            if (crib[g1[o]] == crib[g2[o]]) != (ct[g1[o]] == ct[g2[o]])]
    res["arbitrary-per-offset violations"] = viol
    res["arbitrary-per-offset informative offsets"] = [
        o for o in shared if crib[g1[o]] == crib[g2[o]] or ct[g1[o]] == ct[g2[o]]]
    return res


def part_c(ct, crib):
    return {f"{'from_end' if fe else 'from_start'}{' incl_W' if iw else ''}":
            shared_key_test(ct, crib, fe, iw)
            for fe in (False, True) for iw in (False, True) if not (fe and iw)}


# ---------------------------------------------------------------- plants
def plant_segment_key(rng, kind, A):
    """random plaintext with cribs and Ws placed as in K4, keystream restarting per segment.
    Redrawn until no enciphered letter is W, so the W layout is exactly K4's."""
    while True:
        ct = _plant_segment_key(rng, kind, A)
        if [i for i, c in enumerate(ct) if c == "W"] == [20, 36, 48, 58, 74]:
            return ct


def _plant_segment_key(rng, kind, A):
    Wpos = [20, 36, 48, 58, 74]
    pt = [rng.choice(AZ.replace("W", "")) for _ in range(N)]
    for i, c in CRIB.items():
        pt[i] = c
    ks = [rng.randrange(26) for _ in range(N)]
    ct, off = [], 0
    for i in range(N):
        if i in Wpos:
            ct.append("W")
            off = 0
            continue
        ct.append(enc(kind, A, pt[i], ks[off]))
        off += 1
    return "".join(ct)


def plant_nulls(rng, kind, A, family, P):
    """92-letter plaintext enciphered, then Ws inserted at K4's W positions (redrawn until
    no enciphered letter is W)."""
    while True:
        ct = _plant_nulls(rng, kind, A, family, P)
        if ct.count("W") == 5:
            return ct


def _plant_nulls(rng, kind, A, family, P):
    Wpos = [20, 36, 48, 58, 74]
    full = [None] * N
    for i, c in CRIB.items():
        full[i] = c
    pt = [full[i] if full[i] else rng.choice(AZ) for i in range(N) if i not in Wpos]
    key = [rng.randrange(26) for _ in range(P)]
    ct = []
    for j, p in enumerate(pt):
        if family == "periodic":
            k = key[j % P]
        elif family == "ct-autokey":
            k = key[j] if j < P else A.index(ct[j - P])
        else:  # pt-autokey
            k = key[j] if j < P else A.index(pt[j - P])
        ct.append(enc(kind, A, p, k))
    out, it = [], iter(ct)
    for i in range(N):
        out.append("W" if i in Wpos else next(it))
    return "".join(out)


def plants():
    rng = random.Random(55)
    rows = []
    for kind, A in SETTINGS:
        name = f"{kind}-{'AZ' if A == AZ else 'KA'}"
        ct = plant_segment_key(rng, kind, A)
        r = shared_key_test(ct, CRIB, False, False)
        rows.append(("segment-key", name, r[name], r["arbitrary-per-offset violations"]))
        for fam, P in (("periodic", 7), ("ct-autokey", 5), ("pt-autokey", 9)):
            ct = plant_nulls(rng, kind, A, fam, P)
            t, cr = drop_w(ct, CRIB)
            ok = {"periodic": periodic_ok, "ct-autokey": ct_autokey_ok,
                  "pt-autokey": pt_autokey_ok}[fam](t, cr, kind, A, P)
            rows.append((f"W-null {fam} P={P}", name, ok, None))
    return rows


if __name__ == "__main__":
    if "--plants" in sys.argv:
        for r in plants():
            print(*r)
        sys.exit()
    if "--k4" in sys.argv:
        res = {"A": part_a(K4), "B": part_b(K4, CRIB), "C": part_c(K4, CRIB), "plants": plants()}
        print(json.dumps(res, indent=1, ensure_ascii=False))
        if "--json" in sys.argv:
            with open(sys.argv[sys.argv.index("--json") + 1], "w") as f:
                json.dump(res, f, indent=1, ensure_ascii=False)
