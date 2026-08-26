#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_referee.json"
result = json.loads(path.read_text())
assert result["status"] == "APPROVE_HELD_CONTRACT_ONLY_NOT_LAUNCHED"
assert result["producer_manifest_sha256"] == "2a0d0426ee8eb9e836ca493ab3154e127f705d2e78cdb94600b612abb31cf337"
assert result["producer_plan_sha256"] == "e778f68f78c087a2d63f4491e0d67d9920302dc55cd2d39e80abc380f66c6ce4"
assert result["wholly_new_sibling_no_old_attempt_reuse"] is True
assert result["old_batch_terminal_zero_coverage"] is True
assert result["external_process_listing_commands"] == []
assert result["source_regenerated_sha256"] == "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04"
assert result["source_counts"] == {"variables": 91, "generators": 6577}
assert result["lane"] == {"group_id": 15, "field": "Q", "maximum_lanes": 1, "native_wall_seconds": 240, "wrapper_wall_seconds": 250, "rss_limit_bytes": 8589934592}
assert result["atomic_and_stop_contract"] == "PASS" and all(result["hostile_tests"].values())
assert result["launch_authorized"] is False and result["runner_present"] is False
assert result["runner_requires_separate_pin_and_clearance"] is True
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))
