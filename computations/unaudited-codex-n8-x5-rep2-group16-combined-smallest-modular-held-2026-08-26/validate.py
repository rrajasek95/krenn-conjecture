#!/usr/bin/env python3
"""Fail-closed held-package validator; invokes no solver and creates no attempt."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
Q = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26/rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing"
P = H / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(Q) == "2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339"
assert sha(P) == "66bdb9277c9bff605e0d8a808ca65beb5967afaaf8ae494193286a60338355c6"
qbytes, pbytes = Q.read_bytes(), P.read_bytes()
assert qbytes.count(b"ring r=0,(") == 1 and pbytes.count(b"ring r=32003,(") == 1
assert pbytes.replace(b"ring r=32003,(", b"ring r=0,(", 1) == qbytes
assert all(token in pbytes for token in (
    b"ideal G=slimgb(I);", b"poly remainder=reduce(1,G);",
    b"GROEBNER_SIZE=", b"UNIT_REMAINDER=", b"STATUS=UNIT_IDEAL",
))
derivation = json.loads((H / "source_derivation.json").read_text())
held = json.loads((H / "held_pilot.json").read_text())
refusal = json.loads((H / "refusal_contract.json").read_text())
assert derivation["status"] == "PASS_SOLE_Q_TO_P32003_RING_SUBSTITUTION_ZERO_RUN"
assert derivation["modular"] == {
    "path": P.name, "sha256": sha(P), "bytes": P.stat().st_size,
    "field": "F_32003", "variables": 67, "generators": 6574,
}
assert held["status"] == "HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE"
assert held["execution"] == {
    "maximum_lane_count": 1, "native_wall_seconds": 240,
    "wrapper_wall_seconds": 255, "rss_cap_bytes": 8589934592,
    "direct_libproc_group_rss": True, "fresh_libproc_process_census": True,
    "atomic_result": True, "exclusive_attempt_marker": True,
    "strict_stop_after_any_outcome": True,
}
assert held["pins"]["group16_timeout_final_manifest_sha256"] == "066347c8af9a579b8f09d1c1eebf0197e819753da839f30708616287c4336196"
assert held["pins"]["torus_producer_manifest_sha256"] == "1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282"
assert held["pins"]["comparison_referee_manifest_sha256"] == "1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a"
assert held["pins"]["guard_pivot_design_manifest_sha256"] == "6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee"
assert held["authorization"] == {
    "independent_acceptance_present": False, "fresh_clearance_present": False,
    "exact_Q_authorized": False, "other_chart_authorized": False,
    "automatic_relaunch_authorized": False,
}
assert held["scope"] == {
    "solver_runs": 0, "results": 0, "attempts": 0,
    "mathematical_coverage": False, "group16_closed": False,
    "prior_timeout_reused": False,
}
assert refusal["status"] == "HELD_FAIL_CLOSED_ZERO_RUN" and refusal["solver_runs"] == 0
assert refusal["present_acceptance_files"] == refusal["present_clearance_files"] == 0
assert not (H / "independent_referee_acceptance.json").exists()
assert not (H / "launch_clearance.json").exists()
for forbidden in ("ATTEMPT.json", "result.json", "stdout.log", "stderr.log", "watchdog.json", "RUN_EXCLUSIVE.lock"):
    assert not (H / forbidden).exists()
assert not list(H.glob("*.tmp")) and not list(H.rglob("__pycache__"))
runner = H / "run_one_lane.py"
ast.parse(runner.read_text())
runner_text = runner.read_text()
for literal in (
    "NATIVE_WALL = 240", "WRAPPER_WALL = 255", "RSS_CAP = 8 * 1024**3",
    "fresh_process_census()", "process_group_rss_bytes", "exclusive_json(HERE / \"ATTEMPT.json\"",
    '"exact_Q_launched": False', '"other_chart_launched": False',
    '"automatic_relaunch": False',
):
    assert literal in runner_text, literal
for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((H / schema_name).read_text())
    assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"])
if (H / "MANIFEST.sha256").exists():
    for line in (H / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (H / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest, sha(path))
print(json.dumps({"status": "PASS_HELD_ONE_COMBINED_P32003_ZERO_RUN", "source": sha(P), "variables": 67, "generators": 6574, "attempts": 0, "solver_runs": 0}, sort_keys=True))
