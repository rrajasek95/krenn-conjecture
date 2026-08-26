#!/usr/bin/env python3
"""Static validation of the final conditional 24-source package."""
import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];SELECTED=list(range(138,162));LEDGER_SHA='ed416a9cc138abae890447995f04e084223fccfe0629da47c9e234e5c02e76be';RUNNER_SHA='a942eb6a12512f334bc6bdbf1b023c1428c8372fda46032dbddfb84dcf554f8b';SPEC_SHA='f7750d13c571ef20341dc022f22bc15db94bb9eb2c279f9b3d53e6bb6036463d';ADAPTER_SHA='907519564535bc533e060dbef4545ccf2635234041af5d7e0a320db503991568'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(schema,value):
 props=schema['properties'];assert schema['additionalProperties'] is False and set(schema['required'])==set(props)==set(value)
 for k,r in props.items():
  if 'const' in r:assert value[k]==r['const']
  elif r.get('pattern')=='^[0-9a-f]{64}$':assert isinstance(value[k],str) and len(value[k])==64 and all(c in '0123456789abcdef' for c in value[k])
assert sha(HERE/'source_ledger.json')==LEDGER_SHA and sha(HERE/'run_groups138_161.py')==RUNNER_SHA and sha(HERE/'future_groups88_137_dependency.json')==SPEC_SHA and sha(HERE/'normalize_future_dependency.py')==ADAPTER_SHA
ledger=json.loads((HERE/'source_ledger.json').read_text());plan=json.loads((HERE/'held_schedule.json').read_text());dep=json.loads((HERE/'future_groups88_137_dependency.json').read_text());tests=json.loads((HERE/'results_adapter_tests.json').read_text())
assert [x['group_id'] for x in ledger['lanes']]==SELECTED and plan['status']=='HELD_ZERO_RUNS_FUTURE_GROUPS88_137_HASHES_ABSENT' and plan['execution']['order']==SELECTED and plan['execution']['maximum_lane_count']==24
assert all(plan['execution'][k] is False for k in ('parallel','skip','reorder','relaunch'))
assert dep['future_manifest_sha256'] is dep['future_result_sha256'] is None and dep['satisfied'] is False and dep['expected_baseline_closed_union']==list(range(88)) and dep['expected_future_groups_closed']==list(range(88,138)) and dep['required_closed_union']==list(range(138))
assert not (ROOT/dep['future_manifest_path']).exists() and not (ROOT/dep['future_result_path']).exists()
assert tests['status']=='PASS_VALID_MOCK_AND_12_HOSTILES' and tests['future_files_present'] is False and all(tests['hostile_tests'].values())
for lane in ledger['lanes']:
 p=HERE/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes'];s=p.read_text();assert s.count('ring r=0,')==s.count('ideal G=slimgb(I);')==s.count('poly remainder=reduce(1,G);')==s.count('quit;')==1
runner=(HERE/'run_groups138_161.py').read_text();compile(runner,str(HERE/'run_groups138_161.py'),'exec')
for token in ('SELECTED=tuple(range(138,162))','list(range(1,25))','load_and_normalize(future_manifest_sha,future_result_sha)',"normalized['closed_union']==list(range(138))",'proc_listpgrppids','rusage failure for live member','NATIVE_WALL=240','WRAPPER_WALL=250','if not unit:stop=',"atomic(HERE/'results'/",'BATCH_ATTEMPT.json',"'parallel':False","'relaunch':False"):assert token in runner,token
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 schema=json.loads((HERE/name).read_text());good={k:r.get('const','0'*64) for k,r in schema['properties'].items()};check(schema,good)
 for key,bad in (('future_terminal_manifest_sha256',None),('future_terminal_result_sha256',None),('selected_group_ids',SELECTED[:-1]),('parallel_authorized',True),('skip_reorder_relaunch_authorized',True)):
  candidate=copy.deepcopy(good);candidate[key]=bad
  try:check(schema,candidate)
  except AssertionError:pass
  else:raise AssertionError((name,key))
for absent in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (HERE/absent).exists(),absent
assert not any(HERE.glob('*.tmp'))
print(json.dumps({'status':'PASS_FINAL_HELD_ZERO_RUNS_NULL_DEPENDENCY_HASHES','sources':24,'runner_sha256':RUNNER_SHA,'adapter_hostiles':12,'solver_runs':0},sort_keys=True))
