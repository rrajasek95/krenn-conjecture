#!/usr/bin/env python3
"""Independent zero-run referee for normalized rep1 next50 v2."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PKG = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25"
OLD = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25"
BASE = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-referee-2026-08-25"
NEXT = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-terminal-referee-2026-08-25"
BIND = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-next25-satisfied-binding-audit-2026-08-25"

PINS = {
    PKG / "MANIFEST.sha256": "7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da",
    PKG / "normalize_next25_dependency.py": "c9c3d365f0f2fb3c9a03656822b4112b245455745dd4f707367fff6c6c2e6d11",
    PKG / "normalized_next25_dependency.json": "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76",
    PKG / "results_adapter_tests.json": "b9092d659a2fa866e10e63335943b70ad116178b5a18580e42ba718469bb9b6c",
    PKG / "run_next50_v2.py": "b9fc730669e6e5fc4799e9efbf4e6f12b1f443acc004af9bc536be851c4d8388",
    PKG / "source_ledger.json": "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172",
    OLD / "MANIFEST.sha256": "db8aa8acd4977934273c28249ffba8930c102cec2fc10bad9d86edb7fa51423d",
    OLD / "source_ledger.json": "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172",
    BASE / "FINAL_MANIFEST.sha256": "950e50ea1b1af733b5f20fad076357d29ee76a7b85009c7b93fcad76b1406c75",
    BASE / "results_referee.json": "a4a959cc1eb2392e64fc0c1d8e540deace8141ae43d50fbd7c30a14d6ef6c189",
    NEXT / "FINAL_MANIFEST.sha256": "b5de471b2cbd4f5197492c37f7f885f77059a9eced3e66830998c8edd5d62cde",
    NEXT / "results_referee.json": "a2599e9cee2739fb372e1d45db9625dc999510eb58407609cb581e73acbce450",
    BIND / "FINAL_MANIFEST.sha256": "18e93f3a635496987e58320858bff91e93a965a72504bba7762a9e5675a6b341",
    BIND / "results_binding.json": "e5f441d67b9e372e5946fd0de01b2bab0cc0d13b0bab729f8fceba3c0f3c0880",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def replay(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        expected, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            target = (path.parent / target).resolve()
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count


for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)
manifest_counts = {
    "normalized": replay(PKG / "MANIFEST.sha256"),
    "baseline": replay(BASE / "FINAL_MANIFEST.sha256"),
    "next25": replay(NEXT / "FINAL_MANIFEST.sha256"),
    "binding": replay(BIND / "FINAL_MANIFEST.sha256"),
}

baseline = json.loads((BASE / "results_referee.json").read_text())
terminal = json.loads((NEXT / "results_referee.json").read_text())
binding = json.loads((BIND / "results_binding.json").read_text())
normalized = json.loads((PKG / "normalized_next25_dependency.json").read_text())
tests = json.loads((PKG / "results_adapter_tests.json").read_text())

expected_baseline = list(range(11)) + [13, 15]
expected_next25 = [11, 12, 14] + list(range(16, 38))
expected_union = list(range(38))


def independent_normalize(b: dict, t: dict, d: dict) -> list[int]:
    assert b["schema"] == "KRENN_X5_REP1_NEXT25_EXACT_Q_HELD_REFEREE_V1"
    assert b["status"] == "PASS_APPROVED_HELD_STRICT_REP1_NEXT25_ZERO_RUNS"
    assert b["closed_baseline_group_ids"] == expected_baseline
    assert t["schema"] == "KRENN_X5_REP1_NEXT25_EXACT_Q_TERMINAL_REFEREE_V1"
    assert t["status"] == "PASS_ALL_25_EXACT_Q_UNIT_IDEALS"
    assert t["groups_closed"] == expected_next25 and t["new_groups_closed"] == 25
    assert t["strict_order"] and not t["parallel"] and not t["skipped"] and not t["relaunch"]
    assert d["schema"] == "KRENN_X5_REP1_NEXT50_NEXT25_SATISFIED_BINDING_AUDIT_V1"
    assert d["status"] == "PASS_SATISFIED_NEXT25_PROOF_BINDING_HELD_ACCEPTANCE_NOT_LAUNCH_READY"
    assert d["dependency_proof_satisfied"] and d["dependency_result_manifest_membership"]
    assert d["next25_terminal_referee_manifest_sha256"] == PINS[NEXT / "FINAL_MANIFEST.sha256"]
    assert d["next25_terminal_referee_result_sha256"] == PINS[NEXT / "results_referee.json"]
    assert len(set(expected_baseline)) == 13 and len(set(expected_next25)) == 25
    assert set(expected_baseline).isdisjoint(expected_next25)
    union = sorted(expected_baseline + expected_next25)
    assert union == expected_union and d["closed_union"] == union
    return union


assert independent_normalize(baseline, terminal, binding) == expected_union
assert normalized["baseline_group_ids"] == expected_baseline
assert normalized["next25_groups_closed"] == expected_next25
assert normalized["closed_union"] == expected_union
assert normalized["set_proof"] == {
    "baseline_count": 13, "next25_count": 25, "intersection": [], "union_count": 38,
    "missing_from_0_37": [], "extra_outside_0_37": [], "duplicates": [],
}
assert normalized["pins"] == {
    "baseline_manifest_sha256": PINS[BASE / "FINAL_MANIFEST.sha256"],
    "baseline_result_sha256": PINS[BASE / "results_referee.json"],
    "next25_terminal_manifest_sha256": PINS[NEXT / "FINAL_MANIFEST.sha256"],
    "next25_terminal_result_sha256": PINS[NEXT / "results_referee.json"],
    "binding_audit_manifest_sha256": PINS[BIND / "FINAL_MANIFEST.sha256"],
    "binding_audit_result_sha256": PINS[BIND / "results_binding.json"],
}

# Independently replay the same twelve hostile categories.
hostiles: dict[str, bool] = {}


def rejected(name: str, mutate) -> None:
    b, t, d = copy.deepcopy(baseline), copy.deepcopy(terminal), copy.deepcopy(binding)
    mutate(b, t, d)
    try:
        independent_normalize(b, t, d)
    except (AssertionError, KeyError, TypeError):
        hostiles[name] = True
    else:
        hostiles[name] = False


rejected("baseline_missing", lambda b, t, d: b["closed_baseline_group_ids"].pop())
rejected("baseline_duplicate", lambda b, t, d: b["closed_baseline_group_ids"].append(15))
rejected("baseline_extra", lambda b, t, d: b["closed_baseline_group_ids"].append(99))
rejected("next25_missing", lambda b, t, d: t["groups_closed"].pop())
rejected("next25_duplicate", lambda b, t, d: t["groups_closed"].append(37))
rejected("next25_extra", lambda b, t, d: t["groups_closed"].append(99))
rejected("next25_overlap", lambda b, t, d: t["groups_closed"].__setitem__(0, 0))
rejected("next25_reorder", lambda b, t, d: t["groups_closed"].reverse())
rejected("terminal_status", lambda b, t, d: t.__setitem__("status", "WRONG"))
rejected("terminal_skipped", lambda b, t, d: t.__setitem__("skipped", True))
rejected("binding_union", lambda b, t, d: d["closed_union"].pop())
rejected("binding_manifest", lambda b, t, d: d.__setitem__("next25_terminal_referee_manifest_sha256", "0" * 64))
assert len(hostiles) == 12 and all(hostiles.values())
assert tests["hostile_count"] == 12 and tests["hostile_tests"] == hostiles
assert tests["solver_runs"] == 0 and tests["status"] == "PASS_SCHEMA_EQUIVALENCE_AND_HOSTILES"

# The mathematical sources and ledger are byte-for-byte the frozen v1 payload.
assert (PKG / "source_ledger.json").read_bytes() == (OLD / "source_ledger.json").read_bytes()
ledger = json.loads((PKG / "source_ledger.json").read_text())
lanes = ledger["lanes"]
selected = list(range(38, 88))
assert [lane["group_id"] for lane in lanes] == selected
assert [lane["ordinal"] for lane in lanes] == list(range(1, 51))
total_bytes = 0
for lane in lanes:
    new_source = PKG / lane["source_path"]
    old_source = OLD / lane["source_path"]
    assert sha(new_source) == sha(old_source) == lane["source_sha256"]
    assert new_source.stat().st_size == old_source.stat().st_size == lane["source_bytes"]
    assert lane["variables"] == 91 and lane["generators"] == 6577
    total_bytes += lane["source_bytes"]
assert total_bytes == 89_221_420

schedule = json.loads((PKG / "held_schedule_v2.json").read_text())
execution = schedule["execution"]
assert execution["order"] == selected and execution["maximum_lane_count"] == 50
assert execution["native_wall_seconds_each"] == 240
assert execution["wrapper_wall_seconds_each"] == 250
assert execution["rss_cap_bytes_each"] == 8 * 1024**3
assert execution["parallel"] is execution["skip"] is execution["reorder"] is execution["relaunch"] is False
assert execution["stop_whole_batch_on"] == ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]

runner = (PKG / "run_next50_v2.py").read_text()
ast.parse(runner)
for token in (
    "SELECTED=tuple(range(38,88))", "NATIVE_WALL=240", "WRAPPER_WALL=250",
    "RSS_CAP=8*1024**3", "proc_listpgrppids", "group_rss(process.pid,True)",
    "normalized['closed_union']==list(range(38))", "for lane in lanes:",
    "if not unit:stop=", "break", "'parallel':False", "'relaunch':False",
    "exclusive(HERE/'BATCH_ATTEMPT.json'", "atomic(HERE/'results'/",
):
    assert token in runner, token
assert runner.count("subprocess.Popen(") == 1
assert runner.index("assert manifest.is_file() and acceptance.is_file() and clearance.is_file()") < runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'") < runner.index("subprocess.Popen(")

# Held only: no acceptance, clearance, attempt, result directory, temporary, or solver output.
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (PKG / absent).exists(), absent
assert not list(PKG.rglob("*.tmp"))

result = {
    "schema": "KRENN_X5_REP1_NEXT50_NORMALIZED_HELD_V2_REFEREE_V1",
    "status": "PASS_APPROVED_HELD_NORMALIZED_NEXT50_V2_ZERO_RUNS",
    "producer_manifest_sha256": PINS[PKG / "MANIFEST.sha256"],
    "adapter_sha256": PINS[PKG / "normalize_next25_dependency.py"],
    "normalized_dependency_sha256": PINS[PKG / "normalized_next25_dependency.json"],
    "runner_sha256": PINS[PKG / "run_next50_v2.py"],
    "source_ledger_sha256": PINS[PKG / "source_ledger.json"],
    "baseline_pins_verified": True,
    "next25_pins_verified": True,
    "binding_pins_verified": True,
    "closed_union": expected_union,
    "baseline_next25_disjoint": True,
    "hostiles_passed": len(hostiles),
    "selected_group_ids": selected,
    "sources_byte_identical_to_v1": 50,
    "total_source_bytes": total_bytes,
    "limits_each": {"native_wall_seconds": 240, "wrapper_wall_seconds": 250, "rss_cap_bytes": 8 * 1024**3},
    "strict_sequential_stop_first": True,
    "scope": {"held_approval_only": True, "launch_authorized": False, "solver_runs": 0, "mathematical_coverage": False, "rep1_representative_closed": False},
    "manifest_counts": manifest_counts,
}
approval = {
    "schema": "KRENN_X5_REP1_NEXT50_NORMALIZED_HELD_V2_APPROVAL_NOT_EXECUTOR_ACCEPTANCE_V1",
    "status": "PASS_HELD_ONLY_REQUIRES_FRESH_MANAGER_RESOURCE_NO_OVERLAP_CLEARANCE",
    "producer_manifest_sha256": PINS[PKG / "MANIFEST.sha256"],
    "normalized_dependency_sha256": PINS[PKG / "normalized_next25_dependency.json"],
    "selected_group_ids": selected,
    "launch_authorized": False,
    "solver_runs": 0,
}
(HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
(HERE / "HELD_APPROVAL.json").write_text(json.dumps(approval, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "result_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
