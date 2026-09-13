"""Grade PRED-006 against results/E7.json: does r_safe fall with pool size?"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E7 = json.load(open(os.path.join(HERE, "results", "E7.json")))
CFG, ROWS = E7["config"], E7["rows"]
NS, RATIOS = CFG["ns"], CFG["ratios"]
SAFE_FB = 0.9
PHILLY_RATIO = 0.59          # Philly VC 11cb48: 128-GPU job in a 217-GPU pool


def cell(n, r, pol="srpt"):
    rs = [x for x in ROWS if x["n_servers"] == n and abs(x["ratio"] - r) < 0.004
          and x["policy"] == pol]
    if not rs:
        return None
    def m(key):
        v = [x[key] for x in rs if x[key] is not None and x[key] == x[key]]
        return float(np.mean(v)) if v else float("nan")
    return {"n_seeds": len(rs), "fb": m("fb_m"), "jct_m": m("jct_m"),
            "jct_1": m("jct_1"), "mean_jct": m("mean_jct"), "m": rs[0]["m"],
            "n_classes": rs[0]["n_classes"],
            "bad": any(x["aborted_backlog"] or x["hit_time_limit"]
                       or x["completion_frac"] < 0.98 for x in rs)}


def r_safe(n, pol="srpt"):
    ok = [r for r in RATIOS if (cell(n, r, pol) or {}).get("fb", 0) >= SAFE_FB]
    return max(ok) if ok else None


print("greedy SRPT: flow balance of the large class (>= 0.9 is 'fed')")
print(f"{'m/N':>8} " + " ".join(f"{'N=' + str(n):>9}" for n in NS))
for r in RATIOS:
    print(f"{r:>8} " + " ".join(
        (f"{cell(n, r)['fb']:>9.3f}" if cell(n, r) else f"{'-':>9}") for n in NS))

print("\ngreedy SRPT: mean JCT of the large class")
print(f"{'m/N':>8} " + " ".join(f"{'N=' + str(n):>9}" for n in NS))
for r in RATIOS:
    print(f"{r:>8} " + " ".join(
        (f"{cell(n, r)['jct_m']:>9.1f}" if cell(n, r) else f"{'-':>9}") for n in NS))

print("\nEASY backfill: flow balance of the large class")
print(f"{'m/N':>8} " + " ".join(f"{'N=' + str(n):>9}" for n in NS))
for r in RATIOS:
    print(f"{r:>8} " + " ".join(
        (f"{cell(n, r, 'easy_backfill')['fb']:>9.3f}"
         if cell(n, r, 'easy_backfill') else f"{'-':>9}") for n in NS))

RS = {n: r_safe(n) for n in NS}
print("\nr_safe (largest ratio keeping flow balance >= 0.9), greedy SRPT:")
for n in NS:
    c = cell(n, PHILLY_RATIO if PHILLY_RATIO in RATIOS else 0.625)
    print(f"  N={n:>4}  r_safe={RS[n]}   classes={cell(n, 0.5)['n_classes']}"
          f"   m at r_safe = {int(round(n * RS[n])) if RS[n] else '-'}")

# ------------------------------------------------------------------ grading
V = []


def rec(pid, claim, ok, detail):
    V.append({"id": pid, "claim": claim, "pass": bool(ok), "detail": detail})
    print(f"{pid:>3}  {'PASS' if ok else 'FAIL':<4}  {claim}\n      {detail}")


print("\n\n=== PRED-006 grading ===")

seq = [RS[n] for n in NS]
mono = all(seq[i] is not None and seq[i + 1] is not None
           and seq[i] >= seq[i + 1] for i in range(len(seq) - 1))
rec("U1", "r_safe falls monotonically with pool size", mono,
    "  ".join(f"N={n}:{RS[n]}" for n in NS))

rec("U2", "r_safe(512) <= 0.6875 (at least one grid step below the N=64 value)",
    RS[512] is not None and RS[512] <= 0.6875,
    f"r_safe(512) = {RS[512]}, r_safe(64) = {RS[64]}")

c = cell(256, 0.625)
rec("U3", "DECIDING: at N=256 and m/N=0.625 (just above Philly's real 0.59) "
          "greedy SRPT keeps the class fed",
    c is not None and c["fb"] >= SAFE_FB,
    f"flow balance = {c['fb']:.3f}, class JCT {c['jct_m']:.1f} vs need=1 "
    f"{c['jct_1']:.2f} ({c['jct_m'] / c['jct_1']:.1f}x)" if c else "no cell")

fb_full = [(n, (cell(n, 1.0) or {}).get("fb", float("nan"))) for n in [64, 128, 256]]
rec("U4", "at m = N the whole-pool class gets worse with pool size",
    all(fb_full[i][1] >= fb_full[i + 1][1] for i in range(len(fb_full) - 1)),
    "  ".join(f"N={n}:{v:.3f}" for n, v in fb_full))

eb = [(n, r, cell(n, r, "easy_backfill")["fb"]) for n in NS for r in RATIOS
      if cell(n, r, "easy_backfill") and cell(n, r, "easy_backfill")["fb"] < 0.99]
rec("U5", "EASY backfill stays >= 0.99 at every N and ratio", not eb,
    f"cells below 0.99: {[(n, r, round(v, 3)) for n, r, v in eb] if eb else 'none'}")

a, b = cell(64, 0.75), cell(256, 0.75)
rec("U6", "at a fixed ratio the large class's mean JCT grows with N",
    a and b and b["jct_m"] > a["jct_m"],
    f"N=64: {a['jct_m']:.1f}  ->  N=256: {b['jct_m']:.1f}")

ratio_effect = max((cell(n, 0.5)["fb"] - cell(n, 1.0)["fb"]) for n in NS
                   if cell(n, 0.5) and cell(n, 1.0))
size_effect = max((cell(32, r)["fb"] - cell(512, r)["fb"]) for r in RATIOS
                  if cell(32, r) and cell(512, r))
rec("U7", "the ratio still dominates the pool size", ratio_effect > size_effect,
    f"largest ratio effect {ratio_effect:.3f} vs largest size effect "
    f"{size_effect:.3f}")

rec("U8", "small pools are more forgiving: r_safe(32) > 0.75",
    RS[32] is not None and RS[32] > 0.75, f"r_safe(32) = {RS[32]}")

n_pass = sum(v["pass"] for v in V)
print(f"\n{n_pass}/{len(V)} sealed predictions passed")
u3 = next(v for v in V if v["id"] == "U3")
print("\npre-committed consequence: " + (
    "U3 PASSED -- EP-0004's demotion stands. Replace the single r_safe=0.75 "
    "with a pool-size-dependent band."
    if u3["pass"] else
    "U3 FAILED -- EP-0004's demotion was too generous. Philly's 11cb48 VC is "
    "inside the harmful region at its real scale; reinstate the practical claim "
    "for pools of a few hundred GPUs."))
json.dump({"n_pass": n_pass, "n_total": len(V), "r_safe": RS,
           "u3_passed": u3["pass"], "results": V},
          open(os.path.join(HERE, "results", "E7_grading.json"), "w"), indent=2)
