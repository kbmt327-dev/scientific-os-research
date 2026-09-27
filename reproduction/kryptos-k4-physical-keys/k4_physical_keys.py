"""Keys read off the sculpture's physical form, tested without measuring the shape (EP-0066, EP-0068).

Layout (from photographs, EP-0066): K4 occupies row 24 columns 27-30 and rows 25-27 (31 letters each), right-aligned
with the seam, so K4 position i sits at row 25 + (i - 4) // 31, column (i - 4) % 31 for i >= 4.  Crib positions
32 and 63 share column 28, and 33 and 64 share column 29.

  * A key that depends only on horizontal position needs k(32) = k(63) and k(33) = k(64); a key that is a sum of
    a horizontal and a vertical part needs k(32) - k(63) = k(33) - k(64).
  * A key read off a smooth map (shadow-edge time, sight-line overlap) has small second differences along rows
    and a small 2x2 cross difference.  S = the largest of these (in units of the key's step, the best of 12 unit
    multipliers, 6 conventions and two letter numberings); compared with random crib ciphertext.
Standard library only.
"""
import random

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
TYPES = {"Vigenere": lambda x, y: (y - x) % 26, "Beaufort": lambda x, y: (y + x) % 26,
         "variant": lambda x, y: (x - y) % 26}
UNITS = [u for u in range(1, 26) if u % 2 and u != 13]


def place(i):
    if i < 4:
        return 24, 27 + i
    return 25 + (i - 4) // 31, (i - 4) % 31


def keys(ct, alph, kind):
    n = {ch: k for k, ch in enumerate(alph)}
    return {i: TYPES[kind](n[CRIB[i]], n[ct[i]]) for i in CRIB}


def column_table(ct=K4):
    out = {}
    for an, alph in (("A-Z", AZ), ("KRYPTOS", KA)):
        for kind in TYPES:
            k = keys(ct, alph, kind)
            out[f"{kind} {an}"] = {"k32_k63_k33_k64": [k[32], k[63], k[33], k[64]],
                                   "horizontal_only": k[32] == k[63] and k[33] == k[64],
                                   "horizontal_plus_vertical": (k[32] - k[63]) % 26 == (k[33] - k[64]) % 26}
    return out


def sym(x):
    x %= 26
    return x - 26 if x > 13 else x


RUNS = [list(range(21, 34)), [63, 64, 65], list(range(66, 74))]


def roughness(ct):
    best = 99
    for alph in (AZ, KA):
        for kind in TYPES:
            k = keys(ct, alph, kind)
            for numbering in (AZ, KA):
                v = {i: numbering.index(alph[k[i]]) for i in k}
                for m in UNITS:
                    inv = pow(m, -1, 26)
                    nn = {i: v[i] * inv % 26 for i in v}
                    diffs = [sym(nn[r[j + 2]] - 2 * nn[r[j + 1]] + nn[r[j]]) for r in RUNS for j in range(len(r) - 2)]
                    diffs.append(sym(nn[32] - nn[33] - nn[63] + nn[64]))
                    best = min(best, max(abs(d) for d in diffs))
    return best


def random_roughness(n, seed=680):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        ct = [rng.choice(AZ) for _ in range(97)]
        out.append(roughness("".join(ct)))
    return out
