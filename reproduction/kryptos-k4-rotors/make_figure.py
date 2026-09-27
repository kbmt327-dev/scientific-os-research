"""Draw the Note's figure from results/rotors-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-rotors.svg
"""
import json
import sys
from math import log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "rotors-20260927.json").read_text(encoding="utf-8"))
rows = list(rec["log2_settings"].items())
crib = 24 * log2(26)
X0, W, MAX = 360, 640, 120.0
h = 90 + 34 * len(rows) + 70
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{h}" viewBox="0 0 1080 {h}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Rotor-machine families tested on K4: settings searched '
       '(log2) and settings that fit (all 0)</text>']
yend = 56 + 34 * len(rows)
for t in range(0, 121, 20):
    x = X0 + W * t / MAX
    out.append(f'<line x1="{x:.1f}" y1="50" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 18}" text-anchor="middle" class="small">{t}</text>')
for k, (label, v) in enumerate(rows):
    y = 56 + 34 * k
    out.append(f'<text x="{X0 - 10}" y="{y + 17}" text-anchor="end" class="small">{label}</text>')
    out.append(f'<rect x="{X0}" y="{y + 2}" width="{W * v / MAX:.1f}" height="22" fill="#1f6f5c"/>')
    out.append(f'<text x="{X0 + W * v / MAX + 6:.1f}" y="{y + 18}" class="small">{v:.1f} bits, 0 fit</text>')
xc = X0 + W * crib / MAX
out.append(f'<line x1="{xc:.1f}" y1="46" x2="{xc:.1f}" y2="{yend}" stroke="#b03a2e" stroke-width="2"/>')
out.append(f'<text x="{xc - 6:.1f}" y="{yend + 38}" text-anchor="end" class="small" fill="#b03a2e">'
           f'crib: {crib:.1f} bits</text>')
out.append(f'<text x="30" y="{h - 16}" class="small">The free wiring or free substitution in each family is solved exactly, not searched: '
           f'it adds about 88 bits that the counts above do not include.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
