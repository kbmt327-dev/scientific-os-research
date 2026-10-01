"""One phase shift in the grouping of block ciphers on K4 without its Ws (EP-0169).

Digraph families: a setting (b, phi0) pairs letters (i, i+1) with i = phi0 (mod 2) before b and
i = 1 - phi0 (mod 2) from b on; one letter at the shift stays unpaired.  Bifid families: period p
(0 = whole text) with a first alignment a0, and the alignment restarts at b.

Exact tests that need only K4 and its public cribs:
  * free Four-square (two free cipher squares, standard or keyword plain squares);
  * a fixed arbitrary digraph chart (C08), on 97 letters or on the 92 without W;
  * Bifid with one free square and CM-Bifid with two free squares (coordinate solver).
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
RED = "".join(K4[i] for i in KEEP)                       # 92 letters, 25 types
CR = {KEEP.index(i): ch for i, ch in CRIB.items()}       # cribs at reduced positions 20-32, 59-69
N92 = 92

# hint keywords for keyed plain squares (the list of the W-squares Note, EP-0110)
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


def plain_squares():
    """the standard square and the distinct keyword squares (40)"""
    out = {square(""): "std"}
    for w in sorted(set(KEYWORDS)):
        out.setdefault(square(w), w)
    return list(out)


# ------------------------------------------------------------ digraph shift settings
def shift_pairs(b, phi0, n):
    before = [(i, i + 1) for i in range(phi0, n - 1, 2) if i + 1 < b]
    after = [(i, i + 1) for i in range(1 - phi0, n - 1, 2) if i >= b]
    return before + after


def raw_settings(n):
    return [(b, phi0) for b in range(n + 1) for phi0 in (0, 1)]


def crib_settings(crib=CR, n=N92):
    """deduplicated by the pairs with both letters in the crib: {pairs: [(b, phi0), ...]}"""
    out = {}
    for b, phi in raw_settings(n):
        key = tuple(p for p in shift_pairs(b, phi, n) if p[0] in crib and p[1] in crib)
        out.setdefault(key, []).append((b, phi))
    return out


def full_settings(n):
    out = {}
    for b, phi in raw_settings(n):
        out.setdefault(tuple(shift_pairs(b, phi, n)), []).append((b, phi))
    return out


def is_global(labels, n):
    return any(b in (0, n) for b, _ in labels)


def fs_consistent(text, plain_sq, pairs, crib=CR):
    """free cipher squares: each crib digraph fixes one cell of each; consistent iff no cell holds two
    letters and no letter sits in two cells of one square"""
    cs = coords(plain_sq)
    cells = [{}, {}]
    for i, j in pairs:
        (ra, ca), (rb, cb) = cs[crib[i]], cs[crib[j]]
        for q, cell, letter in ((0, (ra, cb), text[i]), (1, (rb, ca), text[j])):
            if cells[q].setdefault(cell, letter) != letter:
                return False
    return all(len(set(c.values())) == len(c) for c in cells)


def four_square_enc(q1, q2):
    p, c1, c2 = coords(A25), coords(q1), coords(q2)
    return lambda a, b: (q1[p[a][0] * 5 + p[b][1]], q2[p[b][0] * 5 + p[a][1]])


def c08_conflicts(ct, known, pairs):
    """fixed arbitrary digraph chart: equal cipher digraphs need agreeing known plaintext letters, and
    equal fully known plaintext digraphs need equal cipher digraphs"""
    by_c, by_p, bad = {}, {}, 0
    for i, j in pairs:
        cp = ct[i] + ct[j]
        pl = (known.get(i), known.get(j))
        g = by_c.setdefault(cp, [None, None])
        for s in (0, 1):
            if pl[s] is not None:
                if g[s] is None:
                    g[s] = pl[s]
                elif g[s] != pl[s]:
                    bad += 1
        if None not in pl and by_p.setdefault(pl, cp) != cp:
            bad += 1
    return bad


# ------------------------------------------------------------ Bifid / CM-Bifid
def bf_blocks(p, a0, b, n=N92):
    bd = {0, n}
    if p == 0:
        bd.add(b)
    else:
        bd |= set(range(a0, b, p)) | set(range(b, n, p))
    bd = sorted(x for x in bd if 0 <= x <= n)
    return [(s, e) for s, e in zip(bd[:-1], bd[1:]) if e > s]


def bf_settings(crib=CR, n=N92):
    """{crib-touching blocks: [(p, a0, b), ...]}; b = n is the unshifted setting"""
    out = {}
    for p in [0] + list(range(2, 13)):
        for a0 in (range(p) if p else [0]):
            for b in range(1, n + 1):
                key = tuple(x for x in bf_blocks(p, a0, b, n) if any(i in crib for i in range(*x)))
                out.setdefault(key, []).append((p, a0, b))
    return out


def bf_encrypt(pt, q1, q2, blks):
    pos1 = coords(q1)
    out = [None] * len(pt)
    for s, e in blks:
        seq = [pos1[ch][0] for ch in pt[s:e]] + [pos1[ch][1] for ch in pt[s:e]]
        for j in range(e - s):
            out[s + j] = q2[seq[2 * j] * 5 + seq[2 * j + 1]]
    return "".join(out)


class Cap(Exception):
    pass


def bf_consistent(ct, known, blks, one, node_cap=2_000_000):
    """Exact: do square coordinates exist that reproduce the known letters?  one=True: Bifid with one
    square (Q1 = Q2); one=False: CM-Bifid with two squares.  None = node cap reached."""
    par = list(range(200))
    nsq = 1 if one else 2

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    ci = [A25.index(ch) for ch in ct]
    coff = 0 if one else 25
    for s, e in blks:                   # unify plaintext coordinates with ciphertext coordinates
        m = e - s
        seq = [2 * A25.index(known[j]) if j in known else None for j in range(s, e)]
        seq = seq + [None if v is None else v + 1 for v in seq]
        for j in range(m):
            for t in (0, 1):
                a = seq[2 * j + t]
                if a is not None:
                    ra, rb = find(a), find(2 * (coff + ci[s + j]) + t)
                    if ra != rb:
                        par[ra] = rb
    nv = 25 * nsq
    cls = [find(a) for a in range(2 * nv)]
    val, used, nodes, maxv = {}, [set(), set()], [0], [-1]

    def options(v):
        sq = v // 25
        rc, cc = cls[2 * v], cls[2 * v + 1]
        rs = [val[rc]] if rc in val else range(5)
        cs = [val[cc]] if cc in val else range(5)
        return [(r, c) for r in rs for c in cs if (r, c) not in used[sq]], rc, cc

    def rec(left):                      # assign each letter of each square a distinct cell
        nodes[0] += 1
        if nodes[0] > node_cap:
            raise Cap
        if not left:
            return True
        best, bo = None, None
        for v in left:
            o = options(v)
            if not o[0]:
                return False
            if bo is None or len(o[0]) < len(bo[0]):
                best, bo = v, o
                if len(o[0]) == 1:
                    break
        opts, rc, cc = bo
        rest = [v for v in left if v != best]
        sq = best // 25
        for r, c in opts:
            newr, newc = rc not in val, cc not in val and cc != rc
            mv = maxv[0]
            if newr:
                if r > mv + 1:          # symmetry breaking on fresh coordinate values
                    continue
                mv2 = max(mv, r)
            else:
                mv2 = mv
            if newc and c > mv2 + 1:
                continue
            if rc == cc and r != c:
                continue
            saved = maxv[0]
            if newr:
                val[rc] = r
            if newc:
                val[cc] = c
            maxv[0] = max(maxv[0], r if newr else -1, c if newc else -1)
            used[sq].add((r, c))
            if rec(rest):
                return True
            used[sq].discard((r, c))
            if newr:
                del val[rc]
            if newc:
                del val[cc]
            maxv[0] = saved
        return False

    try:
        return rec(list(range(nv)))
    except Cap:
        return None


def plant92(rng):
    """random letters with the cribs written in (the author's controls used English text)"""
    return [CR.get(i, rng.choice(A25)) for i in range(N92)]
