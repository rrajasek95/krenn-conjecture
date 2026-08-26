#!/usr/bin/env python3
"""Seal hardened rep5 launch machinery without launching arithmetic."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = HERE / "run_one_lane.py"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
SOURCE_REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25"
REJECTION = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-referee-2026-08-25"
PRIOR_HELD = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-2026-08-25"
PINS = {
    DESIGN / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    DESIGN / "results_rep5_contraction_design.json": "b2ba095f4f702ac2138cb40d45b7721a8df9b338900282020e83b791264df59b",
    DESIGN / "rep5_guard_minor_tiny_y_p32003.sing": "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
    SOURCE_REFEREE / "FINAL_MANIFEST.sha256": "ad86daeae93aaa154ef9ade124c719c8e683c3ae1b95130f948a2d90c0fc495a",
    SOURCE_REFEREE / "HELD_MODULAR_PILOT.json": "0df5f63b08cb3f601a5d77d22f07293e557f6dae6b7e727849916d943e5b70c7",
    REJECTION / "FINAL_MANIFEST.sha256": "02adea071c6f3eef5a4623ec25afb12f06dd38cec5426a7eed6ced74ff194dbb",
    REJECTION / "results_referee.json": "90ba1b91d1c7b27509227c74be7b03e0bb72aeac7ea8ab3a24ede4f39b500c14",
    PRIOR_HELD / "MANIFEST.sha256": "dcacfb67e77a36a3eeab2caff442b22695cf62ebce49f231c8151a52439985bc",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    Path("/usr/local/bin/gtimeout"): "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            value.update(chunk)
    return value.hexdigest()


def validate(value: dict) -> None:
    assert value["schema"] == "KRENN_X5_REP5_ALL_EQUAL_Y_MODULAR_HELD_V2"
    assert value["status"] == "HELD_PENDING_NEW_INDEPENDENT_ACCEPTANCE_AND_FRESH_CLEARANCE"
    assert value["lane"] == {"representative": "rep5", "chart": "all-equal-y/i0/p00/x0/y0/d01", "field": "F_32003", "variables": 91, "generators": 6577, "maximum_lane_count": 1}
    assert value["limits"] == {"native_wall_seconds": 180, "internal_wrapper_wall_seconds": 195, "rss_cap_bytes": 8589934592, "poll_seconds": 0.1, "term_then_kill_seconds": 5, "maximum_clearance_lifetime_seconds": 600}
    assert value["scope"] == {"launched": False, "ideal_runs": 0, "attempt_marker_created": False, "modular_lanes_authorized": 0, "exact_Q_authorized": False, "second_lane_authorized": False, "automatic_relaunch_authorized": False, "mathematical_coverage": False, "rep2_equivalence_used": False}


def hostile(value: dict, mutation) -> bool:
    candidate = copy.deepcopy(value)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
assert SOURCE.read_bytes() == (DESIGN / "rep5_guard_minor_tiny_y_p32003.sing").read_bytes()
assert sha256(SOURCE) == "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97"
rejection = json.loads((REJECTION / "results_referee.json").read_text())
assert rejection["status"] == "REJECT_LAUNCH_APPROVAL_HELD_SOURCE_ZERO_RUNS_PASS"
assert len(rejection["blocking_defects"]) == 6
assert {item["code"] for item in rejection["blocking_defects"]} == {
    "NO_FRESH_PROCESS_CENSUS", "RSS_OBSERVER_FAILS_OPEN", "RSS_NOT_PROCESS_GROUP_SUM",
    "WRAPPER_NOT_ENFORCED_BY_PINNED_RUNNER", "CLEARANCE_NOT_FRESH_OR_SINGLE_USE",
    "ABRUPT_FAILURE_CAN_BE_RELAUNCHED",
}
runner = RUNNER.read_text()
compile(runner, str(RUNNER), "exec")
for token in (
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids",
    "rusage observation failure for live group member", "process_group_rss_bytes",
    '[str(GTIMEOUT), "--signal=TERM"', 'f"{WRAPPER_WALL}s"',
    "MAX_CLEARANCE_LIFETIME_SECONDS = 600", 'clearance["nonce"]',
    'clearance["no_overlap_confirmed"] is True', "fresh_process_census()",
    'exclusive_json(HERE / "ATTEMPT.json"', 'not (HERE / stale).exists()',
    'atomic_json(HERE / "result.json"', "automatic_relaunch_authorized",
):
    assert token in runner, token

result = {
    "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_MODULAR_HELD_V2",
    "status": "HELD_PENDING_NEW_INDEPENDENT_ACCEPTANCE_AND_FRESH_CLEARANCE",
    "supersession": {
        "prior_held_manifest_sha256": PINS[PRIOR_HELD / "MANIFEST.sha256"],
        "independent_rejection_manifest_sha256": PINS[REJECTION / "FINAL_MANIFEST.sha256"],
        "independent_rejection_result_sha256": PINS[REJECTION / "results_referee.json"],
        "prior_launch_plan_approved": False,
        "source_provenance_preserved": True,
    },
    "lane": {"representative": "rep5", "chart": "all-equal-y/i0/p00/x0/y0/d01", "field": "F_32003", "variables": 91, "generators": 6577, "maximum_lane_count": 1},
    "source": {"path": SOURCE.name, "sha256": sha256(SOURCE), "bytes": SOURCE.stat().st_size, "byte_identical_to_refereed_source": True, "single_ring_and_solver_epilogue": True},
    "runner": {"path": RUNNER.name, "sha256": sha256(RUNNER), "direct_libproc_fresh_census": True, "fail_closed_rusage": True, "process_group_rss_sum": True, "internal_gtimeout_wrapper_seconds": 195, "exclusive_attempt_marker_before_popen": True, "stale_marker_tmp_output_refusal": True, "atomic_result_all_caught_outcomes": True},
    "clearance": {"independent_acceptance_schema": "independent_referee_acceptance.schema.json", "manager_clearance_schema": "launch_clearance.schema.json", "nonce_required": True, "issued_and_expiry_required": True, "maximum_lifetime_seconds": 600, "manager_resource_no_overlap_true_required": True, "census_policy_sha256": "bc690865397e276cba8d5d1d82445462c70203f1144df76f817cf361ec2ebf3b", "single_use": True},
    "limits": {"native_wall_seconds": 180, "internal_wrapper_wall_seconds": 195, "rss_cap_bytes": 8589934592, "poll_seconds": 0.1, "term_then_kill_seconds": 5, "maximum_clearance_lifetime_seconds": 600},
    "pins": {str(path if str(path).startswith("/usr/") else path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "interpretation": {"every_outcome": "diagnostic only", "unit": "does not prove characteristic zero or close rep5", "observer_or_process_failure": "fail closed; attempt consumed; no relaunch"},
    "scope": {"launched": False, "ideal_runs": 0, "attempt_marker_created": False, "modular_lanes_authorized": 0, "exact_Q_authorized": False, "second_lane_authorized": False, "automatic_relaunch_authorized": False, "mathematical_coverage": False, "rep2_equivalence_used": False},
}
validate(result)
tests = {
    "launch_injection": hostile(result, lambda x: x["scope"].__setitem__("launched", True)),
    "attempt_injection": hostile(result, lambda x: x["scope"].__setitem__("attempt_marker_created", True)),
    "Q_injection": hostile(result, lambda x: x["scope"].__setitem__("exact_Q_authorized", True)),
    "second_injection": hostile(result, lambda x: x["scope"].__setitem__("second_lane_authorized", True)),
    "relaunch_injection": hostile(result, lambda x: x["scope"].__setitem__("automatic_relaunch_authorized", True)),
    "wall_widening": hostile(result, lambda x: x["limits"].__setitem__("native_wall_seconds", 181)),
}
assert all(tests.values())
result["hostile_tests"] = tests
temporary = (HERE / "held_pilot.json.tmp")
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "held_pilot.json")
print(json.dumps({"status": result["status"], "runner_sha256": sha256(RUNNER), "source_sha256": sha256(SOURCE), "launched": False}, sort_keys=True))
