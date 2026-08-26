#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ledger=json.loads((HERE/'source_ledger.json').read_text());plan=json.loads((HERE/'held_schedule.json').read_text());runner=(HERE/'run_next25.py').read_text()
SELECTED=[11,12,14]+list(range(16,38));CLOSED=list(range(0,11))+[13,15]
assert sha(HERE/'source_ledger.json')=='67376d9ddc96b65f0c34d0f746c85703417d0fb3be88ce5d2cf90a601945c833'
assert sha(HERE/'run_next25.py')=='ad655676b830652681cddd7aa7af46987713984bb63db7dc68157bf88800c268'
assert plan['status']=='HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT'
assert plan['selection']=={'excluded_closed_groups':CLOSED,'rule':'25 lowest eligible canonical group IDs in strict ascending order','selected_group_ids':SELECTED}
assert [x['group_id'] for x in plan['lanes']]==SELECTED
assert plan['execution']['order']==SELECTED and plan['execution']['parallel'] is False
assert plan['scope']=={'source_regeneration_only':True,'solver_launches':0,'result_files':0,'attempt_markers':0,'clearances':0,'groups_newly_closed':0,'representative_closed':False,'mathematical_coverage':False}
for lane in ledger['lanes']:
 p=HERE/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes']
 s=p.read_text();assert s.count('ring r=0,')==s.count('ideal G=slimgb(I);')==s.count('poly remainder=reduce(1,G);')==s.count('quit;')==1
compile(runner,str(HERE/'run_next25.py'),'exec')
for token in ('proc_listpgrppids','group_rss','rusage failure for live member','SELECTED=(11,12,14)+tuple(range(16,38))','--kill-after={KILL_AFTER}s',"f'{WRAPPER_WALL}s'",'if not unit:stop=','atomic(HERE/\'results\'','BATCH_ATTEMPT.json'):
 assert token in runner,token
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 schema=json.loads((HERE/name).read_text());assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])
for absent in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
 assert not (HERE/absent).exists(),absent
assert not any(HERE.glob('*.tmp'))
print(json.dumps({'status':'PASS_HELD_ZERO_RUNS','groups':SELECTED,'sources':25,'runner_sha256':sha(HERE/'run_next25.py')},sort_keys=True))
