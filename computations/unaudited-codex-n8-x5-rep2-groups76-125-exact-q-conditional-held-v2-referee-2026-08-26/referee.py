#!/usr/bin/env python3
"""Independent held-only referee for the superseding rep2 groups 76..125 v2 plan."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
V2 = ROOT / "computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-v2-2026-08-26"
V1 = ROOT / "computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26"
REJECTION = ROOT / "computations/unaudited-codex-n8-x5-rep2-groups76-125-conditional-independent-referee-2026-08-26"
IDS = list(range(76, 126))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path: Path, base: Path) -> int:
    count = 0
    for raw in path.read_text().splitlines():
        digest, name = raw.split(None, 1)
        target = Path(name.strip())
        target = target if target.is_absolute() else (base / target).resolve()
        assert target.is_file(), target
        assert sha(target) == digest, (target, sha(target), digest)
        count += 1
    return count


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Rejection is a load-bearing dependency, not an overwritten historical note.
assert sha(REJECTION / "FINAL_MANIFEST.sha256") == "58910fda9efb0c9157822910ac5e641cd770cf69fe458f34bdd1a66537cd0c47"
replay(REJECTION / "FINAL_MANIFEST.sha256", REJECTION)
assert sha(REJECTION / "results_independent_referee.json") == "09109d866f5c4241bc8fbbde961dcc6f504f9d1dc09cc449bcfced7f14e0f08f"
rejected = json.loads((REJECTION / "results_independent_referee.json").read_text())
assert rejected["status"] == "REJECT_HELD_RUNNER_DOES_NOT_REPLAY_DEPENDENCY_ARTIFACTS_ZERO_COVERAGE"
assert rejected["runner_replay_gap"] == {
    "hashes_compared_to_files": False,
    "manifest_paths_reopened": False,
    "result_paths_reopened": False,
    "schema_status_groups_union_checked": True,
}

# V2 and the exact V1 source inventory both replay completely.
assert sha(V2 / "MANIFEST.sha256") == "f62e7a7ee38ca747dfd2ac88774d9ee4251f73ef514e2410ddba092da9830d6b"
v2_manifest_entries = replay(V2 / "MANIFEST.sha256", V2)
assert sha(V2 / "run_groups76_125_v2.py") == "b9b3f880b216196658ad827d25b0a612a5334a6582ca76cc6a48d332c36bd826"
assert sha(V2 / "dependency_verifier.py") == "42461b1d52f4909a3439a484d8b7b34b658c767a9ad246d9f4a98cc2929f30b1"
assert sha(V2 / "source_reference_ledger.json") == "6f44241c35e197d557238a405c7549348a39e0f60d8f03f4d092eb3945ca9083"
assert sha(V1 / "MANIFEST.sha256") == "43c34a80cc55488e4840b5d04001211d21f8acbdc6fc62bc5cc5e0e366fc5b0a"
replay(V1 / "MANIFEST.sha256", V1)
assert sha(V1 / "source_ledger.json") == "4aa023638d439fd1250b66593d93dd29dd4472831449ff571e2730bf6950b4ce"

ledger = json.loads((V1 / "source_ledger.json").read_text())
reference = json.loads((V2 / "source_reference_ledger.json").read_text())
lanes = ledger["lanes"]
refs = reference["sources"]
assert [x["group_id"] for x in lanes] == [x["group_id"] for x in refs] == IDS
assert [x["ordinal"] for x in lanes] == list(range(1, 51))
assert reference["source_count"] == 50 and reference["source_mismatches"] == 0
assert reference["selection"]["required_closed_union"] == list(range(76))
assert reference["selection"]["selected_group_ids"] == IDS
source_bytes = 0
for lane, ref in zip(lanes, refs):
    source = V1 / lane["source_path"]
    assert source.resolve() == (ROOT / ref["path"]).resolve()
    assert ref["sha256"] == lane["source_sha256"] == sha(source)
    assert ref["bytes"] == lane["source_bytes"] == source.stat().st_size
    assert ref["variables"] == lane["variables"] == 91
    assert ref["generators"] == lane["generators"] == 6577
    source_bytes += source.stat().st_size
assert source_bytes == reference["total_bytes"] == 92375820

schedule = json.loads((V2 / "held_schedule_v2.json").read_text())
assert schedule["status"] == "PASS_SUPERSEDED_PROVENANCE_REPLAY_HELD_ZERO_RUN"
assert schedule["supersedes"]["rejection_manifest_sha256"] == sha(REJECTION / "FINAL_MANIFEST.sha256")
assert schedule["supersedes"]["rejected_runner_sha256"] == "c1aa9303186a1a1e1efaa867471192b69b746aac52741ad227d901db34cbe24a"
assert schedule["selection"]["required_closed_union"] == list(range(76))
assert schedule["selection"]["selected_group_ids"] == IDS
execution = schedule["execution"]
assert execution["order"] == IDS and execution["maximum_lane_count"] == 50
assert execution["native_wall_seconds_each"] == 240 and execution["wrapper_wall_seconds_each"] == 250
assert execution["rss_cap_bytes_each"] == 8 * 1024**3 and execution["stop_first"] is True
assert execution["parallel"] is execution["relaunch"] is execution["reorder"] is execution["skip"] is False

# Import the exact adapter and repaired verifier, then independently replay all
# 17 hostile classes and a positive four-artifact fixture.
adapter = load_module("rep2_v1_adapter_for_referee", V1 / "normalize_dependencies.py")
verifier = load_module("rep2_v2_dependency_verifier_for_referee", V2 / "dependency_verifier.py")
contract = json.loads((V1 / "future_dependencies.json").read_text())
assert sha(V1 / "future_dependencies.json") == "5173f8f03b8eb7feff428573cb6a0b2813ef1e6cb1d4c4696543c30585e522e4"
assert contract["status"] == "UNSATISFIED_BOTH_NULL_HASH_PAIRS" and contract["satisfied"] is False
assert contract["required_closed_union"] == list(range(76))
assert all(dep["satisfied"] is False and dep["manifest_sha256"] is None and dep["result_sha256"] is None for dep in contract["dependencies"])

first = {
    "schema": contract["dependencies"][0]["result_schema"],
    "status": contract["dependencies"][0]["result_status"],
    "groups_closed": list(range(1, 26)),
}
middle = {
    "schema": contract["dependencies"][1]["result_schema"],
    "status": contract["dependencies"][1]["result_status"],
    "groups_closed": list(range(26, 76)),
}
hostiles = {}


def reject(name, contract_mutator=None, first_mutator=None, middle_mutator=None, mhs=None, rhs=None):
    c, f, m = copy.deepcopy(contract), copy.deepcopy(first), copy.deepcopy(middle)
    if contract_mutator:
        contract_mutator(c)
    if first_mutator:
        first_mutator(f)
    if middle_mutator:
        middle_mutator(m)
    try:
        adapter.validate_payload(c, f, m, mhs or ["a" * 64, "b" * 64], rhs or ["c" * 64, "d" * 64])
    except (AssertionError, KeyError, TypeError):
        hostiles[name] = True
    else:
        hostiles[name] = False


reject("null_treated_satisfied", lambda c: c.__setitem__("satisfied", True))
reject("future_hash_injected", lambda c: c["dependencies"][0].__setitem__("manifest_sha256", "0" * 64))
reject("first_wrong_schema", first_mutator=lambda x: x.__setitem__("schema", "wrong"))
reject("first_wrong_status", first_mutator=lambda x: x.__setitem__("status", "wrong"))
reject("first_missing", first_mutator=lambda x: x["groups_closed"].pop())
reject("first_duplicate", first_mutator=lambda x: x["groups_closed"].__setitem__(24, 24))
reject("first_reordered", first_mutator=lambda x: x["groups_closed"].reverse())
reject("middle_wrong_schema", middle_mutator=lambda x: x.__setitem__("schema", "wrong"))
reject("middle_wrong_status", middle_mutator=lambda x: x.__setitem__("status", "wrong"))
reject("middle_missing", middle_mutator=lambda x: x["groups_closed"].pop())
reject("middle_duplicate", middle_mutator=lambda x: x["groups_closed"].__setitem__(49, 74))
reject("middle_reordered", middle_mutator=lambda x: x["groups_closed"].reverse())
reject("cross_overlap", middle_mutator=lambda x: x["groups_closed"].__setitem__(0, 25))
reject("union_extra", lambda c: c["required_closed_union"].append(76))
reject("bad_manifest_hash", mhs=["a" * 63, "b" * 64])
reject("bad_result_hash", rhs=["c" * 64, "z" * 64])
fabricated = adapter.validate_payload(contract, first, middle, ["a" * 64, "b" * 64], ["c" * 64, "d" * 64])
try:
    verifier.verify_payload(contract, fabricated, ROOT)
except (AssertionError, FileNotFoundError):
    hostiles["fabricated_or_stale_normalized_with_absent_artifacts"] = True
else:
    hostiles["fabricated_or_stale_normalized_with_absent_artifacts"] = False
assert len(hostiles) == 17 and all(hostiles.values())
producer_hostiles = json.loads((V2 / "results_hostile_tests_v2.json").read_text())
assert producer_hostiles["status"] == "PASS_17_HOSTILES_INCLUDING_STALE_NORMALIZED_PROVENANCE"
assert producer_hostiles["tests"] == hostiles and producer_hostiles["solver_runs"] == 0

# A positive isolated fixture proves that the verifier actually reopens both
# manifests and results, replays every listed hash, and reconstructs 0..75.
with tempfile.TemporaryDirectory(prefix="rep2-v2-referee-") as temp:
    fixture_root = Path(temp)
    c = copy.deepcopy(contract)
    fixture_results = [copy.deepcopy(first), copy.deepcopy(middle)]
    manifest_hashes = []
    result_hashes = []
    for index, (dep, result) in enumerate(zip(c["dependencies"], fixture_results), 1):
        directory = fixture_root / f"pair{index}"
        directory.mkdir()
        result_path = directory / "results_referee.json"
        result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        result_hash = sha(result_path)
        manifest_path = directory / "FINAL_MANIFEST.sha256"
        manifest_path.write_text(f"{result_hash}  results_referee.json\n")
        dep["manifest_path"] = str(manifest_path.relative_to(fixture_root))
        dep["result_path"] = str(result_path.relative_to(fixture_root))
        manifest_hashes.append(sha(manifest_path))
        result_hashes.append(result_hash)
    normalized = adapter.validate_payload(c, fixture_results[0], fixture_results[1], manifest_hashes, result_hashes)
    positive = verifier.verify_payload(c, normalized, fixture_root)
    assert positive["status"] == "PASS_REPLAYED_ALL_FOUR_DEPENDENCY_ARTIFACTS_EXACT_UNION_0_75"
    assert positive["closed_union"] == list(range(76)) and positive["manifest_entries"] == [1, 1]
    # Staleness after normalization is rejected by the same launch-time replay.
    stale_result = fixture_root / c["dependencies"][1]["result_path"]
    stale_result.write_text(stale_result.read_text() + "\n")
    try:
        verifier.verify_payload(c, normalized, fixture_root)
    except AssertionError:
        launch_stale_rejected = True
    else:
        launch_stale_rejected = False
    assert launch_stale_rejected

# Exact code-path audit: normalization invokes the verifier after reading and
# hashing artifacts; launch invokes it again before acceptance/attempt/solve.
normalizer_text = (V2 / "normalize_dependencies_v2.py").read_text()
runner_text = (V2 / "run_groups76_125_v2.py").read_text()
verifier_text = (V2 / "dependency_verifier.py").read_text()
assert normalizer_text.count("verify_payload(") == 1
assert runner_text.count("verify_payload(") == 1
assert runner_text.index("replay=verify_payload(") < runner_text.index("acceptance=HERE/") < runner_text.index("exclusive(HERE/'BATCH_ATTEMPT.json'") < runner_text.index("subprocess.Popen(")
for token in (
    "manifest.is_file() and result_path.is_file()",
    "sha(manifest)==mh and sha(result_path)==rh",
    "for line in manifest.read_text().splitlines()",
    "sha(path)==digest",
    "result_path.resolve() in listed",
    "result['schema']==dep['result_schema']",
    "result['status']==dep['result_status']",
    "result['groups_closed']==dep['groups_closed']",
    "closed==list(range(76))",
):
    assert token in verifier_text, token

# Held means the future pair, normalization, authorization, attempt, and solve
# artifacts are all absent now.
future_paths = [ROOT / dep[key] for dep in contract["dependencies"] for key in ("manifest_path", "result_path")]
assert len(future_paths) == 4 and all(not path.exists() for path in future_paths)
absent = [
    V2 / "normalized_dependencies.json",
    V2 / "independent_referee_acceptance.json",
    V2 / "launch_clearance.json",
    V2 / "BATCH_ATTEMPT.json",
    V2 / "batch_result.json",
    V2 / "results",
]
assert all(not path.exists() for path in absent)
assert not list(V2.glob("*.tmp"))

result = {
    "schema": "KRENN_X5_REP2_GROUPS76_125_V2_HELD_INDEPENDENT_REFEREE_V1",
    "status": "PASS_APPROVE_CONDITIONAL_REP2_GROUPS76_125_V2_HELD_ZERO_RUN",
    "held_manifest_sha256": sha(V2 / "MANIFEST.sha256"),
    "held_manifest_entries_replayed": v2_manifest_entries,
    "rejection_manifest_sha256": sha(REJECTION / "FINAL_MANIFEST.sha256"),
    "rejection_bound": True,
    "runner_sha256": sha(V2 / "run_groups76_125_v2.py"),
    "dependency_verifier_sha256": sha(V2 / "dependency_verifier.py"),
    "source_reference_ledger_sha256": sha(V2 / "source_reference_ledger.json"),
    "original_source_ledger_sha256": sha(V1 / "source_ledger.json"),
    "sources_preserved": 50,
    "source_bytes": source_bytes,
    "source_mismatches": 0,
    "hostiles_replayed": 17,
    "positive_four_artifact_replay": True,
    "stale_after_normalization_rejected_at_launch": True,
    "required_closed_union": list(range(76)),
    "selected_group_ids": IDS,
    "future_artifacts_absent": [str(path.relative_to(ROOT)) for path in future_paths],
    "normalized_dependencies_present": False,
    "acceptance_present": False,
    "clearance_present": False,
    "attempt_present": False,
    "results_present": False,
    "solver_runs": 0,
    "groups_newly_closed": 0,
    "mathematical_coverage_added": False,
    "held_only": True,
    "launch_authorized": False,
    "conjecture_closed": False,
}
(HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
approval = {
    "schema": "KRENN_X5_REP2_GROUPS76_125_EXACT_Q_INDEPENDENT_ACCEPTANCE_V2",
    "status": "PASS_APPROVE_CONDITIONAL_REP2_GROUPS76_125_V2_ONLY",
    "held_manifest_sha256": result["held_manifest_sha256"],
    "source_ledger_sha256": result["original_source_ledger_sha256"],
    "source_reference_ledger_sha256": result["source_reference_ledger_sha256"],
    "dependency_verifier_sha256": result["dependency_verifier_sha256"],
    "runner_sha256": result["runner_sha256"],
    "required_closed_union": list(range(76)),
    "selected_group_ids": IDS,
    "maximum_lane_count": 50,
    "exact_Q_authorized": True,
    "parallel_authorized": False,
    "skip_reorder_relaunch_authorized": False,
    "normalized_dependencies_sha256": None,
    "future_artifacts_absent": 4,
    "launch_clearance_required": True,
    "launch_clearance_present": False,
    "solver_runs": 0,
}
(HERE / "HELD_APPROVAL.json").write_text(json.dumps(approval, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "result_sha256": sha(HERE / "results_referee.json"), "approval_sha256": sha(HERE / "HELD_APPROVAL.json")}, sort_keys=True))
