"""Draw the Note's figure: unit x state x sync, which cells a recorded test closed (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-capability-matrix.svg
"""
import sys
from pathlib import Path

import k4_capability_matrix as M

rs = M.rows()
cov, part = M.cube(rs)
CW, CH, X0, Y0, GAP = 96, 30, 250, 90, 36
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{Y0 + 3 * (5 * CH + GAP) + 90}" '
       f'viewBox="0 0 1080 {Y0 + 3 * (5 * CH + GAP) + 90}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">What the recorded tests covered: unit x state x '
       'synchronisation (92 rows, no new K4 computation)</text>']
for j, y in enumerate(M.SYNCS):
    out.append(f'<text x="{X0 + CW * j + CW / 2}" y="{Y0 - 12}" text-anchor="middle" class="small">{M.EN[y]}</text>')
col = {"closed": "#1f6f5c", "touched": "#c9d3cf", "empty": "#fffdf8"}
for b, u in enumerate(M.UNITS):
    yb = Y0 + b * (5 * CH + GAP)
    out.append(f'<text x="{X0 - 235}" y="{yb + 5 * CH / 2 + 5}" class="small" font-weight="600">{M.EN[u]} unit</text>')
    for i, s in enumerate(M.STATES):
        y0 = yb + CH * i
        out.append(f'<text x="{X0 - 8}" y="{y0 + 20}" text-anchor="end" class="small">{M.EN[s]}</text>')
        for j, y in enumerate(M.SYNCS):
            k = "closed" if cov.get((u, s, y)) else ("touched" if part.get((u, s, y)) else "empty")
            out.append(f'<rect x="{X0 + CW * j + 2}" y="{y0 + 2}" width="{CW - 4}" height="{CH - 4}" fill="{col[k]}" '
                       f'stroke="#9aa5b1"/>')
            if k == "empty":
                out.append(f'<text x="{X0 + CW * j + CW / 2}" y="{y0 + 20}" text-anchor="middle" class="small" '
                           f'fill="#b03a2e">gap</text>')
yl = Y0 + 3 * (5 * CH + GAP) - 10
leg = [("closed", "closed or excluded by at least one test"), ("touched", "tested, not closed"),
       ("empty", "no test (gap)")]
for k, (c, lab) in enumerate(leg):
    out.append(f'<rect x="{X0 + 300 * k}" y="{yl}" width="18" height="18" fill="{col[c]}" stroke="#9aa5b1"/>')
    out.append(f'<text x="{X0 + 26 + 300 * k}" y="{yl + 14}" class="small">{lab}</text>')
out.append(f'<text x="60" y="{yl + 46}" class="small">A green cell can be closed by one narrow family only (for example '
           f'machines without fixed points); the Note lists which. Most gaps have no source that would fix an operator.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
