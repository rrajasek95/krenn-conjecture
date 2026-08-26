#!/usr/bin/env python3
import json
from pathlib import Path

d = json.loads((Path(__file__).parent / "results_cap4750_design_audit.json").read_text())
assert d["status"] == "APPROVE_HELD_CAP4750_SUPPORT200K_ONE_ROUND"
assert d["shock_policy"]["declared_bound"] == 450725
assert d["shock_policy"]["cap4500000_shortfall"] == 20436
assert d["shock_policy"]["cap4750000_margin"] == 229564
assert d["column_cap_theorem"]["sole_normalized_command_diff"] == "--column-cap 4250000 -> 4750000"
assert d["dependency_binding"]["this_audit_binds_the_independent_diagnostic"] is True
assert d["acceptance"]["exact_rounds"] == [1641] and d["acceptance"]["r1642_absent"] is True
assert d["scope"] == {"metadata_only": True, "large_candidate_read": False, "clone": False, "launch": False}
print("PASS independent held cap4.75/support200k design audit")
