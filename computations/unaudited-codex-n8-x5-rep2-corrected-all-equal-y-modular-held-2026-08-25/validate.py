#!/usr/bin/env python3
"""Validate the held rep2 modular pilot without launching Singular."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
Q_SOURCE = DESIGN / "rep2_corrected_guard_minor_tiny_y_Q.sing"
MOD_SOURCE = HERE / "rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = HERE / "run_one_lane.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


held = json.loads((HERE / "held_pilot.json").read_text())
assert held["schema"] == "KRENN_X5_REP2_ALL_EQUAL_Y_MODULAR_HELD_V1"
assert held["status"] == "HELD_PENDING_INDEPENDENT_REFEREE_AND_EXPLICIT_CLEARANCE"
assert held["lane"] == {
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
    "modular_lanes_authorized": 0,
    "exact_Q_authorized": False,
    "second_lane_authorized": False,
    "automatic_relaunch_authorized": False,
    "mathematical_coverage": False,
}
assert all(held["hostile_tests"].values())

assert held["modular_source"]["sha256"] == sha256(MOD_SOURCE)
assert held["runner_contract"]["sha256"] == sha256(RUNNER)
assert held["runner_contract"]["launch_command_after_both_clearances"] == "gtimeout 195 python3 run_one_lane.py"

q_program = Q_SOURCE.read_text()
modular = MOD_SOURCE.read_text()
epilogue = "\n".join([
    "ideal G=slimgb(I);",
    'print("GROEBNER_SIZE="+string(size(G)));',
    "poly remainder=reduce(1,G);",
    'print("UNIT_REMAINDER="+string(remainder));',
    'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
    "quit;",
])
expected = q_program.replace("ring r=0,", "ring r=32003,", 1).replace("quit;", epilogue, 1)
assert modular == expected
assert q_program.count("ring r=0,") == modular.count("ring r=32003,") == 1
assert modular.count("slimgb(I)") == modular.count("reduce(1,G)") == 1
assert modular.count("STATUS=UNIT_IDEAL") == modular.count("STATUS=NONUNIT_OR_UNRESOLVED") == 1

runner = RUNNER.read_text()
compile(runner, str(RUNNER), "exec")
for token in (
    'ctypes.CDLL("/usr/lib/libproc.dylib")',
    "NATIVE_WALL = 180", "WRAPPER_WALL = 195", "RSS_CAP = 8 * 1024**3",
    'referee_path = HERE / "independent_referee_acceptance.json"',
    'clearance_path = HERE / "launch_clearance.json"',
    "start_new_session=True", "os.killpg", "atomic_json(HERE / \"result.json\"",
):
    assert token in runner, token

assert not (HERE / "independent_referee_acceptance.json").exists()
assert not (HERE / "launch_clearance.json").exists()
assert not (HERE / "result.json").exists()
assert not any(HERE.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_HELD_ZERO_LAUNCH",
    "source_sha256": sha256(MOD_SOURCE),
    "runner_sha256": sha256(RUNNER),
    "clearances_present": 0,
    "result_present": False,
}, sort_keys=True))
