#!/usr/bin/env python3
"""Static fail-closed audit of held r1464 interlocks and exact geometry."""
import ast
import hashlib
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: preflight requires assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
schedule = json.loads((HERE / "SCHEDULE.json").read_text())
assert schedule["status"] == "PREPARED_HELD_FOR_ROUND1463_FINAL_REPLAY_CLEAR_DISK_AND_RUNTIME_GATE"
assert not (HERE / "FUTURE_INPUT_PINS.json").exists()
assert not (HERE / "RESOURCE_CLEARANCE.json").exists()
texts = {}
for name in ("freeze_future_input.py", "freeze_resource_clearance.py", "run_gate.py", "validate.py"):
    texts[name] = (HERE / name).read_text()
    ast.parse(texts[name], filename=name)
assert 'AUDIT_RESULT_REL = "WAIT_FOR_ROUND1463_AUDIT_RESULT"' in texts["freeze_future_input.py"]
assert 'assert pins_path.exists(), "launch interlock: round1463 FINAL_REPLAY_CLEAR pins absent"' in texts["run_gate.py"]
assert 'assert clearance_path.exists(), "launch interlock: independent disk/runtime clearance absent"' in texts["run_gate.py"]
assert texts["run_gate.py"].index("assert pins_path.exists()") < texts["run_gate.py"].index("SOURCE =")
assert texts["run_gate.py"].index("assert clearance_path.exists()") < texts["run_gate.py"].index("SOURCE =")
assert 'command("portfolio", "auto", "best", 2250000, 520, 1)' in texts["run_gate.py"]
assert 'command("cap2500_candidate", "rare", "cold", 2500000, 180, 256)' in texts["run_gate.py"]
assert 'winner == ("cold", "rare")' in texts["validate.py"]
assert 'differences == [(left.index("2250000"), "2250000", "2500000")]' in texts["validate.py"]
assert schedule["resource_interlocks"]["minimum_free_bytes_before_any_clone"] == 64 << 30
assert schedule["resource_interlocks"]["portfolio_projection_status"] == "UNSAFE_UNTIL_FINAL_INPUT_AND_RUNTIME_REVIEW"
assert 'assert projected_seconds <= 500' in texts["freeze_resource_clearance.py"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


engine = schedule["engine"]
for path_key, hash_key in (
    ("audit_source_parent_manifest", "audit_source_parent_manifest_sha256"),
    ("source", "source_sha256"),
    ("binary", "binary_sha256"),
    ("watchdog540", "watchdog540_sha256"),
    ("provider", "provider_sha256"),
):
    assert sha256(REPO / engine[path_key]) == engine[hash_key]
assert sha256(REPO / schedule["provisional_lineage"]["round1448_gate_audit"] / "FINAL_MANIFEST.sha256") == \
    schedule["provisional_lineage"]["round1448_audit_manifest_sha256"]

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1464_PRELAUNCH_HOSTILES_V1",
    "status": "PASS_PREPARED_HELD_FAIL_CLOSED",
    "future_input_pins_absent": True,
    "resource_clearance_absent": True,
    "unresolved_placeholders_block_before_any_cache_read": True,
    "runner_blocks_before_source_or_cache_hash_and_before_clone": True,
    "scripts_parse": True,
    "portfolio_geometry_frozen": True,
    "cap2500_is_cold_rare_conditional": True,
    "sole_cap_difference_validator_frozen": True,
    "runtime_projection_must_be_at_most_500_seconds": True,
    "free_space_floor_gib": 64,
    "large_reads_or_clones": False,
    "solves": False,
}
(HERE / "hostile_preflight_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
