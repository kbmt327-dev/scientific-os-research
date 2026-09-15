"""Check only the arithmetic and stop branch in the public EP-0017 summary."""

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "results" / "u31-v3-summary.json").read_text(encoding="utf-8"))
cells = data["cells"]
assert data["research_id"] == "GPU-SCHED-EP-0017"
assert data["scope"] == {
    "model": "synthetic MSJ", "mix": "balanced", "policy": "fcfs",
    "n_servers": 64, "horizons": [20000, 40000], "seeds": [111, 222],
}
assert data["fixed_grid"] == [0.7, 0.85, 1.0]
assert [cell["rho"] for cell in cells] == [0.4, 1.2, 0.7, 0.85]
assert all(cell["simulations"] == 4 for cell in cells)
assert all(math.isfinite(cell[key]) for cell in cells for key in ("alpha", "queue_score"))
low, high = (cell["queue_score"] for cell in cells[:2])
assert low < high and low <= 0.01 and high >= 0.05
threshold = (low + high) / 2
assert math.isclose(threshold, data["calibrated_threshold"], rel_tol=0, abs_tol=1e-12)
grid = cells[2:]
labels = [(cell["alpha"] >= data["alpha_line"], cell["queue_score"] >= threshold) for cell in grid]
assert labels == [(False, False), (True, False)]
assert data["verdict"] == "R2 local-disagreement"
assert data["stop_at_rho"] == grid[-1]["rho"] == 0.85
assert data["unexecuted_grid"] == [1.0]
assert data["executed_simulations"] == sum(cell["simulations"] for cell in cells) == 16
assert data["claim_status"] == "UNKNOWN" and data["independent_replications"] == 0
print("EP-0017 public summary: arithmetic and stop branch OK; simulation not reproduced")
