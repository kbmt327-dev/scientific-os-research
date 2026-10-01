"""The finite set Pi of layout transpositions (EP-0185 / EP-0186), ported from the author's
k4_r41_pi.py to the standard library.  Pure geometry on 97 positions: no sculpture text.

Convention.  S = the substituted text in plaintext order, C = the carved ciphertext;
a transposition is an index array src with C[j] = S[src[j]].
Order A undoes it (the crib goes back to plaintext positions 21-33 / 63-73);
order B keeps C and moves the crib to the carved positions inv[i].

Routes on a grid (cells in row-major order): d = 0 write rows, read columns (the K3-type turn);
d = 1 the inverse; four column-read variants (column order and direction): 8 per grid.

Families
  T1  K4's carved shape: 4 letters, then 3 rows of 31.  The 3 x 31 core with the first 4 letters
      fixed at the head (8), moved to the tail (8), or the whole shape routed (8)
  T2  width 21: 97 = 4 x 21 + 13, partial row last or first (16)
  T3  the same shape on the plate's 31-column grid: identical to T1 'shape' (duplicates)
  T4  96 = 4x24, 24x4, 8x12, 12x8, 6x16, 16x6 with one letter outside (first or last, 96 items);
      98 = 7x14, 14x7 with one null cell at the start or the end (32 items)
Duplicates are merged and the identity is dropped.
"""
import hashlib
import random

N = 97


def rect_cells(rows, cols):
    return [(r, c) for r in range(rows) for c in range(cols)]


def column_read(cells, v):
    rev_cols, rev_rows = v & 1, (v >> 1) & 1
    cols = sorted({c for _, c in cells}, reverse=bool(rev_cols))
    out = []
    for c in cols:
        out += sorted([rc for rc in cells if rc[1] == c], key=lambda rc: rc[0], reverse=bool(rev_rows))
    return out


def route(cells, d, v):
    rm, cm = list(cells), column_read(cells, v)
    if d == 0:
        pos = {rc: k for k, rc in enumerate(rm)}
        return [pos[rc] for rc in cm]
    pos = {rc: k for k, rc in enumerate(cm)}
    return [pos[rc] for rc in rm]


def embed(sub, carved_off, s_off, fixed=()):
    src = [None] * N
    for j, s in enumerate(sub):
        src[carved_off + j] = s_off + s
    for j, i in fixed:
        src[j] = i
    assert sorted(src) == list(range(N))
    return src


def with_null(cells, d, v, null_at):
    sub = route(cells, d, v)
    s_index = [k - (1 if null_at == 0 else 0) for k in sub if k != null_at]
    assert sorted(s_index) == list(range(N))
    return s_index


def build():
    items = []
    DV = [(d, v) for d in (0, 1) for v in range(4)]
    core = rect_cells(3, 31)
    shape = [(0, c) for c in range(27, 31)] + [(r, c) for r in (1, 2, 3) for c in range(31)]
    for d, v in DV:
        sub = route(core, d, v)
        items.append(("T1", embed(sub, 4, 4, fixed=[(j, j) for j in range(4)])))
        items.append(("T1", embed(sub, 4, 0, fixed=[(j, 93 + j) for j in range(4)])))
        items.append(("T1", route(shape, d, v)))
        items.append(("T3", route(shape, d, v)))
    w21_last = [(r, c) for r in range(5) for c in range(21) if r * 21 + c < N]
    w21_first = [(0, c) for c in range(8, 21)] + [(r, c) for r in range(1, 5) for c in range(21)]
    for d, v in DV:
        items.append(("T2", route(w21_last, d, v)))
        items.append(("T2", route(w21_first, d, v)))
    for rows, cols in ((4, 24), (24, 4), (8, 12), (12, 8), (6, 16), (16, 6)):
        for d, v in DV:
            sub = route(rect_cells(rows, cols), d, v)
            items.append(("T4", embed(sub, 1, 1, fixed=[(0, 0)])))
            items.append(("T4", embed(sub, 0, 0, fixed=[(96, 96)])))
    for rows, cols in ((7, 14), (14, 7)):
        for d, v in DV:
            for null_at in (0, 97):
                items.append(("T4", with_null(rect_cells(rows, cols), d, v, null_at)))
    return items


def pi_set():
    """deduplicated, identity dropped, first-seen order: list of (src tuple, family of first label)"""
    seen = {}
    ident = tuple(range(N))
    for fam, src in build():
        t = tuple(src)
        if t != ident and t not in seen:
            seen[t] = fam
    return list(seen.items())


def digest(ps):
    h = hashlib.sha256()
    for src, _ in ps:
        h.update(bytes(src))
    return h.hexdigest()


def inverse(src):
    inv = [0] * N
    for j, s in enumerate(src):
        inv[s] = j
    return inv


def transpose(s, src):
    return "".join(s[src[j]] for j in range(N))


def undo(c, src):
    out = [None] * N
    for j, s in enumerate(src):
        out[s] = c[j]
    return "".join(out)


def planted_roundtrip(src, seed):
    """a random 97-letter text, transposed and undone, comes back unchanged"""
    rng = random.Random(seed)
    s = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(N))
    return undo(transpose(s, src), src) == s
