#!/usr/bin/env python3
"""Freeze a conditional next-50 schedule that cannot precede next25 terminal PASS."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER_SHA = "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172"
RUNNER_SHA = "eba736280a2d724cc1c46370d85292d7543f7bfd46a7e51e813c5bfe6ce0b66e"
DEPENDENCY_SHA = "aba4c9792cd2874269722f678864130cfde27c30caa47d505249a77ada82c896"
SELECTED = list(range(38, 88))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


ledger = json.loads((HERE / "source_ledger.json").read_text())
dependency = json.loads((HERE / "future_next25_dependency.json").read_text())
assert sha256(HERE / "source_ledger.json") == LEDGER_SHA
assert sha256(HERE / "run_next50.py") == RUNNER_SHA
assert sha256(HERE / "future_next25_dependency.json") == DEPENDENCY_SHA
assert [lane["group_id"] for lane in ledger["lanes"]] == SELECTED
assert dependency["status"] == "UNSATISFIED_PLACEHOLDER_BLOCKS_LAUNCH" and dependency["satisfied"] is False
plan = {
    "schema": "KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_HELD_SCHEDULE_V1",
    "status": "HELD_ZERO_RUNS_CONDITIONAL_ON_FUTURE_NEXT25_PASS",
    "selection": ledger["selection"],
    "lanes": ledger["lanes"],
    "source_ledger": {"path": "source_ledger.json", "sha256": LEDGER_SHA, "total_bytes": sum(lane["source_bytes"] for lane in ledger["lanes"])},
    "runner": {"path": "run_next50.py", "sha256": RUNNER_SHA, "strict_sequential": True, "direct_libproc_process_group_rss": True, "fail_closed_rusage": True, "internal_gtimeout_wrapper": True, "atomic_per_lane_results": True, "single_use_batch_marker": True},
    "future_dependency": {"path": "future_next25_dependency.json", "sha256": DEPENDENCY_SHA, "currently_satisfied": False, "future_manifest_hash_placeholder": None, "future_result_hash_placeholder": None, "runner_requires_later_acceptance_to_bind_both_exact_hashes": True},
    "execution": {"native_wall_seconds_each": 240, "wrapper_wall_seconds_each": 250, "rss_cap_bytes_each": 8589934592, "maximum_lane_count": 50, "order": SELECTED, "parallel": False, "skip": False, "reorder": False, "relaunch": False, "stop_whole_batch_on": ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]},
    "acceptance": {"field": "Q", "variables": 91, "generators": 6577, "unit_requires": ["returncode=0", "termination=null", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"], "scope_each": "one canonical common-S3 group"},
    "clearance": {"independent_acceptance_required": True, "future_next25_terminal_PASS_required": True, "explicit_batch_clearance_required": True, "files_present_at_seal": 0},
    "scope": {"source_regeneration_only": True, "solver_launches": 0, "result_files": 0, "attempt_markers": 0, "clearances": 0, "groups_newly_closed": 0, "representative_closed": False, "mathematical_coverage": False},
}
atomic_json(HERE / "held_schedule.json", plan)

hex64 = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
acceptance_properties = {
    "schema": {"const": "KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1"},
    "status": {"const": "PASS_APPROVE_STRICT_CONDITIONAL_NEXT50_BATCH_ONLY"},
    "held_manifest_sha256": hex64,
    "source_ledger_sha256": {"const": LEDGER_SHA},
    "runner_sha256": {"const": RUNNER_SHA},
    "selected_group_ids": {"const": SELECTED},
    "maximum_lane_count": {"const": 50},
    "future_dependency_spec_sha256": {"const": DEPENDENCY_SHA},
    "next25_terminal_manifest_sha256": hex64,
    "next25_terminal_result_sha256": hex64,
    "next25_terminal_closed_union": {"const": list(range(38))},
    "exact_Q_authorized": {"const": True},
    "parallel_authorized": {"const": False},
    "skip_reorder_relaunch_authorized": {"const": False},
}
clearance_properties = {
    "schema": {"const": "KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_EXPLICIT_CLEARANCE_V1"},
    "status": {"const": "CLEARED_STRICT_CONDITIONAL_NEXT50_BATCH_ONLY"},
    "held_manifest_sha256": hex64,
    "independent_referee_acceptance_sha256": hex64,
    "source_ledger_sha256": {"const": LEDGER_SHA},
    "runner_sha256": {"const": RUNNER_SHA},
    "singular_sha256": {"const": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"},
    "gtimeout_sha256": {"const": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"},
    "selected_group_ids": {"const": SELECTED},
    "future_dependency_spec_sha256": {"const": DEPENDENCY_SHA},
    "next25_terminal_manifest_sha256": hex64,
    "next25_terminal_result_sha256": hex64,
    "native_wall_seconds_each": {"const": 240},
    "wrapper_wall_seconds_each": {"const": 250},
    "rss_cap_bytes_each": {"const": 8589934592},
    "no_overlap_confirmed": {"const": True},
    "maximum_lane_count": {"const": 50},
    "parallel_authorized": {"const": False},
    "skip_reorder_relaunch_authorized": {"const": False},
}
for name, properties in (("independent_referee_acceptance.schema.json", acceptance_properties), ("launch_clearance.schema.json", clearance_properties)):
    atomic_json(HERE / name, {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": list(properties), "properties": properties})
print(json.dumps({"status": plan["status"], "groups": SELECTED, "runner_sha256": RUNNER_SHA, "future_dependency_satisfied": False}, sort_keys=True))
