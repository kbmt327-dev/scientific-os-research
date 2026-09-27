"""Draw the Note's figure from results/key-bound-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-key-bound.svg
"""
import json
import sys
from math import log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "key-bound-20260927.json").read_text(encoding="utf-8"))
pts = [(log2(int(m)), v) for m, v in rec["share_ic_at_or_below_k4"].items()]
X0, Y0, W, H = 110, 60, 800, 260
XMAX, YMAX = 5.0, 0.15


def xy(x, y):
    return X0 + W * x / XMAX, Y0 + H * (1 - y / YMAX)


out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="420" viewBox="0 0 1080 420">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">How flat can English get? Share of simulations '
       'with an IC as low as K4\'s, by key bits per position</text>']
for t in (0, 0.05, 0.10, 0.15):
    x0, y = xy(0, t)
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X0 + W}" y2="{y:.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{y + 4:.1f}" text-anchor="end" class="small">{t:.2f}</text>')
for b in range(0, 6):
    x, y0 = xy(b, 0)
    out.append(f'<text x="{x:.1f}" y="{Y0 + H + 20}" text-anchor="middle" class="small">{b}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 42}" text-anchor="middle" class="small">bits of key per position '
           f'(log2 of the number of freely chosen rows)</text>')
path = " ".join(("M" if k == 0 else "L") + "%.1f,%.1f" % xy(x, y) for k, (x, y) in enumerate(pts))
out.append(f'<path d="{path}" fill="none" stroke="#1f6f5c" stroke-width="2.5"/>')
for x, y in pts:
    px, py = xy(x, y)
    out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#1f6f5c"/>')
xr, _ = xy(2.86, 0)
out.append(f'<line x1="{xr:.1f}" y1="{Y0}" x2="{xr:.1f}" y2="{Y0 + H}" stroke="#b03a2e" stroke-width="2" '
           f'stroke-dasharray="6 4"/>')
out.append(f'<text x="{xr + 6:.1f}" y="{Y0 + 16}" class="small" fill="#b03a2e">redundancy of English, 2.86 bits</text>')
_, y5 = xy(0, 0.05)
out.append(f'<text x="{X0 + W + 8}" y="{y5 + 4:.1f}" class="small">5%</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 72}" class="small">K4\'s flat letter counts become plausible (about 5%) '
           f'only at about 3 bits per position, past what English redundancy can pin down.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
