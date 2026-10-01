"""Draw the Note's figure: status of each machine family with one phase break, and the recorded
Hagelin English scores against the 40.4 threshold (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-machine-phase-break.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "machine-phase-break-20260930.json").read_text(encoding="utf-8"))
h = rec["EP-0176"]
ROWS = [
    ("Free-wiring rotor R-a (31.2 bit)", "closed", "K4 0; shuffles 0/200; planted 100/100"),
    ("Free-wiring rotor R-b (36.8 bit)", "closed", "K4 0; shuffles 0/200; planted 100/100"),
    ("Enigma + free substitution (43.7 bit)", "closed", "K4 0; shuffles 0/10; planted 20/20"),
    ("Hagelin M-209 type (search 52.6 bit)", "open", "no score >= 40.4; controls not run"),
    ("Chaocipher", "na", "no step counter: a break is not defined"),
]
COL = {"closed": "#1f6f5c", "open": "#c9a227", "na": "#9aa5b1"}
TXT = {"closed": "closed (logical)", "open": "undecidable", "na": "out of scope"}
H = 470
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{H}" viewBox="0 0 1080 {H}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.badge{font-size:12px;fill:#fffdf8;font-weight:600}'
       '.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Machines with one phase break '
       '(1,300 positions and sizes, 10.3 bit)</text>']
for k, (fam, st, note) in enumerate(ROWS):
    y = 50 + 32 * k
    out.append(f'<text x="30" y="{y + 17}" class="small">{fam}</text>')
    out.append(f'<rect x="360" y="{y + 2}" width="130" height="22" rx="4" fill="{COL[st]}"/>')
    out.append(f'<text x="425" y="{y + 17}" text-anchor="middle" class="badge">{TXT[st]}</text>')
    out.append(f'<text x="505" y="{y + 17}" class="small">{note}</text>')
# lower panel: Hagelin E_max
X0, W, Y0, EMAX = 360, 600, 250, 45.0
out.append(f'<text x="30" y="{Y0 - 14}" class="small" font-weight="600">Hagelin type: best English score '
           f'after hill-climbing every crib-consistent setting</text>')
bars = [("K4", h["K4"]["E_max"], h["climbs_b_weighted"], "#b03a2e")] + \
       [(f"shuffle {i + 1}", s["E_max"], s["climbs"], "#9aa5b1") for i, s in enumerate(h["shuffles"])]
yend = Y0 + 36 * len(bars)
for t in range(0, 46, 10):
    x = X0 + W * t / EMAX
    out.append(f'<line x1="{x:.1f}" y1="{Y0 - 4}" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 16}" text-anchor="middle" class="small">{t}</text>')
xt = X0 + W * h["threshold_E"] / EMAX
for i, (name, e, n, col) in enumerate(bars):
    y = Y0 + 36 * i
    out.append(f'<text x="{X0 - 10}" y="{y + 18}" text-anchor="end" class="small">{name} ({n:,} climbs)</text>')
    out.append(f'<rect x="{X0}" y="{y + 4}" width="{W * e / EMAX:.1f}" height="22" fill="{col}"/>')
    out.append(f'<text x="{X0 + W * e / EMAX + 6:.1f}" y="{y + 20}" class="small">{e:.2f}</text>')
out.append(f'<line x1="{xt:.1f}" y1="{Y0 - 8}" x2="{xt:.1f}" y2="{yend}" stroke="#17202a" stroke-width="2" '
           f'stroke-dasharray="5,4"/>')
out.append(f'<text x="{xt + 4:.1f}" y="{Y0 - 14 + 0}" class="small">threshold 40.4</text>')
notes = ["The shuffles had about 500 times fewer climbs than K4, and the best score grows with the number of climbs,",
         "so the bars are not comparable. Planted controls were not run, so it is unknown whether a true key would",
         "reach 40.4. The Hagelin row is therefore undecidable, not a negative result."]
for k, line in enumerate(notes):
    out.append(f'<text x="30" y="{yend + 42 + 18 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
