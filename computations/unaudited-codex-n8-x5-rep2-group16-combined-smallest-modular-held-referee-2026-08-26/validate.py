#!/usr/bin/env python3
"""Read-only validation and optional manifest replay."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
result = json.loads((HERE / "results_referee.json").read_text())
acceptance = json.loads((HERE / "independent_referee_acceptance.json").read_text())
assert result["status"] == "PASS_HELD_APPROVAL_ONLY_ZERO_RUN"
assert result["source"]["Q_sha256"] == "2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339"
assert result["source"]["p32003_sha256"] == "66bdb9277c9bff605e0d8a808ca65beb5967afaaf8ae494193286a60338355c6"
assert result["source"]["variables"] == 67 and result["source"]["generators"] == 6574
assert result["scope"]["full_intersections"] == 57 and result["scope"]["single_chart_closes_group16"] is False
assert result["scope"]["solver_runs"] == result["scope"]["attempts"] == 0
assert result["runner"]["maximum_lane_count"] == 1
assert result["refusal"]["acceptance_present_in_held"] is result["refusal"]["clearance_present_in_held"] is False
assert result["refusal"]["exact_Q_authorized"] is result["refusal"]["other_chart_authorized"] is result["refusal"]["automatic_relaunch_authorized"] is False
assert result["hostiles"] == {"all_pass": True, "count": 12}
assert result["acceptance_sha256"] == sha(HERE / "independent_referee_acceptance.json")
assert acceptance["status"] == "PASS_APPROVE_HELD_ONE_COMBINED_P32003_DIAGNOSTIC_ONLY"
checked = 0
manifest = HERE / "FINAL_MANIFEST.sha256"
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, relative = line.split(None, 1)
        path = (HERE / relative.strip()).resolve()
        assert path.is_file() and sha(path) == digest
        checked += 1
print(json.dumps({"status": "PASS_REFEREE_VALIDATED_ZERO_RUN", "manifest_lines_checked": checked}, sort_keys=True))
