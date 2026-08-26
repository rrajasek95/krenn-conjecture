#!/usr/bin/env python3
"""Independent held-only referee for rep1 groups 88..137."""
from __future__ import annotations
import ast, copy, hashlib, json
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PKG=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25'
BASE=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25'
CENSUS=ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25'
CENSUS_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25'
PINS={
 PKG/'MANIFEST.sha256':'07ab0d198fc80b91025df7c892081f2aaaa94158014052246d7700095c054450',
 PKG/'source_ledger.json':'2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b',
 PKG/'normalize_future_dependency.py':'87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a',
 PKG/'results_adapter_tests.json':'c17c89dd1bcc535b30686c6f4ae69cb5fef2819592fcd3ef2d6dae762f403fbd',
 PKG/'run_groups88_137.py':'604b0b938389e44506d627eba8652d74cfe3d3ba10a932efcb6c4dbfeee987e5',
 PKG/'future_groups38_87_dependency.json':'1374fb5ed562ac0fd6b28ace616e09fbf011509555b02cb98996281d7188b380',
 BASE/'MANIFEST.sha256':'7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da',
 BASE/'normalized_next25_dependency.json':'29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76',
 CENSUS/'MANIFEST.sha256':'6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1',
 CENSUS/'results_canonical_census.json':'5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161',
 CENSUS_REF/'FINAL_MANIFEST.sha256':'f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a',
}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while c:=f.read(1<<20):h.update(c)
 return h.hexdigest()
def replay(manifest):
 count=0
 for line in manifest.read_text().splitlines():
  if not line.strip():continue
  expected,raw=line.split(None,1);p=Path(raw.strip())
  if not p.is_absolute():p=(ROOT/p).resolve() if raw.strip().startswith('computations/') else (manifest.parent/p).resolve()
  assert p.is_file() and sha(p)==expected,p;count+=1
 return count
for p,x in PINS.items():assert sha(p)==x,(p,sha(p),x)
manifest_counts={'package':replay(PKG/'MANIFEST.sha256'),'census':replay(CENSUS/'MANIFEST.sha256'),'census_referee':replay(CENSUS_REF/'FINAL_MANIFEST.sha256')}

base=json.loads((BASE/'normalized_next25_dependency.json').read_text());spec=json.loads((PKG/'future_groups38_87_dependency.json').read_text())
tests=json.loads((PKG/'results_adapter_tests.json').read_text())
expected_base=list(range(38));expected_future=list(range(38,88));expected_union=list(range(88))
good={'schema':spec['required_future_result_schema'],'status':spec['required_future_result_status'],'new_groups_closed':50,'strict_order':True,'parallel':False,'skipped':False,'relaunch':False,'groups_closed':expected_future}
def normalize(b,t,s):
 assert b['schema']=='KRENN_X5_REP1_NEXT50_NORMALIZED_NEXT25_DEPENDENCY_V2' and b['status']=='PASS_NORMALIZED_BASELINE_PLUS_NEXT25_TO_CLOSED_UNION_0_37'
 assert b['closed_union']==s['proven_baseline_closed_union']==expected_base and len(set(b['closed_union']))==38
 assert t['schema']==s['required_future_result_schema'] and t['status']==s['required_future_result_status']
 assert t['new_groups_closed']==50 and t['strict_order'] and not t['parallel'] and not t['skipped'] and not t['relaunch']
 assert t['groups_closed']==s['expected_future_groups_closed']==expected_future and len(set(t['groups_closed']))==50
 assert set(b['closed_union']).isdisjoint(t['groups_closed'])
 union=sorted(b['closed_union']+t['groups_closed']);assert union==s['required_closed_union']==expected_union
 return union
assert normalize(base,good,spec)==expected_union
hostiles={}
def reject(name,target,mut):
 b,t,s=copy.deepcopy(base),copy.deepcopy(good),copy.deepcopy(spec);mut({'baseline':b,'terminal':t,'spec':s}[target])
 try:normalize(b,t,s)
 except (AssertionError,KeyError,TypeError):hostiles[name]=True
 else:hostiles[name]=False
reject('baseline_missing','baseline',lambda x:x['closed_union'].pop())
reject('baseline_duplicate','baseline',lambda x:x['closed_union'].append(37))
reject('future_missing','terminal',lambda x:x['groups_closed'].pop())
reject('future_duplicate','terminal',lambda x:x['groups_closed'].append(87))
reject('future_extra','terminal',lambda x:x['groups_closed'].append(138))
reject('future_overlap','terminal',lambda x:x['groups_closed'].__setitem__(0,37))
reject('future_reordered','terminal',lambda x:x['groups_closed'].reverse())
reject('future_wrong_status','terminal',lambda x:x.__setitem__('status','WRONG'))
reject('future_skipped','terminal',lambda x:x.__setitem__('skipped',True))
reject('future_parallel','terminal',lambda x:x.__setitem__('parallel',True))
reject('future_relaunch','terminal',lambda x:x.__setitem__('relaunch',True))
reject('spec_union_extra','spec',lambda x:x['required_closed_union'].append(88))
assert len(hostiles)==12 and all(hostiles.values()) and tests['hostile_tests']==hostiles and tests['hostile_count']==12 and tests['solver_runs']==0

assert spec['status']=='UNSATISFIED_NULL_HASHES_BLOCK_LAUNCH' and spec['satisfied'] is False
assert spec['future_manifest_sha256'] is None and spec['future_result_sha256'] is None
future_manifest=ROOT/spec['future_manifest_path'];future_result=ROOT/spec['future_result_path']
assert not future_manifest.exists() and not future_result.exists()

ledger=json.loads((PKG/'source_ledger.json').read_text());lanes=ledger['lanes'];selected=list(range(88,138))
assert [x['group_id'] for x in lanes]==selected and [x['ordinal'] for x in lanes]==list(range(1,51))
census=json.loads((CENSUS/'results_canonical_census.json').read_text());records={x['group_id']:x for x in census['enumeration']['records']};assert sorted(records)==list(range(162))
total=0
for lane in lanes:
 rec=records[lane['group_id']];source=PKG/lane['source_path']
 assert lane['canonical_chart']==rec['canonical_chart'] and lane['source_sha256']==rec['exact_Q_source_sha256']
 assert lane['source_bytes']==rec['exact_Q_source_bytes'] and sha(source)==lane['source_sha256'] and source.stat().st_size==lane['source_bytes']
 assert lane['variables']==91 and lane['generators']==6577;total+=lane['source_bytes']
assert total==89_221_428

schedule=json.loads((PKG/'held_schedule.json').read_text());execution=schedule['execution']
assert execution['order']==selected and execution['maximum_lane_count']==50
assert execution['native_wall_seconds_each']==240 and execution['wrapper_wall_seconds_each']==250 and execution['rss_cap_bytes_each']==8*1024**3
assert execution['parallel'] is execution['skip'] is execution['reorder'] is execution['relaunch'] is False
assert execution['stop_whole_batch_on']==['NONUNIT','RESOURCE','PROCESS','SCHEMA_OR_TRANSCRIPT_MISMATCH']
runner=(PKG/'run_groups88_137.py').read_text();ast.parse(runner)
for token in ("SELECTED=tuple(range(88,138))","NATIVE_WALL=240","WRAPPER_WALL=250","RSS_CAP=8*1024**3","proc_listpgrppids","group_rss(process.pid,True)","normalized['closed_union']==list(range(88))","for lane in lanes:","if not unit:stop=","break","'parallel':False","'relaunch':False","exclusive(HERE/'BATCH_ATTEMPT.json'","atomic(HERE/'results'/"):
 assert token in runner,token
assert runner.count('subprocess.Popen(')==1
assert runner.index("assert manifest.is_file() and acceptance.is_file() and clearance.is_file()")<runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")<runner.index('subprocess.Popen(')
for absent in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
 assert not (PKG/absent).exists(),absent
assert not list(PKG.rglob('*.tmp'))

out={'schema':'KRENN_X5_REP1_GROUPS88_137_CONDITIONAL_HELD_REFEREE_V1','status':'PASS_CONDITIONAL_HELD_GROUPS88_137_BLOCKED_ZERO_RUNS','producer_manifest_sha256':PINS[PKG/'MANIFEST.sha256'],'source_ledger_sha256':PINS[PKG/'source_ledger.json'],'adapter_sha256':PINS[PKG/'normalize_future_dependency.py'],'runner_sha256':PINS[PKG/'run_groups88_137.py'],'baseline_closed_union':expected_base,'required_future_groups':expected_future,'derived_union_if_satisfied':expected_union,'dependency_satisfied':False,'future_hashes':[None,None],'future_files_present':False,'hostiles_passed':12,'selected_group_ids':selected,'canonical_sources_verified':50,'total_source_bytes':total,'limits_each':{'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3},'strict_sequential_stop_first':True,'manifest_counts':manifest_counts,'scope':{'held_approval_only':True,'launch_authorized':False,'solver_runs':0,'mathematical_coverage':False,'rep1_representative_closed':False}}
approval={'schema':'KRENN_X5_REP1_GROUPS88_137_CONDITIONAL_HELD_APPROVAL_NOT_EXECUTOR_ACCEPTANCE_V1','status':'PASS_HELD_ONLY_BLOCKED_ON_EXACT_GROUPS38_87_TERMINAL_BINDING','producer_manifest_sha256':PINS[PKG/'MANIFEST.sha256'],'dependency_spec_sha256':PINS[PKG/'future_groups38_87_dependency.json'],'future_terminal_manifest_sha256':None,'future_terminal_result_sha256':None,'launch_authorized':False,'solver_runs':0}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(HERE/'HELD_APPROVAL.json').write_text(json.dumps(approval,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'result_sha256':sha(HERE/'results_referee.json')},sort_keys=True))
