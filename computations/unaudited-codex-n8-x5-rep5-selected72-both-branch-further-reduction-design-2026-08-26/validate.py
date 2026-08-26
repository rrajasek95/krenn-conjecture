#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_design.json').read_text());h=json.loads((H/'results_hostiles.json').read_text());q=json.loads((H/'results_referee.json').read_text())
assert r['status']=='PASS_EXACT_FURTHER_COVERS_BOTH_PARENT_BRANCHES' and r['combined_cover']['subcharts']==4 and r['combined_cover']['every_parent_point_covered'];assert len(r['open_q1_factor_localization']['sources'])==len(r['closed_q0_residual_torus']['sources'])==2
for source in r['open_q1_factor_localization']['sources']+r['closed_q0_residual_torus']['sources']:
 p=H/source['path'];assert p.is_file() and sha(p)==source['sha256']
assert h['status']=='PASS_16_HOSTILES' and len(h['tests'])==16 and all(h['tests'].values());assert r['scope']['singular_runs']==0 and r['scope']['mathematical_coverage_added'] is False
assert q['status']=='PASS_EXACT_FOUR_SUBCHART_COVER_DESIGN_ONLY' and q['combined']['subcharts']==4 and q['scope']['singular_runs']==0
tree=ast.parse((H/'build_design.py').read_text());assert not any(isinstance(x,(ast.Import,ast.ImportFrom)) and any(a.name=='subprocess' for a in x.names) for x in ast.walk(tree));assert not list(H.glob('*.tmp')) and not list(H.rglob('__pycache__'))
print(json.dumps({'status':'PASS_DESIGN_VALIDATED','sources':4,'hostiles':16,'solves':0},sort_keys=True))
