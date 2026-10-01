"""Draw the Note's figure (standard library only): for each stage, the closed-form chance
expectation and K4's non-identity hits; confirmed hits are 0 in every stage.

    python make_figure.py ../../content/assets/kryptos-k4-layout-transposition.svg
"""
import json
import sys
from math import log10
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "layout-transposition-20261001.json").read_text(encoding="utf-8"))
st = rec["stages"]
fam = rec["pi"]["by_family"]
rows = [("S1", "all 208 settings, up to 4 crib errors", st["S1"]),
        ("S2", "48 settings (3 x 31 turn family), up to 7 errors", st["S2"]),
        ("S3", "other 160 settings, up to 7 errors", st["S3"])]
X0, W, lo, hi = 420, 520, -7, 0
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="400" viewBox="0 0 1080 400">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:16px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       f'<text x="540" y="30" text-anchor="middle" class="title">Layout transposition (104 x 2 orders = 208 settings) '
       f'then the procedure enumerator: 0 confirmed hits</text>']
yend = 60 + 70 * len(rows)
for t in range(lo, hi + 1):
    x = X0 + W * (t - lo) / (hi - lo)
    out.append(f'<line x1="{x:.1f}" y1="54" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 18}" text-anchor="middle" class="small">1e{t}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{yend + 38}" text-anchor="middle" class="small">'
           f'grey bar: expected chance hits (closed form, log scale)</text>')
for i, (name, sub, s) in enumerate(rows):
    y = 60 + 70 * i
    out.append(f'<text x="{X0 - 12}" y="{y + 16}" text-anchor="end" class="small" font-weight="600">{name}: {sub}</text>')
    h = s["K4_non_identity_hits"]
    lab = "K4: 0 hits" if h == 0 else "K4: 1 hit, stopped by the rule; not confirmed (p = 0.81)"
    out.append(f'<text x="{X0 - 12}" y="{y + 34}" text-anchor="end" class="small" style="fill:#b03a2e">{lab}</text>')
    w = W * (log10(s["chance"]) - lo) / (hi - lo)
    out.append(f'<rect x="{X0}" y="{y + 4}" width="{w:.1f}" height="24" fill="#9aa5b1"/>')
    out.append(f'<text x="{X0 + w + 6:.1f}" y="{y + 21}" class="small">{s["chance"]:.2g}</text>')
notes = [f"Pi: {fam['T1']} turns of K4's 3 x 31 carved shape, {fam['T2']} routes at width 21, {fam['T4']} routes on "
         f"96- and 98-cell rectangles (fixed before any run on K4).",
         "The one S2 hit is within the chance expectation (0.23 over S2 and S3) and failed the confirmation statistic.",
         "Shuffles: 0 hits. Planted controls: 7/9 to 9/9 found at the true transposition, 0 at a wrong one."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{yend + 70 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
