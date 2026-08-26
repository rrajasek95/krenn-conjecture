#!/usr/bin/env python3
"""Small fail-closed interface tests; never invokes Singular."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from verify_future_dependency import validate_shape

HERE = Path(__file__).resolve().parent
HEX = "0" * 64


def rejected(value: dict) -> bool:
    try:
        validate_shape(value)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


base = {
    "schema": "KRENN_X5_REP5_TORUS_SMALLEST_FUTURE_MODULAR_UNIT_DEPENDENCY_V1",
    "status": "INDEPENDENTLY_SEALED_SAME_CHART_MODULAR_UNIT",
    "held_manifest_sha256": "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72",
    "held_referee_manifest_sha256": "16a32d07221def48a9e8388ca1e8b716cd71dfb44c2dc0cbea0bb22ab91203ab",
    "producer_manifest_path": "future/producer/MANIFEST.sha256", "producer_manifest_sha256": HEX,
    "producer_result_path": "future/producer/result.json", "producer_result_sha256": HEX,
    "referee_manifest_path": "future/referee/FINAL_MANIFEST.sha256", "referee_manifest_sha256": HEX,
    "referee_result_path": "future/referee/results_referee.json", "referee_result_sha256": HEX,
    "modular_source_sha256": "c36bd3b77052487b43751b03f48849c76091ec121a04abc3305cb56ec6494a8b",
    "field": "F_32003", "assignment": {"yn1":1,"yn2":1,"t0":1,"t2":0}, "variables": 73, "generators": 6561,
}
validate_shape(base)
mutations = []
for key, wrong in (
    ("status", "PASS"), ("held_manifest_sha256", HEX), ("held_referee_manifest_sha256", HEX),
    ("modular_source_sha256", HEX), ("field", "Q"), ("assignment", {"yn1":0,"yn2":1,"t0":1,"t2":0}),
    ("variables", 74), ("generators", 6562),
    ("producer_manifest_sha256", None), ("referee_result_sha256", "bad"),
):
    hostile = copy.deepcopy(base); hostile[key] = wrong; mutations.append((key, hostile))
missing = copy.deepcopy(base); del missing["producer_result_path"]; mutations.append(("missing", missing))
extra = copy.deepcopy(base); extra["extra"] = True; mutations.append(("extra", extra))
assert all(rejected(value) for _, value in mutations)
assert not (HERE / "future_modular_unit_dependency.json").exists()
assert not (HERE / "independent_referee_acceptance.json").exists()
assert not (HERE / "launch_clearance.json").exists()
attempt = subprocess.run([sys.executable, str(HERE / "run_one_lane.py")], cwd=HERE, capture_output=True, text=True, timeout=10)
assert attempt.returncode != 0
assert "future modular UNIT seal" in attempt.stderr
for forbidden in ("ATTEMPT.json", "result.json", "RUN_EXCLUSIVE.lock"):
    assert not (HERE / forbidden).exists()
result = {"schema": "KRENN_X5_REP5_TORUS_SMALLEST_SAME_CHART_EXACT_Q_HOSTILES_V1", "status": "PASS", "hostile_count": len(mutations) + 4, "solver_runs": 0, "runner_refused_before_attempt": True}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
