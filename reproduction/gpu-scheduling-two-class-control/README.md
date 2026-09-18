# Two-class strict-FCFS known control (EP-0023)

This small synthetic instance maps the known two-class stability theorem to 64
homogeneous resources, needs 32/64 with probability 1/2 each, and class service
rates 1 and 1/2. Its exact five-state saturated chain has throughput 8/11 jobs
per time, so the nominal resource-load boundary is 10/11. The theorem, not a
simulation trend or the diagnostic being tested, supplies the noncritical label.
See [author manuscript, Theorems 4.2/4.3](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf).

```sh
python -m pip install numpy scipy
python rerun_two_class.py --verify-recorded
python rerun_two_class.py --seeds 10 --horizons 20000 80000 --output rerun.json
python rerun_two_class.py --seeds 100 --horizons 20000 80000 --output full.json
```

The first command checks exact algebra, recorded counts/intervals/losses and
regenerates ten small runs (two seeds by five loads). The last reconstructs the
500-workload, 4000-decision grid. Seed is the repetition unit; the two looks are
nested prefixes. summary.json includes the 1000 seed-look scalar records and
ten cells, not a recorded input trace. All inputs are regenerated from seeds.

Information contracts differ: O_AB observes arrivals/departures through cutoff;
D_ALPHA waits for the cohort to drain, using H/2 versus H JCT elasticity with
20% warmup and threshold .5; K_EXACT knows population class/service parameters
and exact capacity but estimates arrival rate from H exponential gaps. Its
95% chi-square interval uses 2 lambda T_H ~ chi2(2H). NOMINAL_WORK ignores HOL
and compares lambda_hat E[block work]/2 to one. No F-work interval is transferred
to the mixture. AB restores the printed WSC2003 specification using sample
variance; its nominal alpha .05 is not a proven finite-window error guarantee.

Seed-rate CP intervals split family alpha .05 over 80 wrong/UNKNOWN rates.
Input intervals use per-decision alpha .05, a different uncertainty statement.
Loss is e+a u at fixed a=.1/.5/.9. Crossover prices are conditional on benchmark
truth; they are not an online policy for unknown truth. Known population
parameters privilege K, so this does not establish a cross-information ranking.
future_work_share counts service work, not GPU-weighted resource work.

v10 failed representation preflight before any fixture/grid observation; v11
normalized tuples to lists and re-sealed unchanged seeds/model/predictions.
Timestamps and hashes are local, not externally authenticated preregistration.
Recorded native alignment is disclosed; this package regenerates the causal
FCFS oracle, not the private native engine. It demonstrates same-code execution,
not external independent replication, novel queueing theory, general mixed-need
capacity, real GPU validation or operational benefit. No personal paths or
private repository imports are required.

The public summary also discloses the original M0-M4 prediction thresholds and
stop rule; the verification command recalculates all five grades. The original
private protocol digest is provenance only: this curated public summary is not
the byte stream to which that digest was sealed.
