# Frontier metrics: two retracted results

A standalone copy of the world whose two headline results were withdrawn, plus
the two sweeps that withdrew them. Standard library only; no data of any kind is
included or used.

```bash
python scripts/reproduce.py --quick frontier
```

Or from this directory:

```bash
python tests/reproduce_retractions.py
```

Expected: `both_headline_results_retracted: true`, and the surviving result
(reuse responds to the frontier) marked `survives`.

## What the two sweeps do

**Attack 1** sweeps `p_called_idiosyncratic`, the constant that was the only
route from a judgement to a non-rule. If the settling rate simply follows that
constant, it was never measuring the frontier.

**Attack 2** sweeps `theta`, the base novelty, at a frontier that fully closes.
The estimator was characterised at `theta = 30` and the decision line published
as though it depended on sample size alone.

## Boundary

Synthetic. The mechanism family is ours. This package demonstrates how two
published claims were withdrawn; it is not evidence about accounting, about any
organisation, or about the mechanisms that operate in practice.
