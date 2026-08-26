#!/usr/bin/env python3
"""Repair only the first-batch provenance interface for the final rep4 executor."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALIAS = ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-terminal-compatibility-alias-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, value: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(value)
    os.replace(tmp, path)


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


assert sha(ALIAS / "FINAL_MANIFEST.sha256") == "683ca06acdf6ec9879883a68d9006fafbe719bfbeb98faf46a067fc3ed9d44b2"
assert sha(ALIAS / "compatibility_result.json") == "1f3cba3049bf3d90d88d873c19c4df4e75134cf04bd8d3762b47efc603ce36e5"

future_path = HERE / "future_dependencies.json"
future = json.loads(future_path.read_text())
assert future["schema"] == "KRENN_X5_REP4_GROUPS126_161_FUTURE_DEPENDENCIES_V1"
first = future["dependencies"][0]
first.update(
    {
        "manifest_path": str((ALIAS / "FINAL_MANIFEST.sha256").relative_to(ROOT)),
        "result_path": str((ALIAS / "compatibility_result.json").relative_to(ROOT)),
        "result_schema": "KRENN_X5_REP4_FIRST25_TERMINAL_COMPATIBILITY_ALIAS_V1",
        "result_status": "PASS_ALIAS_EXACT_GROUPS_1_25_UNIT",
    }
)
write_json(future_path, future)
future_sha = sha(future_path)

verifier_path = HERE / "dependency_verifier.py"
verifier = verifier_path.read_text()
old_contract = "CONTRACT_SHA='18b7cae58e965187bcbb97ef7a319aacd92fccb6be4010d9630caad83ef77e75'"
assert verifier.count(old_contract) == 1
verifier = verifier.replace(old_contract, f"CONTRACT_SHA='{future_sha}'")
write_text(verifier_path, verifier)
verifier_sha = sha(verifier_path)

runner_path = HERE / "run_groups126_161.py"
runner = runner_path.read_text()
old_future = "FUTURE_SHA='18b7cae58e965187bcbb97ef7a319aacd92fccb6be4010d9630caad83ef77e75'"
old_verifier = "VERIFIER_SHA='fc44d47caef2915dc8cf7dc384d544e8c858e4be8de372b08d01a30abb3b90eb'"
assert runner.count(old_future) == runner.count(old_verifier) == 1
runner = runner.replace(old_future, f"FUTURE_SHA='{future_sha}'")
runner = runner.replace(old_verifier, f"VERIFIER_SHA='{verifier_sha}'")
write_text(runner_path, runner)
runner_sha = sha(runner_path)

for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema_path = HERE / schema_name
    schema = json.loads(schema_path.read_text())
    schema["properties"]["dependency_verifier_sha256"]["const"] = verifier_sha
    schema["properties"]["runner_sha256"]["const"] = runner_sha
    write_json(schema_path, schema)

pins = {
    "future_dependencies_sha256": future_sha,
    "dependency_verifier_sha256": verifier_sha,
    "runner_sha256": runner_sha,
    "source_ledger_sha256": sha(HERE / "source_ledger.json"),
    "normalizer_sha256": sha(HERE / "normalize_dependencies.py"),
    "alias_manifest_sha256": sha(ALIAS / "FINAL_MANIFEST.sha256"),
    "alias_result_sha256": sha(ALIAS / "compatibility_result.json"),
}
write_json(HERE / "v2_pins.json", pins)
print(json.dumps({"status": "PASS_REP4_FINAL36_V2_PREPARED", **pins}, sort_keys=True))
