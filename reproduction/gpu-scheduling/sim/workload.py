"""Workload generation for the multiserver-job (MSJ) cluster model.

A job occupies `need` servers simultaneously for `size` units of time
(gang scheduling). This is the MSJ model of Grosof et al., which is the
mathematical form of gang-scheduled GPU jobs.
"""
from dataclasses import dataclass, field
import numpy as np

# Roughly trace-shaped: 1-GPU jobs dominate with a tail of large gang jobs.
# All needs are powers of two so that ServerFilling is applicable.
DEFAULT_NEEDS = (1, 2, 4, 8, 16, 32)
DEFAULT_NEED_PROBS = (0.50, 0.20, 0.15, 0.10, 0.04, 0.01)


@dataclass
class Job:
    jid: int
    arrival: float
    need: int
    size: float               # true total service time (ground truth)
    est_total: float          # scheduler-visible estimate of total service time
    remaining: float = 0.0    # true remaining work
    attained: float = 0.0     # service time already received
    lost: float = 0.0         # work destroyed by preemptions
    start: float = -1.0
    completion: float = -1.0
    n_preempt: int = 0
    running: bool = False

    def est_remaining(self) -> float:
        # The scheduler knows attained service exactly but only estimates the
        # total, so an overrunning job's estimated remaining collapses to 0.
        return max(self.est_total - self.attained, 0.0)


def expected_need(needs=DEFAULT_NEEDS, probs=DEFAULT_NEED_PROBS) -> float:
    return float(np.dot(needs, probs))


def lognormal_from_cv(mean: float, cv: float, size, rng):
    """Lognormal samples with given mean and coefficient of variation."""
    sigma2 = np.log(1.0 + cv * cv)
    mu = np.log(mean) - 0.5 * sigma2
    return rng.lognormal(mu, np.sqrt(sigma2), size)


def make_workload(
    n_jobs: int,
    rho: float,
    n_servers: int,
    seed: int,
    needs=DEFAULT_NEEDS,
    need_probs=DEFAULT_NEED_PROBS,
    dur_mean: float = 1.0,
    dur_cv: float = 1.0,
    sigma: float = 0.0,
    est_bias: float = 1.0,
):
    """Generate a Poisson arrival stream of MSJ jobs.

    rho   : offered load = lam * E[need * size] / n_servers
    sigma : multiplicative lognormal noise on the size estimate.
            est = size * bias * exp(sigma*Z - sigma^2/2)  (mean-unbiased at bias=1)
    """
    rng = np.random.default_rng(seed)
    e_need = float(np.dot(needs, need_probs))
    lam = rho * n_servers / (e_need * dur_mean)

    gaps = rng.exponential(1.0 / lam, n_jobs)
    arrivals = np.cumsum(gaps)
    need = rng.choice(needs, size=n_jobs, p=need_probs)

    if abs(dur_cv - 1.0) < 1e-12:
        size = rng.exponential(dur_mean, n_jobs)
    else:
        size = lognormal_from_cv(dur_mean, dur_cv, n_jobs, rng)

    if sigma > 0.0:
        z = rng.standard_normal(n_jobs)
        est = size * est_bias * np.exp(sigma * z - 0.5 * sigma * sigma)
    else:
        est = size * est_bias

    jobs = [
        Job(jid=i, arrival=float(arrivals[i]), need=int(need[i]),
            size=float(size[i]), est_total=float(est[i]), remaining=float(size[i]))
        for i in range(n_jobs)
    ]
    return jobs, lam
