# Service-exposure checkpoints and scheduled reporting (EP-0025)

This package compares past-only inference with different reporting contracts.
Known structure: 64 fungible resources, needs32/64, iid marked Poisson arrivals,
independent class-exponential service, strict nonpreemptive FCFS, empty start,
no locality/overhead/backfill/size lookahead. Inference receives arrivals, needs
and completions through A_H; never population parameters, true service or future
completions. Baseline p=.5, service rates1/.5 gives X=8/11; transfer p=.25 and
rates.5/2 gives X=16/13, using [known two-class stability](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf).

```sh
python -m pip install numpy scipy
python runner_checkpoint.py --verify-recorded
python runner_checkpoint.py --seeds 2 --horizons 20000 320000 --output small.json
python runner_checkpoint.py --seeds 20 --horizons 20000 320000 1280000 --output full.json
```

Verifier: recorded480seed-look/2400decision arithmetic, fixed-count tape,
scheduled inference, seven declaration negatives/two non-scheduled cases,
CP/loss/anylook/four sealed predictions and16 regenerated small runs. Full grid
has160 workloads and204800000 generated jobs, taking longer than the quick check.
Small reruns retain all three original planned looks in error allocation; the
budget of omitted outputs is not reassigned. Only original H are supported.
Full re-execution calls the benchmark core without the private native engine.
The public benchmark module omits the private CLI/native adapter; core inference
and generation logic are unchanged. This is a curated projection, not source bytes.

At class j's fixed Kth completion, exposure V_j=integral R_j(t) counts all running
jobs including censored ones. It is not total completed-job duration. The hand
concurrency fixture gives V_small(t_first_completion)=19.9 versus duration10.
The existing [random-time-change theorem, Theorem22](https://warwick.ac.uk/fac/sci/statistics/apts/students/resources-2010-2011/stochproc_notes.pdf)
maps the continuous unbounded compensator mu_j V_j of the infinite model to
unit-rate Poisson time, so2mu_j V_j(t_K)~chi-square(2K). The finite generated
prefix matches that process through A_H; unattained checkpoints are not used.

Fixed milestones256–1048576 doubling (13 each class); looks20k/320k/1280k.
The largest attained fixed milestone can be selected because failure events
are union-bounded over the entire fixed list, unconditionally. Do not claim
coverage conditional on availability or insert the random observed completion
count M into a fixed-count Gamma pivot.
Scheduled joint alpha .05 gives .05/4 to each of lambda,p,mu_small,mu_big.
Arrival/mark errors divide by3looks (chi-square/binomial CP); service errors
divide by13fixed checkpoints. Union bound over6arrival/mark and26service
intervals needs no independence. This is NOT an anytime confidence set.
Capacity rectangles include the interior p extremum and outward rounding.

ANYTIME_RECT retains EP24 likelihood-mixture CS with four errors.0125.
CHECKPOINT_RECT uses scheduled intervals. KNOWN_SCHEDULED knows X and uses
arrival error.05/3; ALLOC_SCHEDULED knows X with the same arrival error as the
checkpoint method; PLUGIN_MLE uses past full exposure point estimates, without
error control. Guarantee scope and known-capacity privilege are disclosed.

20fresh seeds9201–9220 per model/load; z=.8/.99/1.01/1.2, equality excluded.
Windows are nested, common seeds across cells are dependent. CP family .05 over
240cell rates and80anylook rates; anylook counts a seed once if any look is wrong.
n20 gives wide intervals: zero/20anylook wrong has simultaneous upper about.332.
Loss e+a u at a=.1/.5/.9 is benchmark-truth conditional, not online ranking.

Measured CHECKPOINT_RECT wrong=0/480seed-look. Near-boundary1280k UNKNOWN:
ANYTIME_RECT 79/80, CHECKPOINT_RECT 22/80.
Sealed predictions4/4; all cell outcomes and any failures are retained.
This is a model/budget-conditioned comparison, not universal superiority,
novel inference theory or optimal sample complexity.
Reporting scope and the statistic/data subset both change, so this comparison
does not isolate a causal effect of reporting restriction alone. Chi-square/beta
quantiles are floating-point library evaluations, not formally certified coverage.

The exact declaration gate rejects missing/extra/unconfirmed/out-of-scope
model/log statements and reports UNKNOWN without inference. It checks declarations,
not whether exponentiality, independence or log completeness are true in real data.
Matching a real log schema is not verified synthetic-generator provenance.

summary.json is a reviewed projection, not original sealed protocol/result bytes.
Local hashes/clocks are provenance, not externally authenticated preregistration.
Native4096-job fixtures (four) recorded24checkpoint comparisons, not rerun here.
Continuous public verification uses rel1e-9/abs1e-10; labels/counts exact.
Same-design/code execution and OS portability are not third-party independent
replication. General U31/c12/nonexponential/real GPU, new theory, peer review,
manuscript novelty and operational effect remain UNKNOWN; general detectors0.
