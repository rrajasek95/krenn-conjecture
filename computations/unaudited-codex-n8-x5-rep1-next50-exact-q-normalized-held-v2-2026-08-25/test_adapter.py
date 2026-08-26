#!/usr/bin/env python3
"""Exact schema-equivalence and hostile tests for the normalization adapter."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

from normalize_next25_dependency import BASELINE, BINDING, NEXT25, normalize, load_and_normalize

HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline = json.loads((BASELINE / "results_referee.json").read_text())
terminal = json.loads((NEXT25 / "results_referee.json").read_text())
binding = json.loads((BINDING / "results_binding.json").read_text())
normalized = load_and_normalize()
assert normalized == json.loads((HERE / "normalized_next25_dependency.json").read_text())
assert "closed_union" not in terminal
projection = {
    "schema": terminal["schema"],
    "status": terminal["status"],
    "groups_closed": terminal["groups_closed"],
    "closed_union": normalized["closed_union"],
}
assert projection == {
    "schema": "KRENN_X5_REP1_NEXT25_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_ALL_25_EXACT_Q_UNIT_IDEALS",
    "groups_closed": [11, 12, 14] + list(range(16, 38)),
    "closed_union": list(range(38)),
}

hostiles = {}


def rejected(name: str, mutate) -> None:
    b, t, a = copy.deepcopy(baseline), copy.deepcopy(terminal), copy.deepcopy(binding)
    mutate(b, t, a)
    try:
        normalize(b, t, a)
    except (AssertionError, KeyError, TypeError):
        hostiles[name] = True
    else:
        hostiles[name] = False


rejected("baseline_missing", lambda b, t, a: b["closed_baseline_group_ids"].pop())
rejected("baseline_duplicate", lambda b, t, a: b["closed_baseline_group_ids"].append(15))
rejected("baseline_extra", lambda b, t, a: b["closed_baseline_group_ids"].append(99))
rejected("next25_missing", lambda b, t, a: t["groups_closed"].pop())
rejected("next25_duplicate", lambda b, t, a: t["groups_closed"].append(37))
rejected("next25_extra", lambda b, t, a: t["groups_closed"].append(99))
rejected("next25_overlap", lambda b, t, a: t["groups_closed"].__setitem__(0, 0))
rejected("next25_reorder", lambda b, t, a: t["groups_closed"].reverse())
rejected("terminal_status", lambda b, t, a: t.__setitem__("status", "PASS_BUT_WRONG"))
rejected("terminal_skipped", lambda b, t, a: t.__setitem__("skipped", True))
rejected("binding_union", lambda b, t, a: a["closed_union"].pop())
rejected("binding_manifest", lambda b, t, a: a.__setitem__("next25_terminal_referee_manifest_sha256", "0" * 64))
assert all(hostiles.values()) and len(hostiles) == 12
result = {
    "schema": "KRENN_X5_REP1_NEXT50_NORMALIZED_DEPENDENCY_TESTS_V2",
    "status": "PASS_SCHEMA_EQUIVALENCE_AND_HOSTILES",
    "terminal_lacks_closed_union": True,
    "adapter_supplies_closed_union": True,
    "prior_dependency_projection": projection,
    "normalized_dependency_sha256": sha256(HERE / "normalized_next25_dependency.json"),
    "binding_audit_manifest_sha256": normalized["pins"]["binding_audit_manifest_sha256"],
    "hostile_tests": hostiles,
    "hostile_count": len(hostiles),
    "solver_runs": 0,
}
temporary = HERE / "results_adapter_tests.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_adapter_tests.json")
print(json.dumps({"status": result["status"], "hostiles": len(hostiles)}, sort_keys=True))
