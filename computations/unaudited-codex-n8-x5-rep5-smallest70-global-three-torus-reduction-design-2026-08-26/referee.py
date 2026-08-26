#!/usr/bin/env python3
"""Independent replay of the maximal residual three-torus cover."""
from __future__ import annotations
import hashlib,itertools,json,re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations';PARENT=C/'unaudited-codex-n8-x5-rep5-four-subchart-next-symbolic-reduction-design-2026-08-26';SOURCE=PARENT/'sources/closed_V35_21_V_a35_22_Q_design.sing';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def split(path):
 t=path.read_text();n=t.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');b=t.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return n,b.split(',\n')
names,_=split(SOURCE);index={x:i for i,x in enumerate(names)}
def parse(path):
 ring,expr=split(path);out=[]
 for e in expr:
  p={}
  for raw in re.findall(r'[+-]?[^+-]+',e):
   sign=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');c=sign
   if parts[0].isdigit():c*=int(parts.pop(0))
   m=tuple(sorted(index[x] for x in parts if x));p[m]=p.get(m,0)+c
  p={m:c for m,c in p.items() if c};assert p;out.append(p)
 return ring,out
ring,polys=parse(SOURCE);torus_names=['a04_20','a04_21','a04_22'];torus=[index[x] for x in torus_names]
def canonical(values):
 out=[];seen=set()
 for p in values:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  key=tuple(sorted(p.items()))
  if key not in seen:seen.add(key);out.append(p)
 return out
def specialize(assignments):
 zero={i for i,v in assignments.items() if v==0};one=set(assignments)-zero;out=[]
 for p in polys:
  q={}
  for m,c in p.items():
   if zero.intersection(m):continue
   n=tuple(i for i in m if i not in one);q[n]=q.get(n,0)+c
  out.append(q)
 return canonical(out)
result=json.loads((HERE/'results_design.json').read_text());assert result['status']=='PASS_EXACT_MAXIMAL_THREE_TORUS_EIGHT_CHART_COVER';records=result['three_torus_cover']['sources'];assert [x['bits'] for x in records]==[list(x) for x in itertools.product((0,1),repeat=3)]
for record in records:
 path=HERE/record['path'];out_names,out=parse(path);assignments={i:v for i,v in zip(torus,record['bits'])};assert out==specialize(assignments) and out_names==[x for x in names if x not in torus_names] and sha(path)==record['sha256'];body=path.read_text().split('ideal I=',1)[1];assert all(not re.search(rf'\b{re.escape(x)}\b',body) for x in torus_names)
rows=[]
for p in polys:
 ms=sorted(p);base=Counter(ms[0])
 for coordinate in torus:assert len({m.count(coordinate) for m in ms})==1
 for m in ms[1:]:
  now=Counter(m);row={i:base[i]-now[i] for i in set(base)|set(now) if base[i]!=now[i]}
  if row:rows.append(row)
def rank(rows,prime):
 e={}
 for raw in rows:
  r={k:v%prime for k,v in raw.items() if v%prime}
  while r:
   p=min(r)
   if p not in e:
    inv=pow(r[p],-1,prime);e[p]={k:v*inv%prime for k,v in r.items()};break
   f=r[p];known=e[p];r={k:(r.get(k,0)-f*known.get(k,0))%prime for k in set(r)|set(known)};r={k:v for k,v in r.items() if v}
 return len(e)
assert [rank(rows,p) for p in (32003,65521)]==[67,67];hostiles=json.loads((HERE/'results_hostiles.json').read_text());assert hostiles['status']=='PASS_18_HOSTILES' and len(hostiles['tests'])==18 and all(hostiles['tests'].values()) and hostiles['solver_runs']==0
out={'schema':'KRENN_X5_REP5_SMALLEST70_GLOBAL_THREE_TORUS_REFEREE_V1','status':'PASS_EXACT_MAXIMAL_THREE_TORUS_EIGHT_CHART_DESIGN_ONLY','producer_result_sha256':sha(HERE/'results_design.json'),'input_sha256':sha(SOURCE),'grading':{'modular_ranks':[67,67],'rank_over_Q':67,'nullity_over_Q':3,'explicit_independent_unit_vectors':torus_names},'source_replay':{'charts':8,'all_exact_specializations':True,'all_67_variables':True,'all_removed_identifiers_absent':True},'cover':{'identity':'product_i (D(x_i) union V(x_i))','root_free':True,'exhaustive':True,'forward_reverse_exact':True},'hostiles':18,'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'charts':8,'rank':[67,3],'hostiles':18,'solves':0},sort_keys=True))
