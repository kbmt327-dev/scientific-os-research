"""Charts whose row at each position is chosen from a fixed list of keyed alphabets (EP-0098, EP-0114).

Selection-free cover: for a list of rows, count the crib positions that at least one row can explain.  If the count
is below 24, no rule for choosing rows -- in any order, by any position formula -- can produce the crib from that
list.  Conventions (EP-0114): m1 C = row[a(P)], m2 C = index of P in the row, m3 as m2 read in KRYPTOS order,
m4 C = row[k(P)] with k the KRYPTOS index, m5g C = row[(index of P in row) + g] (a cylinder read g places on).
Standard library only.
"""
import random

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = sorted(CRIB)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
LISTS = {
    "keywords": """KRYPTOS PALIMPSEST ABSCISSA BERLIN CLOCK BERLINCLOCK WORLDCLOCK WELTZEITUHR ALEXANDERPLATZ
EASTNORTHEAST NORTHEAST LAYERTWO EGYPT CARTER HOWARDCARTER TUTANKHAMUN SANBORN SCHEIDT LANGLEY IQLUSION
UNDERGRUUND DESPARATLY SHADOWFORCES LUCIDMEMORY VIRTUALLYINVISIBLE TISYOURPOSITION DIGETALINTERPRETATIU
MESSAGE DELIVERINGAMESSAGE BERLINWALL NOVEMBER NINETEENEIGHTYNINE ANTIPODES LODESTONE COMPASS SHADOW LIGHT
ILLUSION NUANCE PYRAMID""".split(),
    "John832": "AND YE SHALL KNOW THE TRUTH AND THE TRUTH SHALL MAKE YOU FREE".split(),
}
CONVS = ["m1", "m2", "m3", "m4"] + ["m5g%d" % g for g in range(1, 26)]


def keyed(word):
    seen = []
    for ch in word + AZ:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


def rows_of(words):
    out = []
    for w in words:
        r = keyed(w)
        if r not in out:
            out.append(r)
    return out


def output(row, p, conv):
    if conv == "m1":
        return row[AZ.index(p)]
    ip = row.index(p)
    if conv == "m2":
        return AZ[ip]
    if conv == "m3":
        return KA[ip]
    if conv == "m4":
        return row[KA.index(p)]
    return row[(ip + int(conv[3:])) % 26]


def cover(rows, ct, conv):
    return sum(any(output(r, CRIB[i], conv) == ct[i] for r in rows) for i in POS)


def cover_all(rows, ct):
    return {c: cover(rows, ct, c) for c in CONVS}


def null_share(rows, n, seed=1140):
    """share of shuffled K4 texts whose best cover over conventions is at least K4's"""
    k4 = max(cover_all(rows, K4).values())
    rng = random.Random(seed)
    letters = list(K4)
    ge = 0
    best = []
    for _ in range(n):
        rng.shuffle(letters)
        b = max(cover_all(rows, "".join(letters)).values())
        best.append(b)
        ge += b >= k4
    best.sort()
    return {"k4_best": k4, "null_median": best[n // 2], "share_ge_k4": ge / n}
