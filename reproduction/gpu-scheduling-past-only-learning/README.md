# Past-only parameter learning in a known two-class FCFS model (EP-0024)

Inference sees arrivals, needs and completions through an arrival cutoff. It
receives no population parameters, true service sizes or future completion times.
It reconstructs strict-FCFS start times and class exposure including right-censored
running jobs; queued jobs contribute zero. The known structure is still 64
fungible resources, needs 32/64, iid marked Poisson arrivals, independent hidden
class-exponential service, and strict nonpreemptive FCFS with no locality,
overhead or size lookahead. This is not a general stability detector.

```sh
python -m pip install numpy scipy
python rerun_past_learning.py --verify-recorded
python rerun_past_learning.py --seeds 2 --horizons 20000 80000 320000 --output small.json
python rerun_past_learning.py --seeds 50 --horizons 20000 80000 320000 --output full.json
```

The verifier checks capacity algebra (20 exact CTMC cases and an interior
extremum), past telemetry and future rejection, 1200 recorded seed-look outputs,
24 cell and eight anylook aggregates, CP intervals/losses/four sealed predictions,
and 16 newly regenerated small runs. Full re-execution regenerates 400 workloads
and 6000 decisions. Seed9101–9150 is the repetition unit. Windows are nested
prefixes; common seeds across model/load cells induce dependence. CP intervals
split family .05 over 240 cell rates and 80 anylook rates. Anylook counts each
seed once if any of its three labels is wrong; unresolved means all looks UNKNOWN.

Five methods: PAST_AB (restored WSC2003 sample-variance interpretation, nominal
alpha .05 without a proven guarantee); KNOWN_CS (true capacity, arrival CS .05);
ALLOCATED_CS (true capacity, arrival CS .0125); LEARNED_CS (four past-only CS,
each .0125); PLUGIN_MLE (same past telemetry, point estimate, no uncertainty).
Known controls deliberately retain an oracle; allocation versus learning is
therefore separated rather than conflated. No F-work interval is used for mixtures.

Baseline p=.5, small/big service rates1/.5 gives X=8/11; transfer p=.25 and
rates.5/2 gives X=16/13. Loads z=lambda/X=.8/.99/1.01/1.2 exclude equality.
Capacity is a specialization of [known two-class theory](https://www.cs.cmu.edu/~harchol/Papers/twoclassstability.pdf):
1/X=(1-p)/mu_big+p(2-p)/(2mu_small). Its rectangle lower bound includes
the interior p*=1-mu_small/mu_big when applicable; endpoint-only evaluation
can fail. Service endpoints use monotonicity, rational arithmetic and outward
float conversion; unbounded intervals give conservative UNKNOWN.

The fixed Gamma(1,rate1) rate mixture is
E(theta)=exp(theta V) Gamma(M+1)/((V+1)^(M+1) theta^M); marks use Beta(1,1).
For service, completion intensity is mu_j R_j(t), V_j=integral R_j; completed
jobs alone are not treated as an iid sample. Existing likelihood-mixture/Ville
methods ([Howard et al.](https://arxiv.org/abs/1810.08240),
[Lindon & Kallus](https://proceedings.mlr.press/v258/lindon25a.html)) support
the model-conditioned counting-process argument. Four-way union allocation gives
nominal joint anytime .05 under the assumptions, not a new inference theorem.
Fixed log slack1e-6 and outward root padding mitigate floating point error;
this implementation is not a formally verified exact-arithmetic CS.

Recorded LEARNED_CS had no wrong-side labels but all 50 seeds remained UNKNOWN
at +/-1% loads even at320k arrivals, in both models. This is a conservative
method's measured cost, not a sample-complexity lower bound or proof that a
sharper method cannot decide. PLUGIN_MLE had 9–13/50 wrong at20k near the
boundary, zero in these cells at320k. LEARNED_CS then has higher point loss
for any positive abstention price; universal superiority is not claimed.
Loss e+a u uses fixed a=.1/.5/.9, conditional on benchmark truth.

summary.json is a reviewed projection, not the sealed protocol bytes. Original
source/result digests and local timestamps are provenance, not authenticated
preregistration. Native-engine alignment is recorded but not rerun here; the
public runner executes the same generator and causal FCFS oracle. No private
paths/imports are required. Same-design re-execution and OS portability are
not third-party independent replication. General U31/c12/nonexponential models,
real GPU effects, novel theory, peer review and manuscript novelty remain UNKNOWN.

Portability correction: the first public CI required exact dictionary equality
of floating-point roots and failed across Windows/Linux. Only the verifier was
changed to relative tolerance1e-9 and absolute tolerance1e-10 for continuous
values; labels, integer counts, booleans and null remain exact. The verifier
prints observed maximum numerical differences. The sealed experiment, priors,
inference implementation, decision thresholds and recorded results are unchanged.
