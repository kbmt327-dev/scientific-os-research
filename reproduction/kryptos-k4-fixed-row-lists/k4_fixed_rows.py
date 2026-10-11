"""Charts whose row at each position is a keyed alphabet taken from a fixed word list (EP-0196, EP-0197, EP-0208).

Row r of a list W is keyed(W[r]) (the word, then the rest of A-Z).  The row used at K4 position i is
    (c + dir * f(i)) mod |W|,     c = 0..|W|-1, dir = +-1,
with f(i) = the position inside the word (EP-0196, from the word start or from the word end), the distance from the
last fold-line restart (EP-0197), or i mod p (EP-0208).  29 readings (EP-0098):
    m1 C = R[AZ(P)]   m2 C = AZ[R^-1(P)]   m3 C = KA[R^-1(P)]   m4 C = R[KA(P)]   m5 C = R[(R^-1(P) + g) mod 26], g = 1..25
Statistic: h = crib positions (24) where the predicted letter differs from K4.  Only counts are computed here.
"""
import numpy as np

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = np.array(sorted(CRIB))
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
PV = np.array([AZ.index(CRIB[i]) for i in POS])
KAV = np.array([AZ.index(ch) for ch in KA])
KAI = np.array([KA.index(ch) for ch in AZ])
READS = ["m1", "m2", "m3", "m4"] + ["m5g%d" % g for g in range(1, 26)]


def keyed(word):
    seen = []
    for ch in word + AZ:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


def tables(words):
    """T[m, r, x] = AZ index of the ciphertext letter for plaintext AZ index x in row r under reading m"""
    A = np.array([[AZ.index(ch) for ch in keyed(w)] for w in words])
    Ainv = np.argsort(A, axis=1)
    T = np.empty((29, len(words), 26), dtype=np.int8)
    T[0], T[1], T[2], T[3] = A, Ainv, KAV[Ainv], A[:, KAI]
    for g in range(1, 26):
        T[3 + g] = np.take_along_axis(A, (Ainv + g) % 26, axis=1)
    return T


def naive_letter(word, p, m):
    """Reference implementation on strings (no tables)."""
    row = keyed(word)
    if m == 0:
        return row[AZ.index(p)]
    ip = row.index(p)
    if m == 1:
        return AZ[ip]
    if m == 2:
        return KA[ip]
    if m == 3:
        return row[KA.index(p)]
    return row[(ip + m - 3) % 26]


def naive_encrypt(P, words, f, c, sgn, m):
    """encrypt a 97-letter text with row (c + sgn*f[i]) mod |W| at position i"""
    n = len(words)
    return "".join(naive_letter(words[(c + sgn * int(f[i])) % n], ch, m) for i, ch in enumerate(P))


def crib_vec(text):
    return np.array([AZ.index(text[p]) for p in POS], dtype=np.int8)


def min_h(T, fvecs, C):
    """min over readings, offsets c, dir and the given f-vectors (each a length-24 array at the crib positions).
    C: (M, 24) ciphertext letters at the crib.  Returns (M,) minima."""
    n = T.shape[1]
    TP = T[:, :, PV]                                   # (29, n, 24)
    c = np.arange(n)[:, None]
    kk = np.arange(24)[None, :]
    best = np.full(C.shape[0], 99)
    for f in fvecs:
        for sgn in (1, -1):
            pred = TP[:, (c + sgn * f[None, :]) % n, kk]                      # (29, n, 24)
            h = 24 - (pred[None] == C[:, None, None, :]).sum(3)                # (M, 29, n)
            best = np.minimum(best, h.reshape(C.shape[0], -1).min(1))
    return best


def cover_bound(T, C, excluded=()):
    """selection-free bound: min over readings of the crib positions that no row of the list can produce"""
    TP = T[:, :, PV]
    cov = (TP == C[None, None, :]).any(1)              # (29, 24)
    keep = np.array([p not in excluded for p in POS])
    return int(((~cov) & keep[None, :]).sum(1).min())


# ---------------------------------------------------------------- EP-0196: position inside the word
BREAKS1 = {"EAST|NORTHEAST": [(21, 24), (25, 33)], "EASTNORTHEAST": [(21, 33)],
           "EAST|NORTH|EAST": [(21, 24), (25, 29), (30, 33)]}
BREAKS2 = {"BERLIN|CLOCK": [(63, 68), (69, 73)], "BERLINCLOCK": [(63, 73)]}


def wordpos_vectors(mode):
    """the j-vectors at the crib for 6 crib-word breaks x outer offsets o1, o2 in 0..3 (o = (0,0) first);
    head: the first word of each crib starts o letters earlier; end: the last word ends o letters later"""
    out = []
    for o1 in range(4):
        for o2 in range(4):
            for b1, w1 in BREAKS1.items():
                for b2, w2 in BREAKS2.items():
                    words = [list(x) for x in w1] + [list(x) for x in w2]
                    k1, k2 = (0, len(w1)) if mode == "head" else (len(w1) - 1, len(words) - 1)
                    if mode == "head":
                        words[k1][0] -= o1
                        words[k2][0] -= o2
                    else:
                        words[k1][1] += o1
                        words[k2][1] += o2
                    J = []
                    for p in POS:
                        s, e = next((s, e) for s, e in words if s <= p <= e)
                        J.append(p - s if mode == "head" else e - p)
                    out.append(((o1, o2), np.array(J)))
    return out


# ---------------------------------------------------------------- EP-0197: distance from the last fold restart
LINES = {"col6": [9, 40, 71], "col25": [28, 59, 90], "both": [9, 28, 40, 59, 71, 90]}
RESTARTS = {"%s/%s" % (ln, cell): sorted({0} | {p + (cell == "next") for p in v})
            for ln, v in LINES.items() for cell in ("crossed", "next")}


def fold_phase(starts):
    return np.array([i - max(s for s in starts if s <= i) for i in range(97)])


# ---------------------------------------------------------------- EP-0208: period band
BAND = [26, 27, 28, 29] + list(range(53, 74))
LAYER1 = [28, 26]
