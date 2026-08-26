#!/usr/bin/env python3
"""Clone the exact 50-source ledger and derive the normalized-dependency runner v2."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25"
PRIOR_MANIFEST_SHA = "db8aa8acd4977934273c28249ffba8930c102cec2fc10bad9d86edb7fa51423d"
LEDGER_SHA = "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172"
PRIOR_RUNNER_SHA = "eba736280a2d724cc1c46370d85292d7543f7bfd46a7e51e813c5bfe6ce0b66e"
ADAPTER_SHA = "c9c3d365f0f2fb3c9a03656822b4112b245455745dd4f707367fff6c6c2e6d11"
NORMALIZED_SHA = "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha256(PRIOR / "MANIFEST.sha256") == PRIOR_MANIFEST_SHA
assert sha256(PRIOR / "source_ledger.json") == LEDGER_SHA
assert sha256(PRIOR / "run_next50.py") == PRIOR_RUNNER_SHA
assert sha256(HERE / "normalize_next25_dependency.py") == ADAPTER_SHA
assert sha256(HERE / "normalized_next25_dependency.json") == NORMALIZED_SHA

(HERE / "sources").mkdir(exist_ok=True)
shutil.copyfile(PRIOR / "source_ledger.json", HERE / "source_ledger.json")
for gid in range(38, 88):
    source = PRIOR / "sources" / f"rep1_group{gid:03d}_Q.sing"
    target = HERE / "sources" / source.name
    shutil.copyfile(source, target)
    assert sha256(target) == sha256(source)
assert sha256(HERE / "source_ledger.json") == LEDGER_SHA

runner = (PRIOR / "run_next50.py").read_text()
runner = runner.replace(
    '"""Refusal-locked strict sequential executor conditional on next25 terminal PASS."""',
    '"""Strict next50 executor using the audited baseline+next25 normalization adapter."""',
)
runner = runner.replace("import ctypes,hashlib,json,os,signal,subprocess,time", "import ctypes,hashlib,json,os,signal,subprocess,time\nfrom normalize_next25_dependency import load_and_normalize")
runner = runner.replace(
    "DEPENDENCY_SPEC=HERE/'future_next25_dependency.json'\nDEPENDENCY_SPEC_SHA='aba4c9792cd2874269722f678864130cfde27c30caa47d505249a77ada82c896'",
    "NORMALIZED_DEPENDENCY=HERE/'normalized_next25_dependency.json'\nNORMALIZED_DEPENDENCY_SHA='29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76'\nDEPENDENCY_ADAPTER_SHA='c9c3d365f0f2fb3c9a03656822b4112b245455745dd4f707367fff6c6c2e6d11'",
)
old_block = '''dependency=json.loads(DEPENDENCY_SPEC.read_text())
assert sha(DEPENDENCY_SPEC)==DEPENDENCY_SPEC_SHA
assert dependency['status']=='UNSATISFIED_PLACEHOLDER_BLOCKS_LAUNCH' and dependency['satisfied'] is False
assert dependency['current_future_manifest_sha256'] is None and dependency['current_future_result_sha256'] is None
future_manifest=ROOT/dependency['future_manifest_path'];future_result=ROOT/dependency['future_result_path']
assert future_manifest.is_file() and future_result.is_file(),'HELD: future next25 terminal referee dependency is absent'
future_manifest_sha=sha(future_manifest);future_result_sha=sha(future_result)
future=json.loads(future_result.read_text())
assert future['schema']==dependency['required_future_result_schema']
assert future['status']==dependency['required_future_result_status']
assert future['groups_closed']==dependency['expected_closed_group_ids']
assert future['closed_union']==dependency['expected_closed_union_after_pass']
manifest_lines=future_manifest.read_text().splitlines()
assert f"{future_result_sha}  {dependency['required_manifest_member']}" in manifest_lines
'''
new_block = '''assert sha(HERE/'normalize_next25_dependency.py')==DEPENDENCY_ADAPTER_SHA
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
assert runner.count(old_block) == 1
runner = runner.replace(old_block, new_block)
runner = runner.replace("KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1", "KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_INDEPENDENT_ACCEPTANCE_V2")
runner = runner.replace("PASS_APPROVE_STRICT_CONDITIONAL_NEXT50_BATCH_ONLY", "PASS_APPROVE_STRICT_NORMALIZED_NEXT50_BATCH_ONLY")
runner = runner.replace("KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_EXPLICIT_CLEARANCE_V1", "KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_EXPLICIT_CLEARANCE_V2")
runner = runner.replace("CLEARED_STRICT_CONDITIONAL_NEXT50_BATCH_ONLY", "CLEARED_STRICT_NORMALIZED_NEXT50_BATCH_ONLY")
runner = runner.replace("KRENN_X5_REP1_NEXT50_CONDITIONAL_BATCH_ATTEMPT_V1", "KRENN_X5_REP1_NEXT50_NORMALIZED_BATCH_ATTEMPT_V2")
runner = runner.replace("KRENN_X5_REP1_NEXT50_CONDITIONAL_LANE_RESULT_V1", "KRENN_X5_REP1_NEXT50_NORMALIZED_LANE_RESULT_V2")
runner = runner.replace("KRENN_X5_REP1_NEXT50_CONDITIONAL_BATCH_RESULT_V1", "KRENN_X5_REP1_NEXT50_NORMALIZED_BATCH_RESULT_V2")
old_acceptance_fields = "'future_dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'next25_terminal_closed_union':list(range(38))"
new_acceptance_fields = "'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'normalized_dependency_sha256':NORMALIZED_DEPENDENCY_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_result_sha256':baseline_result_sha,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'binding_audit_manifest_sha256':binding_audit_manifest_sha,'binding_audit_result_sha256':binding_audit_result_sha,'next25_terminal_closed_union':list(range(38))"
assert runner.count(old_acceptance_fields) == 1
runner = runner.replace(old_acceptance_fields, new_acceptance_fields)
old_clearance_fields = "'future_dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha"
new_clearance_fields = "'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'normalized_dependency_sha256':NORMALIZED_DEPENDENCY_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_result_sha256':baseline_result_sha,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'binding_audit_manifest_sha256':binding_audit_manifest_sha,'binding_audit_result_sha256':binding_audit_result_sha"
assert runner.count(old_clearance_fields) == 2  # clearance plus exclusive attempt
runner = runner.replace(old_clearance_fields, new_clearance_fields)
assert "DEPENDENCY_SPEC" not in runner and "future['closed_union']" not in runner
assert "load_and_normalize()" in runner and "binding_audit_manifest_sha" in runner
compile(runner, str(HERE / "run_next50_v2.py"), "exec")
(HERE / "run_next50_v2.py").write_text(runner)
result = {
    "schema": "KRENN_X5_REP1_NEXT50_NORMALIZED_SUPERSESSION_BUILD_V2",
    "status": "PASS_PRESERVED_50_SOURCES_AND_DERIVED_RUNNER_V2_ZERO_RUNS",
    "prior_manifest_sha256": PRIOR_MANIFEST_SHA,
    "source_ledger_sha256": sha256(HERE / "source_ledger.json"),
    "runner_v2_sha256": sha256(HERE / "run_next50_v2.py"),
    "adapter_sha256": ADAPTER_SHA,
    "normalized_dependency_sha256": NORMALIZED_SHA,
    "sources": 50,
    "solver_runs": 0,
}
temporary = HERE / "build_result.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "build_result.json")
print(json.dumps(result, sort_keys=True))
