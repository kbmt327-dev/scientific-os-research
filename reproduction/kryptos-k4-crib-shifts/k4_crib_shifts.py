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
