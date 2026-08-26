#!/usr/bin/env python3
"""Fail-closed validation of the zero-launch rep5 held package."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25"
ORIGINAL = DESIGN / "rep5_guard_minor_tiny_y_p32003.sing"
SOURCE = HERE / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = HERE / "run_one_lane.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


held = json.loads((HERE / "held_pilot.json").read_text())
assert held["schema"] == "KRENN_X5_REP5_ALL_EQUAL_Y_MODULAR_HELD_V1"
assert held["status"] == "HELD_PENDING_EXPLICIT_CLEARANCE"
assert held["lane"] == {
    "representative": "rep5",
    "chart": "all-equal-y/i0/p00/x0/y0/d01",
    "field": "F_32003",
    "variables": 91,
    "generators": 6577,
    "maximum_lane_count": 1,
}
assert held["limits"] == {
    "native_wall_seconds": 180,
    "wrapper_wall_seconds": 195,
    "rss_cap_bytes": 8589934592,
    "poll_seconds": 0.1,
    "term_then_kill_seconds": 5,
}
assert held["scope"] == {
    "launched": False,
    "ideal_runs": 0,
    "modular_lanes_authorized": 0,
    "exact_Q_authorized": False,
    "second_lane_authorized": False,
    "automatic_relaunch_authorized": False,
    "rep5_closed": False,
    "transport_claimed": False,
    "rep2_equivalence_used": False,
    "mathematical_coverage": False,
}
assert all(held["hostile_tests"].values())
assert SOURCE.read_bytes() == ORIGINAL.read_bytes()
assert sha256(SOURCE) == "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97"
assert held["modular_source"]["sha256"] == sha256(SOURCE)
assert held["runner_contract"]["sha256"] == sha256(RUNNER)
assert held["pins"][str((REFEREE / "FINAL_MANIFEST.sha256").relative_to(ROOT))] == "ad86daeae93aaa154ef9ade124c719c8e683c3ae1b95130f948a2d90c0fc495a"

program = SOURCE.read_text()
assert program.count("ring r=32003,") == 1 and "ring r=0," not in program
for token in (
    "ideal G=slimgb(I);", "poly remainder=reduce(1,G);",
    "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED",
    "INPUT_VARIABLES=", "INPUT_GENERATORS=", "quit;",
):
    assert program.count(token) == 1, token

runner = RUNNER.read_text()
compile(runner, str(RUNNER), "exec")
for token in (
    'ctypes.CDLL("/usr/lib/libproc.dylib")',
    "NATIVE_WALL = 180", "WRAPPER_WALL = 195", "RSS_CAP = 8 * 1024**3",
    'acceptance_path = HERE / "independent_referee_acceptance.json"',
    'clearance_path = HERE / "launch_clearance.json"',
    'REFEREE / "FINAL_MANIFEST.sha256"',
    'REFEREE / "HELD_MODULAR_PILOT.json"',
    "start_new_session=True", "os.killpg", 'atomic_json(HERE / "result.json"',
    '"rep2_equivalence_used": False',
):
    assert token in runner, token

assert not (HERE / "independent_referee_acceptance.json").exists()
assert not (HERE / "launch_clearance.json").exists()
assert not (HERE / "result.json").exists()
assert not any(HERE.glob("*.tmp"))

clearance_schema = json.loads((HERE / "launch_clearance.schema.json").read_text())
assert clearance_schema["additionalProperties"] is False
assert clearance_schema["properties"]["wrapper_wall_seconds"] == {"const": 195}
assert clearance_schema["properties"]["native_wall_seconds"] == {"const": 180}
assert clearance_schema["properties"]["rss_cap_bytes"] == {"const": 8589934592}
assert clearance_schema["properties"]["runner_sha256"] == {"const": sha256(RUNNER)}
assert set(clearance_schema["required"]) == set(clearance_schema["properties"])

refusal = json.loads((HERE / "refusal_contract.json").read_text())
assert refusal == {
    "clearance_files_present_at_seal": 0,
    "fail_before_popen_on": [
        "missing or malformed MANIFEST.sha256",
        "missing or non-byte-identical independent referee acceptance",
        "missing or non-exact manager launch clearance",
        "source, runner, binary, producer, or referee pin mismatch",
        "pre-existing result.json",
    ],
    "forbidden": {
        "automatic_relaunch": True,
        "exact_Q": True,
        "rep2_source_or_transport": True,
        "second_lane": True,
    },
    "refusal_probe": {
        "popen_reached": False,
        "result_created": False,
        "runner_exit_code": 1,
        "trigger": "missing sealed MANIFEST.sha256 before seal",
    },
    "result_present_at_seal": False,
    "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_REFUSAL_CONTRACT_V1",
    "status": "ARMED_ZERO_LAUNCH",
}

print(json.dumps({
    "status": "PASS_HELD_ZERO_LAUNCH",
    "source_sha256": sha256(SOURCE),
    "runner_sha256": sha256(RUNNER),
    "referee_manifest_sha256": sha256(REFEREE / "FINAL_MANIFEST.sha256"),
    "clearances_present": 0,
    "result_present": False,
    "rep2_equivalence_used": False,
}, sort_keys=True))
