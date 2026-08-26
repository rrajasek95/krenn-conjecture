#!/usr/bin/env python3
"""Freeze the strict held rep2 first-25 schedule and refusal schemas."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER_SHA = "20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e"
CENSUS_SHA = "5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a"
RUNNER_SHA = "0727e5e5961f90cd14d3d79f836634bf7df9fff1b8d44bd463678db1f8f72ff2"
CLOSED_MANIFEST_SHA = "c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a"
CLOSED_SECOND_REFEREE_SHA = "c856fae641e355a94684c1c9304ead831d213ecc90f579c0a751c93002c10562"
SELECTED = list(range(1, 26))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


assert sha256(HERE / "source_ledger.json") == LEDGER_SHA
assert sha256(HERE / "canonical_census.json") == CENSUS_SHA
assert sha256(HERE / "run_first25.py") == RUNNER_SHA
ledger = json.loads((HERE / "source_ledger.json").read_text())
assert ledger["selection"]["excluded_proven_group_ids"] == [0]
assert ledger["selection"]["selected_group_ids"] == SELECTED
assert ledger["closed_dependency"]["first_seal_manifest_sha256"] == CLOSED_MANIFEST_SHA
assert ledger["closed_dependency"]["second_referee_manifest_sha256"] == CLOSED_SECOND_REFEREE_SHA
plan = {
    "schema": "KRENN_X5_REP2_FIRST25_EXACT_Q_HELD_SCHEDULE_V1",
    "status": "HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT_AND_CLEARANCE",
    "selection": ledger["selection"],
    "closed_dependency": ledger["closed_dependency"],
    "lanes": ledger["lanes"],
    "source_ledger": {"path": "source_ledger.json", "sha256": LEDGER_SHA, "total_bytes": sum(lane["source_bytes"] for lane in ledger["lanes"])},
    "canonical_census": {"path": "canonical_census.json", "sha256": CENSUS_SHA, "raw": 972, "groups": 162},
    "runner": {"path": "run_first25.py", "sha256": RUNNER_SHA, "strict_sequential": True, "direct_libproc_process_group_rss": True, "fail_closed_rusage": True, "internal_gtimeout_wrapper": True, "atomic_per_lane_results": True, "single_use_batch_marker": True},
    "execution": {"native_wall_seconds_each": 240, "wrapper_wall_seconds_each": 250, "rss_cap_bytes_each": 8589934592, "maximum_lane_count": 25, "order": SELECTED, "parallel": False, "skip": False, "reorder": False, "relaunch": False, "stop_whole_batch_on": ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]},
    "acceptance": {"field": "Q", "variables": 91, "generators": 6577, "unit_requires": ["returncode=0", "termination=null", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"], "scope_each": "one canonical common-S3 group of rep2"},
    "clearance": {"independent_acceptance_required": True, "fresh_explicit_batch_clearance_required": True, "files_present_at_seal": 0},
    "scope": {"representative": "rep2 only", "source_regeneration_only": True, "solver_launches": 0, "result_files": 0, "attempt_markers": 0, "clearances": 0, "groups_newly_closed": 0, "rep2_closed": False, "mathematical_coverage_added": False, "cross_representative_transport": False},
}
atomic(HERE / "held_schedule.json", plan)

hex64 = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
acceptance_properties = {
    "schema": {"const": "KRENN_X5_REP2_FIRST25_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1"},
    "status": {"const": "PASS_APPROVE_STRICT_REP2_FIRST25_BATCH_ONLY"},
    "held_manifest_sha256": hex64,
    "source_ledger_sha256": {"const": LEDGER_SHA},
    "runner_sha256": {"const": RUNNER_SHA},
    "already_closed_group_id": {"const": 0},
    "closed_manifest_sha256": {"const": CLOSED_MANIFEST_SHA},
    "closed_second_referee_manifest_sha256": {"const": CLOSED_SECOND_REFEREE_SHA},
    "selected_group_ids": {"const": SELECTED},
    "maximum_lane_count": {"const": 25},
    "exact_Q_authorized": {"const": True},
    "parallel_authorized": {"const": False},
    "skip_reorder_relaunch_authorized": {"const": False},
}
clearance_properties = {
    "schema": {"const": "KRENN_X5_REP2_FIRST25_EXACT_Q_EXPLICIT_CLEARANCE_V1"},
    "status": {"const": "CLEARED_STRICT_REP2_FIRST25_BATCH_ONLY"},
    "held_manifest_sha256": hex64,
    "independent_referee_acceptance_sha256": hex64,
    "source_ledger_sha256": {"const": LEDGER_SHA},
    "runner_sha256": {"const": RUNNER_SHA},
    "singular_sha256": {"const": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"},
    "gtimeout_sha256": {"const": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"},
    "already_closed_group_id": {"const": 0},
    "closed_manifest_sha256": {"const": CLOSED_MANIFEST_SHA},
    "closed_second_referee_manifest_sha256": {"const": CLOSED_SECOND_REFEREE_SHA},
    "selected_group_ids": {"const": SELECTED},
    "native_wall_seconds_each": {"const": 240},
    "wrapper_wall_seconds_each": {"const": 250},
    "rss_cap_bytes_each": {"const": 8589934592},
    "no_overlap_confirmed": {"const": True},
    "maximum_lane_count": {"const": 25},
    "parallel_authorized": {"const": False},
    "skip_reorder_relaunch_authorized": {"const": False},
}
for name, properties in (("independent_referee_acceptance.schema.json", acceptance_properties), ("launch_clearance.schema.json", clearance_properties)):
    atomic(HERE / name, {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": list(properties), "properties": properties})
print(json.dumps({"status": plan["status"], "closed_group": 0, "selected": SELECTED, "runner_sha256": RUNNER_SHA}, sort_keys=True))
