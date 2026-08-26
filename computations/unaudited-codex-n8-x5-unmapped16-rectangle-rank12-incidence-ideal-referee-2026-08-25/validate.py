#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_referee.json"
plan_path = here / "STAGED_PILOT_HELD_PLAN.json"
result = json.loads(path.read_text())
plan = json.loads(plan_path.read_text())
assert result["status"] == "PASS_EXACT_FINITE_DESIGN_NO_SOLVE_NO_CLOSURE"
assert result["producer_manifest_sha256"] == "743f3e526b21890509e32077ed5bf0c38b1240d25d475e71e2e78520445c85cf"
assert result["producer_result_sha256"] == "96b13ad342acd0fb02c37015b86303c9d6d7d880abe0e2a4e21f5e9e1aea5a28"
assert result["counts"]["rank1"] == {"variables": 76, "generators": 6571, "canonical_inputs": 5}
assert result["counts"]["rank2"] == {"variables": 80, "generators": 6574, "canonical_inputs": 5}
assert result["orbit_census"]["rank1_sizes"] == [3, 6, 6, 6, 6]
assert result["orbit_census"]["rank2_sizes"] == [6, 6, 6, 6, 3]
assert result["orbit_census"]["canonical_Q_inputs"] == 10
assert result["A12_lifts_share_ideal"] is True
assert result["solver_launches"] == result["records_closed"] == 0
assert result["staged_pilot_held_plan_sha256"] == hashlib.sha256(plan_path.read_bytes()).hexdigest()
assert plan["launch_authorized"] is False and plan["automatic_relaunch"] is False
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))
