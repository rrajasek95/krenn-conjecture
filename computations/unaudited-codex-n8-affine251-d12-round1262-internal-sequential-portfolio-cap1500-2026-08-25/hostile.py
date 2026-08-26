#!/usr/bin/env python3
"""Small hostile mutations of the accepted command/state contract."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalized(command, label):
    return [item.replace(f"/{label}/", "/RUN/") for item in command]


def differences(left, right):
    return [(index, a, b) for index, (a, b) in enumerate(zip(left, right)) if a != b]


control = json.loads((HERE / "selected_control/watchdog.json").read_text())["command"]
candidate = json.loads((HERE / "cap1500_candidate/watchdog.json").read_text())["command"]
left = normalized(control, "selected_control")
right = normalized(candidate, "cap1500_candidate")
expected = [(left.index("1250000"), "1250000", "1500000")]
assert differences(left, right) == expected
hostiles = {}
for name, flag, value in [
    ("wrong_workers", "--workers", "8"),
    ("wrong_round", "--round-cap", "1263"),
    ("wrong_pivot", "--pivot", "first"),
    ("wrong_strategy", "--strategy", "repair"),
    ("wrong_parallel", "--portfolio-parallel", "yes"),
    ("wrong_cap", "--column-cap", "1500001"),
]:
    changed = list(right)
    changed[changed.index(flag) + 1] = value
    hostiles[name] = differences(left, changed) != expected
assert all(hostiles.values())
results = [json.loads((HERE / label / "result.json").read_text()) for label in
           ("portfolio", "selected_control", "cap1500_candidate")]
fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
          "selected_strategy", "selected_pivot"]
records = [[result["rounds"][0][field] for field in fields] for result in results]
assert records[0] == records[1] == records[2]
mutated = list(records[2]); mutated[1] += 1
hostiles["wrong_output_columns"] = mutated != records[1]
value = {"schema": "KRENN_AFFINE251_D12_ROUND1262_INTERNAL_PORTFOLIO_HOSTILES_V1",
         "status": "PASS_ALL_HOSTILES_REJECTED", "hostiles": hostiles}
(HERE / "hostile_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
