#!/usr/bin/env python3
"""Hostile schema mutations for the nine-block result."""

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("validator", HERE / "validate.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import validator")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
base = json.loads((HERE / "results_nine_block_induction_census.json").read_text())
cases = []


def add(name, mutate):
    value = copy.deepcopy(base)
    mutate(value)
    cases.append((name, value))


add("drop_record", lambda d: d["records"].pop())
add("wrong_unresolved", lambda d: d["enumeration"].update({"unresolved_records": 3475}))
add("promote_frontier", lambda d: d["frontier_interface_test"].update({"accepted_coverage_now": 2938}))
add("erase_no_degree4", lambda d: d["matching_essential_census"].update({"without_degree_four_vertex": 0}))
add("overcover_max16", lambda d: d["frontier_interface_test"].update({"conditional_if_max15_and_max16_terminal": 2942}))
add("wrong_new", lambda d: d["deletion_parent_census"].update({"genuinely_new_minimal_records": 919}))
add("infer_deletion", lambda d: d["scope"].update({"deletion_monotonicity_claim": True}))
add("close_layer", lambda d: d["scope"].update({"nine_block_layer_closed": True}))
add("claim_conjecture", lambda d: d["scope"].update({"full_conjecture_claim": True}))
add("drop_guard_orbit", lambda d: d["literal_guard_orbits"].pop())
add("wrong_graph_classes", lambda d: d["matching_essential_census"].update({"unlabelled_graph_classes": 190}))
add("wrong_exact17", lambda d: d["frontier_interface_test"]["still_open_breakdown"].update({"exact17_with_degree4": 530}))
add("claim_solver", lambda d: d["scope"].update({"heavy_solver_runs": 1}))
add("lose_source_provenance", lambda d: d["scope"].update({"source_and_guard_provenance_only": False}))

results = []
for name, value in cases:
    try:
        validator.validate_schema(value)
    except Exception as error:
        results.append({"name": name, "status": "REJECTED", "error": str(error)})
    else:
        results.append({"name": name, "status": "ACCEPTED_IN_ERROR"})
if not all(result["status"] == "REJECTED" for result in results):
    raise RuntimeError(results)
output = {"schema": "n8-x5-nine-block-census-hostiles-v1", "status": "PASS", "count": len(results), "tests": results}
(HERE / "results_hostiles.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS", "count": len(results)}, sort_keys=True))
