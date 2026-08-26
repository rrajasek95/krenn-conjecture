#!/usr/bin/env python3
"""Hostile mutations for the exact global-unit torus gauge."""
from __future__ import annotations

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / "results_design.json").read_text())


def accepts(record: dict) -> bool:
    try:
        assert record["status"] == "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE"
        assert record["source"]["variables"] == 64 and record["source"]["generators"] == 6569
        assert record["timeout_binding"]["rerun"] is False
        assert record["grading"]["rank"] == 58 and record["grading"]["nullity"] == 6
        cover = record["cover"]
        assert cover["maximal_primitive_global_gauge_coordinates"] == ["it1", "sat"]
        assert cover["maximal_primitive_global_gauge_weight_rows"] == [[0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 1, 0]]
        assert cover["global_gauge_assignments_including_inverse_partners"] == {"it1": 1, "sat": 1, "t1": 1}
        assert cover["global_unit_witnesses"]["sat"]["equation_indices"] == [6567]
        assert cover["global_unit_witnesses"]["it1"]["equation_indices"] == [6568]
        assert cover["global_unit_witnesses"]["t1"]["equation_indices"] == [6568]
        assert len(cover["sources"]) == 1
        source = cover["sources"][0]
        assert source["variables"] == 61 and source["generators"] == 6568
        assert source["assignment"] == {"it1": 1, "sat": 1, "t1": 1}
        assert source["unit_ideal_structural"] is False
        assert record["conclusion"]["singular_runs"] == 0
        assert record["conclusion"]["old_timeout_consumed"] is True
        assert record["conclusion"]["old_chart_relaunch"] is False
        return True
    except (AssertionError, KeyError, TypeError):
        return False


assert accepts(base)
mutations = []


def mutate(path: tuple, value) -> None:
    record = copy.deepcopy(base)
    cursor = record
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    mutations.append(record)


mutate(("timeout_binding", "rerun"), True)
mutate(("grading", "rank"), 57)
mutate(("grading", "nullity"), 5)
mutate(("cover", "maximal_primitive_global_gauge_coordinates"), ["sat"])
mutate(("cover", "maximal_primitive_global_gauge_weight_rows"), [[0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, -1]])
mutate(("cover", "global_gauge_assignments_including_inverse_partners"), {"it1": 1, "sat": 1})
mutate(("cover", "global_unit_witnesses", "sat", "equation_indices"), [0])
mutate(("cover", "global_unit_witnesses", "it1", "equation_indices"), [])
mutate(("cover", "sources"), [])
mutate(("cover", "sources", 0, "variables"), 62)
mutate(("conclusion", "singular_runs"), 1)
mutate(("conclusion", "old_chart_relaunch"), True)
assert all(not accepts(record) for record in mutations)
result = {"schema": "KRENN_X5_REP2_GROUP16_DT1_TIMEOUT_REDUCTION_HOSTILES_V1", "status": "PASS", "hostile_count": len(mutations), "solver_runs": 0}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
