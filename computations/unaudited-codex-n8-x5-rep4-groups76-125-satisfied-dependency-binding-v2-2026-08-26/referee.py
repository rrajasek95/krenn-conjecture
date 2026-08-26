#!/usr/bin/env python3
"""Independent replay of the rep4 groups76..125 satisfied dependency binding."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "computations"
HELD = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26"
HELD_REF = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-referee-2026-08-26"
FIRST = C / "unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26"
FIRST_REF = C / "unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26"
SECOND = C / "unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26"
SECOND_REF = C / "unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(manifest: Path) -> int:
    count = 0
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        path = (manifest.parent / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest)
        count += 1
    return count

counts = {
    "held": replay(HELD / "MANIFEST.sha256"),
    "held_referee": replay(HELD_REF / "FINAL_MANIFEST.sha256"),
    "first25": replay(FIRST / "TERMINAL_MANIFEST.sha256"),
    "first25_referee": replay(FIRST_REF / "FINAL_MANIFEST.sha256"),
    "groups26_75": replay(SECOND / "TERMINAL_MANIFEST.sha256"),
    "groups26_75_referee": replay(SECOND_REF / "FINAL_MANIFEST.sha256"),
}

binding = json.loads((HERE / "results_binding.json").read_text())
deps = json.loads((HERE / "normalized_dependencies.json").read_text())
acceptance = json.loads((HERE / "independent_referee_acceptance.json").read_text())
first_batch = json.loads((FIRST / "batch_result.json").read_text())
first_ref = json.loads((FIRST_REF / "results_referee.json").read_text())
second_batch = json.loads((SECOND / "batch_result.json").read_text())
second_ref = json.loads((SECOND_REF / "results_referee.json").read_text())

assert binding["status"] == "PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE"
assert deps["status"] == "PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75"
assert deps["closed_union"] == list(range(76)) and deps["duplicates"] == deps["missing"] == deps["extra"] == []
assert [d["groups_closed"] for d in deps["dependencies"]] == [list(range(1, 26)), list(range(26, 76))]
assert first_batch["strict_order"] == list(range(1, 26))
assert [x["group_id"] for x in first_batch["completed"]] == list(range(1, 26))
assert first_ref["closed_union"] == list(range(26)) and first_ref["sealed_group0"] is True
assert second_batch["strict_order"] == list(range(26, 76))
assert [x["group_id"] for x in second_batch["completed"]] == list(range(26, 76))
assert second_ref["dependency_closed_union_before_batch"] == list(range(26))
assert second_ref["groups_closed"] == list(range(26, 76))
assert second_ref["closed_union_after_batch"] == list(range(76))

ledger = json.loads((HELD / "source_ledger.json").read_text())
assert [x["group_id"] for x in ledger["lanes"]] == list(range(76, 126))
assert sum(x["source_bytes"] for x in ledger["lanes"]) == 90617222
for lane in ledger["lanes"]:
    source = HELD / lane["source_path"]
    assert source.stat().st_size == lane["source_bytes"] and sha(source) == lane["source_sha256"]

preservation = {
    "source_count": 50, "source_bytes": 90617222,
    "all_source_hashes_replayed": True,
    "source_ledger_sha256_unchanged": "b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb",
    "runner_sha256_unchanged": "3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd",
    "sources_rewritten": 0, "runner_rewritten": False,
}
assert binding["preservation"] == preservation
schema = json.loads((HELD / "independent_referee_acceptance.schema.json").read_text())
assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"]) == set(acceptance)
for key, rule in schema["properties"].items():
    if "const" in rule:
        assert acceptance[key] == rule["const"]
assert acceptance["normalized_dependencies_sha256"] == sha(HERE / "normalized_dependencies.json")
assert acceptance["required_closed_union"] == list(range(76))
assert acceptance["selected_group_ids"] == list(range(76, 126))
assert acceptance["exact_Q_authorized"] and not acceptance["parallel_authorized"] and not acceptance["skip_reorder_relaunch_authorized"]

for absent in ("normalized_dependencies.json", "independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HELD / absent).exists(), absent
assert not list(HERE.glob("*.tmp"))

out = {
    "schema": "KRENN_X5_REP4_GROUPS76_125_SATISFIED_DEPENDENCY_BINDING_REFEREE_V2",
    "status": "PASS_INDEPENDENT_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE",
    "binding_sha256": sha(HERE / "results_binding.json"),
    "normalized_dependencies_sha256": sha(HERE / "normalized_dependencies.json"),
    "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"),
    "closed_union": list(range(76)), "selected_group_ids": list(range(76, 126)),
    "preservation": preservation, "lineage": binding["lineage"], "manifest_counts": counts,
    "interface_note": "V2 binds both actual sealed referee statuses; stale status literals in the null dependency template are not used.",
    "scope": {
        "held_launch_ready_metadata": True, "install_into_held_performed": False,
        "launch_clearance_materialized": False, "solver_runs": 0,
        "new_arithmetic": False, "mathematical_coverage_added": False,
    },
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "union": 76, "sources": 50, "runs": 0, "clearance": False}, sort_keys=True))
