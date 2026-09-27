"""How many crib letters must be wrong before a periodic key fits K4 (EP-0070, EP-0071)?

For a periodic key with period p, each crib letter needs one key value; letters in the same residue class must share
it.  The fewest crib errors needed is, summed over classes, the class size minus the largest group needing the same
key.  Six conventions: Vigenere, Beaufort and variant Beaufort over A-Z or the KRYPTOS alphabet.  Compared with
shuffled K4.  Standard library only.
"""
import random
from collections import Counter

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
TYPES = {"vigenere": lambda x, y: (y - x) % 26, "beaufort": lambda x, y: (y + x) % 26,
         "variant": lambda x, y: (x - y) % 26}


def min_errors(ct, p, alphabet, kind):
    n = {ch: k for k, ch in enumerate(alphabet)}
    classes = {}
    for i, ch in CRIB.items():
        classes.setdefault(i % p, []).append(TYPES[kind](n[ch], n[ct[i]]))
    return sum(len(v) - Counter(v).most_common(1)[0][1] for v in classes.values())


def best_min_errors(ct, p):
    return min(min_errors(ct, p, a, t) for a in (AZ, KA) for t in TYPES)


def table(periods, n_shuffles, seed=700):
    rng = random.Random(seed)
    letters = list(K4)
    shuf = []
    for _ in range(n_shuffles):
        rng.shuffle(letters)
        shuf.append("".join(letters))
    return {p: {"K4": best_min_errors(K4, p), "shuffles": sorted(best_min_errors(s, p) for s in shuf)}
            for p in periods}
