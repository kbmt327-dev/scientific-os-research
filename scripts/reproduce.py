#!/usr/bin/env python3
"""Run bounded public reproduction checks without claiming independent replication."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"failed in {cwd}: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def gpu() -> None:
    root = ROOT / "reproduction" / "gpu-scheduling"
    pred = root / "predictions" / "PRED-001.json"
    # The sealed digest was computed from the repository's LF byte stream.
    # Normalize checkout line endings so the check is stable on Windows.
    digest = hashlib.sha256(pred.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    expected = "dd977a92c0edf7472a6190d35dab7baa22743375627ca326be354d4c4eda4b01"
    assert digest == expected, (digest, expected)
    grading = json.loads((root / "results" / "E1_grading.json").read_text(encoding="utf-8"))
    assert len(grading) == 10 and sum(row["pass"] for row in grading) == 7
    print("gpu: sealed prediction hash and 7/10 grading verified")


def gpu_phase() -> None:
    root = ROOT / "reproduction" / "gpu-scheduling-phase"
    # Both digests were computed from the repository's LF byte stream.
    expected = {
        "PRED-002": "d726c5a701367f3be0bff47eba10267ee5fcd43bc4b830ec70c97a22477ed8a0",
        "PRED-003": "2f3b1808d806e9af888acaa77a7e00f7e9af86a13d58e42ac75e514a91157d05",
        "PRED-004": "7ef0f5b21d46318e6008a1be3021e9c1ffbefbe3fb23e959c3cffa7268048cbe",
        "PRED-005": "fe3e27d68d27c5c8eb9fb6633d133e17fd6c4ba09158ab80d901dc4630ccb902",
    }
    for name, want in expected.items():
        # read_text() applies universal newlines, so this is the LF byte
        # stream the digest was sealed over, whatever the checkout style.
        text = (root / "predictions" / f"{name}.json").read_text(encoding="utf-8")
        got = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert got == want, (name, got, want)
    e2e3 = json.loads((root / "results" / "E2E3_grading.json").read_text(encoding="utf-8"))
    assert e2e3["n_total"] == 10 and e2e3["n_pass"] == 5
    # The as-run detector is kept so the post-hoc detector change stays auditable.
    assert e2e3["n_pass_asrun"] == 4
    e4 = json.loads((root / "results" / "E4_grading.json").read_text(encoding="utf-8"))
    assert e4["n_total"] == 10 and e4["n_pass"] == 7
    starved = {r["id"] for r in e4["results"] if r["pass"]}
    assert {"R1", "R3", "R6"} <= starved, starved
    # Real-trace measurement. No whole-pool job appears in any Philly virtual
    # cluster, which is what demoted the practical claim of the previous study.
    traces = json.loads((root / "results" / "E5_traces.json").read_text(encoding="utf-8"))
    vcs = traces["philly_vc_capacity"]
    assert len(vcs) == 11, len(vcs)
    assert all(vc["p_ge_peak"] == 0.0 for vc in vcs), vcs
    assert max(vc["max_k_over_peak"] for vc in vcs) < 1.0
    e5 = json.loads((root / "results" / "E5_grading.json").read_text(encoding="utf-8"))
    assert e5["n_total"] == 10 and e5["n_pass"] == 5
    # The decisive prediction was named against the project's own claim, and
    # passing it is what triggered the pre-registered demotion.
    e6 = json.loads((root / "results" / "E6_grading.json").read_text(encoding="utf-8"))
    assert e6["n_total"] == 10 and e6["n_pass"] == 9
    assert e6["t4_passed"] is True
    assert e6["r_safe"] == 0.75
    print("gpu-phase: PRED-002/003/004/005 digests and 5/7/5/9 gradings verified; "
          "no whole-pool job in any measured virtual cluster")


def gpu_boundary() -> None:
    """EP-0005..EP-0013. The arc in which the project's own boundary statistic
    was found to be measuring the wrong thing, and was replaced."""
    root = ROOT / "reproduction" / "gpu-scheduling-boundary"
    # Digests are verified against the committed .sha256 files, each written
    # before its sweep ran.
    for name in [f"PRED-{n:03d}" for n in range(6, 15)]:
        text = (root / "predictions" / f"{name}.json").read_text(encoding="utf-8")
        got = hashlib.sha256(text.encode("utf-8")).hexdigest()
        # some .sha256 files are in sha256sum format ("<hash>  <file>")
        want = (root / "predictions" / f"{name}.sha256").read_text(
            encoding="utf-8").split()[0]
        assert got == want, (name, got, want)

    # EP-0011: flow balance is a censoring ratio, so it cannot see divergence.
    # The largest class's mean response time grows 3.9x over a 4x horizon while
    # flow balance moves from 0.562 to 0.574.
    e13 = json.loads((root / "results" / "E13.json").read_text(encoding="utf-8"))
    cells = [r for r in e13["rows"] if r["arm"] == "H" and r["e_label"] == "C10"
             and abs(r["ratio"] - 1.0) < 1e-9 and abs(r["p"] - 0.02) < 1e-12]
    by_h = {}
    for r in cells:
        by_h.setdefault(r["n_jobs"], []).append(r)
    jct = {h: sum(x["jct_m"] for x in v) / len(v) for h, v in by_h.items()}
    fb = {h: sum(x["fb_m"] for x in v) / len(v) for h, v in by_h.items()}
    assert jct[120_000] / jct[30_000] > 3.5, jct
    assert abs(fb[120_000] - fb[30_000]) < 0.05, fb

    # EP-0012: alpha reads ~0 where the system is stable and ~1 where it is not,
    # and its boundary does not move when the horizon is multiplied by eight.
    g14 = json.loads((root / "results" / "E14_grading.json").read_text(encoding="utf-8"))
    assert g14["verdicts"]["G1"] == "PASS", g14["verdicts"]
    assert g14["verdicts"]["G5"] == "PASS" and g14["verdicts"]["G6"] == "PASS"
    assert g14["verdicts"]["G7"] == "PASS"
    for key, a in g14["alpha4"].items():
        assert a[0] <= 0.25, (key, a[0])      # r = 0.5, converged
        assert a[-1] >= 0.85, (key, a[-1])    # r = 1.0, linear divergence
    # EASY backfill does not diverge even for a whole-pool class
    assert all(e["alpha"] <= 0.25 for e in g14["easy_alpha"]), g14["easy_alpha"]

    # EP-0013: the project's only real-cluster claim rests on one job.
    e15 = json.loads((root / "results" / "E15.json").read_text(encoding="utf-8"))
    target = next(r for r in e15["rows"] if r["vc"] == "11cb48")
    assert target["max_k"] == 128 and round(target["capacity_gpus"]) == 217
    assert round(target["freq"]["0.5"] * target["n_jobs"]) == 1, target["freq"]
    assert all(r["freq"]["1.0"] == 0.0 for r in e15["rows"])
    print("gpu-boundary: PRED-006..014 digests verified; flow balance shown "
          "blind to a 3.9x divergence; alpha 0-at-stable, 1-at-divergent and "
          "horizon-stable; one job in 19,100 carries the real-cluster claim")


def gpu_u31() -> None:
    output = run([sys.executable, 'verify_summary.py'], ROOT / 'reproduction' / 'gpu-scheduling-u31')
    assert 'arithmetic and stop branch OK' in output
    print('gpu-u31: public aggregate arithmetic and stop branch verified; simulation not reproduced')


def gpu_u31_controls() -> None:
    output = run([sys.executable, 'verify_summary.py'], ROOT / 'reproduction' / 'gpu-scheduling-u31-controls')
    assert 'CI arithmetic and stop branches OK' in output
    mmc = run([sys.executable, 'verify_mmc_summary.py'], ROOT / 'reproduction' / 'gpu-scheduling-u31-controls')
    assert 'M/M/4 CI arithmetic and stopping OK' in mmc
    print('gpu-u31-controls: sufficient-statistic CI and stop branches verified; simulation not reproduced')


def queue() -> None:
    root = ROOT / "reproduction" / "simulation-worlds"
    output = run([sys.executable, "analysis/a11_verify_against_truth.py"], root)
    assert output.count("MATCH") == 5
    assert "max |error| = 2.29%" in output
    print("queue: five structural matches and revealed parameter check verified")


def human() -> None:
    root = ROOT / "reproduction" / "human-model-contract"
    output = run([sys.executable, "tests/validate_contract_v0_2.py"], root)
    result = json.loads(output)
    assert result["all_passed"] is True
    assert len(result["negative_controls"]) == 7
    print("human: contract checks and seven negative controls verified")


def human_dataset() -> None:
    root = ROOT / "reproduction" / "human-model-dataset-portfolio"
    output = run([sys.executable, "tests/validate_dataset_portfolio.py"], root)
    assert "human_dataset_portfolio: PASS" in output
    assert "development=30 validation=10 test=10" in output
    print("human-dataset: portfolio roles, fixed split, hashes, leakage guards, and non-execution boundary verified")


def iaa() -> None:
    root = ROOT / "reproduction" / "badminton-biomechanics"
    output = run([sys.executable, "analysis/ep0008_power_simulation.py", "--iterations", "1000", "--seed", "20260913"], root)
    result = json.loads(output)
    assert len(result["scenarios"]) == 168
    assert result["status"] == "sensitivity_only_not_final_sample_size"
    print("iaa: 168-scenario bounded power sensitivity rerun verified")


def intervention() -> None:
    root = ROOT / "reproduction" / "intervention-grammar"
    output = run([sys.executable, "tests/validate_intervention_grammar.py"], root)
    result = json.loads(output)
    assert result["all_passed"] is True
    assert len(result["negative_controls"]) == 9
    assert result["breaches_covered"] == ["B1", "B2", "B3", "B4", "B5"]
    assert all(row["refused"] for row in result["negative_controls"])
    print("intervention: nine negative controls refused across the five breaches of the observational contract")


def frontier() -> None:
    root = ROOT / "reproduction" / "frontier-metrics"
    output = run([sys.executable, "tests/reproduce_retractions.py"], root)
    result = json.loads(output)
    assert result["both_headline_results_retracted"] is True
    assert result["attack_1_settling_rate_pinned_by_a_constant"]["ratio"] > 5
    assert result["attack_2_decision_line_depends_on_an_unobservable"]["closing_frontier_clears_the_line_at"]
    assert result["survivor_reuse_responds_to_the_frontier"]["verdict"] == "survives"
    print("frontier: both retractions reproduced; the constant moves the metric "
          f"{result['attack_1_settling_rate_pinned_by_a_constant']['ratio']}x further than the frontier does")


def gpu_two_class() -> None:
    root = ROOT / 'reproduction' / 'gpu-scheduling-two-class-control'
    print(run([sys.executable, 'rerun_two_class.py', '--verify-recorded'], root).strip())


def gpu_past_learning() -> None:
    root = ROOT / 'reproduction' / 'gpu-scheduling-past-only-learning'
    print(run([sys.executable, 'rerun_past_learning.py', '--verify-recorded'], root).strip())


def gpu_checkpoints() -> None:
    root = ROOT / 'reproduction' / 'gpu-scheduling-exposure-checkpoints'
    print(run([sys.executable, 'runner_checkpoint.py', '--verify-recorded'], root).strip())


def gpu_transition_refusal() -> None:
    root = ROOT / 'reproduction' / 'gpu-scheduling-transition-refusal'
    print(run([sys.executable, 'runner_transition.py', '--verify-recorded', '--seeds', '2'], root).strip())


def gpu_self_containment() -> None:
    root = ROOT / 'reproduction' / 'gpu-scheduling-self-containment'
    print(run([sys.executable, 'verify_self_containment.py'], root).strip())


CHECKS = {"gpu": gpu, "gpu-phase": gpu_phase,
          "gpu-boundary": gpu_boundary, "gpu-u31": gpu_u31, "gpu-u31-controls": gpu_u31_controls, "gpu-two-class": gpu_two_class, "gpu-past-learning": gpu_past_learning, "gpu-checkpoints": gpu_checkpoints, "gpu-transition-refusal": gpu_transition_refusal, "gpu-self-containment": gpu_self_containment, "queue": queue,
          "human": human, "human-dataset": human_dataset, "iaa": iaa,
          "intervention": intervention,
          "frontier": frontier}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", choices=["all", *CHECKS], default="all")
    args = parser.parse_args()
    selected = CHECKS if args.quick == "all" else {args.quick: CHECKS[args.quick]}
    for check in selected.values():
        check()
    print(f"Reproduction checks passed: {len(selected)} package(s). This is not independent replication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
