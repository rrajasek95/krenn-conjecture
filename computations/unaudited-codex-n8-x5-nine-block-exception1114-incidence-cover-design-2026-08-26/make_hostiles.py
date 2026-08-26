#!/usr/bin/env python3
"""Generate fail-closed hostile-schema evidence without any ideal run."""

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "results_exception1114_design.json").read_text())
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
    "transport_overclaim": rejected(lambda value: value["transport"].__setitem__("orbit_count", 0)),
    "missing_record": rejected(lambda value: value["transport"]["records"].pop()),
    "matching_count": rejected(lambda value: value["source_system"].__setitem__("matching_count", 14)),
    "full_x5_count": rejected(lambda value: value["source_system"].__setitem__("full_x5_equations", 6560)),
    "guard_count": rejected(lambda value: value["source_system"].__setitem__("guard_scalar_equations", 44)),
    "carrier_count": rejected(lambda value: value["carriers"].__setitem__("all_supported_carriers", 415)),
    "incidence_raw": rejected(lambda value: value["rank_and_incidence_cover"].__setitem__("raw_profiles", 624)),
    "incidence_orbits": rejected(lambda value: value["rank_and_incidence_cover"].__setitem__("simultaneous_color_S3_orbits", 149)),
    "cramer_overclaim": rejected(lambda value: value["rank_and_incidence_cover"]["cramer"].__setitem__("S3_orbits", 2485)),
    "rank3_count": rejected(lambda value: value["H_rank_split_inside_all_invertible"]["rank3"].__setitem__("S3_minor_orbits", 5)),
    "rank1_variable": rejected(lambda value: value["H_rank_split_inside_all_invertible"]["rank1"]["counts"].__setitem__("variables", 80)),
    "torus_rank": rejected(lambda value: value["torus"].__setitem__("exact_rank_over_Q", 97)),
    "run_injection": rejected(lambda value: value["scope"].__setitem__("ideal_runs", 1)),
    "closure_overclaim": rejected(lambda value: value["scope"].__setitem__("records_closed", 4)),
}
if not all(tests.values()):
    raise RuntimeError({name: outcome for name, outcome in tests.items() if not outcome})
(HERE / "results_hostiles.json").write_text(json.dumps({"status": "PASS", "count": len(tests), "tests": tests}, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS", "count": len(tests)}, sort_keys=True))
