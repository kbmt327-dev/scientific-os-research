# IAA EP-0008 protocol and power sensitivity

This package contains a public preregistration draft and its Monte Carlo power-sensitivity script. It contains no confirmatory data and does not authorize data collection.

```bash
python scripts/reproduce.py --quick iaa
```

For the original 10,000 iterations per scenario:

```bash
cd reproduction/badminton-biomechanics
python analysis/ep0008_power_simulation.py --iterations 10000 --seed 20260913
```

The simulation assumes balanced complete cells, residual SD 1, participant random-slope SD 0.20, and a Bonferroni per-test threshold. These assumptions are not empirically calibrated to the proposed experiment.

