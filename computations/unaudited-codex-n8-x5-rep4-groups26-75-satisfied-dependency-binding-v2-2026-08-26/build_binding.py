#!/usr/bin/env python3
"""Bind the sealed rep4 first25 result into the unchanged groups26..75 held batch."""
from __future__ import annotations
import hashlib,json,os,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
HELD=ROOT/'computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26'
HELD_REF=ROOT/'computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-referee-2026-08-26'
FIRST=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26'
FIRST_REF=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26'
PINS={
 HELD/'MANIFEST.sha256':'c79cf415a4dc6327dcaefa7f9f002a1f1f2b5af5afef2a80bab16d8cfc9ccbb6',
 HELD/'source_ledger.json':'48e9fb104efd69a1267f5ff1015a2142af33d481a430bebab2f794442afa8341',
 HELD/'run_groups26_75.py':'b29a78c495517ddb9c43147c5c9ec1091c921a63e4a8285cf7549d0926d721aa',
 HELD/'normalize_dependency.py':'3fca6f290c810bbf9e15d524de79510ab7c7bad11069890e85d12ab8843895a9',
 HELD/'future_dependency.json':'14914c42a19896d680a8cab0c154795ea15b7e8fae0d52b0a0b58e26c8f40a5d',
 HELD/'independent_referee_acceptance.schema.json':'33ca0d910abd5ce8b799cad9203441e0ca545e8dfeff3ac6830887428b9c6a13',
 HELD_REF/'results_referee.json':'6b2d15c8c0b27ef3e6d931bcba44b3471691baad913230cb03a9c6993b6587e4',
 HELD_REF/'HELD_APPROVAL.json':'690da61862010e23a13351919c2f6c32091e3f9bfad6ddc312ec7b1091144ed9',
 HELD_REF/'FINAL_MANIFEST.sha256':'55d13a229ecf359351e8f66a36fae944d14889f4212866eaafa25c83c151962c',
 FIRST/'batch_result.json':'6e982385c76686e743f740e4373b253a6a039c565e8cb6bd59a051cb189fc0dd',
 FIRST/'TERMINAL_MANIFEST.sha256':'8310384d0b26473fec57134cbb5f1b7c2c606e7b6a1af5dcefd5c5dfb3054260',
 FIRST_REF/'results_referee.json':'c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd',
 FIRST_REF/'FINAL_MANIFEST.sha256':'429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,v):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
spec=json.loads((HELD/'future_dependency.json').read_text());batch=json.loads((FIRST/'batch_result.json').read_text());ref=json.loads((FIRST_REF/'results_referee.json').read_text())
assert spec['status']=='UNSATISFIED_NULL_HASH_PAIR' and spec['satisfied'] is False and spec['manifest_sha256'] is spec['result_sha256'] is None
assert batch['status']=='PASS_ALL_25_UNIT' and batch['strict_order']==list(range(1,26)) and [x['group_id'] for x in batch['completed']]==list(range(1,26)) and all(x['status']=='UNIT_IDEAL_EXACT_Q' for x in batch['completed']) and batch['stop'] is None and batch['skipped_after_stop']==[] and batch['parallel'] is batch['relaunch'] is False
assert ref['schema']=='KRENN_X5_REP4_FIRST25_EXACT_Q_TERMINAL_REFEREE_V1' and ref['status']=='PASS_EXACT_GROUPS_1_25_UNIT' and ref['unit_groups_closed']==list(range(1,26)) and ref['closed_union']==list(range(26)) and ref['sealed_group0'] is True
assert spec['required']['groups_closed']==list(range(1,26)) and spec['required']['closed_union']==list(range(26))
ledger=json.loads((HELD/'source_ledger.json').read_text());lanes=ledger['lanes'];assert [x['group_id'] for x in lanes]==list(range(26,76)) and [x['ordinal'] for x in lanes]==list(range(1,51))
for lane in lanes:
 p=HELD/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes']
assert sum(x['source_bytes'] for x in lanes)==90617198
normalized={'schema':'KRENN_X5_REP4_FIRST25_NORMALIZED_DEPENDENCY_V1','status':'PASS_NORMALIZED_EXACT_CLOSED_UNION_0_25','dependency_manifest_path':str((FIRST_REF/'FINAL_MANIFEST.sha256').relative_to(ROOT)),'dependency_result_path':str((FIRST_REF/'results_referee.json').relative_to(ROOT)),'dependency_manifest_sha256':PINS[FIRST_REF/'FINAL_MANIFEST.sha256'],'dependency_result_sha256':PINS[FIRST_REF/'results_referee.json'],'dependency_result_schema':ref['schema'],'dependency_result_status':ref['status'],'groups_closed_by_future':list(range(1,26)),'baseline_closed_group':0,'closed_union':list(range(26)),'duplicates':[],'missing':[],'extra':[],'normalization_note':'old null adapter expected stale PASS_ALL_25_EXACT_Q_UNIT_IDEALS; v2 binds actual sealed PASS_EXACT_GROUPS_1_25_UNIT without changing runner or sources'}
atomic(HERE/'normalized_dependency.json',normalized);dep_sha=sha(HERE/'normalized_dependency.json')
acceptance={'schema':'KRENN_X5_REP4_GROUPS26_75_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1','status':'PASS_APPROVE_CONDITIONAL_REP4_GROUPS26_75_ONLY','held_manifest_sha256':PINS[HELD/'MANIFEST.sha256'],'source_ledger_sha256':PINS[HELD/'source_ledger.json'],'normalized_dependency_sha256':dep_sha,'runner_sha256':PINS[HELD/'run_groups26_75.py'],'required_closed_union':list(range(26)),'selected_group_ids':list(range(26,76)),'maximum_lane_count':50,'exact_Q_authorized':True,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}
atomic(HERE/'independent_referee_acceptance.json',acceptance)
schema=json.loads((HELD/'independent_referee_acceptance.schema.json').read_text());assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])==set(acceptance)
for k,rule in schema['properties'].items():
 if 'const' in rule:assert acceptance[k]==rule['const']
 elif 'pattern' in rule:assert re.fullmatch(rule['pattern'],acceptance[k])
result={'schema':'KRENN_X5_REP4_GROUPS26_75_SATISFIED_DEPENDENCY_BINDING_V2','status':'PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE','normalized_dependency':normalized,'held_acceptance':acceptance,'set_proof':{'baseline':[0],'sealed_future':list(range(1,26)),'intersection':[],'closed_union':list(range(26)),'missing':[],'extra':[],'duplicates':[]},'preservation':{'source_count':50,'source_bytes':90617198,'all_source_hashes_replayed':True,'source_ledger_sha256_unchanged':PINS[HELD/'source_ledger.json'],'runner_sha256_unchanged':PINS[HELD/'run_groups26_75.py'],'sources_rewritten':0,'runner_rewritten':False},'lineage':{'producer_batch_sha256':PINS[FIRST/'batch_result.json'],'producer_terminal_manifest_sha256':PINS[FIRST/'TERMINAL_MANIFEST.sha256'],'referee_result_sha256':PINS[FIRST_REF/'results_referee.json'],'referee_manifest_sha256':PINS[FIRST_REF/'FINAL_MANIFEST.sha256'],'held_manifest_sha256':PINS[HELD/'MANIFEST.sha256'],'held_referee_result_sha256':PINS[HELD_REF/'results_referee.json'],'held_referee_approval_sha256':PINS[HELD_REF/'HELD_APPROVAL.json'],'held_referee_manifest_sha256':PINS[HELD_REF/'FINAL_MANIFEST.sha256']},'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'scope':{'held_launch_ready_metadata':True,'launch_clearance_materialized':False,'solver_runs':0,'new_arithmetic':False,'mathematical_coverage_added':False}}
atomic(HERE/'results_binding.json',result)
print(json.dumps({'status':result['status'],'union':26,'sources':50,'runs':0,'clearance':False},sort_keys=True))
