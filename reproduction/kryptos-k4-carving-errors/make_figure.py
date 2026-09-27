"""Draw the Note's figure from results/carving-errors-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-carving-errors.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.loads((HERE / "results" / "carving-errors-20260927.json").read_text(encoding="utf-8"))
d = d["periodic_min_errors"]["by_period"]
X0, Y0, W, H, YMAX = 80, 60, 940, 250, 22
bw = W / 48
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="430" viewBox="0 0 1080 430">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}.tiny{font-size:11px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Fewest wrong crib letters a periodic key needs, by '
       'period: K4 (dot) and 100 shuffles (bar)</text>']
for t in (0, 5, 10, 15, 20):
    y = Y0 + H * (1 - t / YMAX)
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X0 + W}" y2="{y:.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{y + 4:.1f}" text-anchor="end" class="small">{t}</text>')
y5 = Y0 + H * (1 - 5 / YMAX)
out.append(f'<line x1="{X0}" y1="{y5:.1f}" x2="{X0 + W}" y2="{y5:.1f}" stroke="#b03a2e" stroke-dasharray="6 4"/>')
out.append(f'<text x="{X0 + W - 4}" y="{y5 - 6:.1f}" text-anchor="end" class="small" fill="#b03a2e">5 errors</text>')
for p in range(1, 49):
    v = d[str(p)]
    x = X0 + (p - 0.5) * bw
    ya, yb = Y0 + H * (1 - v["shuffle_max"] / YMAX), Y0 + H * (1 - v["shuffle_min"] / YMAX)
    out.append(f'<rect x="{x - bw * 0.3:.1f}" y="{ya:.1f}" width="{bw * 0.6:.1f}" height="{max(yb - ya, 1):.1f}" '
               f'fill="#d9dde2"/>')
    out.append(f'<circle cx="{x:.1f}" cy="{Y0 + H * (1 - v["K4"] / YMAX):.1f}" r="3.5" fill="#1f6f5c"/>')
    if p % 4 == 0 or p == 1:
        out.append(f'<text x="{x:.1f}" y="{Y0 + H + 16}" text-anchor="middle" class="tiny">{p}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 34}" text-anchor="middle" class="small">period p</text>')
lines = ["Below the dashed line a key fits with at most 5 wrong crib letters. K4 needs more than 5 at every period up",
         "to 23 and tracks the shuffles throughout: carving errors do not make periodic keys more likely for K4",
         "than for random ciphertext."]
for k, line in enumerate(lines):
    out.append(f'<text x="{X0}" y="{Y0 + H + 60 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
