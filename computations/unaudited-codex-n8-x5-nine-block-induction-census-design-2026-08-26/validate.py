#!/usr/bin/env python3
"""Fail-closed validator for the nine-block census."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_nine_block_induction_census.json"


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def validate_schema(data):
    require(data["schema"] == "n8-x5-nine-block-induction-census-design-v1")
    require(data["status"] == "PASS_EXACT_CENSUS_ZERO_SOLVER")
    enum = data["enumeration"]
    require(enum["nine_added_supports"] == 167960)
    require(enum["fixed_identity_closed"] == 57308)
    require(enum["fixed_identity_evaders"] == 110652)
    require(enum["stable_nine_supports"] == 2329)
    require(enum["stable_variable_strata"] == 37264)
    require(enum["classification_census"] == {"fixed_identity_cap": 26380, "nonidentity_hyperplane_cap": 7408, "unresolved_coefficient_locus": 3476})
    require(enum["unresolved_records"] == 3476)
    deletion = data["deletion_parent_census"]
    require(deletion["unresolved_eight_parent_count_histogram"] == {"0": 920, "1": 732, "2": 1412, "3": 364, "4": 48})
    require(deletion["with_at_least_one_unresolved_eight_parent"] == 2556)
    require(deletion["genuinely_new_minimal_records"] == 920)
    require(deletion["scope"].startswith("parent relation only"))
    census = data["matching_essential_census"]
    require(census["essential_edge_histogram"] == {"12": 224, "13": 472, "14": 358, "15": 780, "16": 1108, "17": 534})
    require(census["with_degree_four_vertex"] == 3472)
    require(census["without_degree_four_vertex"] == 4)
    require(census["unlabelled_graph_classes"] == 191)
    require(census["literal_guard_orbits"] == 1778)
    require(census["guard_orbit_size_census"] == {"1": 80, "2": 1698})
    require(census["unique_labelled_essential_skeletons"] == 2628)
    require(len(data["unlabelled_graph_classes"]) == 191)
    require(len(data["literal_guard_orbits"]) == 1778)
    require(len(data["records"]) == 3476)
    require(sum(bool(record["unresolved_eight_deletion_parents"]) for record in data["records"]) == 2556)
    require(sum(record["has_degree_four_vertex"] for record in data["records"]) == 3472)
    frontier = data["frontier_interface_test"]
    require(frontier["accepted_coverage_now"] == 0)
    require(frontier["conditional_if_max15_terminal"] == 1834)
    require(frontier["conditional_if_max15_and_max16_terminal"] == 2938)
    require(frontier["still_open_after_max16"] == 538)
    require(frontier["still_open_breakdown"] == {"exact16_without_degree4": 4, "exact17_with_degree4": 534})
    require(frontier["genuinely_new"]["records"] == 920)
    require(frontier["genuinely_new"]["at_most15_eligible"] == 598)
    require(frontier["genuinely_new"]["exact16_additional_eligible"] == 242)
    require(frontier["genuinely_new"]["remaining_after_max16"] == 80)
    scope = data["scope"]
    require(scope["source_and_guard_provenance_only"] is True)
    require(scope["heavy_solver_runs"] == 0 and scope["singular_runs"] == 0)
    require(scope["external_frontier_theorem_promoted"] is False)
    require(scope["deletion_monotonicity_claim"] is False)
    require(scope["nine_block_layer_closed"] is False)
    require(scope["full_conjecture_claim"] is False)
    return True


def main():
    observed = json.loads(RESULT.read_text())
    validate_schema(observed)
    if __debug__:
        spec = importlib.util.spec_from_file_location("builder", HERE / "build_census.py")
        require(spec is not None and spec.loader is not None)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rebuilt = module.make_result()
        require(json.dumps(observed, sort_keys=True, separators=(",", ":")) == json.dumps(rebuilt, sort_keys=True, separators=(",", ":")), "semantic rebuild mismatch")
    print(json.dumps({"status": "PASS", "result_sha256": sha(RESULT)}, sort_keys=True))


if __name__ == "__main__":
    main()
