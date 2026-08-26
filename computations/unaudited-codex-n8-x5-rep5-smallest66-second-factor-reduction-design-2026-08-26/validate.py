#!/usr/bin/env python3
"""Fail-closed validation of the second-factor producer and referee records."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
design = json.loads((HERE / "results_design.json").read_text())
referee = json.loads((HERE / "results_referee.json").read_text())
hostiles = json.loads((HERE / "results_hostiles.json").read_text())
assert design["status"] == "PASS_EXACT_SECOND_FACTOR_COVER_NO_TORUS_MONIC_OR_LITERAL_MINOR_REDUCTION"
assert referee["status"] == "PASS_EXACT_SECOND_FACTOR_COVER_DESIGN_ONLY"
assert referee["design_sha256"] == sha(HERE / "results_design.json")
assert referee["input_sha256"] == design["input"]["sha256"] == "4821a045e6f4c799a002a9d097c7353857b8058f4dfdb01b1048d09b5dcd6927"
assert referee["coordinate"] == design["selected_cover"]["selected_coordinate"] == "a04_00"
assert referee["factor_count"] == design["selected_cover"]["divisible_generators"] == 108
assert referee["grading_rank"] == 66 and referee["grading_nullity"] == 0 and referee["linear_rank"] == 39
assert referee["minor_tests"] == design["minor_rank_split"]["available_candidates"] == 47
assert referee["source_sizes"] == {"D": [67, 3592, 137579], "V": [65, 3483, 128231]}
for kind, digest in referee["source_hashes"].items():
    assert digest == sha(HERE / f"sources/{kind}_a04_00_Q_design.sing")
assert hostiles["status"] == "PASS_17_HOSTILES" and all(hostiles["tests"].values())
assert design["scope"]["singular_runs"] == referee["singular_runs"] == 0
assert design["scope"]["mathematical_coverage_added"] is referee["closure_added"] is False
print(json.dumps({"status": "PASS_DESIGN_VALIDATED", "sources": 2, "hostiles": 17, "solves": 0}, sort_keys=True))
