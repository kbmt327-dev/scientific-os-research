"""A11: post-reveal scoring of FINAL-MODEL against the disclosed truth."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "world"))
from world import derive_world, server_multipliers  # noqa: E402

seal = json.loads(Path("seal/world_seal.json").read_text(encoding="utf-8"))
truth = derive_world(seal["master_seed"])
final = json.loads(Path("predictions/FINAL-MODEL.json").read_text(encoding="utf-8"))

print("=== structural claims ===")
rows = [
    ("arrival family", "batch (compound Poisson)", truth["arrival"]["kind"]),
    ("service law", "exponential", truth["service"]["kind"]),
    ("server structure", "heterogeneous", truth["servers"]["kind"]),
    ("customer behaviour", "patient (no abandon/balk)", truth["customers"]["kind"]),
    ("number of deviations from M/M/c", "2", str(truth["_meta"]["n_deviations"])),
]
for name, claimed, actual in rows:
    ok = claimed.split(" ")[0] == actual or actual in claimed
    print(f"  {name:32s} claimed={claimed:26s} truth={actual:16s} {'MATCH' if ok else 'MISS'}")

print("\n=== batch size ===")
tb = truth["arrival"]["params"]["mean_batch"]
print(f"  E[B] estimated 1.9810   truth {tb:.4f}   error {100*(1.9810-tb)/tb:+.2f}%")

print("\n=== server rates ===")
mult = server_multipliers(seal["master_seed"], truth, 6)
est = final["deviation_2_heterogeneous_servers"]["pool"]
print(f"  {'server':>6s} {'estimated':>10s} {'truth':>10s} {'error %':>9s}")
errs = []
for i in range(6):
    e = est[str(i)]
    errs.append(100 * (e - mult[i]) / mult[i])
    print(f"  {i:6d} {e:10.4f} {mult[i]:10.4f} {errs[-1]:+9.2f}")
print(f"  max |error| = {max(abs(x) for x in errs):.2f}%")
print(f"  note: servers 1 and 2 were TIED at 0.3625; truth is "
      f"{mult[1]:.4f} and {mult[2]:.4f} (they differ by {100*abs(mult[1]-mult[2])/mult[1]:.1f}%, "
      f"which 2000 observations each cannot resolve)")

print("\n=== capacity ===")
for c in (3, 4, 6):
    print(f"  c={c}: predicted {sum(est[str(i)] for i in range(c)):.4f}   "
          f"truth {mult[:c].sum():.4f}   error {100*(sum(est[str(i)] for i in range(c))-mult[:c].sum())/mult[:c].sum():+.2f}%")

print("\n=== the rate-spread parameter I declared UNKNOWN ===")
lv = np.log(mult[:6])
print(f"  truth log_sd = {truth['servers']['params']['log_sd']:.4f}")
print(f"  sd of log of my six estimated rates = {np.std(np.log([est[str(i)] for i in range(6)]), ddof=1):.4f}")
print("  declaring it unidentified from 4-6 servers was right in kind: the 6-server sample sd")
print(f"  of log truth is {lv.std(ddof=1):.4f}, itself far from {truth['servers']['params']['log_sd']:.4f}")
