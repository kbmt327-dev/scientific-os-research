"""Discrete-event engine for the multiserver-job (MSJ) cluster.

Decision epochs are arrivals and departures only. Preemption charges a fixed
restart overhead c_pre * E[S] of extra work, which the scheduler is aware of
(est_total grows by the same amount): checkpoint/restart semantics with a
progress-independent overhead.

Two measurement decisions matter and are deliberate:

1. Time averages (utilization, backlog) are accumulated over
   [warmup boundary, last arrival] only. Including the drain phase after the
   last arrival dilutes utilization and hides divergence.
2. Stability is NOT inferred from a single open-arrival run. After the arrival
   stream ends any finite system drains, so a diverging run still completes
   every job (a completion-based detector calls it stable), while
   `utilization < offered load` also fires for a long transient in a stable
   system. rho_max is therefore measured separately as saturated throughput
   (calib/c05) and `backlog_growing` is only a diagnostic here. Both detector
   errors were found in calibration, not assumed away.
"""
import numpy as np

from .placement import PLACEMENTS, excess_nodes, gang_rate
from .policies import POLICIES

EPS = 1e-9


def simulate(jobs, n_servers, policy_name, c_pre=0.0, dur_mean=1.0,
             warmup_frac=0.2, t_limit_factor=50.0, backlog_cap=None,
             saturated=False, server_speeds=None, placement="first_fit",
             node_size=None, cross_node_penalty=0.0, penalty_mode="all"):
    """saturated=True: treat the whole run as a saturation experiment (used to
    measure a policy's rho_max as its saturated throughput).

    server_speeds / node_size / cross_node_penalty turn on the heterogeneous
    engine (sim/placement.py). When both server_speeds and node_size are None
    the heterogeneous path is skipped entirely and every job runs at rate 1.0,
    which reproduces the homogeneous engine exactly -- calib/c08 asserts that
    equality run-for-run rather than assuming it.
    """
    policy, preemptive = POLICIES[policy_name]
    het = server_speeds is not None or node_size is not None
    if het:
        speeds = (np.ones(n_servers) if server_speeds is None
                  else np.asarray(server_speeds, dtype=float))
        assert len(speeds) == n_servers
        choose = PLACEMENTS[placement]
        free_set = set(range(n_servers))
        n_placements = 0
        excess_total = 0
    c_pre_abs = c_pre * dur_mean
    n = len(jobs)
    aborted = False

    active = []            # arrived, incomplete jobs, in arrival order
    running = []
    t = 0.0
    next_idx = 0
    completed = 0
    n_preempt_total = 0
    t_last_arr = jobs[-1].arrival
    if saturated:
        # Every job arrives at t = 0 in a saturation run, so t_last_arr is 0
        # and `t_last_arr * t_limit_factor + 1.0` collapses to 1.0 NO MATTER
        # what t_limit_factor is. Every saturation run in this repo therefore
        # stopped after one mean service time, having completed 32 of 4000
        # jobs under fcfs against 654 under srpt, and reported the work done
        # in that first instant as though it were capacity. Utilization read
        # ~1.0 throughout, which is why it looked healthy. Found in EP-0015;
        # it invalidated calib/c05, calib/c08 E4 and calib/c09.
        #
        # Total work is the only timescale a saturation run has, so scale by
        # that instead.
        total_work = sum(j.need * j.size for j in jobs) / n_servers
        t_limit = t_limit_factor * total_work + 1.0
    else:
        t_limit = t_last_arr * t_limit_factor + 1.0
    # A saturation run stops being saturated the moment nothing is waiting;
    # after that it is draining a burst, and averaging over the tail deflates
    # the throughput. Areas are accumulated only while the queue is backed up.
    sat_open = True
    t_queue_empty = -1.0

    measure_from_jid = int(n * warmup_frac)
    t_meas = jobs[measure_from_jid].arrival
    busy_area = 0.0
    running_area = 0.0
    backlog_area = 0.0
    bl_t, bl_n = [], []

    while completed < n and t < t_limit:
        if not running:
            t_dep = np.inf
        elif het:
            t_dep = t + min(j.remaining / j.rate for j in running)
        else:
            t_dep = t + min(j.remaining for j in running)
        t_arr = jobs[next_idx].arrival if next_idx < n else np.inf
        t_next = min(t_dep, t_arr)
        if t_next == np.inf:
            break

        # time averages over [t_meas, t_last_arr] only
        hi = t_next if saturated else min(t_next, t_last_arr)
        dt_meas = hi - max(t, t_meas)
        if saturated and not sat_open:
            dt_meas = 0.0
        if dt_meas > 0:
            busy_area += sum(j.need for j in running) * dt_meas
            backlog_area += len(active) * dt_meas
            running_area += len(running) * dt_meas
        dt = t_next - t
        if dt > 0:
            for j in running:
                # attained counts WORK done, not wall time, so a job placed on
                # slow servers is not mistaken by est_remaining() for one that
                # has made progress.
                w = dt * j.rate if het else dt
                j.remaining -= w
                j.attained += w
        t = t_next

        if t_dep <= t_arr + EPS and running:
            done = [j for j in running if j.remaining <= EPS]
            if done:
                done_ids = {id(j) for j in done}
                for j in done:
                    j.completion = t
                    j.running = False
                    completed += 1
                    if het and j.servers:
                        free_set |= set(j.servers)
                        j.servers = ()
                running = [j for j in running if id(j) not in done_ids]
                active = [j for j in active if id(j) not in done_ids]
        if t_arr <= t_dep + EPS and next_idx < n:
            while next_idx < n and jobs[next_idx].arrival <= t + EPS:
                active.append(jobs[next_idx])
                next_idx += 1

        if saturated and sat_open and len(active) == len(running):
            sat_open = False
            t_queue_empty = t

        if t_meas <= t <= t_last_arr:
            bl_t.append(t)
            bl_n.append(len(active))

        if backlog_cap is not None and len(active) > backlog_cap:
            aborted = True
            break

        waiting = [j for j in active if not j.running]
        sel = policy(waiting, running, n_servers, t)
        sel_ids = {id(j) for j in sel}
        assert len(sel_ids) == len(sel), "policy selected a job twice"
        assert sum(j.need for j in sel) <= n_servers, "policy overcommitted servers"

        if preemptive:
            for j in running:
                if id(j) not in sel_ids:
                    j.running = False
                    j.n_preempt += 1
                    n_preempt_total += 1
                    if c_pre_abs > 0.0:
                        j.remaining += c_pre_abs
                        j.est_total += c_pre_abs
                        j.lost += c_pre_abs
        else:
            for j in running:
                assert id(j) in sel_ids, "non-preemptive policy dropped a running job"

        if het:
            sel_ids2 = {id(j) for j in sel}
            for j in running:
                if id(j) not in sel_ids2 and j.servers:
                    free_set |= set(j.servers)
                    j.servers = ()
            for j in sel:
                if not j.servers:
                    got = choose(sorted(free_set), j.need, speeds, node_size)
                    assert len(got) == j.need, "placement returned wrong count"
                    j.servers = tuple(got)
                    free_set -= set(got)
                    j.rate = gang_rate(got, speeds, node_size,
                                       cross_node_penalty, penalty_mode)
                    if node_size:
                        n_placements += 1
                        excess_total += excess_nodes(got, node_size)
        for j in sel:
            if not j.running:
                j.running = True
                if j.start < 0:
                    j.start = t
        running = list(sel)

    t_sat_end = t_queue_empty if (saturated and t_queue_empty > 0) else t
    span = max((t_sat_end if saturated else t_last_arr) - t_meas, 1e-12)
    out = _metrics(jobs, n_servers, t_sat_end if saturated else t, span,
                   measure_from_jid, busy_area, backlog_area, n_preempt_total,
                   completed, bl_t, bl_n, t_meas, t_last_arr, saturated,
                   running_area)
    if saturated:
        out["t_queue_empty"] = t_queue_empty
        out["t_run_end"] = t
    if het:
        if node_size:
            out["n_placements"] = n_placements
            out["excess_nodes_per_placement"] = excess_total / max(n_placements, 1)
        meas = [j for j in jobs if j.jid >= measure_from_jid and j.start >= 0]
        if meas:
            out["mean_gang_rate"] = float(np.mean([j.rate for j in meas]))
            by = {}
            for j in meas:
                by.setdefault(j.need, []).append(j.rate)
            out["gang_rate_by_need"] = {int(k): float(np.mean(v))
                                        for k, v in sorted(by.items())}
    out["aborted_backlog"] = aborted
    out["hit_time_limit"] = (t >= t_limit)
    if aborted or out["hit_time_limit"]:
        out["unstable"] = True
    return out


def _metrics(jobs, n_servers, t_end, span, measure_from_jid, busy_area,
             backlog_area, n_preempt_total, completed, bl_t, bl_n,
             t_meas, t_last_arr, saturated, running_area=0.0):
    meas = [j for j in jobs if j.jid >= measure_from_jid]
    done = [j for j in meas if j.completion >= 0]
    resp = np.array([j.completion - j.arrival for j in done])
    slowdown = np.array([(j.completion - j.arrival) / j.size for j in done])
    wait = np.array([j.start - j.arrival for j in done if j.start >= 0])

    # empirical offered load over the same window the time averages use
    win = [j for j in jobs if t_meas <= j.arrival <= t_last_arr]
    rho_emp = sum(j.need * j.size for j in win) / (n_servers * max(t_last_arr - t_meas, 1e-12))
    util = busy_area / (n_servers * span)

    # Server occupancy stops measuring capacity as soon as servers differ in
    # speed: a cluster can be 100 percent occupied and still be doing less
    # work, because a gang runs at its slowest member's speed. `goodput` is the
    # useful work (need * size) finished inside the same window, per server per
    # unit time. Under homogeneity the two agree; under heterogeneity goodput
    # is the one that means capacity. Registered in calib/c07.
    t_hi = t_end if saturated else t_last_arr
    work_done = sum(j.need * j.size for j in meas
                    if t_meas <= j.completion <= t_hi)
    goodput = work_done / (n_servers * span)

    out = {
        "n_measured": len(meas),
        "n_completed": len(done),
        "completion_frac": len(done) / max(len(meas), 1),
        "mean_jct": float(resp.mean()) if len(resp) else float("nan"),
        "p99_jct": float(np.percentile(resp, 99)) if len(resp) else float("nan"),
        "mean_slowdown": float(slowdown.mean()) if len(slowdown) else float("nan"),
        "p99_slowdown": float(np.percentile(slowdown, 99)) if len(slowdown) else float("nan"),
        "mean_wait": float(wait.mean()) if len(wait) else float("nan"),
        "max_wait": float(wait.max()) if len(wait) else float("nan"),
        "utilization": float(util),
        "goodput": float(goodput),
        "rho_emp": float(rho_emp),
        "util_over_rho": float(util / rho_emp) if rho_emp > 0 else float("nan"),
        "mean_backlog": backlog_area / span,
        "mean_running": running_area / span,
        "preempts_per_job": n_preempt_total / max(len(jobs), 1),
        "lost_work_frac": float(sum(j.lost for j in jobs) / sum(j.size for j in jobs)),
        "t_end": t_end,
        "all_completed": completed == len(jobs),
    }

    by_need = {}
    for j in done:
        by_need.setdefault(j.need, []).append(j.completion - j.arrival)
    out["jct_by_need"] = {int(k): float(np.mean(v)) for k, v in sorted(by_need.items())}
    n_arr = {}
    for j in meas:
        n_arr[j.need] = n_arr.get(j.need, 0) + 1
    out["completion_frac_by_need"] = {
        int(k): len(by_need.get(k, [])) / n_arr[k] for k in sorted(n_arr)}

    # Per-class flow balance inside the arrival window. A class whose queue is
    # growing completes fewer jobs than arrive while arrivals are still on, no
    # matter how long the post-arrival drain later takes. This separates a
    # starving class (real instability of that class) from a long transient,
    # which util_over_rho alone cannot do (EP-0001 lesson M-6).
    arr_w, done_w = {}, {}
    for j in meas:
        if t_meas <= j.arrival <= t_last_arr:
            arr_w[j.need] = arr_w.get(j.need, 0) + 1
        if 0 <= j.completion <= t_last_arr and j.arrival >= t_meas:
            done_w[j.need] = done_w.get(j.need, 0) + 1
    # A class needs enough arrivals in the window for the ratio to mean
    # anything. The guard was 20; it is 8 because a rare whole-cluster class
    # (p=0.0005 of 30k jobs = 15 arrivals) is exactly the case of interest, and
    # 0 completions out of 15 is already an unambiguous starvation signal.
    out["flow_balance_by_need"] = {
        int(k): done_w.get(k, 0) / arr_w[k] for k in sorted(arr_w) if arr_w[k] >= 8}
    out["n_arrivals_by_need"] = {int(k): v for k, v in sorted(arr_w.items())}
    fb = out["flow_balance_by_need"]
    out["min_flow_balance"] = float(min(fb.values())) if fb else float("nan")
    out["starving_needs"] = [k for k, v in fb.items() if v < 0.5]
    jbn = out["jct_by_need"]
    out["jct_spread_by_need"] = (float(max(jbn.values()) / min(jbn.values()))
                                 if jbn else float("nan"))

    # backlog growth over the arrival window
    if len(bl_t) > 100:
        a, b = np.polyfit(np.asarray(bl_t), np.asarray(bl_n, dtype=float), 1)
        out["backlog_slope"] = float(a)
        k = len(bl_n) // 10
        out["backlog_first_decile"] = float(np.mean(bl_n[:k]))
        out["backlog_last_decile"] = float(np.mean(bl_n[-k:]))
    else:
        out["backlog_slope"] = float("nan")
        out["backlog_first_decile"] = float("nan")
        out["backlog_last_decile"] = float("nan")

    # util < offered load means the backlog grew over the window. That happens
    # both for a diverging system AND for a long transient in a stable one, so
    # it is reported as a diagnostic, not as proof of instability. rho_max is
    # measured separately by saturation (calib/c05).
    out["backlog_growing"] = bool(out["util_over_rho"] < 0.995)
    out["unstable"] = False if saturated else bool(out["completion_frac"] < 0.98)
    return out
