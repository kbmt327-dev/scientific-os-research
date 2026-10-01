"""Crib-only parts of EP-0180 (Morse mask), EP-0181 (digit-wise addition), EP-0182 (W as a null in the key index)
and EP-0183 (reversed key direction).  Standard library only.

  * W as a null: the key index of carved letter i is J = i - (number of W before i).  The five W sit at 20, 36,
    48, 58 and 74, none inside a crib, so crib 1 moves by -1 and crib 2 by -4 (relative shift -3).
  * Reversed direction: in a stride family k_i = S[(a*J + b) mod L] with every a in 1..L-1 and every b in 0..L-1,
    reading J backwards (J' = n - 1 - J) or reading S from its end gives exactly the same set of key sequences.
  * Morse mask (pure form): C_i = Morse^-1(g_i(Morse(P_i))) with g in {identity, invert dots and dashes, reverse,
    invert and reverse}.  All four keep the length of the Morse code, so a crib position whose plaintext and
    ciphertext letters have Morse codes of different length (or no g linking them) cannot be met.
  * Digit-wise addition: letter -> two decimal digits, add (or subtract) two stream digits mod 10 without carry,
    fold mod 26.  Only the mechanism and planted controls on random streams are here; the 22 fixed strings of the
    episode are not published, and their K4 counts are recorded.
"""
import random
from itertools import product

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
N = len(K4)
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
CI = sorted(CRIB)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ------------------------------------------------------------------ W as a null (EP-0182)
WPOS = [i for i, c in enumerate(K4) if c == "W"]


def wskip(i):
    return i - sum(1 for w in WPOS if w < i)


def crib_shifts():
    """shift of each crib under the W-skipping index, and whether any W lies inside a crib"""
    out = {s: sorted({wskip(s + k) - (s + k) for k in range(len(w))}) for s, w in CRIBS.items()}
    inside = [w for w in WPOS if w in CRIB]
    return out, inside


# ------------------------------------------------------------------ reversed direction (EP-0183)
def family(L, J):
    """all key-index sequences (a*J + b) mod L, a in 1..L-1, b in 0..L-1, over the positions J"""
    return {tuple((a * j + b) % L for j in J) for a in range(1, L) for b in range(L)}


def reversed_text(L, J):
    """the same family read on S reversed: index L-1-x into S"""
    return {tuple(L - 1 - x for x in t) for t in family(L, J)}


def direction_identity(lengths):
    """True for every L where rev, revtext, wskip_rev and wskip_revtext give the forward family's key sequences"""
    pos = range(N)
    J_id = list(pos)
    J_rev = [N - 1 - i for i in pos]
    J_ws = [wskip(i) for i in pos]
    nonw = N - len(WPOS)
    J_wsrev = [nonw - 1 - wskip(i) for i in pos]
    bad = []
    for L in lengths:
        f_id, f_ws = family(L, J_id), family(L, J_ws)
        if not (family(L, J_rev) == f_id == reversed_text(L, J_id)
                and family(L, J_wsrev) == f_ws == reversed_text(L, J_ws)):
            bad.append(L)
    return bad


# ------------------------------------------------------------------ Morse mask (EP-0180)
MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
         'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
         'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
         'Y': '-.--', 'Z': '--..'}
G_NAMES = ("identity", "invert", "reverse", "invert+reverse")


def g_op(g, s):
    if g & 1:
        s = s.translate(str.maketrans(".-", "-."))
    if g & 2:
        s = s[::-1]
    return s


def morse_admissible():
    """for each crib position, the operations g with Morse^-1(g(Morse(P))) = C"""
    return {i: [G_NAMES[g] for g in range(4) if g_op(g, MORSE[CRIB[i]]) == MORSE[K4[i]]] for i in CI}


def morse_length_mismatch():
    return [i for i in CI if len(MORSE[CRIB[i]]) != len(MORSE[K4[i]])]


# ------------------------------------------------------------------ digit-wise addition (EP-0181)
def digit_f(x, dd, eb, db, sign):
    """letter index x -> two digits of x + eb, add sign * (d0, d1) digit-wise mod 10, -> (10t + u - db) mod 26"""
    v = x + eb
    t, u = (v // 10 + sign * dd[0]) % 10, (v % 10 + sign * dd[1]) % 10
    return (10 * t + u - db) % 26


def digit_settings(streams, offsets=61):
    out, seen = [], set()
    for name, s in streams.items():
        for o in range(offsets):
            dig = tuple((int(s[o + 2 * i]), int(s[o + 2 * i + 1])) for i in CI)
            for dr, sg, eb, db in product(("enc", "dec"), (1, -1), (0, 1), (0, 1)):
                k = (dr, sg, eb, db, dig)
                if k not in seen:
                    seen.add(k)
                    out.append((name, o) + k)
    return out


def digit_hits(ct, settings):
    hits = []
    for st in settings:
        name, o, dr, sg, eb, db, dig = st
        ok = True
        for j, i in enumerate(CI):
            p, c = AZ.index(CRIB[i]), AZ.index(ct[i])
            if (digit_f(p, dig[j], eb, db, sg) != c) if dr == "enc" else (digit_f(c, dig[j], eb, db, sg) != p):
                ok = False
                break
        if ok:
            hits.append(st)
    return hits


def digit_plant(rng, streams):
    """a ciphertext made by one random setting on one random stream (crib letters kept)"""
    while True:
        name = rng.choice(sorted(streams))
        s, o = streams[name], rng.randrange(61)
        dr, sg, eb, db = rng.choice(("enc", "dec")), rng.choice((1, -1)), rng.randrange(2), rng.randrange(2)
        pt = [rng.randrange(26) for _ in range(N)]
        for i, c in CRIB.items():
            pt[i] = AZ.index(c)
        ct, ok = [], True
        for i in range(N):
            dd = (int(s[o + 2 * i]), int(s[o + 2 * i + 1]))
            if dr == "enc":
                ct.append(digit_f(pt[i], dd, eb, db, sg))
            else:
                pre = [c for c in range(26) if digit_f(c, dd, eb, db, sg) == pt[i]]
                if not pre:
                    if i in CRIB:
                        ok = False
                        break
                    pre = list(range(26))
                ct.append(rng.choice(pre))
        if ok:
            return "".join(AZ[c] for c in ct), (name, o, dr, sg, eb, db)


def random_streams(rng, n=22, length=400):
    return {f"random-{k}": "".join(rng.choice("0123456789") for _ in range(length)) for k in range(n)}
