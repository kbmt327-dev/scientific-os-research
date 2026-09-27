"""Draw the Note's figure from results/chosen-rows-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-chosen-rows.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "chosen-rows-20260927.json").read_text(encoding="utf-8"))["cover"]
labels = {"keywords": "Hint keywords (40 rows)", "John832": "John 8:32 words (9 rows)",
          "worldclock": "World Clock places (146 rows)"}
X0, W = 330, 620
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="330" viewBox="0 0 1080 330">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Crib letters that any row of the list could explain '
       '(best convention), out of 24</text>']
for t in (0, 6, 12, 18, 24):
    x = X0 + W * t / 24
    out.append(f'<line x1="{x:.1f}" y1="52" x2="{x:.1f}" y2="170" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="188" text-anchor="middle" class="small">{t}</text>')
for k, (name, r) in enumerate(rec.items()):
    y = 58 + 38 * k
    out.append(f'<text x="{X0 - 10}" y="{y + 18}" text-anchor="end" class="small">{labels[name]}</text>')
    out.append(f'<rect x="{X0}" y="{y}" width="{W * r["best_cover"] / 24:.1f}" height="26" fill="#1f6f5c"/>')
    xm = X0 + W * r["null"]["null_median"] / 24
    out.append(f'<line x1="{xm:.1f}" y1="{y - 3}" x2="{xm:.1f}" y2="{y + 29}" stroke="#c9a227" stroke-width="3"/>')
    out.append(f'<text x="{X0 + W * r["best_cover"] / 24 + 8:.1f}" y="{y + 18}" class="small" fill="#fffdf8">'
               f'</text>')
x24 = X0 + W
out.append(f'<line x1="{x24}" y1="48" x2="{x24}" y2="172" stroke="#b03a2e" stroke-width="2"/>')
lines = ["Green: K4. Yellow tick: median over 200 shuffled texts. A list below 24 (red line) cannot produce the crib",
         "under any rule for choosing its rows. The internal run found the same for all 44 lists with up to 64 rows,",
         "including the K1-K3 words and the K3 grids; sequential choosing reached at most 10/24 in 190 million settings."]
for k, line in enumerate(lines):
    out.append(f'<text x="60" y="{226 + 22 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
