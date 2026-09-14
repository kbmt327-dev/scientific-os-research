# Intervention prediction grammar reproduction

A standalone reference implementation of the prediction contract used when the
predictor is also the actor, together with a negative control for every
invariant it adds. Standard library only; no connection to the private research
runtime, and nothing here reads private data.

```bash
python scripts/reproduce.py --quick intervention
```

Or from this directory:

```bash
python tests/validate_intervention_grammar.py
```

Expected: `all_passed: true`, nine refused negative controls covering B1–B5, and
three positive checks (a scoring date that never came is recorded without being
scored; an executed commitment that missed still scores; observational
predictions still need no attribution).

## Boundary

This bundle demonstrates that the contract refuses the records it claims to
refuse. It is not evidence that the grammar is sufficient for real intervention
research, that the five breaches are the complete set, or that any prediction
written in this form has ever been scored. No sealed prediction in this grammar
has reached its scoring date.

`contract.py` is a reference implementation written for reading and running. The
research runtime it mirrors is not public, so agreement between the two is
asserted here, not demonstrated.
