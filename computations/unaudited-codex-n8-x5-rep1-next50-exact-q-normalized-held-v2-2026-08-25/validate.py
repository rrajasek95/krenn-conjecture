#!/usr/bin/env python3
"""Static validation for the normalized next50 superseding zero-run package."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25"
SELECTED = list(range(38, 88))
LEDGER_SHA = "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172"
RUNNER_SHA = "b9fc730669e6e5fc4799e9efbf4e6f12b1f443acc004af9bc536be851c4d8388"
ADAPTER_SHA = "c9c3d365f0f2fb3c9a03656822b4112b245455745dd4f707367fff6c6c2e6d11"
NORMALIZED_SHA = "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76"


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
            assert isinstance(value[key], str) and len(value[key]) == 64 and all(c in "0123456789abcdef" for c in value[key])


assert sha256(HERE / "source_ledger.json") == sha256(PRIOR / "source_ledger.json") == LEDGER_SHA
for gid in SELECTED:
    current = HERE / "sources" / f"rep1_group{gid:03d}_Q.sing"
    prior = PRIOR / "sources" / current.name
    assert sha256(current) == sha256(prior) and current.stat().st_size == prior.stat().st_size
assert sha256(HERE / "run_next50_v2.py") == RUNNER_SHA
assert sha256(HERE / "normalize_next25_dependency.py") == ADAPTER_SHA
assert sha256(HERE / "normalized_next25_dependency.json") == NORMALIZED_SHA
normalized = json.loads((HERE / "normalized_next25_dependency.json").read_text())
assert normalized["status"] == "PASS_NORMALIZED_BASELINE_PLUS_NEXT25_TO_CLOSED_UNION_0_37"
assert normalized["baseline_group_ids"] == list(range(11)) + [13, 15]
assert normalized["next25_groups_closed"] == [11, 12, 14] + list(range(16, 38))
assert normalized["closed_union"] == list(range(38))
assert normalized["set_proof"] == {"baseline_count": 13, "next25_count": 25, "intersection": [], "union_count": 38, "missing_from_0_37": [], "extra_outside_0_37": [], "duplicates": []}
tests = json.loads((HERE / "results_adapter_tests.json").read_text())
assert tests["status"] == "PASS_SCHEMA_EQUIVALENCE_AND_HOSTILES" and tests["hostile_count"] == 12 and all(tests["hostile_tests"].values())
assert tests["prior_dependency_projection"]["closed_union"] == list(range(38))
plan = json.loads((HERE / "held_schedule_v2.json").read_text())
assert plan["status"] == "HELD_ZERO_RUNS_NORMALIZED_DEPENDENCY_PENDING_NEW_ACCEPTANCE_AND_CLEARANCE"
assert plan["supersedes_manifest_sha256"] == "db8aa8acd4977934273c28249ffba8930c102cec2fc10bad9d86edb7fa51423d"
assert plan["execution"]["order"] == SELECTED and plan["execution"]["maximum_lane_count"] == 50
assert plan["execution"]["native_wall_seconds_each"] == 240 and plan["execution"]["wrapper_wall_seconds_each"] == 250 and plan["execution"]["rss_cap_bytes_each"] == 8589934592
assert all(plan["execution"][key] is False for key in ("parallel", "skip", "reorder", "relaunch"))
assert plan["scope"] == {"source_files_preserved": 50, "solver_launches": 0, "result_files": 0, "attempt_markers": 0, "acceptances": 0, "clearances": 0, "groups_newly_closed": 0, "mathematical_coverage": False}
runner = (HERE / "run_next50_v2.py").read_text()
compile(runner, str(HERE / "run_next50_v2.py"), "exec")
for token in (
    "load_and_normalize()", "normalized['closed_union']==list(range(38))",
    "binding_audit_manifest_sha", "baseline_manifest_sha", "next25_terminal_manifest_sha",
    "SELECTED=tuple(range(38,88))", "NATIVE_WALL=240", "WRAPPER_WALL=250",
    "proc_listpgrppids", "rusage failure for live member", "if not unit:stop=",
    "atomic(HERE/'results'/", "BATCH_ATTEMPT.json", "'parallel':False", "'relaunch':False",
):
    assert token in runner, token
assert "future['closed_union']" not in runner and "UNSATISFIED_PLACEHOLDER" not in runner

for name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((HERE / name).read_text())
    good = {key: rule.get("const", "0" * 64) for key, rule in schema["properties"].items()}
    schema_validate(schema, good)
    for key, bad in (
        ("baseline_result_sha256", "1" * 64), ("next25_terminal_result_sha256", "2" * 64),
        ("binding_audit_manifest_sha256", "3" * 64), ("normalized_dependency_sha256", "4" * 64),
        ("selected_group_ids", SELECTED[:-1]), ("parallel_authorized", True),
        ("skip_reorder_relaunch_authorized", True),
    ):
        candidate = copy.deepcopy(good)
        candidate[key] = bad
        try:
            schema_validate(schema, candidate)
        except AssertionError:
            pass
        else:
            raise AssertionError((name, key))
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HERE / absent).exists(), absent
assert not any(HERE.glob("*.tmp"))
print(json.dumps({"status": "PASS_SUPERSEDING_NORMALIZED_HELD_ZERO_RUN", "sources": 50, "runner_sha256": RUNNER_SHA, "adapter_hostiles": 12, "solver_runs": 0}, sort_keys=True))
