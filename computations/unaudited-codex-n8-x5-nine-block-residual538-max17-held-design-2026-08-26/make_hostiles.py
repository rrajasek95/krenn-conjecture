#!/usr/bin/env python3
"""Hostile mutations for the residual-538 schema."""

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
base = json.loads((HERE / "results_residual538_design.json").read_text())
cases = []


def add(name, mutation):
    value = copy.deepcopy(base)
    mutation(value)
    cases.append((name, value))


add("promote_e17", lambda d: d["residual_ledger"].update({"accepted_coverage_now": 534}))
add("drop_e17_record", lambda d: d["exact17_degree4"]["record_indices"].pop())
add("wrong_guard_orbits", lambda d: d["exact17_degree4"].update({"literal_guard_orbits": 266}))
add("wrong_graph_classes", lambda d: d["exact17_degree4"].update({"unlabelled_graph_classes": 49}))
add("erase_exception", lambda d: d["exact16_no_degree4"].update({"records": 3}))
add("claim_two_transport_orbits", lambda d: d["exact16_no_degree4"].update({"full_source_site_transport_orbits": 2}))
add("claim_fourregular", lambda d: d["exact16_no_degree4"]["known_interface_tests"].update({"four_regular": "APPLICABLE"}))
add("claim_balanced_bridge", lambda d: d["exact16_no_degree4"]["known_interface_tests"].update({"max_degree5_balanced_all_bridge": "APPLICABLE"}))
add("claim_residual_closed", lambda d: d["scope"].update({"residual_closed": True}))
add("claim_cnf_read", lambda d: d["scope"].update({"large_cnf_materialized_or_read": True}))
add("claim_sat_run", lambda d: d["scope"].update({"sat_or_drat_runs": 1}))
add("claim_external_promotion", lambda d: d["scope"].update({"external_theorem_promoted": True}))
add("claim_conjecture", lambda d: d["scope"].update({"full_conjecture_claim": True}))
add("wrong_matching_count", lambda d: d["exact16_no_degree4"]["records_detail"][0]["supported_perfect_matchings"].pop())

results = []
for name, value in cases:
    try:
        validator.validate_schema(value, check_file=False)
    except Exception as error:
        results.append({"name": name, "status": "REJECTED", "error": str(error)})
    else:
        results.append({"name": name, "status": "ACCEPTED_IN_ERROR"})
if not all(result["status"] == "REJECTED" for result in results):
    raise RuntimeError(results)
out = {"schema": "n8-x5-residual538-hostiles-v1", "status": "PASS", "count": len(results), "tests": results}
(HERE / "results_hostiles.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS", "count": len(results)}, sort_keys=True))
