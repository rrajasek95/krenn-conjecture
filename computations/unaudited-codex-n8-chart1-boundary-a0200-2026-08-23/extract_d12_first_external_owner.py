#!/usr/bin/env python3
"""Extract the lex-first exact counterowner to r13 shell privacy."""

from collections import defaultdict
from fractions import Fraction
import importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
S=load(HERE/'run_d12_lazy_cegar.py','boundary_external_owner_source')
p=S.Provider(); P=1_073_741_827
checkpoint=json.loads((HERE/'checkpoint_d12_incremental_cegar.json').read_text())
selected={(int(c),bytes.fromhex(m)) for c,m in checkpoint['column_insertion_sequence']}

def orbit(row):
 return tuple(sorted(set(bytes(sorted(t[v] for v in row)) for t in p.transforms)))
def entries(column):
 a=defaultdict(int)
 for code,mult in p.column_orbit(column):
  for term,coefficient in p.generator(code).items():
   row=bytes(sorted(mult+term))
   if row==orbit(row)[0]: a[row]+=coefficient
 return {r:v for r,v in a.items() if v}
def lift(v):
 values={Fraction(n,d) for d in range(1,65) for n in range(-64,65)
         if n*pow(d,-1,P)%P==v}
 assert len(values)==1; return values.pop()
dual={bytes.fromhex(r):lift(int(v)) for r,v in checkpoint['last_modular_dual']}
candidates=p.incident_columns(dual)
pending=[]; outputs=[]
for col in sorted(candidates):
 e=entries(col); q=sum(Fraction(a)*dual.get(r,0) for r,a in e.items())
 if q and col not in selected: pending.append(col); outputs.append(e)
assert len(candidates)==1204 and len(pending)==1186
count=defaultdict(int)
for e in outputs:
 for row in e: count[row]+=1
answer=None
for col,e in zip(pending,outputs):
 for row in sorted(e,key=lambda r:(-len(r),r)):
  if count[row]!=1 or p.target_coefficient(row)!=0: continue
  incident=p.incident_columns_for_row(row)
  if any(owner in selected for owner in incident): continue
  external=[owner for owner in incident if owner!=col]
  if not external: continue
  owner=external[0]; oe=entries(owner)
  assert row in oe
  answer={
   'format':'n8-chart1-boundary-d12-first-external-owner-v1',
   'shell_column':[col[0],col[1].hex()],'shell_coefficient':e[row],
   'shell_private_row':row.hex(),'target_coefficient':0,
   'full_incident_column_orbits':[[c,m.hex()] for c,m in incident],
   'external_column':[owner[0],owner[1].hex()],
   'external_coefficient':oe[row],
   'external_is_selected':owner in selected,
   'incident_count':len(incident),
  }; break
 if answer: break
assert answer
(HERE/'results_d12_first_external_owner.json').write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
print(json.dumps(answer,sort_keys=True))
