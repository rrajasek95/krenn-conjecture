#!/usr/bin/env python3
import json
from pathlib import Path

d = json.loads((Path(__file__).parent / "results_retry3_audit.json").read_text())
assert d["status"] == "APPROVE_HELD_FINAL_RESOURCE_RETRY3"
assert d["retry2"]["verdict"] == "REJECT_HARD_WALL_ZERO_COVERAGE"
assert d["retry3_diff"]["only_changes"] == ["native wall 300 -> 450", "wrapper wall 360 -> 540"]
assert d["retry3_diff"]["last_permitted_escalation"] is True
assert d["retry3_diff"]["any_failure_action"].startswith("STOP_THIS_GEOMETRY")
assert d["acceptance"]["fresh_distinct_audited_r1640_clone"] is True
assert d["acceptance"]["exact_rounds"] == [1641] and d["acceptance"]["r1642_absent"] is True
assert d["scope"] == {"metadata_only": True, "large_payload_rehash": False, "clone": False, "launch": False}
print("PASS final retry3 resource referee")
