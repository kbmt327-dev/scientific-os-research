"""Draw the Note's figure: status of each machine family with one phase break, and the recorded Hagelin
English scores (K4, three shuffles, and the five controls planted under K4's own crib stage on 2026-10-02)
against the 40.4 threshold (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-machine-phase-break.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "machine-phase-break-20260930.json").read_text(encoding="utf-8"))
add = json.loads((HERE / "results" / "hagelin-controls-under-20261002.json").read_text(encoding="utf-8"))
h = rec["EP-0176"]
k4v5 = add["k4_v5_reproduction"]
ctl = add["controls_under"]
ROWS = [
    ("Free-wiring rotor R-a (31.2 bit)", "closed", "K4 0; shuffles 0/200; planted 100/100"),
    ("Free-wiring rotor R-b (36.8 bit)", "closed", "K4 0; shuffles 0/200; planted 100/100"),
    ("Enigma + free substitution (43.7 bit)", "closed", "K4 0; shuffles 0/10; planted 20/20"),
    ("Hagelin M-209 type (search 52.6 bit)", "ctl",
     f"no score >= {h['threshold_E']}; controls under K4's crib stage {sum(c['truth_found'] for c in ctl)}/{len(ctl)} (2026-10-02)"),
    ("Chaocipher", "na", "no step counter: a break is not defined"),
]
COL = {"closed": "#1f6f5c", "ctl": "#1f6f5c", "na": "#9aa5b1"}
TXT = {"closed": "closed (logical)", "ctl": "closed (controls 5/5)", "na": "out of scope"}
H = 660
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
    out.append(f'<rect x="340" y="{y + 2}" width="160" height="22" rx="4" fill="{COL[st]}"/>')
    out.append(f'<text x="420" y="{y + 17}" text-anchor="middle" class="badge">{TXT[st]}</text>')
    out.append(f'<text x="515" y="{y + 17}" class="small">{note}</text>')
# lower panel: best English score of K4, the shuffles and the planted controls on one axis
X0, W, Y0, EMAX, STEP = 360, 600, 260, 160.0, 30
out.append(f'<text x="30" y="{Y0 - 36}" class="small" font-weight="600">Hagelin type: best English score '
           f'after hill-climbing every crib-consistent setting (K4, shuffles) and the true plaintext of each planted control</text>')
bars = [("K4 on engine v5", k4v5["E_max"], f"{int(k4v5['leaves_b_weighted']):,} climbs", "#b03a2e")] + \
       [(f"shuffle {i + 1}", s["E_max"], f"{s['climbs']:,} climbs", "#9aa5b1") for i, s in enumerate(h["shuffles"])] + \
       [(f"control {c['seed']}", c["E_true"], "1 K4-size run", "#2f6db5") for c in ctl]
yend = Y0 + STEP * len(bars)
for t in range(0, 161, 40):
    x = X0 + W * t / EMAX
    out.append(f'<line x1="{x:.1f}" y1="{Y0 - 4}" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 16}" text-anchor="middle" class="small">{t}</text>')
xt = X0 + W * h["threshold_E"] / EMAX
for i, (name, e, n, col) in enumerate(bars):
    y = Y0 + STEP * i
    out.append(f'<text x="{X0 - 10}" y="{y + 17}" text-anchor="end" class="small">{name} ({n})</text>')
    out.append(f'<rect x="{X0}" y="{y + 4}" width="{W * e / EMAX:.1f}" height="20" fill="{col}"/>')
    xl = X0 + W * e / EMAX + 6
    if abs(xl - xt) < 16:          # keep the value label off the threshold line
        xl = xt + 8
    out.append(f'<text x="{xl:.1f}" y="{y + 19}" class="small">{e:.2f}</text>')
out.append(f'<line x1="{xt:.1f}" y1="{Y0 - 8}" x2="{xt:.1f}" y2="{yend}" stroke="#17202a" stroke-width="2" '
           f'stroke-dasharray="5,4"/>')
out.append(f'<text x="{xt + 4:.1f}" y="{Y0 - 12}" class="small">threshold {h["threshold_E"]}</text>')
notes = ["The shuffles had about 500 times fewer climbs than K4, and the best score grows with the number of climbs, so their bars",
         "are still not comparable with K4's. The five controls were planted under K4's own crib stage (2026-10-02), each searched with",
         f"one K4-size run: every true plaintext is the global maximum (E_true {min(c['E_true'] for c in ctl):.2f} to "
         f"{max(c['E_true'] for c in ctl):.2f}, all above {h['threshold_E']}), while K4's best, {k4v5['E_max']:.2f}, stays below",
         "the threshold. The Hagelin row is closed within the family; not rarer than random (no size-matched null)."]
for k, line in enumerate(notes):
    out.append(f'<text x="30" y="{yend + 42 + 18 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
