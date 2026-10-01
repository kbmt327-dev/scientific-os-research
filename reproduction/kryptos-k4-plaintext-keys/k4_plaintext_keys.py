"""Keys that depend on the plaintext history (EP-0150, EP-0179): crib-only consistency checks.
Standard library only.

EP-0150  plaintext autokey with lag L (k_i = primer_i for i < L, k_i = P_{i-L} afterwards), Vigenere / Beaufort /
         variant Beaufort over A-Z or KRYPTOS.  Along each residue class mod L the table is invertible both ways,
         so one known plaintext letter fixes the whole class; no primer search is needed.  'conflicts' = crib
         letters of a class that disagree with the best anchor in that class, summed over classes.
EP-0179  periodic key K[j mod p] whose index j advances one extra step after a plaintext letter in a set V:
         j_{i+1} = j_i + 1 + [P_i in V].  Inside each crib the plaintext is known, so the relative index of every
         crib letter is fixed; the offset delta between the two cribs is free (0..p-1).
         shift tables (A-Z / KRYPTOS x Vig / Beau / VBeau): crib letters on the same index need the same key;
         arbitrary rows: the (P, C) pairs on the same index must form a partial one-to-one map.
         A cell (V, p) passes if some delta gives no conflict.
"""
from itertools import combinations

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
N = 97
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ALPHABETS = (("AZ", AZ), ("KA", KA))
DIRS = ("Vig", "Beau", "VBeau")


# ---- EP-0150: plaintext autokey with lag L --------------------------------------------------------------------
def encipher(A, d, p, k):
    """index arithmetic of the three tables; p, k are indices in A"""
    return A[(p + k) % 26] if d == "Vig" else A[(k - p) % 26] if d == "Beau" else A[(p - k) % 26]


def key_of(A, d, c, p):
    c, p = A.index(c), A.index(p)
    return (c - p) % 26 if d == "Vig" else (c + p) % 26 if d == "Beau" else (p - c) % 26


def dec(A, d, c, k):
    c = A.index(c)
    return A[(c - k) % 26] if d == "Vig" else A[(k - c) % 26] if d == "Beau" else A[(c + k) % 26]


def autokey_conflicts(ct, A, d, L, crib=CRIB):
    """(conflicting crib letters, checks) for plaintext autokey with lag L"""
    tot = chk = 0
    for r in range(L):
        cps = [i for i in range(r, N, L) if i in crib]
        if len(cps) < 2:
            continue
        chk += len(cps) - 1
        best = None
        for a in cps:
            P = {a: crib[a]}
            j = a
            while j + L < N:                                   # forward: key of j+L is P_j
                P[j + L] = dec(A, d, ct[j + L], A.index(P[j]))
                j += L
            j = a
            while j - L >= 0:                                  # backward: P_{j-L} is the key of j
                P[j - L] = A[key_of(A, d, ct[j], P[j])]
                j -= L
            bad = sum(P[i] != crib[i] for i in cps)
            best = bad if best is None else min(best, bad)
        tot += best
    return tot, chk


def autokey_plant(rng, A, d, L):
    """random letters with the cribs written in, random primer; returns the ciphertext"""
    P = [rng.choice(A) for _ in range(N)]
    for i, c in CRIB.items():
        P[i] = c
    primer = [rng.randrange(26) for _ in range(L)]
    return "".join(encipher(A, d, A.index(P[i]), primer[i] if i < L else A.index(P[i - L])) for i in range(N))


# ---- EP-0179: plaintext-indexed periodic key ------------------------------------------------------------------
C1 = list(range(21, 34))
C2 = list(range(63, 74))
# Only the crib letters that are followed by another crib letter move a relative index.
RELEVANT = "".join(sorted({CRIB[i] for i in C1[:-1] + C2[:-1]}))
VOW = set("AEIOU")
# The sets of the record that need no other text: 26 single letters, vowels / consonants, halves of the alphabet.
# (The record's 28 further sets are the letter sets of 14 words from another part of the sculpture and their
# complements; they are not printed here.  The exhaustive check below covers every possible V.)
PUBLIC_SETS = [(c, {c}) for c in AZ] + [("vowels", VOW), ("vowels+Y", VOW | {"Y"}),
                                        ("consonants", set(AZ) - VOW), ("consonants-Y", set(AZ) - VOW - {"Y"}),
                                        ("A-M", set(AZ[:13])), ("N-Z", set(AZ[13:]))]


def rel_index(run, V):
    j, out = 0, []
    for i in run:
        out.append(j)
        j += 1 + (CRIB[i] in V)
    return out


def classes(V, p, delta):
    g = {}
    for i, j in zip(C1, rel_index(C1, V)):
        g.setdefault(j % p, []).append(i)
    for i, j in zip(C2, rel_index(C2, V)):
        g.setdefault((j + delta) % p, []).append(i)
    return [c for c in g.values() if len(c) > 1]


def crib_keys(ct):
    """key index of every crib letter under each of the six shift tables"""
    return [{i: key_of(A, d, ct[i], CRIB[i]) for i in CRIB} for _, A in ALPHABETS for d in DIRS]


def fixed_ok(ct, V, p, keys=None):
    keys = keys or crib_keys(ct)
    for delta in range(p):
        cl = classes(V, p, delta)
        for kv in keys:
            if all(len({kv[i] for i in c}) == 1 for c in cl):
                return True
    return False


def rows_ok(ct, V, p):
    for delta in range(p):
        if all((CRIB[a] == CRIB[b]) == (ct[a] == ct[b]) for c in classes(V, p, delta) for a, b in combinations(c, 2)):
            return True
    return False


def indexed_plant(rng, V, p, A, d):
    K = [rng.randrange(26) for _ in range(p)]
    P = [rng.choice(AZ) for _ in range(N)]
    for i, c in CRIB.items():
        P[i] = c
    j, ct = rng.randrange(p), []
    for i in range(N):
        ct.append(encipher(A, d, A.index(P[i]), K[j % p]))
        j += 1 + (P[i] in V)
    return "".join(ct)


def all_relevant_subsets():
    """every V up to equivalence: only V & RELEVANT matters inside the cribs (2^12 classes)"""
    for r in range(len(RELEVANT) + 1):
        for s in combinations(RELEVANT, r):
            yield set(s)
