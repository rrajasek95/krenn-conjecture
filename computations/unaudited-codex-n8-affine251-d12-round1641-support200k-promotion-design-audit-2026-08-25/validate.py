#!/usr/bin/env python3
import json
from pathlib import Path

data = json.loads((Path(__file__).parent / "results_support200k_design_audit.json").read_text())
assert data["status"] == "APPROVE_HELD_SUPPORT200K_DIRECT_PROMOTION"
assert data["source_referee"]["support_cap_token_count"] == 7
assert data["source_referee"]["occurrence_lines"] == [1630, 1728, 1766, 1797, 3188, 3783]
assert data["semantic_diff"]["only_changed_frozen_literal"] == "support_cap: 100000 -> 200000"
assert data["control_referee"]["lower_cap_control_necessary"] is False
assert data["projection"]["conservative_next_support"] == 131506
assert data["projection"]["selected_cap"] == 200000
assert data["acceptance"]["exact_rounds"] == [1641]
assert data["acceptance"]["round1642_absent"] is True
assert data["scope"] == {"metadata_only": True, "large_read": False, "clone": False, "launch": False}
print("PASS independent r1641 support200k held-design audit")
