#!/usr/bin/env python3
"""Static/exact validator for the hardened zero-launch rep5 package."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = HERE / "run_one_lane.py"
DESIGN_SOURCE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/rep5_guard_minor_tiny_y_p32003.sing"


def sha256(path: Path) -> str:
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    return value


held = json.loads((HERE / "held_pilot.json").read_text())
assert held["schema"] == "KRENN_X5_REP5_ALL_EQUAL_Y_MODULAR_HELD_V2"
assert held["status"] == "HELD_PENDING_NEW_INDEPENDENT_ACCEPTANCE_AND_FRESH_CLEARANCE"
assert held["source"]["sha256"] == sha256(SOURCE) == "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97"
assert SOURCE.read_bytes() == DESIGN_SOURCE.read_bytes()
assert held["runner"]["sha256"] == sha256(RUNNER) == "9eaef175601f51dcd7a50321fc80d02dc71ec81b91a8f13f02116d3b76cdadb9"
assert held["scope"] == {"launched": False, "ideal_runs": 0, "attempt_marker_created": False, "modular_lanes_authorized": 0, "exact_Q_authorized": False, "second_lane_authorized": False, "automatic_relaunch_authorized": False, "mathematical_coverage": False, "rep2_equivalence_used": False}
assert all(held["hostile_tests"].values())
runner = RUNNER.read_text()
compile(runner, str(RUNNER), "exec")
for token in ("proc_listallpids", "proc_pidpath", "proc_listpgrppids", "process_group_rss_bytes", "rusage observation failure for live group member", '[str(GTIMEOUT), "--signal=TERM"', 'f"{WRAPPER_WALL}s"', "MAX_CLEARANCE_LIFETIME_SECONDS = 600", 'clearance["no_overlap_confirmed"] is True', "fresh_process_census()", 'exclusive_json(HERE / "ATTEMPT.json"', 'not (HERE / stale).exists()', 'atomic_json(HERE / "result.json"'):
    assert token in runner, token
for name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((HERE / name).read_text())
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(schema["properties"])
assert json.loads((HERE / "launch_clearance.schema.json").read_text())["properties"]["census_policy_sha256"] == {"const": "bc690865397e276cba8d5d1d82445462c70203f1144df76f817cf361ec2ebf3b"}
refusal = json.loads((HERE / "refusal_contract.json").read_text())
assert refusal["status"] == "ARMED_ZERO_LAUNCH_SINGLE_USE" and len(refusal["defect_repairs"]) == 6
for stale in ("ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json", "independent_referee_acceptance.json", "launch_clearance.json"):
    assert not (HERE / stale).exists(), stale
assert not any(HERE.glob("*.tmp"))
print(json.dumps({"status": "PASS_SUPERSEDING_HELD_ZERO_LAUNCH", "source_sha256": sha256(SOURCE), "runner_sha256": sha256(RUNNER), "defects_repaired": 6, "attempt_present": False, "result_present": False}, sort_keys=True))
