#!/usr/bin/env python3
"""Blinded queueing simulation world for the Scientific OS benchmark.

The world's mechanism and parameters are derived deterministically from a
master seed created with os.urandom and stored in a seal file.  The seal file
contains ONLY the random hex seed plus a commitment hash, so reading it does
not disclose the mechanism.  `observe` never prints or writes any part of the
truth; only `reveal` does, and it is meant to be run once, after the study is
closed.

Sub-commands
------------
  seal        create the hidden world (writes seal/world_seal.json)
  fingerprint print sha256 of the canonical truth JSON (a commitment, not the truth)
  observe     run one experiment and write an observation file
  reveal      print the truth  (DO NOT RUN UNTIL THE STUDY IS CLOSED)
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

SCHEMA = "queue-world.v1"
MEAN_SERVICE = 1.0  # time unit: one mean service time at an ordinary, unloaded server


# --------------------------------------------------------------------------
# world derivation (deterministic in the master seed)
# --------------------------------------------------------------------------
def _rng(master_seed_hex: str, stream: str) -> np.random.Generator:
    h = hashlib.sha256((master_seed_hex + "|" + stream).encode()).digest()
    return np.random.default_rng(list(h))


def derive_world(master_seed_hex: str) -> dict:
    r = _rng(master_seed_hex, "world-derivation")

    world = {
        "arrival": {"kind": "poisson", "params": {}},
        "service": {"kind": "exponential", "params": {"cv": 1.0}},
        "servers": {"kind": "homogeneous", "params": {}},
        "customers": {"kind": "patient", "params": {}},
    }

    n_dev = int(r.choice([0, 1, 2], p=[0.15, 0.50, 0.35]))
    dims = list(r.choice(["arrival", "service", "servers", "customers"],
                         size=n_dev, replace=False)) if n_dev else []

    if "arrival" in dims:
        kind = str(r.choice(["mmpp", "sinusoidal", "batch"], p=[0.4, 0.3, 0.3]))
        if kind == "mmpp":
            hi = float(r.uniform(1.8, 3.5))
            p_hi = float(r.uniform(0.15, 0.40))
            lo = max((1.0 - p_hi * hi) / (1.0 - p_hi), 0.05)
            world["arrival"] = {"kind": "mmpp", "params": {
                "mult_low": lo, "mult_high": hi, "p_high": p_hi,
                "mean_sojourn_low": float(r.uniform(8, 40)),
                "mean_sojourn_high": float(r.uniform(3, 15))}}
        elif kind == "sinusoidal":
            world["arrival"] = {"kind": "sinusoidal", "params": {
                "amplitude": float(r.uniform(0.35, 0.85)),
                "period": float(r.uniform(40, 220)),
                "phase": float(r.uniform(0, 2 * math.pi))}}
        else:
            world["arrival"] = {"kind": "batch", "params": {
                "mean_batch": float(r.uniform(1.8, 4.5))}}

    if "service" in dims:
        kind = str(r.choice(["erlang", "lognormal", "hyperexponential"], p=[0.3, 0.4, 0.3]))
        if kind == "erlang":
            k = int(r.integers(2, 9))
            world["service"] = {"kind": "erlang", "params": {"k": k, "cv": 1 / math.sqrt(k)}}
        elif kind == "lognormal":
            world["service"] = {"kind": "lognormal", "params": {"cv": float(r.uniform(1.6, 3.2))}}
        else:
            world["service"] = {"kind": "hyperexponential", "params": {
                "cv": float(r.uniform(2.0, 4.0)), "p1": float(r.uniform(0.55, 0.9))}}

    if "servers" in dims:
        kind = str(r.choice(["heterogeneous", "vacation", "state_dependent"], p=[0.35, 0.35, 0.30]))
        if kind == "heterogeneous":
            world["servers"] = {"kind": "heterogeneous",
                                "params": {"log_sd": float(r.uniform(0.35, 0.8))}}
        elif kind == "vacation":
            world["servers"] = {"kind": "vacation", "params": {
                "mean_vacation": float(r.uniform(0.3, 2.5)), "policy": "multiple"}}
        else:
            world["servers"] = {"kind": "state_dependent", "params": {
                "beta": float(r.choice([1.0, -1.0], p=[0.75, 0.25]) * r.uniform(0.15, 0.6)),
                "cap": 20.0}}

    if "customers" in dims:
        kind = str(r.choice(["abandonment", "balking"], p=[0.6, 0.4]))
        if kind == "abandonment":
            world["customers"] = {"kind": "abandonment",
                                  "params": {"mean_patience": float(r.uniform(1.2, 8.0))}}
        else:
            world["customers"] = {"kind": "balking",
                                  "params": {"beta": float(r.uniform(0.15, 0.6))}}

    world["_meta"] = {"schema": SCHEMA, "mean_service": MEAN_SERVICE, "n_deviations": n_dev}
    return world


def server_multipliers(master_seed_hex: str, world: dict, c: int) -> np.ndarray:
    """Per-server *rate* multipliers (mean 1).  Stable across experiments."""
    if world["servers"]["kind"] != "heterogeneous":
        return np.ones(c)
    sd = world["servers"]["params"]["log_sd"]
    r = _rng(master_seed_hex, "server-pool")
    x = r.normal(-0.5 * sd * sd, sd, size=256)  # E[e^x] = 1
    return np.exp(x[:c])


# --------------------------------------------------------------------------
# simulation
# --------------------------------------------------------------------------
ARRIVAL, DEPARTURE, ABANDON, VACATION_END, MMPP_SWITCH = 0, 1, 2, 3, 4


def _draw_service(world, rng, mult_rate, q_wait, c):
    kind = world["service"]["kind"]
    p = world["service"]["params"]
    if kind == "exponential":
        s = rng.exponential(MEAN_SERVICE)
    elif kind == "erlang":
        k = p["k"]
        s = rng.gamma(k, MEAN_SERVICE / k)
    elif kind == "lognormal":
        cv = p["cv"]
        sigma = math.sqrt(math.log(1 + cv * cv))
        mu = math.log(MEAN_SERVICE) - 0.5 * sigma * sigma
        s = rng.lognormal(mu, sigma)
    elif kind == "hyperexponential":
        cv, p1 = p["cv"], p["p1"]
        c2 = cv * cv
        lo, hi = 1e-9, 1.0 / p1 - 1e-9
        for _ in range(200):
            a = 0.5 * (lo + hi)
            m2 = (1 - p1 * a) / (1 - p1)
            if 2 * (p1 * a * a + (1 - p1) * m2 * m2) < 1 + c2:
                hi = a
            else:
                lo = a
        a = 0.5 * (lo + hi)
        m2 = (1 - p1 * a) / (1 - p1)
        s = rng.exponential(a if rng.random() < p1 else m2)
    else:
        raise ValueError(kind)

    if world["servers"]["kind"] == "state_dependent":
        pr = world["servers"]["params"]
        s *= 1.0 + pr["beta"] * min(q_wait, pr["cap"] * c) / c
    return s / mult_rate


def simulate(master_seed_hex: str, world: dict, lam: float, c: int,
             horizon: float, run_seed: int) -> dict:
    rng = np.random.default_rng(list(hashlib.sha256(
        f"{master_seed_hex}|run|{lam}|{c}|{horizon}|{run_seed}".encode()).digest()))
    mult = server_multipliers(master_seed_hex, world, c)

    akind = world["arrival"]["kind"]
    ap = world["arrival"]["params"]
    ckind = world["customers"]["kind"]
    cp = world["customers"]["params"]
    vac = world["servers"]["kind"] == "vacation"
    vp = world["servers"]["params"] if vac else {}

    mean_batch = ap["mean_batch"] if akind == "batch" else 1.0
    epoch_rate = lam / mean_batch
    mmpp_state = 0

    def rate_at(t):
        if akind == "sinusoidal":
            return epoch_rate * (1 + ap["amplitude"] *
                                 math.sin(2 * math.pi * t / ap["period"] + ap["phase"]))
        if akind == "mmpp":
            return epoch_rate * (ap["mult_high"] if mmpp_state else ap["mult_low"])
        return epoch_rate

    if akind == "sinusoidal":
        rate_max = epoch_rate * (1 + ap["amplitude"])
    elif akind == "mmpp":
        rate_max = epoch_rate * ap["mult_high"]
    else:
        rate_max = epoch_rate

    def next_epoch(t):
        while True:
            t = t + rng.exponential(1.0 / rate_max)
            if t > horizon:
                return t
            if akind in ("poisson", "batch"):
                return t
            if rng.random() < rate_at(t) / rate_max:
                return t

    events = []
    seq = 0

    def push(t, kind, data):
        nonlocal seq
        seq += 1
        heapq.heappush(events, (t, seq, kind, data))

    push(next_epoch(0.0), ARRIVAL, None)
    if akind == "mmpp":
        push(rng.exponential(ap["mean_sojourn_low"]), MMPP_SWITCH, None)

    servers = [{"state": "idle", "cust": None} for _ in range(c)]
    queue = []
    custs = []
    qsamples = []
    next_sample = 0.0
    sample_dt = max(horizon / 4000.0, 0.05)
    last_t = 0.0
    busy_time = 0.0
    hetero = world["servers"]["kind"] == "heterogeneous"

    def start_service(i, cust, t):
        s = _draw_service(world, rng, mult[i], len(queue), c)
        servers[i]["state"] = "busy"
        servers[i]["cust"] = cust
        cust["start"] = t
        cust["server"] = i
        cust["service_time"] = s
        push(t + s, DEPARTURE, i)

    while events:
        t, _, kind, data = heapq.heappop(events)
        if t > horizon:
            break
        nb = sum(1 for s in servers if s["state"] == "busy")
        busy_time += nb * (t - last_t)
        while next_sample <= t:
            qsamples.append((next_sample, len(queue), nb))
            next_sample += sample_dt
        last_t = t

        if kind == MMPP_SWITCH:
            mmpp_state = 1 - mmpp_state
            soj = ap["mean_sojourn_high"] if mmpp_state else ap["mean_sojourn_low"]
            push(t + rng.exponential(soj), MMPP_SWITCH, None)

        elif kind == ARRIVAL:
            n = int(rng.geometric(1.0 / mean_batch)) if akind == "batch" else 1
            for _ in range(n):
                cust = {"id": len(custs), "arr": t, "start": None, "dep": None,
                        "server": None, "reason": None, "service_time": None}
                custs.append(cust)
                if ckind == "balking":
                    q = len(queue)
                    if q > 0 and rng.random() < 1 - math.exp(-cp["beta"] * q / c):
                        cust["reason"] = "balked"
                        continue
                free = [i for i, s in enumerate(servers) if s["state"] == "idle"]
                if free:
                    i = int(max(free, key=lambda j: mult[j])) if hetero else free[0]
                    start_service(i, cust, t)
                else:
                    queue.append(cust)
                    if ckind == "abandonment":
                        pat = rng.exponential(cp["mean_patience"])
                        push(t + pat, ABANDON, cust["id"])
            push(next_epoch(t), ARRIVAL, None)

        elif kind == DEPARTURE:
            i = data
            cust = servers[i]["cust"]
            cust["dep"] = t
            cust["reason"] = "served"
            servers[i]["cust"] = None
            servers[i]["state"] = "idle"
            if queue:
                start_service(i, queue.pop(0), t)
            elif vac:
                servers[i]["state"] = "vacation"
                push(t + rng.exponential(vp["mean_vacation"]), VACATION_END, i)

        elif kind == VACATION_END:
            i = data
            if queue:
                servers[i]["state"] = "idle"
                start_service(i, queue.pop(0), t)
            else:
                push(t + rng.exponential(vp["mean_vacation"]), VACATION_END, i)

        elif kind == ABANDON:
            cust = custs[data]
            if cust["start"] is None and cust["reason"] is None and cust in queue:
                queue.remove(cust)
                cust["reason"] = "abandoned"
                cust["dep"] = t

    return {"customers": custs, "qsamples": qsamples, "horizon": horizon,
            "c": c, "lam_requested": lam, "busy_time": busy_time}


# --------------------------------------------------------------------------
# observation writing
# --------------------------------------------------------------------------
def write_observation(res: dict, level: int, out: Path, meta: dict) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["customer_id", "arrival_time", "departure_time"]
    if level >= 2:
        cols.append("service_start_time")
    if level >= 3:
        cols += ["server_id", "exit_reason"]
    warm = meta.get("warmup", 0.0)
    lines = [",".join(cols)]
    for cu in res["customers"]:
        if cu["arr"] < warm:
            continue
        row = [str(cu["id"]), f"{cu['arr']:.6f}",
               "" if cu["reason"] != "served" else f"{cu['dep']:.6f}"]
        if level >= 2:
            row.append("" if cu["start"] is None else f"{cu['start']:.6f}")
        if level >= 3:
            row.append("" if cu["server"] is None else str(cu["server"]))
            row.append(cu["reason"] or "in_system")
        lines.append(",".join(row))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    side = {"schema": SCHEMA, "observation_level": level, "c": res["c"],
            "horizon": res["horizon"], "warmup": warm,
            "requested_arrival_rate": res["lam_requested"], "n_rows": len(lines) - 1}
    side.update(meta.get("extra", {}))
    out.with_suffix(".meta.json").write_text(json.dumps(side, indent=2), encoding="utf-8")

    if level >= 3:
        ql = ["time,n_waiting,n_busy"]
        ql += [f"{t:.4f},{q},{b}" for (t, q, b) in res["qsamples"] if t >= warm]
        out.with_name(out.stem + "_qsamples.csv").write_text("\n".join(ql) + "\n", encoding="utf-8")


def canonical_truth(world: dict) -> str:
    return json.dumps(world, sort_keys=True, separators=(",", ":"))


def main() -> int:
    ap = argparse.ArgumentParser(description="blinded queueing world")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("seal")
    s.add_argument("--out", required=True)
    s.add_argument("--force", action="store_true")
    f = sub.add_parser("fingerprint")
    f.add_argument("--seal", required=True)
    o = sub.add_parser("observe")
    o.add_argument("--seal", required=True)
    o.add_argument("--arrival-rate", type=float, required=True)
    o.add_argument("--servers", type=int, required=True)
    o.add_argument("--horizon", type=float, required=True)
    o.add_argument("--warmup", type=float, default=0.0)
    o.add_argument("--run-seed", type=int, required=True)
    o.add_argument("--level", type=int, default=1, choices=[1, 2, 3])
    o.add_argument("--out", required=True)
    rv = sub.add_parser("reveal")
    rv.add_argument("--seal", required=True)

    a = ap.parse_args()

    if a.cmd == "seal":
        p = Path(a.out)
        if p.exists() and not a.force:
            print("seal already exists: " + str(p), file=sys.stderr)
            return 1
        p.parent.mkdir(parents=True, exist_ok=True)
        seed = os.urandom(16).hex()
        commit = hashlib.sha256(canonical_truth(derive_world(seed)).encode()).hexdigest()
        p.write_text(json.dumps({
            "schema": SCHEMA, "master_seed": seed,
            "truth_commitment_sha256": commit,
            "note": "Only a random seed and a commitment hash are stored here. "
                    "The mechanism is derived at run time and never written to disk.",
        }, indent=2), encoding="utf-8")
        print("sealed -> " + str(p))
        print("commitment: " + commit)
        return 0

    seal = json.loads(Path(a.seal).read_text(encoding="utf-8"))
    world = derive_world(seal["master_seed"])

    if a.cmd == "fingerprint":
        print(hashlib.sha256(canonical_truth(world).encode()).hexdigest())
        return 0

    if a.cmd == "reveal":
        print(json.dumps(world, indent=2, sort_keys=True))
        print("commitment: " + hashlib.sha256(canonical_truth(world).encode()).hexdigest())
        return 0

    res = simulate(seal["master_seed"], world, a.arrival_rate, a.servers, a.horizon, a.run_seed)
    write_observation(res, a.level, Path(a.out), {
        "warmup": a.warmup,
        "extra": {"run_seed": a.run_seed,
                  "time_unit": "one mean service time at an ordinary unloaded server"}})
    print("wrote " + a.out + " (level " + str(a.level) + ", " +
          str(len(res["customers"])) + " arrivals simulated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
