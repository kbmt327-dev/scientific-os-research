"""Server assignment for the heterogeneous / topology-aware MSJ cluster.

The policies in sim/policies.py decide WHICH jobs run; they only count servers.
This module decides WHICH servers each running job gets. That is a separate
decision, and it is the one heterogeneity and locality act through: in the
homogeneous fungible-server model the assignment cannot matter, so it was never
represented.

Two modelling commitments, both stated so they can be attacked:

1. A gang job runs at the speed of its SLOWEST assigned server. This is the
   synchronous data-parallel model: every worker waits at the step barrier, so
   one slow GPU paces the whole gang. It is what makes heterogeneity bite; an
   additive-throughput model would make it nearly free.

2. Placement is STICKY. A job that keeps running keeps its servers. Migration
   is not free in a real cluster, and stickiness is what lets fragmentation
   accumulate across epochs instead of being re-optimised away every event.

Feasibility is never at stake here. The policy already guarantees
sum(need) <= n_servers, and any `need` free servers can host a job, so
placement changes a job's RATE, never its admission. A model where
fragmentation blocks admission is a different model and is not this one.
"""
import numpy as np


# ------------------------------------------------------------- speed layouts
def speed_layout(n_servers, ratio, fast_frac=0.5, layout="blocked"):
    """Two-speed cluster with max/min speed = `ratio`, normalised so that the
    ARITHMETIC MEAN speed is exactly 1.0 at every ratio.

    Normalising the mean keeps one thing fixed across the sweep, but it does
    NOT keep capacity fixed: under the slowest-server rule the usable capacity
    falls as the ratio grows. That drop is measured separately by saturated
    throughput and must be divided out before any queueing claim is made.
    """
    n_fast = int(round(n_servers * fast_frac))
    n_slow = n_servers - n_fast
    # s_fast / s_slow = ratio, (n_fast*s_fast + n_slow*s_slow) / n = 1
    s_slow = n_servers / (n_fast * ratio + n_slow)
    s_fast = s_slow * ratio
    speeds = np.full(n_servers, s_slow, dtype=float)
    if layout == "blocked":
        speeds[:n_fast] = s_fast
    elif layout == "interleaved":
        # Spread the SLOW servers as evenly as possible over the index range,
        # for any fast_frac. A stride of 2 only works at fast_frac = 0.5 and
        # silently under-assigns above it, which would have made `first_fit`
        # look speed-aware again -- the confound this layout exists to remove.
        if n_slow:
            pos = np.unique(np.round(
                np.linspace(0, n_servers - 1, n_slow)).astype(int))
            while len(pos) < n_slow:
                extra = np.setdiff1d(np.arange(n_servers), pos)
                pos = np.union1d(pos, extra[:n_slow - len(pos)])
            speeds[:] = s_fast
            speeds[pos] = s_slow
        else:
            speeds[:] = s_fast
    elif layout == "random":
        rng = np.random.default_rng(20260914)
        take = rng.choice(n_servers, size=n_fast, replace=False)
        speeds[take] = s_fast
    else:
        raise ValueError(f"unknown layout {layout}")
    assert abs(float(speeds.mean()) - 1.0) < 1e-9, speeds.mean()
    return speeds


# --------------------------------------------------------------- rate model
def excess_nodes(servers, node_size):
    """Nodes spanned beyond the minimum ceil(need / node_size)."""
    n_nodes = len({i // node_size for i in servers})
    return n_nodes - -(-len(servers) // node_size)


def gang_rate(servers, speeds, node_size=None, cross_node_penalty=0.0,
              penalty_mode="all"):
    """Progress rate of a gang placed on `servers` (indices).

    penalty_mode="all" charges every node after the first, so a gang that must
    span several nodes pays even when perfectly placed. "excess" charges only
    nodes beyond ceil(need / node_size): job sizes are then read as measured
    under ideal placement, and the penalty is the cost of fragmentation alone.
    """
    r = float(min(speeds[i] for i in servers))
    if node_size and cross_node_penalty:
        if penalty_mode == "excess":
            extra = excess_nodes(servers, node_size)
        elif penalty_mode == "all":
            extra = len({i // node_size for i in servers}) - 1
        else:
            raise ValueError(f"unknown penalty_mode {penalty_mode}")
        r /= (1.0 + cross_node_penalty * extra)
    return r


# ------------------------------------------------------------------ choosers
def _first_fit(free, need, speeds, node_size):
    return free[:need]


def _fastest(free, need, speeds, node_size):
    """Greedy-optimal for the job at hand: take the fastest free servers, which
    maximises this gang's min speed. Every such choice takes a fast server away
    from some later job."""
    return sorted(free, key=lambda i: (-speeds[i], i))[:need]


def _slowest(free, need, speeds, node_size):
    """The opposite reservation instinct: run on the slowest servers that will
    do, keeping the fast ones free. Included so that `fastest` is compared with
    something, not with nothing."""
    return sorted(free, key=lambda i: (speeds[i], i))[:need]


def _uniform(free, need, speeds, node_size):
    """Heterogeneity-aware: among free servers sorted by speed, take the window
    of `need` consecutive servers whose MINIMUM is highest -- i.e. the fastest
    feasible set -- but break ties toward a tight speed band so that fast
    servers are not wasted padding a gang whose floor is already slow.

    With `need` servers required, the fastest set and the tightest band are the
    same window here; the function differs from `_fastest` only in its tie
    order, and exists to make that explicit rather than accidental.
    """
    order = sorted(free, key=lambda i: (-speeds[i], i))
    win = order[:need]
    floor = speeds[win[-1]]
    # among free servers no faster than is useful, prefer the slowest that
    # still match the floor, so genuinely faster servers stay free
    usable = [i for i in order if speeds[i] >= floor - 1e-12]
    return sorted(usable, key=lambda i: (speeds[i], i))[:need]


def _compact(free, need, speeds, node_size):
    """Locality-aware: minimise the number of nodes the gang spans, preferring
    nodes that are already the most occupied (best fit), so that whole nodes
    stay free for gangs that need them."""
    if not node_size:
        return _first_fit(free, need, speeds, node_size)
    by_node = {}
    for i in free:
        by_node.setdefault(i // node_size, []).append(i)
    # best fit: fullest nodes first (fewest free servers), then node index
    order = sorted(by_node, key=lambda nd: (len(by_node[nd]), nd))
    # a gang that needs whole nodes should get the emptiest ones instead
    if need >= node_size:
        order = sorted(by_node, key=lambda nd: (-len(by_node[nd]), nd))
    out = []
    for nd in order:
        for i in by_node[nd]:
            out.append(i)
            if len(out) == need:
                return out
    return out


PLACEMENTS = {
    "first_fit": _first_fit,
    "fastest": _fastest,
    "slowest": _slowest,
    "uniform": _uniform,
    "compact": _compact,
}
