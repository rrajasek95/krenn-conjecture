#!/usr/bin/env python3
"""Freeze the held groups88..137 schedule and future-hash schemas."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SELECTED = list(range(88, 138))
LEDGER_SHA = "2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b"
RUNNER_SHA = "604b0b938389e44506d627eba8652d74cfe3d3ba10a932efcb6c4dbfeee987e5"
SPEC_SHA = "1374fb5ed562ac0fd6b28ace616e09fbf011509555b02cb98996281d7188b380"
ADAPTER_SHA = "87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a"
BASELINE_MANIFEST_SHA = "7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da"
BASELINE_DEPENDENCY_SHA = "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


assert sha256(HERE / "source_ledger.json") == LEDGER_SHA
assert sha256(HERE / "run_groups88_137.py") == RUNNER_SHA
assert sha256(HERE / "future_groups38_87_dependency.json") == SPEC_SHA
assert sha256(HERE / "normalize_future_dependency.py") == ADAPTER_SHA
ledger = json.loads((HERE / "source_ledger.json").read_text())
dependency = json.loads((HERE / "future_groups38_87_dependency.json").read_text())
assert [lane["group_id"] for lane in ledger["lanes"]] == SELECTED
assert dependency["satisfied"] is False and dependency["future_manifest_sha256"] is None and dependency["future_result_sha256"] is None
plan = {
    "schema": "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_HELD_SCHEDULE_V1",
    "status": "HELD_ZERO_RUNS_FUTURE_GROUPS38_87_HASHES_ABSENT",
    "selection": ledger["selection"], "lanes": ledger["lanes"],
    "source_ledger": {"path": "source_ledger.json", "sha256": LEDGER_SHA, "total_bytes": sum(lane["source_bytes"] for lane in ledger["lanes"])},
    "dependency": {"spec_path": "future_groups38_87_dependency.json", "spec_sha256": SPEC_SHA, "adapter_path": "normalize_future_dependency.py", "adapter_sha256": ADAPTER_SHA, "proven_baseline_closed_union": list(range(38)), "required_future_groups": list(range(38, 88)), "required_closed_union": list(range(88)), "future_manifest_sha256": None, "future_result_sha256": None, "satisfied": False},
    "runner": {"path": "run_groups88_137.py", "sha256": RUNNER_SHA, "strict_sequential": True, "direct_libproc_process_group_rss": True, "fail_closed_rusage": True, "internal_gtimeout_wrapper": True, "atomic_per_lane_results": True, "single_use_batch_marker": True},
    "execution": {"native_wall_seconds_each": 240, "wrapper_wall_seconds_each": 250, "rss_cap_bytes_each": 8589934592, "maximum_lane_count": 50, "order": SELECTED, "parallel": False, "skip": False, "reorder": False, "relaunch": False, "stop_whole_batch_on": ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]},
    "scope": {"source_regeneration_only": True, "solver_launches": 0, "result_files": 0, "attempt_markers": 0, "acceptances": 0, "clearances": 0, "groups_newly_closed": 0, "mathematical_coverage": False},
}
atomic_json(HERE / "held_schedule.json", plan)
hex64 = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
common = {
    "source_ledger_sha256": {"const": LEDGER_SHA}, "runner_sha256": {"const": RUNNER_SHA},
    "selected_group_ids": {"const": SELECTED}, "maximum_lane_count": {"const": 50},
    "dependency_spec_sha256": {"const": SPEC_SHA}, "dependency_adapter_sha256": {"const": ADAPTER_SHA},
    "baseline_manifest_sha256": {"const": BASELINE_MANIFEST_SHA}, "baseline_dependency_sha256": {"const": BASELINE_DEPENDENCY_SHA},
    "future_terminal_manifest_sha256": hex64, "future_terminal_result_sha256": hex64,
}
acceptance = {
    "schema": {"const": "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1"},
    "status": {"const": "PASS_APPROVE_STRICT_GROUPS88_137_BATCH_ONLY"},
    "held_manifest_sha256": hex64, **common, "required_closed_union": {"const": list(range(88))},
    "exact_Q_authorized": {"const": True}, "parallel_authorized": {"const": False}, "skip_reorder_relaunch_authorized": {"const": False},
}
clearance = {
    "schema": {"const": "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_EXPLICIT_CLEARANCE_V1"},
    "status": {"const": "CLEARED_STRICT_GROUPS88_137_BATCH_ONLY"},
    "held_manifest_sha256": hex64, "independent_referee_acceptance_sha256": hex64, **common,
    "singular_sha256": {"const": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"},
    "gtimeout_sha256": {"const": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"},
    "native_wall_seconds_each": {"const": 240}, "wrapper_wall_seconds_each": {"const": 250}, "rss_cap_bytes_each": {"const": 8589934592},
    "no_overlap_confirmed": {"const": True}, "parallel_authorized": {"const": False}, "skip_reorder_relaunch_authorized": {"const": False},
}
for name, properties in (("independent_referee_acceptance.schema.json", acceptance), ("launch_clearance.schema.json", clearance)):
    atomic_json(HERE / name, {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": list(properties), "properties": properties})
print(json.dumps({"status": plan["status"], "groups": SELECTED, "runner_sha256": RUNNER_SHA, "future_hashes_present": False}, sort_keys=True))
