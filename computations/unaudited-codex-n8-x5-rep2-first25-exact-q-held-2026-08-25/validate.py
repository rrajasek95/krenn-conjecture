#!/usr/bin/env python3
"""Validate the strict zero-run rep2 first-25 held package."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


ledger = json.loads((HERE / "source_ledger.json").read_text())
census = json.loads((HERE / "canonical_census.json").read_text())
plan = json.loads((HERE / "held_schedule.json").read_text())
hostiles = json.loads((HERE / "results_hostile_tests.json").read_text())
assert sha256(HERE / "source_ledger.json") == "20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e"
assert sha256(HERE / "canonical_census.json") == "5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a"
assert sha256(HERE / "run_first25.py") == "0727e5e5961f90cd14d3d79f836634bf7df9fff1b8d44bd463678db1f8f72ff2"
assert census["closed_group_identification"]["group_id"] == 0
assert census["closed_group_identification"]["method"] == "unique exact-Q source SHA match to independently sealed all-equal-y chart"
assert census["closed_group_identification"]["source_sha256"] == "5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf"
groups = census["groups"]
assert [entry["group_id"] for entry in groups] == list(range(162))
assert all(entry["raw_member_count"] == len(entry["raw_members"]) == 6 for entry in groups)
raw = [tuple(member) for entry in groups for member in entry["raw_members"]]
assert len(raw) == len(set(raw)) == 972
assert sum(entry["family"] == "y" for entry in groups) == 81
assert sum(entry["family"] == "z" for entry in groups) == 81
assert ledger["selection"]["excluded_proven_group_ids"] == [0]
assert ledger["selection"]["selected_group_ids"] == list(range(1, 26))
assert [lane["group_id"] for lane in ledger["lanes"]] == list(range(1, 26))
for lane in ledger["lanes"]:
    source = HERE / lane["source_path"]
    assert source.is_file() and sha256(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    text = source.read_text()
    assert text.count("ring r=0,") == text.count("ideal G=slimgb(I);") == text.count("poly remainder=reduce(1,G);") == text.count("quit;") == 1
    assert "INPUT_GENERATORS=" in text and "STATUS=UNIT_IDEAL" in text
runner = (HERE / "run_first25.py").read_text()
compile(runner, str(HERE / "run_first25.py"), "exec")
for token in ("proc_listpgrppids", "group_rss", "rusage failure for live member", "SELECTED = tuple(range(1, 26))", "NATIVE_WALL = 240", "WRAPPER_WALL = 250", "RSS_CAP = 8 * 1024**3", "if not unit:", "BATCH_ATTEMPT.json", "atomic(result_path, record)"):
    assert token in runner, token
assert plan["status"] == "HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT_AND_CLEARANCE"
assert plan["execution"]["order"] == list(range(1, 26))
assert plan["execution"]["parallel"] is plan["execution"]["skip"] is plan["execution"]["reorder"] is plan["execution"]["relaunch"] is False
assert plan["scope"] == {"representative": "rep2 only", "source_regeneration_only": True, "solver_launches": 0, "result_files": 0, "attempt_markers": 0, "clearances": 0, "groups_newly_closed": 0, "rep2_closed": False, "mathematical_coverage_added": False, "cross_representative_transport": False}
assert hostiles["status"] == "PASS_10_HOSTILES_ZERO_RUN" and len(hostiles["tests"]) == 10 and all(hostiles["tests"].values())
for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((HERE / schema_name).read_text())
    assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"])
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HERE / absent).exists(), absent
assert not list(HERE.glob("*.tmp"))
for relative, expected in ledger["pins"].items():
    path = ROOT / relative
    assert path.is_file() and sha256(path) == expected
manifest = HERE / "MANIFEST.sha256"
checked = 0
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, relative = line.split("  ", 1)
        path = (HERE / relative).resolve()
        assert path.is_file() and sha256(path) == digest, relative
        checked += 1
print(json.dumps({"status": "PASS_HELD_REP2_FIRST25_ZERO_RUN", "closed_group": 0, "selected": list(range(1, 26)), "sources": 25, "raw_census": 972, "canonical_groups": 162, "manifest_lines_checked": checked, "solver_runs": 0}, sort_keys=True))
