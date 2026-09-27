"""Draw the Note's figure: roughness S of random crib keys, K4 and model-smooth keys (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-physical-keys.svg
"""
import sys
from collections import Counter
from pathlib import Path

import k4_physical_keys as P

r = Counter(P.random_roughness(2000))
k4 = P.roughness(P.K4)
X0, Y0, W, H = 90, 60, 900, 240
vals = list(range(0, 14))
bw = W / len(vals)
top = max(r.values())
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="460" viewBox="0 0 1080 460">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">How rough is the key along the carved rows? '
       'Roughness S of 2,000 random crib keys, and K4</text>']
for k, v in enumerate(vals):
    x = X0 + k * bw
    h = H * r.get(v, 0) / top
    col = "#b03a2e" if v == k4 else "#9aa5b1"
    out.append(f'<rect x="{x + 4:.1f}" y="{Y0 + H - h:.1f}" width="{bw - 8:.1f}" height="{h:.1f}" fill="{col}"/>')
    out.append(f'<text x="{x + bw / 2:.1f}" y="{Y0 + H + 18}" text-anchor="middle" class="small">{v}</text>')
x0, x1 = X0, X0 + 5 * bw
out.append(f'<rect x="{x0:.1f}" y="{Y0 - 10}" width="{x1 - x0:.1f}" height="8" fill="#1f6f5c"/>')
out.append(f'<text x="{x0:.1f}" y="{Y0 - 16}" class="small">smooth keys from the 3D model: S of 4 or less in 95% or more (sight lines, slow shadow clocks)</text>')
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 40}" text-anchor="middle" class="small">S (largest second difference '
           f'along rows, or 2x2 cross difference, in key steps)</text>')
lines = [f"K4 (red) has S = {k4}, the median of random keys. Keys read off a smooth physical map rarely exceed S = 4",
         "(S of 10 or more: 0 of 828 sight lines, at most 2.3% of slow shadow clocks), so K4's crib keys look nothing",
         "like them. Keys that depend only on horizontal position are ruled out outright: positions 32 and 63, and",
         "33 and 64, share a column but need different keys in every convention."]
for k, line in enumerate(lines):
    out.append(f'<text x="{X0}" y="{Y0 + H + 72 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
