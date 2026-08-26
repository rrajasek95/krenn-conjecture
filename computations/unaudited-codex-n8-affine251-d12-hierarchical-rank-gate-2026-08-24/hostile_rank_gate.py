#!/usr/bin/env python3
import copy
import json
from pathlib import Path
from validate_rank_gate import validate


def rejected(value):
    try:
        validate(value)
        return False
    except (AssertionError, KeyError, TypeError):
        return True


root = Path(__file__).resolve().parent
original = json.loads((root / "results_rank_gate_audit.json").read_text())
assert validate(original)
mutations = {
    "false_nonpromotion": lambda x: x.__setitem__("promotion", False),
    "wrong_configuration": lambda x: x["recommended_configuration"].__setitem__("rank_shards", 32),
    "continued": lambda x: x.__setitem__("continued_beyond_round660", True),
    "missing_run": lambda x: x.__setitem__("run_count", 8),
    "checkpoint_mismatch": lambda x: x["records"][0].__setitem__("checkpoint_sha256", "00" * 32),
    "hidden_equation_failure": lambda x: x.__setitem__("all_equations_verified", False),
    "rank_order_mutation": lambda x: x["ordering_contract"].__setitem__("owned_tuple_sort_matches_old_frequency_row_order", False),
    "source_order_mutation": lambda x: x["ordering_contract"].__setitem__("worker_chunks_join_in_source_order", False),
    "rss_overrun": lambda x: x["records"][0].__setitem__("peak_rss_bytes", 37 * 1024**3),
    "wall_overrun": lambda x: x["records"][0].__setitem__("total_seconds", 121),
    "false_speedup": lambda x: x["improvement"].__setitem__("fair_solve_factor", 1.1),
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
