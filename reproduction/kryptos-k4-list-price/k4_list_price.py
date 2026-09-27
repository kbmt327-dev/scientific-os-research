"""Price of the target-list choice for the W-gap reading of K4 (EP-0135, Q1).

The reading family is the one of EP-0011, written for a text of length n: for a set of
m marker positions, the gap definition (letters strictly between / difference), the
anchor (from the start / from 0 / cyclic / none), the direction and A=1 or A=0 are free.
With K4's letters as markers, positions are uniform among the 97 cells under the null,
so the expected number of list words the family produces is a finite sum (union bound
over conventions):

    E[hits] = sum over words, m of carriers(m) * #(position sets giving the word) / C(97, m)

Standard library only.
"""
from collections import defaultdict
from math import comb

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
GAPDEF = ("between", "difference")
ANCHOR = ("start", "zero", "cyclic", "none")


def decode(word, base):
    lo = 1 if base == "A1" else 0
    return [ord(c) - 65 + lo for c in word]


def readings(v, n):
    """every string the family yields for one sorted position list v: {string: [convention, ...]}"""
    m = len(v)
    out = defaultdict(list)
    for gd in GAPDEF:
        sub = 1 if gd == "between" else 0
        for an in ANCHOR:
            if an == "none":
                seq = [v[k] - v[k - 1] - sub for k in range(1, m)]
            else:
                pre = -1 if an == "start" else 0 if an == "zero" else v[-1] - n
                seq = [v[0] - pre - sub] + [v[k] - v[k - 1] - sub for k in range(1, m)]
            if len(seq) < 3:
                continue
            for dr in ("fwd", "rev"):
                s = seq[::-1] if dr == "rev" else seq
                for base in ("A1", "A0"):
                    lo, hi = (1, 26) if base == "A1" else (0, 25)
                    if all(lo <= x <= hi for x in s):
                        out["".join(chr(65 + x - lo) for x in s)].append(f"{gd}/{an}/{dr}/{base}")
    return out


def count_sets(seq, m, n, gd, an):
    """number of increasing m-position sets in [0, n) whose gaps under (gd, an) equal seq"""
    sub = 1 if gd == "between" else 0
    if an == "none":
        if len(seq) != m - 1 or any(g + sub < 1 for g in seq):
            return 0
        return max(0, n - (sum(seq) + (m - 1) * sub))
    if len(seq) != m:
        return 0
    if an == "cyclic":
        if sum(seq) + m * sub != n or any(g + sub < 1 for g in seq):
            return 0
        return max(0, n - (sum(seq[1:]) + (m - 1) * sub))
    pre = -1 if an == "start" else 0
    v0 = pre + seq[0] + sub
    if v0 < 0 or any(g + sub < 1 for g in seq[1:]):
        return 0
    return 1 if v0 + sum(seq[1:]) + (m - 1) * sub < n else 0


def expected(words, carriers, n):
    """union-bound E[hits] for a word list, given {m: number of marker types with m positions}"""
    total, per = 0.0, {}
    for w in words:
        e = 0.0
        for m, c in carriers.items():
            if len(w) not in (m, m - 1):
                continue
            s = 0
            for gd in GAPDEF:
                for an in ANCHOR:
                    for dr in (1, -1):
                        for base in ("A1", "A0"):
                            s += count_sets(decode(w, base)[::dr], m, n, gd, an)
            e += c * s / comb(n, m)
        if e:
            per[w] = e
            total += e
    return total, per


def letter_markers(text):
    pos = defaultdict(list)
    for i, c in enumerate(text):
        pos[c].append(i)
    return pos


def k4_carriers():
    car = defaultdict(int)
    for v in letter_markers(K4).values():
        car[len(v)] += 1
    return dict(car)


def k4_hits(lists):
    """list words produced by K4's own letters under the family"""
    found = []
    for letter, v in sorted(letter_markers(K4).items()):
        for s, convs in readings(v, len(K4)).items():
            for name, words in lists.items():
                if s in words:
                    found.append((letter, s, name, convs[0]))
    return found
