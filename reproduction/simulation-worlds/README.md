# Sim World EP-0001 reproduction

This package contains the completed blinded queueing benchmark at source commit `16a8821`: the world generator, seed commitment, observations, sealed predictions, fitted simulator, and ordered analysis scripts.

The completed package is no longer blind because the reveal is public. To test the method prospectively, generate a fresh seal and withhold `reveal` from the analyst until the final model is sealed.

## Quick completed-run check

```bash
python scripts/reproduce.py --quick queue
```

## Re-run the analysis ladder

From this directory, with NumPy and SciPy installed, run `analysis/a01_baseline.py` through `analysis/a11_verify_against_truth.py` in numerical order. Some scripts generate or overwrite sealed artifacts and should only be used on a copy for a genuinely new blind run.

## New hidden world

```bash
python world/world.py seal --out seal/new_world_seal.json
python world/world.py fingerprint --seal seal/new_world_seal.json
```

Do not run `reveal` until the final model has been sealed.

## Boundary

The family of candidate mechanisms is known in advance. The benchmark tests hidden-instance identification inside that family, not open-world discovery.

