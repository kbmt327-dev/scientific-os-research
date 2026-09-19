"""Sealed eventual-tail drift and declaration-gate audit.

The known label is supplied by the stationary regime that persists forever
after a finite change.  This does not claim that data alone verifies model
applicability; it measures the consequence of a false stationary declaration.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, subprocess, sys, time
import numpy as np

from two_class_control import exact_capacity, fcfs
from observation_capacity import diagnose
from checkpoint_capacity import (ATTESTATION, applicability, checkpoint_tape,
                                  scheduled_diagnose)

MODELS = [
    dict(id="baseline", p=.5, mu_small=1., mu_big=.5),
    dict(id="transfer", p=.25, mu_small=.5, mu_big=2.),
]
SCENARIOS = ["stationary_subcritical", "stationary_overloaded",
             "arrival_up", "arrival_down", "service_degrade", "service_improve"]
HORIZONS = [100000, 160000, 320000]
MILESTONES = [2**j for j in range(8, 19)]
SEEDS = list(range(9301, 9311))
CHANGE_AFTER = 80000

def now(): return datetime.now(timezone.utc).isoformat()
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def capacity(model):
    return float(F(exact_capacity(F(model["p"]), F(model["mu_small"]),
                                  F(model["mu_big"]))["throughput"]))

def scenario_spec(model, name, n):
    x = capacity(model)
    pre = dict(p=model["p"], mu_small=model["mu_small"], mu_big=model["mu_big"])
    post = dict(pre)
    if name == "stationary_subcritical": pre_lam = post_lam = .8*x
    elif name == "stationary_overloaded": pre_lam = post_lam = 1.2*x
    elif name == "arrival_up": pre_lam, post_lam = .8*x, 1.2*x
    elif name == "arrival_down": pre_lam, post_lam = 1.2*x, .8*x
    elif name == "service_degrade":
        pre_lam = post_lam = .8*x
        post.update(mu_small=.5*model["mu_small"], mu_big=.5*model["mu_big"])
    elif name == "service_improve":
        pre.update(mu_small=.5*model["mu_small"], mu_big=.5*model["mu_big"])
        pre_lam = post_lam = .8*x
    else: raise ValueError(name)
    post_x = float(F(exact_capacity(F(post["p"]), F(post["mu_small"]),
                                     F(post["mu_big"]))["throughput"]))
    tail = "subcritical" if post_lam < post_x else "overloaded"
    changed = name not in ("stationary_subcritical", "stationary_overloaded")
    return dict(pre=pre, post=post, pre_lambda=pre_lam, post_lambda=post_lam,
                post_capacity=post_x, tail_truth=tail, changed=changed,
                change_after_arrival=CHANGE_AFTER if changed else None)

def generate_piecewise(n, seed, spec):
    streams = [np.random.default_rng(x) for x in np.random.SeedSequence(seed).spawn(3)]
    after = np.arange(n) >= CHANGE_AFTER if spec["changed"] else np.zeros(n, dtype=bool)
    lam = np.where(after, spec["post_lambda"], spec["pre_lambda"])
    arrival = np.cumsum(streams[0].exponential(1/lam))
    p = np.where(after, spec["post"]["p"], spec["pre"]["p"])
    need = np.where(streams[1].random(n) < p, 1, 2)
    mus = np.where(need == 1,
                   np.where(after, spec["post"]["mu_small"], spec["pre"]["mu_small"]),
                   np.where(after, spec["post"]["mu_big"], spec["pre"]["mu_big"]))
    service = streams[2].exponential(1., n)/mus
    return arrival, service, need

def truthful_attestation(spec):
    if not spec["changed"]: return dict(ATTESTATION)
    out = dict(ATTESTATION)
    out["parameter_transition"] = dict(kind="permanent_after_arrival_index",
                                        after=CHANGE_AFTER,
                                        fields=["arrival_rate", "service_rates"])
    return out

def execute(contract, progress=None):
    result = dict(protocol_id=contract["protocol_id"], started_at=now(), contract=contract,
                  decisions=[], cells=[], verdict="RUNNING", validated_general_detector=False,
                  independent_replication=False)
    for model in contract["models"]:
        for scenario in contract["scenarios"]:
            spec = scenario_spec(model, scenario, max(contract["horizons"]))
            expected_gate = not spec["changed"]
            for seed in contract["seeds"]:
                a, s, k = generate_piecewise(max(contract["horizons"]), seed, spec)
                d = fcfs(a, s, k)
                for h in contract["horizons"]:
                    aa, kk, dd = a[:h], k[:h], d[:h]
                    tau = float(aa[-1]); mask = dd <= tau
                    tape = checkpoint_tape(aa, kk, np.where(mask)[0], dd[mask], tau,
                                           contract["milestones"])
                    declared = scheduled_diagnose(tape, truthful_attestation(spec),
                                                  contract["horizons"], contract["milestones"],
                                                  contract["alpha"])
                    bypass = scheduled_diagnose(tape, dict(ATTESTATION), contract["horizons"],
                                                contract["milestones"], contract["alpha"])
                    anytime = diagnose(tape["observed"], contract["alpha"])
                    result["decisions"].append(dict(
                        model=model["id"], scenario=scenario, seed=seed, horizon=h,
                        eventual_tail_truth=spec["tail_truth"], post_capacity=spec["post_capacity"],
                        truthful_gate_expected=expected_gate,
                        truthful=dict(label=declared["label"], inference_performed=declared["inference_performed"],
                                       reason=declared.get("reason"), gate=declared["gate"]),
                        false_stationary_declaration=dict(checkpoint_label=bypass["label"],
                                                          anytime_label=anytime["label"]),
                        observed=tape["observed"], selected_checkpoints=bypass.get("selected_checkpoints")))
                if progress: progress(result)
            print(model["id"], scenario, "finished", flush=True)
    for model in contract["models"]:
        for scenario in contract["scenarios"]:
            for h in contract["horizons"]:
                rows=[r for r in result["decisions"] if (r["model"],r["scenario"],r["horizon"])==(model["id"],scenario,h)]
                truth=rows[0]["eventual_tail_truth"]
                def metric(key):
                    labels=[r["false_stationary_declaration"][key] for r in rows]
                    return dict(wrong=sum(x not in ("UNKNOWN",truth) for x in labels),
                                unknown=sum(x=="UNKNOWN" for x in labels),
                                correct=sum(x==truth for x in labels))
                result["cells"].append(dict(model=model["id"], scenario=scenario, horizon=h,
                                             n=len(rows), truth=truth,
                                             checkpoint=metric("checkpoint_label"),
                                             anytime=metric("anytime_label"),
                                             truthful_inference=sum(r["truthful"]["inference_performed"] for r in rows)))
    def cells(scenarios,h): return [c for c in result["cells"] if c["scenario"] in scenarios and c["horizon"]==h]
    stationary=[r for r in result["decisions"] if r["scenario"].startswith("stationary")]
    drift=[r for r in result["decisions"] if not r["scenario"].startswith("stationary")]
    result["prediction_grading"]={
        "D1_stationary_truthful_accepts_and_correct": all(r["truthful"]["inference_performed"] and r["truthful"]["label"]==r["eventual_tail_truth"] for r in stationary),
        "D2_declared_drift_always_refused": all(not r["truthful"]["inference_performed"] and r["truthful"]["label"]=="UNKNOWN" for r in drift),
        "D3_arrival_drift_wrong_at_100k": sum(c["checkpoint"]["wrong"] for c in cells(["arrival_up","arrival_down"],100000)) >= 30,
        "D4_arrival_drift_recovers_by_320k": sum(c["checkpoint"]["wrong"] for c in cells(["arrival_up","arrival_down"],320000)) <= 5,
        "D5_service_drift_has_wrong_at_100k": sum(c["checkpoint"]["wrong"] for c in cells(["service_degrade","service_improve"],100000)) >= 1,
    }
    result.update(verdict="MEASURED eventual-tail-transition-audit", completed_at=now(),
                  executed_workloads=len(contract["models"])*len(contract["scenarios"])*len(contract["seeds"]),
                  executed_looks=len(result["decisions"]), executed_method_decisions=3*len(result["decisions"]))
    return result
