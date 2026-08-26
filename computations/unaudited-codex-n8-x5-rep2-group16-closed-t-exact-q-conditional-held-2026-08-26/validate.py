#!/usr/bin/env python3
"""Validate the rep2 exact-Q conditional held package without invoking Singular."""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from verify_modular_unit_dependency import verify_dependency

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/rep2_group016_67_Vt0_Vt1_Vt2_Q.sing"
RUNTIME = HERE / "rep2_group016_62_Vt0_Vt1_Vt2_Q_strong.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(BASE) == "43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc"
assert sha(RUNTIME) == "53fc0b26c52c5f55505c101c72ed0a7a73159092667edde4cdf1c573e4bd6795"
old = b'print("INPUT_GENERATORS="+string(size(I)));\nquit;\n'
strong = (
    b'print("INPUT_GENERATORS="+string(size(I)));\nideal G=slimgb(I);\n'
    b'print("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\n'
    b'print("UNIT_REMAINDER="+string(remainder));\n'
    b'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'
)
assert RUNTIME.read_bytes().replace(strong, old, 1) == BASE.read_bytes()
dependency = verify_dependency(HERE / "modular_unit_dependency.json")
assert dependency["status"] == "INDEPENDENTLY_SEALED_SAME_CHART_MODULAR_UNIT"
for script in ("build_source.py", "verify_modular_unit_dependency.py", "hostile_tests.py", "run_one_lane.py", "validate.py", "seal_manifest.py"):
    ast.parse((HERE / script).read_text())
plan = json.loads((HERE / "held_plan.json").read_text())
assert plan["status"].startswith("HELD_ZERO_RUN_MODULAR_UNIT_BOUND")
assert plan["dependency"]["binding_present"] is True and plan["dependency"]["binding_sha256"] == sha(HERE / "modular_unit_dependency.json")
assert plan["source"]["sha256"] == sha(RUNTIME) and plan["source"]["field"] == "Q"
assert plan["scope"] == {
    "attempts": 0, "group16_closed": False, "mathematical_coverage": False, "other_charts": 0,
    "prior_timeout_reused": False, "rep2_closed": False, "solver_runs": 0,
}
assert plan["authorization"] == {
    "automatic_relaunch_authorized": False, "exact_Q_authorized": False, "fresh_clearance_present": False,
    "independent_acceptance_present": False, "other_chart_authorized": False,
}
assert plan["execution"] == {
    "atomic_single_result": True, "direct_libproc_group_rss": True, "fresh_libproc_process_census": True,
    "maximum_lane_count": 1, "native_wall_seconds": 480, "rss_cap_bytes": 8589934592,
    "strict_stop_after_any_outcome": True, "wrapper_wall_seconds": 510,
}
for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((HERE / schema_name).read_text())
    assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"])
for absent in (
    "independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json", "result.json",
    "result.json.tmp", "RUN_EXCLUSIVE.lock", "stdout.log", "stderr.log", "watchdog.json",
):
    assert not (HERE / absent).exists(), absent
assert not list(HERE.glob("*.tmp"))
attempt = subprocess.run(
    [sys.executable, str(HERE / "hostile_tests.py")], cwd=HERE, capture_output=True, text=True, timeout=20,
    check=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
)
hostiles = json.loads((HERE / "results_hostiles.json").read_text())
assert hostiles["status"] == "PASS" and hostiles["hostile_count"] == 16 and hostiles["solver_runs"] == 0
result = {
    "schema": "KRENN_X5_REP2_GROUP16_CLOSED_T_EXACT_Q_CONDITIONAL_VALIDATION_V1",
    "status": "PASS_ZERO_RUN_MODULAR_UNIT_BOUND_FAIL_CLOSED",
    "source": {"base_Q_sha256": sha(BASE), "runtime_Q_sha256": sha(RUNTIME), "variables": 62, "generators": 6568},
    "dependency": {"binding_sha256": sha(HERE / "modular_unit_dependency.json"), "verified": True},
    "execution": {"maximum_lane_count": 1, "native_wall_seconds": 480, "wrapper_wall_seconds": 510, "rss_cap_bytes": 8589934592},
    "hostile_count": 16,
    "scope": {"attempts": 0, "solver_runs": 0, "mathematical_coverage": False, "group16_closed": False, "rep2_closed": False},
}
(HERE / "results_validation.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
