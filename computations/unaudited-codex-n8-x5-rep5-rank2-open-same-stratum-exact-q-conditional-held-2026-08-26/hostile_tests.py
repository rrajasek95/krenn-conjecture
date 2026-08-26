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
    "schema": "KRENN_X5_REP5_OPEN84_FUTURE_MODULAR_UNIT_DEPENDENCY_V1",
    "status": "INDEPENDENTLY_SEALED_SAME_STRATUM_MODULAR_UNIT",
    "held_manifest_sha256": "687dd47c10265ad82421cd06e015db4a88982710dbdba370ac0fee82f5f5596b",
    "held_referee_v1_manifest_sha256": "1c33eea1ba807ef5502a1f3047844faaec05afe355858a3b041a0dd1584479f7",
    "held_referee_v2_manifest_sha256": "78ec2054761b8e6a6eeb3dc338f82338d02b48d25436a46b5cbcc37755d18a49",
    "producer_manifest_path": "future/producer/MANIFEST.sha256", "producer_manifest_sha256": HEX,
    "producer_result_path": "future/producer/result.json", "producer_result_sha256": HEX,
    "referee_manifest_path": "future/referee/FINAL_MANIFEST.sha256", "referee_manifest_sha256": HEX,
    "referee_result_path": "future/referee/results_referee.json", "referee_result_sha256": HEX,
    "modular_source_sha256": "fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a",
    "field": "F_32003", "pivot_k": 2, "t_open": 1, "variables": 84, "generators": 6562,
}
validate_shape(base)
mutations = []
for key, wrong in (
    ("status", "PASS"), ("held_manifest_sha256", HEX), ("held_referee_v1_manifest_sha256", HEX),
    ("held_referee_v2_manifest_sha256", HEX), ("modular_source_sha256", HEX), ("field", "Q"),
    ("pivot_k", 1), ("t_open", 2), ("variables", 85), ("generators", 6561),
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
result = {"schema": "KRENN_X5_REP5_OPEN84_SAME_STRATUM_EXACT_Q_HOSTILES_V1", "status": "PASS", "hostile_count": len(mutations) + 4, "solver_runs": 0, "runner_refused_before_attempt": True}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
