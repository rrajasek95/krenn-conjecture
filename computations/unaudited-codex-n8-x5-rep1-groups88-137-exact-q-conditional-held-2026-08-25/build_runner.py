#!/usr/bin/env python3
"""Derive the groups88..137 conditional runner from the sealed normalized next50 runner."""
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25/run_next50_v2.py"
TEMPLATE_SHA = "b9fc730669e6e5fc4799e9efbf4e6f12b1f443acc004af9bc536be851c4d8388"
LEDGER_SHA = "2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b"
SPEC_SHA = "1374fb5ed562ac0fd6b28ace616e09fbf011509555b02cb98996281d7188b380"
ADAPTER_SHA = "87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a"
RUNNER = HERE / "run_groups88_137.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha256(TEMPLATE) == TEMPLATE_SHA
runner = TEMPLATE.read_text()
runner = runner.replace(
    '"""Strict next50 executor using the audited baseline+next25 normalization adapter."""',
    '"""Strict groups88..137 executor conditional on future exact closure 38..87."""',
)
runner = runner.replace("from normalize_next25_dependency import load_and_normalize", "from normalize_future_dependency import load_and_normalize")
runner = runner.replace(
    "NORMALIZED_DEPENDENCY=HERE/'normalized_next25_dependency.json'\nNORMALIZED_DEPENDENCY_SHA='29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76'\nDEPENDENCY_ADAPTER_SHA='c9c3d365f0f2fb3c9a03656822b4112b245455745dd4f707367fff6c6c2e6d11'",
    f"DEPENDENCY_SPEC=HERE/'future_groups38_87_dependency.json'\nDEPENDENCY_SPEC_SHA='{SPEC_SHA}'\nDEPENDENCY_ADAPTER_SHA='{ADAPTER_SHA}'",
)
runner = runner.replace("LEDGER_SHA='1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172'", f"LEDGER_SHA='{LEDGER_SHA}'")
runner = runner.replace("SELECTED=tuple(range(38,88))", "SELECTED=tuple(range(88,138))")
old_normalize = '''assert sha(HERE/'normalize_next25_dependency.py')==DEPENDENCY_ADAPTER_SHA
assert sha(NORMALIZED_DEPENDENCY)==NORMALIZED_DEPENDENCY_SHA
normalized=load_and_normalize()
assert normalized==json.loads(NORMALIZED_DEPENDENCY.read_text())
assert normalized['closed_union']==list(range(38))
future_manifest_sha=normalized['pins']['next25_terminal_manifest_sha256']
future_result_sha=normalized['pins']['next25_terminal_result_sha256']
baseline_manifest_sha=normalized['pins']['baseline_manifest_sha256']
baseline_result_sha=normalized['pins']['baseline_result_sha256']
binding_audit_manifest_sha=normalized['pins']['binding_audit_manifest_sha256']
binding_audit_result_sha=normalized['pins']['binding_audit_result_sha256']
'''
new_normalize = '''assert sha(HERE/'normalize_future_dependency.py')==DEPENDENCY_ADAPTER_SHA
assert sha(DEPENDENCY_SPEC)==DEPENDENCY_SPEC_SHA
assert set(a) >= {'future_terminal_manifest_sha256','future_terminal_result_sha256'}
future_manifest_sha=a['future_terminal_manifest_sha256'];future_result_sha=a['future_terminal_result_sha256']
normalized=load_and_normalize(future_manifest_sha,future_result_sha)
assert normalized['closed_union']==list(range(88))
baseline_manifest_sha=normalized['pins']['baseline_manifest_sha256']
baseline_dependency_sha=normalized['pins']['baseline_dependency_sha256']
'''
assert runner.count(old_normalize) == 1
runner = runner.replace(old_normalize, new_normalize)
runner = runner.replace("KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_INDEPENDENT_ACCEPTANCE_V2", "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1")
runner = runner.replace("PASS_APPROVE_STRICT_NORMALIZED_NEXT50_BATCH_ONLY", "PASS_APPROVE_STRICT_GROUPS88_137_BATCH_ONLY")
runner = runner.replace("KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_EXPLICIT_CLEARANCE_V2", "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_EXPLICIT_CLEARANCE_V1")
runner = runner.replace("CLEARED_STRICT_NORMALIZED_NEXT50_BATCH_ONLY", "CLEARED_STRICT_GROUPS88_137_BATCH_ONLY")
runner = runner.replace("KRENN_X5_REP1_NEXT50_NORMALIZED_BATCH_ATTEMPT_V2", "KRENN_X5_REP1_GROUPS88_137_BATCH_ATTEMPT_V1")
runner = runner.replace("KRENN_X5_REP1_NEXT50_NORMALIZED_LANE_RESULT_V2", "KRENN_X5_REP1_GROUPS88_137_LANE_RESULT_V1")
runner = runner.replace("KRENN_X5_REP1_NEXT50_NORMALIZED_BATCH_RESULT_V2", "KRENN_X5_REP1_GROUPS88_137_BATCH_RESULT_V1")
old_fields = "'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'normalized_dependency_sha256':NORMALIZED_DEPENDENCY_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_result_sha256':baseline_result_sha,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'binding_audit_manifest_sha256':binding_audit_manifest_sha,'binding_audit_result_sha256':binding_audit_result_sha,'next25_terminal_closed_union':list(range(38))"
new_fields = "'dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_dependency_sha256':baseline_dependency_sha,'future_terminal_manifest_sha256':future_manifest_sha,'future_terminal_result_sha256':future_result_sha,'required_closed_union':list(range(88))"
assert runner.count(old_fields) == 1
runner = runner.replace(old_fields, new_fields)
old_clearance = "'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'normalized_dependency_sha256':NORMALIZED_DEPENDENCY_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_result_sha256':baseline_result_sha,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'binding_audit_manifest_sha256':binding_audit_manifest_sha,'binding_audit_result_sha256':binding_audit_result_sha"
new_clearance = "'dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_dependency_sha256':baseline_dependency_sha,'future_terminal_manifest_sha256':future_manifest_sha,'future_terminal_result_sha256':future_result_sha"
assert runner.count(old_clearance) == 2
runner = runner.replace(old_clearance, new_clearance)
assert "range(38,88)" not in runner and "NORMALIZED_DEPENDENCY" not in runner
assert "load_and_normalize(future_manifest_sha,future_result_sha)" in runner
compile(runner, str(RUNNER), "exec")
RUNNER.write_text(runner)
print(sha256(RUNNER))
