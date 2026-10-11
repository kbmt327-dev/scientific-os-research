"""Free Four-square behind a mask fixed by outside facts (EP-0195), on the public K4 ciphertext and cribs.

Families (the author's conventions, rewritten here):
  alpha-1  C_i = M_i(FS(P)_i), all 97 letters; the squares drop J (J -> I); M is the keyed Vigenere of K1/K2
           (KRYPTOS alphabet of 26 letters, keys PALIMPSEST and ABSCISSA, every phase)
  beta-1   W as separator (92 letters, A-Z minus W): C = M(FS(P)), M on the KRYPTOS alphabet without W (25)
  beta-2   the same with the order swapped: C = FS(M(P))
The plain squares are standard; the two cipher squares are free.  A crib pair (both letters in the crib) puts one
letter into one cell of each cipher square; two pairs conflict when they put different letters into one cell or one
letter into two cells of the same square.  d* = the minimum vertex cover of this conflict graph (dropping one crib
position removes its pair).  alpha: a J anywhere in y = M^-1(C) at a paired position kills the setting, because the
squares have no J (d* = 9 here, 'dead').
The fourth family of the Note (letters behind K4 when the panels are folded at a seam) needs the carved text
around K4, which this site does not publish; it is recorded, not rerun.
Standard library only, except null_dstar(), which uses numpy for the 20,000 shuffles.
"""
import random
from itertools import combinations

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA26 = "KRYPTOSABCDEFGHIJLMNQUVWXZ"            # the keyed alphabet of K1/K2
KA25 = KA26.replace("W", "")
STDJ = AZ.replace("J", "")                     # alpha squares: 25 letters without J
STDW = AZ.replace("W", "")                     # beta squares: 25 letters without W
KEYS = {"PALIMPSEST": 10, "ABSCISSA": 8}
J = "J"

WPOS = [i for i, ch in enumerate(K4) if ch == "W"]
KEEP = [i for i in range(97) if K4[i] != "W"]
RED = "".join(K4[i] for i in KEEP)
RIDX = {i: n for n, i in enumerate(KEEP)}
CR = {RIDX[i]: ch for i, ch in CRIB.items()}  # the crib in reduced positions
SEG_STARTS = [0] + [RIDX[i + 1] for i in range(96) if K4[i] == "W" and i + 1 in RIDX and RIDX[i + 1] > 0]


def coords(sq):
    return {ch: divmod(k, 5) for k, ch in enumerate(sq)}


CJ, CW = coords(STDJ), coords(STDW)


def beta_pairs(mode, n=92):
    if mode in (0, 1):
        return [(i, i + 1) for i in range(mode, n - 1, 2)]
    out, b = [], SEG_STARTS + [n]
    for s, e in zip(b[:-1], b[1:]):
        out += [(i, i + 1) for i in range(s, e - 1, 2)]
    return out


def alpha_pairs(mode):
    return [(i, i + 1) for i in range(mode, 96, 2)]


PAIR_MODES = {0: beta_pairs(0), 1: beta_pairs(1), "seg": beta_pairs("seg")}


def settings():
    """The 288 settings of alpha-1 (36), beta-1 (108) and beta-2 (108), in the author's order."""
    S = []
    for key, p in KEYS.items():
        for ph in range(p):
            k = [KA26.index(key[(i + ph) % p]) for i in range(97)]
            for mode in (0, 1):
                S.append(dict(fam="R31a", grp="R31a/%d" % mode, label="%s ph%d pair%d" % (key, ph, mode),
                              alpha=True, order1=True, k=k, pairs=alpha_pairs(mode)))
            for kidx in ("red", "orig"):
                kk = [KA25.index(key[((n if kidx == "red" else KEEP[n]) + ph) % p]) for n in range(92)]
                for mode in PAIR_MODES:
                    for fam, o1 in (("R31b1", True), ("R31b2", False)):
                        S.append(dict(fam=fam, grp="%s/%s" % (fam, mode),
                                      label="%s ph%d %s pair%s" % (key, ph, kidx, mode),
                                      alpha=False, order1=o1, k=kk, pairs=PAIR_MODES[mode]))
    return S


def instance(s, ct=K4):
    """(dead, vertices) for one ciphertext: vertices are crib pairs (cell2, letter2, cell3, letter3)."""
    if s["alpha"]:
        text, cr, cc, order = ct, CRIB, CJ, KA26
    else:
        text, cr, cc, order = "".join(ct[i] for i in KEEP), CR, CW, KA25
    m, k = len(order), s["k"]
    cp = [(i, j) for i, j in s["pairs"] if i in cr and j in cr]
    if s["order1"]:
        y = [order[(order.index(c) - k[i]) % m] for i, c in enumerate(text)]
        dead = s["alpha"] and any(y[x] == J for pr in s["pairs"] for x in pr)
        pl = [(cr[i], cr[j], y[i], y[j]) for i, j in cp]
    else:
        dead = False
        x = {i: order[(order.index(ch) + k[i]) % m] for i, ch in cr.items()}
        pl = [(x[i], x[j], text[i], text[j]) for i, j in cp]
    verts = [((cc[a][0], cc[b][1]), l2, (cc[b][0], cc[a][1]), l3) for a, b, l2, l3 in pl]
    return dead, verts


def conflict_edges(verts):
    E = []
    for u, v in combinations(range(len(verts)), 2):
        a, b = verts[u], verts[v]
        if (a[0] == b[0]) != (a[1] == b[1]) or (a[2] == b[2]) != (a[3] == b[3]):
            E.append((u, v))
    return E


def min_vertex_cover(n, E):
    """Exact minimum vertex cover by increasing size (n <= 12 here, so at most 4,096 subsets)."""
    for size in range(n + 1):
        for cover in combinations(range(n), size):
            c = set(cover)
            if all(u in c or v in c for u, v in E):
                return size, cover
    return n, tuple(range(n))


def dstar_exact(s, ct=K4):
    """Exact d* (no cap), or 9 if the setting is dead by J; also one minimum cover as crib positions."""
    dead, verts = instance(s, ct)
    if dead:
        return 9, ()
    E = conflict_edges(verts)
    d, cover = min_vertex_cover(len(verts), E)
    return d, cover


def shuffles(n, seed=195):
    """The author's null: K4's non-W letters shuffled, the five Ws kept in place (seed 195)."""
    rng = random.Random(seed)
    nonw = [ch for ch in K4 if ch != "W"]
    out = []
    for _ in range(n):
        p = nonw[:]
        rng.shuffle(p)
        it = iter(p)
        out.append("".join("W" if ch == "W" else next(it) for ch in K4))
    return out


def null_dstar(s, CT):
    """d* capped at 3 (0, 1, 2, 3 = '3 or more', 9 = dead by J) for every row of CT (numpy int array, S x 97),
    vectorised like the author's checker."""
    import numpy as np
    order = KA26 if s["alpha"] else KA25
    m = len(order)
    to_ord = np.full(26, -1, dtype=np.int16)
    for i, ch in enumerate(order):
        to_ord[AZ.index(ch)] = i
    from_ord = np.array([AZ.index(ch) for ch in order], dtype=np.int16)
    if s["alpha"]:
        W, cr, cc = CT, CRIB, CJ
    else:
        W, cr, cc = CT[:, KEEP], CR, CW
    k = np.array(s["k"], dtype=np.int16)
    cp = [(i, j) for i, j in s["pairs"] if i in cr and j in cr]
    dead = np.zeros(len(CT), dtype=bool)
    if s["order1"]:
        y = from_ord[(to_ord[W] - k) % m]
        if s["alpha"]:
            idx = sorted({x for pr in s["pairs"] for x in pr})
            dead = (y[:, idx] == AZ.index(J)).any(axis=1)
        L2, L3 = y[:, [i for i, _ in cp]], y[:, [j for _, j in cp]]
        pl = [(cr[i], cr[j]) for i, j in cp]
    else:
        L2, L3 = W[:, [i for i, _ in cp]], W[:, [j for _, j in cp]]
        x = {i: order[(order.index(ch) + s["k"][i]) % m] for i, ch in cr.items()}
        pl = [(x[i], x[j]) for i, j in cp]
    cell2 = [(cc[a][0], cc[b][1]) for a, b in pl]
    cell3 = [(cc[b][0], cc[a][1]) for a, b in pl]
    V = len(cp)
    E = list(combinations(range(V), 2))
    U, Vv = [u for u, _ in E], [v for _, v in E]
    same2 = np.array([cell2[u] == cell2[v] for u, v in E])
    same3 = np.array([cell3[u] == cell3[v] for u, v in E])
    eq2, eq3 = L2[:, U] == L2[:, Vv], L3[:, U] == L3[:, Vv]
    edges = np.where(same2, ~eq2, eq2) | np.where(same3, ~eq3, eq3)
    inc = np.zeros((len(E), V), dtype=np.int16)
    for e, (u, v) in enumerate(E):
        inc[e, u] = inc[e, v] = 1
    etot = edges.sum(axis=1)
    deg = edges.astype(np.int16) @ inc
    d = np.full(len(CT), 3, dtype=np.int16)
    two = np.zeros(len(CT), dtype=bool)
    for e, (u, v) in enumerate(E):
        two |= (deg[:, u] + deg[:, v] - edges[:, e]) == etot
    d[two] = 2
    d[(deg == etot[:, None]).any(axis=1)] = 1
    d[etot == 0] = 0
    d[dead] = 9
    return d
