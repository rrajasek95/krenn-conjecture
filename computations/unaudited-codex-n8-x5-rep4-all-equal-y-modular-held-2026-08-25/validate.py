#!/usr/bin/env python3
"""Validate the rep4 held package without launching Singular."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-referee-2026-08-25"
Q_SOURCE = DESIGN / "rep4_guard_minor_tiny_y_Q.sing"
SOURCE = HERE / "rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = HERE / "run_one_lane.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


held = json.loads((HERE / "held_pilot.json").read_text())
assert held["schema"] == "KRENN_X5_REP4_ALL_EQUAL_Y_MODULAR_HELD_V1"
assert held["status"] == "HELD_PENDING_EXPLICIT_CLEARANCE"
assert held["lane"] == {
    "representative": "rep4", "chart": "all-equal-y/i0/p00/x0/y0/d01",
    "field": "F_32003", "variables": 91, "generators": 6577, "maximum_lane_count": 1,
}
assert held["limits"] == {
    "native_wall_seconds": 180, "wrapper_wall_seconds": 195,
    "rss_cap_bytes": 8589934592, "poll_seconds": 0.1, "term_then_kill_seconds": 5,
}
assert held["scope"] == {
    "launched": False, "ideal_runs": 0, "modular_lanes_authorized": 0,
    "exact_Q_authorized": False, "second_lane_authorized": False,
    "automatic_relaunch_authorized": False, "rep4_closed": False,
    "transport_claimed": False, "cross_representative_equivalence_used": False,
    "mathematical_coverage": False,
}
assert all(held["hostile_tests"].values())
assert held["pins"][str((REFEREE / "FINAL_MANIFEST.sha256").relative_to(ROOT))] == "185b51b8107d5dcf12e7194a7d806157e0df6a2b6d047cf4adc6c8ac400fa4ae"
assert held["pins"][str((REFEREE / "ONE_CHART_MODULAR_HELD_PLAN.json").relative_to(ROOT))] == "ee484b5a58d63cef6ed60c81760a790b06be363426678f50031f9891fb149203"

q_program = Q_SOURCE.read_text()
epilogue = "\n".join([
    "ideal G=slimgb(I);", 'print("GROEBNER_SIZE="+string(size(G)));',
    "poly remainder=reduce(1,G);", 'print("UNIT_REMAINDER="+string(remainder));',
    'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
    "quit;",
])
expected = q_program.replace("ring r=0,", "ring r=32003,", 1).replace("quit;", epilogue, 1)
assert SOURCE.read_text() == expected
assert sha256(SOURCE) == "9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524"
assert SOURCE.stat().st_size == 1764288
assert held["modular_source"]["sha256"] == sha256(SOURCE)
assert held["runner_contract"]["sha256"] == sha256(RUNNER)

runner = RUNNER.read_text()
compile(runner, str(RUNNER), "exec")
for token in (
    'ctypes.CDLL("/usr/lib/libproc.dylib")', "proc_listpgrppids",
    "process_group_rss_bytes", "NATIVE_WALL = 180", "WRAPPER_WALL = 195",
    "RSS_CAP = 8 * 1024**3", 'acceptance_path = HERE / "independent_referee_acceptance.json"',
    'clearance_path = HERE / "launch_clearance.json"',
    'REFEREE / "ONE_CHART_MODULAR_HELD_PLAN.json"', "start_new_session=True",
    "os.killpg", 'atomic_json(HERE / "result.json"',
    '"cross_representative_equivalence_used": False',
):
    assert token in runner, token

schema = json.loads((HERE / "launch_clearance.schema.json").read_text())
assert schema["additionalProperties"] is False
assert set(schema["required"]) == set(schema["properties"])
assert schema["properties"]["runner_sha256"] == {"const": sha256(RUNNER)}
assert schema["properties"]["source_sha256"] == {"const": sha256(SOURCE)}
assert schema["properties"]["native_wall_seconds"] == {"const": 180}
assert schema["properties"]["wrapper_wall_seconds"] == {"const": 195}
assert schema["properties"]["rss_cap_bytes"] == {"const": 8589934592}

refusal = json.loads((HERE / "refusal_contract.json").read_text())
assert refusal["schema"] == "KRENN_X5_REP4_ALL_EQUAL_Y_REFUSAL_CONTRACT_V1"
assert refusal["status"] == "ARMED_ZERO_LAUNCH"
assert refusal["clearance_files_present_at_seal"] == 0
assert refusal["result_present_at_seal"] is False
assert all(refusal["forbidden"].values())
assert not (HERE / "independent_referee_acceptance.json").exists()
assert not (HERE / "launch_clearance.json").exists()
assert not (HERE / "result.json").exists()
assert not any(HERE.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_HELD_ZERO_LAUNCH", "source_sha256": sha256(SOURCE),
    "runner_sha256": sha256(RUNNER), "referee_manifest_sha256": sha256(REFEREE / "FINAL_MANIFEST.sha256"),
    "clearances_present": 0, "result_present": False,
    "cross_representative_equivalence_used": False,
}, sort_keys=True))
