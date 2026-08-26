#!/usr/bin/env python3
"""Freeze the held one-lane contract and future acceptance schemas; zero run."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

H = Path(__file__).resolve().parent
SOURCE_SHA = "66bdb9277c9bff605e0d8a808ca65beb5967afaaf8ae494193286a60338355c6"
DERIVATION_SHA = "1e08d3d13f7c069a3991e6a2871838c7960ba31dc2a923ac673270207fa297ad"
RUNNER_SHA = "cec7089a43ddb82dc5f9654b5338a0dcc21f30fe2ace5640b8421dd7ef6ce656"
TIMEOUT_FINAL = "066347c8af9a579b8f09d1c1eebf0197e819753da839f30708616287c4336196"
TORUS = "1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282"
COMPARISON = "1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a"
GUARD = "6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee"
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


assert sha(H / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing") == SOURCE_SHA
assert sha(H / "source_derivation.json") == DERIVATION_SHA
assert sha(H / "run_one_lane.py") == RUNNER_SHA
policy = {
    "method": "libproc proc_listallpids + proc_pidpath",
    "forbidden_executable_basenames": [
        "Singular", "gtimeout", "sparse_d12_dual", "sparse_d12_dual_v4_1",
        "sparse_d12_dual_fixed_lane", "sparse_d12_dual_portfolio_audit",
    ],
    "self_pid_excluded": True,
}
policy_sha = hashlib.sha256(json.dumps(policy, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
held = {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_HELD_V1",
    "status": "HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE",
    "source": {
        "path": "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing",
        "sha256": SOURCE_SHA, "derivation_sha256": DERIVATION_SHA,
        "field": "F_32003", "variables": 67, "generators": 6574,
        "exact_Q_parent_sha256": "2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339",
    },
    "chart": {
        "torus_stratum": "A67=A12=0", "guard_pivot_k": 0,
        "logical_scope": "V(A67,A12) intersect D(b0)",
        "single_chart_closes_group16": False,
    },
    "pins": {
        "group16_timeout_final_manifest_sha256": TIMEOUT_FINAL,
        "torus_producer_manifest_sha256": TORUS,
        "comparison_referee_manifest_sha256": COMPARISON,
        "guard_pivot_design_manifest_sha256": GUARD,
        "runner_sha256": RUNNER_SHA,
        "singular_sha256": SINGULAR_SHA,
        "gtimeout_sha256": GTIMEOUT_SHA,
    },
    "execution": {
        "maximum_lane_count": 1, "native_wall_seconds": 240,
        "wrapper_wall_seconds": 255, "rss_cap_bytes": 8589934592,
        "direct_libproc_group_rss": True, "fresh_libproc_process_census": True,
        "atomic_result": True, "exclusive_attempt_marker": True,
        "strict_stop_after_any_outcome": True,
    },
    "authorization": {
        "independent_acceptance_present": False, "fresh_clearance_present": False,
        "exact_Q_authorized": False, "other_chart_authorized": False,
        "automatic_relaunch_authorized": False,
    },
    "scope": {
        "solver_runs": 0, "results": 0, "attempts": 0,
        "mathematical_coverage": False, "group16_closed": False,
        "prior_timeout_reused": False,
    },
}
atomic(H / "held_pilot.json", held)
refusal = {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_REFUSAL_V1",
    "status": "HELD_FAIL_CLOSED_ZERO_RUN",
    "required_absent_until_future_authority": [
        "independent_referee_acceptance.json", "launch_clearance.json",
    ],
    "runner_refuses": [
        "missing or malformed independent acceptance", "missing or stale clearance",
        "clearance lifetime over 600 seconds", "source/runner/tool/input pin mismatch",
        "any forbidden heavy process in fresh libproc census", "any stale attempt/result/tmp/lock",
        "process-group RSS observer failure", "RSS above 8 GiB", "native wall above 240 seconds",
        "wrapper wall above 255 seconds", "any second lane, exact-Q lane, other chart, or relaunch",
    ],
    "attempt_consumption": "ATTEMPT.json and RUN_EXCLUSIVE.lock are O_EXCL-created before Popen; every subsequent outcome consumes the lane",
    "present_acceptance_files": 0, "present_clearance_files": 0,
    "solver_runs": 0,
}
atomic(H / "refusal_contract.json", refusal)
hex64 = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
acceptance_properties = {
    "schema": {"const": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_INDEPENDENT_ACCEPTANCE_V1"},
    "status": {"const": "PASS_APPROVE_ONE_COMBINED_P32003_DIAGNOSTIC_ONLY"},
    "held_manifest_sha256": hex64,
    "source_derivation_sha256": {"const": DERIVATION_SHA},
    "source_sha256": {"const": SOURCE_SHA},
    "runner_sha256": {"const": RUNNER_SHA},
    "timeout_final_manifest_sha256": {"const": TIMEOUT_FINAL},
    "torus_producer_manifest_sha256": {"const": TORUS},
    "comparison_referee_manifest_sha256": {"const": COMPARISON},
    "guard_pivot_manifest_sha256": {"const": GUARD},
    "torus_stratum": {"const": "A67=A12=0"}, "guard_pivot_k": {"const": 0},
    "variables": {"const": 67}, "generators": {"const": 6574},
    "maximum_lane_count": {"const": 1}, "exact_Q_authorized": {"const": False},
    "other_chart_authorized": {"const": False}, "automatic_relaunch_authorized": {"const": False},
}
clearance_properties = {
    "schema": {"const": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_EXPLICIT_CLEARANCE_V1"},
    "status": {"const": "CLEARED_ONE_COMBINED_P32003_DIAGNOSTIC_ONLY"},
    "held_manifest_sha256": hex64, "independent_referee_acceptance_sha256": hex64,
    "source_sha256": {"const": SOURCE_SHA}, "runner_sha256": {"const": RUNNER_SHA},
    "singular_sha256": {"const": SINGULAR_SHA}, "gtimeout_sha256": {"const": GTIMEOUT_SHA},
    "nonce": {"type": "string", "pattern": "^[0-9a-f]{32}$"},
    "issued_at_utc": {"type": "string"}, "expires_at_utc": {"type": "string"},
    "maximum_lane_count": {"const": 1}, "native_wall_seconds": {"const": 240},
    "wrapper_wall_seconds": {"const": 255}, "rss_cap_bytes": {"const": 8589934592},
    "no_overlap_confirmed": {"const": True}, "manager_clearance_confirmed": {"const": True},
    "resource_clearance_confirmed": {"const": True},
    "census_policy_sha256": {"const": policy_sha}, "expected_census_match_count": {"const": 0},
    "exact_Q_authorized": {"const": False}, "other_chart_authorized": {"const": False},
    "automatic_relaunch_authorized": {"const": False},
}
for name, properties in (
    ("independent_referee_acceptance.schema.json", acceptance_properties),
    ("launch_clearance.schema.json", clearance_properties),
):
    atomic(H / name, {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
        "additionalProperties": False, "required": list(properties), "properties": properties,
    })
print(json.dumps({"status": held["status"], "source_sha256": SOURCE_SHA, "runner_sha256": RUNNER_SHA, "policy_sha256": policy_sha, "solver_runs": 0}, sort_keys=True))
