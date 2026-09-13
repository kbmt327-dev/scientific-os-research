"""Grade PRED-005 against results/E6.json: where between N/2 and N does
whole-pool starvation switch on?"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E6 = json.load(open(os.path.join(HERE, "results", "E6.json")))
CFG, ROWS = E6["config"], E6["rows"]
RATIOS, RHOS = CFG["ratios"], CFG["rhos"]
POLICIES = CFG["policies"]
N_JOBS, HORIZON2 = CFG["n_jobs"], CFG["horizon2"]
SAFE_FB, STARVE_FB = 0.9, 0.5


def sel(n_servers, ratio, rho, pol, n_jobs=None):
    n = N_JOBS if n_jobs is None else n_jobs
    return [r for r in ROWS if r["n_servers"] == n_servers
            and abs(r["ratio"] - ratio) < 0.002 and abs(r["rho"] - rho) < 1e-9
            and r["policy"] == pol and r["n_jobs"] == n]


def cell(n_servers, ratio, rho, pol):
    rs = sel(n_servers, ratio, rho, pol)
    if not rs:
        return None
    def m(key):
        v = [r[key] for r in rs if r[key] is not None and r[key] == r[key]]
        return float(np.mean(v)) if v else float("nan")
    fb = m("fb_m")
    return {"n": len(rs), "fb": fb, "jct_m": m("jct_m"), "jct_1": m("jct_1"),
            "mean_jct": m("mean_jct"), "m": rs[0]["m"],
            "n_arr_m": float(np.mean([r["n_arrivals_by_need"].get(str(r["m"]), 0)
                                      for r in rs])),
            "verdict": ("starved" if fb < STARVE_FB else
                        "safe" if fb >= SAFE_FB else "degraded")}


def fmt(c):
    if c is None:
        return f"{'-':>18}"
    mark = {"starved": "S", "degraded": "d", "safe": " "}[c["verdict"]]
    return f"{c['fb']:>7.3f}{mark} {c['jct_m']:>9.1f}"


print("m class: flow balance (S starved <0.5, d degraded <0.9) and its mean JCT")
for rho in RHOS:
    print(f"\n=== N=64, rho={rho} ===")
    print(f"{'m/N':>6}{'m':>5} " + " ".join(f"{p:>18}" for p in POLICIES)
          + f"{'jct_1(srpt)':>13}")
    for r in RATIOS:
        cs = [cell(64, r, rho, p) for p in POLICIES]
        s = cell(64, r, rho, "srpt")
        print(f"{r:>6}{cs[0]['m'] if cs[0] else 0:>5} "
              + " ".join(fmt(c) for c in cs)
              + f"{(s['jct_1'] if s else float('nan')):>13.2f}")

print("\n=== ServerFilling where applicable (powers of two only) ===")
print(f"{'m/N':>6} " + " ".join(f"{p:>18}" for p in CFG["sf_policies"]))
for r in (0.5, 1.0):
    print(f"{r:>6} " + " ".join(fmt(cell(64, r, 0.85, p))
                                for p in CFG["sf_policies"]))

print("\n=== scale check: greedy SRPT flow balance at matched m/N, rho=0.85 ===")
print(f"{'m/N':>6}{'N=64':>10}{'N=128':>10}{'diff':>9}")
scale = []
for r in RATIOS:
    a, b = cell(64, r, 0.85, "srpt"), cell(128, r, 0.85, "srpt")
    if a and b:
        scale.append((r, a["fb"], b["fb"], abs(a["fb"] - b["fb"])))
        print(f"{r:>6}{a['fb']:>10.3f}{b['fb']:>10.3f}{abs(a['fb']-b['fb']):>9.3f}")

safe = [r for r in RATIOS if (cell(64, r, 0.85, "srpt") or {}).get("fb", 0) >= SAFE_FB]
r_safe = max(safe) if safe else None
print(f"\nlargest m/N at which greedy SRPT keeps the class fed (fb >= {SAFE_FB}) "
      f"at rho=0.85: r_safe = {r_safe}")

# ---------------------------------------------------------------- grading
V = []


def rec(pid, claim, ok, detail):
    V.append({"id": pid, "claim": claim, "pass": bool(ok), "detail": detail})
    print(f"{pid:>3}  {'PASS' if ok else 'FAIL':<4}  {claim}\n      {detail}")


print("\n\n=== PRED-005 grading ===")

j = [(r, (cell(64, r, 0.85, "srpt") or {}).get("jct_m", float("nan")))
     for r in RATIOS]
mono = all(j[i + 1][1] >= j[i][1] * 0.95 for i in range(len(j) - 1))
jumps = [(j[i][0], j[i + 1][0], j[i + 1][1] / j[i][1])
         for i in range(len(j) - 1) if j[i][1] > 0 and j[i + 1][1] / j[i][1] > 10]
early = [x for x in jumps if x[1] < 1.0]
rec("T1", "degradation is continuous in m; no >10x jump before m=N",
    mono and not early,
    "jct by m/N: " + " ".join(f"{r}:{v:.1f}" for r, v in j)
    + f"; monotone={mono}; >10x jumps at {jumps if jumps else 'none'}")

c32 = [cell(64, 0.5, rho, "srpt") for rho in RHOS]
rec("T2", "m = N/2 does not starve (reproduces EP-0003)",
    all(c and c["fb"] >= SAFE_FB for c in c32),
    "; ".join(f"rho={rho}: fb={c['fb']:.3f} jct={c['jct_m']:.2f}"
              for rho, c in zip(RHOS, c32)))

c64 = [cell(64, 1.0, rho, "srpt") for rho in RHOS]
rec("T3", "m = N starves (reproduces EP-0003)",
    all(c and c["fb"] < STARVE_FB for c in c64),
    "; ".join(f"rho={rho}: fb={c['fb']:.3f} jct={c['jct_m']:.1f}"
              for rho, c in zip(RHOS, c64)))

c38 = cell(64, 0.594, 0.85, "srpt")
rec("T4", "DECIDING: at m/N = 0.594 (Philly VC 11cb48's real ratio) greedy SRPT "
          "does NOT starve the class",
    c38 is not None and c38["fb"] >= STARVE_FB,
    f"fb={c38['fb']:.3f} ({c38['verdict']}), class JCT {c38['jct_m']:.2f}, "
    f"need=1 JCT {c38['jct_1']:.2f}, arrivals {c38['n_arr_m']:.0f}")

ratio38 = c38["jct_m"] / c38["jct_1"] if c38 else float("nan")
rec("T5", "the m/N=0.594 class is still measurably harmed: JCT >= 5x the "
          "need=1 class", ratio38 >= 5,
    f"{c38['jct_m']:.2f} / {c38['jct_1']:.2f} = {ratio38:.1f}x")

worst = max((d for _, _, _, d in scale), default=float("nan"))
rec("T6", "the onset is a ratio, not an absolute size (N=64 vs N=128 within 0.15)",
    scale and worst <= 0.15,
    f"largest |difference| across matched ratios = {worst:.3f}"
    if scale else "no matched cells")

bad7 = [(r, rho, cell(64, r, rho, "easy_backfill")["fb"])
        for r in RATIOS for rho in RHOS
        if cell(64, r, rho, "easy_backfill")["fb"] < SAFE_FB]
rec("T7", "EASY backfill never starves the m class at any m", not bad7,
    f"cells below {SAFE_FB}: {bad7 if bad7 else 'none'}; worst fb = "
    f"{min(cell(64, r, rho, 'easy_backfill')['fb'] for r in RATIOS for rho in RHOS):.3f}")

bad8 = [(r, cell(64, r, 0.85, "srpt_np")["fb"], cell(64, r, 0.85, "srpt")["fb"])
        for r in RATIOS
        if cell(64, r, 0.85, "srpt_np")["fb"] > cell(64, r, 0.85, "srpt")["fb"] + 0.05]
rec("T8", "srpt_np is at least as bad as srpt at every m", not bad8,
    f"m/N where srpt_np is better: {bad8 if bad8 else 'none'}")

lo = sel(64, 1.0, 0.85, "srpt")
hi = sel(64, 1.0, 0.85, "srpt", HORIZON2)
if lo and hi:
    base = [r for r in lo if r["seed"] == hi[0]["seed"]][0]
    g_m = hi[0]["jct_m"] / base["jct_m"] if base["jct_m"] else float("nan")
    g_1 = hi[0]["jct_1"] / base["jct_1"]
    rec("T9", "at m=N the starved class's delay is unbounded (>=2x over a 4x "
              "horizon) while need=1 grows <=1.2x",
        g_m >= 2.0 and g_1 <= 1.2,
        f"class JCT {base['jct_m']:.0f} -> {hi[0]['jct_m']:.0f} (x{g_m:.2f}), "
        f"need=1 x{g_1:.2f}")
else:
    rec("T9", "horizon growth at m=N", False, "no horizon run found")

rec("T10", "a usable boundary exists: 0.5 < r_safe < 1.0",
    r_safe is not None and 0.5 < r_safe < 1.0,
    f"r_safe = {r_safe}; verdicts: " + " ".join(
        f"{r}:{(cell(64,r,0.85,'srpt') or {}).get('verdict','?')}" for r in RATIOS))

n = sum(v["pass"] for v in V)
print(f"\n{n}/{len(V)} sealed predictions passed")
t4 = next(v for v in V if v["id"] == "T4")
print("\npre-committed consequence: " + (
    "T4 PASSED -- the EP-0003 mechanism does not reach any measured production "
    "pool; demote the practical implications to a conditional on pool sizing."
    if t4["pass"] else
    "T4 FAILED -- the mechanism reaches Philly's 11cb48 VC; the practical claim "
    "survives, narrowed to pools whose largest job exceeds r_safe of capacity."))
json.dump({"n_pass": n, "n_total": len(V), "r_safe": r_safe,
           "t4_passed": t4["pass"], "results": V},
          open(os.path.join(HERE, "results", "E6_grading.json"), "w"), indent=2)
