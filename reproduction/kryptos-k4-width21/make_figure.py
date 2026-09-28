"""Draw the Note's figure: repeated vertical pair types R and single-letter coincidences kappa at
each lag, K4 against the permutation mean (standard library only, reads results/).

    python make_figure.py ../../content/assets/kryptos-k4-width21.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "width21-20260928.json").read_text(encoding="utf-8"))
lags = list(rec["lags"])
X0, Y0, W, H = 90, 70, 900, 250
MAX = 12
gw = W / len(lags)
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="440" viewBox="0 0 1080 440">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Only the lag-21 pair count stands out: '
       'K4 against 20,000 permutations of its letters</text>']
for t in range(0, MAX + 1, 2):
    y = Y0 + H - H * t / MAX
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X0 + W}" y2="{y:.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{y + 4:.1f}" text-anchor="end" class="small">{t}</text>')
for i, w in enumerate(lags):
    d = rec["lags"][w]
    x = X0 + gw * i
    for j, (key, ekey, col) in enumerate((("R", "E_R", "#b03a2e" if w == "21" else "#1f6f5c"),
                                          ("kappa", "E_kappa", "#9aa5b1"))):
        bx = x + 14 + j * (gw / 2 - 8)
        h = H * d[key] / MAX
        out.append(f'<rect x="{bx:.1f}" y="{Y0 + H - h:.1f}" width="{gw / 2 - 20:.1f}" height="{h:.1f}" fill="{col}"/>')
        ey = Y0 + H - H * d[ekey] / MAX
        out.append(f'<line x1="{bx - 3:.1f}" y1="{ey:.1f}" x2="{bx + gw / 2 - 17:.1f}" y2="{ey:.1f}" stroke="#17202a" '
                   f'stroke-width="2"/>')
    out.append(f'<text x="{x + gw / 2:.1f}" y="{Y0 + H + 18}" text-anchor="middle" class="small">lag {w}</text>')
leg = [("#1f6f5c", "R: pair types seen twice or more (red: lag 21)"),
       ("#9aa5b1", "kappa: equal letters at that distance"), ("#17202a", "black tick: permutation mean")]
for k, (c, lab) in enumerate(leg):
    out.append(f'<rect x="{X0 + 330 * k}" y="{Y0 + H + 34}" width="14" height="14" fill="{c}"/>')
    out.append(f'<text x="{X0 + 20 + 330 * k}" y="{Y0 + H + 46}" class="small">{lab}</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 76}" class="small">R at 21 is 11 against 3.5 (P = 0.0001; paid over widths 2-48 about '
           f'0.001-0.003). The column period (kappa at 21), two and three rows apart (42, 63) and the diagonals (20, 22)</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 96}" class="small">are at chance, so nothing in K4 besides this one pair table points to 21.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
