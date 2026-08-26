#!/usr/bin/env python3
"""Bind sealed next25 PASS evidence to the conditional next50 package, without launch."""
import ast, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
N50 = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25"
N50REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-referee-2026-08-25"
N25 = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-2026-08-25"
N25REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-referee-2026-08-25"
N25TERM = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-terminal-referee-2026-08-25"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

pins = {
    N50 / "MANIFEST.sha256": "db8aa8acd4977934273c28249ffba8930c102cec2fc10bad9d86edb7fa51423d",
    N50 / "source_ledger.json": "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172",
    N50 / "run_next50.py": "eba736280a2d724cc1c46370d85292d7543f7bfd46a7e51e813c5bfe6ce0b66e",
    N50 / "future_next25_dependency.json": "aba4c9792cd2874269722f678864130cfde27c30caa47d505249a77ada82c896",
    N50REF / "FINAL_MANIFEST.sha256": "e3522c8ced743bbeebc62565a6c9547f14955110ebe805f5d553e544577f0808",
    N50REF / "results_referee.json": "a53182653d8f57804a114bf472ef507c611bdc63d79ae8698f8bfc493228bbeb",
    N25 / "batch_result.json": "b60bbf4f9a3090a4c76f5fa80aa02df6a753ce4d5cf7f39eb96cf56033d0a5fa",
    N25 / "TERMINAL_MANIFEST.sha256": "155ebddcdca47f7ff67b3814bb85a3c2148469f5d38227e07378e0bded87485e",
    N25REF / "FINAL_MANIFEST.sha256": "950e50ea1b1af733b5f20fad076357d29ee76a7b85009c7b93fcad76b1406c75",
    N25REF / "results_referee.json": "a4a959cc1eb2392e64fc0c1d8e540deace8141ae43d50fbd7c30a14d6ef6c189",
    N25TERM / "results_referee.json": "a2599e9cee2739fb372e1d45db9625dc999510eb58407609cb581e73acbce450",
    N25TERM / "FINAL_MANIFEST.sha256": "b5de471b2cbd4f5197492c37f7f885f77059a9eced3e66830998c8edd5d62cde",
}
for path, expected in pins.items(): assert sha(path) == expected, (path, sha(path), expected)

def replay(path, base):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        expected, raw = line.split(None, 1); target = Path(raw.strip())
        if not target.is_absolute(): target = ROOT / target if raw.strip().startswith("computations/") else (base / target).resolve()
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count

manifest_counts = {
    "next50_producer": replay(N50 / "MANIFEST.sha256", N50),
    "next50_prior_referee": replay(N50REF / "FINAL_MANIFEST.sha256", N50REF),
    "next25_producer_terminal": replay(N25 / "TERMINAL_MANIFEST.sha256", N25),
    "next25_held_referee": replay(N25REF / "FINAL_MANIFEST.sha256", N25REF),
    "next25_terminal_referee": replay(N25TERM / "FINAL_MANIFEST.sha256", N25TERM),
}

def manifest_has(path, digest, member):
    return f"{digest}  {member}" in path.read_text().splitlines()

assert manifest_has(N25 / "TERMINAL_MANIFEST.sha256", pins[N25 / "batch_result.json"], "batch_result.json")
assert manifest_has(N25TERM / "FINAL_MANIFEST.sha256", pins[N25TERM / "results_referee.json"], "results_referee.json")
batch = json.loads((N25 / "batch_result.json").read_text())
terminal = json.loads((N25TERM / "results_referee.json").read_text())
held_ref = json.loads((N25REF / "results_referee.json").read_text())
dependency = json.loads((N50 / "future_next25_dependency.json").read_text())
new_groups = [11, 12, 14] + list(range(16, 38))
baseline = list(range(0, 11)) + [13, 15]
closed_union = sorted(baseline + new_groups)
assert len(baseline) == 13 and len(new_groups) == 25 and not set(baseline) & set(new_groups)
assert closed_union == list(range(38))
assert held_ref["closed_baseline_group_ids"] == baseline and held_ref["selected_group_ids"] == new_groups
assert batch["status"] == "PASS_ALL_25_UNIT" and batch["stop"] is None and batch["skipped_after_stop"] == []
assert [item["group_id"] for item in batch["completed"]] == new_groups and batch["strict_order"] == new_groups
assert batch["parallel"] is batch["relaunch"] is False
assert terminal["schema"] == dependency["required_future_result_schema"]
assert terminal["status"] == dependency["required_future_result_status"]
assert terminal["groups_closed"] == dependency["expected_closed_group_ids"] == new_groups
assert dependency["expected_closed_union_after_pass"] == closed_union
assert terminal["batch_result_sha256"] == pins[N25 / "batch_result.json"]
assert terminal["terminal_manifest_sha256"] == pins[N25 / "TERMINAL_MANIFEST.sha256"]
assert terminal["new_groups_closed"] == 25 and terminal["groups_beyond_37_launched"] is False

# The proof dependency is now satisfied, but the frozen runner expects a field
# that the sealed terminal result does not contain.  This is deliberately kept
# fail closed and prevents this held acceptance from being launch-ready.
assert "closed_union" not in terminal
runner = (N50 / "run_next50.py").read_text(); ast.parse(runner)
assert "future['closed_union']==dependency['expected_closed_union_after_pass']" in runner
assert dependency["current_future_manifest_sha256"] is None and dependency["current_future_result_sha256"] is None
assert dependency["satisfied"] is False

acceptance = json.loads((HERE / "independent_referee_acceptance.json").read_text())
expected_acceptance = {
    "schema": "KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_STRICT_CONDITIONAL_NEXT50_BATCH_ONLY",
    "held_manifest_sha256": pins[N50 / "MANIFEST.sha256"],
    "source_ledger_sha256": pins[N50 / "source_ledger.json"],
    "runner_sha256": pins[N50 / "run_next50.py"],
    "selected_group_ids": list(range(38, 88)), "maximum_lane_count": 50,
    "future_dependency_spec_sha256": pins[N50 / "future_next25_dependency.json"],
    "next25_terminal_manifest_sha256": pins[N25TERM / "FINAL_MANIFEST.sha256"],
    "next25_terminal_result_sha256": pins[N25TERM / "results_referee.json"],
    "next25_terminal_closed_union": closed_union,
    "exact_Q_authorized": True, "parallel_authorized": False, "skip_reorder_relaunch_authorized": False,
}
assert acceptance == expected_acceptance
schema = json.loads((N50 / "independent_referee_acceptance.schema.json").read_text())
assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"]) == set(acceptance)
for key, value in acceptance.items():
    if "const" in schema["properties"][key]: assert value == schema["properties"][key]["const"]
assert not (N50 / "independent_referee_acceptance.json").exists()
assert not (N50 / "launch_clearance.json").exists()
assert not (HERE / "launch_clearance.json").exists()
assert not any(HERE.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_SATISFIED_NEXT25_PROOF_BINDING_HELD_ACCEPTANCE_NOT_LAUNCH_READY",
    "closed_union": closed_union, "next25_groups": new_groups,
    "producer_batch_sha256": sha(N25 / "batch_result.json"),
    "producer_terminal_manifest_sha256": sha(N25 / "TERMINAL_MANIFEST.sha256"),
    "terminal_referee_result_sha256": sha(N25TERM / "results_referee.json"),
    "terminal_referee_manifest_sha256": sha(N25TERM / "FINAL_MANIFEST.sha256"),
    "dependency_result_manifest_membership": True,
    "held_acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"),
    "runner_interface_satisfied": False,
    "runner_interface_blocker": "sealed terminal result lacks runner-required closed_union field",
    "manifest_counts": manifest_counts,
    "scope": {"launch_authorized": False, "clearance_present": False, "solver_runs": 0},
}, sort_keys=True))
