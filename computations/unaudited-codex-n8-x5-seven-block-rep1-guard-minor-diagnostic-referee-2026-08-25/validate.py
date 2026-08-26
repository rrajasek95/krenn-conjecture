#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "results_referee.json").read_text())
plan = json.loads((HERE / "EXACT_Q_HELD_PLAN.json").read_text())
assert result["status"] == "PASS_UNIT_IDEAL_MODULAR_DIAGNOSTIC_ONLY"
assert result["input"] == {"field": "F_32003", "generators": 6577, "sha256": "edd174ccbc75a563fd67e0515b6dde2c54e5469b742629953080290fe7d1fb49", "variables": 91}
assert result["terminal"]["basis_size"] == 1 and result["terminal"]["remainder_of_one"] == 0
assert result["terminal"]["wall_seconds"] == 13.57906291692052
assert result["terminal"]["peak_rss_bytes"] == 733069312
assert all(result["exclusions"].values())
assert result["scope"] == {"D12_reads": False, "characteristic_zero_coverage": False, "ideal_runs_by_referee": 0, "modular_chart_eliminated": True, "rep1_closed": False}
assert plan["status"] == "APPROVE_HELD_NOT_RUN"
assert plan["limits"]["maximum_exact_Q_lane_count"] == 1
assert plan["limits"]["native_wall_seconds"] == 240 and plan["limits"]["wrapper_wall_seconds"] == 250
assert plan["limits"]["rss_cap_bytes"] == 8 * 1024**3
assert "other 161" in plan["acceptance"]["rep1_promotion"]
print(json.dumps({"status": "PASS", "Q_plan": "HELD_NOT_RUN"}, sort_keys=True))
