"""Resource-pooled SRPT: the lower-bound reference used by Grosof et al.

All server-need constraints are removed. One super-server of speed n_servers
processes total work k_j * S_j per job under preemptive SRPT. No MSJ policy can
beat this, so it is the instrument check on the main engine.
"""
import heapq
import numpy as np


def simulate_pooled(jobs, n_servers, warmup_frac=0.2):
    n = len(jobs)
    work = [j.need * j.size for j in jobs]
    resp = np.full(n, np.nan)
    heap = []                        # (remaining_work, jid)
    t = 0.0
    idx = 0
    while idx < n or heap:
        if heap:
            rem, jid = heap[0]
            t_done = t + rem / n_servers
            t_arr = jobs[idx].arrival if idx < n else np.inf
            if t_arr < t_done:
                served = (t_arr - t) * n_servers
                heapq.heapreplace(heap, (rem - served, jid))
                t = t_arr
                heapq.heappush(heap, (work[idx], idx))
                idx += 1
            else:
                heapq.heappop(heap)
                t = t_done
                resp[jid] = t - jobs[jid].arrival
        else:
            t = max(t, jobs[idx].arrival)
            heapq.heappush(heap, (work[idx], idx))
            idx += 1

    m0 = int(n * warmup_frac)
    r = resp[m0:]
    r = r[~np.isnan(r)]
    return {"mean_jct": float(r.mean()), "p99_jct": float(np.percentile(r, 99)),
            "n": len(r)}
