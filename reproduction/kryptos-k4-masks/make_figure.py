"""Draw the Note's figure: masked periodic keys by period (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-masks.svg
"""
import sys
from pathlib import Path

import k4_masks as M

power = M.periodic_power(200)
k4 = set(M.periodic_survivors(M.K4))
X0, Y0, W, H = 80, 60, 940, 110
bw = W / 48
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="470" viewBox="0 0 1080 470">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}.tiny{font-size:11px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Periodic key with a free mask: share of 200 shuffles '
       'that fit (bars) and K4 (dots)</text>']
for row, side in enumerate(("before", "after")):
    y0 = Y0 + row * (H + 60)
    out.append(f'<text x="{X0}" y="{y0 - 6}" class="small">mask {side} the key</text>')
    out.append(f'<line x1="{X0}" y1="{y0 + H}" x2="{X0 + W}" y2="{y0 + H}" class="grid"/>')
    out.append(f'<line x1="{X0}" y1="{y0 + H * 0.95:.1f}" x2="{X0 + W}" y2="{y0 + H * 0.95:.1f}" stroke="#b03a2e" '
               f'stroke-dasharray="4 4"/>')
    for p in range(1, 49):
        x = X0 + (p - 1) * bw
        r = power[(side, p)]
        if r:
            out.append(f'<rect x="{x + 2:.1f}" y="{y0 + H * (1 - r):.1f}" width="{bw - 4:.1f}" height="{H * r:.1f}" '
                       f'fill="#d9dde2"/>')
        if (side, p) in k4:
            col = "#b03a2e" if r <= 0.05 else "#1f6f5c"
            out.append(f'<circle cx="{x + bw / 2:.1f}" cy="{y0 + H + 10}" r="4" fill="{col}"/>')
        if p % 4 == 0 or p == 1 or p in (19, 38):
            out.append(f'<text x="{x + bw / 2:.1f}" y="{y0 + H + 30}" text-anchor="middle" class="tiny">{p}</text>')
lines = ["A dot marks a period where K4 fits. Where shuffles almost never fit (below the dashed 5% line) K4 fits only at",
         "19 and 38 (red), and both come from one coincidence in the crib (R to P at 27 and 65, 38 apart).",
         "Elsewhere the test cannot decide: most shuffles fit too. A key linear in position fits nowhere, on either side."]
for k, line in enumerate(lines):
    out.append(f'<text x="{X0}" y="{Y0 + 2 * (H + 60) + 16 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
