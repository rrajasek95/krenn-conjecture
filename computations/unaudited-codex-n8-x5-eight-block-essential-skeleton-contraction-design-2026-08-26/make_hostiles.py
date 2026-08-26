#!/usr/bin/env python3
"""Hostile mutations for the fail-closed result schema."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_validator():
    spec = importlib.util.spec_from_file_location("validator", HERE / "validate.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    validator = load_validator()
    base = json.loads((HERE / "results_essential_skeleton_contraction_design.json").read_text())
    mutations = []

    def add(name, function):
        value = copy.deepcopy(base)
        function(value)
        mutations.append((name, value))

    add("drop_record", lambda d: d["all_record_details"].pop())
    add("promote_max15_early", lambda d: d["degree_four_interfaces"]["fresh_at_most15"].update({"accepted_coverage_now": 500}))
    add("import_legacy", lambda d: d["scope"].update({"legacy_theorem_imported": True}))
    add("import_unverified_drat", lambda d: d["scope"].update({"fresh_drat_result_imported": True}))
    add("wrong_atmost15", lambda d: d["essential_skeleton_census"].update({"at_most_15_records": 501}))
    add("wrong_exact16", lambda d: d["essential_skeleton_census"].update({"exact_16_records": 115}))
    add("conflate_signature_graph", lambda d: d["essential_skeleton_census"].update({"unlabelled_graph_classes_all": 32}))
    add("drop_guard_orbit", lambda d: d["exact16_guard_orbits"].pop())
    add("claim_chart_coverage", lambda d: d["smallest_contracted_held_chart"].update({"scope": "all strata"}))
    add("wrong_variable_count", lambda d: d["smallest_contracted_held_chart"].update({"contracted_variables": 81}))
    add("claim_solve", lambda d: d["smallest_contracted_held_chart"].update({"solve_status": "UNIT_IDEAL"}))
    add("claim_layer_closed", lambda d: d["scope"].update({"eight_block_layer_closed": True}))
    add("claim_deletion_monotonicity", lambda d: d["scope"].update({"deletion_monotonicity_claim": True}))
    add("claim_conjecture", lambda d: d["scope"].update({"full_conjecture_claim": True}))

    results = []
    for name, value in mutations:
        try:
            validator.validate_schema(value, check_files=False)
        except Exception as error:
            results.append({"name": name, "status": "REJECTED", "error": str(error)})
        else:
            results.append({"name": name, "status": "ACCEPTED_IN_ERROR"})
    if not all(result["status"] == "REJECTED" for result in results):
        raise RuntimeError(results)
    output = {"schema": "n8-x5-eight-block-essential-skeleton-hostiles-v1", "status": "PASS", "count": len(results), "tests": results}
    (HERE / "results_hostiles.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "count": len(results)}, sort_keys=True))


if __name__ == "__main__":
    main()
