"""Key-position slips inside and between the cribs (EP-0149, EP-0151, EP-0165, EP-0166).

Ported from the author's audit scripts (k4_crib_shift_periodic.py for the periodic test).
Needs only the public K4 ciphertext and the 24 public crib letters.  Standard library only.

Slip model: the carved letters and the crib letters stay at their carved positions; only the
"key position" read by position-type selectors moves.  A slip of d = +1 skips one key position,
d = -1 uses one twice.
"""
import random
from collections import Counter
from math import comb

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
C1 = [i for i in sorted(CRIB) if i < 50]
C2 = [i for i in sorted(CRIB) if i >= 50]


# ---------- counting the configurations and the closed-form chance ----------

def inside_slip_configurations():
    """EP-0149: one slip just before a crib letter strictly inside each crib, each +1 or -1.
    Crib 1 covers 21..33 -> cuts s1 = 22..33 (12); crib 2 covers 63..73 -> cuts s2 = 64..73 (10)."""
    return [(s1, d1, s2, d2) for s1 in range(22, 34) for d1 in (-1, 1)
            for s2 in range(64, 74) for d2 in (-1, 1)]


def between_shift_configurations():
    """EP-0165: one shift d between the cribs (somewhere in 34..62), applied to crib 2 only; d = 0 was
    already run by the plain enumerator."""
    return [d for d in (-2, -1, 1, 2)]


def chance(procedures, settings, e, letters=24):
    """expected number of procedures that agree with at least 24 - e crib letters by chance:
    settings x procedures x sum_{j<=e} C(24, j) 25^j / 26^24 (an upper bound: settings overlap)"""
    return settings * procedures * sum(comb(letters, j) * 25 ** j for j in range(e + 1)) * 26.0 ** -letters


# ---------- EP-0151: periodic arbitrary rows with a crib-2 shift ----------

def drops_class(pairs):
    """fewest (P, C) pairs to delete so that the rest is a partial bijection (exact, small classes)"""
    cnt = Counter(pairs)
    kinds = list(cnt)
    n = len(kinds)
    conf = [[(a[0] == b[0]) != (a[1] == b[1]) for b in kinds] for a in kinds]
    order = sorted(range(n), key=lambda k: -cnt[kinds[k]])
    keep = 0

    def rec(idx, chosen, w):
        nonlocal keep
        if w + sum(cnt[kinds[order[j]]] for j in range(idx, n)) <= keep:
            return
        if idx == n:
            keep = max(keep, w)
            return
        k = order[idx]
        if all(not conf[k][c] for c in chosen):
            rec(idx + 1, chosen + [k], w + cnt[kinds[k]])
        rec(idx + 1, chosen, w)

    rec(0, [], 0)
    return len(pairs) - keep


def drops(ct, p, d):
    """crib letters to drop so that period-p arbitrary rows fit, crib 2 read at key position i + d"""
    classes = {}
    for i in C1:
        classes.setdefault(i % p, []).append((CRIB[i], ct[i]))
    for i in C2:
        classes.setdefault((i + d) % p, []).append((CRIB[i], ct[i]))
    return sum(drops_class(v) for v in classes.values())


PERIODS = range(1, 49)
SHIFTS = (-2, -1, 0, 1, 2)


def periodic_table(ct=K4):
    return {(p, d): drops(ct, p, d) for p in PERIODS for d in SHIFTS}


def shuffle_p(k4tab, cells, shuffles=2000, seed=20260930):
    """share of ciphertext shuffles (crib plaintext kept) with drops <= K4's, per cell.
    Same generator and seed as the author's run; the shuffle sequence does not depend on which
    cells are evaluated, so any subset of cells reproduces the full run's values."""
    rng = random.Random(seed)
    le = {c: 0 for c in cells}
    for _ in range(shuffles):
        s = list(K4)
        rng.shuffle(s)
        s = "".join(s)
        for p, d in cells:
            if drops(s, p, d) <= k4tab[(p, d)]:
                le[(p, d)] += 1
    return {c: le[c] / shuffles for c in cells}


def planted(p, d, seed):
    """a ciphertext made by period-p arbitrary rows with crib 2 at key position i + d"""
    rng = random.Random(seed)
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rows = []
    for _ in range(p):
        r = list(AZ)
        rng.shuffle(r)
        rows.append(dict(zip(AZ, r)))
    pt = [CRIB.get(i, rng.choice(AZ)) for i in range(len(K4))]
    return "".join(rows[(i + (d if i >= 50 else 0)) % p][ch] for i, ch in enumerate(pt))


# ---------- 2026-10-10 addendum, EP-0211: one-square Bifid with a deletion / insertion between the cribs ----------
# Ported from the author's f3d.py (settings only: crib positions and W positions, no other K4 letters).
# W removed -> 92 coordinates.  d > 0: d cipher letters lost after enciphering at true q..q+d-1;
# d < 0: |d| junk letters carved at q..q+|d|-1.  Events sit between the cribs (carved 33..59).

KEEP = [i for i, ch in enumerate(K4) if ch != "W"]
RIDX = {i: k for k, i in enumerate(KEEP)}
N92 = len(KEEP)
CR92 = {RIDX[i] for i in CRIB}
_WCUT = [0] + [RIDX[i + 1] for i, ch in enumerate(K4) if ch == "W" and i + 1 < len(K4)] + [N92]
SEGS = list(zip(_WCUT[:-1], _WCUT[1:]))             # W segments in the 92 coordinates
F3D_DS = (1, 2, -1, -2)
F3D_QS = range(33, 60)
SEG_QS = [33, 34, 35, 55, 56, 57, 58, 59]


def tl_global(d, q, n=N92):
    """true position -> carved index (None = lost cipher letter)"""
    if d >= 0:
        return list(range(q)) + [None] * d + list(range(q, n))
    return list(range(q)) + list(range(q - d, n))


def per_blocks(L, p, a0):
    bd = [0] + ([a0] if a0 else []) + list(range(a0 + p if a0 else p, L, p)) + [L]
    bd = sorted(set(x for x in bd if 0 <= x <= L))
    return [list(range(s, e)) for s, e in zip(bd[:-1], bd[1:]) if e > s]


def seg_true(d, q):
    segs = [list(range(s, e)) for s, e in SEGS]
    if d > 0:
        si = 1 if q <= 35 else 4                       # crib 1's segment (events 33..35) or crib 2's (55..59)
        s = SEGS[si][0]
        segs[si] = segs[si][:q - s] + [None] * d + segs[si][q - s:]
    elif d < 0:
        junk = set(range(q, q - d))
        segs = [[c for c in seg if c not in junk] for seg in segs]
    return segs


def layout(conv, p, a0, d, q):
    """-> (tl, tblocks): true position -> carved index / None, and the blocks as lists of true positions"""
    if conv in ("per", "full"):
        tl = tl_global(d, q)
        tb = [list(range(len(tl)))] if conv == "full" else per_blocks(len(tl), p, a0)
        return tl, tb
    tl, tb = [], []
    for seg in seg_true(d, q):
        base, m = len(tl), len(seg)
        tl += seg
        if p == 0:
            tb.append(list(range(base, base + m)))
        else:
            tb += [list(range(base + s, base + min(m, s + p))) for s in range(0, m, p)]
    return tl, tb


def crib_key(tl, tb):
    """the crib-touching blocks as carved indices: the structure the exact solver sees"""
    blocks = [[tl[t] for t in b] for b in tb]
    return tuple(tuple(b) for b in blocks if any(c is not None and c in CR92 for c in b))


def contiguous(b):
    return None not in b and all(y == x + 1 for x, y in zip(b[:-1], b[1:]))


def f3d_settings():
    """EP-0211's generator: periodic settings split into covered (the broken block touches no crib letter, so
    the crib blocks are those of EP-0169's model) and residual, plus the full-text and W-segment settings"""
    S = {"per_raw": 0, "per_cov": [], "per_res": [], "full": [], "seg": []}
    for p in range(2, 13):
        for a0 in range(p):
            for d in F3D_DS:
                for q in F3D_QS:
                    S["per_raw"] += 1
                    if d < 0 and q - d - 1 >= 59:     # the junk would run into crib 2
                        continue
                    key = crib_key(*layout("per", p, a0, d, q))
                    grp = "per_cov" if all(contiguous(b) for b in key) else "per_res"
                    S[grp].append((("per", p, a0, d, q), key))
    for d in F3D_DS:
        for q in F3D_QS:
            if d < 0 and q - d - 1 >= 59:
                continue
            S["full"].append((("full", 0, 0, d, q), crib_key(*layout("full", 0, 0, d, q))))
    for p in list(range(2, 13)) + [0]:
        for d in F3D_DS:
            for q in SEG_QS:
                if d < 0 and q - d - 1 >= 59 and q >= 55:
                    continue
                S["seg"].append((("seg", p, 0, d, q), crib_key(*layout("seg", p, 0, d, q))))
    return S


def f3d_structures(S):
    """{structure: [labels]} over the residual settings (periodic residual + full text + W segments)"""
    out = {}
    for grp in ("per_res", "full", "seg"):
        for lab, key in S[grp]:
            out.setdefault(key, []).append(lab)
    return out


EDGE_SYSTEMS = [(d, edge, phi) for d in (2, -2) for edge in ("T", "B", "TB") for phi in (0, 1)]


def edge_tl(d, edge):
    if d == 2:
        if edge == "T":
            return tl_global(2, 33)                   # lost right after crib 1
        if edge == "B":
            return tl_global(2, 59)                   # lost right before crib 2
        return list(range(33)) + [None] + list(range(33, 59)) + [None] + list(range(59, N92))
    if edge == "T":
        return tl_global(-2, 33)
    if edge == "B":
        return tl_global(-2, 57)
    return [c for c in range(N92) if c not in (33, 58)]


def edge_constraints(system):
    """(pairs with both plaintext letters known, pairs with one known) in the true pairing of the system"""
    d, edge, phi = system
    tl = edge_tl(d, edge)
    full, weak = [], []
    for t in range(phi, len(tl) - 1, 2):
        ca, cb = tl[t], tl[t + 1]
        ka = ca is not None and ca in CR92
        kb = cb is not None and cb in CR92
        if ka and kb:
            full.append((ca, cb))
        elif ka or kb:
            weak.append((ca, cb, 0 if ka else 1))
    return tuple(full), tuple(weak)


# ---------- 2026-10-10 addendum, EP-0215: Enigma + sigma with a machine-step shift between the cribs ----------

def crib_group_sizes():
    """multiplicities of the 13 distinct crib letters over the 24 positions"""
    return sorted(Counter(CRIB.values()).values(), reverse=True)


def chance_drop_le(h):
    """EP-0192 T3's closed form: P(some drop set D, |D| <= h, leaves a consistent injection) for values uniform
    on 26 letters, as the union bound sum_D (26)_k / 26^m (m remaining positions, k distinct letters among them).
    Exact rational arithmetic over the 1 + 24 + 276 drop sets for h = 2."""
    from fractions import Fraction
    from itertools import combinations
    pos = sorted(CRIB)
    tot = Fraction(0)
    for size in range(h + 1):
        for D in combinations(pos, size):
            rem = [CRIB[i] for i in pos if i not in D]
            m, k = len(rem), len(set(rem))
            q = 1
            for j in range(k):
                q *= 26 - j
            tot += Fraction(q, 26 ** m)
    return float(tot)


def enigma_settings_per_column(machines):
    """machines x 6 rotor orders x 26^3 ring offsets x 26 reflector positions x 26^2 turnover phases"""
    return machines * 6 * 26 ** 3 * 26 * 26 ** 2
