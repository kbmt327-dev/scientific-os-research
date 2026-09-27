"""Position-varying affine maps and periodic Hill matrices on K4 (EP-0117), exact tests on the cribs.

  * Affine: C = a_i * P + b_i (or P = a_i * C + b_i), with a_i and b_i polynomials of degree <= 2 in the position
    (mod 26) and a_i invertible at all 97 positions; numbers from A-Z or the KRYPTOS alphabet.
  * Hill, 2x2, no constant vector: the text is cut into blocks of two from offset o; block t uses matrix
    M_(t mod p).  Each row of each matrix must satisfy one linear equation per crib block; the matrix must be
    invertible.  Every row is enumerated, so the test is exact.
Standard library only.
"""
import random
from math import gcd

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
POS = sorted(CRIB)
UNITS = [u for u in range(26) if gcd(u, 26) == 1]


def poly(c, i):
    return (c[0] + c[1] * i + c[2] * i * i) % 26


A_POLYS = [(a0, a1, a2) for a0 in range(26) for a1 in range(26) for a2 in range(26)
           if all(gcd(poly((a0, a1, a2), i), 26) == 1 for i in range(97))]


def affine_fits(ct, alphabet, direction, crib=CRIB):
    """all (a-poly, b1, b2, b0) that reproduce every crib letter"""
    n = {ch: k for k, ch in enumerate(alphabet)}
    if direction == "enc":
        x = {i: n[crib[i]] for i in POS}
        y = {i: n[ct[i]] for i in POS}
    else:
        x = {i: n[ct[i]] for i in POS}
        y = {i: n[crib[i]] for i in POS}
    fits = []
    i0 = POS[0]
    for a in A_POLYS:
        r = {i: (y[i] - poly(a, i) * x[i]) % 26 for i in POS}
        for b1 in range(26):
            for b2 in range(26):
                b0 = (r[i0] - b1 * i0 - b2 * i0 * i0) % 26
                if all((b0 + b1 * i + b2 * i * i) % 26 == r[i] for i in POS):
                    fits.append((a, b0, b1, b2))
    return fits


def affine_encrypt(pt, alphabet, a, b):
    n = {ch: k for k, ch in enumerate(alphabet)}
    return "".join(alphabet[(poly(a, i) * n[ch] + poly(b, i)) % 26] for i, ch in enumerate(pt))


def affine_controls(n_plants, seed=1170):
    rng = random.Random(seed)
    found = 0
    for _ in range(n_plants):
        pt = [rng.choice(AZ) for _ in range(97)]
        for i, ch in CRIB.items():
            pt[i] = ch
        alph = rng.choice((AZ, KA))
        a = rng.choice(A_POLYS)
        b = tuple(rng.randrange(26) for _ in range(3))
        ct = affine_encrypt("".join(pt), alph, a, b)
        found += any(f[0] == a and (f[1], f[2], f[3]) == b for f in affine_fits(ct, alph, "enc"))
    return found


def det_invertible(r1, r2):
    return gcd((r1[0] * r2[1] - r1[1] * r2[0]) % 26, 26) == 1


def hill_consistent(ct, alphabet, o, p, crib=CRIB):
    """True / False: is there, for each class t mod p, an invertible 2x2 matrix mapping every crib block?"""
    n = {ch: k for k, ch in enumerate(alphabet)}
    blocks = {}
    for t, s in enumerate(range(o, 96, 2)):
        if s in crib and s + 1 in crib:
            blocks.setdefault(t % p, []).append(((n[crib[s]], n[crib[s + 1]]), (n[ct[s]], n[ct[s + 1]])))
    for eqs in blocks.values():
        rows = []
        for k in (0, 1):
            ok = [(u, v) for u in range(26) for v in range(26)
                  if all((u * pp[0] + v * pp[1]) % 26 == cc[k] for pp, cc in eqs)]
            rows.append(ok)
        if not any(det_invertible(r1, r2) for r1 in rows[0] for r2 in rows[1]):
            return False
    return True


def hill_settings():
    return [(name, alph, o, p) for name, alph in (("A-Z", AZ), ("KRYPTOS", KA)) for o in (0, 1) for p in range(1, 9)]


def hill_shuffle_consistent(n_shuffles, seed=1171):
    """per setting, how many shuffled K4 texts are consistent (the test's power)"""
    rng = random.Random(seed)
    letters = list(K4)
    counts = {(name, o, p): 0 for name, _, o, p in hill_settings()}
    for _ in range(n_shuffles):
        rng.shuffle(letters)
        ct = "".join(letters)
        for name, alph, o, p in hill_settings():
            counts[(name, o, p)] += hill_consistent(ct, alph, o, p)
    return counts


def hill_encrypt(pt, alphabet, o, mats):
    n = {ch: k for k, ch in enumerate(alphabet)}
    out = list(pt)
    for t, s in enumerate(range(o, 96, 2)):
        (a, b), (c, d) = mats[t % len(mats)]
        x, y = n[pt[s]], n[pt[s + 1]]
        out[s], out[s + 1] = alphabet[(a * x + b * y) % 26], alphabet[(c * x + d * y) % 26]
    return "".join(out)


def hill_controls(n_plants, seed=1172):
    rng = random.Random(seed)
    ok = 0
    for _ in range(n_plants):
        pt = [rng.choice(AZ) for _ in range(97)]
        for i, ch in CRIB.items():
            pt[i] = ch
        name, alph = rng.choice((("A-Z", AZ), ("KRYPTOS", KA)))
        o, p = rng.randrange(2), rng.randrange(1, 9)
        mats = []
        while len(mats) < p:
            r1, r2 = (rng.randrange(26), rng.randrange(26)), (rng.randrange(26), rng.randrange(26))
            if det_invertible(r1, r2):
                mats.append((r1, r2))
        ok += hill_consistent(hill_encrypt("".join(pt), alph, o, mats), alph, o, p)
    return ok


def affine_shuffles(n_shuffles, seed=1173):
    rng = random.Random(seed)
    letters = list(K4)
    hits = 0
    for _ in range(n_shuffles):
        rng.shuffle(letters)
        ct = "".join(letters)
        hits += any(affine_fits(ct, a, d) for a in (AZ, KA) for d in ("enc", "dec"))
    return hits
