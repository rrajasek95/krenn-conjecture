#!/usr/bin/env python3
"""Fail-closed static validator for the held rep5 guard-pivot k0 package."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25"
Q_SOURCE = DESIGN / "rep5_p00_guardpivot_k0_Q.sing"
SOURCE = HERE / "rep5_p00_guardpivot_k0_p32003.sing"
RUNNER = HERE / "run_one_lane.py"
SOURCE_SHA = "dc04c72252144d1a8ff798f49aa1130b1742fff342f21eaf02146b889e3370c1"
RUNNER_SHA = "fdaaea4fead4ec7d47f0a513fa6b8c74a04e4821d1abb4751d32806f9cabc965"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def simple_schema_validate(schema: dict, value: dict) -> None:
    assert isinstance(value, dict)
    properties = schema["properties"]
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(properties)
    assert set(value) == set(properties)
    for key, rule in properties.items():
        if "const" in rule:
            assert value[key] == rule["const"]
        elif rule.get("pattern") == "^[0-9a-f]{64}$":
            assert isinstance(value[key], str) and len(value[key]) == 64 and all(c in "0123456789abcdef" for c in value[key])
        elif rule.get("pattern") == "^[0-9a-f]{32}$":
            assert isinstance(value[key], str) and len(value[key]) == 32 and all(c in "0123456789abcdef" for c in value[key])


assert sha256(Q_SOURCE) == "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1"
q_bytes = Q_SOURCE.read_bytes()
assert q_bytes.count(b"ring r=0,") == 1
assert SOURCE.read_bytes() == q_bytes.replace(b"ring r=0,", b"ring r=32003,")
assert sha256(SOURCE) == SOURCE_SHA
assert SOURCE.read_bytes().count(b"ring r=32003,") == 1
assert SOURCE.read_bytes().count(b"ideal G=slimgb(I);") == 1
assert SOURCE.read_bytes().count(b"poly remainder=reduce(1,G);") == 1
assert sha256(RUNNER) == RUNNER_SHA
runner = RUNNER.read_text()
compile(runner, str(RUNNER), "exec")
for token in (
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids",
    "process_group_rss_bytes", "rusage observation failure for live group member",
    '[str(GTIMEOUT), "--signal=TERM"', 'f"{WRAPPER_WALL}s"',
    "NATIVE_WALL = 240", "WRAPPER_WALL = 250", "RSS_CAP = 8 * 1024**3",
    "MAX_CLEARANCE_LIFETIME_SECONDS = 600", "fresh_process_census()",
    'exclusive_json(HERE / "ATTEMPT.json"', 'atomic_json(HERE / "result.json"',
    'clearance["no_overlap_confirmed"] is True', 'clearance["other_k_authorized"] is False',
):
    assert token in runner, token
assert runner.index('exclusive_json(HERE / "ATTEMPT.json"') < runner.index("subprocess.Popen(")
assert "second_lane" not in runner and "ALL_EQUAL_Y" not in runner

held = json.loads((HERE / "held_pilot.json").read_text())
assert held["status"] == "HELD_ZERO_RUN_PENDING_INDEPENDENT_ACCEPTANCE_AND_FRESH_CLEARANCE"
assert held["lane"] == {"representative": "rep5", "chart": "p00/guard-pivot/k0", "field": 32003, "variables": 88, "generators": 6574, "maximum_lane_count": 1}
assert held["source"]["sha256"] == SOURCE_SHA and held["runner"]["sha256"] == RUNNER_SHA
assert held["limits"] == {"native_wall_seconds": 240, "wrapper_wall_seconds": 250, "rss_cap_bytes": 8589934592, "maximum_clearance_lifetime_seconds": 600}
assert held["scope"] == {"launched": False, "solver_runs": 0, "attempt_marker_created": False, "modular_lanes_authorized": 0, "exact_Q_authorized": False, "other_k_authorized": False, "automatic_relaunch_authorized": False, "mathematical_coverage": False}
assert sha256(REFEREE / "FINAL_MANIFEST.sha256") == held["pins"]["design_referee_manifest_sha256"]
assert sha256(REFEREE / "HELD_DIAGNOSTIC_PLAN.json") == held["pins"]["held_plan_sha256"]

acceptance_schema = json.loads((HERE / "independent_referee_acceptance.schema.json").read_text())
clearance_schema = json.loads((HERE / "launch_clearance.schema.json").read_text())
fake_acceptance = {key: rule.get("const", "0" * (32 if rule.get("pattern") == "^[0-9a-f]{32}$" else 64)) for key, rule in acceptance_schema["properties"].items()}
fake_clearance = {key: rule.get("const", "0" * (32 if rule.get("pattern") == "^[0-9a-f]{32}$" else 64)) for key, rule in clearance_schema["properties"].items()}
fake_clearance["issued_at_utc"] = "2026-08-25T00:00:00+00:00"
fake_clearance["expires_at_utc"] = "2026-08-25T00:01:00+00:00"
simple_schema_validate(acceptance_schema, fake_acceptance)
simple_schema_validate(clearance_schema, fake_clearance)
hostiles = {}
for name, schema, good, key, bad in (
    ("acceptance_extra", acceptance_schema, fake_acceptance, "extra", 1),
    ("acceptance_Q", acceptance_schema, fake_acceptance, "exact_Q_authorized", True),
    ("acceptance_other_k", acceptance_schema, fake_acceptance, "other_k_authorized", True),
    ("clearance_wall", clearance_schema, fake_clearance, "native_wall_seconds", 241),
    ("clearance_overlap", clearance_schema, fake_clearance, "no_overlap_confirmed", False),
    ("clearance_relaunch", clearance_schema, fake_clearance, "automatic_relaunch_authorized", True),
):
    candidate = copy.deepcopy(good)
    candidate[key] = bad
    try:
        simple_schema_validate(schema, candidate)
    except AssertionError:
        hostiles[name] = True
    else:
        hostiles[name] = False
assert all(hostiles.values())
assert json.loads((HERE / "refusal_contract.json").read_text())["status"] == "ARMED_HELD_ZERO_RUN_SINGLE_USE"
for stale in (
    "ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json",
    "independent_referee_acceptance.json", "launch_clearance.json",
):
    assert not (HERE / stale).exists(), stale
assert not any(HERE.glob("*.tmp"))
print(json.dumps({"status": "PASS_HELD_ZERO_RUN", "source_sha256": SOURCE_SHA, "runner_sha256": RUNNER_SHA, "hostiles": len(hostiles), "solver_runs": 0}, sort_keys=True))
