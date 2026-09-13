"""A09: PRED-003, sealed before OBS-005..012 (replication) and OBS-013 (c=6).

Two open items after A08:
  (a) M3t missed W_mean / Wq_mean on OBS-003 (observed 3.370 vs predicted 2.965).
      Is that a residual mis-specification, or one lucky run?  Eight fresh world
      replications at the same setting decide it.
  (b) The server pool has only four known members.  c=6 introduces two servers
      whose rates the model cannot predict.  That is declared UNKNOWN in advance.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fitted_model import simulate

POOL_T = [0.6930, 0.3625, 0.3625, 1.0275]
BATCH = 1.9810
N_REP = 8

runs = [simulate(1.6, 4, POOL_T, BATCH, 6000, 300, "fastest", seed=9000 + k)
        for k in range(200)]
W = np.array([r["W_mean"] for r in runs])
Wq = np.array([r["Wq_mean"] for r in runs])

# predictive distribution for the MEAN of N_REP independent runs
boot = np.array([W[np.random.default_rng(s).integers(0, len(W), N_REP)].mean()
                 for s in range(4000)])
bootq = np.array([Wq[np.random.default_rng(s).integers(0, len(Wq), N_REP)].mean()
                  for s in range(4000)])

out = {
    "prediction_id": "PRED-003",
    "registered_at": "2026-09-13",
    "status": "sealed-before-observation",
    "world_commitment_sha256": "7c4e47709de366e295aec26be7fac462100d1c6bf3d49fcd9ec03e40930b663a",
    "information_cutoff": "OBS-001..004",
    "model": {"name": "M3t", "server_pool": POOL_T, "mean_batch": BATCH,
              "assignment": "fastest idle",
              "note": "the assignment rule is world-FAMILY knowledge (I wrote the generator), "
                      "not a blind inference; A06 utilisation only confirmed it is consistent"},
    "single_run_reference": {
        "W_mean": {"mean": float(W.mean()), "sd": float(W.std(ddof=1)),
                   "lo95": float(np.quantile(W, .025)), "hi95": float(np.quantile(W, .975))},
        "Wq_mean": {"mean": float(Wq.mean()), "sd": float(Wq.std(ddof=1)),
                    "lo95": float(np.quantile(Wq, .025)), "hi95": float(np.quantile(Wq, .975))},
    },
    "predictions": [
        {"id": "R1",
         "experiment": "OBS-005..012: eight fresh world runs, lambda=1.6, c=4, "
                       "horizon 6000, warmup 300, run-seeds 101..108, level 3",
         "claim": f"the mean of W_mean over the eight runs falls in "
                  f"[{np.quantile(boot,.025):.3f}, {np.quantile(boot,.975):.3f}] "
                  f"(M3t predictive 95% interval for an 8-run mean; point {boot.mean():.3f})",
         "interval": [float(np.quantile(boot, .025)), float(np.quantile(boot, .975))],
         "also": f"mean of Wq_mean falls in [{np.quantile(bootq,.025):.3f}, "
                 f"{np.quantile(bootq,.975):.3f}]",
         "interval_Wq": [float(np.quantile(bootq, .025)), float(np.quantile(bootq, .975))],
         "if_it_fails": "M3t is mis-specified for the waiting-time law at moderate load; "
                        "the OBS-003 excess was not luck and a further mechanism is needed",
         "if_it_holds": "the OBS-003 miss was ordinary run-to-run variation and M3t stands"},
        {"id": "R2",
         "experiment": "OBS-013: lambda=2.0, c=6, horizon 6000, warmup 300, run-seed 21, level 3",
         "claim": "servers 0,1,2,3 reproduce the pool rates 0.6930 / 0.3625 / 0.3625 / 1.0275 "
                  "within their 95% CIs; servers 4 and 5 have stable, server-specific, "
                  "exponential service (per-server CV in [0.92, 1.08]).",
         "declared_unknown": "the RATES of servers 4 and 5. Four observed rates are not enough "
                             "to identify the distribution they are drawn from, so the model "
                             "cannot predict capacity at c>4. This is a boundary of M3t, "
                             "stated before the observation rather than after it.",
         "if_it_fails": "server identity is not a persistent property and the pool abstraction "
                        "must be replaced"},
    ],
}

p = Path("predictions/PRED-003.json")
p.write_text(json.dumps(out, indent=2), encoding="utf-8")
print("wrote", p)
print(json.dumps(out["predictions"], indent=2)[:1600])
