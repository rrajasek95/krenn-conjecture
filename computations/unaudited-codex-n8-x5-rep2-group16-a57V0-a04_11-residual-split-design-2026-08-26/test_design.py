#!/usr/bin/env python3
"""Fail-closed structural hostiles for the exact residual chart split."""
from __future__ import annotations

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / "results_design.json").read_text())


def accepted(record: dict) -> bool:
    try:
        assert record["status"] == "PASS_EXACT_PRIMITIVE_TORUS_DV_COVER"
        assert record["source"]["variables"] == 60 and record["source"]["generators"] == 6568
        assert record["grading"]["rank"] == 56 and record["grading"]["nullity"] == 4
        cover = record["cover"]
        assert cover["identity"] == "D(q) union V(q)" and cover["root_free"] is True
        assert cover["selected"] == {
            "basis_index": 0,
            "coordinate": "a04_11",
            "objective": [174407, 332236, 6568],
            "weight": 1,
        }
        assert [(source["branch"], source["variables"], source["generators"], source["total_terms"])
                for source in cover["sources"]] == [
            ("D1", 59, 6568, 174407),
            ("V0", 59, 6064, 157829),
        ]
        assert record["factor_census"]["source_generators_divisible_by_coordinate"] == 504
        update = record["global_cover_update"]
        assert update["leaf_count_before"] == 2 and update["leaf_count_after"] == 3
        assert update["exhaustive"] is True
        assert record["conclusion"]["singular_runs"] == 0
        assert record["conclusion"]["mathematical_coverage"] is False
        return True
    except (AssertionError, KeyError, TypeError):
        return False


assert accepted(base)
hostiles: list[dict] = []


def mutate(path: tuple[str | int, ...], value: object) -> None:
    record = copy.deepcopy(base)
    current: object = record
    for key in path[:-1]:
        current = current[key]  # type: ignore[index]
    current[path[-1]] = value  # type: ignore[index]
    hostiles.append(record)


mutate(("source", "variables"), 61)
mutate(("source", "generators"), 6567)
mutate(("grading", "rank"), 55)
mutate(("grading", "nullity"), 3)
mutate(("cover", "root_free"), False)
mutate(("cover", "selected", "coordinate"), "a04_12")
mutate(("cover", "selected", "weight"), 2)
mutate(("cover", "sources", 0, "variables"), 60)
mutate(("cover", "sources", 1, "generators"), 6568)
mutate(("factor_census", "source_generators_divisible_by_coordinate"), 503)
mutate(("global_cover_update", "exhaustive"), False)
mutate(("global_cover_update", "leaf_count_after"), 2)
mutate(("conclusion", "singular_runs"), 1)
mutate(("conclusion", "mathematical_coverage"), True)
assert all(not accepted(record) for record in hostiles)

result = {
    "schema": "KRENN_X5_REP2_GROUP16_A57V0_A04_11_RESIDUAL_SPLIT_HOSTILES_V1",
    "status": "PASS",
    "hostile_count": len(hostiles),
    "solver_runs": 0,
}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
