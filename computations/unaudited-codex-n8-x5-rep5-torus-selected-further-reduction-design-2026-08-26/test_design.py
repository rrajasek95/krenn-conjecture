#!/usr/bin/env python3
"""Hostile metadata tests for the exact residual-torus cover; no solver."""
from __future__ import annotations

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def validate(value: dict) -> None:
    assert value["schema"] == "KRENN_X5_REP5_TORUS_SELECTED_FURTHER_REDUCTION_DESIGN_V1"
    assert value["status"] == "PASS_EXACT_TWO_CHART_RESIDUAL_ONE_TORUS_COVER"
    assert value["source"] == {"bytes": 4416511, "field": "Q", "generators": 6561, "order": "dp", "sha256": "13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0", "variables": 73}
    grading = value["grading"]
    assert (grading["rank"], grading["nullity"]) == (72, 1)
    assert grading["nonzero_weights"] == [{"a04_20": 1, "a04_21": 1, "a04_22": 1, "a35_21": -1, "a35_22": -1, "a37_20": -1}]
    cover = value["residual_torus_cover"]
    assert cover["root_free"] is True and cover["selected_coordinate"] == "a37_20" and cover["selected_weight"] == -1
    assert len(cover["sources"]) == 2
    assert [(source["variables"], source["generators"], source["unit"], source["zeros"]) for source in cover["sources"]] == [
        (72, 6561, "a37_20", []), (72, 6561, None, ["a37_20"]),
    ]
    assert [source["grading_nullity_over_Q"] for source in cover["sources"]] == [0, 1]
    assert all(not source["monic_graph_substitutions"] and not source["inactive"] for source in cover["sources"])
    linear = value["linear_reduction"]
    assert linear["amplitude_inactive_coordinates"] == [] and linear["unit_coefficient_graph_substitutions"] == []
    assert (linear["affine_linear_generator_count"], linear["affine_linear_generator_rank"], linear["all_generator_linear_part_rank"]) == (0, 0, 43)
    assert value["block_structure"]["component_sizes"] == [73]
    assert value["conclusion"]["singular_runs"] == 0 and value["conclusion"]["mathematical_coverage"] is False


base = json.loads((HERE / "results_design.json").read_text())
validate(base)
mutations = [
    ("status", lambda x: x.__setitem__("status", "PASS")),
    ("source", lambda x: x["source"].__setitem__("sha256", "0" * 64)),
    ("rank", lambda x: x["grading"].__setitem__("rank", 71)),
    ("nullity", lambda x: x["grading"].__setitem__("nullity", 0)),
    ("weights", lambda x: x["grading"].__setitem__("nonzero_weights", [])),
    ("root", lambda x: x["residual_torus_cover"].__setitem__("root_free", False)),
    ("coordinate", lambda x: x["residual_torus_cover"].__setitem__("selected_coordinate", "a04_20")),
    ("weight", lambda x: x["residual_torus_cover"].__setitem__("selected_weight", 2)),
    ("missing_chart", lambda x: x["residual_torus_cover"]["sources"].pop()),
    ("chart_shape", lambda x: x["residual_torus_cover"]["sources"][0].__setitem__("variables", 73)),
    ("monic", lambda x: x["linear_reduction"].__setitem__("unit_coefficient_graph_substitutions", ["false"])),
    ("solver", lambda x: x["conclusion"].__setitem__("singular_runs", 1)),
]
passed = {}
for name, mutate in mutations:
    value = copy.deepcopy(base)
    mutate(value)
    try:
        validate(value)
    except (AssertionError, KeyError, TypeError):
        passed[name] = True
    else:
        passed[name] = False
assert len(passed) == 12 and all(passed.values())
result = {"schema": "KRENN_X5_REP5_TORUS_SELECTED_FURTHER_REDUCTION_HOSTILES_V1", "status": "PASS", "hostile_count": 12, "solver_runs": 0, "tests": passed}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS", "hostiles": 12, "solver_runs": 0}, sort_keys=True))
