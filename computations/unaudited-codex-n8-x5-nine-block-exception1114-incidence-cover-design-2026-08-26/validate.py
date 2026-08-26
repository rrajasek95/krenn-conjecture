#!/usr/bin/env python3
"""Fail-closed validator for the representative-1114 design package."""

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_exception1114_design.json"


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def validate_schema(data, check_files=True):
    require(data["schema"] == "n8-x5-nine-block-exception1114-incidence-cover-design-v1")
    require(data["status"] == "PASS_DESIGN_ONLY_ZERO_IDEAL_RUNS")
    require(data["transport"]["representative"] == 1114)
    require(data["transport"]["records"] == [1114, 1978, 2014, 2036])
    require(data["transport"]["orbit_count"] == 1 and data["transport"]["group_order"] == 8)
    require(set(data["transport"]["site_maps"]) == {"1114", "1978", "2014", "2036"})

    source = data["source_system"]
    require(source["matrix_variables_before_reduction"] == 108)
    require(source["matching_count"] == 15 and len(source["supported_matchings"]) == 15)
    require(source["full_x5_equations"] == 6561 and source["guard_scalar_equations"] == 45)
    require(len(source["guards"]) == 5)
    linear = data["linear_reduction"]
    require(linear["variables"] == 90 and linear["residual_guard_scalars"] == 27)
    require(linear["base_generators_with_full_x5"] == 6588)

    carriers = data["carriers"]
    require(carriers["all_supported_carriers"] == 416)
    require(carriers["load_histogram"] == {"2": 16, "3": 32, "4": 44, "5": 72, "6": 72, "7": 40, "8": 8, "10": 56, "11": 32, "12": 44})
    require(carriers["minimum_load"] == 2 and carriers["minimum_carriers"] == 16)
    require(set(carriers["useful_oriented_factors"]) == {"F04", "F17", "F26", "F35"})
    require(set(carriers["selected_factorization_source_terms"]) == {"F04", "F17", "F26", "F35"})

    cover = data["rank_and_incidence_cover"]
    require(cover["raw_profiles"] == 625 and cover["simultaneous_color_S3_orbits"] == 150)
    require(cover["orbit_size_census"] == {"1": 16, "3": 65, "6": 69})
    require(cover["uncontracted_count_range"] == {"variables": [91, 126], "generators": [6589, 6624]})
    require(cover["cramer"]["raw_pivot_charts"] == 14641 and cover["cramer"]["S3_orbits"] == 2486)
    ranks = data["H_rank_split_inside_all_invertible"]
    require(ranks["exact_support_excludes_rank0"] is True)
    require(ranks["rank3"]["raw_minor_charts"] == 20 and ranks["rank3"]["S3_minor_orbits"] == 6)
    require(ranks["rank3"]["counts_after_substitution"] == {"variables": 83, "generators": 6572})
    require(ranks["rank2"]["full_half_rank_subcharts"] == {"raw": 27, "S3_orbits": 5, "variables": 87, "generators": 6572})
    require(ranks["rank1"]["raw_charts"] == 54 and ranks["rank1"]["S3_orbits"] == 10)
    require(ranks["rank1"]["counts"] == {"variables": 81, "generators": 6566})
    require(ranks["refined_complete_cover"] == {"raw_branches": 645, "S3_orbit_branches": 156, "derivation": "replace the all-I profile by one rank(H)<=2 branch and the 20 rank3 minor charts (6 S3 orbits)"})

    torus = data["torus"]
    require(torus["variables"] == 108 and torus["exact_rank_over_Q"] == 98 and torus["torus_nullity"] == 10)
    require(torus["rank_over_p1000003"] == 98 and torus["block_scaling_subtorus_dimension"] == 4)
    held = data["held_smallest_chart"]
    require(held["variables"] == 81 and held["generators"] == 6566)
    scope = data["scope"]
    require(scope == {"transport_orbits": 1, "ideal_runs": 0, "singular_runs": 0, "large_cnf_reads": 0, "records_closed": 0, "conjecture_claim": False})

    if check_files:
        for group, path_key, hash_key in (
            (carriers, "ledger_path", "ledger_sha256"),
            (cover, "ledger_path", "ledger_sha256"),
            (torus, "nullspace_basis_path", "nullspace_basis_sha256"),
            (held, "plan_path", "plan_sha256"),
            (held, "source_path", "source_sha256"),
        ):
            path = HERE / group[path_key]
            require(path.is_file() and sha(path) == group[hash_key], (path, "hash"))
        plan = json.loads((HERE / held["plan_path"]).read_text())
        require(plan["status"] == "HELD_DESIGN_ONLY_NO_CLEARANCE")
        require(all(value is None for value in plan["dependencies"].values()))
        require(plan["source"]["variables"] == 81 and plan["source"]["generators"] == 6566)
        require(plan["source"]["sha256"] == held["source_sha256"])
        require(plan["refusal"].startswith("no Singular"))
        program = (HERE / held["source_path"]).read_text()
        ring = program.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
        require(len(ring) == len(set(ring)) == 81)
        require(program.count("\n") > 6566)
        lowered = program.lower()
        require("slimgb" not in lowered and "groebner" not in lowered and "reduce(1" not in lowered)
        require('print("INPUT_VARIABLES="' in program and 'print("INPUT_GENERATORS="' in program)
        basis = json.loads((HERE / torus["nullspace_basis_path"]).read_text())
        require(len(basis["variable_order"]) == 108 and len(basis["basis"]) == 10)
        require(all(vector for vector in basis["basis"]))


def main():
    observed = json.loads(RESULT.read_text())
    validate_schema(observed)
    if __debug__:
        spec = importlib.util.spec_from_file_location("exception1114_builder", HERE / "build_design.py")
        require(spec is not None and spec.loader is not None)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rebuilt = module.make_result()
        require(
            json.dumps(observed, sort_keys=True, separators=(",", ":")) == json.dumps(rebuilt, sort_keys=True, separators=(",", ":")),
            "semantic rebuild mismatch",
        )
    print(json.dumps({"status": "PASS", "result_sha256": sha(RESULT)}, sort_keys=True))


if __name__ == "__main__":
    main()
