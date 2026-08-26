#!/usr/bin/env python3
"""Static fail-closed validator for the conditional next-50 held schedule."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SELECTED = list(range(38, 88))
LEDGER_SHA = "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172"
RUNNER_SHA = "eba736280a2d724cc1c46370d85292d7543f7bfd46a7e51e813c5bfe6ce0b66e"
DEPENDENCY_SHA = "aba4c9792cd2874269722f678864130cfde27c30caa47d505249a77ada82c896"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def simple_schema_validate(schema: dict, value: dict) -> None:
    properties = schema["properties"]
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(properties) == set(value)
    for key, rule in properties.items():
        if "const" in rule:
            assert value[key] == rule["const"]
        elif rule.get("pattern") == "^[0-9a-f]{64}$":
            assert isinstance(value[key], str) and len(value[key]) == 64 and all(c in "0123456789abcdef" for c in value[key])


ledger = json.loads((HERE / "source_ledger.json").read_text())
plan = json.loads((HERE / "held_schedule.json").read_text())
dependency = json.loads((HERE / "future_next25_dependency.json").read_text())
runner_path = HERE / "run_next50.py"
runner = runner_path.read_text()
assert sha256(HERE / "source_ledger.json") == LEDGER_SHA
assert sha256(runner_path) == RUNNER_SHA
assert sha256(HERE / "future_next25_dependency.json") == DEPENDENCY_SHA
assert [lane["group_id"] for lane in ledger["lanes"]] == SELECTED
assert ledger["selection"] == {"assumed_closed_group_ids": list(range(38)), "dependency": "future exact next25 terminal referee PASS", "rule": "50 lowest canonical group IDs remaining after conditional closure of groups 0..37", "selected_group_ids": SELECTED}
assert plan["status"] == "HELD_ZERO_RUNS_CONDITIONAL_ON_FUTURE_NEXT25_PASS"
assert plan["execution"]["order"] == SELECTED and plan["execution"]["maximum_lane_count"] == 50
assert plan["execution"]["parallel"] is plan["execution"]["skip"] is plan["execution"]["reorder"] is plan["execution"]["relaunch"] is False
assert plan["future_dependency"] == {"path": "future_next25_dependency.json", "sha256": DEPENDENCY_SHA, "currently_satisfied": False, "future_manifest_hash_placeholder": None, "future_result_hash_placeholder": None, "runner_requires_later_acceptance_to_bind_both_exact_hashes": True}
assert dependency["status"] == "UNSATISFIED_PLACEHOLDER_BLOCKS_LAUNCH"
assert dependency["satisfied"] is False and dependency["current_future_manifest_sha256"] is None and dependency["current_future_result_sha256"] is None
assert dependency["expected_closed_union_after_pass"] == list(range(38))
assert not (ROOT / dependency["future_manifest_path"]).exists()
assert not (ROOT / dependency["future_result_path"]).exists()
for lane in ledger["lanes"]:
    path = HERE / lane["source_path"]
    assert sha256(path) == lane["source_sha256"] and path.stat().st_size == lane["source_bytes"]
    source = path.read_text()
    assert source.count("ring r=0,") == source.count("ideal G=slimgb(I);") == source.count("poly remainder=reduce(1,G);") == source.count("quit;") == 1
compile(runner, str(runner_path), "exec")
for token in (
    "SELECTED=tuple(range(38,88))", "proc_listpgrppids", "group_rss",
    "rusage failure for live member", "future_manifest.is_file() and future_result.is_file()",
    "UNSATISFIED_PLACEHOLDER_BLOCKS_LAUNCH", "future_manifest_sha=sha(future_manifest)",
    "future_result_sha=sha(future_result)", "future['groups_closed']==dependency['expected_closed_group_ids']",
    "future['closed_union']==dependency['expected_closed_union_after_pass']",
    "next25_terminal_manifest_sha256", "next25_terminal_result_sha256",
    "if not unit:stop=", "atomic(HERE/'results'/", "BATCH_ATTEMPT.json",
    "'parallel':False", "'relaunch':False", "NATIVE_WALL=240", "WRAPPER_WALL=250",
):
    assert token in runner, token

schemas = [json.loads((HERE / name).read_text()) for name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json")]
for schema in schemas:
    properties = schema["properties"]
    good = {key: rule.get("const", "0" * 64) for key, rule in properties.items()}
    simple_schema_validate(schema, good)
    for key, bad in (("next25_terminal_manifest_sha256", "1" * 63), ("next25_terminal_result_sha256", "g" * 64), ("selected_group_ids", SELECTED[:-1]), ("parallel_authorized", True), ("skip_reorder_relaunch_authorized", True)):
        candidate = copy.deepcopy(good)
        candidate[key] = bad
        try:
            simple_schema_validate(schema, candidate)
        except AssertionError:
            pass
        else:
            raise AssertionError((schema["properties"]["schema"], key))
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HERE / absent).exists(), absent
assert not any(HERE.glob("*.tmp"))
print(json.dumps({"status": "PASS_CONDITIONAL_HELD_ZERO_RUNS", "groups": SELECTED, "sources": 50, "runner_sha256": RUNNER_SHA, "future_dependency_satisfied": False}, sort_keys=True))
