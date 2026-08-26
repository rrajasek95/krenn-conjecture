#!/usr/bin/env python3
"""Build an exact V1 dependency payload compatible with the frozen rep4 runner."""
from __future__ import annotations
import copy, hashlib, json, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "computations"
HELD = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26"
HELD_REF = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-referee-2026-08-26"
OLD = C / "unaudited-codex-n8-x5-rep4-groups76-125-satisfied-dependency-binding-v2-2026-08-26"
REFUSAL = C / "unaudited-codex-n8-x5-rep4-groups76-125-prelaunch-interface-refusal-referee-2026-08-26"
FIRST = C / "unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26"
FIRST_REF = C / "unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26"
MIDDLE = C / "unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26"
MIDDLE_REF = C / "unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26"

PINS = {
    HELD / "MANIFEST.sha256": "0d2d7cfce0ed9e862b573e4fdc5791b3384c7bd21fbd6e9ff9e663c79f387115",
    HELD / "source_ledger.json": "b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb",
    HELD / "run_groups76_125.py": "3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd",
    HELD / "independent_referee_acceptance.schema.json": "f9b440bcd45fd3ca97f72f81c9426c3ef575665d43f3dc8225e0f1ba6d0f0e22",
    HELD_REF / "FINAL_MANIFEST.sha256": "50e6f9aa6e7a5751c324393d7a158b63d535bd63999070fe46f85b5c7fb75118",
    OLD / "FINAL_MANIFEST.sha256": "4fbc4430abf903b329519ca4499183c9571c574073b0be69eb36b0efd8f5ab73",
    REFUSAL / "results_referee.json": "601b5a44cd5ecb4ce07a5763e0a01ce1218a24b4608de8ca49024bd1fcb81321",
    REFUSAL / "FINAL_MANIFEST.sha256": "e1f0edef4b666292651e3f9e8d7d674df9a487384f509c48b24d1d65aacd0be1",
    FIRST / "batch_result.json": "6e982385c76686e743f740e4373b253a6a039c565e8cb6bd59a051cb189fc0dd",
    FIRST / "TERMINAL_MANIFEST.sha256": "8310384d0b26473fec57134cbb5f1b7c2c606e7b6a1af5dcefd5c5dfb3054260",
    FIRST_REF / "results_referee.json": "c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd",
    FIRST_REF / "FINAL_MANIFEST.sha256": "429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d",
    MIDDLE / "batch_result.json": "67a36a426418ab7b65ea60aed934aed022c62e2b2ab5257b7512c9efd6a0298d",
    MIDDLE / "TERMINAL_MANIFEST.sha256": "b8ba01dcfb43cdf92244fe85703c5423a9186c6d44c73a73df2ea694f585ff98",
    MIDDLE_REF / "results_referee.json": "611d09abe73ef7032abf6280af3d9428e64d08db6aa731d1fde67ea004322e13",
    MIDDLE_REF / "FINAL_MANIFEST.sha256": "76cbf6f8ec9759cfb8f3ba7abc7d27b5e2aa13b24fce0201a6e17299fcd318e1",
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def atomic(path: Path, value: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)

def replay(manifest: Path, result: Path) -> int:
    listed = {}
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        path = (manifest.parent / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest
        listed[path] = digest
    assert result.resolve() in listed and listed[result.resolve()] == sha(result)
    return len(listed)

def normalize(first: dict, middle: dict, manifest_paths: list[str], result_paths: list[str], manifest_hashes: list[str], result_hashes: list[str]) -> dict:
    assert first["schema"] == "KRENN_X5_REP4_FIRST25_EXACT_Q_TERMINAL_REFEREE_V1"
    assert first["status"] == "PASS_EXACT_GROUPS_1_25_UNIT"
    assert first["unit_groups_closed"] == list(range(1, 26))
    assert first["closed_union"] == list(range(26)) and first["sealed_group0"] is True
    assert middle["schema"] == "KRENN_X5_REP4_GROUPS26_75_EXACT_Q_TERMINAL_REFEREE_V1"
    assert middle["status"] == "PASS_ALL_50_EXACT_Q_UNIT_IDEALS"
    assert middle["dependency_closed_union_before_batch"] == list(range(26))
    assert middle["groups_closed"] == list(range(26, 76))
    assert middle["closed_union_after_batch"] == list(range(76))
    assert len(manifest_paths) == len(result_paths) == len(manifest_hashes) == len(result_hashes) == 2
    assert all(isinstance(x, str) and x.startswith("computations/") for x in manifest_paths + result_paths)
    assert all(re.fullmatch(r"[0-9a-f]{64}", x) for x in manifest_hashes + result_hashes)
    assert manifest_paths == [
        "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
        "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    ]
    assert result_paths == [
        "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/results_referee.json",
        "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/results_referee.json",
    ]
    assert manifest_hashes == ["429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d", "76cbf6f8ec9759cfb8f3ba7abc7d27b5e2aa13b24fce0201a6e17299fcd318e1"]
    assert result_hashes == ["c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd", "611d09abe73ef7032abf6280af3d9428e64d08db6aa731d1fde67ea004322e13"]
    closed = [0] + first["unit_groups_closed"] + middle["groups_closed"]
    assert closed == list(range(76)) and len(closed) == len(set(closed))
    return {
        "schema": "KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1",
        "status": "PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75",
        "dependency_manifest_paths": manifest_paths,
        "dependency_result_paths": result_paths,
        "dependency_manifest_sha256": manifest_hashes,
        "dependency_result_sha256": result_hashes,
        "dependency_result_schemas": [first["schema"], middle["schema"]],
        "dependency_result_statuses": [first["status"], middle["status"]],
        "groups_closed_by_first": list(range(1, 26)),
        "groups_closed_by_middle": list(range(26, 76)),
        "baseline_closed_group": 0,
        "closed_union": list(range(76)),
        "duplicates": [], "missing": [], "extra": [],
    }

for path, digest in PINS.items():
    assert sha(path) == digest, (path, sha(path), digest)
refusal = json.loads((REFUSAL / "results_referee.json").read_text())
assert refusal["status"] == "PASS_FAIL_CLOSED_PRELAUNCH_INTERFACE_MISMATCH_ZERO_RUNS"
assert refusal["arithmetic_launched"] is False and refusal["results_absent"] is True
assert refusal["batch_attempt_absent"] is True and refusal["future_groups_attempted"] == []
assert refusal["classification"]["frozen_runner_requires_schema"] == "KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1"

manifest_paths = [
    str((FIRST_REF / "FINAL_MANIFEST.sha256").relative_to(ROOT)),
    str((MIDDLE_REF / "FINAL_MANIFEST.sha256").relative_to(ROOT)),
]
result_paths = [
    str((FIRST_REF / "results_referee.json").relative_to(ROOT)),
    str((MIDDLE_REF / "results_referee.json").relative_to(ROOT)),
]
manifest_hashes = [PINS[FIRST_REF / "FINAL_MANIFEST.sha256"], PINS[MIDDLE_REF / "FINAL_MANIFEST.sha256"]]
result_hashes = [PINS[FIRST_REF / "results_referee.json"], PINS[MIDDLE_REF / "results_referee.json"]]
first = json.loads((FIRST_REF / "results_referee.json").read_text())
middle = json.loads((MIDDLE_REF / "results_referee.json").read_text())
replay_counts = [replay(FIRST_REF / "FINAL_MANIFEST.sha256", FIRST_REF / "results_referee.json"), replay(MIDDLE_REF / "FINAL_MANIFEST.sha256", MIDDLE_REF / "results_referee.json")]
normalized = normalize(first, middle, manifest_paths, result_paths, manifest_hashes, result_hashes)
atomic(HERE / "normalized_dependencies.json", normalized)
normalized_sha = sha(HERE / "normalized_dependencies.json")

acceptance = {
    "schema": "KRENN_X5_REP4_GROUPS76_125_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_CONDITIONAL_REP4_GROUPS76_125_ONLY",
    "held_manifest_sha256": PINS[HELD / "MANIFEST.sha256"],
    "source_ledger_sha256": PINS[HELD / "source_ledger.json"],
    "normalized_dependencies_sha256": normalized_sha,
    "runner_sha256": PINS[HELD / "run_groups76_125.py"],
    "required_closed_union": list(range(76)), "selected_group_ids": list(range(76, 126)),
    "maximum_lane_count": 50, "exact_Q_authorized": True,
    "parallel_authorized": False, "skip_reorder_relaunch_authorized": False,
}
atomic(HERE / "independent_referee_acceptance.json", acceptance)
schema = json.loads((HELD / "independent_referee_acceptance.schema.json").read_text())
assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"]) == set(acceptance)
for key, rule in schema["properties"].items():
    if "const" in rule:
        assert acceptance[key] == rule["const"]
    elif "pattern" in rule:
        assert re.fullmatch(rule["pattern"], acceptance[key])

ledger = json.loads((HELD / "source_ledger.json").read_text())
assert [x["group_id"] for x in ledger["lanes"]] == list(range(76, 126))
for lane in ledger["lanes"]:
    source = HELD / lane["source_path"]
    assert source.stat().st_size == lane["source_bytes"] and sha(source) == lane["source_sha256"]
assert sum(x["source_bytes"] for x in ledger["lanes"]) == 90617222

def rejects(mutator) -> bool:
    f, m = copy.deepcopy(first), copy.deepcopy(middle)
    mp, rp, mh, rh = map(copy.deepcopy, (manifest_paths, result_paths, manifest_hashes, result_hashes))
    mutator(f, m, mp, rp, mh, rh)
    try:
        normalize(f, m, mp, rp, mh, rh)
    except (AssertionError, KeyError, TypeError):
        return True
    return False

tests = {
    "stale_first_status": rejects(lambda f,m,mp,rp,mh,rh: f.__setitem__("status", "PASS_ALL_25_EXACT_Q_UNIT_IDEALS")),
    "wrong_first_schema": rejects(lambda f,m,mp,rp,mh,rh: f.__setitem__("schema", "STALE")),
    "missing_first_group_array": rejects(lambda f,m,mp,rp,mh,rh: f.pop("unit_groups_closed")),
    "reordered_first_groups": rejects(lambda f,m,mp,rp,mh,rh: f.__setitem__("unit_groups_closed", list(range(25,0,-1)))),
    "duplicate_first_group": rejects(lambda f,m,mp,rp,mh,rh: f.__setitem__("unit_groups_closed", [1] + list(range(1,25)))),
    "wrong_middle_status": rejects(lambda f,m,mp,rp,mh,rh: m.__setitem__("status", "PASS_ALL_50_UNIT")),
    "wrong_middle_schema": rejects(lambda f,m,mp,rp,mh,rh: m.__setitem__("schema", "STALE")),
    "middle_union_gap": rejects(lambda f,m,mp,rp,mh,rh: m.__setitem__("groups_closed", list(range(27,77)))),
    "manifest_path_array_short": rejects(lambda f,m,mp,rp,mh,rh: mp.pop()),
    "result_path_array_swapped": rejects(lambda f,m,mp,rp,mh,rh: rp.reverse()),
    "manifest_hash_array_short": rejects(lambda f,m,mp,rp,mh,rh: mh.pop()),
    "result_hash_malformed": rejects(lambda f,m,mp,rp,mh,rh: rh.__setitem__(0, "0" * 63)),
}
runner_text = (HELD / "run_groups76_125.py").read_text()
tests["runner_requires_v1_schema"] = "dep['schema']=='KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1'" in runner_text
tests["runner_requires_path_hash_arrays"] = all(token in runner_text for token in ("dependency_manifest_paths", "dependency_manifest_sha256", "dependency_result_paths", "dependency_result_sha256"))
tests["old_v2_hash_rejected_by_acceptance"] = normalized_sha != "a9134eef5e3b2f98782197809695b8f672841eb92957e085b1c0f264840c289b"
assert len(tests) == 15 and all(tests.values())
hostiles = {"schema": "KRENN_X5_REP4_GROUPS76_125_COMPATIBILITY_HOSTILES_V1", "status": "PASS_15_INTERFACE_HOSTILES", "tests": tests, "solver_runs": 0, "attempts": 0}
atomic(HERE / "results_hostile_tests.json", hostiles)

result = {
    "schema": "KRENN_X5_REP4_GROUPS76_125_SATISFIED_BINDING_V3_COMPATIBILITY",
    "status": "PASS_HELD_LAUNCH_READY_COMPATIBLE_V1_ZERO_RUNS_NO_CLEARANCE",
    "normalized_dependencies_sha256": normalized_sha,
    "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"),
    "runner_interface": {"frozen_runner_sha256": PINS[HELD / "run_groups76_125.py"], "interface_only_repair": True, "runner_v2_created": False},
    "dependency_replay": {"manifest_entries": replay_counts, "closed_union": list(range(76)), "duplicates": [], "missing": [], "extra": []},
    "preservation": {"source_count": 50, "source_bytes": 90617222, "all_source_hashes_replayed": True, "source_ledger_sha256": PINS[HELD / "source_ledger.json"], "runner_sha256": PINS[HELD / "run_groups76_125.py"], "sources_rewritten": 0, "runner_rewritten": False, "math_order_resources_unchanged": True},
    "refusal_binding": {"result_sha256": PINS[REFUSAL / "results_referee.json"], "manifest_sha256": PINS[REFUSAL / "FINAL_MANIFEST.sha256"], "zero_run": True, "zero_attempt": True},
    "supersession": {"old_binding_manifest_sha256": PINS[OLD / "FINAL_MANIFEST.sha256"], "old_v2_payload_not_installable": True, "old_acceptance_not_installable": True},
    "hostiles_sha256": sha(HERE / "results_hostile_tests.json"),
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "scope": {"held_launch_ready_metadata": True, "install_into_held_performed": False, "launch_clearance_materialized": False, "solver_runs": 0, "attempts": 0, "mathematical_coverage_added": False},
}
atomic(HERE / "results_compatibility.json", result)
print(json.dumps({"status": result["status"], "hostiles": 15, "sources": 50, "runs": 0, "attempts": 0}, sort_keys=True))
