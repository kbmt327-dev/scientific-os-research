"""Experiment E23 (EP-0034, C-058): where does fcfs's state coupling come from?

E21/E22's ladder via run_e20.one in its opt-in C-058 mode: BASE and F record
every placement's cluster state, and fcfs gets three stratified shuffles of F's
slowdowns (CO busy servers, CQ queue length, CT arrival-order block) beside CS.
New seeds 2301-2306, horizons 160k/320k.

Predictions were sealed in predictions/PRED-022.json before this script ran.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_e20 as e

HORIZONS = [160_000, 320_000]
SEEDS = [2301, 2302, 2303, 2304, 2305, 2306]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "E23.json")


def to_py(o):
    return o.item() if hasattr(o, "item") else str(o)


if __name__ == "__main__":
    if os.path.exists(OUT):
        raise FileExistsError(OUT)
    tasks = [(pol, rho, pen, s, h) for pol in e.POLICIES for rho, pen in e.ROWS
             for s in SEEDS for h in HORIZONS]
    tasks = [t + ({"c058": True},) for t in tasks]
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
                          "arms": {"fcfs": e.ARMS["fcfs"] + e.C058_ARMS, "srpt": e.ARMS["srpt"]}, "mix": [list(e.MIX[0]), list(e.MIX[1])],
                          "penalty_mode": "excess", "placement": "first_fit",
                          "backlog_cap": e.BACKLOG_CAP, "pred": "PRED-022", "c058": True},
               "rows": rows}, open(OUT, "w"), indent=1, default=to_py)
    print(f"wrote {OUT} in {time.time() - t0:.0f}s")
