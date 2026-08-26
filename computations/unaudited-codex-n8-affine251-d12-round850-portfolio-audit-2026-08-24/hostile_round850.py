#!/usr/bin/env python3
import copy
import json
from pathlib import Path
from validate_round850 import validate


def rejected(value):
    try:
        validate(value)
        return False
    except (AssertionError, KeyError, TypeError):
        return True


root = Path(__file__).resolve().parent
original = json.loads((root / "results_round850_audit.json").read_text())
assert validate(original)
mutations = {
    "wrong_selection": lambda x: x.__setitem__("selected_pivot", "first"),
    "false_cold_rare": lambda x: x.__setitem__("cold_rare_remains_selected", False),
    "missing_portfolio_task": lambda x: x["portfolio_compared"].__setitem__("task_count", 5),
    "checkpoint_mismatch": lambda x: x["selected_control"]["hashes"].__setitem__("checkpoint.bin", "00" * 32),
    "cache_mismatch": lambda x: x["selected_control"]["hashes"].__setitem__("vectors.bin", "00" * 32),
    "input_replay_failure": lambda x: x["round849_input_all_column_replay"].__setitem__("verification_failures", 1),
    "continued": lambda x: x.__setitem__("continued_beyond_round850", True),
    "production_mutated": lambda x: x.__setitem__("production_mutated", True),
    "rss_overrun": lambda x: x["portfolio"].__setitem__("peak_rss_kib", 36 * 1024 * 1024),
    "false_terminal": lambda x: x.__setitem__("global_annihilation", True),
}
cases = {}
for label, mutation in mutations.items():
    candidate = copy.deepcopy(original)
    mutation(candidate)
    cases[label] = rejected(candidate)
assert all(cases.values())
output = {"status": "PASS", "positive_control": True, "fail_closed": True, "cases": cases}
(root / "hostile_results.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
print(json.dumps(output, sort_keys=True))
