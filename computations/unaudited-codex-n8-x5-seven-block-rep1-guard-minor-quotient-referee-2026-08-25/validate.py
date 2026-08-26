#!/usr/bin/env python3
"""Strict small-file validator for the independent quotient referee."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

result = json.loads((HERE / "results_referee.json").read_text())
plan = json.loads((HERE / "RESOURCE_PLAN.json").read_text())

assert result["schema"] == "KRENN_X5_REP1_GUARD_MINOR_QUOTIENT_REFEREE_V1"
assert result["status"] == "PASS_EXACT_DESIGN_ONLY_NO_CLOSURE"
assert result["equivalence"] == {
    "A06_cramer_entries": 9,
    "combined_saturation_exact": True,
    "forward_reverse_localization": True,
    "partner_entries": 3,
    "tautological_guard_rows_removed": 3,
    "two_minor_cover": True,
    "v_w_independence": True,
}
assert result["census"] == {
    "all_equal_y_minor_orbits": 1,
    "orbit_sizes": {"6": 162},
    "raw": 972,
    "s3_orbits": 162,
    "y_orbits": 81,
    "z_orbits": 81,
}
assert result["counts"] == {"generators": 6577, "variables": 91}
assert result["scope"] == {"D12_reads": False, "design_only": True, "ideal_runs": 0, "rep1_closed": False}

assert plan["status"] == "APPROVE_HELD_NOT_RUN"
assert plan["limits"]["maximum_lane_count"] == 1
assert plan["limits"]["native_wall_seconds"] == 300
assert plan["limits"]["wrapper_wall_seconds"] == 310
assert plan["limits"]["rss_cap_bytes"] == 8 * 1024**3
assert plan["lane"]["field"] == "F_32003"
assert "all-equal-y" in plan["lane"]["chart"]
assert "no rep1 or characteristic-zero closure" in plan["interpretation"]["unit_ideal"]
assert "no second modular chart and no exact-Q lane regardless of outcome" in plan["required_controls"]

print(json.dumps({"status": "PASS", "design": result["status"], "launches": 0}, sort_keys=True))
