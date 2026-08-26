#!/usr/bin/env python3
"""Hostile tests for selection, sealed dependency, execution geometry, and scope."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(plan: dict, ledger: dict, census: dict) -> None:
    assert plan["status"] == "HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT_AND_CLEARANCE"
    assert census["counts"] == {"raw": 972, "canonical_groups": 162, "members_each": 6, "y_groups": 81, "z_groups": 81}
    assert census["closed_group_identification"]["group_id"] == 0
    assert census["closed_group_identification"]["source_sha256"] == "5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf"
    assert ledger["selection"] == {"excluded_proven_group_ids": [0], "rule": "25 lowest canonical group IDs after excluding exactly the sealed all-equal-y group", "selected_group_ids": list(range(1, 26))}
    assert [lane["group_id"] for lane in ledger["lanes"]] == list(range(1, 26))
    assert plan["execution"] == {"native_wall_seconds_each": 240, "wrapper_wall_seconds_each": 250, "rss_cap_bytes_each": 8589934592, "maximum_lane_count": 25, "order": list(range(1, 26)), "parallel": False, "skip": False, "reorder": False, "relaunch": False, "stop_whole_batch_on": ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]}
    assert plan["scope"]["representative"] == "rep2 only"
    assert plan["scope"]["solver_launches"] == plan["scope"]["result_files"] == plan["scope"]["groups_newly_closed"] == 0
    assert plan["scope"]["cross_representative_transport"] is False


plan = json.loads((HERE / "held_schedule.json").read_text())
ledger = json.loads((HERE / "source_ledger.json").read_text())
census = json.loads((HERE / "canonical_census.json").read_text())
validate(plan, ledger, census)
tests = {}
for name, mutate in {
    "wrong_closed_group": lambda p, l, c: c["closed_group_identification"].__setitem__("group_id", 1),
    "wrong_closed_source": lambda p, l, c: c["closed_group_identification"].__setitem__("source_sha256", "0" * 64),
    "exclude_extra_group": lambda p, l, c: l["selection"]["excluded_proven_group_ids"].append(1),
    "missing_selected_group": lambda p, l, c: l["lanes"].pop(),
    "reordered_groups": lambda p, l, c: l["lanes"].reverse(),
    "parallel_true": lambda p, l, c: p["execution"].__setitem__("parallel", True),
    "wall_widened": lambda p, l, c: p["execution"].__setitem__("native_wall_seconds_each", 241),
    "rss_widened": lambda p, l, c: p["execution"].__setitem__("rss_cap_bytes_each", 8589934593),
    "cross_rep_overclaim": lambda p, l, c: p["scope"].__setitem__("cross_representative_transport", True),
    "run_injected": lambda p, l, c: p["scope"].__setitem__("solver_launches", 1),
}.items():
    candidate_plan, candidate_ledger, candidate_census = copy.deepcopy(plan), copy.deepcopy(ledger), copy.deepcopy(census)
    mutate(candidate_plan, candidate_ledger, candidate_census)
    try:
        validate(candidate_plan, candidate_ledger, candidate_census)
    except (AssertionError, KeyError, TypeError):
        tests[name] = True
    else:
        tests[name] = False
assert len(tests) == 10 and all(tests.values())
result = {"schema": "KRENN_X5_REP2_FIRST25_HELD_HOSTILE_TESTS_V1", "status": "PASS_10_HOSTILES_ZERO_RUN", "tests": tests, "plan_sha256": sha256(HERE / "held_schedule.json"), "ledger_sha256": sha256(HERE / "source_ledger.json"), "census_sha256": sha256(HERE / "canonical_census.json"), "solver_runs": 0}
temporary = HERE / "results_hostile_tests.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_hostile_tests.json")
print(json.dumps({"status": result["status"], "tests": 10}, sort_keys=True))
