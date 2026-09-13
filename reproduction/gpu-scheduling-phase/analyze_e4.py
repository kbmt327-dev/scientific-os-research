"""Grade PRED-003 against results/E4.json.

The stability detector is the one written into the seal (PRED-003.detector):
unusable / class-starved (flow-balance spread > 0.30) / stable (min >= 0.995) /
otherwise decided by the 30k-vs-120k horizon test. E4 carries its own horizon
runs for p64=0.002 at rho=0.85; any other ambiguous cell is reported as
'unadjudicated' rather than silently treated as stable.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E4 = json.load(open(os.path.join(HERE, "results", "E4.json")))
CFG = E4["config"]
ROWS = E4["rows"]
POLICIES = CFG["policies"]
RHOS = CFG["rhos"]
BASE = [f"p64={p}" for p in CFG["p64"]]
MATCHED = [l for l, _, _ in CFG["mixes"] if l.startswith("matched")][0]
LABELS = BASE + [MATCHED]
N_JOBS, HORIZON2 = CFG["n_jobs"], CFG["horizon2"]
SPREAD_STARVE, LEVEL_OK = 0.30, 0.995
MARK = {"stable": ".", "class-starved": "S", "overloaded": "O", "unusable": "X",
        "unadjudicated": "!"}


def spread(r):
    fb = r["flow_balance_by_need"]
    return max(fb.values()) - min(fb.values()) if fb else float("nan")


def rows(label, rho, pol, n_jobs=None):
    n = N_JOBS if n_jobs is None else n_jobs
    return [r for r in ROWS if r["label"] == label and abs(r["rho"] - rho) < 1e-9
            and r["policy"] == pol and r["n_jobs"] == n]


def cell(label, rho, pol):
    rs = rows(label, rho, pol)
    if not rs:
        return None
    jct = np.array([r["mean_jct"] for r in rs])
    if any(r["aborted_backlog"] or r["hit_time_limit"] or r["completion_frac"] < 0.98
           for r in rs):
        v = "unusable"
    elif any(spread(r) > SPREAD_STARVE for r in rs):
        v = "class-starved"
    elif all(r["min_flow_balance"] >= LEVEL_OK for r in rs):
        v = "stable"
    else:
        long = rows(label, rho, pol, HORIZON2)
        if long:
            # seed-paired: compare the long run against the SAME seed at 30k,
            # otherwise seed-to-seed variation leaks into the growth ratio
            sd = long[0]["seed"]
            base = [r for r in rs if r["seed"] == sd]
            den = base[0]["mean_jct"] if base else jct.mean()
            if any(r["aborted_backlog"] or r["hit_time_limit"]
                   or r["completion_frac"] < 0.98 for r in long):
                v = "overloaded"     # the long run could not even drain
            else:
                g = np.mean([r["mean_jct"] for r in long]) / den
                v = ("overloaded" if g >= 2.0 else "stable" if g <= 1.3
                     else "unadjudicated")
        else:
            v = "unadjudicated"
    return {"verdict": v, "ok": v == "stable", "mark": MARK[v],
            "starving": sorted({int(k) for r in rs for k in r["starving_needs"]}),
            "jct": float(jct.mean()),
            "se": float(jct.std(ddof=1) / np.sqrt(len(jct))),
            "by_seed": {r["seed"]: r["mean_jct"] for r in rs},
            "worst_class_jct": float(np.mean([max(r["jct_by_need"].values()) for r in rs])),
            "jct64": float(np.mean([r["jct_by_need"].get("64", r["jct_by_need"].get(64, float("nan")))
                                    for r in rs])),
            "jct1": float(np.mean([r["jct_by_need"].get("1", r["jct_by_need"].get(1, float("nan")))
                                   for r in rs])),
            "fb64": float(np.mean([r["flow_balance_by_need"].get("64", float("nan"))
                                   for r in rs])),
            "min_fb": float(np.mean([r["min_flow_balance"] for r in rs]))}


def pair_ratio(a, b):
    if a is None or b is None or not a["ok"] or not b["ok"]:
        return float("nan")
    s = sorted(set(a["by_seed"]) & set(b["by_seed"]))
    return float(np.mean([a["by_seed"][x] / b["by_seed"][x] for x in s]))


print("mixes (E[k], max need, p(64)):")
for label, needs, probs in CFG["mixes"]:
    ek = float(np.dot(needs, probs))
    print(f"  {label:<44} E[k]={ek:.3f}  max_need={max(needs)}  "
          f"p(64)={probs[-1] if max(needs) == 64 else 0.0:.4f}")

print("\n=== PHASE  (. stable  S class-starved  O overloaded  X unusable) ===")
for rho in RHOS:
    print(f"\n rho={rho}")
    print(f"{'mix':<44} " + " ".join(f"{p:>14}" for p in POLICIES))
    for lb in LABELS:
        print(f"{lb:<44} " + " ".join(f"{cell(lb, rho, p)['mark']:>14}"
                                      for p in POLICIES))

for name, key in [("mean JCT (all jobs)", "jct"),
                  ("worst need-class mean JCT", "worst_class_jct"),
                  ("need=64 class mean JCT", "jct64"),
                  ("need=64 class flow balance", "fb64")]:
    print(f"\n=== {name} ===")
    for rho in RHOS:
        print(f"\n rho={rho}")
        print(f"{'mix':<44} " + " ".join(f"{p:>14}" for p in POLICIES))
        for lb in LABELS:
            print(f"{lb:<44} " + " ".join(
                f"{cell(lb, rho, p)[key]:>13.3f}{cell(lb, rho, p)['mark']}"
                for p in POLICIES))

print(f"\n=== horizon check at p64=0.002, rho=0.85 ({N_JOBS} -> {HORIZON2}) ===")
print(f"{'policy':<16}{'jct@30k':>10}{'jct@120k':>10}{'grow':>7}"
      f"{'jct64@30k':>11}{'jct64@120k':>12}{'grow64':>8}"
      f"{'jct1@30k':>10}{'grow1':>7}")
HZ = {}
for pol in POLICIES:
    a = cell("p64=0.002", 0.85, pol)
    lg = rows("p64=0.002", 0.85, pol, HORIZON2)
    if not lg:
        continue
    b_jct = np.mean([r["mean_jct"] for r in lg])
    b64 = np.mean([r["jct_by_need"].get("64", r["jct_by_need"].get(64, np.nan)) for r in lg])
    b1 = np.mean([r["jct_by_need"].get("1", r["jct_by_need"].get(1, np.nan)) for r in lg])
    # compare against the same seed (301) at 30k for a paired horizon ratio
    s0 = [r for r in rows("p64=0.002", 0.85, pol) if r["seed"] == lg[0]["seed"]][0]
    g64 = b64 / s0["jct_by_need"].get("64", s0["jct_by_need"].get(64, np.nan))
    g1 = b1 / s0["jct_by_need"].get("1", s0["jct_by_need"].get(1, np.nan))
    HZ[pol] = {"grow": b_jct / s0["mean_jct"], "grow64": g64, "grow1": g1}
    print(f"{pol:<16}{s0['mean_jct']:>10.2f}{b_jct:>10.2f}{HZ[pol]['grow']:>7.2f}"
          f"{s0['jct_by_need'].get('64', np.nan):>11.1f}{b64:>12.1f}{g64:>8.2f}"
          f"{s0['jct_by_need'].get('1', np.nan):>10.2f}{g1:>7.2f}")

# ------------------------------------------------------------------- grading
V = []


def rec(pid, claim, ok, detail):
    V.append({"id": pid, "claim": claim, "pass": bool(ok), "detail": detail})
    print(f"{pid}  {'PASS' if ok else 'FAIL':<4}  {claim}\n      {detail}")


print("\n\n=== PRED-003 grading ===")

pos = [f"p64={p}" for p in CFG["p64"] if p > 0]
r1 = [(lb, cell(lb, 0.85, "srpt")["verdict"], cell(lb, 0.85, "srpt")["starving"])
      for lb in pos]
rec("R1", "greedy SRPT starves need=64 at every p64>0 (rho=0.85)",
    all(v == "class-starved" and 64 in s for _, v, s in r1),
    "; ".join(f"{lb}:{v}/starving={s}" for lb, v, s in r1))

z, zsf = cell("p64=0.0", 0.85, "srpt"), cell("p64=0.0", 0.85, "sf_srpt")
z7 = cell("p64=0.0", 0.7, "srpt")
rec("R2", "at p64=0 greedy SRPT starves nothing and beats sf_srpt on mean JCT",
    z["ok"] and z7["ok"] and z["jct"] < zsf["jct"],
    f"srpt p64=0: rho=0.7 {z7['verdict']}, rho=0.85 {z['verdict']}; mean JCT "
    f"srpt {z['jct']:.3f} vs sf_srpt {zsf['jct']:.3f} "
    f"(paired ratio {pair_ratio(z, zsf):.3f})")

m = cell(MATCHED, 0.85, "srpt")
p03 = cell("p64=0.03", 0.85, "srpt")
rec("R3", "the E[k]-matched max-need-32 control does not starve under greedy SRPT",
    m["ok"],
    f"matched control (E[k]=4.076, max need 32): {m['verdict']}, min_fb="
    f"{m['min_fb']:.3f}, mean JCT {m['jct']:.3f}; same-E[k] p64=0.03 mix: "
    f"{p03['verdict']} (starving {p03['starving']}), mean JCT {p03['jct']:.3f}")

a, b = cell("p64=0.0", 0.85, "sf_srpt"), cell("p64=0.008", 0.85, "sf_srpt")
rec("R4", "sf_srpt's mean JCT changes by less than 25% from p64=0 to 0.008",
    a["ok"] and b["ok"] and abs(b["jct"] / a["jct"] - 1) < 0.25,
    f"{a['jct']:.3f} -> {b['jct']:.3f} ({b['jct'] / a['jct']:.3f}x), "
    f"verdicts {a['verdict']}/{b['verdict']}")

eb = [(lb, rho, cell(lb, rho, "easy_backfill")["verdict"])
      for lb in LABELS for rho in RHOS
      if not cell(lb, rho, "easy_backfill")["ok"]]
rec("R5", "EASY backfill starves nothing at any p64 or load", not eb,
    f"non-stable backfill cells: {eb if eb else 'none'}; worst min_fb="
    f"{min(cell(lb, rho, 'easy_backfill')['min_fb'] for lb in LABELS for rho in RHOS):.3f}")

want_starve = ["srpt", "srpt_np"]
want_clean = ["fcfs", "sf_srpt", "sf_fcfs"]
g = {p: cell("p64=0.008", 0.85, p) for p in POLICIES}
ok6 = (all(64 in g[p]["starving"] for p in want_starve)
       and all(64 not in g[p]["starving"] for p in want_clean))
rec("R6", "at p64=0.008 exactly the greedy+size-priority policies starve need=64",
    ok6, "; ".join(f"{p}:{g[p]['verdict']}/starving={g[p]['starving']}"
                   for p in POLICIES))

h = HZ.get("srpt")
rec("R7", "greedy SRPT's need=64 JCT grows >=2x over a 4x horizon while need=1 "
          "grows <=1.2x (p64=0.002, rho=0.85)",
    h is not None and h["grow64"] >= 2.0 and h["grow1"] <= 1.2,
    f"need=64 x{h['grow64']:.2f}, need=1 x{h['grow1']:.2f}, aggregate "
    f"x{h['grow']:.2f}" if h else "no horizon run")

band = []
for p in CFG["p64"]:
    if p > 0.008:
        continue
    lb = f"p64={p}"
    s, e = cell(lb, 0.85, "srpt"), cell(lb, 0.85, "easy_backfill")
    band.append((lb, s["jct"] / e["jct"]))
rec("R8", "greedy SRPT's aggregate mean JCT stays within 30% of backfill's for "
          "p64<=0.008 (the aggregate metric cannot see the starvation)",
    all(0.7 <= r <= 1.3 for _, r in band),
    "; ".join(f"{lb}:{r:.3f}" for lb, r in band))

wc = [cell(f"p64={p}", 0.85, "srpt")["worst_class_jct"] for p in CFG["p64"]]
wcb = [cell(f"p64={p}", 0.85, "easy_backfill")["worst_class_jct"] for p in CFG["p64"]]
mono = all(wc[i + 1] >= wc[i] for i in range(len(wc) - 1))
big = all(cell(f"p64={p}", 0.85, "srpt")["worst_class_jct"] > 100
          for p in CFG["p64"] if p >= 0.002)
rec("R9", "worst-class JCT under greedy SRPT rises monotonically with p64 and "
          "exceeds 100 for p64>=0.002, while backfill stays below 25",
    mono and big and all(v < 25 for v in wcb),
    f"srpt worst-class: {[round(v, 1) for v in wc]} (monotone={mono}); "
    f"backfill: {[round(v, 1) for v in wcb]}")

sffc = [(lb, cell(lb, rho, "sf_fcfs")["verdict"]) for lb in LABELS for rho in RHOS
        if not cell(lb, rho, "sf_fcfs")["ok"]]
worse = [(lb, cell(lb, 0.85, "sf_fcfs")["jct"], cell(lb, 0.85, "sf_srpt")["jct"])
         for lb in LABELS]
rec("R10", "sf_fcfs is stable everywhere but worse than sf_srpt on mean JCT at "
           "every p64 (filling and priority are separable axes)",
    not sffc and all(a > b for _, a, b in worse),
    f"non-stable sf_fcfs cells: {sffc if sffc else 'none'}; "
    + "; ".join(f"{lb}:{a:.2f} vs {b:.2f}" for lb, a, b in worse))

n = sum(v["pass"] for v in V)
print(f"\n{n}/{len(V)} sealed predictions passed")
json.dump({"n_pass": n, "n_total": len(V), "results": V},
          open(os.path.join(HERE, "results", "E4_grading.json"), "w"), indent=2)
