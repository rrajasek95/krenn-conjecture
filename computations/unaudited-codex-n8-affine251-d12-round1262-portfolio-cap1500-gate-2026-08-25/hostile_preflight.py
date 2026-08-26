#!/usr/bin/env python3
"""Static/lightweight proof that the pre-seal launch contract fails closed."""
import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
plan = json.loads((HERE / "PLAN.json").read_text())
assert plan["status"] == "PREPARED_HELD_FOR_POINCARE_FINAL_REPLAY_CLEAR"
assert not (HERE / "LAUNCH_PINS.json").exists()
scripts = {}
for name in ("freeze_poincare_pins.py", "run_after_poincare.py", "validate_outputs.py"):
    text = (HERE / name).read_text()
    ast.parse(text, filename=name)
    scripts[name] = text
assert 'EXPECTED_MANIFEST_SHA256 = "WAIT_FOR_POINCARE_FINAL_REPLAY_CLEAR"' in scripts["freeze_poincare_pins.py"]
assert 'EXPECTED_MANIFEST_SHA256 != "WAIT_FOR_POINCARE_FINAL_REPLAY_CLEAR"' in scripts["freeze_poincare_pins.py"]
assert 'native("portfolio", "auto", "best", 1250000)' in scripts["run_after_poincare.py"]
assert 'native("cap1500_candidate", "rare", "cold", 1500000)' in scripts["run_after_poincare.py"]
assert 'normalized_control.index("1250000"), "1250000", "1500000"' in scripts["validate_outputs.py"]
assert 'assert sha256(vectors) == pins["vectors_sha256"]' in scripts["run_after_poincare.py"]
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_PREFLIGHT_HOSTILES_V1",
    "status": "PASS_PRESEAL_FAIL_CLOSED",
    "manifest_hash_placeholder_blocks_freeze": True,
    "launch_pins_absent": True,
    "large_reads_performed": False,
    "solves_performed": False,
    "control_cap": 1250000,
    "candidate_cap": 1500000,
    "normalized_one_diff_validator_present": True,
    "scripts_parse": True
}
(HERE / "hostile_preflight_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
