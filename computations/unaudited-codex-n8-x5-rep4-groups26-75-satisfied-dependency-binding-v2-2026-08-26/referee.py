#!/usr/bin/env python3
"""Independent audit of the rep4 groups26..75 satisfied binding."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
HELD=ROOT/'computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26';HELD_REF=ROOT/'computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-referee-2026-08-26';FIRST=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26';FIRST_REF=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26'
PINS={HELD/'MANIFEST.sha256':'c79cf415a4dc6327dcaefa7f9f002a1f1f2b5af5afef2a80bab16d8cfc9ccbb6',HELD/'source_ledger.json':'48e9fb104efd69a1267f5ff1015a2142af33d481a430bebab2f794442afa8341',HELD/'run_groups26_75.py':'b29a78c495517ddb9c43147c5c9ec1091c921a63e4a8285cf7549d0926d721aa',HELD_REF/'results_referee.json':'6b2d15c8c0b27ef3e6d931bcba44b3471691baad913230cb03a9c6993b6587e4',HELD_REF/'HELD_APPROVAL.json':'690da61862010e23a13351919c2f6c32091e3f9bfad6ddc312ec7b1091144ed9',HELD_REF/'FINAL_MANIFEST.sha256':'55d13a229ecf359351e8f66a36fae944d14889f4212866eaafa25c83c151962c',FIRST/'batch_result.json':'6e982385c76686e743f740e4373b253a6a039c565e8cb6bd59a051cb189fc0dd',FIRST/'TERMINAL_MANIFEST.sha256':'8310384d0b26473fec57134cbb5f1b7c2c606e7b6a1af5dcefd5c5dfb3054260',FIRST_REF/'results_referee.json':'c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd',FIRST_REF/'FINAL_MANIFEST.sha256':'429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(m):
 n=0
 for line in m.read_text().splitlines():
  if not line.strip():continue
  h,x=line.split(None,1);p=(m.parent/x.strip()).resolve();assert p.is_file() and sha(p)==h,(p,h);n+=1
 return n
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
counts={'held':replay(HELD/'MANIFEST.sha256'),'held_referee':replay(HELD_REF/'FINAL_MANIFEST.sha256'),'first25':replay(FIRST/'TERMINAL_MANIFEST.sha256'),'first25_referee':replay(FIRST_REF/'FINAL_MANIFEST.sha256')}
b=json.loads((HERE/'results_binding.json').read_text());dep=json.loads((HERE/'normalized_dependency.json').read_text());accept=json.loads((HERE/'independent_referee_acceptance.json').read_text());batch=json.loads((FIRST/'batch_result.json').read_text());ref=json.loads((FIRST_REF/'results_referee.json').read_text())
assert b['status']=='PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE' and dep['status']=='PASS_NORMALIZED_EXACT_CLOSED_UNION_0_25'
assert dep['groups_closed_by_future']==list(range(1,26)) and dep['baseline_closed_group']==0 and dep['closed_union']==list(range(26)) and dep['duplicates']==dep['missing']==dep['extra']==[]
assert dep['dependency_result_status']=='PASS_EXACT_GROUPS_1_25_UNIT' and dep['dependency_result_sha256']==PINS[FIRST_REF/'results_referee.json'] and dep['dependency_manifest_sha256']==PINS[FIRST_REF/'FINAL_MANIFEST.sha256']
assert batch['strict_order']==list(range(1,26)) and [x['group_id'] for x in batch['completed']]==list(range(1,26)) and all(x['status']=='UNIT_IDEAL_EXACT_Q' for x in batch['completed']) and batch['stop'] is None
assert ref['unit_groups_closed']==list(range(1,26)) and ref['closed_union']==list(range(26)) and ref['sealed_group0']
ledger=json.loads((HELD/'source_ledger.json').read_text());assert [x['group_id'] for x in ledger['lanes']]==list(range(26,76)) and sum(x['source_bytes'] for x in ledger['lanes'])==90617198
for lane in ledger['lanes']:
 p=HELD/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes']
assert b['preservation']=={'source_count':50,'source_bytes':90617198,'all_source_hashes_replayed':True,'source_ledger_sha256_unchanged':PINS[HELD/'source_ledger.json'],'runner_sha256_unchanged':PINS[HELD/'run_groups26_75.py'],'sources_rewritten':0,'runner_rewritten':False}
schema=json.loads((HELD/'independent_referee_acceptance.schema.json').read_text());assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])==set(accept)
for k,rule in schema['properties'].items():
 if 'const' in rule:assert accept[k]==rule['const']
assert accept['normalized_dependency_sha256']==sha(HERE/'normalized_dependency.json') and accept['required_closed_union']==list(range(26)) and accept['selected_group_ids']==list(range(26,76)) and accept['exact_Q_authorized'] and not accept['parallel_authorized'] and not accept['skip_reorder_relaunch_authorized']
for absent in ('normalized_dependency.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
 assert not (HELD/absent).exists(),absent
assert not list(HERE.glob('*.tmp'))
out={'schema':'KRENN_X5_REP4_GROUPS26_75_SATISFIED_DEPENDENCY_BINDING_REFEREE_V2','status':'PASS_INDEPENDENT_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE','binding_sha256':sha(HERE/'results_binding.json'),'normalized_dependency_sha256':sha(HERE/'normalized_dependency.json'),'acceptance_sha256':sha(HERE/'independent_referee_acceptance.json'),'closed_union':list(range(26)),'selected_group_ids':list(range(26,76)),'preservation':b['preservation'],'lineage':b['lineage'],'manifest_counts':counts,'interface_note':'v2 binds actual sealed first25 referee status; old null adapter stale status literal is not used','scope':{'held_launch_ready_metadata':True,'install_into_held_performed':False,'launch_clearance_materialized':False,'solver_runs':0,'new_arithmetic':False,'mathematical_coverage_added':False}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'union':26,'sources':50,'runs':0,'clearance':False},sort_keys=True))
