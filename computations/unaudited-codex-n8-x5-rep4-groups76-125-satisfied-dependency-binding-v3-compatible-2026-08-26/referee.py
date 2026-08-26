#!/usr/bin/env python3
"""Independent frozen-runner interface and provenance replay for compatibility v3."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "computations"
HELD = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26"
FIRST_REF = C / "unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26"
MIDDLE_REF = C / "unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26"
REFUSAL = C / "unaudited-codex-n8-x5-rep4-groups76-125-prelaunch-interface-refusal-referee-2026-08-26"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

def replay(manifest: Path, required: Path | None = None) -> int:
    listed = {}
    for line in manifest.read_text().splitlines():
        if not line.strip(): continue
        digest, name = line.split(None, 1); path = (manifest.parent / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest; listed[path] = digest
    if required is not None: assert listed[required.resolve()] == sha(required)
    return len(listed)

counts = {
    "held": replay(HELD / "MANIFEST.sha256"),
    "first25_referee": replay(FIRST_REF / "FINAL_MANIFEST.sha256", FIRST_REF / "results_referee.json"),
    "groups26_75_referee": replay(MIDDLE_REF / "FINAL_MANIFEST.sha256", MIDDLE_REF / "results_referee.json"),
    "refusal": replay(REFUSAL / "FINAL_MANIFEST.sha256", REFUSAL / "results_referee.json"),
}
result = json.loads((HERE / "results_compatibility.json").read_text())
dep = json.loads((HERE / "normalized_dependencies.json").read_text())
accept = json.loads((HERE / "independent_referee_acceptance.json").read_text())
hostiles = json.loads((HERE / "results_hostile_tests.json").read_text())
first = json.loads((FIRST_REF / "results_referee.json").read_text())
middle = json.loads((MIDDLE_REF / "results_referee.json").read_text())
refusal = json.loads((REFUSAL / "results_referee.json").read_text())

assert result["status"] == "PASS_HELD_LAUNCH_READY_COMPATIBLE_V1_ZERO_RUNS_NO_CLEARANCE"
assert dep["schema"] == "KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1"
assert dep["status"] == "PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75"
assert dep["groups_closed_by_first"] == list(range(1,26)) and dep["groups_closed_by_middle"] == list(range(26,76))
assert dep["closed_union"] == list(range(76)) and dep["duplicates"] == dep["missing"] == dep["extra"] == []
assert dep["dependency_manifest_sha256"] == [sha(FIRST_REF / "FINAL_MANIFEST.sha256"), sha(MIDDLE_REF / "FINAL_MANIFEST.sha256")]
assert dep["dependency_result_sha256"] == [sha(FIRST_REF / "results_referee.json"), sha(MIDDLE_REF / "results_referee.json")]
assert dep["dependency_result_schemas"] == [first["schema"], middle["schema"]]
assert dep["dependency_result_statuses"] == [first["status"], middle["status"]]

runner_sha = sha(HELD / "run_groups76_125.py")
ledger_sha = sha(HELD / "source_ledger.json")
manifest_sha = sha(HELD / "MANIFEST.sha256")
expected_accept = {"schema":"KRENN_X5_REP4_GROUPS76_125_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1","status":"PASS_APPROVE_CONDITIONAL_REP4_GROUPS76_125_ONLY","held_manifest_sha256":manifest_sha,"source_ledger_sha256":ledger_sha,"normalized_dependencies_sha256":sha(HERE/"normalized_dependencies.json"),"runner_sha256":runner_sha,"required_closed_union":list(range(76)),"selected_group_ids":list(range(76,126)),"maximum_lane_count":50,"exact_Q_authorized":True,"parallel_authorized":False,"skip_reorder_relaunch_authorized":False}
assert accept == expected_accept
runner = (HELD / "run_groups76_125.py").read_text()
for token in ("KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1", "dependency_manifest_paths", "dependency_result_paths", "dependency_manifest_sha256", "dependency_result_sha256", "NATIVE_WALL=240", "WRAPPER_WALL=250", "RSS_CAP=8*1024**3"):
    assert token in runner

ledger = json.loads((HELD / "source_ledger.json").read_text())
assert [x["group_id"] for x in ledger["lanes"]] == list(range(76,126))
assert sum(x["source_bytes"] for x in ledger["lanes"]) == 90617222
for lane in ledger["lanes"]:
    source = HELD / lane["source_path"]; assert source.stat().st_size == lane["source_bytes"] and sha(source) == lane["source_sha256"]
assert hostiles["status"] == "PASS_15_INTERFACE_HOSTILES" and len(hostiles["tests"]) == 15 and all(hostiles["tests"].values())
assert refusal["status"] == "PASS_FAIL_CLOSED_PRELAUNCH_INTERFACE_MISMATCH_ZERO_RUNS" and refusal["batch_attempt_absent"] is True
for absent in ("normalized_dependencies.json", "independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HELD / absent).exists(), absent
assert not list(HERE.glob("*.tmp"))

out = {
    "schema": "KRENN_X5_REP4_GROUPS76_125_SATISFIED_BINDING_V3_COMPATIBILITY_REFEREE",
    "status": "PASS_INDEPENDENT_HELD_LAUNCH_READY_COMPATIBLE_V1_ZERO_RUNS_NO_CLEARANCE",
    "compatibility_result_sha256": sha(HERE / "results_compatibility.json"),
    "normalized_dependencies_sha256": sha(HERE / "normalized_dependencies.json"),
    "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"),
    "hostiles_sha256": sha(HERE / "results_hostile_tests.json"),
    "manifest_counts": counts, "closed_union": list(range(76)), "selected_group_ids": list(range(76,126)),
    "preservation": result["preservation"], "refusal_binding": result["refusal_binding"],
    "scope": result["scope"],
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "hostiles": 15, "sources": 50, "runs": 0}, sort_keys=True))
