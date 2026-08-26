#!/usr/bin/env python3
"""Validate source derivation and held single-lane refusal contract without execution."""
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((HERE/'source_derivation.json').read_text());h=json.loads((HERE/'held_pilot.json').read_text())
assert sha(HERE/'source_derivation.json')=='194eabb95c628649489f232207a784092a7c5ff040ec82a98ff8ac18bdc6f411'
assert sha(HERE/'rep5_rank2_k2_t1_p32003.sing')=='fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a'
assert sha(HERE/'run_one_lane.py')=='e459c779d54b93e58166b639ed29e0aa4e79b69b1366e65dc05b948381473ec7'
assert d['status']=='PASS_DETERMINISTIC_SOURCE_DERIVATION_ZERO_RUN' and d['selection']['all_six_tied_on_first_three_metrics'] is True
c=d['selection']['candidates'];assert len(c)==6 and d['selection']['selected']==sorted(c,key=lambda x:(x['bytes'],x['generators'],x['factored_operator_tokens'],x['source_sha256']))[0]
assert (d['selection']['selected']['pivot_k'],d['selection']['selected']['t_open'])==(2,1)
assert d['prior_consumed_k0']['attempt_consumed'] is True and d['prior_consumed_k0']['source_reused'] is d['prior_consumed_k0']['relaunch_authorized'] is False
q=ROOT/d['derivation']['Q_path'];p=HERE/d['derivation']['p_path'];qt=q.read_text();pt=p.read_text();assert pt.replace('ring r=32003,(','ring r=0,(',1)==qt
for token in ('ideal G=slimgb(I);','poly remainder=reduce(1,G);','GROEBNER_SIZE=','UNIT_REMAINDER=','STATUS=UNIT_IDEAL','STATUS=NONUNIT_OR_UNRESOLVED'):assert qt.count(token)==pt.count(token)==1
assert h['status']=='HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE' and h['execution']=={'maximum_lane_count':1,'native_wall_seconds':300,'wrapper_wall_seconds':315,'rss_cap_bytes':8589934592,'direct_libproc_group_rss':True,'fresh_libproc_process_census':True,'atomic_result':True,'strict_stop_after_any_outcome':True}
assert h['authorization']=={'independent_acceptance_present':False,'fresh_clearance_present':False,'exact_Q_authorized':False,'other_stratum_authorized':False,'automatic_relaunch_authorized':False}
runner=(HERE/'run_one_lane.py').read_text();compile(runner,str(HERE/'run_one_lane.py'),'exec')
for token in ('proc_listallpids','proc_pidpath','proc_listpgrppids','proc_pid_rusage','NATIVE_WALL = 300','WRAPPER_WALL = 315','RSS_CAP = 8 * 1024**3','MAX_CLEARANCE_LIFETIME_SECONDS = 600','RUN_EXCLUSIVE.lock','exclusive_json(HERE / "ATTEMPT.json"','atomic_json(HERE / "result.json"','prior_consumed_k0_reused'):assert token in runner,token
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 s=json.loads((HERE/name).read_text());assert s['additionalProperties'] is False and set(s['required'])==set(s['properties'])
for absent in ('independent_referee_acceptance.json','launch_clearance.json','RUN_EXCLUSIVE.lock','ATTEMPT.json','result.json','stdout.log','stderr.log','watchdog.json'):assert not (HERE/absent).exists(),absent
assert not list(HERE.glob('*.tmp'))
for relative,expected in d['pins'].items():path=ROOT/relative;assert path.is_file() and sha(path)==expected
m=HERE/'MANIFEST.sha256';checked=0
if m.exists():
 for line in m.read_text().splitlines():digest,name=line.split('  ',1);path=(HERE/name).resolve();assert path.is_file() and sha(path)==digest,name;checked+=1
print(json.dumps({'status':'PASS_HELD_ZERO_RUN','selected':[2,1],'variables':84,'generators':6562,'manifest_lines_checked':checked,'solver_runs':0},sort_keys=True))
