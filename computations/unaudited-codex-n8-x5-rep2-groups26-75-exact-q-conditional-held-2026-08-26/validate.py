#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
l=json.loads((HERE/'source_ledger.json').read_text());f=json.loads((HERE/'future_dependency.json').read_text());p=json.loads((HERE/'held_schedule.json').read_text());h=json.loads((HERE/'results_hostile_tests.json').read_text());assert sha(HERE/'source_ledger.json')=='0a9ad8dfb140d8e601c88429c13945d1182ac6dffe2c7dcc022a1b353a1005e7' and sha(HERE/'future_dependency.json')=='df9ec9aba49241c0d17853c9081917e48b134e16b51f382fee85f4f5f550651c' and sha(HERE/'normalize_dependency.py')=='c4625a17f0368e94a1debed8c76126284f9a66e4dc0de929025046f2ca15e150' and sha(HERE/'run_groups26_75.py')=='2cdcfa471e0432a734b9089a14f4f8443ea609b3517a6cd7f4bd853133b568b9';assert f['status']=='UNSATISFIED_NULL_HASH_PAIR' and f['satisfied'] is False and f['manifest_sha256'] is f['result_sha256'] is None and f['required']['groups_closed']==list(range(1,26)) and f['required']['closed_union']==list(range(26));assert not (ROOT/f['required']['manifest_path']).exists() and not (ROOT/f['required']['result_path']).exists() and not (HERE/'normalized_dependency.json').exists();assert l['selection']['required_closed_union']==list(range(26)) and l['selection']['selected_group_ids']==list(range(26,76)) and [x['group_id'] for x in l['lanes']]==list(range(26,76))
for x in l['lanes']:s=HERE/x['source_path'];assert sha(s)==x['source_sha256'] and s.stat().st_size==x['source_bytes'];text=s.read_text();assert text.count('ring r=0,')==text.count('ideal G=slimgb(I);')==text.count('poly remainder=reduce(1,G);')==text.count('quit;')==1
adapter=(HERE/'normalize_dependency.py').read_text();runner=(HERE/'run_groups26_75.py').read_text();compile(adapter,str(HERE/'normalize_dependency.py'),'exec');compile(runner,str(HERE/'run_groups26_75.py'),'exec')
for token in ('proc_listpgrppids','proc_pid_rusage','group_rss','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','NORMALIZED.is_file()','PASS_NORMALIZED_EXACT_CLOSED_UNION_0_25','BATCH_ATTEMPT.json','if not unit:stop=','atomic(path,record)'):assert token in runner,token
assert p['status']=='HELD_FUTURE_FIRST25_PASS_ABSENT_ZERO_RUN' and p['execution']['order']==list(range(26,76)) and not any(p['execution'][x] for x in ('parallel','skip','reorder','relaunch'));assert p['scope']['solver_launches']==p['scope']['groups_newly_closed']==0 and p['scope']['cross_representative_transport'] is False;assert h['status']=='PASS_12_HOSTILES_FUTURE_ABSENT' and len(h['tests'])==12 and all(h['tests'].values())
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):s=json.loads((HERE/name).read_text());assert s['additionalProperties'] is False and set(s['required'])==set(s['properties'])
for absent in ('normalized_dependency.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (HERE/absent).exists(),absent
assert not list(HERE.glob('*.tmp'))
for rel,expected in l['pins'].items():path=ROOT/rel;assert path.is_file() and sha(path)==expected
m=HERE/'MANIFEST.sha256';n=0
if m.exists():
 for line in m.read_text().splitlines():digest,name=line.split('  ',1);path=(HERE/name).resolve();assert path.is_file() and sha(path)==digest,name;n+=1
print(json.dumps({'status':'PASS_CONDITIONAL_HELD_ZERO_RUN','selected':[26,75],'sources':50,'future_hashes_null':2,'manifest_lines_checked':n,'solver_runs':0},sort_keys=True))
