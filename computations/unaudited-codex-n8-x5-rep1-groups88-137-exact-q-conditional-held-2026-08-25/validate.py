#!/usr/bin/env python3
"""Static fail-closed validation for the conditional groups88..137 package."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SELECTED = list(range(88, 138))
LEDGER_SHA = "2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b"
RUNNER_SHA = "604b0b938389e44506d627eba8652d74cfe3d3ba10a932efcb6c4dbfeee987e5"
SPEC_SHA = "1374fb5ed562ac0fd6b28ace616e09fbf011509555b02cb98996281d7188b380"
ADAPTER_SHA = "87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_validate(schema: dict, value: dict) -> None:
    properties = schema["properties"]
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(properties) == set(value)
    for key, rule in properties.items():
        if "const" in rule:
            assert value[key] == rule["const"]
        elif rule.get("pattern") == "^[0-9a-f]{64}$":
            assert isinstance(value[key], str) and len(value[key]) == 64 and all(char in "0123456789abcdef" for char in value[key])


assert sha256(HERE / "source_ledger.json") == LEDGER_SHA
assert sha256(HERE / "run_groups88_137.py") == RUNNER_SHA
assert sha256(HERE / "future_groups38_87_dependency.json") == SPEC_SHA
assert sha256(HERE / "normalize_future_dependency.py") == ADAPTER_SHA
ledger = json.loads((HERE / "source_ledger.json").read_text())
plan = json.loads((HERE / "held_schedule.json").read_text())
spec = json.loads((HERE / "future_groups38_87_dependency.json").read_text())
assert [lane["group_id"] for lane in ledger["lanes"]] == SELECTED
assert plan["status"] == "HELD_ZERO_RUNS_FUTURE_GROUPS38_87_HASHES_ABSENT"
assert plan["execution"]["order"] == SELECTED and plan["execution"]["maximum_lane_count"] == 50
assert all(plan["execution"][key] is False for key in ("parallel", "skip", "reorder", "relaunch"))
assert plan["dependency"]["future_manifest_sha256"] is None and plan["dependency"]["future_result_sha256"] is None and plan["dependency"]["satisfied"] is False
assert spec["future_manifest_sha256"] is None and spec["future_result_sha256"] is None and spec["satisfied"] is False
assert spec["proven_baseline_closed_union"] == list(range(38)) and spec["expected_future_groups_closed"] == list(range(38, 88)) and spec["required_closed_union"] == list(range(88))
assert not (ROOT / spec["future_manifest_path"]).exists()
assert not (ROOT / spec["future_result_path"]).exists()
tests = json.loads((HERE / "results_adapter_tests.json").read_text())
assert tests["status"] == "PASS_MOCK_VALID_SCHEMA_AND_12_HOSTILES" and tests["future_files_present"] is False and all(tests["hostile_tests"].values())
for lane in ledger["lanes"]:
    path = HERE / lane["source_path"]
    assert sha256(path) == lane["source_sha256"] and path.stat().st_size == lane["source_bytes"]
    source = path.read_text()
    assert source.count("ring r=0,") == source.count("ideal G=slimgb(I);") == source.count("poly remainder=reduce(1,G);") == source.count("quit;") == 1
runner = (HERE / "run_groups88_137.py").read_text()
compile(runner, str(HERE / "run_groups88_137.py"), "exec")
for token in (
    "SELECTED=tuple(range(88,138))", "load_and_normalize(future_manifest_sha,future_result_sha)",
    "normalized['closed_union']==list(range(88))", "future_terminal_manifest_sha256", "future_terminal_result_sha256",
    "proc_listpgrppids", "rusage failure for live member", "NATIVE_WALL=240", "WRAPPER_WALL=250",
    "if not unit:stop=", "atomic(HERE/'results'/", "BATCH_ATTEMPT.json", "'parallel':False", "'relaunch':False",
):
    assert token in runner, token
schemas = [json.loads((HERE / name).read_text()) for name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json")]
for schema in schemas:
    good = {key: rule.get("const", "0" * 64) for key, rule in schema["properties"].items()}
    schema_validate(schema, good)
    for key, bad in (
        ("future_terminal_manifest_sha256", None), ("future_terminal_result_sha256", None),
        ("future_terminal_manifest_sha256", "0" * 63), ("selected_group_ids", SELECTED[:-1]),
        ("parallel_authorized", True), ("skip_reorder_relaunch_authorized", True),
    ):
        candidate = copy.deepcopy(good)
        candidate[key] = bad
        try:
            schema_validate(schema, candidate)
        except AssertionError:
            pass
        else:
            raise AssertionError((key, bad))
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HERE / absent).exists(), absent
assert not any(HERE.glob("*.tmp"))
print(json.dumps({"status": "PASS_HELD_ZERO_RUNS_DEPENDENCY_HASHES_ABSENT", "sources": 50, "runner_sha256": RUNNER_SHA, "adapter_hostiles": 12, "solver_runs": 0}, sort_keys=True))
