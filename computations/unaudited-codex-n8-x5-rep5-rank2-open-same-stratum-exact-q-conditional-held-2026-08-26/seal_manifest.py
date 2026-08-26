#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = [
    "EXTERNAL_PINS.sha256", "REPORT.md", "future_dependency_contract.json", "held_plan.json",
    "historical_superseded_pin.json", "hostile_tests.py", "independent_referee_acceptance.schema.json",
    "launch_clearance.schema.json", "rep5_rank2_k2_t1_Q.sing", "results_hostiles.json",
    "results_validation.json", "run_one_lane.py", "seal_manifest.py", "validate.py",
    "verify_future_dependency.py",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert not any(HERE.glob("*.tmp"))
for forbidden in ("future_modular_unit_dependency.json", "independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json", "result.json", "RUN_EXCLUSIVE.lock"):
    assert not (HERE / forbidden).exists()
assert all((HERE / item).is_file() for item in FILES)
(HERE / "MANIFEST.sha256").write_text("".join(f"{sha256(HERE / item)}  {item}\n" for item in FILES))
for line in (HERE / "MANIFEST.sha256").read_text().splitlines():
    expected, relative = line.split("  ", 1); assert sha256(HERE / relative) == expected
print(sha256(HERE / "MANIFEST.sha256"))
