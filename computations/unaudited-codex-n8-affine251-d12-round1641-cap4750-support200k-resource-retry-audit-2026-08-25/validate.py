#!/usr/bin/env python3
import json
from pathlib import Path

d = json.loads((Path(__file__).parent / "results_resource_retry_audit.json").read_text())
assert d["status"] == "APPROVE_HELD_RESOURCE_ONLY_RETRY2"
assert d["attempt1"]["verdict"] == "REJECT_HARD_WALL_ZERO_COVERAGE"
assert d["attempt1"]["result_absent"] and d["attempt1"]["tmp_absent"]
assert d["attempt1"]["checkpoint_cache_equal_audited_r1640"]
assert d["retry_diff"]["only_changes"] == ["native wall 210 -> 300", "wrapper wall 240 -> 360"]
assert d["retry_acceptance"]["fresh_distinct_r1640_clone"]
assert d["retry_acceptance"]["exact_rounds"] == [1641]
assert d["retry_acceptance"]["r1642_absent"]
assert d["scope"] == {"metadata_only": True, "large_payload_replay": False, "clone": False, "launch": False}
print("PASS r1641 resource-only retry referee")
