"""Procedures printed in Delastelle (1902) and Gaines (1939), as used in EP-0231..EP-0234 and EP-0237.

Everything here is standard library only.  The printed rules and examples were transcribed from public-domain
copies (Delastelle 1902: archive.org item 8VSUP3207b; Gaines 1939: Project Gutenberg #75074) and are kept here
only as test vectors.  Nothing in this module prints or returns a decryption of K4; the functions that touch K4
return counts, mismatch numbers h, or True / False.
"""
import random

# ------------------------------------------------------------------ K4, its cribs, the W-free text beta
K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A25 = AZ.replace("W", "")                                   # Delastelle's bifid alphabet has no W (p.86)
WPOS = [i for i, ch in enumerate(K4) if ch == "W"]
KEEP = [i for i in range(97) if K4[i] != "W"]
RED = "".join(K4[i] for i in KEEP)                          # beta: the 92 letters without W
CR = {KEEP.index(i): ch for i, ch in CRIB.items()}          # the crib in beta positions (20-32, 59-69)
KA26 = "KRYPTOSABCDEFGHIJLMNQUVWXZ"                         # the KRYPTOS keyed alphabet
KA25 = KA26.replace("W", "")
MASK_KEYS = (("PALIMPSEST", 10), ("ABSCISSA", 8))           # the K1 / K2 keywords: 18 phases


def w_shuffle(rng):
    """K4 with the five W kept in place and the other 92 letters shuffled (one draw from rng)"""
    p = [ch for ch in K4 if ch != "W"]
    rng.shuffle(p)
    it = iter(p)
    return "".join("W" if ch == "W" else next(it) for ch in K4)


def beta_shuffle(seed):
    """the 92 beta letters shuffled with random.Random(seed) (EP-0232 / EP-0233 null texts)"""
    x = list(RED)
    random.Random(seed).shuffle(x)
    return "".join(x)


# ------------------------------------------------------------------ EP-0231: Ohaver's Morse "mutilation" (Gaines Fig.173)
# Gaines 1939, ch. XXII, Fig. 173, "The Alphabet, Arranged by Group-Lengths" (30 entries).  The four non-letter symbols
# are written here as u, a, o (umlauts) and ch: '1' .. '4' below.
GAINES_FIG173 = {
    "E": ".", "T": "-",
    "I": "..", "A": ".-", "N": "-.", "M": "--",
    "S": "...", "U": "..-", "R": ".-.", "W": ".--", "D": "-..", "K": "-.-", "G": "--.", "O": "---",
    "H": "....", "V": "...-", "F": "..-.", "1": "..--", "L": ".-..", "2": ".-.-", "P": ".--.", "J": ".---",
    "B": "-...", "X": "-..-", "C": "-.-.", "Y": "-.--", "Z": "--..", "Q": "--.-", "3": "---.", "4": "----"}
NONLETTER = {"1": "u-umlaut", "2": "a-umlaut", "3": "o-umlaut", "4": "ch"}
ITU_MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
             "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
             "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
             "Y": "-.--", "Z": "--.."}
MORSE_INV = {v: k for k, v in GAINES_FIG173.items()}
GS = list(range(2, 98))                                      # group lengths g = 2..97
TAILS = ("rev", "pass")                                      # incomplete last group: reversed (main) / passed


def ohaver_group(grp):
    """reverse the Morse-length sequence of a group and re-cut the same dot-dash string"""
    dots = "".join(GAINES_FIG173[x] for x in grp)
    out, o = [], 0
    for x in reversed(grp):
        L = len(GAINES_FIG173[x])
        out.append(MORSE_INV[dots[o:o + L]])
        o += L
    return out


def ohaver(syms, g, tail="rev"):
    """groups of g from position 0; tail 'rev' reverses the incomplete last group inside itself, 'pass' copies it"""
    out = []
    for s in range(0, len(syms), g):
        grp = list(syms[s:s + g])
        if len(grp) < g and tail == "pass":
            out += grp
        else:
            out += ohaver_group(grp)
    return out


def ka26_phases():
    """the 18 K1/K2 mask phases (EP-0195): per phase the KA26 index of the key letter at every K4 position"""
    out = []
    for key, p in MASK_KEYS:
        for ph in range(p):
            out.append(("%s ph%d" % (key, ph), [KA26.index(key[(i + ph) % p]) for i in range(97)]))
    return out


PHASES26 = ka26_phases()


def mask26_dec(ct, k):
    return [KA26[(KA26.index(c) - k[i]) % 26] for i, c in enumerate(ct)]


def mask26_enc(y, k):
    return [KA26[(KA26.index(c) + k[i]) % 26] for i, c in enumerate(y)]


CRIB_LIST = sorted(CRIB.items())


def ohaver_scan(ct, letter_only=True, groups_touching_only=False):
    """all 3,456 labels (g, tail, phase) of 'Ohaver after the mask' on a 97-letter text.
    Returns {(g, tail, f): (h, letter_only_flag or None)}.  h counts crib positions whose decrypted symbol differs
    from the crib (a non-letter symbol at a crib position is a mismatch).  No decryption is returned."""
    res = {}
    cpos = set(CRIB)
    for f, (_, k) in enumerate(PHASES26):
        y = mask26_dec(ct, k)
        for g in GS:
            starts = list(range(0, 97, g))
            for ti, tail in enumerate(TAILS):
                h = 0
                lo = True
                for s in starts:
                    e = min(s + g, 97)
                    touches = any(s <= q < e for q in cpos)
                    if groups_touching_only and not touches:
                        continue
                    grp = y[s:e]
                    out = grp if (e - s < g and tail == "pass") else ohaver_group(grp)
                    if touches:
                        for j, sym in enumerate(out):
                            c = CRIB.get(s + j)
                            if c is not None and sym != c:
                                h += 1
                    if letter_only and lo and any(sym in NONLETTER for sym in out):
                        lo = False
                res[(g, ti, f)] = (h, lo if letter_only and not groups_touching_only else None)
    return res


def ohaver_forced(g, tail):
    """crib-only structure: groups that lie inside the crib and whose Ohaver image of the crib letters has a
    non-letter symbol (then no letter-only mask output can give them).  Returns the minimum number of crib letters
    that must change in those groups (0 = nothing forced)."""
    forced = 0
    for s in range(0, 97, g):
        e = min(s + g, 97)
        if not all(q in CRIB for q in range(s, e)):
            continue
        if e - s < g and tail == "pass":
            continue
        grp = [CRIB[q] for q in range(s, e)]
        if not any(x in NONLETTER for x in ohaver_group(grp)):
            continue
        best = None
        for j in range(len(grp)):
            for c in AZ:
                if c == grp[j]:
                    continue
                g2 = grp[:j] + [c] + grp[j + 1:]
                if not any(x in NONLETTER for x in ohaver_group(g2)):
                    best = 1
                    break
            if best:
                break
        forced += best if best else 2
    return forced


# ------------------------------------------------------------------ Delastelle 1902: bifid / trifid / tours / groupements
DELASTELLE = {
    # p.86, alphabet bifide normal: letters in code order, A = 11 ... Z = 55 (no W)
    "p86_normal": "ABCDEFGHIJKLMNOPQRSTUVXYZ",
    "p86_examples": [("CI", "BN"), ("JK", "HU"), ("LY", "OI"), ("BN", "CI"), ("HU", "JK"), ("OI", "LY")],
    # p.87, alphabet bifide interverti (chiffrant)
    "p87_codes": ("A=42 B=22 C=14 D=32 E=34 F=25 G=11 H=53 I=51 J=41 K=15 L=23 M=54 N=12 O=55 P=33 Q=31 R=52 "
                  "S=21 T=35 U=13 V=24 X=44 Y=43 Z=45"),
    # p.92, the p.87 alphabet with groups of five
    "p92_example": ("ATTENDEZDESORDRES", [5, 5, 5, 2], "YPNOAPYDZVFHIRBDJ"),
    # pp.93-94, tours de cle multiples: nine letters, groups of 3 then 9
    "p93_upper": "a1 c1 b2 d1 f1 e2 g1 i1 h2",
    "p93_lower": "b1 a2 c2 e1 d2 f2 h1 g2 i2",
    "p94_final": "a1c1 b2d1 f1e2 g1i1 h2b1 a2c2 e1d2 f2h1 g2i2",
    # p.102, alphabet trifide (chiffrant); the 27th sign is '+'
    "p102_codes": ("+=211 A=321 B=233 C=122 D=223 E=212 F=333 G=123 H=332 I=313 J=213 K=131 L=231 M=311 N=111 "
                   "O=323 P=132 Q=221 R=112 S=322 T=232 U=133 V=113 W=121 X=331 Y=222 Z=312"),
    "p102_example": ("NETATTENDSQUATOISEUL", [5, 5, 5, 5], "CAPZEQBRYPJTOJGHWJHL"),
    "p103_example": ("HDAJ+HBQSL+XDEHJERUQ", [7, 7, 6], "AIDETOILECIELTAIDERA"),
    # p.108, groupements: key CHIEN -> group lengths from the letters' ranks; fixed series 5, 9, 11
    "p108_key": ("CHIEN", [3, 8, 9, 5, 14]),
    "p108_series": [5, 9, 11],
    # p.77 damier (quadrants 1 top-left, 2 top-right, 3 bottom-right, 4 bottom-left) and the p.98 helix example
    "p77": {"Q1": "QHKZEAYTNIPBFLSURCJGXOMDV", "Q2": "FSBPLMVOXDKEHQZCGRUJTIYAN",
            "Q3": "RHEMOKBAVQFIZCYNLXGPDJTSU", "Q4": "GXNPLVAKQBSTDUJMEROHCZFYI"},
    "p98_example": ("ILFAUTAUTANTQUONPEUT" "OBLIGERTOUTLEMONDE", "SUKSDFOVRCMRDVJPDHLF" "DXEHXHFNDGRYHNNPMIS"),
}


def codes_from(spec):
    return {item.split("=")[0]: tuple(int(d) for d in item.split("=")[1]) for item in spec.split()}


def normal_codes():
    return {ch: (k // 5 + 1, k % 5 + 1) for k, ch in enumerate(DELASTELLE["p86_normal"])}


def bifid_groups(pt, codes, lengths):
    """Delastelle's scission: codes written vertically under the letters, groups read horizontally"""
    inv = {v: k for k, v in codes.items()}
    out, s, i = [], 0, 0
    while s < len(pt):
        L = lengths[i % len(lengths)]
        grp = pt[s:s + L]
        seq = [codes[c][0] for c in grp] + [codes[c][1] for c in grp]
        out += [inv[(seq[2 * j], seq[2 * j + 1])] for j in range(len(grp))]
        s += L
        i += 1
    return "".join(out)


def trifid_groups(text, codes, lengths, decrypt=False):
    inv = {v: k for k, v in codes.items()}
    out, s, i = [], 0, 0
    while s < len(text):
        L = lengths[i % len(lengths)]
        grp = text[s:s + L]
        n = len(grp)
        if not decrypt:
            seq = [codes[c][m] for m in range(3) for c in grp]
            out += [inv[tuple(seq[3 * j:3 * j + 3])] for j in range(n)]
        else:
            seq = [d for c in grp for d in codes[c]]
            out += [inv[(seq[j], seq[n + j], seq[2 * n + j])] for j in range(n)]
        s += L
        i += 1
    return "".join(out)


def ranks(word, alpha=AZ):
    return [alpha.index(c) + 1 for c in word]


# Bifid as a programme G on the coordinate string x = [row P0, col P0, row P1, col P1, ...]:  y_j = x[G[j]],
# cipher letter k = square[y_2k][y_2k+1]   (EP-0219 / EP-0232 convention)
def bounds_periodic(p, n):
    return list(range(0, n, p)) + [n]


def bounds_cyclic(lengths, n):
    b, k = [0], 0
    while b[-1] < n:
        b.append(min(n, b[-1] + lengths[k % len(lengths)]))
        k += 1
    return b


def G_of_bounds(b, order="rc"):
    G = []
    for s, e in zip(b[:-1], b[1:]):
        rows = [2 * m for m in range(s, e)]
        cols = [2 * m + 1 for m in range(s, e)]
        G += rows + cols if order == "rc" else cols + rows
    return G


def G_tours(p1, p2, n=92):
    """tours de cle multiples: pass 1 in groups of p1, pass 2 in groups of p2, no letters in between"""
    G1 = G_of_bounds(bounds_periodic(p1, n))
    G2 = G_of_bounds(bounds_periodic(p2, n))
    return [G1[j] for j in G2]


PERIODS = list(range(2, 13)) + [92]
PAIRS = [(a, b) for a in PERIODS for b in PERIODS if (a, b) != (2, 2)]
EAST92 = set(range(20, 24)) | set(range(29, 33))


def encrypt_G(pt, sq, G):
    qi = {ch: k for k, ch in enumerate(sq)}
    x = []
    for ch in pt:
        x += [qi[ch] // 5, qi[ch] % 5]
    y = [x[g] for g in G]
    return "".join(sq[y[2 * k] * 5 + y[2 * k + 1]] for k in range(len(pt)))


def forced_bifid(G, ct92, crib=CR):
    """square-free crib contradictions of a Bifid programme G on a 92-letter text (R3 check of EP-0232).
    'equal': two cipher letters whose two coordinates come from the same parts of the same crib letters must be
    equal; 'value': a cipher letter made of (row of X, column of X) must be X.  Returns a list of dicts."""
    groups, contra = {}, []
    for k in range(len(ct92)):
        a, c = G[2 * k], G[2 * k + 1]
        m1, p1, m2, p2 = a >> 1, a & 1, c >> 1, c & 1
        if m1 in crib and m2 in crib:
            groups.setdefault((p1, crib[m1], p2, crib[m2]), []).append((k, m1, m2))
            if p1 == 0 and p2 == 1 and crib[m1] == crib[m2] and ct92[k] != crib[m1]:
                contra.append(dict(kind="value", k=[k], src=[m1, m2]))
    for lst in groups.values():
        k0, a0, b0 = lst[0]
        for k, m1, m2 in lst[1:]:
            if ct92[k] != ct92[k0]:
                contra.append(dict(kind="equal", k=[k0, k], src=[a0, b0, m1, m2]))
    return contra


def forced_trifid(b, ct97, crib=CRIB):
    """the same check for Trifid groups on the 97 letters (cube-free)"""
    groups, contra = {}, []
    for s, e in zip(b[:-1], b[1:]):
        L = e - s
        for kk in range(L):
            src = []
            for m in range(3):
                d = 3 * kk + m
                c = d // L
                src.append((c, s + d - c * L))
            if all(j in crib for _, j in src):
                groups.setdefault(tuple((c, crib[j]) for c, j in src), []).append(s + kk)
                if [c for c, _ in src] == [0, 1, 2] and len({crib[j] for _, j in src}) == 1 and \
                        ct97[s + kk] != crib[src[0][1]]:
                    contra.append(dict(kind="value", k=[s + kk]))
    for lst in groups.values():
        for k in lst[1:]:
            if ct97[k] != ct97[lst[0]]:
                contra.append(dict(kind="equal", k=[lst[0], k]))
    return contra


def random_square(rng):
    q = list(A25)
    rng.shuffle(q)
    return "".join(q)


# ------------------------------------------------------------------ EP-0234: Bifid on crib-word groups (free square)
def group_sources(s, e, order):
    """for each output k of the group [s, e): ((letter position, part), (letter position, part)); part 0 row, 1 col"""
    L = e - s
    seq = [(s + j, 0) for j in range(L)] + [(s + j, 1) for j in range(L)]
    if order == "cr":
        seq = [(s + j, 1) for j in range(L)] + [(s + j, 0) for j in range(L)]
    return [(seq[2 * k], seq[2 * k + 1]) for k in range(L)]


def forced_equalities_groups(groups, order, crib=CR):
    """output positions forced equal for every square (same crib-letter parts), from the crib alone"""
    seen, out = {}, []
    for s, e in groups:
        for k, ((m1, p1), (m2, p2)) in enumerate(group_sources(s, e, order)):
            if m1 in crib and m2 in crib:
                key = (p1, crib[m1], p2, crib[m2])
                if key in seen:
                    out.append((seen[key], s + k))
                else:
                    seen[key] = s + k
    return out


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def same_cell_conflicts(eqs):
    """eqs: list of (letter1, part1, letter2, part2) coordinate equalities on ONE square.  Returns the pairs of
    distinct letters forced into the same cell (same row class and same column class)."""
    uf = UF(52)
    idx = lambda L, part: 2 * A25.index(L) + part
    for a, pa, b, pb in eqs:
        uf.union(idx(a, pa), idx(b, pb))
    letters = sorted({x for a, _, b, _ in eqs for x in (a, b)})
    bad = []
    for i, x in enumerate(letters):
        for y in letters[i + 1:]:
            if uf.find(idx(x, 0)) == uf.find(idx(y, 0)) and uf.find(idx(x, 1)) == uf.find(idx(y, 1)):
                bad.append((x, y))
    return bad


def core_equations(ct92, s, e, order, outs, crib=CR):
    """coordinate equalities 'part of cipher letter at output k = part of the crib letter it came from' for the
    outputs k in `outs` of one group [s, e)"""
    eqs = []
    for k, srcs in enumerate(group_sources(s, e, order)):
        if s + k not in outs:
            continue
        for part_out, (m, p) in enumerate(srcs):
            eqs.append((ct92[s + k], part_out, crib[m], p))
    return eqs


# ------------------------------------------------------------------ EP-0233: Delastelle's helix (p.97, example p.98)
def pos(q, ch):
    return divmod(q.index(ch), 5)


def helix_enc(P, Q1, Q3, Q2, Q4, segs, L_order=False):
    """C[k] = Q2[row of P[k-1] in Q1, col of P[k] in Q3] (k even), Q4[row of P[k-1] in Q3, col of P[k] in Q1] (k odd);
    P[-1] = P[n-1] in each segment; order L keeps the copy of the first pair at the end"""
    C = [None] * len(P)
    for s, n in segs:
        seg = P[s:s + n]
        out = []
        for j in range(n):
            a, b = seg[j - 1], seg[j]
            if j % 2 == 0:
                out.append(Q2[pos(Q1, a)[0] * 5 + pos(Q3, b)[1]])
            else:
                out.append(Q4[pos(Q3, a)[0] * 5 + pos(Q1, b)[1]])
        if L_order:
            out = out[1:] + out[:1]
        C[s:s + n] = out
    return C


def helix_dec(C, Q1, Q3, Q2, Q4, segs, L_order=False):
    P = [None] * len(C)
    for s, n in segs:
        c = list(C[s:s + n])
        if L_order:
            c = c[-1:] + c[:-1]
        rc = [pos(Q2 if j % 2 == 0 else Q4, c[j]) for j in range(n)]
        for j in range(n):
            main = Q3 if j % 2 == 0 else Q1
            P[s + j] = main[rc[(j + 1) % n][0] * 5 + rc[j][1]]
    return P


def transpose(q):
    return "".join(q[c * 5 + r] for r in range(5) for c in range(5))


STD = {"AZrows": A25, "AZcols": transpose(A25), "KArows": KA25, "KAcols": transpose(KA25)}
ROWS = [(0, 4), (4, 30), (34, 28), (62, 30)]               # beta segments of the inscribed rows
TOPO = {"F": ([(0, 92)], False), "L": ([(0, 92)], True), "rF": (ROWS, False), "rL": (ROWS, True)}


def mask25(kidx):
    out = []
    for key, p in MASK_KEYS:
        for ph in range(p):
            out.append([KA25.index(key[((n if kidx == "red" else KEEP[n]) + ph) % p]) for n in range(92)])
    return out


MASK25 = {"red": mask25("red"), "orig": mask25("orig")}


def mask25_apply(T, k, inverse=False):
    sgn = -1 if inverse else 1
    return [KA25[(KA25.index(ch) + sgn * k[n]) % 25] for n, ch in enumerate(T)]


def seg_of(q, segs):
    for s, n in segs:
        if s <= q < s + n:
            return s, n
    raise ValueError(q)


def _square_ok(full, half):
    cell2, let2 = {}, {}
    for cell, L in full:
        if cell2.get(cell, L) != L or let2.get(L, cell) != cell:
            return False
        cell2[cell] = L
        let2[L] = cell
    need = {}
    for L, kind, val in half:
        if L in let2:
            r, c = divmod(let2[L], 5)
            if (kind == "r" and r != val) or (kind == "c" and c != val):
                return False
        else:
            need.setdefault(L, []).append((kind, val))
    free = [x for x in range(25) if x not in cell2]
    opts = {L: [x for x in free if all((k == "r" and x // 5 == v) or (k == "c" and x % 5 == v) for k, v in cs)]
            for L, cs in need.items()}
    letters = sorted(opts, key=lambda L: len(opts[L]))

    def bt(i, used):
        if i == len(letters):
            return True
        return any(bt(i + 1, used | {x}) for x in opts[letters[i]] if x not in used)
    return bt(0, frozenset())


def helix_free_ok(text92, a, b, kidx, mi, order, topo, crib=CR):
    """logic column (d) of EP-0233: Q1 = STD[a], Q3 = STD[b], auxiliary quadrants Q2 and Q4 FREE, K1/K2 mask
    (order 1: C = H(M(P)); order 2: C = M(H(P))).  True iff some pair of squares makes every crib letter fit (h = 0)."""
    Q1, Q3 = STD[a], STD[b]
    segs, Lo = TOPO[topo]
    k = MASK25[kidx][mi]
    c = list(text92) if order == 1 else mask25_apply(text92, k, inverse=True)
    if Lo:
        cF = [None] * 92
        for s, n in segs:
            seg = c[s:s + n]
            cF[s:s + n] = seg[-1:] + seg[:-1]
        c = cF
    tgt = ({q: KA25[(KA25.index(ch) + k[q]) % 25] for q, ch in crib.items()} if order == 1 else dict(crib))
    colc, rowc = {}, {}
    for q in sorted(crib):
        s, n = seg_of(q, segs)
        j = q - s
        par = j % 2
        main = Q3 if par == 0 else Q1
        tr, tc = pos(main, tgt[q])
        nxt = s + (j + 1) % n
        colc[q] = (par, c[q], tc)                 # column of C[q] in the auxiliary square of parity par
        rowc[nxt] = (1 - par, c[nxt], tr)          # row of C[q+1] in the other auxiliary square
    cons = {0: ([], []), 1: ([], [])}
    for j in sorted(set(colc) | set(rowc)):
        if j in colc and j in rowc:
            pc, lc, vc = colc[j]
            pr, lr, vr = rowc[j]
            cons[pc][0].append((vr * 5 + vc, lc))
        elif j in colc:
            pc, lc, vc = colc[j]
            cons[pc][1].append((lc, "c", vc))
        else:
            pr, lr, vr = rowc[j]
            cons[pr][1].append((lr, "r", vr))
    return _square_ok(*cons[0]) and _square_ok(*cons[1])


def helix_logic_labels(main_only=False):
    out = []
    for a in STD:
        for b in STD:
            for kidx in ("red", "orig"):
                for mi in range(18):
                    for order in (1, 2):
                        for topo in TOPO:
                            if main_only and not (a == b and kidx == "red" and topo == "F"):
                                continue
                            out.append((a, b, kidx, mi, order, topo))
    return out


def helix_single_square_equalities(crib=CR):
    """one auxiliary square for both parities, no mask, Q1 = Q3: cipher positions whose plain pair (P[j-1], P[j])
    is the same crib pair must carry the same letter, for any square"""
    full = [(q, (crib[q - 1], crib[q])) for q in sorted(crib) if q - 1 in crib]
    return [(full[x][0], full[y][0]) for x in range(len(full)) for y in range(x + 1, len(full))
            if full[x][1] == full[y][1]]
