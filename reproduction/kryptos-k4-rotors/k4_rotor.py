"""One rotor with completely free wiring, stepped d positions per letter (EP-0083, family H).

At position i the rotor is shifted by o_i = s + d*i, so C_i = T_-o R T_o (P_i) in contact numbers given by an
alphabet (A-Z or KRYPTOS).  Each crib letter gives R(u) = v with u = n(P_i) + o_i and v = n(C_i) + o_i.  A wiring
R exists exactly when u_j = u_k <=> v_j = v_k over the 24 crib letters.  The constant s shifts every u and v alike,
so it never changes the answer; the test runs over d and the numbering.  Standard library only.
"""
import random

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


def wiring_exists(ct, alphabet, d, crib=CRIB):
    n = {ch: k for k, ch in enumerate(alphabet)}
    fwd, back = {}, {}
    for i, p in crib.items():
        u, v = (n[p] + d * i) % 26, (n[ct[i]] + d * i) % 26
        if fwd.setdefault(u, v) != v or back.setdefault(v, u) != u:
            return False
    return True


def passing_settings(ct):
    return [(name, d) for name, alph in (("A-Z", AZ), ("KRYPTOS", KA)) for d in range(26)
            if wiring_exists(ct, alph, d)]


def encrypt(pt, alphabet, wiring, s, d):
    n = {ch: k for k, ch in enumerate(alphabet)}
    out = []
    for i, ch in enumerate(pt):
        o = s + d * i
        out.append(alphabet[(wiring[(n[ch] + o) % 26] - o) % 26])
    return "".join(out)


def planted_controls(n, seed=830):
    rng = random.Random(seed)
    found = 0
    for _ in range(n):
        pt = [rng.choice(AZ) for _ in range(97)]
        for i, ch in CRIB.items():
            pt[i] = ch
        name, alph = rng.choice((("A-Z", AZ), ("KRYPTOS", KA)))
        d, s = rng.randrange(26), rng.randrange(26)
        wiring = list(range(26))
        rng.shuffle(wiring)
        ct = encrypt("".join(pt), alph, wiring, s, d)
        found += (name, d) in passing_settings(ct)
    return found


def shuffle_null(n, seed=831):
    rng = random.Random(seed)
    letters = list(K4)
    hits = 0
    for _ in range(n):
        rng.shuffle(letters)
        hits += bool(passing_settings("".join(letters)))
    return hits
