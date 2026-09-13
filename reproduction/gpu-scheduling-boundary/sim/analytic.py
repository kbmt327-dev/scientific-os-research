"""Closed-form references used to check the simulator (not for the study)."""
import math


def erlang_c(c: int, a: float) -> float:
    """Probability of waiting in M/M/c with offered load a = lam/mu, rho = a/c."""
    rho = a / c
    if rho >= 1.0:
        return 1.0
    s = sum(a ** k / math.factorial(k) for k in range(c))
    last = a ** c / math.factorial(c)
    return last / (1 - rho) / (s + last / (1 - rho))


def mmc(lam: float, mu: float, c: int):
    """Mean wait and mean response time for M/M/c."""
    a = lam / mu
    rho = a / c
    pw = erlang_c(c, a)
    wq = pw / (c * mu - lam)
    return {"rho": rho, "p_wait": pw, "mean_wait": wq, "mean_jct": wq + 1.0 / mu}
