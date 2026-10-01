"""Draw the Note's figure: for every Portax period P = 1..48, K4 is inconsistent in both layers; the bars are the
share of 200 shuffled ciphertexts that are consistent (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-portax-playfair-mask.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "portax-playfair-mask-20260930.json").read_text(encoding="utf-8"))
per = rec["portax"]["per_period"]
X0, Y0, W, H = 90, 70, 920, 200
bw = W / 48
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="420" viewBox="0 0 1080 420">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Portax with a free substitution: '
       'K4 is inconsistent at every period P = 1..48 (96 exact proofs)</text>']
for t in (0, 10, 20, 30, 40):
    y = Y0 + H - H * t / 40
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X0 + W}" y2="{y:.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{y + 4:.1f}" text-anchor="end" class="small">{t}%</text>')
for P in range(1, 49):
    x = X0 + bw * (P - 1)
    for k, (layer, col) in enumerate((("after", "#5d6d7e"), ("before", "#d68910"))):
        share = per[layer][str(P)]["shuffles_SAT"] / per[layer][str(P)]["shuffles"]
        h = H * share / 0.40
        out.append(f'<rect x="{x + 2 + k * (bw - 4) / 2:.1f}" y="{Y0 + H - h:.1f}" width="{(bw - 4) / 2:.1f}" '
                   f'height="{h:.1f}" fill="{col}"/>')
    if P % 4 == 0 or P == 1:
        out.append(f'<text x="{x + bw / 2:.1f}" y="{Y0 + H + 18}" text-anchor="middle" class="small">{P}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 38}" text-anchor="middle" class="small">period P</text>')
out.append(f'<text x="{X0 - 60}" y="{Y0 - 14}" class="small">share of 200 shuffles consistent</text>')
out.append(f'<rect x="{X0 + 560}" y="{Y0 - 26}" width="12" height="12" fill="#5d6d7e"/>'
           f'<text x="{X0 + 578}" y="{Y0 - 15}" class="small">substitution after (up to 37%, P = 26)</text>')
out.append(f'<rect x="{X0 + 560}" y="{Y0 - 8}" width="12" height="12" fill="#d68910"/>'
           f'<text x="{X0 + 578}" y="{Y0 + 3}" class="small">substitution before (1 of 9,600 overall)</text>')
notes = ["K4: inconsistent at all 48 periods in both layers. Planted texts: 20/20 consistent at every period.",
         "Free-square Playfair followed by a shift mask: K4 inconsistent in m1 (6), m2 p <= 5 (60), m3 (7,680) and",
         "m4 (15,660) settings; m2 p = 6..12 undecidable. Shuffles mostly fail too: logical refutations, not rarer than random."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{Y0 + H + 75 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
