#!/usr/bin/env python3
"""Replay the fail-closed rep4 groups76..125 prelaunch refusal."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26"
BIND = ROOT / "computations/unaudited-codex-n8-x5-rep4-groups76-125-satisfied-dependency-binding-v2-2026-08-26"
FIRST = ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(RUN / "MANIFEST.sha256") == "0d2d7cfce0ed9e862b573e4fdc5791b3384c7bd21fbd6e9ff9e663c79f387115"
assert sha(RUN / "run_groups76_125.py") == "3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd"
assert sha(RUN / "source_ledger.json") == "b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb"
assert sha(BIND / "results_binding.json") == "b7d70144cf0f99b9201e52f0cea5c0252f7c44613d8667458c4ca40fe3fbe648"
assert sha(BIND / "results_referee.json") == "02fc2f2add733fa0212b22905f5eb276f4cde1d608c0ba8bf8f35ad0d99cc773"
assert sha(BIND / "FINAL_MANIFEST.sha256") == "4fbc4430abf903b329519ca4499183c9571c574073b0be69eb36b0efd8f5ab73"
assert sha(BIND / "normalized_dependencies.json") == "a9134eef5e3b2f98782197809695b8f672841eb92957e085b1c0f264840c289b"
assert sha(BIND / "independent_referee_acceptance.json") == "1c31af2f1b633f05102455d0b55a7d5fc74bf9b6038aafa68095710f10c8f1f6"

runner = (RUN / "run_groups76_125.py").read_text()
normalized = json.loads((BIND / "normalized_dependencies.json").read_text())
acceptance = json.loads((BIND / "independent_referee_acceptance.json").read_text())
first = json.loads((FIRST / "results_referee.json").read_text())

assert "KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1" in runner
assert normalized["schema"] == "KRENN_X5_REP4_GROUPS1_75_NORMALIZED_DEPENDENCIES_V2"
assert acceptance["normalized_dependencies_sha256"] == sha(BIND / "normalized_dependencies.json")
for required in (
    "dependency_manifest_paths",
    "dependency_result_paths",
    "dependency_manifest_sha256",
    "dependency_result_sha256",
):
    assert required not in normalized

old_contract = json.loads((RUN / "future_dependencies.json").read_text())
assert old_contract["dependencies"][0]["result_status"] == "PASS_ALL_25_EXACT_Q_UNIT_IDEALS"
assert first["status"] == "PASS_EXACT_GROUPS_1_25_UNIT"
assert "groups_closed" not in first

for name in (
    "normalized_dependencies.json",
    "independent_referee_acceptance.json",
    "launch_clearance.json",
    "BATCH_ATTEMPT.json",
    "batch_result.json",
    "results",
):
    assert not (RUN / name).exists(), name
assert not any(RUN.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_FAIL_CLOSED_PRELAUNCH_INTERFACE_MISMATCH_ZERO_RUNS",
    "frozen_runner_schema": "KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1",
    "sealed_binding_schema": normalized["schema"],
    "batch_attempt_absent": True,
    "results_absent": True,
}, sort_keys=True))
