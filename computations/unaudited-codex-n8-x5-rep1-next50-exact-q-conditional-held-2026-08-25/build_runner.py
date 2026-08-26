#!/usr/bin/env python3
"""Derive the strict conditional next-50 executor from the sealed next-25 runner."""
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-2026-08-25/run_next25.py"
RUNNER = HERE / "run_next50.py"
TEMPLATE_SHA = "ad655676b830652681cddd7aa7af46987713984bb63db7dc68157bf88800c268"
LEDGER_SHA = "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172"
DEPENDENCY_SHA = "PLACEHOLDER_REPLACED_AFTER_FIRST_BUILD"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha256(TEMPLATE) == TEMPLATE_SHA
dependency_sha = sha256(HERE / "future_next25_dependency.json")
runner = TEMPLATE.read_text()
runner = runner.replace(
    '"""Refusal-locked strict sequential executor for the sealed rep1 next-25 ledger."""',
    '"""Refusal-locked strict sequential executor conditional on next25 terminal PASS."""',
)
runner = runner.replace("run_next25.py", "run_next50.py")
runner = runner.replace("LEDGER_SHA='67376d9ddc96b65f0c34d0f746c85703417d0fb3be88ce5d2cf90a601945c833'", f"LEDGER_SHA='{LEDGER_SHA}'")
runner = runner.replace("SELECTED=(11,12,14)+tuple(range(16,38))", "SELECTED=tuple(range(38,88))")
runner = runner.replace("NEXT25", "NEXT50")
runner = runner.replace("next-25", "conditional next-50")
runner = runner.replace("range(1,26)", "range(1,51)")
runner = runner.replace("'maximum_lane_count':25", "'maximum_lane_count':50")
runner = runner.replace("'maximum_lane_count':25", "'maximum_lane_count':50")
runner = runner.replace("'PASS_ALL_25_UNIT'", "'PASS_ALL_50_UNIT'")
runner = runner.replace("'completed':len(batch)", "'completed':len(batch)")
runner = runner.replace("'KRENN_X5_REP1_NEXT50_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1'", "'KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_INDEPENDENT_ACCEPTANCE_V1'")
runner = runner.replace("'PASS_APPROVE_STRICT_NEXT50_BATCH_ONLY'", "'PASS_APPROVE_STRICT_CONDITIONAL_NEXT50_BATCH_ONLY'")
runner = runner.replace("'KRENN_X5_REP1_NEXT50_EXACT_Q_EXPLICIT_CLEARANCE_V1'", "'KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_EXPLICIT_CLEARANCE_V1'")
runner = runner.replace("'CLEARED_STRICT_NEXT50_BATCH_ONLY'", "'CLEARED_STRICT_CONDITIONAL_NEXT50_BATCH_ONLY'")
runner = runner.replace("'KRENN_X5_REP1_NEXT50_BATCH_ATTEMPT_V1'", "'KRENN_X5_REP1_NEXT50_CONDITIONAL_BATCH_ATTEMPT_V1'")
runner = runner.replace("'KRENN_X5_REP1_NEXT50_LANE_RESULT_V1'", "'KRENN_X5_REP1_NEXT50_CONDITIONAL_LANE_RESULT_V1'")
runner = runner.replace("'KRENN_X5_REP1_NEXT50_BATCH_RESULT_V1'", "'KRENN_X5_REP1_NEXT50_CONDITIONAL_BATCH_RESULT_V1'")

anchor = "LEDGER=HERE/'source_ledger.json'; SINGULAR=Path('/usr/local/bin/Singular'); GTIMEOUT=Path('/usr/local/bin/gtimeout')"
replacement = anchor + "\nDEPENDENCY_SPEC=HERE/'future_next25_dependency.json'\nDEPENDENCY_SPEC_SHA='" + dependency_sha + "'"
assert runner.count(anchor) == 1
runner = runner.replace(anchor, replacement)

old_load = "a=json.loads(acceptance.read_text());c=json.loads(clearance.read_text());runner_sha=sha(Path(__file__))"
new_load = '''a=json.loads(acceptance.read_text());c=json.loads(clearance.read_text());runner_sha=sha(Path(__file__))
dependency=json.loads(DEPENDENCY_SPEC.read_text())
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
assert runner.count(old_load) == 1
runner = runner.replace(old_load, new_load)

old_acceptance = "'selected_group_ids':list(SELECTED),'maximum_lane_count':50,'exact_Q_authorized':True,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}"
new_acceptance = "'selected_group_ids':list(SELECTED),'maximum_lane_count':50,'future_dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'next25_terminal_closed_union':list(range(38)),'exact_Q_authorized':True,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}"
assert runner.count(old_acceptance) == 1
runner = runner.replace(old_acceptance, new_acceptance)

old_clearance = "'selected_group_ids':list(SELECTED),'native_wall_seconds_each':NATIVE_WALL"
new_clearance = "'selected_group_ids':list(SELECTED),'future_dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'native_wall_seconds_each':NATIVE_WALL"
assert runner.count(old_clearance) == 1
runner = runner.replace(old_clearance, new_clearance)

old_attempt = "'clearance_sha256':sha(clearance)}"
new_attempt = "'clearance_sha256':sha(clearance),'future_dependency_spec_sha256':DEPENDENCY_SPEC_SHA,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha}"
assert runner.count(old_attempt) == 1
runner = runner.replace(old_attempt, new_attempt)

assert "range(1,26)" not in runner and "maximum_lane_count':25" not in runner
assert "NEXT25" not in runner
assert "future_manifest.is_file()" in runner and "UNSATISFIED_PLACEHOLDER_BLOCKS_LAUNCH" in runner
compile(runner, str(RUNNER), "exec")
RUNNER.write_text(runner)
print(sha256(RUNNER))
