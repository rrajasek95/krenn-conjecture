#!/usr/bin/env python3
"""Fail-closed validator for the rank-one refinement design."""

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_rank1_refinement.json"


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
    require(data["schema"] == "n8-x5-exception1114-rank1-refinement-design-v1")
    require(data["status"] == "PASS_EXACT_REFINEMENT_ZERO_RUN")
    transport = data["transport_scope"]
    require(transport == {"representative": 1114, "records": [1114, 1978, 2014, 2036], "transport_orbits": 1, "no_cross_orbit_claim": True})
    require(data["parent_chart"] == {"variables": 81, "generators": 6566, "source_sha256": "273a246e6cd8747401da95f56086686bd9b0b91ae70e1c54671c1aaca8b311e6"})
    cover = data["exact_block_torus_cover"]
    require(cover["raw_profiles"] == 2187 and cover["residual_color_S2_orbits"] == 1094)
    require(cover["z0_orbits"] == 365 and cover["z12_orbits"] == 729)
    require(cover["z0_counts"] == {"variables": 65, "generators": 6554})
    require(cover["z12_counts"] == {"variables": 64, "generators": 6553})
    torus = data["torus"]
    require(torus["parent_torus_dimension"] == 10 and torus["rank_preserving"] is True)
    require(torus["block_character_determinant"] in ("1", "-1"))
    require(torus["ten_by_ten_weight_determinant"] in ("1", "-1"))
    require(len(torus["exact_block_torus_pivots"]) == 4 and len(torus["held_full_torus_extra_pivots"]) == 6)
    held = data["held_full_torus_subchart"]
    require(held["z"] == "z1=1" and held["variables"] == 58 and held["generators"] == 6553)
    require(len(held["normalized_source_coordinates"]) == 9)
    require(held["monic_scan_after_reduction"] == {"hits": 0, "records": []})
    require(held["proper_common_factor_scan"] == {"hits": 0, "records": []})
    ranks = data["irreducibility_diagnosis"]["rank_diagnostics"]
    require(ranks["variables"] == 58 and ranks["all_variables_active"] is True)
    require(ranks["exponent_difference_rank_mod_1000003"] == 58 and ranks["residual_grading_nullity"] == 0)
    require(ranks["jacobian_rank_lower_bound_over_Q"] >= 57)
    require(len(ranks["jacobian_modular_trials"]) == 2)
    require(data["irreducibility_diagnosis"]["full_Groebner_or_unit_claim"] is False)
    require(data["scope"] == {"singular_runs": 0, "sat_runs": 0, "large_cnf_reads": 0, "records_closed": 0, "full_conjecture_claim": False})

    if check_files:
        source_path = HERE / held["source_path"]
        plan_path = HERE / held["plan_path"]
        require(source_path.is_file() and sha(source_path) == held["source_sha256"])
        require(plan_path.is_file() and sha(plan_path) == held["plan_sha256"])
        program = source_path.read_text()
        ring = program.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
        require(len(ring) == len(set(ring)) == 58)
        lowered = program.lower()
        require("slimgb" not in lowered and "groebner" not in lowered and "reduce(1" not in lowered)
        require('print("INPUT_VARIABLES="' in program and 'print("INPUT_GENERATORS="' in program)
        plan = json.loads(plan_path.read_text())
        require(plan["status"] == "HELD_DIAGNOSTIC_ZERO_RUN")
        require(all(value is None for value in plan["dependencies"].values()))
        require(plan["source"]["sha256"] == held["source_sha256"])
        require(plan["source"]["variables"] == 58 and plan["source"]["generators"] == 6553)
        require(plan["refusal"].startswith("no Singular"))


def main():
    observed = json.loads(RESULT.read_text())
    validate_schema(observed)
    if __debug__:
        spec = importlib.util.spec_from_file_location("refinement_builder", HERE / "build_refinement.py")
        require(spec is not None and spec.loader is not None)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rebuilt = module.make_result()
        require(json.dumps(observed, sort_keys=True, separators=(",", ":")) == json.dumps(rebuilt, sort_keys=True, separators=(",", ":")), "semantic rebuild mismatch")
    print(json.dumps({"status": "PASS", "result_sha256": sha(RESULT)}, sort_keys=True))


if __name__ == "__main__":
    main()
