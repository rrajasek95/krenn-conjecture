#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_referee.json"
plan_path = here / "SUPERSEDING_STAGED_HELD_PLAN.json"
result = json.loads(path.read_text())
plan = json.loads(plan_path.read_text())
assert result["status"] == "PASS_SOLVER_EPILOGUE_EXACT_HELD_NOT_RUN"
assert result["old_plan_disposition"] == "REJECT_SUPERSEDED_UNLAUNCHED"
assert result["Q_diagnostic_source_sha256"] == "1d9875cab81417094d51193862f40097b1c03e4816aedd8ceaf07a917eeb248b"
assert result["p32003_diagnostic_source_sha256"] == "b70098251cfe8aceb845c1a3c2af92a5ae944e9bfcb1c611d21adada8edd44cb"
assert result["p32003_execution_source_sha256"] == "7c34d1efbf74220f01a6ea150ede232b9f51f9168f15dd997ed2b204e8aacf9c"
assert result["Q_execution_source_expected_sha256"] == "c062396aa8835e9c31d0e845a997d89f3b1d151f6494d36d5ba990cdadf9c44f"
assert (result["variables"], result["generators"]) == (76, 6571)
assert result["unchanged_ring_ideal_prefix"] is True and result["sole_solver_epilogue"] is True
assert all(result["hostile_tests"].values()) and result["solver_launches"] == 0
assert result["superseding_held_plan_sha256"] == hashlib.sha256(plan_path.read_bytes()).hexdigest()
assert plan["launch_authorized"] is False and plan["solver_launches"] == 0
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))
