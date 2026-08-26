#!/usr/bin/env python3
"""Independent seal of the groups88..137 satisfied dependency binding."""
from __future__ import annotations
import hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
HELD=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25';HELD_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-referee-2026-08-25';ALIAS=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups38-87-exact-q-terminal-referee-2026-08-25';PROD=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25';TERM_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-terminal-referee-2026-08-25'
PINS={HELD/'MANIFEST.sha256':'07ab0d198fc80b91025df7c892081f2aaaa94158014052246d7700095c054450',HELD/'source_ledger.json':'2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b',HELD/'run_groups88_137.py':'604b0b938389e44506d627eba8652d74cfe3d3ba10a932efcb6c4dbfeee987e5',HELD/'normalize_future_dependency.py':'87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a',HELD_REF/'results_referee.json':'cb9e28e03a6f3449cec78d344e7964c0fd90bd20bb4668ffa0bab1b156fe0bbf',HELD_REF/'HELD_APPROVAL.json':'e2bcfd41206c316487d8372bf5ccd56439381909fe3ff3cf50b4ca3c5238a519',HELD_REF/'FINAL_MANIFEST.sha256':'f664aa999331fa81309a5df1b69d17d3b32d2d3783d44e833b856bc803c60e39',ALIAS/'results_referee.json':'42e13d3e2103283e80f4f91af4d8433e21dc482435b945b3c252fa13452e7763',ALIAS/'FINAL_MANIFEST.sha256':'e6987baa4abf37de21e0466932f554ab9272da8a775ae89e5e25cfadd7ba17fc',PROD/'batch_result.json':'006893f6da40d00fe96df9f09ad2617e5a16edd7ac8677fe19ceec0991fd7a0b',PROD/'TERMINAL_MANIFEST.sha256':'fe4d9f2a1dcb54e0b15b660bfef6d52aca1fe1cb7960246e0958a5e95380cc92',TERM_REF/'results_referee.json':'f6ab9c40f6909b057beb40dcf4a19f28f59df60521a16f1524cf85980e2871e4',TERM_REF/'FINAL_MANIFEST.sha256':'a1aeb1444dcfdde38db7eb80d9759b360da1da66b4c456f4d371f2a8915dae7d'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(m):
 n=0
 for line in m.read_text().splitlines():
  if not line.strip():continue
  e,x=line.split(None,1);p=Path(x.strip());
  if not p.is_absolute():
   local=(m.parent/p).resolve();rooted=(ROOT/p).resolve();p=local if local.is_file() else rooted
  assert p.is_file() and sha(p)==e,p;n+=1
 return n
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
counts={'held':replay(HELD/'MANIFEST.sha256'),'held_referee':replay(HELD_REF/'FINAL_MANIFEST.sha256'),'terminal_binding':replay(ALIAS/'FINAL_MANIFEST.sha256'),'terminal_referee':replay(TERM_REF/'FINAL_MANIFEST.sha256')}
binding=json.loads((HERE/'results_binding.json').read_text());dep=json.loads((HERE/'normalized_dependency_v2.json').read_text());accept=json.loads((HERE/'HELD_ACCEPTANCE_V2.json').read_text());schema=json.loads((HERE/'held_acceptance_v2.schema.json').read_text())
assert binding['status']=='PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE' and dep['status']=='PASS_EXACT_NORMALIZED_CLOSED_UNION_0_87'
assert dep['baseline_closed_union']==list(range(38)) and dep['future_groups_closed']==list(range(38,88)) and dep['closed_union']==list(range(88))
assert len(set(dep['baseline_closed_union']))==38 and len(set(dep['future_groups_closed']))==50 and not set(dep['baseline_closed_union'])&set(dep['future_groups_closed'])
spec=importlib.util.spec_from_file_location('independent_sealed_adapter',HELD/'normalize_future_dependency.py');assert spec and spec.loader
adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter);fresh=adapter.load_and_normalize(PINS[ALIAS/'FINAL_MANIFEST.sha256'],PINS[ALIAS/'results_referee.json'])
assert fresh['baseline_closed_union']==dep['baseline_closed_union'] and fresh['future_groups_closed']==dep['future_groups_closed'] and fresh['closed_union']==dep['closed_union']
alias=json.loads((ALIAS/'results_referee.json').read_text());actual=json.loads((TERM_REF/'results_referee.json').read_text());batch=json.loads((PROD/'batch_result.json').read_text())
assert alias['groups_closed']==actual['groups_closed']==list(range(38,88)) and alias['closed_union']==actual['closed_union_after_batch']==list(range(88))
assert batch['strict_order']==list(range(38,88)) and [x['group_id'] for x in batch['completed']]==list(range(38,88)) and all(x['status']=='UNIT_IDEAL_EXACT_Q' for x in batch['completed']) and batch['stop'] is None
ledger=json.loads((HELD/'source_ledger.json').read_text());assert [x['group_id'] for x in ledger['lanes']]==list(range(88,138)) and sum(x['source_bytes'] for x in ledger['lanes'])==89221428
for lane in ledger['lanes']:
 p=HELD/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes']
assert binding['preservation']=={'source_count':50,'source_bytes':89221428,'source_ledger_sha256_unchanged':PINS[HELD/'source_ledger.json'],'runner_sha256_unchanged':PINS[HELD/'run_groups88_137.py'],'all_source_hashes_replayed':True}
assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])==set(accept)
for key,rule in schema['properties'].items():assert rule=={'const':accept[key]}
assert accept['schema']=='KRENN_X5_REP1_GROUPS88_137_EXACT_Q_SATISFIED_DEPENDENCY_HELD_ACCEPTANCE_V2' and accept['status']=='PASS_HELD_LAUNCH_READY_DEPENDENCY_SATISFIED_NO_CLEARANCE'
assert accept['held_manifest_sha256']==PINS[HELD/'MANIFEST.sha256'] and accept['held_referee_result_sha256']==PINS[HELD_REF/'results_referee.json'] and accept['held_referee_approval_sha256']==PINS[HELD_REF/'HELD_APPROVAL.json'] and accept['held_referee_manifest_sha256']==PINS[HELD_REF/'FINAL_MANIFEST.sha256']
assert accept['required_closed_union']==list(range(88)) and accept['selected_group_ids']==list(range(88,138)) and accept['maximum_lane_count']==50 and accept['exact_Q_authorized']
assert not accept['parallel_authorized'] and not accept['skip_reorder_relaunch_authorized'] and accept['launch_clearance_required'] and not accept['launch_clearance_materialized'] and accept['solver_runs']==0
for absent in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
 assert not (HERE/absent).exists(),absent
assert not (HELD/'independent_referee_acceptance.json').exists() and not (HELD/'launch_clearance.json').exists() and not list(HERE.glob('*.tmp'))
out={'schema':'KRENN_X5_REP1_GROUPS88_137_SATISFIED_DEPENDENCY_BINDING_REFEREE_V2','status':'PASS_INDEPENDENT_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE','producer_binding_sha256':sha(HERE/'results_binding.json'),'normalized_dependency_sha256':sha(HERE/'normalized_dependency_v2.json'),'held_acceptance_sha256':sha(HERE/'HELD_ACCEPTANCE_V2.json'),'acceptance_schema_sha256':sha(HERE/'held_acceptance_v2.schema.json'),'closed_union':list(range(88)),'selected_group_ids':list(range(88,138)),'source_preservation':binding['preservation'],'terminal_lineage':{'producer_batch_sha256':PINS[PROD/'batch_result.json'],'producer_terminal_manifest_sha256':PINS[PROD/'TERMINAL_MANIFEST.sha256'],'referee_result_sha256':PINS[TERM_REF/'results_referee.json'],'referee_manifest_sha256':PINS[TERM_REF/'FINAL_MANIFEST.sha256'],'compatibility_binding_result_sha256':PINS[ALIAS/'results_referee.json'],'compatibility_binding_manifest_sha256':PINS[ALIAS/'FINAL_MANIFEST.sha256']},'held_lineage':{'producer_manifest_sha256':PINS[HELD/'MANIFEST.sha256'],'referee_result_sha256':PINS[HELD_REF/'results_referee.json'],'approval_sha256':PINS[HELD_REF/'HELD_APPROVAL.json'],'referee_manifest_sha256':PINS[HELD_REF/'FINAL_MANIFEST.sha256']},'manifest_counts':counts,'scope':{'held_launch_ready_metadata':True,'runner_acceptance_materialized':False,'launch_clearance_materialized':False,'solver_runs':0,'new_arithmetic':False,'groups_newly_closed':0,'mathematical_coverage_added':False}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'union':88,'sources':50,'runs':0,'clearance':False},sort_keys=True))
