#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
def s(p):return hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads((H/'results_design.json').read_text());assert x['status']=='PASS_STRICT_SMALLER_EXACT_THREE_CHART_DESIGN_ZERO_SOLVES'
assert x['reduction']['variables']==88 and x['reduction']['generators']==6574
assert x['scope']=={'design_inputs_materialized':3,'solver_runs':0,'parent_relaunched':False,'mathematical_coverage':False,'rep5_closed':False}
assert x['proof']['chart_union']=='three k charts cover the full original p00 chart; no symmetry identification is assumed'
assert len(x['inputs'])==3 and [q['pivot_k'] for q in x['inputs']]==[0,1,2]
for q in x['inputs']:
 p=H/q['path'];assert s(p)==q['sha256'] and p.stat().st_size==q['bytes'];t=p.read_text()
 assert t.count('ring r=0,')==t.count('ideal G=slimgb(I);')==t.count('poly remainder=reduce(1,G);')==t.count('quit;')==1
 assert 'INPUT_VARIABLES=' in t and 'INPUT_GENERATORS=' in t
assert not any(H.glob('*.tmp'))
print(json.dumps({'status':'PASS_EXACT_DESIGN_ZERO_SOLVES','inputs':[(q['pivot_k'],q['sha256']) for q in x['inputs']],'variables':88,'generators':6574},sort_keys=True))
