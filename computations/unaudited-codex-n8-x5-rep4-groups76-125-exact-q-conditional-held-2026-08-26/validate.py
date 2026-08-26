#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
l=json.loads((HERE/'source_ledger.json').read_text());f=json.loads((HERE/'future_dependencies.json').read_text());p=json.loads((HERE/'held_schedule.json').read_text());h=json.loads((HERE/'results_hostile_tests.json').read_text());assert sha(HERE/'source_ledger.json')=='b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb' and sha(HERE/'future_dependencies.json')=='02e042533a68fb7a9a08d230caa7de915c3176e4d7e54b8f68a9704da7e6916e' and sha(HERE/'normalize_dependencies.py')=='5afc90779b09c31950e30cb7f11cb198d9c37f5d655e6926fcfad2980561733c' and sha(HERE/'run_groups76_125.py')=='3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd';assert f['status']=='UNSATISFIED_BOTH_NULL_HASH_PAIRS' and f['satisfied'] is False and f['required_closed_union']==list(range(76));assert [d['groups_closed'] for d in f['dependencies']]==[list(range(1,26)),list(range(26,76))] and all(d['satisfied'] is False and d['manifest_sha256'] is d['result_sha256'] is None for d in f['dependencies'])
for d in f['dependencies']:assert not (ROOT/d['manifest_path']).exists() and not (ROOT/d['result_path']).exists()
assert not (HERE/'normalized_dependencies.json').exists();assert l['selection']['required_closed_union']==list(range(76)) and l['selection']['selected_group_ids']==list(range(76,126)) and [x['group_id'] for x in l['lanes']]==list(range(76,126))
for x in l['lanes']:s=HERE/x['source_path'];assert sha(s)==x['source_sha256'] and s.stat().st_size==x['source_bytes'];text=s.read_text();assert text.count('ring r=0,')==text.count('ideal G=slimgb(I);')==text.count('poly remainder=reduce(1,G);')==text.count('quit;')==1
adapter=(HERE/'normalize_dependencies.py').read_text();runner=(HERE/'run_groups76_125.py').read_text();compile(adapter,str(HERE/'normalize_dependencies.py'),'exec');compile(runner,str(HERE/'run_groups76_125.py'),'exec')
for token in ('proc_listpgrppids','proc_pid_rusage','group_rss','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','NORMALIZED.is_file()','PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75','BATCH_ATTEMPT.json','if not unit:stop=','atomic(path,record)'):assert token in runner,token
assert p['status']=='HELD_BOTH_FUTURE_PASSES_ABSENT_ZERO_RUN' and p['execution']['order']==list(range(76,126)) and not any(p['execution'][x] for x in ('parallel','skip','reorder','relaunch'));assert p['scope']['solver_launches']==p['scope']['groups_newly_closed']==0 and p['scope']['cross_representative_transport'] is False;assert h['status']=='PASS_12_HOSTILES_BOTH_FUTURES_ABSENT' and len(h['tests'])==12 and all(h['tests'].values())
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):s=json.loads((HERE/name).read_text());assert s['additionalProperties'] is False and set(s['required'])==set(s['properties'])
for absent in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (HERE/absent).exists(),absent
assert not list(HERE.glob('*.tmp'))
for rel,expected in l['pins'].items():path=ROOT/rel;assert path.is_file() and sha(path)==expected
m=HERE/'MANIFEST.sha256';n=0
if m.exists():
 for line in m.read_text().splitlines():digest,name=line.split('  ',1);path=(HERE/name).resolve();assert path.is_file() and sha(path)==digest,name;n+=1
print(json.dumps({'status':'PASS_CONDITIONAL_HELD_ZERO_RUN','selected':[76,125],'sources':50,'future_hashes_null':4,'manifest_lines_checked':n,'solver_runs':0},sort_keys=True))
