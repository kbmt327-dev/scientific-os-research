"""K1-K3 production traces on the carved layout (EP-0141): row lengths against letter widths,
row breaks against word breaks, and the post hoc offset from a 31-column grid, recomputed
from recorded per-row numbers.  Standard library only.

The carved text of K1-K3 is not published on this site, so the per-row mean letter widths
(three fonts as stand-ins for hand-cut letters) are recorded numbers; the re-breaking null of
T2 and the word boundaries of T1 need the text and are recorded only.
"""
import random
from itertools import accumulate
from math import comb, prod


def ranks(v):
    """Average ranks (1-based) with ties."""
    order = sorted(range(len(v)), key=v.__getitem__)
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def ols_residuals(n, m, fit_rows, test_rows):
    """Fit n = a + b m on fit_rows, return residuals of test_rows."""
    xs, ys = [m[i] for i in fit_rows], [n[i] for i in fit_rows]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    return [n[i] - (a + b * m[i]) for i in test_rows]


def at_least_one(ps):
    return 1 - prod(1 - p for p in ps)


def offset_range(lens):
    """Range of the cumulative offset of the row ends from a 31-column grid, the plate's mean excess removed."""
    base = (sum(lens) - 31 * len(lens)) / len(lens)
    c = [s - base * (k + 1) for k, s in enumerate(accumulate(x - 31 for x in lens))]
    return max(c) - min(c)


def permutation_null(lens, n, rng):
    obs, sims, x = offset_range(lens), [], list(lens)
    for _ in range(n):
        rng.shuffle(x)
        sims.append(offset_range(x))
    return obs, sum(sims) / n, (1 + sum(s <= obs + 1e-9 for s in sims)) / (n + 1)


def last_k_all(lens, k=4, value=31):
    """Exact chance that the last k rows all have `value` letters under a random order of the rows."""
    m = sum(x == value for x in lens)
    return comb(m, k) / comb(len(lens), k)
