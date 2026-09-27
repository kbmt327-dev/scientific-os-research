"""K4 with the Ws taken out as separators, enciphered with 25-letter squares (EP-0110, 0120, 0125, 0126).

Exact checks that need only K4 and its public cribs:
  * Four-square with two completely free cipher squares (plain squares standard or keyed);
  * the self-encryption argument against Two-square in every corner convention;
  * doubled ciphertext pairs, which rule out Playfair as the last step.
Standard library only.
"""
import random

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A25 = AZ.replace("W", "")
KEEP = [i for i in range(97) if K4[i] != "W"]
RED = "".join(K4[i] for i in KEEP)                        # the 92 letters, 25 letter types
RIDX = {i: n for n, i in enumerate(KEEP)}
CR = {RIDX[i]: ch for i, ch in CRIB.items()}               # the crib in reduced positions (20-32, 59-69)
SEG_STARTS = [RIDX[i + 1] for i in range(96) if K4[i] == "W" and i + 1 in RIDX]
SEG_STARTS = [0] + [s for s in SEG_STARTS if s > 0]

# hint keywords used for keyed plain squares (EP-0110)
KEYWORDS = """KRYPTOS PALIMPSEST ABSCISSA BERLIN CLOCK BERLINCLOCK WORLDCLOCK WELTZEITUHR ALEXANDERPLATZ
EASTNORTHEAST NORTHEAST LAYERTWO EGYPT CARTER HOWARDCARTER TUTANKHAMUN SANBORN SCHEIDT LANGLEY IQLUSION
UNDERGRUUND DESPARATLY SHADOWFORCES LUCIDMEMORY VIRTUALLYINVISIBLE TISYOURPOSITION DIGETALINTERPRETATIU
MESSAGE DELIVERINGAMESSAGE BERLINWALL NOVEMBER NINETEENEIGHTYNINE ANTIPODES LODESTONE COMPASS SHADOW LIGHT
ILLUSION NUANCE PYRAMID""".split()


def square(word=""):
    seen = []
    for ch in word.upper() + A25:
        if ch in A25 and ch not in seen:
            seen.append(ch)
    return "".join(seen)


def coords(sq):
    return {ch: divmod(k, 5) for k, ch in enumerate(sq)}


def pairs(mode, n=92):
    """digraph positions in the reduced text: from 0, from 1, or restarting in each W segment"""
    if mode in (0, 1):
        return [(i, i + 1) for i in range(mode, n - 1, 2)]
    out = []
    bounds = SEG_STARTS + [n]
    for s, e in zip(bounds[:-1], bounds[1:]):
        out += [(i, i + 1) for i in range(s, e - 1, 2)]
    return out


PAIR_MODES = {"0": pairs(0), "1": pairs(1), "seg": pairs("seg")}


def crib_digraphs(mode):
    return [(i, j) for i, j in PAIR_MODES[mode] if i in CR and j in CR]


def foursquare_consistent(text, plain_sq, mode, crib=CR):
    """free cipher squares: each crib digraph fixes one cell of each; consistent iff no cell holds two letters
    and no letter sits in two cells of the same square"""
    cs = coords(plain_sq)
    cells = [{}, {}]
    for i, j in PAIR_MODES[mode]:
        if i in crib and j in crib:
            (ra, ca), (rb, cb) = cs[crib[i]], cs[crib[j]]
            for q, cell, letter in ((0, (ra, cb), text[i]), (1, (rb, ca), text[j])):
                if cells[q].setdefault(cell, letter) != letter:
                    return False
    return all(len(set(c.values())) == len(c) for c in cells)


def foursquare_encrypt(pt, plain_sq, q1, q2, mode):
    cs = coords(plain_sq)
    out = list(pt)
    for i, j in PAIR_MODES[mode]:
        (ra, ca), (rb, cb) = cs[pt[i]], cs[pt[j]]
        out[i], out[j] = q1[ra * 5 + cb], q2[rb * 5 + ca]
    return "".join(out)


def planted_controls(n, seed=1100):
    """random 92-letter plaintext with the cribs written in, enciphered by a true Four-square with random cipher
    squares; the exact test must call every one consistent"""
    rng = random.Random(seed)
    ok = 0
    for t in range(n):
        pt = [rng.choice(A25) for _ in range(92)]
        for i, ch in CR.items():
            pt[i] = ch
        mode = list(PAIR_MODES)[t % 3]
        q1, q2 = "".join(rng.sample(A25, 25)), "".join(rng.sample(A25, 25))
        ct = foursquare_encrypt("".join(pt), square(), q1, q2, mode)
        ok += foursquare_consistent(ct, square(), mode)
    return ok


def shuffle_null(n, seed=1105):
    rng = random.Random(seed)
    return {m: sum(foursquare_consistent("".join(rng.sample(RED, 92)), square(), m) for _ in range(n)) / n
            for m in PAIR_MODES}


def twosquare_witnesses(mode):
    """crib digraphs that break the Two-square conventions whatever the squares are.
    Standard corners: an output letter equals its plaintext letter only if the other one does too.
    Swapped corners: output 1 equals plaintext 2 exactly when output 2 equals plaintext 1."""
    std, swp = [], []
    for i, j in crib_digraphs(mode):
        p1, p2, c1, c2 = CR[i], CR[j], RED[i], RED[j]
        if (c1 == p1) != (c2 == p2):
            std.append((i, j, p1 + p2, c1 + c2))
        if (c1 == p2) != (c2 == p1):
            swp.append((i, j, p1 + p2, c1 + c2))
    return std, swp


def doubled_ciphertext_pairs(mode):
    """standard Playfair never outputs a doubled pair, so these rule it out as the last step"""
    return [(i, j, RED[i] + RED[j]) for i, j in PAIR_MODES[mode] if RED[i] == RED[j]]
