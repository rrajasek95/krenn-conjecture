#!/usr/bin/env python3
"""Freeze the normalized superseding held schedule and acceptance schemas."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SELECTED = list(range(38, 88))
LEDGER_SHA = "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172"
RUNNER_SHA = "b9fc730669e6e5fc4799e9efbf4e6f12b1f443acc004af9bc536be851c4d8388"
ADAPTER_SHA = "c9c3d365f0f2fb3c9a03656822b4112b245455745dd4f707367fff6c6c2e6d11"
NORMALIZED_SHA = "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76"
BASELINE_MANIFEST_SHA = "950e50ea1b1af733b5f20fad076357d29ee76a7b85009c7b93fcad76b1406c75"
BASELINE_RESULT_SHA = "a4a959cc1eb2392e64fc0c1d8e540deace8141ae43d50fbd7c30a14d6ef6c189"
NEXT25_MANIFEST_SHA = "b5de471b2cbd4f5197492c37f7f885f77059a9eced3e66830998c8edd5d62cde"
NEXT25_RESULT_SHA = "a2599e9cee2739fb372e1d45db9625dc999510eb58407609cb581e73acbce450"
BINDING_MANIFEST_SHA = "18e93f3a635496987e58320858bff91e93a965a72504bba7762a9e5675a6b341"
BINDING_RESULT_SHA = "e5f441d67b9e372e5946fd0de01b2bab0cc0d13b0bab729f8fceba3c0f3c0880"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


assert sha256(HERE / "source_ledger.json") == LEDGER_SHA
assert sha256(HERE / "run_next50_v2.py") == RUNNER_SHA
assert sha256(HERE / "normalize_next25_dependency.py") == ADAPTER_SHA
assert sha256(HERE / "normalized_next25_dependency.json") == NORMALIZED_SHA
ledger = json.loads((HERE / "source_ledger.json").read_text())
normalized = json.loads((HERE / "normalized_next25_dependency.json").read_text())
assert [lane["group_id"] for lane in ledger["lanes"]] == SELECTED
assert normalized["closed_union"] == list(range(38))
plan = {
    "schema": "KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_HELD_SCHEDULE_V2",
    "status": "HELD_ZERO_RUNS_NORMALIZED_DEPENDENCY_PENDING_NEW_ACCEPTANCE_AND_CLEARANCE",
    "supersedes_manifest_sha256": "db8aa8acd4977934273c28249ffba8930c102cec2fc10bad9d86edb7fa51423d",
    "selection": ledger["selection"],
    "lanes": ledger["lanes"],
    "source_ledger": {"path": "source_ledger.json", "sha256": LEDGER_SHA, "byte_identical_to_superseded": True, "total_bytes": sum(lane["source_bytes"] for lane in ledger["lanes"])},
    "dependency": {"adapter_path": "normalize_next25_dependency.py", "adapter_sha256": ADAPTER_SHA, "normalized_path": "normalized_next25_dependency.json", "normalized_sha256": NORMALIZED_SHA, "closed_union": list(range(38)), "binding_audit_manifest_sha256": BINDING_MANIFEST_SHA},
    "runner": {"path": "run_next50_v2.py", "sha256": RUNNER_SHA, "strict_sequential": True, "direct_libproc_process_group_rss": True, "fail_closed_rusage": True, "internal_gtimeout_wrapper": True, "atomic_per_lane_results": True, "single_use_batch_marker": True},
    "execution": {"native_wall_seconds_each": 240, "wrapper_wall_seconds_each": 250, "rss_cap_bytes_each": 8589934592, "maximum_lane_count": 50, "order": SELECTED, "parallel": False, "skip": False, "reorder": False, "relaunch": False, "stop_whole_batch_on": ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]},
    "scope": {"source_files_preserved": 50, "solver_launches": 0, "result_files": 0, "attempt_markers": 0, "acceptances": 0, "clearances": 0, "groups_newly_closed": 0, "mathematical_coverage": False},
}
atomic_json(HERE / "held_schedule_v2.json", plan)

hex64 = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
common = {
    "source_ledger_sha256": {"const": LEDGER_SHA}, "runner_sha256": {"const": RUNNER_SHA},
    "selected_group_ids": {"const": SELECTED}, "maximum_lane_count": {"const": 50},
    "dependency_adapter_sha256": {"const": ADAPTER_SHA}, "normalized_dependency_sha256": {"const": NORMALIZED_SHA},
    "baseline_manifest_sha256": {"const": BASELINE_MANIFEST_SHA}, "baseline_result_sha256": {"const": BASELINE_RESULT_SHA},
    "next25_terminal_manifest_sha256": {"const": NEXT25_MANIFEST_SHA}, "next25_terminal_result_sha256": {"const": NEXT25_RESULT_SHA},
    "binding_audit_manifest_sha256": {"const": BINDING_MANIFEST_SHA}, "binding_audit_result_sha256": {"const": BINDING_RESULT_SHA},
}
acceptance = {
    "schema": {"const": "KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_INDEPENDENT_ACCEPTANCE_V2"},
    "status": {"const": "PASS_APPROVE_STRICT_NORMALIZED_NEXT50_BATCH_ONLY"},
    "held_manifest_sha256": hex64, **common,
    "next25_terminal_closed_union": {"const": list(range(38))},
    "exact_Q_authorized": {"const": True}, "parallel_authorized": {"const": False},
    "skip_reorder_relaunch_authorized": {"const": False},
}
clearance = {
    "schema": {"const": "KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_EXPLICIT_CLEARANCE_V2"},
    "status": {"const": "CLEARED_STRICT_NORMALIZED_NEXT50_BATCH_ONLY"},
    "held_manifest_sha256": hex64, "independent_referee_acceptance_sha256": hex64, **common,
    "singular_sha256": {"const": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"},
    "gtimeout_sha256": {"const": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"},
    "native_wall_seconds_each": {"const": 240}, "wrapper_wall_seconds_each": {"const": 250},
    "rss_cap_bytes_each": {"const": 8589934592}, "no_overlap_confirmed": {"const": True},
    "parallel_authorized": {"const": False}, "skip_reorder_relaunch_authorized": {"const": False},
}
for name, properties in (("independent_referee_acceptance.schema.json", acceptance), ("launch_clearance.schema.json", clearance)):
    atomic_json(HERE / name, {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": list(properties), "properties": properties})
print(json.dumps({"status": plan["status"], "runner_sha256": RUNNER_SHA, "sources": 50, "solver_runs": 0}, sort_keys=True))
