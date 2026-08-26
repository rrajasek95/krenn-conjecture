#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_referee.json"
plan_path = here / "ONE_CHART_MODULAR_HELD_PLAN.json"
result = json.loads(path.read_text())
plan = json.loads(plan_path.read_text())
assert result["status"] == "PASS_STRICT_SMALLER_EXACT_DESIGN_NO_RUN_NO_CLOSURE"
assert result["producer_manifest_sha256"] == "7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02"
assert result["producer_result_sha256"] == "7e96874cca1afaaa377aa3001d8e00b73ed4fe9322381ec269c4a46b9144bf0c"
assert result["support_guard_carrier_regenerated"] is True
assert result["cramer_polynomial_identities"] == 12
assert result["counts"]["old_variables"] == 100 and result["counts"]["new_variables"] == 91
assert result["counts"]["old_generators"] == 6586 and result["counts"]["new_generators"] == 6577
assert result["chart_census"] == {"raw": 972, "S3_orbits": 162, "orbit_size": 6, "y_orbits": 81, "z_orbits": 81}
assert result["materialized_Q_sources"] == 2 and result["ideal_runs"] == 0
assert result["rep4_closed"] is False
assert result["one_chart_held_plan_sha256"] == hashlib.sha256(plan_path.read_bytes()).hexdigest()
assert plan["launch_authorized"] is False and plan["solver_launches"] == 0
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))
