"""Draw the Note's figure from results/consistency-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-consistency.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "consistency-20260927.json").read_text(encoding="utf-8"))
rates = {int(p): r for p, r in rec["switching_shuffle_null"]["per_period_share"].items()}
feas = set(rec["switching_feasible_periods"]["AZ"]) | set(rec["switching_feasible_periods"]["KRYPTOS"])
cons = set(rec["switching_feasible_periods"]["constrained"])
X0, Y0, W, H = 80, 70, 940, 240
bw = W / 52
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="420" viewBox="0 0 1080 420">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}.tiny{font-size:11px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Vigenere / Beaufort / variant chosen freely at each '
       'position, periodic key: which periods fit the cribs?</text>']
for t in (0, 0.25, 0.5, 0.75, 1.0):
    y = Y0 + H * (1 - t)
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X0 + W}" y2="{y:.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{y + 4:.1f}" text-anchor="end" class="small">{t:g}</text>')
for p in range(1, 53):
    x = X0 + (p - 1) * bw
    r = rates[p]
    if r:
        out.append(f'<rect x="{x + 2:.1f}" y="{Y0 + H * (1 - r):.1f}" width="{bw - 4:.1f}" height="{H * r:.1f}" '
                   f'fill="{"#d9dde2" if p not in cons else "#9aa5b1"}"/>')
    mark = "#1f6f5c" if p in feas else "#b03a2e"
    sym = "o" if p in feas else "x"
    out.append(f'<text x="{x + bw / 2:.1f}" y="{Y0 + H + 22}" text-anchor="middle" class="small" fill="{mark}">'
               f'{sym}</text>')
    if p % 4 == 0 or p == 1:
        out.append(f'<text x="{x + bw / 2:.1f}" y="{Y0 + H + 40}" text-anchor="middle" class="tiny">{p}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 58}" text-anchor="middle" class="small">period p</text>')
out.append(f'<text x="30" y="{Y0 + H / 2}" class="small" transform="rotate(-90 30 {Y0 + H / 2})" '
           f'text-anchor="middle">share of 2,000 shuffles that fit</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 84}" class="small">Marks under the axis are K4: x = no key fits, '
           f'o = fits. K4 fits only at p = 27-29, where no two crib positions share a residue (light bars).</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 104}" class="small">Shuffles almost never fit at p ≤ 24 either (1 in 2,000), and '
           f'{rec["switching_shuffle_null"]["share_failing_every_constrained_p"]:.0%} of them fail every '
           f'constrained period, as K4 does.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
