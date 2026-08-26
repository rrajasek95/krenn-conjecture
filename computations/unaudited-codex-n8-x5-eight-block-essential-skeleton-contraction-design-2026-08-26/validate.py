#!/usr/bin/env python3
"""Fail-closed validator for the essential-skeleton/contraction design."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_essential_skeleton_contraction_design.json"


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def validate_schema(data, check_files=True):
    require(data["schema"] == "n8-x5-eight-block-essential-skeleton-contraction-design-v1")
    require(data["status"] == "PASS_EXACT_CENSUS__HELD_ONE_CHART_ZERO_RUN")
    census = data["essential_skeleton_census"]
    require(census["unresolved_records"] == 616)
    require(census["all_have_degree_four_vertex"] is True)
    require(census["essential_edge_histogram"] == {"12": 88, "13": 104, "14": 124, "15": 184, "16": 116})
    require(census["at_most_15_records"] == 500)
    require(census["exact_16_records"] == 116)
    require(census["diagnostic_signature_classes"] == 32)
    require(census["unlabelled_graph_classes_all"] == 51)
    require(census["unlabelled_graph_classes_exact16"] == 16)
    require(census["exact16_graph_class_size_census"] == {"4": 5, "8": 10, "16": 1})
    require(census["exact16_literal_guard_orbits"] == 58)
    require(census["exact16_guard_orbit_size"] == 2)
    require(len(data["exact16_graph_classes"]) == 16)
    require(len(data["exact16_guard_orbits"]) == 58)
    require(len(data["all_record_details"]) == 616)
    require(sum(d["essential_edge_count"] <= 15 for d in data["all_record_details"]) == 500)
    require(sum(d["essential_edge_count"] == 16 for d in data["all_record_details"]) == 116)
    require(all(d["degree_four_vertices"] for d in data["all_record_details"]))
    interfaces = data["degree_four_interfaces"]
    require(interfaces["fresh_at_most15"]["proof_status"] == "ACTIVE_UNPROMOTED_PRELAUNCH_ONLY")
    require(interfaces["fresh_at_most15"]["accepted_coverage_now"] == 0)
    require(interfaces["fresh_at_most15"]["conditional_coverage_after_current_cnf_drat_replay"] == 500)
    require(interfaces["historical_exact16"]["eligible_current_records"] == 116)
    require(interfaces["historical_exact16"]["status_here"].startswith("IDENTIFIED_HYPOTHESIS_ONLY"))
    require(interfaces["historical_exact17"]["eligible_current_records"] == 0)
    require(interfaces["unconditional_closed_by_external_interfaces_now"] == 0)
    chart = data["smallest_contracted_held_chart"]
    require(chart["orbit"] == 1)
    require(chart["pre_substitution_variables"] == 171)
    require(chart["contracted_variables"] == 82)
    require(chart["listed_generators"] == 6566)
    require(chart["expanded_polynomial_terms"] == 23011)
    require(chart["largest_generator_terms"] == 12)
    require(chart["further_constant_coefficient_monic_pivots"] == 0)
    require(abs(chart["torus_selected_minor_determinant"]) == 1)
    require(chart["solve_status"] == "ZERO_RUN_HELD")
    require(chart["scope"] == "one exact diagnostic chart; not the other chart or orbit strata")
    if check_files:
        require(sha(HERE / "orbit1_diagonal_i0_k0_all00_q.sing") == chart["q_source_sha256"])
        require(sha(HERE / "orbit1_diagonal_i0_k0_all00_p32003.sing") == chart["p32003_source_sha256"])
        plan = json.loads((HERE / "held_pilot_plan.json").read_text())
        require(plan["status"] == "HELD_ZERO_RUN_NO_CLEARANCE")
        require(plan["refusal"].startswith("no clearance artifact"))
        require(plan["source_sha256"] == chart["p32003_source_sha256"])
    scope = data["scope"]
    require(scope["legacy_theorem_imported"] is False)
    require(scope["fresh_drat_result_imported"] is False)
    require(scope["singular_runs"] == 0 and scope["heavy_solver_runs"] == 0)
    require(scope["deletion_monotonicity_claim"] is False)
    require(scope["eight_block_layer_closed"] is False)
    require(scope["full_conjecture_claim"] is False)
    return True


def main():
    observed = json.loads(RESULT.read_text())
    validate_schema(observed)
    if __debug__:
        spec = importlib.util.spec_from_file_location("build_design", HERE / "build_design.py")
        require(spec is not None and spec.loader is not None)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rebuilt = module.make_result()
        require(
            json.dumps(observed, sort_keys=True, separators=(",", ":")) ==
            json.dumps(rebuilt, sort_keys=True, separators=(",", ":")),
            "byte-semantic rebuild mismatch",
        )
    print(json.dumps({
        "status": "PASS",
        "result_sha256": sha(RESULT),
        "q_source_sha256": sha(HERE / "orbit1_diagonal_i0_k0_all00_q.sing"),
        "p32003_source_sha256": sha(HERE / "orbit1_diagonal_i0_k0_all00_p32003.sing"),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
