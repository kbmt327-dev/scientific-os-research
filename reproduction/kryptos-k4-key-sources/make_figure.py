"""Draw the Note's figure: vertical repeats by width (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-key-sources.svg
"""
import sys
from pathlib import Path

import k4_key_sources as S

counts = {w: S.vertical_repeats(S.K4, w) for w in S.WIDTHS}
X0, Y0, W, H, YMAX = 90, 60, 900, 240, 12
bw = W / len(counts)
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="420" viewBox="0 0 1080 420">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}.tiny{font-size:11px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">K4 written in rows of width w: vertical letter pairs '
       'that occur twice or more</text>']
for t in (0, 4, 8, 12):
    y = Y0 + H * (1 - t / YMAX)
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X0 + W}" y2="{y:.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{y + 4:.1f}" text-anchor="end" class="small">{t}</text>')
for k, (w, c) in enumerate(counts.items()):
    x = X0 + k * bw
    col = "#b03a2e" if w == 21 else "#9aa5b1"
    out.append(f'<rect x="{x + 2:.1f}" y="{Y0 + H * (1 - c / YMAX):.1f}" width="{bw - 4:.1f}" '
               f'height="{H * c / YMAX:.1f}" fill="{col}"/>')
    if w % 4 == 0 or w == 21 or w == 2:
        out.append(f'<text x="{x + bw / 2:.1f}" y="{Y0 + H + 16}" text-anchor="middle" class="tiny">{w}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 36}" text-anchor="middle" class="small">width w</text>')
lines = ["Width 21 gives 11, the most of any width: about 1 in 20,000 permutations of K4 reach it there, and",
         "about 1 in 1,000 reach an equally small tail probability at some width 2-48. Keys taken from texts",
         "or from a period of 21 do not produce it, so it remains unexplained."]
for k, line in enumerate(lines):
    out.append(f'<text x="{X0}" y="{Y0 + H + 62 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
