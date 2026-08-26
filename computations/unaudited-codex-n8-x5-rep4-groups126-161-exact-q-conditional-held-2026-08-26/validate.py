#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={'source_ledger.json':'fa301fd4d1e61626781cedd3ecb362189671b042c9cba8cfbe68977bb79ceb38','future_dependencies.json':'18b7cae58e965187bcbb97ef7a319aacd92fccb6be4010d9630caad83ef77e75','dependency_verifier.py':'fc44d47caef2915dc8cf7dc384d544e8c858e4be8de372b08d01a30abb3b90eb','normalize_dependencies.py':'08f1f5c834499939a06635d7fd95bf4fddb12d9eae047e9ecb3a15dcf87a661f','run_groups126_161.py':'959ab7cfa85ddf23f328ae03edeaefabc0a775ede98b4768953b46c91fe0022a','results_hostile_tests.json':'b15cdacc3ff88d14b43760f430bd9ba327fe332d1d34a99d1b5ffb989dcfcc90'}
for name,want in pins.items():assert sha(HERE/name)==want,(name,sha(HERE/name),want)
ledger=json.loads((HERE/'source_ledger.json').read_text());future=json.loads((HERE/'future_dependencies.json').read_text());plan=json.loads((HERE/'held_schedule.json').read_text());hostiles=json.loads((HERE/'results_hostile_tests.json').read_text());assert ledger['selection']['selected_group_ids']==list(range(126,162)) and ledger['selection']['required_closed_union']==list(range(126)) and len(ledger['lanes'])==36 and sum(x['source_bytes'] for x in ledger['lanes'])==65177850
for lane in ledger['lanes']:source=HERE/lane['source_path'];assert source.is_file() and sha(source)==lane['source_sha256'] and source.stat().st_size==lane['source_bytes'] and lane['variables']==91 and lane['generators']==6577;text=source.read_text();assert text.count('ring r=0,')==text.count('ideal G=slimgb(I);')==text.count('poly remainder=reduce(1,G);')==text.count('quit;')==1
assert future['status']=='UNSATISFIED_THREE_NULL_HASH_PAIRS' and future['required_closed_union']==list(range(126)) and [d['groups_closed'] for d in future['dependencies']]==[list(range(1,26)),list(range(26,76)),list(range(76,126))] and all(d['manifest_sha256'] is d['result_sha256'] is None and d['satisfied'] is False for d in future['dependencies'])
for dep in future['dependencies']:assert not (ROOT/dep['manifest_path']).exists() and not (ROOT/dep['result_path']).exists()
runner=(HERE/'run_groups126_161.py').read_text();verifier=(HERE/'dependency_verifier.py').read_text();ast.parse(runner);ast.parse(verifier);assert runner.count('subprocess.Popen(')==1 and runner.index('verify_payload(')<runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")<runner.index('subprocess.Popen(')
for token in ('manifest.is_file() and result_path.is_file()','sha(manifest)==mh and sha(result_path)==rh','result_path.resolve() in listed',"result['schema']==dep['result_schema']", "result['status']==dep['result_status']", "result['groups_closed']==dep['groups_closed']"):assert token in verifier,token
assert hostiles['status']=='PASS_21_HOSTILES_ALL_THREE_FUTURES_ABSENT' and len(hostiles['tests'])==21 and all(hostiles['tests'].values()) and hostiles['solver_runs']==0
assert plan['status']=='HELD_THREE_FUTURE_PASSES_ABSENT_ZERO_RUN' and plan['execution']['order']==list(range(126,162)) and plan['execution']['maximum_lane_count']==36 and not any(plan['execution'][x] for x in ('parallel','skip','reorder','relaunch')) and plan['scope']['solver_launches']==plan['scope']['groups_newly_closed']==0
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):schema=json.loads((HERE/name).read_text());assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])
for absent in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (HERE/absent).exists(),absent
assert not list(HERE.rglob('*.tmp')) and not (HERE/'__pycache__').exists()
for rel,want in ledger['pins'].items():path=ROOT/rel;assert path.is_file() and sha(path)==want,(rel,sha(path),want)
m=HERE/'MANIFEST.sha256';checked=0
if m.exists():
 for line in m.read_text().splitlines():digest,name=line.split('  ',1);path=(HERE/name).resolve();assert path.is_file() and sha(path)==digest,name;checked+=1
print(json.dumps({'status':'PASS_FINAL_REP4_CONDITIONAL_HELD_ZERO_RUN','sources':36,'hostiles':21,'manifest_lines_checked':checked,'solver_runs':0},sort_keys=True))
