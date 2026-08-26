#!/usr/bin/env python3
"""Static proof that the prepared gate is held and command diff is frozen."""
import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
plan = json.loads((HERE / "PLAN.json").read_text())
assert plan["status"] == "PREPARED_HELD_FOR_POINCARE_FINAL_REPLAY_CLEAR"
assert not (HERE / "LAUNCH_PINS.json").exists()
texts = {}
for name in ("freeze_poincare_pins.py", "run_gate.py", "validate.py"):
    texts[name] = (HERE / name).read_text()
    ast.parse(texts[name], filename=name)
assert 'EXPECTED_MANIFEST_SHA256 = "7dea99f68ab4d5e04be287b6e382165b679ca29e8271001400152c6c01c33d20"' in texts["freeze_poincare_pins.py"]
assert 'run("cap1500_control", 1500000' in texts["run_gate.py"]
assert 'run("cap1750_candidate", 1750000' in texts["run_gate.py"]
assert 'left.index("1500000"), "1500000", "1750000"' in texts["validate.py"]
value = {"schema": "KRENN_AFFINE251_D12_ROUND1343_CAP_PREFLIGHT_V1",
         "status": "PASS_POSTSEAL_PRELAUNCH", "launch_pins_absent": True,
         "authoritative_manifest_pin_present": True, "large_reads_performed": False,
         "solves_performed": False, "scripts_parse": True,
         "normalized_cap_only_validator_present": True}
(HERE / "hostile_preflight_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
