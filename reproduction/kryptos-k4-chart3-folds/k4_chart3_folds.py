"""The two fold lines on the public chart #3 reconstruction, and a key that restarts at them (EP-0148, EP-0167).

Chart #3 is a 14 x 31 grid (rows and columns counted from 1).  K3's 336 letters fill rows 1-10 and row 11,
columns 1-26; the '?' is row 11, column 27; K4 (0-based positions 0-96) fills row 11, columns 28-31, then rows
12-14.  The only marks inside K4's cells are two fold lines through the whole sheet, at columns 6 and 25.
Only the cell geometry is used here; no K3 letters.

Restart test (EP-0167): if the same key sequence restarts at every fold crossing, crib letters at the same
distance from their segment start (the same phase) must have the same key, whatever generated the key.
    fixed shift table (Vigenere / Beaufort / variant Beaufort, A-Z or KRYPTOS): the key values must agree
    arbitrary rows chosen by phase (a different method): the same-phase pairs must be a partial bijection
Null: the ciphertext shuffled with random.Random(20260930), 100,000 times, in the author's order.
Standard library only.
"""
import random

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ROWS, COLS, NK3 = 14, 31, 336
FOLD_COLUMNS = (6, 25)


def cell(k):
    """(row, column), 1-based, of sheet index k (K3 = 0..335, '?' = 336, K4 position i = 337 + i)"""
    return k // COLS + 1, k % COLS + 1


def k4_cell(i):
    return cell(NK3 + 1 + i)


def fold_crossings():
    """K4 positions and the number of K3 cells on the fold columns"""
    k4 = sorted(i for i in range(len(K4)) if k4_cell(i)[1] in FOLD_COLUMNS)
    k3 = sum(1 for k in range(NK3) if cell(k)[1] in FOLD_COLUMNS)
    return k4, k3


def segment_starts(cols=FOLD_COLUMNS):
    return [0] + sorted(i for i in range(len(K4)) if k4_cell(i)[1] in cols)


def phase(i, starts):
    return i - max(s for s in starts if s <= i)


def groups(starts):
    g = {}
    for i in sorted(CRIB):
        g.setdefault(phase(i, starts), []).append(i)
    return [v for v in g.values() if len(v) > 1]


def key(alpha, kind, c, p):
    c, p = alpha.index(c), alpha.index(p)
    return (c - p) % 26 if kind == "Vig" else (c + p) % 26 if kind == "Beau" else (p - c) % 26


def fixed_fail(ct, G):
    """key disagreements over the same-phase groups, per convention"""
    out = {}
    for an, alpha in (("AZ", AZ), ("KA", KA)):
        for kind in ("Vig", "Beau", "VBeau"):
            out[an + " " + kind] = sum(len({key(alpha, kind, ct[i], CRIB[i]) for i in g}) - 1 for g in G)
    return out


def rows_fail(ct, G):
    """pairs breaking a partial bijection (same plaintext <=> same ciphertext within a phase)"""
    bad = 0
    for g in G:
        for a in g:
            for b in g:
                if a < b and (CRIB[a] == CRIB[b]) != (ct[a] == ct[b]):
                    bad += 1
    return bad


CASES = {"all six crossings": FOLD_COLUMNS, "column 6 only": (6,), "column 25 only": (25,)}


def run(shuffles=100000, seed=20260930):
    rng = random.Random(seed)
    out = {}
    for name, cols in CASES.items():
        st = segment_starts(cols)
        G = groups(st)
        f, r = fixed_fail(K4, G), rows_fail(K4, G)
        le_f = le_r = 0
        for _ in range(shuffles):
            s = list(K4)
            rng.shuffle(s)
            s = "".join(s)
            le_f += min(fixed_fail(s, G).values()) <= min(f.values())
            le_r += rows_fail(s, G) <= r
        out[name] = {"starts": st, "same_phase_groups": G, "fixed_disagreements": f,
                     "fixed_shuffles_le": round(le_f / shuffles, 4), "rows_conflicts": r,
                     "rows_shuffles_le": round(le_r / shuffles, 4)}
    return out
