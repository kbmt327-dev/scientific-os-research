"""Grade PRED-007 against results/E8.json (arms B and C) plus results/E7.json
(arm A, the baseline reused)."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E8 = json.load(open(os.path.join(HERE, "results", "E8.json")))
E7 = json.load(open(os.path.join(HERE, "results", "E7.json")))
CFG = E8["config"]
NS, RATIOS = CFG["ns"], CFG["ratios"]
SAFE_FB = 0.9
ROWS = {"B": [r for r in E8["rows"] if r["arm"] == "B"],
        "C": [r for r in E8["rows"] if r["arm"] == "C"],
        "A": [r for r in E7["rows"] if r["policy"] == "srpt"]}


def cell(arm, n, r):
    rs = [x for x in ROWS[arm] if x["n_servers"] == n
          and abs(x["ratio"] - r) < 0.004]
    if not rs:
        return None
    def m(k):
        v = [x[k] for x in rs if x.get(k) is not None and x.get(k) == x.get(k)]
        return float(np.mean(v)) if v else float("nan")
    return {"fb": m("fb_m"), "jct_m": m("jct_m"), "run": m("mean_running"),
            "m": rs[0]["m"], "n_seeds": len(rs)}


def r_safe(arm, n):
    ok = [r for r in RATIOS if (cell(arm, n, r) or {}).get("fb", 0) >= SAFE_FB]
    return max(ok) if ok else None


def step_gap(a, b):
    """distance between two ratios measured in grid steps."""
    if a is None or b is None:
        return None
    return abs(RATIOS.index(a) - RATIOS.index(b))


ARMS = [("A", "背景 1..N/2 の全2べき（E7 baseline）"),
        ("B", "背景 {1,2,4,8} 固定"),
        ("C", "背景 {N/64,N/32,N/16,N/8}（相対固定）")]

for arm, label in ARMS:
    print(f"\n=== arm {arm}: {label} ===")
    print(f"{'m/N':>8} " + " ".join(f"{'N=' + str(n):>9}" for n in NS))
    for r in RATIOS:
        print(f"{r:>8} " + " ".join(
            (f"{cell(arm, n, r)['fb']:>9.3f}" if cell(arm, n, r) else f"{'-':>9}")
            for n in NS))

print("\n=== r_safe by arm ===")
print(f"{'arm':>5} " + " ".join(f"{'N=' + str(n):>9}" for n in NS))
RS = {}
for arm, _ in ARMS:
    RS[arm] = {n: r_safe(arm, n) for n in NS}
    print(f"{arm:>5} " + " ".join(f"{str(RS[arm][n]):>9}" for n in NS))

print("\n=== mean concurrently running jobs (at m/N = 0.75) ===")
print(f"{'arm':>5} " + " ".join(f"{'N=' + str(n):>9}" for n in NS))
for arm, _ in ARMS:
    print(f"{arm:>5} " + " ".join(
        (f"{cell(arm, n, 0.75)['run']:>9.1f}"
         if cell(arm, n, 0.75) and cell(arm, n, 0.75)["run"] == cell(arm, n, 0.75)["run"]
         else f"{'-':>9}") for n in NS))

# ------------------------------------------------------------------ grading
V = []


def rec(pid, claim, ok, detail):
    V.append({"id": pid, "claim": claim, "pass": bool(ok), "detail": detail})
    print(f"{pid:>3}  {'PASS' if ok else 'FAIL':<4}  {claim}\n      {detail}")


print("\n\n=== PRED-007 grading ===")

rec("V1", "class count is not the driver: arm B's r_safe still falls with N",
    RS["B"][512] is not None and RS["B"][64] is not None
    and RS["B"][512] < RS["B"][64],
    "arm B r_safe: " + "  ".join(f"N={n}:{RS['B'][n]}" for n in NS))

vals = [RS["C"][n] for n in NS]
spread = (step_gap(max(v for v in vals if v is not None),
                   min(v for v in vals if v is not None))
          if all(v is not None for v in vals) else None)
rec("V2", "DECIDING: arm C (concurrency held ~constant) has a roughly FLAT "
          "r_safe across N", spread is not None and spread <= 1,
    "arm C r_safe: " + "  ".join(f"N={n}:{RS['C'][n]}" for n in NS)
    + f"; spread = {spread} grid step(s)")

cB = [cell("B", n, 0.75) for n in NS]
cC = [cell("C", n, 0.75) for n in NS]
rB = [c["run"] for c in cB if c]
rC = [c["run"] for c in cC if c]
growB = max(rB) / min(rB) if rB else float("nan")
growC = max(rC) / min(rC) if rC else float("nan")
rec("V3", "arm C really does hold concurrency fixed (<2x) while arm B lets it "
          "grow (>4x)", growC < 2.0 and growB > 4.0,
    f"mean_running spread: arm C {growC:.2f}x ({min(rC):.1f}-{max(rC):.1f}), "
    f"arm B {growB:.2f}x ({min(rB):.1f}-{max(rB):.1f})")

pairs, bad4 = [], []
for arm, _ in ARMS:
    for n in NS:
        c = cell(arm, n, 0.75)
        if c and RS[arm][n] is not None and c["run"] == c["run"]:
            pairs.append((arm, n, c["run"], RS[arm][n]))
for i in range(len(pairs)):
    for j in range(i + 1, len(pairs)):
        a, b = pairs[i], pairs[j]
        if max(a[2], b[2]) / min(a[2], b[2]) <= 1.2:
            g = step_gap(a[3], b[3])
            if g is not None and g > 1:
                bad4.append((a[0], a[1], round(a[2]), a[3],
                             b[0], b[1], round(b[2]), b[3], g))
rec("V4", "at matched concurrency (within 20%), r_safe agrees within one grid step",
    not bad4,
    f"{len(pairs)} cells compared; disagreements: {bad4 if bad4 else 'none'}")

rec("V5", "arms B and C agree at N=64 (same workload by construction)",
    RS["B"][64] == RS["C"][64],
    f"B:{RS['B'][64]}  C:{RS['C'][64]}")

rec("V6", "arm B is the harshest at N=512: r_safe_B(512) <= 0.5",
    RS["B"][512] is not None and RS["B"][512] <= 0.5,
    f"arm B {RS['B'][512]} vs baseline arm A {RS['A'][512]}")

n_pass = sum(v["pass"] for v in V)
print(f"\n{n_pass}/{len(V)} sealed predictions passed")
v2 = next(v for v in V if v["id"] == "V2")
print("\npre-committed consequence: " + (
    "V2 PASSED -- r_safe is set by how many background jobs compete for the "
    "pool, not by the pool's size in servers. Relabel the v5 table accordingly."
    if v2["pass"] else
    "V2 FAILED -- pool size matters in its own right beyond concurrency. v5 "
    "stands as written."))
json.dump({"n_pass": n_pass, "n_total": len(V), "r_safe": RS,
           "v2_passed": v2["pass"], "results": V},
          open(os.path.join(HERE, "results", "E8_grading.json"), "w"),
          indent=2, default=str)
