"""Draw the Note's figure (standard library only).

Left: the enumerator runs with a slip, K4's hits and the closed-form chance expectation.
Right: EP-0151's 240 shuffle P values, sorted, against the uniform quantiles.

    python make_figure.py ../../content/assets/kryptos-k4-crib-shifts.svg
"""
import json
import sys
from math import log10
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "crib-shifts-20260930.json").read_text(encoding="utf-8"))
r49 = rec["EP-0149 slips inside both cribs"]
r65 = rec["EP-0165 shift between the cribs with crib errors"]
P = sorted(rec["EP-0151 shift between the cribs"]["periodic_arbitrary_rows"]["P"].values())

out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="440" viewBox="0 0 1080 440">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:16px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="270" y="30" text-anchor="middle" class="title">Procedure enumerator with a slip: K4 hits</text>',
       '<text x="810" y="30" text-anchor="middle" class="title">Periodic arbitrary rows, crib-2 shift: 240 cells</text>']

# left panel: chance expectation on a log scale, K4 hits as text
rows = [("Inside both cribs (EP-0149)", f"{r49['configurations']} settings, up to {r49['crib_errors_max']} crib errors",
         r49["chance"]["e4"], r49["K4_other_hits"]),
        ("Between the cribs (EP-0165)", f"{r65['configurations']} settings (d = -2, -1, +1, +2), up to "
         f"{r65['crib_errors_max']} crib errors", r65["chance"], r65["K4_other_hits"])]
X0, W, lo, hi = 60, 400, -14, 0
for t in range(lo, hi + 1, 2):
    x = X0 + W * (t - lo) / (hi - lo)
    out.append(f'<line x1="{x:.1f}" y1="70" x2="{x:.1f}" y2="270" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="288" text-anchor="middle" class="small">1e{t}</text>')
out.append(f'<text x="{X0 + W / 2}" y="308" text-anchor="middle" class="small">expected chance passes (log scale)</text>')
for i, (name, sub, ch, hits) in enumerate(rows):
    y = 80 + 100 * i
    out.append(f'<text x="{X0}" y="{y}" class="small" font-weight="600">{name}</text>')
    out.append(f'<text x="{X0}" y="{y + 17}" class="small">{sub}</text>')
    w = W * (log10(ch) - lo) / (hi - lo)
    out.append(f'<rect x="{X0}" y="{y + 26}" width="{w:.1f}" height="22" fill="#9aa5b1"/>')
    out.append(f'<text x="{X0 + w + 6:.1f}" y="{y + 42}" class="small">chance {ch:.1e}</text>')
    out.append(f'<text x="{X0}" y="{y + 66}" class="small" style="fill:#b03a2e">K4: {hits} hits; two shuffles: 0 and 0</text>')
for k, line in enumerate(["With no crib errors, any shift between the cribs is already ruled out",
                          "for the enumerator by the per-crib run (EP-0134): no computation needed."]):
    out.append(f'<text x="{X0}" y="{340 + 18 * k}" class="small">{line}</text>')

# right panel: sorted P against uniform quantiles
PX, PY, S = 620, 60, 260
m = len(P)
for t in (0, 0.25, 0.5, 0.75, 1):
    out.append(f'<line x1="{PX + S * t:.1f}" y1="{PY}" x2="{PX + S * t:.1f}" y2="{PY + S}" class="grid"/>')
    out.append(f'<line x1="{PX}" y1="{PY + S - S * t:.1f}" x2="{PX + S}" y2="{PY + S - S * t:.1f}" class="grid"/>')
    out.append(f'<text x="{PX + S * t:.1f}" y="{PY + S + 16}" text-anchor="middle" class="small">{t:g}</text>')
    out.append(f'<text x="{PX - 6}" y="{PY + S - S * t + 4:.1f}" text-anchor="end" class="small">{t:g}</text>')
out.append(f'<line x1="{PX}" y1="{PY + S}" x2="{PX + S}" y2="{PY}" stroke="#5d6d7e" stroke-dasharray="4 3"/>')
for k, p in enumerate(P):
    q = (k + 1) / (m + 1)
    out.append(f'<circle cx="{PX + S * q:.1f}" cy="{PY + S - S * p:.1f}" r="2.2" fill="#2e86c1"/>')
out.append(f'<text x="{PX + S / 2}" y="{PY + S + 36}" text-anchor="middle" class="small">uniform quantile</text>')
out.append(f'<text x="{PX - 40}" y="{PY + S / 2}" text-anchor="middle" class="small" '
           f'transform="rotate(-90 {PX - 40} {PY + S / 2})">shuffle P of the cell</text>')
out.append(f'<text x="{PX + 20}" y="{PY + S - 14}" class="small">smallest P {P[0]} (p 8, d +2)</text>')
for k, line in enumerate(["No cell falls clearly below the dashed line (K4 not rarer than shuffles).",
                          f"Expected smallest of {m} independent P values: about {1 / (m + 1):.3f}."]):
    out.append(f'<text x="560" y="{PY + S + 64 + 18 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
