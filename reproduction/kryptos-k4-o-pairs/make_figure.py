"""Draw the Note's figure: for each square method, K4 is inconsistent; the bar is the share of
1,000 shuffled ciphertexts that are consistent (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-o-pairs.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "o-pairs-20260928.json").read_text(encoding="utf-8"))
rows = [(k, v["settings"], v["shuffles_consistent"][0] / v["shuffles_consistent"][1])
        for k, v in rec["free_square_settings"].items()]
X0, W, Y0 = 400, 560, 60
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="330" viewBox="0 0 1080 330">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Pairs (21+o, 59+o) as digraphs in 5x5 squares: '
       'K4 is inconsistent in all 56 settings</text>']
yend = Y0 + 40 * len(rows)
for t in range(0, 101, 20):
    x = X0 + W * t / 100
    out.append(f'<line x1="{x:.1f}" y1="{Y0 - 6}" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 18}" text-anchor="middle" class="small">{t}%</text>')
for i, (name, n, share) in enumerate(rows):
    y = Y0 + 40 * i
    out.append(f'<text x="{X0 - 10}" y="{y + 12}" text-anchor="end" class="small">{name.split(" (")[0]} '
               f'({n} settings)</text>')
    out.append(f'<text x="{X0 - 10}" y="{y + 28}" text-anchor="end" class="small" fill="#b03a2e">K4: inconsistent</text>')
    out.append(f'<rect x="{X0}" y="{y + 4}" width="{max(W * share, 1.5):.1f}" height="22" fill="#9aa5b1"/>')
    out.append(f'<text x="{X0 + W * share + 6:.1f}" y="{y + 20}" class="small">{share:.1%}</text>')
notes = ["Grey bar: share of 1,000 shuffled ciphertexts (W positions kept) that are consistent with the cribs.",
         "Every setting rejects K4 by an exact proof, but shuffles mostly fail too, so this is a logical",
         f"refutation, not evidence that K4 is further from these methods than random. Keyed squares: 0 of "
         f"{rec['keyed_squares']['settings']:,}."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{yend + 50 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
