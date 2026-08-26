#!/usr/bin/env python3
import copy
import json
from pathlib import Path
from validate_geometry import validate


def rejected(value):
    try:
        validate(value)
        return False
    except (AssertionError, KeyError, TypeError):
        return True


root = Path(__file__).resolve().parent
original = json.loads((root / "results_geometry_audit.json").read_text())
assert validate(original)
cases = {}
for label, mutation in {
    "false_promotion": lambda x: x.__setitem__("promotion", True),
    "false_verdict": lambda x: x.__setitem__("verdict", "PROMOTE"),
    "continued": lambda x: x.__setitem__("continued_beyond_round660", True),
    "missing_run": lambda x: x.__setitem__("run_count", 14),
    "checkpoint_mismatch": lambda x: x["best_observed"].__setitem__("checkpoint_sha256", "00" * 32),
    "hidden_equation_failure": lambda x: x.__setitem__("all_equations_verified", False),
    "rss_overrun": lambda x: x["records"][0].__setitem__("peak_rss_bytes", 37 * 1024**3),
    "wall_overrun": lambda x: x["records"][0].__setitem__("total_seconds", 121),
    "false_stability": lambda x: x["normalized_16x8"].__setitem__("speedup", 2.62),
}.items():
    candidate = copy.deepcopy(original)
    mutation(candidate)
    cases[label] = rejected(candidate)
assert all(cases.values())
output = {"status": "PASS", "positive_control": True, "fail_closed": True, "cases": cases}
(root / "hostile_results.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
print(json.dumps(output, sort_keys=True))
