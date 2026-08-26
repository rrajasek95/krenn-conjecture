#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((H/'results_design.json').read_text());r=json.loads((H/'results_referee.json').read_text());h=json.loads((H/'results_hostiles.json').read_text())
assert d['status']=='PASS_EXACT_THIRD_FACTOR_COVER_NO_TORUS_MONIC_OR_LITERAL_MINOR_REDUCTION' and r['status']=='PASS_EXACT_THIRD_FACTOR_COVER_DESIGN_ONLY' and r['design_sha256']==sha(H/'results_design.json')
assert r['input_sha256']==d['input']['sha256']=='4cd663b6d7861c52681d42a6bc8ebaa4d8d77228e7e8aa4b4e9d3dbb1fdfd4bf' and r['coordinate']=='a24_10' and r['factor_count']==162
assert r['source_sizes']=={'D':[66,3484,128233],'V':[64,3321,118979]} and r['grading_rank']==65 and r['linear_rank']==38 and r['minor_tests']==45 and r['nine_stratum_ledger_preserved']
for kind,digest in r['source_hashes'].items():assert sha(H/f'sources/{kind}_a24_10_Q_design.sing')==digest
assert h['status']=='PASS_20_HOSTILES' and all(h['tests'].values()) and d['scope']['singular_runs']==r['singular_runs']==0 and not d['scope']['mathematical_coverage_added'] and not r['closure_added']
print(json.dumps({'status':'PASS_DESIGN_VALIDATED','sources':2,'hostiles':20,'solves':0},sort_keys=True))
