#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_referee.json').read_text());p=json.loads((H/'HELD_PILOT_PLAN.json').read_text())
assert r['status']=='PASS_EXACT_DESIGN_AND_HELD_SMALLEST_PILOT_NO_SOLVE' and r['word_checks']==157464 and r['factorization_words']==6561
assert r['symmetry']['literal_classes']==[[12,13],[14,15]] and r['symmetry']['reduced_class']==[[12,13,14,15]] and r['symmetry']['A12_inactive']
assert all(x['all']==728 and x['triangle']==560 and x['star']==168 for x in r['carrier_census'].values())
assert r['full_x5']=={'variables':81,'generators':6561} and r['rank_design']['rank0']=='CLOSED_BY_ZERO_RESPONSE_MAP'
assert r['rank_design']['rank1']=={'variables':85,'generators':6568,'raw':27,'orbits':5,'solved':False} and r['rank_design']['rank2']=={'variables':89,'generators':6568,'raw':27,'orbits':5,'solved':False} and r['rank_design']['rank3']=={'variables':82,'generators':6562,'solved':False}
assert r['scope']=={'solver_runs':0,'closed_full_records':0,'rank0_branch_closed':True,'rank1_rank2_rank3_closed':False,'full_conjecture':False}
assert p['status']=='HELD_ZERO_RUNS_REQUIRES_CLEARANCE' and not p['execution']['launch_authorized'] and p['execution']['solver_runs']==0 and not p['execution']['stage2_automatic']
print(json.dumps({'status':'PASS','result_sha256':h(H/'results_referee.json'),'pilot_sha256':h(H/'HELD_PILOT_PLAN.json')},sort_keys=True))
