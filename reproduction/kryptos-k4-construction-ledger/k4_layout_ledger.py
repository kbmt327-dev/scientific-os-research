"""Operators fixed by K4's place on the carved panel (EP-0140): an arbitrary substitution table
per carved row (L1) or per carved column (L2), tested for exact consistency with the cribs.
Standard library only.

K4's place (from public photographs): positions 0-3 are row 24, columns 27-30; positions 4-34,
35-65 and 66-96 are rows 25, 26 and 27, 31 letters each.  Only these coordinates are used; the
rest of the carved text is not needed.  The fold operators of the Note (G1-G3) need the letters
behind K4 on the tableau and on the upper cipher plate, which this site does not publish, so
they are recorded, not rerun.
"""
import random
from itertools import combinations
from math import comb

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
CI = sorted(CRIB)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

RC = [(24, 27 + i) for i in range(4)] + [(25 + (p - 4) // 31, (p - 4) % 31) for p in range(4, 97)]


def classes():
    return {"L1 row": [r for r, _ in RC], "L2 column": [c for _, c in RC]}


def within_class_pairs(cls):
    return [(a, b) for a, b in combinations(CI, 2) if cls[a] == cls[b]]


def consistent(ct, cls):
    """First crib pair inside one class that breaks 'P -> C is a function and injective', or None."""
    for a, b in combinations(CI, 2):
        if cls[a] == cls[b] and (CRIB[a] == CRIB[b]) != (ct[a] == ct[b]):
            return (a, b)
    return None


def plant(rng, cls):
    tab, pt = {}, [rng.choice(AZ) for _ in range(97)]
    for i, ch in CRIB.items():
        pt[i] = ch
    ct = []
    for i, ch in enumerate(pt):
        if cls[i] not in tab:
            tab[cls[i]] = dict(zip(AZ, rng.sample(AZ, 26)))
        ct.append(tab[cls[i]][ch])
    return "".join(ct)


def run(n=20000, seed=140):
    """Same order of random draws as the author's run (L1, then L2), so the fractions match exactly."""
    rng = random.Random(seed)
    res = {}
    for name, cls in classes().items():
        bad = consistent(K4, cls)
        ok, lst = 0, list(K4)
        for _ in range(n):
            rng.shuffle(lst)
            ok += consistent(lst, cls) is None
        plants = sum(consistent(plant(rng, cls), cls) is None for _ in range(20))
        res[name] = {"consistent": bad is None, "first_conflict": list(bad) if bad else None,
                     "null_consistent_fraction": ok / n, "plants_consistent": f"{plants}/20",
                     "within_class_crib_pairs": len(within_class_pairs(cls))}
    return res


def last_rows_all_31(rows=28, rows_31=15, last=4):
    """Chance that the last `last` rows are all 31 letters when `rows_31` of `rows` are, at random."""
    return comb(rows - last, rows_31 - last) / comb(rows, rows_31)
