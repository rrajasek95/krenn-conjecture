#!/usr/bin/env python3
"""Exact mock/hostile tests for the final conditional dependency."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

from normalize_future_dependency import normalize_record

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "future_groups88_137_dependency.json").read_text())
GOOD = {
    "schema": SPEC["required_future_result_schema"], "status": SPEC["required_future_result_status"],
    "new_groups_closed": 50, "strict_order": True, "parallel": False, "skipped": False, "relaunch": False,
    "baseline_closed_union": list(range(88)), "groups_closed": list(range(88, 138)), "closed_union": list(range(138)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


normalized = normalize_record(GOOD, SPEC)
assert normalized["closed_union"] == list(range(138))
hostiles = {}


def rejected(name: str, mutation) -> None:
    terminal, spec = copy.deepcopy(GOOD), copy.deepcopy(SPEC)
    mutation(terminal, spec)
    try:
        normalize_record(terminal, spec)
    except (AssertionError, KeyError, TypeError):
        hostiles[name] = True
    else:
        hostiles[name] = False


rejected("baseline_missing", lambda t, s: t["baseline_closed_union"].pop())
rejected("baseline_duplicate", lambda t, s: t["baseline_closed_union"].append(87))
rejected("future_missing", lambda t, s: t["groups_closed"].pop())
rejected("future_duplicate", lambda t, s: t["groups_closed"].append(137))
rejected("future_extra", lambda t, s: t["groups_closed"].append(162))
rejected("future_overlap", lambda t, s: t["groups_closed"].__setitem__(0, 87))
rejected("future_reorder", lambda t, s: t["groups_closed"].reverse())
rejected("wrong_closed_union", lambda t, s: t["closed_union"].pop())
rejected("wrong_status", lambda t, s: t.__setitem__("status", "PASS_WRONG"))
rejected("skipped", lambda t, s: t.__setitem__("skipped", True))
rejected("parallel", lambda t, s: t.__setitem__("parallel", True))
rejected("relaunch", lambda t, s: t.__setitem__("relaunch", True))
assert all(hostiles.values()) and len(hostiles) == 12
result = {"schema": "KRENN_X5_REP1_GROUPS138_161_FUTURE_ADAPTER_TESTS_V1", "status": "PASS_VALID_MOCK_AND_12_HOSTILES", "valid_mock_normalized": normalized, "dependency_spec_sha256": sha256(HERE / "future_groups88_137_dependency.json"), "adapter_sha256": sha256(HERE / "normalize_future_dependency.py"), "hostile_tests": hostiles, "hostile_count": 12, "future_files_present": False, "solver_runs": 0}
temporary = HERE / "results_adapter_tests.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_adapter_tests.json")
print(json.dumps({"status": result["status"], "hostiles": 12}, sort_keys=True))
