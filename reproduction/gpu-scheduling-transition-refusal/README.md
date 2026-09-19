# Permanent transition refusal audit (EP-0026)

This package audits an applicability gate for a known two-class exponential
strict-FCFS model. After arrival80000, arrival rate or both class service rates
change once and remain fixed forever. The post-transition stationary regime
supplies an independent eventual-tail stability label from the existing exact
capacity theorem. It is not a finite-window queue-state label.

```sh
python -m pip install numpy scipy
python runner_transition.py --verify-recorded --seeds 2
python runner_transition.py --seeds 10 --output full.json
```

The truthful arm passes the sealed provenance manifest. Stationary controls are
accepted; transition manifests contain an extra parameter_transition statement
and are refused as UNKNOWN without inference. The misuse arms deliberately lie
by passing the old stationary attestation on the same transition data. This is
an adversarial audit, not a recommended method.

120 workloads =2 models x6 scenarios x10 fresh seeds, three fixed looks
(100k/160k/320k),360 look records and1080 method outcomes. Cross-cell common
seeds are dependent. Five sealed predictions were fixed before execution.
At100k, false stationary scheduled/anytime methods are wrong in all80 drift
records. At320k, arrival changes and service degradation recover, while service
improvement leaves scheduled20/20 wrong and anytime20/20 UNKNOWN.

The gate relies on truthful provenance and does not detect an undeclared change
from data. It does not cover gradual/repeated/adaptive change, changing class
probabilities, nonexponential structure or real GPU systems. This is not a new
stability/changepoint theorem, general U31 detector, authenticated preregistration
or third-party independent replication. General validated detectors remain zero.
