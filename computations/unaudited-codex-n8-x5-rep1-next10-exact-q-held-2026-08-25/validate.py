#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ledger=json.loads((HERE/'source_ledger.json').read_text());plan=json.loads((HERE/'held_schedule.json').read_text());runner=(HERE/'run_next10.py').read_text()
assert sha(HERE/'source_ledger.json')=='9daee573bd3560b381920e72e95dcdb45246f7feaaae02ffcf24e373f6bb6fcd'
assert sha(HERE/'run_next10.py')=='810ba01dc8823f9ea7c9064989720f5ba65b488d19c182ef00886cc8a4941d6b'
assert plan['status']=='HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT'
assert plan['selection']=={'excluded_closed_groups':[0,13,15],'rule':'ten lowest eligible canonical group IDs in strict ascending order','selected_group_ids':list(range(1,11))}
assert [x['group_id'] for x in plan['lanes']]==list(range(1,11))
assert plan['execution']['order']==list(range(1,11)) and plan['execution']['parallel'] is False
assert plan['scope']=={'source_regeneration_only':True,'solver_launches':0,'result_files':0,'attempt_markers':0,'clearances':0,'groups_newly_closed':0,'representative_closed':False,'mathematical_coverage':False}
for lane in ledger['lanes']:
 p=HERE/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes']
 s=p.read_text();assert s.count('ring r=0,')==s.count('ideal G=slimgb(I);')==s.count('poly remainder=reduce(1,G);')==s.count('quit;')==1
compile(runner,str(HERE/'run_next10.py'),'exec')
for token in ('proc_listpgrppids','group_rss','rusage failure for live member','list(range(1,11))','--kill-after={KILL_AFTER}s',"f'{WRAPPER_WALL}s'",'if not unit:stop=','atomic(HERE/\'results\'','BATCH_ATTEMPT.json'):
 assert token in runner,token
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 schema=json.loads((HERE/name).read_text());assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])
for absent in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
 assert not (HERE/absent).exists(),absent
assert not any(HERE.glob('*.tmp'))
print(json.dumps({'status':'PASS_HELD_ZERO_RUNS','groups':list(range(1,11)),'sources':10,'runner_sha256':sha(HERE/'run_next10.py')},sort_keys=True))
