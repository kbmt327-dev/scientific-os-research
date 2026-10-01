"""How much key K4 needs, and maps that the cribs forbid outright (EP-0089, EP-0091).

  * K4's index of coincidence (IC) is flat.  English letters sent through m freely chosen rows (a random
    substitution per row, the row picked at random at each position) reach an IC as low as K4's only when m is
    about 8 or more, i.e. >= 3 bits of key per position -- more than the redundancy of English.  The IC depends
    only on letter frequencies, so plaintext letters are drawn independently from standard English frequencies.
  * A map that does not depend on position (the ciphertext letter depends only on a window of <= 4 plaintext
    letters) is impossible: EAST occurs twice in the crib EASTNORTHEAST and enciphers differently.
Standard library only.
"""
import random
from math import log2

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH = [.08167, .01492, .02782, .04253, .12702, .02228, .02015, .06094, .06966, .00153, .00772, .04025, .02406,
           .06749, .07507, .01929, .00095, .05987, .06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074]


def ic(s):
    n = len(s)
    return sum(s.count(c) * (s.count(c) - 1) for c in set(s)) / (n * (n - 1))


def free_rows_share(m, trials, seed=910):
    """share of simulated 97-letter ciphertexts (English through m random rows) with IC <= K4's"""
    rng = random.Random(seed + m)
    target = ic(K4)
    low = 0
    for _ in range(trials):
        rows = []
        for _ in range(m):
            r = list(AZ)
            rng.shuffle(r)
            rows.append(r)
        pt = rng.choices(range(26), weights=ENGLISH, k=97)
        ct = "".join(rows[rng.randrange(m)][x] for x in pt)
        low += ic(ct) <= target
    return low / trials


def uniform_share(trials, seed=20260930):
    """share of uniform 97-letter strings with IC <= K4's (EP-0152: a uniform key gives uniform ciphertext)"""
    rng = random.Random(seed)
    target = ic(K4)
    return sum(ic("".join(rng.choice(AZ) for _ in range(97))) <= target for _ in range(trials)) / trials


def english_entropy():
    return -sum(p * log2(p) for p in ENGLISH)


def window_conflicts(max_width=4):
    """for every window shape (a letters before, b after, a + b + 1 <= max_width), a pair of crib positions with
    the same plaintext window and different ciphertext letters"""
    out = {}
    for w in range(1, max_width + 1):
        for a in range(w):
            b = w - 1 - a
            witness = None
            for i in CRIB:
                for j in CRIB:
                    if i < j and all(i + d in CRIB and j + d in CRIB and CRIB[i + d] == CRIB[j + d]
                                     for d in range(-a, b + 1)) and K4[i] != K4[j]:
                        witness = (i, j)
                        break
                if witness:
                    break
            out[f"{a}+1+{b}"] = witness
    return out
