"""Draw the Note's figure from results/affine-hill-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-affine-hill.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "affine-hill-20260927.json").read_text(encoding="utf-8"))
hill = rec["recorded_not_rerun"]["EP-0117 periodic Hill, all 160 settings (n = 2, 3; with and without vector; p = 1-8)"]
segs = [("decidable, K4 inconsistent", hill["K4_inconsistent_in_decidable"], "#1f6f5c"),
        ("not decidable (too few crib blocks per matrix)", hill["undecidable"], "#c9a227")]
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="330" viewBox="0 0 1080 330">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Periodic Hill matrices on K4: 160 settings '
       '(block size 2 or 3, with or without a vector, period 1-8)</text>']
x, W, tot = 60, 960, 160
for label, n, col in segs:
    w = W * n / tot
    out.append(f'<rect x="{x:.1f}" y="60" width="{w:.1f}" height="44" fill="{col}"/>')
    out.append(f'<text x="{x + w / 2:.1f}" y="88" text-anchor="middle" class="small" fill="#fffdf8">{n}</text>')
    out.append(f'<rect x="{x:.1f}" y="120" width="14" height="14" fill="{col}"/>')
    out.append(f'<text x="{x + 20:.1f}" y="132" class="small">{label}</text>')
    x += w
lines = ["A setting counts as decidable when at most 5 of 100 shuffled texts are consistent or unresolved.",
         "In the 69 undecidable settings K4 behaves like the shuffles. With matrices taken from listed texts,",
         "all 160 settings give 0 of 2,378,384 (expected by chance 8e-21).",
         "Position-varying affine maps with polynomial multipliers (1,896 x 17,576 x 4) give 0 fits;",
         "planted controls are all found."]
for k, line in enumerate(lines):
    out.append(f'<text x="60" y="{180 + 24 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
