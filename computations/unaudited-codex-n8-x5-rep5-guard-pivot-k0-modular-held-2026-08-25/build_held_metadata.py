#!/usr/bin/env python3
"""Build fail-closed zero-run metadata and schemas for the rep5 k0 pilot."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rep5_p00_guardpivot_k0_p32003.sing"
RUNNER = HERE / "run_one_lane.py"
SOURCE_SHA = "dc04c72252144d1a8ff798f49aa1130b1742fff342f21eaf02146b889e3370c1"
RUNNER_SHA = "fdaaea4fead4ec7d47f0a513fa6b8c74a04e4821d1abb4751d32806f9cabc965"
DESIGN_MANIFEST_SHA = "00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9"
Q_SHA = "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1"
REFEREE_MANIFEST_SHA = "af4bee0ca8db5391aac9f59cb1e52051d32e66fdb2974a126468b054ca3f5a4b"
HELD_PLAN_SHA = "acf0923735e96633389f8df6a74a0a35c3700fd9fd77ee28e1deffd1d8bac796"
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
CENSUS_POLICY_SHA = "bc690865397e276cba8d5d1d82445462c70203f1144df76f817cf361ec2ebf3b"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


assert sha256(SOURCE) == SOURCE_SHA
assert sha256(RUNNER) == RUNNER_SHA
compile(RUNNER.read_text(), str(RUNNER), "exec")

held = {
    "schema": "KRENN_X5_REP5_GUARD_PIVOT_K0_MODULAR_HELD_V1",
    "status": "HELD_ZERO_RUN_PENDING_INDEPENDENT_ACCEPTANCE_AND_FRESH_CLEARANCE",
    "lane": {
        "representative": "rep5",
        "chart": "p00/guard-pivot/k0",
        "field": 32003,
        "variables": 88,
        "generators": 6574,
        "maximum_lane_count": 1,
    },
    "source": {
        "path": SOURCE.name,
        "sha256": SOURCE_SHA,
        "bytes": SOURCE.stat().st_size,
        "source_Q_sha256": Q_SHA,
        "derivation": "replace sole literal ring r=0, by ring r=32003,; no other byte change",
        "expected_referee_modular_sha256": SOURCE_SHA,
    },
    "runner": {
        "path": RUNNER.name,
        "sha256": RUNNER_SHA,
        "fresh_direct_libproc_process_census": True,
        "process_group_rss_sum": True,
        "fail_closed_rusage_observer": True,
        "internally_pinned_wrapper": True,
        "exclusive_attempt_before_popen": True,
        "atomic_terminal_result": True,
        "stale_attempt_tmp_output_refusal": True,
    },
    "limits": {
        "native_wall_seconds": 240,
        "wrapper_wall_seconds": 250,
        "rss_cap_bytes": 8589934592,
        "maximum_clearance_lifetime_seconds": 600,
    },
    "pins": {
        "design_manifest_sha256": DESIGN_MANIFEST_SHA,
        "source_Q_sha256": Q_SHA,
        "design_referee_manifest_sha256": REFEREE_MANIFEST_SHA,
        "held_plan_sha256": HELD_PLAN_SHA,
        "singular_sha256": SINGULAR_SHA,
        "gtimeout_sha256": GTIMEOUT_SHA,
    },
    "scope": {
        "launched": False,
        "solver_runs": 0,
        "attempt_marker_created": False,
        "modular_lanes_authorized": 0,
        "exact_Q_authorized": False,
        "other_k_authorized": False,
        "automatic_relaunch_authorized": False,
        "mathematical_coverage": False,
    },
}

refusal = {
    "schema": "KRENN_X5_REP5_GUARD_PIVOT_K0_REFUSAL_CONTRACT_V1",
    "status": "ARMED_HELD_ZERO_RUN_SINGLE_USE",
    "refuse_without": [
        "independent_referee_acceptance.json matching its fail-closed schema",
        "fresh launch_clearance.json with nonce and <=600-second lifetime",
        "manager/resource/no-overlap booleans all true",
        "fresh direct-libproc census with zero forbidden process matches",
        "exact source, runner, input, tool, referee, and held-plan pins",
    ],
    "refuse_on": [
        "any stale attempt/result/log/watchdog/tmp artifact",
        "any live forbidden solver or D12 executable",
        "any process-group member with unobservable rusage while wrapper is live",
        "any source/schema/pin/limit mismatch",
    ],
    "terminal_policy": "every attempt is consumed before popen; stop and seal after any outcome",
    "forbidden": {"exact_Q": True, "other_k": True, "relaunch": True, "parallel": True},
}

hex64 = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
acceptance_properties = {
    "schema": {"const": "KRENN_X5_REP5_GUARD_PIVOT_K0_INDEPENDENT_ACCEPTANCE_V1"},
    "status": {"const": "PASS_APPROVE_ONE_GUARD_PIVOT_K0_MODULAR_DIAGNOSTIC_ONLY"},
    "held_manifest_sha256": hex64,
    "source_sha256": {"const": SOURCE_SHA},
    "runner_sha256": {"const": RUNNER_SHA},
    "design_manifest_sha256": {"const": DESIGN_MANIFEST_SHA},
    "source_Q_sha256": {"const": Q_SHA},
    "design_referee_manifest_sha256": {"const": REFEREE_MANIFEST_SHA},
    "held_plan_sha256": {"const": HELD_PLAN_SHA},
    "singular_sha256": {"const": SINGULAR_SHA},
    "gtimeout_sha256": {"const": GTIMEOUT_SHA},
    "field": {"const": 32003},
    "pivot_k": {"const": 0},
    "variables": {"const": 88},
    "generators": {"const": 6574},
    "maximum_lane_count": {"const": 1},
    "exact_Q_authorized": {"const": False},
    "other_k_authorized": {"const": False},
    "automatic_relaunch_authorized": {"const": False},
}
acceptance_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": list(acceptance_properties),
    "properties": acceptance_properties,
}
clearance_properties = {
    "schema": {"const": "KRENN_X5_REP5_GUARD_PIVOT_K0_EXPLICIT_LAUNCH_CLEARANCE_V1"},
    "status": {"const": "CLEARED_ONE_GUARD_PIVOT_K0_MODULAR_DIAGNOSTIC_ONLY"},
    "held_manifest_sha256": hex64,
    "independent_referee_acceptance_sha256": hex64,
    "source_sha256": {"const": SOURCE_SHA},
    "runner_sha256": {"const": RUNNER_SHA},
    "singular_sha256": {"const": SINGULAR_SHA},
    "gtimeout_sha256": {"const": GTIMEOUT_SHA},
    "nonce": {"type": "string", "pattern": "^[0-9a-f]{32}$"},
    "issued_at_utc": {"type": "string", "format": "date-time"},
    "expires_at_utc": {"type": "string", "format": "date-time"},
    "maximum_lane_count": {"const": 1},
    "native_wall_seconds": {"const": 240},
    "wrapper_wall_seconds": {"const": 250},
    "rss_cap_bytes": {"const": 8589934592},
    "no_overlap_confirmed": {"const": True},
    "manager_clearance_confirmed": {"const": True},
    "resource_clearance_confirmed": {"const": True},
    "census_policy_sha256": {"const": CENSUS_POLICY_SHA},
    "expected_census_match_count": {"const": 0},
    "exact_Q_authorized": {"const": False},
    "other_k_authorized": {"const": False},
    "automatic_relaunch_authorized": {"const": False},
}
clearance_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": list(clearance_properties),
    "properties": clearance_properties,
}

atomic_json(HERE / "held_pilot.json", held)
atomic_json(HERE / "refusal_contract.json", refusal)
atomic_json(HERE / "independent_referee_acceptance.schema.json", acceptance_schema)
atomic_json(HERE / "launch_clearance.schema.json", clearance_schema)
print(json.dumps({"status": held["status"], "source_sha256": SOURCE_SHA, "runner_sha256": RUNNER_SHA}, sort_keys=True))
