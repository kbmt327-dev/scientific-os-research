---
research_id: GPU-SCHED-EP-0019
title: A small overload remained unresolved within a finite window
date: '2026-09-17'
lang: en
domain: GPU Cluster Scheduling
type: Negative Result
status: Finite-window UNKNOWN; general detector unvalidated
evidence_level: Synthetic known-model controls
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-known-control
  source: 51 input/oracle workloads, 17 CI comparisons; public sufficient-statistic CI arithmetic only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Known full-gang M/M/1; homogeneous FCFS; independent exponential inputs; true required work accessible; no mixed-need or real-cluster capacity claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0019
source_episode_sha256: 772e57cdb1532f4aa047b32cda13fb04fe9e7d36d3272360ddd1106f34daf320
publication:
  status: publishable
tags:
- negative-result
- gpu-scheduling
- known-controls
- uncertainty
- en
aliases:
- /research/gpu-scheduling-drift-uncertainty/index
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Known controls and finite-window uncertainty</span><a href="/ja/research/gpu-scheduling-drift-uncertainty/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Negative Result</span><span>Synthetic known model</span><span>Capacity UNKNOWN</span><span>No peer review</span><span>Independent replications 0</span></div>

## Current finding

**An input-drift confidence interval resolved three holdout cells correctly and left a smaller overload UNKNOWN.** At rho=1.005, even 320k jobs per seed across three seeds gave a load interval of [0.998880,1.008229], spanning capacity 1. Execution stopped at the first maximum-window UNKNOWN.

This did not detect that overload. It avoided forcing unresolved evidence into a stable label. The check needs exponential inputs, all jobs' true required work and known unit capacity; it does not validate a general MSJ detector.

## Research question

Can input-drift uncertainty replace the midpoint miss in [[en/research/gpu-scheduling-known-controls/index|EP-0018]], distinguish known labels near the boundary and return UNKNOWN when the finite window cannot resolve them?

## Why this matters

Small growth and no growth may be indistinguishable with the available data. Counting abstention as no growth turns detector uncertainty into a stability claim.

## Method

The known full-gang M/M/1 case was retained. Calibration used rho=0.97/1.03 and seeds 601/602/603. Ordered holdout loads were 0.99/1.01/0.995/1.005/0.999/1.001 with separate seeds 701/702/703. Horizons were fixed at 20k/40k/80k/160k/320k. Calibration checked acceptance; it did not fit a threshold.

All input service work B and arrival gap time T were pooled across three seeds. R=B/T estimates load, with n=3H. Under mutually independent iid exponential inputs, R/rho follows F(2n,2n), giving CI=[R/q_high,R/q_low]. Applying the [established F law](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html) to these sufficient statistics is a model-specific inference, not a new theorem.

Each of the 40 potential comparisons (8 cells by 5 windows) receives delta=0.05/40. A union bound limits the probability of any wrong declared side to 5% under that model, including dependent windows and stopping. This is not a real-cluster error rate, an abstention-rate guarantee or an empirical guarantee derived from zero errors in this run.

An upper endpoint below 1 declares subcritical; a lower endpoint above 1 declares overloaded; otherwise the label is UNKNOWN. Intermediate UNKNOWN advances to the next fixed window; resolved cells stop extending. The first wrong declared label stops at R2; maximum-window UNKNOWN or missingness stops at R3. Sealing used local hashes and time only.

## Results

| rho | H | load CI | label |
|---:|---:|---|---|
| 0.970 | 20,000 | [0.956913, 0.993245] | subcritical |
| 1.030 | 20,000 | [1.016103, 1.054683] | overloaded |
| 0.990 | 40,000 | [0.972746, 0.998718] | subcritical |
| 1.010 | 160,000 | [1.001040, 1.014316] | overloaded |
| 0.995 | 160,000 | [0.986173, 0.999252] | subcritical |
| 1.005 | 320,000 | [0.998880, 1.008229] | UNKNOWN |

Both controls resolved at 20k. Holdout 0.99 resolved at 40k; 1.01/0.995 at 160k. Load 1.005 remained UNKNOWN at all five windows; execution stopped at R3 after 51 workloads and 17 comparisons. Loads 0.999/1.001 were unexecuted and unscored. The final net-input drift interval was [-0.001120,0.008229]. There were zero wrong declared labels in the executed scope.

## What changed

The rule returns only the side supported by a known-model input interval instead of comparing positive growth with an arbitrary midpoint. Uncertainty is now explicit, but the acceptance requirement to resolve the known 1.005 overload within the budget was not met.

## What failed

The small overload could not be resolved even at 320k jobs per seed. No extra seeds or looser error budget were added after observation. Subcritical refers to the known full-gang capacity case; it is not a stability label for mixed needs.

## Evidence boundary

Scope is synthetic full-gang M/M/1 with independent exponential inputs, observable true service work and known unit capacity. All offered work, including unfinished jobs, is counted. Reflected remaining-workload drift differs from net input drift R-1. Availability of true required work on arrival in real data is unverified. The check does not validate mixed needs, alpha=0.5, bisection capacity, real clusters or independent replication.

The public verifier recalculates F quantiles, interval arithmetic and stop branches from pooled sufficient statistics. It does not regenerate jobs, rerun the simulator, test exponentiality or independence, or assess repeated-sampling coverage.

## UNKNOWN

How to obtain independent labels when mixed-need capacity is unknown; what uncertainty model supports non-exponential or dependent inputs; whether input work is observable in operation. General capacity and U-31 thresholds remain UNKNOWN.

## Falsification targets

Withdraw the description if sufficient-statistic arithmetic, quantiles, labels or stopping cannot be recalculated. Do not claim the conditional error bound where exponentiality, independence or known capacity fails. A future contract's resolution does not retroactively resolve this UNKNOWN.

## Reproduce

```bash
python reproduction/gpu-scheduling-u31-controls/verify_summary.py
```

SciPy is required. This is a bounded sufficient-statistic CI check, not a simulation rerun or independent scientific replication.

## Evidence / Artifacts

[Public sufficient statistics and verifier](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-u31-controls). Private Episode SHA-256: `772e57cdb1532f4aa047b32cda13fb04fe9e7d36d3272360ddd1106f34daf320`. Raw job sequences, simulator source and private work state are excluded.

## External audit

Zero independent replications and no peer review. Internal checks covered seal order, source hashes, quantile-CDF roundtrips, all 17 intervals, stopping and protocol-tamper rejection. Editorial/privacy review is not scientific or domain-expert review.

## Next experiment

Fix mechanism, input-work observability, exponentiality/independence and native-engine alignment before transfer to fixed-need M/M/c controls whose need divides pool capacity. Seal new controls/holdout, horizon cap, error budget and first R2/R3 stopping. Do not apply the interval to mixed needs without independent known labels. Full reruns of the existing 18 bisection cells and real-cluster validation remain separate gates.
