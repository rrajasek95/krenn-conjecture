#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_design.json').read_text());q=json.loads((H/'results_referee.json').read_text());h=json.loads((H/'results_hostiles.json').read_text());assert r['status']=='PASS_EXACT_STRICT_FACTOR_COVER_NO_LITERAL_DETERMINANT_REDUCTION' and q['status']=='PASS_EXACT_STRICT_FACTOR_COVER_DESIGN_ONLY' and len(r['selected_cover']['sources'])==2
for x in r['selected_cover']['sources']:p=H/x['path'];assert p.is_file() and sha(p)==x['sha256']
assert h['status']=='PASS_19_HOSTILES' and len(h['tests'])==19 and all(h['tests'].values()) and r['scope']['singular_runs']==0
tree=ast.parse((H/'build_design.py').read_text());assert not any(isinstance(x,(ast.Import,ast.ImportFrom)) and any(a.name=='subprocess' for a in x.names) for x in ast.walk(tree));assert not list(H.glob('*.tmp')) and not list(H.rglob('__pycache__'));print(json.dumps({'status':'PASS_DESIGN_VALIDATED','sources':2,'hostiles':19,'solves':0},sort_keys=True))
