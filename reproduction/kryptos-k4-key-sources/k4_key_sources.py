"""Testing key sources without knowing the chart (EP-0092, EP-0093, EP-0100).

A key source assigns a symbol X_i to each position (a keyword letter, a digit, i mod p, ...).  If the chart is a
Latin square (each row a permutation of the alphabet and, for each plaintext letter, different rows give different
ciphertext letters), then over the crib:
    same X and same P  ->  same C          same X and different P -> different C
    same P and same C  ->  same X          same C and different P -> different X
A source that breaks any of these is impossible whatever the chart's contents.  Also the vertical-repeat phenomenon
at width 21 (Bean 2021), priced over the widths scanned.  Standard library only.
"""
import random
from itertools import combinations

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = sorted(CRIB)
PAIRS = list(combinations(POS, 2))
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KEYWORDS = """KRYPTOS PALIMPSEST ABSCISSA BERLIN CLOCK BERLINCLOCK WORLDCLOCK WELTZEITUHR ALEXANDERPLATZ
EASTNORTHEAST NORTHEAST LAYERTWO EGYPT CARTER HOWARDCARTER TUTANKHAMUN SANBORN SCHEIDT LANGLEY IQLUSION
UNDERGRUUND DESPARATLY SHADOWFORCES LUCIDMEMORY VIRTUALLYINVISIBLE TISYOURPOSITION DIGETALINTERPRETATIU
MESSAGE DELIVERINGAMESSAGE BERLINWALL NOVEMBER NINETEENEIGHTYNINE ANTIPODES LODESTONE COMPASS SHADOW LIGHT
ILLUSION NUANCE PYRAMID""".split()
DIGITS = ["1986", "1989", "19891109", "09111989", "11091989", "1990", "19901103", "38576577844", "385765",
          "77844", "1922", "19221126"]


def violations(x, latin=True, ct=K4):
    """number of crib position pairs that break the chart rules for key symbols x (a dict or list by position)"""
    bad = 0
    for i, j in PAIRS:
        xe, pe, ce = x[i] == x[j], CRIB[i] == CRIB[j], ct[i] == ct[j]
        v = xe and pe != ce
        if latin:
            v = v or (pe and xe != ce) or (ce and xe != pe)
        bad += v
    return bad


def cyclic_source(s, phase):
    return [s[(i + phase) % len(s)] for i in range(97)]


def keyword_sources(words):
    return [(w, ph, cyclic_source(w, ph)) for w in words for ph in range(len(w))]


def pass_count(sources, latin=True):
    return sum(violations(x, latin) == 0 for _, _, x in sources)


def period_passes(latin=True):
    return [p for p in range(2, 49) if violations([i % p for i in range(97)], latin) == 0]


def decoy_keyword_null(n, seed=930):
    """pass counts for decoy lists: random letter strings with the same lengths as the keywords"""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        decoys = ["".join(rng.choice(AZ) for _ in w) for w in KEYWORDS]
        out.append(pass_count(keyword_sources(decoys)))
    return out


def decoy_digit_null(n, seed=931):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        decoys = ["".join(rng.choice("0123456789") for _ in d) for d in DIGITS]
        out.append(pass_count(keyword_sources(decoys)))
    return out


WIDTHS = range(2, 49)


def vertical_repeats(ct, w):
    """number of vertical bigram types (C_i, C_{i+w}) that occur at least twice"""
    seen = {}
    for i in range(len(ct) - w):
        k = ct[i] + ct[i + w]
        seen[k] = seen.get(k, 0) + 1
    return sum(1 for v in seen.values() if v >= 2)


def width_scan(n, seed=933):
    """P(count >= K4's) at width 21 alone, and the scan-corrected P: how often a permutation of K4 reaches, at some
    width, a tail probability as small as K4's smallest"""
    rng = random.Random(seed)
    letters = list(K4)
    perms = []
    for _ in range(n):
        rng.shuffle(letters)
        perms.append([vertical_repeats(letters, w) for w in WIDTHS])
    k4 = [vertical_repeats(K4, w) for w in WIDTHS]
    tail = []
    for k, w in enumerate(WIDTHS):
        col = sorted(p[k] for p in perms)
        tail.append({v: sum(1 for c in col if c >= v) / n for v in set(col) | {k4[k]}})
    k4_min = min(tail[k][k4[k]] for k in range(len(WIDTHS)))
    perm_min = [min(tail[k][p[k]] for k in range(len(WIDTHS))) for p in perms]
    return {"k4_counts": dict(zip(WIDTHS, k4)), "p_width21": tail[WIDTHS.index(21)][k4[WIDTHS.index(21)]],
            "k4_min_tail": k4_min, "p_scan": sum(1 for m in perm_min if m <= k4_min) / n}
