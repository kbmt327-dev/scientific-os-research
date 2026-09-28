"""Width 21 in K4's ciphertext (EP-0146): which statistics point to 21, and which only follow from
the lag-21 pair table.  Ciphertext only; the cribs are used only to list which revealed pieces
start on a width-21 row.  Ported from the author's audit script; needs numpy.
"""
from collections import defaultdict

import numpy as np

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

LAGS = (7, 14, 20, 21, 22, 28, 35, 42, 63)


def R(M, w):
    """number of lag-w pair types (C_i, C_{i+w}) that occur at least twice (Bean's count)"""
    code = np.sort(M[:, :-w] * 26 + M[:, w:], axis=1)
    eq = code[:, 1:] == code[:, :-1]
    start = eq & np.concatenate([np.ones((M.shape[0], 1), bool), ~eq[:, :-1]], axis=1)
    return start.sum(1)


def kappa(M, w):
    return (M[:, :-w] == M[:, w:]).sum(1)


def mi(M, w):
    """plug-in mutual information (bits) of the lag-w pair table"""
    out = np.empty(M.shape[0])
    n = M.shape[1] - w
    for r in range(M.shape[0]):
        t = np.zeros((26, 26))
        np.add.at(t, (M[r, :-w], M[r, w:]), 1)
        pa, pb = t.sum(1) / n, t.sum(0) / n
        nz = t > 0
        p = t[nz] / n
        out[r] = (p * np.log2(p / np.outer(pa, pb)[nz])).sum()
    return out


def coincident_pairpairs(M, w):
    """number of index pairs i<j with (C_i, C_{i+w}) = (C_j, C_{j+w})"""
    code = M[:, :-w] * 26 + M[:, w:]
    out = np.empty(M.shape[0], int)
    for r in range(M.shape[0]):
        _, c = np.unique(code[r], return_counts=True)
        out[r] = (c * (c - 1) // 2).sum()
    return out


def R_nodouble(M, w):
    """R_w without the types whose only repeat is (i, i+1), i.e. produced by doubles at i and i+w"""
    out = np.zeros(M.shape[0], int)
    for r in range(M.shape[0]):
        m = M[r]
        seen = defaultdict(list)
        for i in range(len(m) - w):
            seen[(m[i], m[i + w])].append(i)
        out[r] = sum(1 for pos in seen.values() if len(pos) >= 2 and not (len(pos) == 2 and pos[1] - pos[0] == 1))
    return out


def permutations(nperm=20000, seed=2109):
    rng = np.random.default_rng(seed)
    k4 = np.array([AZ.index(c) for c in K4])
    return k4[None], np.stack([rng.permutation(k4) for _ in range(nperm)])


def repeated_types(w=21):
    seen = defaultdict(list)
    for i in range(97 - w):
        seen[K4[i] + K4[i + w]].append(i)
    return {k: v for k, v in seen.items() if len(v) >= 2}


def doubles():
    return [i for i in range(96) if K4[i] == K4[i + 1]]
