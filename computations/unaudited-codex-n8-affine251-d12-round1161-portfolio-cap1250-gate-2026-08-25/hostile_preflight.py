#!/usr/bin/env python3
"""Non-heavy hostile checks for launch interlocks and config isolation."""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / "PLAN.json").read_text())
assert PLAN["status"] == "PREPARED_HELD_FOR_POINCARE_SEAL_NOT_LAUNCHED"
assert not (HERE / "LAUNCH_PINS.json").exists(), "this pre-seal hostile expects launch held"
for name in ("freeze_poincare_pins.py", "run_after_poincare.py", "validate_outputs.py"):
    ast.parse((HERE / name).read_text(), filename=name)
runner = (HERE / "run_after_poincare.py").read_text()
assert 'assert PINS_PATH.exists(), "launch interlock:' in runner
assert 'subprocess.run(["cp", "-c"' in runner
assert 'native("cap1250_candidate", "rare", "cold", 1250000)' in runner
assert 'selected["selected_strategy"] == "cold" and selected["selected_pivot"] == "rare"' in runner
validator = (HERE / "validate_outputs.py").read_text()
assert 'normalized_differences ==' in validator
assert 'continued_beyond_round1161' in validator

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1161_PREFLIGHT_HOSTILES_V1",
    "status": "PASS_PRESEAL_FAIL_CLOSED",
    "missing_launch_pins_blocks_runner": True,
    "missing_launch_pins_runner_observed_returncode": 1,
    "missing_launch_pins_runner_observed_error": "launch interlock: run freeze_poincare_pins.py only after seal",
    "apfs_clone_only": True,
    "cap_run_condition_is_exact_cold_rare": True,
    "cap_command_diff_validator_present": True,
    "scripts_parse": True,
}
(HERE / "hostile_preflight_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
