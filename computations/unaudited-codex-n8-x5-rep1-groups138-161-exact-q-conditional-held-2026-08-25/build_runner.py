#!/usr/bin/env python3
"""Derive the final strict 24-lane runner without launching it."""
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25/run_groups88_137.py"
TEMPLATE_SHA = "604b0b938389e44506d627eba8652d74cfe3d3ba10a932efcb6c4dbfeee987e5"
LEDGER_SHA = "ed416a9cc138abae890447995f04e084223fccfe0629da47c9e234e5c02e76be"
SPEC_SHA = "f7750d13c571ef20341dc022f22bc15db94bb9eb2c279f9b3d53e6bb6036463d"
ADAPTER_SHA = "907519564535bc533e060dbef4545ccf2635234041af5d7e0a320db503991568"
RUNNER = HERE / "run_groups138_161.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha256(TEMPLATE) == TEMPLATE_SHA
runner = TEMPLATE.read_text()
runner = runner.replace(
    '"""Strict groups88..137 executor conditional on future exact closure 38..87."""',
    '"""Strict final groups138..161 executor conditional on exact closure 0..137."""',
)
runner = runner.replace("DEPENDENCY_SPEC=HERE/'future_groups38_87_dependency.json'", "DEPENDENCY_SPEC=HERE/'future_groups88_137_dependency.json'")
runner = runner.replace("DEPENDENCY_SPEC_SHA='1374fb5ed562ac0fd6b28ace616e09fbf011509555b02cb98996281d7188b380'", f"DEPENDENCY_SPEC_SHA='{SPEC_SHA}'")
runner = runner.replace("DEPENDENCY_ADAPTER_SHA='87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a'", f"DEPENDENCY_ADAPTER_SHA='{ADAPTER_SHA}'")
runner = runner.replace("LEDGER_SHA='2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b'", f"LEDGER_SHA='{LEDGER_SHA}'")
runner = runner.replace("SELECTED=tuple(range(88,138))", "SELECTED=tuple(range(138,162))")
runner = runner.replace("list(range(1,51))", "list(range(1,25))")
old_normalize = '''normalized=load_and_normalize(future_manifest_sha,future_result_sha)
assert normalized['closed_union']==list(range(88))
baseline_manifest_sha=normalized['pins']['baseline_manifest_sha256']
baseline_dependency_sha=normalized['pins']['baseline_dependency_sha256']
'''
new_normalize = '''normalized=load_and_normalize(future_manifest_sha,future_result_sha)
assert normalized['closed_union']==list(range(138))
'''
assert runner.count(old_normalize) == 1
runner = runner.replace(old_normalize, new_normalize)
runner = runner.replace("KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1", "KRENN_X5_REP1_GROUPS138_161_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1")
runner = runner.replace("PASS_APPROVE_STRICT_GROUPS88_137_BATCH_ONLY", "PASS_APPROVE_STRICT_GROUPS138_161_BATCH_ONLY")
runner = runner.replace("KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_EXPLICIT_CLEARANCE_V1", "KRENN_X5_REP1_GROUPS138_161_EXACT_Q_CONDITIONAL_EXPLICIT_CLEARANCE_V1")
runner = runner.replace("CLEARED_STRICT_GROUPS88_137_BATCH_ONLY", "CLEARED_STRICT_GROUPS138_161_BATCH_ONLY")
runner = runner.replace("KRENN_X5_REP1_GROUPS88_137_BATCH_ATTEMPT_V1", "KRENN_X5_REP1_GROUPS138_161_BATCH_ATTEMPT_V1")
runner = runner.replace("KRENN_X5_REP1_GROUPS88_137_LANE_RESULT_V1", "KRENN_X5_REP1_GROUPS138_161_LANE_RESULT_V1")
runner = runner.replace("KRENN_X5_REP1_GROUPS88_137_BATCH_RESULT_V1", "KRENN_X5_REP1_GROUPS138_161_BATCH_RESULT_V1")
old_fields = "'dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_dependency_sha256':baseline_dependency_sha,'future_terminal_manifest_sha256':future_manifest_sha,'future_terminal_result_sha256':future_result_sha,'required_closed_union':list(range(88))"
new_fields = "'dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'future_terminal_manifest_sha256':future_manifest_sha,'future_terminal_result_sha256':future_result_sha,'required_closed_union':list(range(138))"
assert runner.count(old_fields) == 1
runner = runner.replace(old_fields, new_fields)
old_clearance = "'dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_dependency_sha256':baseline_dependency_sha,'future_terminal_manifest_sha256':future_manifest_sha,'future_terminal_result_sha256':future_result_sha"
new_clearance = "'dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'future_terminal_manifest_sha256':future_manifest_sha,'future_terminal_result_sha256':future_result_sha"
assert runner.count(old_clearance) == 2
runner = runner.replace(old_clearance, new_clearance)
runner = runner.replace("'maximum_lane_count':50", "'maximum_lane_count':24")
runner = runner.replace("'PASS_ALL_50_UNIT'", "'PASS_ALL_24_UNIT'")
assert "range(88,138)" not in runner and "baseline_manifest_sha" not in runner
assert "list(range(138))" in runner and "maximum_lane_count':24" in runner
compile(runner, str(RUNNER), "exec")
RUNNER.write_text(runner)
print(sha256(RUNNER))
