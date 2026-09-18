"""Bounded diagnostic definitions; AB uses a disclosed sample-variance interpretation."""
import math
import numpy as np
from scipy.stats import t as student_t, beta

def occupancy_integral(arrival, dep, t0, t1):
    return float(np.maximum(0.0, np.minimum(dep, t1) - np.maximum(arrival, t0)).sum())

def algorithm_ab(arrival, dep, tau, batches, alpha):
    width = tau / batches
    obs = np.array([occupancy_integral(arrival, dep, (j - 1) * width, j * width) / width
                    for j in range(2, batches + 1)])
    growth = float(obs[-1] - obs[0])
    variance = float(np.sum((obs - obs.mean()) ** 2) / (batches - 2))
    literal = float((np.sum(obs ** 2) - batches * growth ** 2) / (batches - 2))
    critical = float(student_t.ppf(1 - alpha, batches - 2))
    degenerate = not (variance > 0) or not math.isfinite(variance)
    if degenerate:
        label, statistic = ('overloaded' if growth > 0 else 'subcritical'), None
    else:
        statistic = growth / (math.sqrt(2) * math.sqrt(variance))
        label = 'overloaded' if statistic > critical else 'subcritical'
    return dict(growth=growth, batch_variance=variance, literal_variance=literal,
                literal_variance_negative=bool(literal < 0), statistic=statistic,
                critical=critical, degenerate=bool(degenerate), label=label)

def window_elasticity(arrival, dep, horizon, ratio, warmup, threshold):
    def cohort_mean(k):
        start = int(warmup * k)
        return float(np.mean(dep[start:k] - arrival[start:k]))
    small = cohort_mean(max(2, int(horizon / ratio)))
    large = cohort_mean(horizon)
    if not (small > 0 and large > 0):
        raise RuntimeError('nonpositive cohort mean JCT')
    alpha = (math.log(large) - math.log(small)) / math.log(ratio)
    return dict(mean_jct_small=small, mean_jct_large=large, alpha=float(alpha),
                label='overloaded' if alpha >= threshold else 'subcritical')

def clopper_pearson(x, m, error):
    low = float(beta.ppf(error / 2, x, m - x + 1)) if x > 0 else 0.0
    high = float(beta.ppf(1 - error / 2, x + 1, m - x)) if x < m else 1.0
    return low, high
