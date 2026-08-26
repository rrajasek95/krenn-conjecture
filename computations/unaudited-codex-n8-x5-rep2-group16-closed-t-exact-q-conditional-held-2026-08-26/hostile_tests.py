#!/usr/bin/env python3
"""Fail-closed interface tests; never invokes Singular."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

from verify_modular_unit_dependency import validate_shape

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / "modular_unit_dependency.json").read_text())
validate_shape(base)
zero = "0" * 64
tests: dict[str, bool] = {}
for key, wrong in (
    ("status", "PASS"), ("held_manifest_sha256", zero), ("held_referee_manifest_sha256", zero),
    ("producer_terminal_manifest_sha256", zero), ("producer_result_sha256", zero),
    ("referee_terminal_manifest_sha256", zero), ("referee_result_sha256", zero),
    ("modular_source_sha256", zero), ("field", "Q"), ("chart", "wrong"),
    ("variables", 63), ("generators", 6567),
):
    hostile = copy.deepcopy(base)
    hostile[key] = wrong
    try:
        validate_shape(hostile)
    except (AssertionError, KeyError, TypeError):
        tests[key] = True
    else:
        tests[key] = False
for absent in ("independent_referee_acceptance.json", "launch_clearance.json"):
    tests[absent] = not (HERE / absent).exists()
attempt = subprocess.run(
    [sys.executable, str(HERE / "run_one_lane.py")], cwd=HERE, capture_output=True, text=True,
    timeout=15, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
)
tests["runner_refuses_before_attempt"] = attempt.returncode != 0 and "independent exact-Q acceptance" in attempt.stderr
tests["no_attempt_artifacts"] = all(not (HERE / name).exists() for name in ("ATTEMPT.json", "RUN_EXCLUSIVE.lock", "result.json"))
assert len(tests) == 16 and all(tests.values()), tests
result = {
    "schema": "KRENN_X5_REP2_GROUP16_CLOSED_T_EXACT_Q_CONDITIONAL_HOSTILES_V1",
    "status": "PASS", "hostile_count": 16, "runner_refused_before_attempt": True,
    "solver_runs": 0, "tests": tests,
}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS", "hostiles": 16, "solver_runs": 0}, sort_keys=True))
