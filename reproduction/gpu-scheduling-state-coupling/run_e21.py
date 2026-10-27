"""Experiment E21 (C-056): E20's exact-work ladder on longer windows.

E20 (PRED-019) was unscorable: every fcfs cell at pi > 0 was UNKNOWN with the
40k/80k pair on six seeds. pilot_e21.py (seeds 3001-3006) found all 27 cells
STABLE with the 160k/320k pair. E21 reruns E20's design unchanged -- same
rows, arms, policies and statistics, via run_e20.one -- on new seeds
2101-2106 with horizons 160k/320k.

Predictions were sealed in predictions/PRED-020.json before this script ran.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_e20 as e

HORIZONS = [160_000, 320_000]
SEEDS = [2101, 2102, 2103, 2104, 2105, 2106]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "E21.json")


def to_py(o):
    return o.item() if hasattr(o, "item") else str(o)


if __name__ == "__main__":
    if os.path.exists(OUT):
        raise FileExistsError(OUT)
    tasks = [(pol, rho, pen, s, h) for pol in e.POLICIES for rho, pen in e.ROWS
             for s in SEEDS for h in HORIZONS]
    tasks.sort(key=lambda t: (t[0] != "fcfs", -t[4]))
    print(f"{len(tasks)} tasks", flush=True)
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=int(os.environ.get("WORKERS", 14))) as ex:
        for i, recs in enumerate(ex.map(e.one, tasks), 1):
            rows.extend(recs)
            if i % 10 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)} ({time.time() - t0:.0f}s)", flush=True)
    json.dump({"config": {"n_servers": e.N, "node_size": e.NODE, "horizons": HORIZONS,
                          "seeds": SEEDS, "rows": e.ROWS, "policies": e.POLICIES,
                          "arms": e.ARMS, "mix": [list(e.MIX[0]), list(e.MIX[1])],
                          "penalty_mode": "excess", "placement": "first_fit",
                          "backlog_cap": e.BACKLOG_CAP, "pred": "PRED-020"},
               "rows": rows}, open(OUT, "w"), indent=1, default=to_py)
    print(f"wrote {OUT} in {time.time() - t0:.0f}s")
