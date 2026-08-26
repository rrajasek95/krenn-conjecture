#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
b = json.loads((HERE / "results_binding.json").read_text())
r = json.loads((HERE / "results_referee.json").read_text())
d = json.loads((HERE / "normalized_dependencies.json").read_text())
a = json.loads((HERE / "independent_referee_acceptance.json").read_text())
assert b["status"] == "PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE"
assert r["status"] == "PASS_INDEPENDENT_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE"
assert d["closed_union"] == list(range(76))
assert a["selected_group_ids"] == list(range(76, 126)) and a["required_closed_union"] == list(range(76))
assert a["normalized_dependencies_sha256"] == sha(HERE / "normalized_dependencies.json")
assert b["scope"]["solver_runs"] == 0 and b["scope"]["launch_clearance_materialized"] is False
checked = 0
if (HERE / "FINAL_MANIFEST.sha256").exists():
    for line in (HERE / "FINAL_MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (HERE / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest
        checked += 1
print(json.dumps({"status": "PASS_BINDING_VALIDATED_ZERO_RUN", "manifest_lines_checked": checked}, sort_keys=True))
