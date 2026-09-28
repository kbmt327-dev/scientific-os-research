"""The YAR measurement of EP-0139 (catalog J10): are three letters of one carved cipher row
(0-based columns 3, 4 and 6, the letters Y, A and R) raised on purpose, or is it a
construction offset?  The pre-registered statistic and classes, ported from the author's
audit script (committed there before any letter was measured).  Needs numpy.

Measurement (per letter, pixels of a public photo as served): the bounding box of the
cut-out letter, [col, x_left, x_right, y_top, y_bottom], for carved rows 13, 14 and 15
(row 14 holds the letters in question; rows 13 and 15 are controls).  Photos taken from
the back are mirrored; only column order and distances are used.

  y_c = (y_top + y_bottom) / 2; each row gets its own quadratic fit y_c ~ x.  Row 14 is fitted
  without columns 2..7.  Residuals r are in units of the row pitch P (median distance between
  neighbouring row fits at the x of columns 3..6).  Controls: rows 13 and 15, and row 14
  outside columns 2..7; sigma = 1.4826 MAD.  A letter is displaced when
  |r| >= T = max(5 sigma, 0.08 P, largest control |r|).
  intended     Y, A, R displaced; columns 2, 5, 7 and the nearby letters of rows 13/15 not
  local-build  displacement spreads to neighbours or rows 13/15 move the same way
  row-offset   nothing displaced but row 14 sits off the pitch grid at every x
  partial      some of Y, A, R displaced only;  none: nothing displaced
  Across photos a class stands when two photos from different positions agree.
"""
import statistics as st

import numpy as np

YAR = (3, 4, 6)
NEAR = (2, 5, 7)


def mad_sigma(v):
    v = np.asarray(v, float)
    return 1.4826 * float(np.median(np.abs(v - np.median(v)))) if len(v) else float("nan")


def qfit(xs, ys):
    deg = 2 if len(xs) >= 5 else 1
    return np.poly1d(np.polyfit(xs, ys, deg))


def centers(boxes):
    return {b[0]: ((b[1] + b[2]) / 2.0, (b[3] + b[4]) / 2.0, b[2] - b[1]) for b in boxes}


def yar(rows):
    c = {int(r): centers(b) for r, b in rows.items()}
    if 14 not in c:
        return {"class": "undecided", "why": "row 14 not measured"}
    fits = {}
    for r, d in c.items():
        keep = [k for k in d if not (r == 14 and 2 <= k <= 7)]
        fits[r] = qfit([d[k][0] for k in keep], [d[k][1] for k in keep])
    xs_yar = [c[14][k][0] for k in YAR if k in c[14]]
    pairs = [(a, a + 1) for a in sorted(c) if a + 1 in c]
    P = float(np.median([abs(fits[b](x) - fits[a](x)) for a, b in pairs for x in xs_yar]))
    res = {r: {k: (d[k][1] - fits[r](d[k][0])) / P for k in d} for r, d in c.items()}
    ctrl = [v for r, d in res.items() if r != 14 for v in d.values()]
    ctrl += [v for k, v in res[14].items() if not 2 <= k <= 7]
    sig = mad_sigma(ctrl)
    cmax = max(abs(v) for v in ctrl)
    T = max(5 * sig, 0.08, cmax)
    disp = {k: abs(v) >= T for k, v in res[14].items()}
    out = {"P_px": P, "sigma_P": sig, "ctrl_max_P": cmax, "T_P": T, "T_cm": T * 11.7,
           "n_row14": len(c[14]), "n_ctrl": len(ctrl),
           "row14_resid_P": {k: round(v, 4) for k, v in sorted(res[14].items())}}
    if P < 20 or sig > 0.04 or len(c[14]) < 8 or len(ctrl) < 15:
        out["class"] = "undecided"
        out["why"] = "resolution"
        return out
    pitch_x = float(np.median(np.diff(sorted(v[0] for v in c[14].values()))))
    x0, x1 = min(xs_yar) - 1.5 * pitch_x, max(xs_yar) + 1.5 * pitch_x
    near_rows = {r: {k: res[r][k] for k in c[r] if x0 <= c[r][k][0] <= x1} for r in (13, 15) if r in c}
    near_disp = any(abs(v) >= T for d in near_rows.values() for v in d.values())
    yar_mean = st.mean(res[14][k] for k in YAR if k in res[14])
    same_way = any(abs(v) >= abs(yar_mean) / 2 and np.sign(v) == np.sign(yar_mean)
                   for d in near_rows.values() for v in d.values())
    y_all = all(disp.get(k, False) for k in YAR)
    y_any = any(disp.get(k, False) for k in YAR)
    n_near = any(disp.get(k, False) for k in NEAR)
    out.update({"displaced": sorted(k for k, v in disp.items() if v), "yar_mean_P": yar_mean,
                "near_rows_resid_P": {r: {k: round(v, 4) for k, v in d.items()} for r, d in near_rows.items()}})
    if y_all and not n_near and not near_disp and not same_way:
        out["class"] = "intended"
    elif y_any and (n_near or near_disp or same_way):
        out["class"] = "local-build"
    elif y_any:
        out["class"] = "intended" if y_all else "partial"
    elif not any(disp.values()):
        g = [(fits[14](x) - fits[13](x), fits[15](x) - fits[14](x)) for x in xs_yar] if 13 in c and 15 in c else []
        if g and all(abs(a - b) >= 0.15 * P for a, b in g) and len({np.sign(a - b) for a, b in g}) == 1:
            out["class"] = "row-offset"
        else:
            out["class"] = "none"
    else:
        out["class"] = "partial"
    return out


def verdict(classes):
    cls = [c for c in classes if c != "undecided"]
    if not cls:
        return "undecided (no usable photo)"
    if len(set(cls)) > 1:
        return "undecided (photos disagree)"
    return cls[0] + (" (provisional, one photo)" if len(cls) == 1 else f" ({len(cls)} photos agree)")
