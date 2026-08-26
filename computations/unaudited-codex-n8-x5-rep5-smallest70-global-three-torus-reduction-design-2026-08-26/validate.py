#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_design.json').read_text());q=json.loads((H/'results_referee.json').read_text());h=json.loads((H/'results_hostiles.json').read_text());assert r['status']=='PASS_EXACT_MAXIMAL_THREE_TORUS_EIGHT_CHART_COVER' and q['status']=='PASS_EXACT_MAXIMAL_THREE_TORUS_EIGHT_CHART_DESIGN_ONLY' and len(r['three_torus_cover']['sources'])==8
for x in r['three_torus_cover']['sources']:p=H/x['path'];assert p.is_file() and sha(p)==x['sha256'] and x['variables']==67
assert h['status']=='PASS_18_HOSTILES' and len(h['tests'])==18 and all(h['tests'].values()) and r['scope']['singular_runs']==0 and r['scope']['held_modular_plan_needed'] is False
tree=ast.parse((H/'build_design.py').read_text());assert not any(isinstance(x,(ast.Import,ast.ImportFrom)) and any(a.name=='subprocess' for a in x.names) for x in ast.walk(tree));assert not list(H.glob('*.tmp')) and not list(H.rglob('__pycache__'));print(json.dumps({'status':'PASS_DESIGN_VALIDATED','charts':8,'hostiles':18,'solves':0},sort_keys=True))
