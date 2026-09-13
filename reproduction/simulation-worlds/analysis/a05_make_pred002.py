"""A05: build PRED-002 - prospective predictions for two NOT-YET-OBSERVED experiments.

Run BEFORE requesting OBS-003 / OBS-004.  Writes predictions/PRED-002.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fitted_model import predictive

RATES = [0.6930, 0.3625, 0.3625, 1.0275]   # tied mu1=mu2, from A04
MEAN_BATCH = 1.9810                        # from A02/A03
CAP4 = sum(RATES)
CAP3 = sum(RATES[:3])

E2 = dict(lam=1.6, c=4, horizon=6000, warmup=300)
E3 = dict(lam=1.2, c=3, horizon=6000, warmup=300)

out = {
    "prediction_id": "PRED-002",
    "registered_at": "2026-09-13",
    "status": "sealed-before-observation",
    "world_commitment_sha256": "7c4e47709de366e295aec26be7fac462100d1c6bf3d49fcd9ec03e40930b663a",
    "information_cutoff": "OBS-001 (level 1) and OBS-002 (level 3), both from run-seed 1 at lambda=2.8, c=4",
    "candidate_model_M3": {
        "arrivals": "homogeneous Poisson epochs at rate lambda/E[B]; batch size Geometric{1,2,..} with E[B]=1.9810",
        "service": "exponential, server-specific rate",
        "server_pool": RATES,
        "discipline": "FCFS, infinite queue, no abandonment, no balking, no vacation",
        "free_parameters": "E[B], mu_A=0.6930, mu_B=0.3625 (shared by servers 1 and 2), mu_C=1.0275  -> 4",
        "capacity_c4": CAP4, "capacity_c3": CAP3,
        "assignment_policy": "UNIDENTIFIED by OBS-001/002 (saturated); predicted separately below",
    },
    "baseline_for_comparison_M_M_c": {
        "note": "M/M/4 with the nominal mu=1 predicts a stable queue with W=1.33 at lambda=2.76; "
                "it was wrong by a factor of 234 on OBS-001 and predicts the wrong stability regime here too",
    },
    "experiments_requested": [],
    "structural_predictions": [
        {"id": "Q1", "claim": "OBS-003 (lambda=1.6, c=4) is STABLE: no systematic growth of sojourn "
                              "time across time deciles, and throughput equals the arrival rate to within 1%.",
         "because": "lambda=1.6 < fitted capacity 2.4455"},
        {"id": "Q2", "claim": "OBS-004 (lambda=1.2, c=3) is STABLE with utilisation near 0.85.",
         "because": "server identity is assumed to persist when c changes, so capacity(c=3) = 1.4180; "
                    "this is an assumption from the world FAMILY (which I authored), not a blind inference, "
                    "and it is exactly what this experiment tests"},
        {"id": "Q3", "claim": "In OBS-004 the three per-server rates recomputed from completions/busy-time "
                              "will match servers 0,1,2 of OBS-002 to within their 95% CIs "
                              "(0.6930, 0.3625, 0.3625).",
         "falsifies_if_wrong": "server identity does not persist across configurations; the 'server pool' "
                               "abstraction would have to be replaced by a per-configuration draw"},
        {"id": "Q4", "claim": "Exit reasons in both runs are only 'served' / 'in_system'; no abandonment, no balking."},
        {"id": "Q5", "claim": "In both runs, batch sizes stay Geometric with mean in [1.90, 2.06], and epoch "
                              "inter-arrival times stay exponential (KS p > 0.01)."},
        {"id": "Q6", "claim": "The dispersion-index excess seen at bin width 80-160 in OBS-002 "
                              "(ID=1.61, z=+3.6) does NOT replicate in the new runs. I am calling it sampling "
                              "noise from only 36-72 bins. If it replicates in both new runs, the homogeneous "
                              "Poisson epoch assumption is wrong and an MMPP/cyclic arrival term is needed."},
        {"id": "Q7", "claim": "Assignment policy is identified by per-server utilisation at low load. "
                              "See the numeric table: 'fastest-idle' predicts the fast server (index 3) "
                              "much more loaded than the slow ones; 'random idle' predicts utilisations "
                              "far closer together. Whichever policy's interval contains the observation wins; "
                              "if neither does, M3 is structurally wrong."},
    ],
    "what_would_falsify_M3_as_a_whole": [
        "either run unstable when predicted stable, or vice versa",
        "observed mean sojourn outside the 95% predictive interval of BOTH assignment policies",
        "per-server rates in OBS-004 inconsistent with the OBS-002 pool",
        "any abandonment/balking rows",
    ],
}

for name, E in (("OBS-003", E2), ("OBS-004", E3)):
    rates = RATES[:E["c"]]
    entry = {
        "id": name,
        "command": (f"world.py observe --arrival-rate {E['lam']} --servers {E['c']} "
                    f"--horizon {E['horizon']} --warmup {E['warmup']} "
                    f"--run-seed {7 if name == 'OBS-003' else 11} --level 3"),
        "conditions": E,
        "fitted_capacity": sum(rates),
        "predicted_rho": E["lam"] / sum(rates),
        "by_policy": {},
    }
    for pol in ("fastest", "random"):
        print(f"simulating {name} under policy={pol} ...", flush=True)
        entry["by_policy"][pol] = predictive(E["lam"], E["c"], rates, MEAN_BATCH,
                                             E["horizon"], E["warmup"], pol, reps=40)
    out["experiments_requested"].append(entry)

p = Path("predictions/PRED-002.json")
p.parent.mkdir(exist_ok=True)
p.write_text(json.dumps(out, indent=2), encoding="utf-8")
print("wrote", p)

for e in out["experiments_requested"]:
    print(f"\n--- {e['id']}  lambda={e['conditions']['lam']} c={e['conditions']['c']} "
          f"rho={e['predicted_rho']:.3f} ---")
    for pol, r in e["by_policy"].items():
        print(f"  policy={pol:8s} W={r['W_mean']['mean']:.3f} "
              f"[{r['W_mean']['lo95']:.3f},{r['W_mean']['hi95']:.3f}]  "
              f"Wq={r['Wq_mean']['mean']:.3f}  P(wait)={r['P_wait']['mean']:.3f}  "
              f"Lq={r['Lq']['mean']:.2f}")
        print(f"           util={[round(u,3) for u in r['util']['mean']]}")
