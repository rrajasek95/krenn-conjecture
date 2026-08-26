#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_promotion_audit.json').read_text())
assert r['status']=='PASS_ALL_RANK1_ORBITS_EXACT_Q_CLOSED_ACROSS_12_RECTANGLE_RECORDS' and r['exact_Q_orbits']==[0,1,2,3,4]
assert r['canonical_record_orbit_cases']==60 and r['raw_chart_record_cases']==324 and r['A12_lifts']['both_lifts_closed']
assert r['scope']=={'rank1_rectangle12_closed':True,'rank2_closed':False,'nonrectangle_records_excluded':[12,13,14,15],'full_conjecture':False,'new_solver_runs':0}
print(json.dumps({'status':'PASS','result_sha256':h(H/'results_promotion_audit.json')},sort_keys=True))
