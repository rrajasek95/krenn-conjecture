#!/usr/bin/env python3
"""Independent flat-polynomial replay of all four further-cover sources."""
from __future__ import annotations
import hashlib,json,re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations';PARENT=C/'unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-2026-08-26';OPEN=PARENT/'sources/stage0_a37_201_Q_design.sing';CLOSED=PARENT/'sources/stage1_a37_200_closed_Q_design.sing';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def split(path):
 text=path.read_text();names=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');body=text.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return names,body.split(',\n')
open_names,_=split(OPEN);universe=open_names+['inv_a04_20'];index={x:i for i,x in enumerate(universe)}
def parse(path):
 names,expressions=split(path);polys=[]
 for expression in expressions:
  polynomial={}
  for raw in re.findall(r'[+-]?[^+-]+',expression):
   sign=-1 if raw.startswith('-') else 1;raw=raw.lstrip('+-');parts=raw.split('*');coefficient=sign
   if parts[0].isdigit():coefficient*=int(parts.pop(0))
   monomial=tuple(sorted(index[x] for x in parts if x));polynomial[monomial]=polynomial.get(monomial,0)+coefficient
  polynomial={m:c for m,c in polynomial.items() if c};assert polynomial;polys.append(polynomial)
 return names,polys
def canonical(polys):
 out=[];seen=set()
 for p in polys:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  key=tuple(sorted(p.items()))
  if key not in seen:seen.add(key);out.append(p)
 return out
def specialize(polys,coordinate,value):
 out=[]
 for p in polys:
  q={}
  for m,c in p.items():
   if value==0 and coordinate in m:continue
   n=tuple(i for i in m if not(value==1 and i==coordinate));q[n]=q.get(n,0)+c
  out.append(q)
 return canonical(out)
open_ring,open_polys=parse(OPEN);closed_ring,closed_polys=parse(CLOSED);assert open_ring==closed_ring==open_names and len(open_polys)==len(closed_polys)==6561
result=json.loads((HERE/'results_design.json').read_text());assert result['status']=='PASS_EXACT_FURTHER_COVERS_BOTH_PARENT_BRANCHES'
records=result['open_q1_factor_localization']['sources']+result['closed_q0_residual_torus']['sources']
paths=[HERE/x['path'] for x in records];assert all(sha(p)==x['sha256'] for p,x in zip(paths,records))
names_D,actual_D=parse(paths[0]);names_V,actual_V=parse(paths[1]);x=index['a04_20'];divided=[];count=0
for p in open_polys:
 if all(x in m for m in p):
  count+=1;q={}
  for m,c in p.items():work=list(m);work.remove(x);q[tuple(work)]=c
  divided.append(q)
 else:divided.append(p)
expected_D=canonical(divided+[{():1,tuple(sorted((x,index['inv_a04_20']))):-1}]);expected_V=specialize(open_polys,x,0)
assert count==486 and actual_D==expected_D and actual_V==expected_V;assert names_D==open_names+['inv_a04_20'] and names_V==[n for n in open_names if n!='a04_20']
factor_coordinates=[]
for coordinate,name in enumerate(open_names):
 count_here=sum(all(coordinate in m for m in p) for p in open_polys)
 if count_here:factor_coordinates.append([name,count_here])
assert factor_coordinates==[['a04_20',486],['a04_21',486],['a04_22',486]]
closed_coordinate=index[result['closed_q0_residual_torus']['selected_coordinate']];names_CD,actual_CD=parse(paths[2]);names_CV,actual_CV=parse(paths[3]);assert actual_CD==specialize(closed_polys,closed_coordinate,1) and actual_CV==specialize(closed_polys,closed_coordinate,0);assert names_CD==names_CV==[n for n in closed_ring if n!=result['closed_q0_residual_torus']['selected_coordinate']]
weights={index[k]:v for k,v in result['closed_q0_residual_torus']['primitive_weights'].items()}
rows=[]
for p in closed_polys:
 ms=sorted(p);base=Counter(ms[0]);target=sum(weights.get(i,0)*n for i,n in base.items())
 for m in ms[1:]:
  now=Counter(m);assert sum(weights.get(i,0)*n for i,n in now.items())==target;row={i:base[i]-now[i] for i in set(base)|set(now) if base[i]!=now[i]}
  if row:rows.append(row)
def rank_mod(rows,prime):
 e={}
 for raw in rows:
  r={k:v%prime for k,v in raw.items() if v%prime}
  while r:
   p=min(r)
   if p not in e:
    inv=pow(r[p],-1,prime);e[p]={k:v*inv%prime for k,v in r.items()};break
   f=r[p];known=e[p];r={k:(r.get(k,0)-f*known.get(k,0))%prime for k in set(r)|set(known)};r={k:v for k,v in r.items() if v}
 return len(e)
assert [rank_mod(rows,p) for p in (32003,65521)]==[71,71]
hostiles=json.loads((HERE/'results_hostiles.json').read_text());assert hostiles['status']=='PASS_16_HOSTILES' and len(hostiles['tests'])==16 and all(hostiles['tests'].values()) and hostiles['solver_runs']==0
out={'schema':'KRENN_X5_REP5_SELECTED72_BOTH_BRANCH_FURTHER_REDUCTION_REFEREE_V1','status':'PASS_EXACT_FOUR_SUBCHART_COVER_DESIGN_ONLY','producer_result_sha256':sha(HERE/'results_design.json'),'producer_manifest_pending':True,'open_q1':{'factor_coordinates':factor_coordinates,'selected':'a04_20','divided_generators':486,'D_source_sha256':sha(paths[0]),'V_source_sha256':sha(paths[1]),'D_identity_replayed':True,'V_identity_replayed':True},'closed_q0':{'grading_modular_ranks':[71,71],'explicit_nonzero_weight_nullvector':result['closed_q0_residual_torus']['primitive_weights'],'selected':result['closed_q0_residual_torus']['selected_coordinate'],'D_source_sha256':sha(paths[2]),'V_source_sha256':sha(paths[3]),'D_identity_replayed':True,'V_identity_replayed':True},'combined':{'parent_branches':2,'subcharts':4,'exhaustive':True,'root_free':True,'direct_parent_implication':False},'hostiles':16,'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'subcharts':4,'hostiles':16,'solves':0},sort_keys=True))
