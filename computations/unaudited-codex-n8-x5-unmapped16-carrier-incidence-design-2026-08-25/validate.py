#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "results_unmapped16_design.json").read_text())
assert result["schema"] == "KRENN_X5_UNMAPPED16_CARRIER_INCIDENCE_DESIGN_V1"
assert result["status"] == "PASS_RECONSTRUCTION_AND_SINGULAR_BRANCH_REDUCTION"
assert result["census"] == {"records": 16, "orbit_ids": 8, "matchings_per_record": 8,
                            "no_anchor_records": 12, "no_rectangle_records": 4,
                            "mathematically_closed_records": 0}
assert len(result["records"]) == 16
assert all(r["carrier_scan"] == {"triangle": 560, "star": 168} for r in result["records"])
assert all(r["two_sandwich_census"]["total"] in (24, 40) for r in result["records"])
selected = result["selected_reduction"]
assert selected["support"] == ["01", "15", "17", "23", "26", "46", "47"]
assert selected["guard"]["reduced"] == "(I-A17*A26)*A47^T=0"
assert selected["singular_branch"]["rank_chart_census"] == {"raw_per_rank": 27, "S3_orbits_per_rank": 5}
assert result["scope"] == {"large_groebner_runs": 0, "mathematically_closed_records": 0,
                           "full_conjecture": False}
assert all(result["hostile_tests"].values())
print(json.dumps({"status": "PASS", "result_sha256": digest(HERE / "results_unmapped16_design.json")},
                 sort_keys=True))
