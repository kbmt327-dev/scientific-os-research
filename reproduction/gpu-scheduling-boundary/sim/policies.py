"""Scheduling policies for the MSJ cluster.

Every policy implements
    select(waiting, running, n_servers, now) -> list of jobs that should run
Non-preemptive policies must include every currently running job in the result.
`waiting` is ordered by arrival time (FCFS order).
"""


def _free(running, n_servers):
    return n_servers - sum(j.need for j in running)


# ---------------------------------------------------------------- FCFS (gang)
def fcfs(waiting, running, n_servers, now):
    """Strict FCFS with head-of-line blocking. Non-preemptive."""
    sel = list(running)
    free = _free(running, n_servers)
    for j in waiting:
        if j.need <= free:
            sel.append(j)
            free -= j.need
        else:
            break
    return sel


# ------------------------------------------------------- FCFS + EASY backfill
def easy_backfill(waiting, running, n_servers, now):
    """EASY backfilling: the head job gets a reservation computed from
    estimated remaining times; later jobs may run if they do not push that
    reservation back. Non-preemptive. Uses estimates only."""
    sel = list(running)
    free = _free(running, n_servers)
    if not waiting:
        return sel

    # start whatever fits in FCFS order until the head blocks
    idx = 0
    while idx < len(waiting) and waiting[idx].need <= free:
        sel.append(waiting[idx])
        free -= waiting[idx].need
        idx += 1
    if idx >= len(waiting):
        return sel

    head = waiting[idx]

    # reservation time for head: walk estimated completions of active jobs
    active = [(now + j.est_remaining(), j.need) for j in sel]
    active.sort()
    avail = free
    t_res = now
    freed_by = []            # (time, need) of jobs freeing servers before t_res
    for t_end, need in active:
        if avail >= head.need:
            break
        avail += need
        t_res = t_end
        freed_by.append((t_end, need))
    if avail < head.need:
        return sel           # cannot even reserve; nothing to backfill against

    # servers still occupied at t_res (strictly after it) by already-active jobs
    occupied_at_res = sum(n for t_end, n in active if t_end > t_res)
    slack_at_res = n_servers - occupied_at_res - head.need

    for j in waiting[idx + 1:]:
        if j.need > free:
            continue
        ends_before_res = now + j.est_remaining() <= t_res
        if ends_before_res or j.need <= slack_at_res:
            sel.append(j)
            free -= j.need
            if not ends_before_res:
                slack_at_res -= j.need
    return sel


# -------------------------------------------------------------- SRPT (greedy)
def _srpt_order(waiting, running):
    jobs = list(running) + list(waiting)
    jobs.sort(key=lambda j: (j.est_remaining(), j.arrival, j.jid))
    return jobs


def srpt_greedy(waiting, running, n_servers, now):
    """Preemptive SRPT priority with greedy packing: walk jobs in SRPT order
    and run each one that still fits (skipping those that do not)."""
    cap = n_servers
    sel = []
    for j in _srpt_order(waiting, running):
        if j.need <= cap:
            sel.append(j)
            cap -= j.need
        if cap == 0:
            break
    return sel


def srpt_nonpreempt(waiting, running, n_servers, now):
    """SRPT priority among waiting jobs only; running jobs are never preempted."""
    sel = list(running)
    cap = _free(running, n_servers)
    order = sorted(waiting, key=lambda j: (j.est_remaining(), j.arrival, j.jid))
    for j in order:
        if j.need <= cap:
            sel.append(j)
            cap -= j.need
        if cap == 0:
            break
    return sel


# ------------------------------------------------------- ServerFilling-SRPT
def server_filling_srpt(waiting, running, n_servers, now):
    """ServerFilling-SRPT (Grosof et al.). Take the shortest prefix of the
    SRPT-ordered job list whose total server need reaches n_servers, then fill
    the servers exactly by taking that prefix in decreasing order of need.
    Requires powers-of-two needs and a power-of-two server count, and requires
    preemption."""
    order = _srpt_order(waiting, running)
    cum = 0
    prefix = []
    for j in order:
        prefix.append(j)
        cum += j.need
        if cum >= n_servers:
            break
    if cum < n_servers:
        return prefix                      # everything fits, run it all

    cap = n_servers
    sel = []
    for j in sorted(prefix, key=lambda j: (-j.need, j.est_remaining(), j.jid)):
        if j.need <= cap:
            sel.append(j)
            cap -= j.need
        if cap == 0:
            break
    return sel


def server_filling_fcfs(waiting, running, n_servers, now):
    """ServerFilling with FCFS priority (isolates the filling mechanism from
    the size-based priority)."""
    order = list(running) + list(waiting)
    order.sort(key=lambda j: (j.arrival, j.jid))
    cum = 0
    prefix = []
    for j in order:
        prefix.append(j)
        cum += j.need
        if cum >= n_servers:
            break
    if cum < n_servers:
        return prefix
    cap = n_servers
    sel = []
    for j in sorted(prefix, key=lambda j: (-j.need, j.arrival, j.jid)):
        if j.need <= cap:
            sel.append(j)
            cap -= j.need
        if cap == 0:
            break
    return sel


POLICIES = {
    "fcfs": (fcfs, False),
    "easy_backfill": (easy_backfill, False),
    "srpt_np": (srpt_nonpreempt, False),
    "srpt": (srpt_greedy, True),
    "sf_srpt": (server_filling_srpt, True),
    "sf_fcfs": (server_filling_fcfs, True),
}
