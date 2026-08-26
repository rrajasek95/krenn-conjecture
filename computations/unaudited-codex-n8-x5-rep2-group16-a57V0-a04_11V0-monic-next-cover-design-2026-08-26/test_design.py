#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / "results_design.json").read_text())


def accepted(record: dict) -> bool:
    try:
        graph = record["graph_elimination"]
        assert graph["equation"] == "-1-a26_00-a26_02*a57_02"
        assert graph["substitution"] == "a26_00=-1-a26_02*a57_02"
        assert graph["unit_coefficient"] == -1 and graph["forward_reverse_exact"] is True
        assert graph["source_variables_before_after"] == [59, 58]
        assert graph["source_generators_before_after"] == [6064, 6063]
        assert graph["source_terms_before_after"] == [157829, 113139]
        assert record["grading"]["rank"] == 54 and record["grading"]["nullity"] == 4
        linear = record["linear_census"]
        assert linear["affine_linear_rank"] == 3 and linear["all_linear_part_rank"] == 43
        assert len(linear["unit_coefficient_graph_substitutions"]) == 18
        cover = record["cover"]
        assert cover["identity"] == "D(q) union V(q)" and cover["root_free"] is True
        assert cover["selected"] == {
            "basis_index": 2, "coordinate": "a14_01",
            "objective": [111546, 111547, 6015], "weight": -1,
        }
        assert [(source["branch"], source["variables"], source["generators"], source["total_terms"], source["unit_ideal_structural"])
                for source in cover["sources"]] == [
            ("D1", 57, 1, 1, True),
            ("V0", 57, 6015, 111546, False),
        ]
        factors = record["factor_census"]
        assert factors["maximum_complete_factor_generators"] == 504
        assert factors["positive_complete_factor_coordinates"] == 28
        update = record["global_cover_update"]
        assert update["exhaustive"] is True and update["leaf_count_before"] == update["leaf_count_after"] == 3
        assert update["forced_zero"] == "a14_01=0"
        conclusion = record["conclusion"]
        assert conclusion["open_branch_structural_unit_ideal"] is True
        assert conclusion["forced_zero_reduction"] == "a14_01=0"
        assert conclusion["singular_runs"] == 0 and conclusion["mathematical_coverage"] is False
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


mutate(("graph_elimination", "unit_coefficient"), 2)
mutate(("graph_elimination", "forward_reverse_exact"), False)
mutate(("graph_elimination", "source_variables_before_after"), [59, 59])
mutate(("graph_elimination", "source_generators_before_after"), [6064, 6064])
mutate(("grading", "rank"), 53)
mutate(("grading", "nullity"), 3)
mutate(("linear_census", "affine_linear_rank"), 2)
mutate(("linear_census", "all_linear_part_rank"), 42)
mutate(("cover", "selected", "coordinate"), "a14_11")
mutate(("cover", "selected", "weight"), 1)
mutate(("cover", "sources", 0, "unit_ideal_structural"), False)
mutate(("cover", "sources", 1, "generators"), 6016)
mutate(("factor_census", "maximum_complete_factor_generators"), 503)
mutate(("global_cover_update", "exhaustive"), False)
mutate(("global_cover_update", "leaf_count_after"), 4)
mutate(("conclusion", "singular_runs"), 1)
mutate(("conclusion", "mathematical_coverage"), True)
assert all(not accepted(record) for record in hostiles)

result = {
    "schema": "KRENN_X5_REP2_GROUP16_A57V0_A04_11V0_MONIC_NEXT_COVER_HOSTILES_V1",
    "status": "PASS",
    "hostile_count": len(hostiles),
    "solver_runs": 0,
}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
