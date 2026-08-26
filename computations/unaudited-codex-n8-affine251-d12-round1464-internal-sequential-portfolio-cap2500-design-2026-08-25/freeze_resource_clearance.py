#!/usr/bin/env python3
"""Small pre-clone r1464 disk/runtime gate; absent final pins fail before I/O."""
import json
import os
from pathlib import Path
import shutil

if not __debug__:
    raise RuntimeError("fail closed: resource gate requires assertions enabled")

HERE = Path(__file__).resolve().parent
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
pins_path = HERE / "FUTURE_INPUT_PINS.json"
assert pins_path.exists(), "round1463 pins absent; no resource clearance"
pins = json.loads(pins_path.read_text())
assert pins["status"] == "PASS_FROZEN_INDEPENDENT_ROUND1463_FINAL_REPLAY_CLEAR"
columns = pins["checkpoint_header"]["columns"]
assert columns == pins["vectors_header"]["columns"]
projected_seconds = 475.636649 * columns / 1582672
free_bytes = shutil.disk_usage(HERE).free
assert projected_seconds <= 500, \
    f"portfolio projection {projected_seconds:.3f}s lacks margin below native 520s"
assert free_bytes >= SCHEDULE["resource_interlocks"]["minimum_free_bytes_before_any_clone"], \
    "free-space floor not met"
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1464_RESOURCE_CLEARANCE_V1",
    "status": "PASS_FROZEN_RESOURCE_CLEARANCE",
    "round1463_columns": columns,
    "projection_model": "475.636649 * round1463_columns / 1582672",
    "projected_portfolio_seconds": projected_seconds,
    "required_projection_max_seconds": 500,
    "native_wall_seconds": 520,
    "wrapper_wall_seconds": 540,
    "free_bytes": free_bytes,
    "minimum_free_bytes": SCHEDULE["resource_interlocks"]["minimum_free_bytes_before_any_clone"],
    "process_clearance_still_required_at_launch": True,
}
temporary = HERE / "RESOURCE_CLEARANCE.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "RESOURCE_CLEARANCE.json")
print(json.dumps(value, sort_keys=True))
