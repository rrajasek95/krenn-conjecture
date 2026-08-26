#!/usr/bin/env python3
"""Bounded exact contract tests for the future 38..87 dependency adapter."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

from normalize_future_dependency import BASELINE, normalize_records

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "future_groups38_87_dependency.json").read_text())
BASE = json.loads((BASELINE / "normalized_next25_dependency.json").read_text())
GOOD = {
    "schema": SPEC["required_future_result_schema"],
    "status": SPEC["required_future_result_status"],
    "new_groups_closed": 50,
    "strict_order": True,
    "parallel": False,
    "skipped": False,
    "relaunch": False,
    "groups_closed": list(range(38, 88)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


normalized = normalize_records(BASE, GOOD, SPEC)
assert normalized["closed_union"] == list(range(88))
hostiles = {}


def rejected(name: str, target: str, mutation) -> None:
    baseline, terminal, spec = copy.deepcopy(BASE), copy.deepcopy(GOOD), copy.deepcopy(SPEC)
    mutation({"baseline": baseline, "terminal": terminal, "spec": spec}[target])
    try:
        normalize_records(baseline, terminal, spec)
    except (AssertionError, KeyError, TypeError):
        hostiles[name] = True
    else:
        hostiles[name] = False


rejected("baseline_missing", "baseline", lambda value: value["closed_union"].pop())
rejected("baseline_duplicate", "baseline", lambda value: value["closed_union"].append(37))
rejected("future_missing", "terminal", lambda value: value["groups_closed"].pop())
rejected("future_duplicate", "terminal", lambda value: value["groups_closed"].append(87))
rejected("future_extra", "terminal", lambda value: value["groups_closed"].append(138))
rejected("future_overlap", "terminal", lambda value: value["groups_closed"].__setitem__(0, 37))
rejected("future_reordered", "terminal", lambda value: value["groups_closed"].reverse())
rejected("future_wrong_status", "terminal", lambda value: value.__setitem__("status", "PASS_WRONG"))
rejected("future_skipped", "terminal", lambda value: value.__setitem__("skipped", True))
rejected("future_parallel", "terminal", lambda value: value.__setitem__("parallel", True))
rejected("future_relaunch", "terminal", lambda value: value.__setitem__("relaunch", True))
rejected("spec_union_extra", "spec", lambda value: value["required_closed_union"].append(88))
assert all(hostiles.values()) and len(hostiles) == 12
result = {
    "schema": "KRENN_X5_REP1_GROUPS88_137_FUTURE_ADAPTER_TESTS_V1",
    "status": "PASS_MOCK_VALID_SCHEMA_AND_12_HOSTILES",
    "valid_mock_normalized": normalized,
    "baseline_dependency_sha256": sha256(BASELINE / "normalized_next25_dependency.json"),
    "dependency_spec_sha256": sha256(HERE / "future_groups38_87_dependency.json"),
    "adapter_sha256": sha256(HERE / "normalize_future_dependency.py"),
    "hostile_tests": hostiles,
    "hostile_count": len(hostiles),
    "future_files_present": False,
    "solver_runs": 0,
}
temporary = HERE / "results_adapter_tests.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_adapter_tests.json")
print(json.dumps({"status": result["status"], "hostiles": 12}, sort_keys=True))
