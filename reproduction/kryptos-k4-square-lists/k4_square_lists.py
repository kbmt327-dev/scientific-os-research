"""Doppelkasten applied twice with boxes from a fixed list, on K4 without its Ws (EP-0193 T1, EP-0200; numpy).

K4 without its five Ws is 92 letters over the 25-letter alphabet A-Z minus W; the cribs sit at reduced positions
20-32 (EASTNORTHEAST) and 59-69 (BERLINCLOCK).  A box is square(word): the word's letters (W dropped), then the rest
of the 25 letters in order (the convention of the W-squares Note, EP-0110).

Doppelkasten (EP-0116 / EP-0193 conventions).  Left box Q1 holds the first letter a at (r1, c1), right box Q2 the
second letter b at (r2, c2).  Rows differ: C1 = Q2[r1, c2], C2 = Q1[r2, c1].  Same row r (the cross rule, the
invertible one): C1 = Q2[r, c2 + s], C2 = Q1[r, c1 + s] with s = +1 (cross+) or -1 (cross-).  Two passes: the
second pass uses the same boxes or the boxes swapped.  A letter left without a partner by a pairing passes
through unchanged.

Pairings: adjacent pairs from reduced position 0 (adj0), from 1 (adj1), restarting at each W segment (adjseg),
and seriated pairs (i, i + d) in blocks of 2d, d = 2..46 (48 in all, EP-0116).  EP-0200 adds a different pairing
per pass: two different adjacent pairings, or one pass shifted once (EP-0169: pairs keep one parity before
position b and the other parity from b on; b = 1..91, phase 0/1).
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A25 = AZ.replace("W", "")
WPOS = [i for i, ch in enumerate(K4) if ch == "W"]
KEEP = [i for i in range(97) if K4[i] != "W"]
RED = "".join(K4[i] for i in KEEP)
CR = {KEEP.index(i): ch for i, ch in CRIB.items()}
CPOS = sorted(CR)
CIDX = {p: t for t, p in enumerate(CPOS)}
CVAL = np.array([A25.index(CR[i]) for i in CPOS], dtype=np.intp)
N92 = 92

# the 40 hint keywords of the W-squares Note (EP-0110), as published in that package
KEYWORDS = """KRYPTOS PALIMPSEST ABSCISSA BERLIN CLOCK BERLINCLOCK WORLDCLOCK WELTZEITUHR ALEXANDERPLATZ
EASTNORTHEAST NORTHEAST LAYERTWO EGYPT CARTER HOWARDCARTER TUTANKHAMUN SANBORN SCHEIDT LANGLEY IQLUSION
UNDERGRUUND DESPARATLY SHADOWFORCES LUCIDMEMORY VIRTUALLYINVISIBLE TISYOURPOSITION DIGETALINTERPRETATIU
MESSAGE DELIVERINGAMESSAGE BERLINWALL NOVEMBER NINETEENEIGHTYNINE ANTIPODES LODESTONE COMPASS SHADOW LIGHT
ILLUSION NUANCE PYRAMID""".split()
KRYPTOS_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


def places():
    return json.loads((HERE / "data" / "worldclock-places.json").read_text(encoding="utf-8"))["letters"]


def square(word=""):
    seen = []
    for ch in word.upper() + A25:
        if ch in A25 and ch not in seen:
            seen.append(ch)
    return "".join(seen)


def squares185():
    """EP-0193's boxes: plain A-Z, the K1/K2 keywords, the 40 hint keywords and the 146 World Clock places"""
    out = []
    for w in ["", "KRYPTOS", "PALIMPSEST", "ABSCISSA"] + KEYWORDS + places():
        s = square(w)
        if s not in out:
            out.append(s)
    return out


# ------------------------------------------------------------------ pairings
def seg_starts():
    out, st = [], 0
    for i in range(98):
        if i == 97 or K4[i] == "W":
            if i > st:
                out.append(KEEP.index(st))
            st = i + 1
    return out


def adjacent(mode, n=N92):
    if mode in (0, 1):
        return [(i, i + 1) for i in range(mode, n - 1, 2)]
    b = seg_starts() + [n]
    return [(i, i + 1) for s, e in zip(b[:-1], b[1:]) for i in range(s, e - 1, 2)]


def seriated(d, n=N92):
    out = []
    for b0 in range(0, n, 2 * d):
        r = min(2 * d, n - b0)
        h = d if r == 2 * d else r // 2
        out += [(b0 + c, b0 + h + c) for c in range(h)]
    return out


PAIRINGS = {"adj0": adjacent(0), "adj1": adjacent(1), "adjseg": adjacent("seg")}
PAIRINGS.update({"ser%d" % d: seriated(d) for d in range(2, 47)})
ADJ = ["adj0", "adj1", "adjseg"]


def shift_pairs(b, phi0, n=N92):
    before = [(i, i + 1) for i in range(phi0, n - 1, 2) if i + 1 < b]
    after = [(i, i + 1) for i in range(1 - phi0, n - 1, 2) if i >= b]
    return before + after


def partner(pairs):
    p = -np.ones(N92, dtype=np.intp)
    for i, j in pairs:
        p[i], p[j] = j, i
    return p


def combos():
    """EP-0200's 1,146 (label, pass-1 pairs, pass-2 pairs, (shifted pass, lone letters) or None, part)"""
    out = []
    for a in ADJ:
        for b in ADJ:
            if a != b:
                out.append(("%s|%s" % (a, b), PAIRINGS[a], PAIRINGS[b], None, 1))
    for b0 in range(1, N92):
        for phi in (0, 1):
            sp = shift_pairs(b0, phi)
            paired = {x for pr in sp for x in pr}
            lone = [x for x in range(N92) if x not in paired]
            for other in ADJ:
                out.append(("shift(%d,%d)|%s" % (b0, phi, other), sp, PAIRINGS[other], (1, lone), 1))
                out.append(("%s|shift(%d,%d)" % (other, b0, phi), PAIRINGS[other], sp, (2, lone), 1))
    for pm in PAIRINGS:
        out.append(("same %s" % pm, PAIRINGS[pm], PAIRINGS[pm], None, 2))
    return out


def program(p1, p2, lone):
    """rows (u, v, crib index of u, crib index of v) for the pass-1 pairs (or single letters) that reach the crib,
    the pass-2 partners, and the crib indices that are not judged because they depend on a letter left alone by
    a shift (EP-0200's conservative rule)"""
    pa, pb = partner(p1), partner(p2)
    rows, seen = [], set()
    for i in CPOS:
        j = pa[i]
        if j < 0:
            rows.append((i, -1, CIDX[i], -1))
        else:
            u, v = min(i, j), max(i, j)
            if (u, v) not in seen:
                seen.add((u, v))
                rows.append((u, v, CIDX.get(u, -1), CIDX.get(v, -1)))
    excl = np.zeros(24, dtype=bool)
    if lone:
        ps, ls = lone
        for x in ls:
            if ps == 1 and x in CIDX:
                excl[CIDX[x]] = True
            if ps == 2:
                for y in (x, pa[x]):
                    if y >= 0 and y in CIDX:
                        excl[CIDX[y]] = True
    return rows, pb, excl


# ------------------------------------------------------------------ Doppelkasten
def encrypt_pair(q1, q2, s, a, b):
    r1, c1 = divmod(q1.index(a), 5)
    r2, c2 = divmod(q2.index(b), 5)
    if r1 != r2:
        return q2[r1 * 5 + c2], q1[r2 * 5 + c1]
    return q2[r1 * 5 + (c2 + s) % 5], q1[r1 * 5 + (c1 + s) % 5]


def encrypt(P, p1, p2, qa, qb, s, sw):
    x = list(P)
    for pairs, (q1, q2) in ((p1, (qa, qb)), (p2, (qb, qa) if sw else (qa, qb))):
        for i, j in pairs:
            x[i], x[j] = encrypt_pair(q1, q2, s, x[i], x[j])
    return "".join(x)


class Boxes:
    """every ordered box pair (a, b) of a list at once.  T[s][c1 * 25 + c2, a * S + b] = 25 * p1 + p2, the pair that
    one Doppelkasten step with left box a, right box b and same-row shift s turns into (c1, c2)"""

    def __init__(self, sq):
        S = self.S = len(sq)
        self.S2 = S * S
        Q = np.array([[A25.index(c) for c in s] for s in sq], dtype=np.int32)       # cell -> letter
        QI = np.argsort(Q, axis=1).astype(np.int32)                                 # letter -> cell
        Qf, QIf = Q.ravel(), QI.ravel()
        a = np.repeat(np.arange(S, dtype=np.int32), S) * 25                          # row offsets of box a
        b = np.tile(np.arange(S, dtype=np.int32), S) * 25
        self.swap = (b // 25) * S + a // 25                                          # column of (b, a)
        r1, x1 = np.divmod(QIf.take(a[None, :] + np.arange(25, dtype=np.int32)[:, None]), 5)   # c2 in the left box
        self.T = {}
        for s in (1, -1):
            T = np.empty((625, self.S2), dtype=np.int16)
            for c1 in range(25):
                r2, x2 = np.divmod(QIf.take(b + c1), 5)                             # c1 in the right box
                d = r2 != r1
                p1 = Qf.take(a + r2 * 5 + np.where(d, x1, (x1 - s) % 5))
                p2 = Qf.take(b + np.where(d, r1, r2) * 5 + np.where(d, x2, (x2 - s) % 5))
                T[c1 * 25:(c1 + 1) * 25] = p1 * 25 + p2
            self.T[s] = T


DIV = (np.arange(625) // 25).astype(np.int16)
MOD = (np.arange(625) % 25).astype(np.int16)


def program_key(rows, pb, excl):
    """two programs with the same key give the same h for every setting"""
    key = [(u, v, tu, tv, int(pb[u]), int(pb[v]) if v >= 0 else -9) for u, v, tu, tv in rows]
    return tuple(key) + (tuple(np.nonzero(excl)[0].tolist()),)


def scan(bx, text, rows, pb, excl, passes=2, lone="pass"):
    """histogram (25 bins) of the crib mismatch h over every (a, b, s, swap) of one pairing program.
    lone: how a crib letter without a pass-1 partner is judged -- 'pass' (it passes through and is compared,
    EP-0200), 'skip' (not judged, EP-0225's repair) or 'miss' (always counted as a mismatch, EP-0193's kernel)."""
    ct = [A25.index(c) for c in text]
    hist = np.zeros(25, dtype=np.int64)
    idx = np.arange(bx.S2, dtype=np.int32)
    for s in (1, -1):
        T = bx.T[s]
        Tf = T.ravel()
        for sw in ((0, 1) if passes == 2 else (0,)):
            cache = {}

            def xval(k):
                if passes == 1 or pb[k] < 0:
                    return ct[k]
                u, v = min(k, pb[k]), max(k, pb[k])
                if (u, v) not in cache:
                    row = T[ct[u] * 25 + ct[v]]
                    if sw:
                        row = row.take(bx.swap)
                    cache[(u, v)] = row
                row = cache[(u, v)]
                return DIV.take(row) if k == u else MOD.take(row)
            h = np.zeros(bx.S2, dtype=np.int8)
            for u, v, tu, tv in rows:
                xu = xval(u)
                if v < 0:
                    if lone == "miss":
                        h += 1
                    elif lone == "pass" and not excl[tu]:
                        h += xu != CVAL[tu]
                    continue
                code = xu * 25 + xval(v)
                out = T[code] if np.isscalar(code) else Tf.take(code.astype(np.int32) * bx.S2 + idx)
                if tu >= 0 and not excl[tu]:
                    h += DIV.take(out) != CVAL[tu]
                if tv >= 0 and not excl[tv]:
                    h += MOD.take(out) != CVAL[tv]
            hist += np.bincount(h, minlength=25)[:25]
    return hist


# ------------------------------------------------------------------ Bifid block settings (EP-0169)
def bf_blocks(p, a0, b, n=N92):
    bd = {0, n}
    if p == 0:
        bd.add(b)
    else:
        bd |= set(range(a0, b, p)) | set(range(b, n, p))
    bd = sorted(x for x in bd if 0 <= x <= n)
    return [(s, e) for s, e in zip(bd[:-1], bd[1:]) if e > s]


def bf_settings(n=N92):
    """{crib-touching blocks: [(p, a0, b), ...]} -- EP-0169's 2,765 CM-Bifid block settings"""
    out = {}
    for p in [0] + list(range(2, 13)):
        for a0 in (range(p) if p else [0]):
            for b in range(1, n + 1):
                key = tuple(x for x in bf_blocks(p, a0, b, n) if any(i in CR for i in range(*x)))
                out.setdefault(key, []).append((p, a0, b))
    return out
