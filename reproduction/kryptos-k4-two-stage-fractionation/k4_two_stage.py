"""Building blocks for the two-stage fractionation Note (EP-0202, 0219, 0220, 0221, 0222, 0239).  Standard library only.

Everything here is position geometry or a public cipher device; no sculpture text other than the K4 ciphertext
and its public cribs.

  * Pi: the 104 layout transpositions of EP-0186 (ported from the author's k4_r41_pi.py, the same code as in the
    layout-transposition package).  Convention C[j] = S[src[j]].  With the W's as separators, the five carved W's
    land at S positions src[j] (j a W position); a Pi that puts a W on a crib position is a hard contradiction
    of the separator model.  'inverse' means the transposition inverse(src).
  * frame / pairs / blocks: the W-segment frame of the 92 letters, Playfair pairings (from 0, from 1, per
    W segment) and Bifid blocks (period 2..12, whole text = 0, per W segment), as in the author's EP-0221 code.
  * Playfair (EP-0125 rules: same row -> right, same column -> down, rectangle -> own row / partner's column;
    a doubled pair (a, a) follows the same-row rule; no filler) and Bifid (EP-0110: rows of the block, then
    columns, read in pairs) on 25-letter squares (A-Z without W).
  * The R1-1 coordinate transpositions of EP-0219: K3's encryption written as two rotations of a grid, and the
    three registered ways to carry it from 336 letters to 184 coordinates.  Pure index geometry.
"""
import hashlib
import math

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
N = 97
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A25 = AZ.replace("W", "")
WPOS = [i for i in range(N) if K4[i] == "W"]
KEEP = [i for i in range(N) if K4[i] != "W"]


# ------------------------------------------------------------------ Pi (EP-0185 / EP-0186)
def _rect_cells(rows, cols):
    return [(r, c) for r in range(rows) for c in range(cols)]


def _column_read(cells, v):
    rev_cols, rev_rows = v & 1, (v >> 1) & 1
    cols = sorted({c for _, c in cells}, reverse=bool(rev_cols))
    out = []
    for c in cols:
        out += sorted([rc for rc in cells if rc[1] == c], key=lambda rc: rc[0], reverse=bool(rev_rows))
    return out


def _route(cells, d, v):
    rm, cm = list(cells), _column_read(cells, v)
    if d == 0:
        pos = {rc: k for k, rc in enumerate(rm)}
        return [pos[rc] for rc in cm]
    pos = {rc: k for k, rc in enumerate(cm)}
    return [pos[rc] for rc in rm]


def _embed(sub, carved_off, s_off, fixed=()):
    src = [None] * N
    for j, s in enumerate(sub):
        src[carved_off + j] = s_off + s
    for j, i in fixed:
        src[j] = i
    assert sorted(src) == list(range(N))
    return src


def _with_null(cells, d, v, null_at):
    sub = _route(cells, d, v)
    s_index = [k - (1 if null_at == 0 else 0) for k in sub if k != null_at]
    assert sorted(s_index) == list(range(N))
    return s_index


def pi_build():
    items = []
    dv = [(d, v) for d in (0, 1) for v in range(4)]
    core = _rect_cells(3, 31)
    shape = [(0, c) for c in range(27, 31)] + [(r, c) for r in (1, 2, 3) for c in range(31)]
    for d, v in dv:
        sub = _route(core, d, v)
        items.append(("T1", _embed(sub, 4, 4, fixed=[(j, j) for j in range(4)])))
        items.append(("T1", _embed(sub, 4, 0, fixed=[(j, 93 + j) for j in range(4)])))
        items.append(("T1", _route(shape, d, v)))
        items.append(("T3", _route(shape, d, v)))
    w21_last = [(r, c) for r in range(5) for c in range(21) if r * 21 + c < N]
    w21_first = [(0, c) for c in range(8, 21)] + [(r, c) for r in range(1, 5) for c in range(21)]
    for d, v in dv:
        items.append(("T2", _route(w21_last, d, v)))
        items.append(("T2", _route(w21_first, d, v)))
    for rows, cols in ((4, 24), (24, 4), (8, 12), (12, 8), (6, 16), (16, 6)):
        for d, v in dv:
            sub = _route(_rect_cells(rows, cols), d, v)
            items.append(("T4", _embed(sub, 1, 1, fixed=[(0, 0)])))
            items.append(("T4", _embed(sub, 0, 0, fixed=[(96, 96)])))
    for rows, cols in ((7, 14), (14, 7)):
        for d, v in dv:
            for null_at in (0, 97):
                items.append(("T4", _with_null(_rect_cells(rows, cols), d, v, null_at)))
    return items


def pi_set():
    """deduplicated, identity dropped, first-seen order: list of (src tuple, family)"""
    seen = {}
    ident = tuple(range(N))
    for fam, src in pi_build():
        t = tuple(src)
        if t != ident and t not in seen:
            seen[t] = fam
    return list(seen.items())


def pi_digest(ps):
    h = hashlib.sha256()
    for src, _ in ps:
        h.update(bytes(src))
    return h.hexdigest()


def inverse(src):
    inv = [0] * len(src)
    for j, s in enumerate(src):
        inv[s] = j
    return inv


def w_on_crib(src):
    """True if a carved W lands on a crib position (src[j] for j a W position)"""
    return any(src[j] in CRIB for j in WPOS)


# ------------------------------------------------------------------ the W frame, pairings, Bifid blocks
def frame(src):
    """W set in the S frame, kept positions (92) and the W-segment starts in reduced positions"""
    wset = {src[j] for j in WPOS}
    keep = [i for i in range(N) if i not in wset]
    ridx = {i: j for j, i in enumerate(keep)}
    starts, begin = [], 0
    for i in sorted(wset) + [N]:
        if i > begin:
            starts.append(ridx[begin])
        begin = i + 1
    return wset, keep, starts


def pairs(mode, starts, n=92):
    if mode in (0, 1):
        return [(i, i + 1) for i in range(mode, n - 1, 2)]
    bounds = starts + [n]
    return [(i, i + 1) for s, e in zip(bounds[:-1], bounds[1:]) for i in range(s, e - 1, 2)]


def blocks(p, starts, n=92):
    if p == "seg":
        return list(zip(starts, starts[1:] + [n]))
    p = p or n
    return [(s, min(s + p, n)) for s in range(0, n, p)]


# ------------------------------------------------------------------ devices
def square(word=""):
    seen = []
    for ch in word.upper() + A25:
        if ch in A25 and ch not in seen:
            seen.append(ch)
    return "".join(seen)


def pf_pair(q, a, b):
    ia, ib = q.index(a), q.index(b)
    ra, ca = divmod(ia, 5)
    rb, cb = divmod(ib, 5)
    if ra == rb:
        return q[ra * 5 + (ca + 1) % 5], q[rb * 5 + (cb + 1) % 5]
    if ca == cb:
        return q[((ra + 1) % 5) * 5 + ca], q[((rb + 1) % 5) * 5 + cb]
    return q[ra * 5 + cb], q[rb * 5 + ca]


def pf_unpair(q, a, b):
    ia, ib = q.index(a), q.index(b)
    ra, ca = divmod(ia, 5)
    rb, cb = divmod(ib, 5)
    if ra == rb:
        return q[ra * 5 + (ca - 1) % 5], q[rb * 5 + (cb - 1) % 5]
    if ca == cb:
        return q[((ra - 1) % 5) * 5 + ca], q[((rb - 1) % 5) * 5 + cb]
    return q[ra * 5 + cb], q[rb * 5 + ca]


def playfair(text, q, mode, starts, dec=False):
    out = list(text)
    f = pf_unpair if dec else pf_pair
    for i, j in pairs(mode, starts, len(text)):
        out[i], out[j] = f(q, text[i], text[j])
    return "".join(out)


def bifid(text, q, p, starts, dec=False):
    out = list(text)
    pos = {ch: divmod(k, 5) for k, ch in enumerate(q)}
    for s, e in blocks(p, starts, len(text)):
        co = [pos[x] for x in text[s:e]]
        m = e - s
        if dec:
            seq = [v for rc in co for v in rc]
            out[s:e] = [q[seq[j] * 5 + seq[m + j]] for j in range(m)]
        else:
            seq = [rc[0] for rc in co] + [rc[1] for rc in co]
            out[s:e] = [q[seq[j] * 5 + seq[j + 1]] for j in range(0, 2 * m, 2)]
    return "".join(out)


# ------------------------------------------------------------------ EP-0219 R1-1: K3's double rotation, carried to 184
NC = 184


def cells_rows(n, w, conv):
    q, r = divmod(n, w)
    if r == 0 or conv == "last":
        return [(i // w, i % w) for i in range(n)]
    return [(0, c) for c in range(w - r, w)] + [(1 + i // w, i % w) for i in range(n - r)]


def cells_cols(n, h, conv):
    q, r = divmod(n, h)
    if r == 0:
        return [(i // q, i % q) for i in range(n)]
    cells = []
    for row in range(h):
        if conv == "colLast":
            length, off = (q + 1, 0) if row < r else (q, 0)
        else:
            length, off = (q + 1, 0) if row >= h - r else (q, 1)
        cells += [(row, off + c) for c in range(length)]
    return cells


def rotate_read(cells, d):
    """cells in written order -> gather index of the rotated grid read by rows (cw: columns left to right, each
    bottom to top; ccw: columns right to left, each top to bottom)"""
    cols = sorted({c for _, c in cells}, reverse=(d == "ccw"))
    pos = {rc: k for k, rc in enumerate(cells)}
    out = []
    for c in cols:
        out += [pos[rc] for rc in sorted([rc for rc in cells if rc[1] == c], key=lambda rc: rc[0],
                                         reverse=(d == "cw"))]
    return out


def two_stage(s1, s2):
    return [s1[j] for j in s2]


K3_DESC = [(7, 84, "cw"), (7, 84, "ccw"), (14, 42, "cw"), (14, 42, "ccw"), (21, 28, "cw"), (21, 28, "ccw"),
           (28, 21, "cw"), (28, 21, "ccw"), (42, 14, "cw"), (42, 14, "ccw"), (84, 7, "cw"), (84, 7, "ccw")]


def k3_permutation(w1, w2, d):
    """the 336-position gather index of K3's encryption written with widths (w1, w2), both stages turned d"""
    return two_stage(rotate_read(cells_rows(336, w1, "last"), d), rotate_read(cells_rows(336, w2, "last"), d))


def r11_labels():
    out = []
    for w1, w2, d in K3_DESC:
        h1, h2 = 336 // w1, 336 // w2
        core = (w1, w2) in ((14, 42), (42, 14))
        for c1 in ("last", "first"):
            for c2 in ("last", "first"):
                out.append(("F1", core, tuple(two_stage(rotate_read(cells_rows(NC, w1, c1), d),
                                                        rotate_read(cells_rows(NC, w2, c2), d)))))
        for c1 in ("last", "first"):
            for c2 in ("last", "first"):
                v1, v2 = math.ceil(NC / h1), math.ceil(NC / h2)
                out.append(("F2", False, tuple(two_stage(rotate_read(cells_rows(NC, v1, c1), d),
                                                         rotate_read(cells_rows(NC, v2, c2), d)))))
        for c1 in ("colLast", "colFirst"):
            for c2 in ("colLast", "colFirst"):
                out.append(("F3", False, tuple(two_stage(rotate_read(cells_cols(NC, h1, c1), d),
                                                         rotate_read(cells_cols(NC, h2, c2), d)))))
    return out


LPERM = {"alt": list(range(NC)), "rc": [2 * (i % 92) + i // 92 for i in range(NC)]}


def same_letter_pairs(g):
    """number of recombined letters whose two coordinates come from one plaintext letter"""
    return sum(g[2 * k] // 2 == g[2 * k + 1] // 2 for k in range(92))


def r11_settings():
    labs = r11_labels()
    ts, order = {}, []
    for form, core, t in labs:
        if t not in ts:
            ts[t] = dict(form=form, core=core)
            order.append(t)
        ts[t]["core"] = ts[t]["core"] or core
    sets = []
    for t in order:
        for lay in ("alt", "rc"):
            g = [LPERM[lay][x] for x in t]
            col = ("core" if ts[t]["core"] else ts[t]["form"]) + "|" + lay
            sets.append(dict(col=col, same=same_letter_pairs(g)))
    return labs, order, sets
