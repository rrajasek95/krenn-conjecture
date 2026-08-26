#!/usr/bin/env python3
"""Mutation hostiles for the design contract; no solver invocation."""
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / "results_design.json").read_text())


def valid(value):
    assert value["status"] == "PASS_EXACT_16_CHART_73_VARIABLE_COVER_ZERO_SOLVES"
    assert value["consumed_timeout"]["consumed_no_reuse_no_retry"] is True
    assert value["consumed_timeout"]["mathematical_coverage"] is False
    assert value["grading"]["rank"] == 74 and value["grading"]["nullity"] == 10
    assert abs(value["grading"]["selected_minor_determinant"]) == 1
    assert value["global_gauge"]["normalized_units"] == ["beta", "abar", "a37_00", "t1", "sat", "d", "b2"]
    assert value["global_gauge"]["root_extraction"] is False
    assert value["residual_cover"]["charts"] == 16
    assert value["residual_cover"]["variables_each"] == 73
    assert value["residual_cover"]["generators_each"] == 6561
    assert len(value["residual_cover"]["sources"]) == 16
    assert value["order_and_scope"]["singular_runs"] == 0
    assert value["order_and_scope"]["mathematical_coverage"] is False


mutations = [
    lambda x: x.update(status="PASS_CLOSED"),
    lambda x: x["consumed_timeout"].update(consumed_no_reuse_no_retry=False),
    lambda x: x["consumed_timeout"].update(mathematical_coverage=True),
    lambda x: x["grading"].update(rank=73),
    lambda x: x["grading"].update(nullity=11),
    lambda x: x["grading"].update(selected_minor_determinant=2),
    lambda x: x["global_gauge"].update(normalized_units=["beta"]),
    lambda x: x["global_gauge"].update(root_extraction=True),
    lambda x: x["residual_cover"].update(charts=15),
    lambda x: x["residual_cover"].update(variables_each=74),
    lambda x: x["residual_cover"].update(generators_each=6562),
    lambda x: x["residual_cover"]["sources"].pop(),
    lambda x: x["order_and_scope"].update(singular_runs=1),
    lambda x: x["order_and_scope"].update(mathematical_coverage=True),
]
passed = 0
for mutation in mutations:
    candidate = copy.deepcopy(base)
    mutation(candidate)
    try:
        valid(candidate)
    except (AssertionError, KeyError, TypeError):
        passed += 1
assert passed == len(mutations)
valid(base)
(HERE / "results_hostiles.json").write_text(json.dumps({
    "schema": "KRENN_X5_REP5_K2_T1_TORUS_COVER_HOSTILES_V1",
    "status": "PASS_14_HOSTILES_ZERO_RUN",
    "hostiles": passed,
    "solver_runs": 0,
}, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS_14_HOSTILES_ZERO_RUN", "hostiles": passed}, sort_keys=True))
