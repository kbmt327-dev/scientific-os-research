"""Helpers for the premise-audit Note (EP-0188 to EP-0194).  Standard library only.

  crib information and closed forms   bits per crib, the 2-substitution multiplier, injective-consistency
                                      probabilities (free sigma with crib positions dropped)
  2x2 Hill per section (EP-0190 G1)    GL2(Z/26), full blocks inside one crib, exhaustive hit test
  partition-preserving maps (G5)       closed-form chance of passing crib 1
  minimum drop d* (EP-0194)            the number of crib positions that must be dropped before some setting of a
                                       sub-family agrees with the rest of the crib; tables that are arbitrary per
                                       class are handled exactly by maximum-weight bipartite matching

Only the public K4 ciphertext, the 24 public crib letters, the KRYPTOS keyed alphabet, standard English Braille,
the carved-row coordinates of K4 (rows of 4 + 31 + 31 + 31 letters) and the cell geometry of chart #3 (the fold
columns 6 and 25) are used.  No decryption of K4 is printed anywhere.
"""
import itertools
from collections import Counter, defaultdict
from math import comb, log2, prod

try:                                             # optional: only speeds up the 720-permutation Braille scan
    import numpy as np
except ImportError:                              # pragma: no cover
    np = None

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
CI = sorted(CRIB)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


# ---------------------------------------------------------------- closed forms
def crib_bits(n):
    return n * log2(26)


def substitution_multiplier(n=24, j_max=2, alternatives=25):
    """number of plaintexts within j_max substitutions of the crib: sum_j C(n, j) * 25^j"""
    return sum(comb(n, j) * alternatives ** j for j in range(j_max + 1))


def p_injective(letters):
    """chance that uniform values on these positions are equal exactly where the plaintext letters are equal
    (consistency with one free injective substitution)"""
    d = len(set(letters))
    return prod(26 - k for k in range(d)) / 26 ** len(letters)


def drop_sum(letters, max_drop=2):
    """sum over every set D of at most max_drop dropped positions of p_injective(rest); per size"""
    out = []
    idx = range(len(letters))
    for r in range(max_drop + 1):
        out.append(sum(p_injective([letters[i] for i in idx if i not in D]) for D in itertools.combinations(idx, r)))
    return out


# ---------------------------------------------------------------- 2x2 Hill per section (EP-0190 G1)
def gl2():
    """all invertible 2x2 matrices over Z/26, as (a, b, c, d) with C1 = a*P1 + b*P2, C2 = c*P1 + d*P2"""
    out = []
    for a, b, c, d in itertools.product(range(26), repeat=4):
        det = (a * d - b * c) % 26
        if det % 2 and det % 13:
            out.append((a, b, c, d))
    return out


def blocks(start, word, phase):
    """full 2-letter blocks inside the crib whose first index has parity `phase`"""
    i0 = start if start % 2 == phase else start + 1
    return [(i, i + 1) for i in range(i0, start + len(word) - 1, 2)]


def block_values(ct, crib, alpha, phase, pt=None):
    start, word = CRIBS[crib]
    src = pt if pt is not None else CRIB
    return [(alpha.index(src[i]), alpha.index(src[j]), alpha.index(ct[i]), alpha.index(ct[j]))
            for i, j in blocks(start, word, phase)]


def hill_hits_bruteforce(vals, GL):
    """every matrix of GL that maps each plaintext block to its ciphertext block"""
    p1, p2, c1, c2 = vals[0]
    cand = [m for m in GL if (m[0] * p1 + m[1] * p2) % 26 == c1 and (m[2] * p1 + m[3] * p2) % 26 == c2]
    return [m for m in cand if all((m[0] * x + m[1] * y) % 26 == u and (m[2] * x + m[3] * y) % 26 == v
                                   for x, y, u, v in vals[1:])]


def hill_hits_rows(vals):
    """the same set, solved row by row (each row of the matrix meets its own equations), then invertibility"""
    r1 = [(a, b) for a in range(26) for b in range(26) if all((a * x + b * y) % 26 == u for x, y, u, _ in vals)]
    r2 = [(c, d) for c in range(26) for d in range(26) if all((c * x + d * y) % 26 == v for x, y, _, v in vals)]
    return [(a, b, c, d) for a, b in r1 for c, d in r2 if ((a * d - b * c) % 26) % 2 and ((a * d - b * c) % 26) % 13]


def hill_encrypt(text, start, end, m, alpha):
    out = list(text)
    for i in range(start, end - 1, 2):
        p1, p2 = alpha.index(text[i]), alpha.index(text[i + 1])
        out[i] = alpha[(m[0] * p1 + m[1] * p2) % 26]
        out[i + 1] = alpha[(m[2] * p1 + m[3] * p2) % 26]
    return "".join(out)


# ---------------------------------------------------------------- partition-preserving maps (EP-0190 G5)
G5_PARTITIONS = {
    "A-Z halves": ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"],
    "A-Z parity": [AZ[0::2], AZ[1::2]],
    "KRYPTOS halves": [KA[:13], KA[13:]],
    "vowels AEIOU": ["AEIOU", "".join(c for c in AZ if c not in "AEIOU")],
    "vowels AEIOUY": ["AEIOUY", "".join(c for c in AZ if c not in "AEIOUY")],
    "QWERTY rows": ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"],
}
G5_SWAP = ("A-Z halves", "A-Z parity", "KRYPTOS halves")   # two equal blocks: the swap form is added


def g5_pass_chance(name, word="EASTNORTHEAST"):
    """chance that a uniform ciphertext letter lies in the block allowed at every crib-1 position"""
    blk = {ch: len(b) for b in G5_PARTITIONS[name] for ch in b}
    return prod(blk[ch] / 26 for ch in word)


# ---------------------------------------------------------------- minimum drop d* (EP-0194)
def _hungarian_max(w):
    """maximum total weight of a matching in the n x m weight matrix w (exact, O(n^2 m))"""
    n, m = len(w), len(w[0])
    if n > m:
        w = [list(r) for r in zip(*w)]
        n, m = m, n
    big = max(max(r) for r in w)
    cost = [[big - x for x in r] for r in w]
    inf = float("inf")
    u, v, p, way = [0] * (n + 1), [0] * (m + 1), [0] * (m + 1), [0] * (m + 1)
    for i in range(1, n + 1):
        p[0], j0 = i, 0
        minv, used = [inf] * (m + 1), [False] * (m + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], inf, 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    return sum(w[p[j] - 1][j - 1] for j in range(1, m + 1) if p[j])


def max_bijection(pairs):
    """largest number of (p, c) pairs that a partial one-to-one table can satisfy"""
    if not pairs:
        return 0
    cnt = Counter(pairs)
    if len({p for p, _ in cnt}) == len({c for _, c in cnt}) == len(cnt):
        return len(pairs)                        # already a partial one-to-one map
    ps = sorted({p for p, _ in cnt})
    cs = sorted({c for _, c in cnt})
    return _hungarian_max([[cnt.get((p, c), 0) for c in cs] for p in ps])


def dstar_classes(pt, ct, cls):
    g = defaultdict(list)
    for i in CI:
        g[cls[i]].append((pt[i], ct[i]))
    return sum(len(v) - max_bijection(v) for v in g.values())


# C14: crib word segmentations (EAST|NORTH|EAST, EAST|NORTHEAST, EASTNORTHEAST x BERLIN|CLOCK, BERLINCLOCK)
SEGS = [(a, b) for a in ((4, 5, 4), (4, 9), (13,)) for b in ((6, 5), (11,))]


def word_classes(seg, mode):
    cls, slot = {}, 0
    for start, lens in ((21, seg[0]), (63, seg[1])):
        p = start
        for L in lens:
            for j in range(L):
                cls[p + j] = {"slot": slot, "jstart": j, "jend": L - 1 - j}[mode]
            p += L
            slot += 1
    return cls


def c14(pt, ct, mode):
    return min(dstar_classes(pt, ct, word_classes(s, mode)) for s in SEGS)


# J05: standard English Braille, dots 1-6 as bits 0-5
BRAILLE = dict(a='1', b='12', c='14', d='145', e='15', f='124', g='1245', h='125', i='24', j='245',
               k='13', l='123', m='134', n='1345', o='135', p='1234', q='12345', r='1235', s='234', t='2345',
               u='136', v='1236', w='2456', x='1346', y='13456', z='1356')
BITS = {ch.upper(): sum(1 << (int(d) - 1) for d in s) for ch, s in BRAILLE.items()}
LETTERS = set(BITS.values())
PERMS = list(itertools.permutations(range(6)))
PMAP = [[sum(((x >> j) & 1) << perm[j] for j in range(6)) for x in range(64)] for perm in PERMS]
if np is not None:
    _PMAP_NP = np.array(PMAP, dtype=np.int64)
    _ROW64 = (np.arange(len(PMAP), dtype=np.int64) * 64)[:, None]


def popcount(x):
    return bin(x).count("1")


def letter_preserving():
    """(permutation index, xor key) pairs whose map sends the 26 letter cells onto the 26 letter cells"""
    return [(a, k) for a, pm in enumerate(PMAP) for k in range(64) if {pm[x] ^ k for x in LETTERS} == LETTERS]


def j05a(pbits, cbits, maps=None):
    """one global map C = pi(P) xor k; d* = 24 - the largest number of crib positions it satisfies"""
    if maps is not None:
        return len(pbits) - max(sum(PMAP[a][p] ^ k == c for p, c in zip(pbits, cbits)) for a, k in maps)
    if np is not None:
        keys = _PMAP_NP[:, pbits] ^ np.asarray(cbits)
        cnt = np.bincount((keys + _ROW64).ravel(), minlength=len(PMAP) * 64).reshape(len(PMAP), 64)
        return len(pbits) - int(cnt.max())
    best = 0
    for pm in PMAP:
        cnt = [0] * 64
        for p, c in zip(pbits, cbits):
            cnt[pm[p] ^ c] += 1
        best = max(best, max(cnt))
    return len(pbits) - best


J05B_PARTS = {
    "dot count": popcount,
    "dot count or complement": None,
    "decade (dots 3,6)": lambda x: x & 0b100100,
    "upper 4 dots": lambda x: x & 0b011011,
    "left column": lambda x: x & 0b000111,
    "right column": lambda x: x & 0b111000,
    "top row": lambda x: x & 0b001001,
    "middle row": lambda x: x & 0b010010,
    "bottom row": lambda x: x & 0b100100,
}


def j05b(pbits, cbits, name):
    if name == "dot count or complement":
        return sum(popcount(c) not in (popcount(p), 6 - popcount(p)) for p, c in zip(pbits, cbits))
    f = J05B_PARTS[name]
    return sum(f(p) != f(c) for p, c in zip(pbits, cbits))


# J12: one table per carved row (K4 positions 0-3, 4-34, 35-65, 66-96 are carved rows 24-27)
def carved_row(i):
    return 24 if i < 4 else 25 + (i - 4) // 31


ROWS = {i: carved_row(i) for i in range(97)}


# S3-19: key restart at the chart #3 fold columns (K4 position i sits at sheet index 337 + i of a 31-wide grid)
def fold_positions(cols):
    return sorted(i for i in range(97) if (337 + i) % 31 + 1 in cols)


FOLDS = {"all six folds": [0] + fold_positions((6, 25)), "column 6 only": [0] + fold_positions((6,)),
         "column 25 only": [0] + fold_positions((25,))}
CONV = [(an, A, d) for an, A in (("AZ", AZ), ("KA", KA)) for d in ("Vig", "Beau", "VBeau")]


def phase(i, starts):
    return i - max(s for s in starts if s <= i)


def shift_key(A, d, c, p):
    c, p = A.index(c), A.index(p)
    return (c - p) % 26 if d == "Vig" else (c + p) % 26 if d == "Beau" else (p - c) % 26


def shift_enc(A, d, p, k):
    p = A.index(p)
    return A[(p + k) % 26] if d == "Vig" else A[(k - p) % 26] if d == "Beau" else A[(p - k) % 26]


def s319(pt, ct, starts):
    best = None
    for _, A, d in CONV:
        g = defaultdict(list)
        for i in CI:
            g[phase(i, starts)].append(shift_key(A, d, ct[i], pt[i]))
        v = sum(len(x) - Counter(x).most_common(1)[0][1] for x in g.values())
        best = v if best is None else min(best, v)
    return best


def all_dstar(pt, ct, cbits=None, maps_identity=None):
    """d* of every sub-family; pt, ct: dict crib position -> letter"""
    pb = [BITS[pt[i]] for i in CI]
    cb = cbits if cbits is not None else [BITS[ct[i]] for i in CI]
    r = {"C14a word alphabet": c14(pt, ct, "slot"),
         "C14b restart j from start": c14(pt, ct, "jstart"),
         "C14c restart j from end": c14(pt, ct, "jend"),
         "J05a dot perm x XOR (global)": j05a(pb, cb),
         "J05a' letter-preserving (identity only)": j05a(pb, cb, maps_identity or letter_preserving())}
    for name in J05B_PARTS:
        r["J05b " + name] = j05b(pb, cb, name)
    r["J12 L1 carved row"] = dstar_classes(pt, ct, ROWS)
    for fn, st in FOLDS.items():
        r["S3-19 shift table, " + fn + " [K1-K3 variant]"] = s319(pt, ct, st)
        r["S3-19r any row, " + fn] = dstar_classes(pt, ct, {i: phase(i, st) for i in CI})
    return r


def crib_dicts(ctext):
    return {i: CRIB[i] for i in CI}, {i: ctext[i] for i in CI}


# plants for the d* code: random settings of each sub-family, two crib letters altered before enciphering
def _altered(rng):
    pt = {i: CRIB[i] for i in CI}
    for i in rng.sample(CI, 2):
        pt[i] = rng.choice([x for x in AZ if x != pt[i]])
    return pt


def _table_per_class(rng, pt, cls):
    tabs = {}
    out = {}
    for i in CI:
        if cls[i] not in tabs:
            s = list(AZ)
            rng.shuffle(s)
            tabs[cls[i]] = dict(zip(AZ, s))
        out[i] = tabs[cls[i]][pt[i]]
    return out


def plant_dstar(rng, fam, maps_identity):
    pt = _altered(rng)
    crib = {i: CRIB[i] for i in CI}
    pb = [BITS[crib[i]] for i in CI]
    if fam.startswith("C14"):
        mode = {"C14a": "slot", "C14b": "jstart", "C14c": "jend"}[fam[:4]]
        ct = _table_per_class(rng, pt, word_classes(rng.choice(SEGS), mode))
        return c14(crib, ct, mode)
    if fam.startswith("J05a'"):
        return j05a(pb, [BITS[pt[i]] for i in CI], maps_identity)
    if fam.startswith("J05a"):
        pm, k = rng.choice(PMAP), rng.randrange(64)
        return j05a(pb, [pm[BITS[pt[i]]] ^ k for i in CI])
    if fam.startswith("J05b"):
        name = fam[5:]
        cls = (lambda x: min(popcount(x), 6 - popcount(x))) if name == "dot count or complement" else J05B_PARTS[name]
        groups = defaultdict(list)
        for x in sorted(LETTERS):
            groups[cls(x)].append(x)
        return j05b(pb, [rng.choice(groups[cls(BITS[pt[i]])]) for i in CI], name)
    if fam.startswith("J12"):
        return dstar_classes(crib, _table_per_class(rng, pt, ROWS), ROWS)
    if fam.startswith("S3-19r"):
        st = FOLDS[fam.split(", ")[1]]
        cls = {i: phase(i, st) for i in CI}
        return dstar_classes(crib, _table_per_class(rng, pt, cls), cls)
    if fam.startswith("S3-19"):
        st = FOLDS[fam.split(", ")[1].split(" [")[0]]
        _, A, d = rng.choice(CONV)
        ks = {}
        ct = {}
        for i in CI:
            ph = phase(i, st)
            if ph not in ks:
                ks[ph] = rng.randrange(26)
            ct[i] = shift_enc(A, d, pt[i], ks[ph])
        return s319(crib, ct, st)
    raise ValueError(fam)
