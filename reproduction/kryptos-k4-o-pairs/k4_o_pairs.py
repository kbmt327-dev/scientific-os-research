"""The two O-segments of the W-bracket reading (EP-0138, catalog J02): letters at the same
offset in positions 21-35 and 59-73 paired as digraphs.  Crib-only checks and the 2x2 Hill
search on these pairs.  Standard library only.
"""
from itertools import product

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
A, B, LEN = 21, 59, 15        # the two segments of equal length between Ws
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ALPHABETS = {"AZ": AZ, "KA": KA, "AZ without W": AZ.replace("W", ""), "KA without W": KA.replace("W", "")}


def pairs(first=A, second=B, mirror=False):
    """[(offset, (P1, P2), (C1, C2))]; unknown plaintext letters are None."""
    out = []
    for o in range(LEN):
        i, j = first + o, (second + LEN - 1 - o) if mirror else second + o
        out.append((o, (CRIB.get(i), CRIB.get(j)), (K4[i], K4[j])))
    return out


def both_known(ps):
    return [(p, c) for _, p, c in ps if None not in p]


def repeated_inputs(ps):
    """Input digraphs that occur twice: a fixed digraph table must map them alike."""
    seen, clash, same = {}, [], []
    for p, c in both_known(ps):
        if p in seen:
            (clash if seen[p] != c else same).append((p, seen[p], c))
        seen.setdefault(p, c)
    return clash, same


def hill_rows(alpha, affine, rev=False):
    """Count solutions (m1, m2, b) of each output row of C = M P (+ b) mod n over the
    fully known pairs; a 2x2 Hill needs both rows solvable."""
    n = len(alpha)
    eqs = []
    for p, c in both_known(pairs()):
        if any(ch not in alpha for ch in p + c):
            return None
        pv = [alpha.index(ch) for ch in p]
        cv = [alpha.index(ch) for ch in c]
        if rev:
            pv, cv = pv[::-1], cv[::-1]
        eqs.append((pv, cv))
    return solve_rows(eqs, n, affine)


def solve_rows(eqs, n, affine):
    """eqs = [(p vector, c vector)]; solutions of each output row by brute force."""
    counts = []
    for r in range(2):
        k = 0
        for m1, m2, b in product(range(n), range(n), range(n) if affine else (0,)):
            if all((m1 * pv[0] + m2 * pv[1] + b) % n == cv[r] for pv, cv in eqs):
                k += 1
        counts.append(k)
    return counts
