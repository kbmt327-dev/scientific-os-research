"""Letters reordered inside each crib word (EP-0137, catalog J01): the counts and crib checks
that need only the public ciphertext and cribs.  Standard library only.

Segmentations of the two cribs into words (0-based positions):
  S1  EAST|NORTHEAST|BERLIN|CLOCK     the spans of Sanborn's hints
  S2  EAST|NORTH|EAST|BERLIN|CLOCK
  S3  EASTNORTHEAST|BERLINCLOCK       each crib one word
"""
from collections import Counter
from itertools import combinations
from math import factorial, log2

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = sorted(CRIB)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

SEGS = {"S1": [(21, 25), (25, 34), (63, 69), (69, 74)],
        "S2": [(21, 25), (25, 30), (30, 34), (63, 69), (69, 74)],
        "S3": [(21, 34), (63, 74)]}
# the two further splits used only in the word-restart (J03) check
J03_SEGS = dict(SEGS, **{"EASTNORTHEAST+BERLIN|CLOCK": [(21, 34), (63, 69), (69, 74)],
                         "EAST|NORTHEAST+BERLINCLOCK": [(21, 25), (25, 34), (63, 74)]})


def _rail(n):
    return list(range(0, n, 2)) + list(range(1, n, 2))


RULES = {
    "id": lambda n: list(range(n)),
    "rev": lambda n: list(range(n))[::-1],
    "rotL1": lambda n: [(j + 1) % n for j in range(n)],
    "rotR1": lambda n: [(j - 1) % n for j in range(n)],
    "swap": lambda n: [j ^ 1 if (j ^ 1) < n else j for j in range(n)],
    "rail2": _rail,
    "rail2i": lambda n: sorted(range(n), key=_rail(n).__getitem__),
    "half": lambda n: [(j + n // 2) % n for j in range(n)],
}


def word(a, b):
    return "".join(CRIB[i] for i in range(a, b))


def arrangements(seg):
    """Distinct orders of the letters inside each word, multiplied over the words."""
    n = 1
    for a, b in SEGS[seg]:
        w = word(a, b)
        m = factorial(len(w))
        for c in Counter(w).values():
            m //= factorial(c)
        n *= m
    return n


def arrange(seg, perms):
    """perms[w] = p with X[j] = word[p[j]] -> {position: letter}."""
    out = {}
    for (a, b), p in zip(SEGS[seg], perms):
        w = word(a, b)
        for j, i in enumerate(range(a, b)):
            out[i] = w[p[j]]
    return out


def rule_assignments():
    """Distinct crib assignments given by the 8 fixed rules over the 3 segmentations."""
    seen = {}
    for rn, rf in RULES.items():
        for s in SEGS:
            cr = arrange(s, [rf(b - a) for a, b in SEGS[s]])
            seen.setdefault("".join(cr[i] for i in POS), []).append(f"{rn}/{s}")
    return seen


def word_restart_conflicts(ws, from_end):
    """J03: if the key restarts at every word, letters at the same place in their words share one
    chart row, so equal plaintext letters must give equal ciphertext letters and vice versa.
    Count the crib pairs that break this."""
    items = []
    for a, b in ws:
        for p in range(a, b):
            items.append(((b - 1 - p) if from_end else (p - a), CRIB[p], K4[p]))
    return sum(1 for x, y in combinations(items, 2)
               if x[0] == y[0] and ((x[1] == y[1]) != (x[2] == y[2])))


def near_keys(assign):
    """Crib positions whose A-Z shift key (ciphertext minus plaintext) is within +-3."""
    c = 0
    for p in POS:
        k = (AZ.index(K4[p]) - AZ.index(assign[p])) % 26
        c += min(k, 26 - k) <= 3
    return c


def reversed_assignment(seg):
    return arrange(seg, [RULES["rev"](b - a) for a, b in SEGS[seg]])


CRIB_BITS = len(CRIB) * log2(26)
