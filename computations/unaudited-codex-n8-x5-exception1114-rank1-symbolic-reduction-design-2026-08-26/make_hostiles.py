#!/usr/bin/env python3
"""Create result mutations that the strict validator must reject."""

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / "results_symbolic_reduction.json").read_text())
hostiles = {}


def add(name, mutation):
    value = copy.deepcopy(base)
    mutation(value)
    path = HERE / f"hostile_{name}.json"
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    hostiles[name] = path.name


add("status", lambda x: x.__setitem__("status", "PASS"))
add("solve_count", lambda x: x["scope"].__setitem__("singular_runs", 1))
add("closed", lambda x: x["scope"].__setitem__("records_closed", 4))
add("rank", lambda x: x["exact_generator_reduction"].__setitem__("exact_Q_rank", 6534))
add("relation_count", lambda x: x["exact_generator_reduction"].__setitem__("signed_relation_count", 19))
add("relation_sign", lambda x: x["exact_generator_reduction"]["relations"][0]["coefficients"].__setitem__("342", -1))
add("removed", lambda x: x["exact_generator_reduction"]["removed_original_equation_indices"].__setitem__(0, 341))
add("minor", lambda x: x["jacobian"].__setitem__("determinant_mod_prime", 0))
add("site", lambda x: x["source_site_symmetry"].__setitem__("formal_guard_stabilizer_order", 2))
add("orbits", lambda x: x["source_site_symmetry"].__setitem__("residual_color_S2_orbits", 1093))
add("rank_profiles", lambda x: x["determinantal_rank_strata"].__setitem__("rank_profiles", 26))
add("monic", lambda x: x["elimination_exhaustion"]["localized_unit_coefficient_scan"].__setitem__("hits", [{"fake": True}]))

(HERE / "hostiles.json").write_text(json.dumps({"count": len(hostiles), "files": hostiles}, indent=2, sort_keys=True) + "\n")
print(len(hostiles))
