#!/usr/bin/env python3
"""Hostile-schema checks for the rank-one refinement."""

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "results_rank1_refinement.json").read_text())
spec = importlib.util.spec_from_file_location("validator", HERE / "validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def rejected(mutator):
    candidate = copy.deepcopy(DATA)
    mutator(candidate)
    try:
        validator.validate_schema(candidate, check_files=False)
    except Exception:
        return True
    return False


tests = {
    "cross_transport": rejected(lambda value: value["transport_scope"].__setitem__("no_cross_orbit_claim", False)),
    "parent_variable": rejected(lambda value: value["parent_chart"].__setitem__("variables", 80)),
    "cover_raw": rejected(lambda value: value["exact_block_torus_cover"].__setitem__("raw_profiles", 2186)),
    "cover_orbit": rejected(lambda value: value["exact_block_torus_cover"].__setitem__("residual_color_S2_orbits", 1093)),
    "z0_count": rejected(lambda value: value["exact_block_torus_cover"]["z0_counts"].__setitem__("variables", 64)),
    "z12_count": rejected(lambda value: value["exact_block_torus_cover"]["z12_counts"].__setitem__("generators", 6552)),
    "torus_dimension": rejected(lambda value: value["torus"].__setitem__("parent_torus_dimension", 9)),
    "torus_determinant": rejected(lambda value: value["torus"].__setitem__("ten_by_ten_weight_determinant", "2")),
    "held_variable": rejected(lambda value: value["held_full_torus_subchart"].__setitem__("variables", 57)),
    "monic_hidden": rejected(lambda value: value["held_full_torus_subchart"]["monic_scan_after_reduction"].__setitem__("hits", 1)),
    "factor_hidden": rejected(lambda value: value["held_full_torus_subchart"]["proper_common_factor_scan"].__setitem__("hits", 1)),
    "grading_rank": rejected(lambda value: value["irreducibility_diagnosis"]["rank_diagnostics"].__setitem__("exponent_difference_rank_mod_1000003", 57)),
    "run_injection": rejected(lambda value: value["scope"].__setitem__("singular_runs", 1)),
    "closure_overclaim": rejected(lambda value: value["scope"].__setitem__("records_closed", 4)),
}
if not all(tests.values()):
    raise RuntimeError({name: outcome for name, outcome in tests.items() if not outcome})
(HERE / "results_hostiles.json").write_text(json.dumps({"status": "PASS", "count": len(tests), "tests": tests}, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS", "count": len(tests)}, sort_keys=True))
