#!/usr/bin/env python3
import copy,hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,l,c):
 assert p['status']=='HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT_AND_CLEARANCE' and c['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81} and c['closed_group_identification']['group_id']==0 and c['closed_group_identification']['source_sha256']=='c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019';assert l['selection']['excluded_proven_group_ids']==[0] and l['selection']['selected_group_ids']==list(range(1,26)) and [x['group_id'] for x in l['lanes']]==list(range(1,26));assert p['execution']['order']==list(range(1,26)) and p['execution']['native_wall_seconds_each']==240 and p['execution']['wrapper_wall_seconds_each']==250 and p['execution']['rss_cap_bytes_each']==8589934592 and not any(p['execution'][x] for x in ('parallel','skip','reorder','relaunch'));assert p['scope']['representative']=='rep4 only' and p['scope']['solver_launches']==0 and p['scope']['cross_representative_transport'] is False
p=json.loads((HERE/'held_schedule.json').read_text());l=json.loads((HERE/'source_ledger.json').read_text());c=json.loads((HERE/'canonical_census.json').read_text());check(p,l,c);tests={}
for name,mut in {'closed_group':lambda p,l,c:c['closed_group_identification'].__setitem__('group_id',1),'closed_source':lambda p,l,c:c['closed_group_identification'].__setitem__('source_sha256','0'*64),'extra_exclusion':lambda p,l,c:l['selection']['excluded_proven_group_ids'].append(1),'missing_lane':lambda p,l,c:l['lanes'].pop(),'reorder':lambda p,l,c:l['lanes'].reverse(),'parallel':lambda p,l,c:p['execution'].__setitem__('parallel',True),'wall':lambda p,l,c:p['execution'].__setitem__('native_wall_seconds_each',241),'rss':lambda p,l,c:p['execution'].__setitem__('rss_cap_bytes_each',8589934593),'cross_rep':lambda p,l,c:p['scope'].__setitem__('cross_representative_transport',True),'run':lambda p,l,c:p['scope'].__setitem__('solver_launches',1)}.items():
 pp,ll,cc=copy.deepcopy(p),copy.deepcopy(l),copy.deepcopy(c);mut(pp,ll,cc)
 try:check(pp,ll,cc)
 except (AssertionError,KeyError,TypeError):tests[name]=True
 else:tests[name]=False
assert len(tests)==10 and all(tests.values());r={'schema':'KRENN_X5_REP4_FIRST25_HOSTILES_V1','status':'PASS_10_HOSTILES_ZERO_RUN','tests':tests,'plan_sha256':sha(HERE/'held_schedule.json'),'ledger_sha256':sha(HERE/'source_ledger.json'),'census_sha256':sha(HERE/'canonical_census.json'),'solver_runs':0};t=HERE/'results_hostile_tests.json.tmp';t.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');os.replace(t,HERE/'results_hostile_tests.json');print(json.dumps({'status':r['status'],'tests':10},sort_keys=True))
