# Human Model Contract v0.2 reproduction

This public bundle contains the v0.2 schemas, examples, cross-document validator, and validation evidence. One example was privacy-sanitized by replacing machine-local documentation paths with repository-relative placeholders; therefore public artifact hashes are not represented as the internal evidence hashes.

```bash
python scripts/reproduce.py --quick human
```

Or from this directory:

```bash
python tests/validate_contract_v0_2.py
```

Expected: `all_passed: true`, nine positive check groups, and seven rejected negative controls.

## Boundary

The validator does not execute Nimble/OpenSim, read B3D numerical frames, validate coordinate transforms, or demonstrate predictive performance. The example adapter remains blocked.

