"""One phase break added to machines already closed on K4 (EP-0168, with EP-0176 recorded).

A break at position b shifts the machine's step state by t (t = 1..25) for every letter from b on.
Only b between crib letters matters (b = 22..73); with the 24 crib positions, b only decides how many
crib letters are unbroken (the split m), so 52 x 25 = 1,300 (b, t) reduce to 23 x 25 = 575 classes.

The exact single-rotor test (free wiring R, alphabet s, step d per letter; EP-0083):
    u_j = s(P_j) + d*p_j, v_j = s(C_j) + d*p_j, and with the break u_j, v_j += t for j >= m.
A wiring exists iff (u_j = u_k) <=> (v_j = v_k) over the 24 crib letters.  Standard library only.
"""
import math
import random
from itertools import product

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = sorted(CRIB)
PT = [CRIB[i] for i in POS]
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ALPHABETS = {"A-Z": AZ, "KRYPTOS": KA}
B_RANGE = range(22, 74)
T_RANGE = range(1, 26)


def split_of(b):
    """number of crib letters before position b (the unbroken part)"""
    return sum(p < b for p in POS)


def split_classes():
    """{split m: [b values]} for b = 22..73"""
    out = {}
    for b in B_RANGE:
        out.setdefault(split_of(b), []).append(b)
    return out


def counts():
    cls = split_classes()
    n_bt = len(B_RANGE) * len(T_RANGE)
    n_cls = len(cls) * len(T_RANGE)
    ra = 274 * 274 * 26                 # R-a: (s1, s2, d) over 274 alphabets
    rb = 274 * 329_366                  # R-b: alphabet x position-only keys
    en = 3 * 6 * 2 * 26 ** 4 * 676      # Enigma + free entry substitution (EP-0132 settings)
    groups = len(set(PT))
    p_pass = 26.0 ** -(24 - groups) * math.prod(1 - k / 26 for k in range(groups))
    return {
        "splits": len(cls), "b_values": len(B_RANGE), "b_in_largest_split": max(len(v) for v in cls.values()),
        "classes": n_cls, "bt": n_bt, "bits_bt": math.log2(n_bt), "bits_classes": math.log2(n_cls),
        "settings": {"R-a": ra, "R-b": rb, "Enigma+sigma": en},
        "bits_with_break": {k: math.log2(v * n_bt) for k, v in (("R-a", ra), ("R-b", rb), ("Enigma+sigma", en))},
        "crib_letter_groups": groups, "enigma_p_pass": p_pass,
        "enigma_expected_false": p_pass * en * n_cls, "enigma_expected_false_no_break": p_pass * en,
    }


def uv(ct, alphabet, d):
    n = {ch: k for k, ch in enumerate(alphabet)}
    return ([(n[p] + d * i) % 26 for p, i in zip(PT, POS)],
            [(n[ct[i]] + d * i) % 26 for i in POS])


def passing_classes(u, v):
    """[(m, t)] for which one wiring fits with crib letters j >= m shifted by t (exact, bitmask form)"""
    out = []
    for m in range(1, 24):
        ok = all((u[j] == u[k]) == (v[j] == v[k]) for j in range(m) for k in range(j + 1, m)) and \
             all((u[j] == u[k]) == (v[j] == v[k]) for j in range(m, 24) for k in range(j + 1, 24))
        if not ok:
            continue
        bad = 0
        for j in range(m):
            for k in range(m, 24):
                du, dv = (u[j] - u[k]) % 26, (v[j] - v[k]) % 26
                if du != dv:          # cross pair: shift t must not make exactly one side equal
                    bad |= (1 << du) | (1 << dv)
        out += [(m, t) for t in T_RANGE if not bad >> t & 1]
    return out


def passing_classes_ref(u, v):
    """brute force over (m, t): build the wiring and check it is a permutation"""
    out = []
    for m, t in product(range(1, 24), T_RANGE):
        f, g, ok = {}, {}, True
        for j in range(24):
            a, b = (u[j] + (t if j >= m else 0)) % 26, (v[j] + (t if j >= m else 0)) % 26
            if f.setdefault(a, b) != b or g.setdefault(b, a) != a:
                ok = False
                break
        if ok:
            out.append((m, t))
    return out


def single_rotor_passes(ct):
    """(alphabet, d, m, t) passing for the EP-0083 single rotor (s1 = s2 in {A-Z, KRYPTOS}, d = 0..25)"""
    return [(name, d, m, t) for name, al in ALPHABETS.items() for d in range(26)
            for m, t in passing_classes(*uv(ct, al, d))]


def shuffled(seed):
    """the shuffle convention of the author's code (seed 0 = K4)"""
    if seed == 0:
        return K4
    x = list(K4)
    random.Random(seed).shuffle(x)
    return "".join(x)


def encrypt(pt, alphabet, wiring, s, d, b, t):
    n = {ch: k for k, ch in enumerate(alphabet)}
    out = []
    for i, ch in enumerate(pt):
        o = s + d * i + (t if i >= b else 0)
        out.append(alphabet[(wiring[(n[ch] + o) % 26] - o) % 26])
    return "".join(out)


def planted_controls(n, seed=1681):
    """random plaintext with the cribs, a random wiring, alphabet, step, start and break; the planted
    (alphabet, d, m, t) must be among the passes"""
    rng = random.Random(seed)
    found = 0
    for _ in range(n):
        w = list(range(26))
        rng.shuffle(w)
        pt = "".join(CRIB.get(i, rng.choice(AZ)) for i in range(97))
        name = rng.choice(list(ALPHABETS))
        d, s, b, t = rng.randrange(26), rng.randrange(26), rng.choice(B_RANGE), rng.choice(T_RANGE)
        ct = encrypt(pt, ALPHABETS[name], w, s, d, b, t)
        found += (split_of(b), t) in passing_classes(*uv(ct, ALPHABETS[name], d))
    return found
