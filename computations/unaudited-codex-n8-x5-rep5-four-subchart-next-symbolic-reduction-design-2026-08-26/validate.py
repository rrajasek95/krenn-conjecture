#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_design.json').read_text());h=json.loads((H/'results_hostiles.json').read_text());q=json.loads((H/'results_referee.json').read_text());assert r['status']=='PASS_EXACT_NEXT_REDUCTION_ON_ALL_FOUR_BRANCHES' and r['combined']['input_branches']==4 and r['combined']['output_subcharts']==8
sources=[s for x in r['factor_localizations'] for s in x['sources']]+r['residual_torus']['sources'];assert len(sources)==8
for s in sources:p=H/s['path'];assert p.is_file() and sha(p)==s['sha256']
assert h['status']=='PASS_20_HOSTILES' and len(h['tests'])==20 and all(h['tests'].values()) and r['scope']['singular_runs']==0 and r['scope']['mathematical_coverage_added'] is False
assert q['status']=='PASS_EXACT_EIGHT_SUBCHART_REFINEMENT_DESIGN_ONLY' and q['combined']['inputs']==4 and q['combined']['outputs']==8 and q['scope']['singular_runs']==0
tree=ast.parse((H/'build_design.py').read_text());assert not any(isinstance(x,(ast.Import,ast.ImportFrom)) and any(a.name=='subprocess' for a in x.names) for x in ast.walk(tree));assert not list(H.glob('*.tmp')) and not list(H.rglob('__pycache__'));print(json.dumps({'status':'PASS_DESIGN_VALIDATED','sources':8,'hostiles':20,'solves':0},sort_keys=True))
