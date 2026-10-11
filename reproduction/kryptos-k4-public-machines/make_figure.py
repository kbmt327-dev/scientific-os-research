"""Draw the Note's figure: for every family x column, K4's minimum (h, or d* where a part is free) against the range of
the null minima and the registered pass region (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-public-machines.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "public-machines-20261010.json").read_text(encoding="utf-8"))


def expand(d):
    return [int(k) for k, v in d.items() for _ in range(v)]


def col(lst, name, key="column"):
    return next(c for c in lst if c[key] == name)


e193, e203, e206, e207, e209, e215 = (rec[k] for k in ("EP-0193_T2", "EP-0203", "EP-0206", "EP-0207", "EP-0209",
                                                         "EP-0215"))
d209 = e209["diagnostic_d_star"]
n207 = e207["null"]["columns"]
groups = [
    ("Enigma + free substitution σ, no plugboard, Π = id   (d*, pass d* = 0)", [
        ("Enigma I, entry QWi (EP-0193 T2; d* from EP-0209)", e193["min_d_star_from_EP0209"]["K4"],
         e193["min_d_star_from_EP0209"]["null_min"], 0, "N 1.1e11 · E 7.9e-7 · P 1.00", None),
        ("Enigma I, entry QW (EP-0209)", col(d209, "EP-0193 T2 x QW")["K4"], expand(col(d209, "EP-0193 T2 x QW")["null_min"]),
         0, "N 5.6e10 · E 3.95e-7 · P 1.00", None),
        ("Commercial D/K, Swiss-K, Railway, entry QW (EP-0209)", col(d209, "EP-0132 x QW")["K4"],
         expand(col(d209, "EP-0132 x QW")["null_min"]), 0, "N 5.6e9 · E 3.95e-8 · P 0.76", None),
        ("Commercial, entry QWi (EP-0132 as first run)", col(d209, "EP-0132 x QWi")["K4"],
         expand(col(d209, "EP-0132 x QWi")["null_min"]), 0, "P 1.00", None),
    ]),
    ("Same + crib 2 read d = ±1, ±2 machine steps away (EP-0215, d*)", [
        ("Enigma I, 3 entry readings x 4 d (pass d* <= 1)", min(e215["K4_min"]["EnigmaI_columns"]),
         e215["null"]["EnigmaI"]["column_min"], 1, "N 6.7e11 · E 0.0025 · P 0.31-1.00", None),
        ("Commercial, 3 x 4 (pass d* <= 2 at ±1, <= 1 at ±2)", e215["null"]["commercial"]["K4_family_min"],
         e215["null"]["commercial"]["family_min"], 2, "N 6.7e10 · E 0.031 · P 1.00", None),
    ]),
    ("Reflector-less rotors from 14 public wirings (EP-0203, h, pass h <= 2)", [
        ("3 rotors, 9 entry/exit alphabet pairs", col(e203["columns"], "forward 3-rotor main9")["K4_min_h"],
         col(e203["columns"], "forward 3-rotor main9")["null_min"], 2, "N 4.9e11 · E 9.3e-18 · P 0.9", None),
        ("3 rotors, reverse direction", col(e203["columns"], "reverse 3-rotor main9")["K4_min_h"],
         col(e203["columns"], "reverse 3-rotor main9")["null_min"], 2, "P 0.8", None),
        ("2 rotors, 9 pairs", col(e203["columns"], "forward 2-rotor main9")["K4_min_h"],
         col(e203["columns"], "forward 2-rotor main9")["null_min"], 2, "N 2.9e8 · E 5.5e-21 · P 0.2", None),
    ]),
    ("Reflector Enigma, no σ, x layout transposition Π (EP-0206, h, pass h <= 2)", [
        ("all 208 (Π, order), 33 machines, 3 entry readings", col(e206["null_full"]["columns"], "all 208")["K4_min_h"],
         col(e206["null_full"]["columns"], "all 208")["null_min"], 2, "N 3.8e13 · E 7.3e-16 · P 1.00", None),
        ("T1: the 48 (Π, order) of the 3 x 31 shape", col(e206["null_t1id"]["columns"], "T1 A+B")["K4_min_h"],
         col(e206["null_t1id"]["columns"], "T1 A+B")["null_min"], 2, "P 1.00 (20 shuffles)", None),
        ("commercial machines, entry QW", col(e206["null_full"]["columns"], "commercial x QW")["K4_min_h"],
         col(e206["null_full"]["columns"], "commercial x QW")["null_min"], 2, "P 0.60", None),
        ("Π = id reference (R4: S->S at 32, K->K at 73)", col(e206["null_t1id"]["columns"], "Pi = id reference")["K4_min_h"],
         col(e206["null_t1id"]["columns"], "Pi = id reference")["null_min"], 2, "P 1.00", None),
    ]),
    ("M-94, 25 public disks, any order, x layout transposition Π (EP-0207, d*, pass d* = 0)", [
        ("order A, line phase s = 0 (99 Π)", col(n207, "order A main")["K4_min_e"], col(n207, "order A main")["null_min"],
         0, "P 0.0 (shuffles), 0.12 (random)", None),
        ("order B, s = 0 (99 Π)", col(n207, "order B main")["K4_min_e"], col(n207, "order B main")["null_min"], 0,
         "main 102 bit · E0 5.3e-4 · P 0.2", None),
        ("sensitivity: order A, s free", col(n207, "sensitivity (order A, s free)")["K4_min_e"],
         col(n207, "sensitivity (order A, s free)")["null_min"], 0, "E0 7.5e-3", "unconfirmed hit, p = 0.415"),
    ]),
]

X0, X1, VMAX = 455, 845, 16
U = (X1 - X0) / VMAX


def x(v):
    return X0 + U * v


rows = sum(len(r) for _, r in groups)
H = 96 + 26 * len(groups) + 25 * rows + 112
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{H}" viewBox="0 0 1080 {H}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:12.5px}.tiny{font-size:11.5px}'
       '.title{font-size:17px;font-weight:600}.head{font-size:13px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}'
       '</style>',
       '<text x="540" y="28" text-anchor="middle" class="title">Machines built only from published wirings and disks: '
       "K4's best setting vs shuffled K4</text>",
       '<text x="540" y="50" text-anchor="middle" class="small">dot = K4\'s minimum over the family; grey bar = range of '
       'the null minima; shaded = registered pass region</text>']
top = 78
bottom = H - 104
for v in range(0, VMAX + 1, 2):
    out.append(f'<line x1="{x(v):.1f}" y1="{top - 6}" x2="{x(v):.1f}" y2="{bottom}" class="grid"/>')
    out.append(f'<text x="{x(v):.1f}" y="{bottom + 16}" text-anchor="middle" class="small">{v}</text>')
    out.append(f'<text x="{x(v):.1f}" y="{top - 10}" text-anchor="middle" class="tiny">{v}</text>')
y = top + 4
for head, rs in groups:
    out.append(f'<text x="18" y="{y + 14}" class="head">{head.replace("<=", "&#8804;")}</text>')
    y += 26
    for label, k4, nulls, thr, right, note in rs:
        cy = y + 9
        out.append(f'<rect x="{x(-0.45):.1f}" y="{cy - 10}" width="{(thr + 0.9) * U:.1f}" height="20" fill="#f5cba7" '
                   f'opacity="0.7"/>')
        lo, hi = min(nulls), max(nulls)
        out.append(f'<rect x="{x(lo - 0.18):.1f}" y="{cy - 4}" width="{(hi - lo + 0.36) * U:.1f}" height="8" rx="3" '
                   f'fill="#aab7b8"/>')
        colr = "#c0392b" if note else "#1b4f72"
        out.append(f'<circle cx="{x(k4):.1f}" cy="{cy}" r="5.5" fill="{colr}"/>')
        out.append(f'<text x="30" y="{cy + 4}" class="small">{label.replace("<=", "&#8804;")}</text>')
        out.append(f'<text x="{X1 + 14}" y="{cy + 4}" class="tiny">{right}</text>')
        if note:
            out.append(f'<text x="{x(k4) + 64:.1f}" y="{cy + 4}" class="small" style="fill:#c0392b">{note}</text>')
        y += 25
    y += 0
out.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{bottom + 34}" text-anchor="middle" class="small">crib positions that '
           f'must be given up: h (no free part) or d* (free σ or free disk order)</text>')
notes = ["No registered pass in any column except the M-94 sensitivity column: 1 setting remained, the confirmation",
         "statistic did not confirm it (p = 0.415), and it is recorded as unconfirmed, not as closed. Everywhere else:",
         "logical refutation; K4's minimum lies inside the null range, so K4 is not shown to be rarer than random."]
for k, line in enumerate(notes):
    out.append(f'<text x="30" y="{bottom + 60 + 18 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8", newline="\n")
