#!/usr/bin/env python3
"""Validate the zero-run conditional held package without invoking Singular."""
from __future__ import annotations

import hashlib
import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


source = HERE / "rep5_rank2_k2_t1_Q.sing"
original = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25/rep5_p00_guardpivot_k2_rank2_t1_Q.sing"
assert source.read_bytes() == original.read_bytes()
assert sha256(source) == "1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e"
text = source.read_text()
assert text.startswith("// DESIGN INPUT ONLY: zero Singular or ideal runs authorized.\noption(noredefine);\nring r=0,")
for literal in ("print(\"INPUT_VARIABLES=\"+string(nvars(r)))", "print(\"INPUT_GENERATORS=\"+string(size(I)))", "ideal G=slimgb(I)", "poly remainder=reduce(1,G)", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED"):
    assert literal in text
assert text.rstrip().endswith("quit;")
for script in ("run_one_lane.py", "verify_future_dependency.py", "hostile_tests.py", "validate.py", "seal_manifest.py"):
    py_compile.compile(str(HERE / script), doraise=True)
for raw in (HERE / "EXTERNAL_PINS.sha256").read_text().splitlines():
    match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw); assert match
    expected, relative = match.groups(); target = (HERE / relative).resolve(strict=True)
    assert ROOT in target.parents and sha256(target) == expected
plan = json.loads((HERE / "held_plan.json").read_text())
contract = json.loads((HERE / "future_dependency_contract.json").read_text())
assert plan["status"].startswith("HELD_ZERO_RUN") and plan["scope"] == {"attempts": 0, "mathematical_coverage": False, "other_strata": 0, "prior_consumed_k0_reused": False, "solver_runs": 0}
assert all(value is None for value in contract["future_hashes"].values())
assert all(value is None for value in contract["future_paths"].values())
for absent in ("future_modular_unit_dependency.json", "independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json", "result.json", "RUN_EXCLUSIVE.lock"):
    assert not (HERE / absent).exists(), absent
hostile = subprocess.run([sys.executable, str(HERE / "hostile_tests.py")], cwd=HERE, check=True, capture_output=True, text=True)
hostile_result = json.loads((HERE / "results_hostiles.json").read_text())
assert hostile_result["status"] == "PASS" and hostile_result["solver_runs"] == 0
result = {
    "dependency": {"future_binding_absent": True, "future_hashes_null": True, "future_paths_null": True, "independent_modular_unit_required": True},
    "execution": {"maximum_lane_count": 1, "native_wall_seconds": 480, "wrapper_wall_seconds": 510, "rss_cap_bytes": 8589934592, "direct_libproc_group_rss": True, "atomic": True, "stop_any": True},
    "hostile_count": hostile_result["hostile_count"],
    "pins": {"Q_source_sha256": sha256(source), "modular_held_manifest_sha256": plan["pins"]["modular_held_manifest_sha256"], "modular_referee_v1_manifest_sha256": plan["pins"]["modular_referee_v1_manifest_sha256"], "modular_referee_v2_manifest_sha256": plan["pins"]["modular_referee_v2_manifest_sha256"], "prior_consumed_k0_manifest_sha256": plan["pins"]["prior_consumed_k0_terminal_manifest_sha256"]},
    "schema": "KRENN_X5_REP5_OPEN84_SAME_STRATUM_EXACT_Q_CONDITIONAL_VALIDATION_V1",
    "scope": {"solver_runs": 0, "attempts": 0, "mathematical_coverage": False, "rep5_closed": False},
    "status": "PASS_ZERO_RUN_FAIL_CLOSED",
}
(HERE / "results_validation.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
