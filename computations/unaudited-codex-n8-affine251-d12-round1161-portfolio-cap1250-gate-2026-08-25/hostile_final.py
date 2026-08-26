#!/usr/bin/env python3
"""Hostile mutations of the load-bearing command and state-equality contract."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def argument(command, flag):
    if command.count(flag) != 1:
        raise AssertionError("flag cardinality")
    return command[command.index(flag) + 1]


def normalized_differences(control, candidate):
    assert len(control) == len(candidate)
    left = [item.replace("/selected_control/", "/RUN/") for item in control]
    right = [item.replace("/cap1250_candidate/", "/RUN/") for item in candidate]
    return [(index, a, b) for index, (a, b) in enumerate(zip(left, right)) if a != b]


control = json.loads((HERE / "selected_control/watchdog.json").read_text())["command"]
candidate = json.loads((HERE / "cap1250_candidate/watchdog.json").read_text())["command"]
expected = [(control.index("1000000"), "1000000", "1250000")]
assert normalized_differences(control, candidate) == expected

hostiles = {}
for name, mutate in {
    "wrong_workers": lambda command: command.__setitem__(command.index("--workers") + 1, "8"),
    "wrong_round_cap": lambda command: command.__setitem__(command.index("--round-cap") + 1, "1162"),
    "wrong_strategy": lambda command: command.__setitem__(command.index("--strategy") + 1, "repair"),
    "wrong_pivot": lambda command: command.__setitem__(command.index("--pivot") + 1, "first"),
    "wrong_candidate_cap": lambda command: command.__setitem__(command.index("--column-cap") + 1, "1250001"),
}.items():
    changed = list(candidate)
    mutate(changed)
    hostiles[name] = normalized_differences(control, changed) != expected
assert all(hostiles.values())

portfolio_result = json.loads((HERE / "portfolio/result.json").read_text())
control_result = json.loads((HERE / "selected_control/result.json").read_text())
candidate_result = json.loads((HERE / "cap1250_candidate/result.json").read_text())
fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
          "selected_strategy", "selected_pivot"]
records = [[result["rounds"][0][field] for field in fields]
           for result in (portfolio_result, control_result, candidate_result)]
assert records[0] == records[1] == records[2]
mutated = list(records[2])
mutated[1] += 1
assert mutated != records[1]
hostiles["wrong_output_columns"] = True

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1161_FINAL_HOSTILES_V1",
    "status": "PASS_ALL_HOSTILE_MUTATIONS_REJECTED",
    "hostiles": hostiles,
    "cap_flag_cardinality": argument(candidate, "--column-cap") == "1250000",
}
(HERE / "hostile_final_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
