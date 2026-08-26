#!/usr/bin/env python3
"""Independent exact replay of the smallest67 factor cover and determinant census."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations';PARENT=C/'unaudited-codex-n8-x5-rep5-smallest70-global-three-torus-reduction-design-2026-08-26';SOURCE=PARENT/'sources/chart_a04_200_a04_210_a04_220_Q_design.sing';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();result=json.loads((HERE/'results_design.json').read_text());pivot=result['selected_cover']['selected_coordinate'];inverse='inv_factor_pivot'
def split(path):
 t=path.read_text();n=t.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');b=t.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return n,b.split(',\n')
names,_=split(SOURCE);universe=names+[inverse];index={x:i for i,x in enumerate(universe)}
def parse(path):
 ring,expr=split(path);out=[]
 for e in expr:
  p={}
  for raw in re.findall(r'[+-]?[^+-]+',e):
   s=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');c=s
   if parts[0].isdigit():c*=int(parts.pop(0))
   m=tuple(sorted(index[x] for x in parts if x));p[m]=p.get(m,0)+c
  p={m:c for m,c in p.items() if c};assert p;out.append(p)
 return ring,out
def canonical(values):
 out=[];seen=set()
 for p in values:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  key=tuple(sorted(p.items()))
  if key not in seen:seen.add(key);out.append(p)
 return out
ring,polys=parse(SOURCE);x=index[pivot];divided=[];count=0
for p in polys:
 if all(x in m for m in p):
  count+=1;q={}
  for m,c in p.items():w=list(m);w.remove(x);q[tuple(w)]=c
  divided.append(q)
 else:divided.append(p)
Drec=next(s for s in result['selected_cover']['sources'] if s['kind']=='D');Vrec=next(s for s in result['selected_cover']['sources'] if s['kind']=='V');Dnames,D=parse(HERE/Drec['path']);Vnames,V=parse(HERE/Vrec['path']);expected_D=canonical(divided+[{():1,tuple(sorted((x,index[inverse]))):-1}]);zero=[]
for p in polys:
 q={m:c for m,c in p.items() if x not in m};zero.append(q)
expected_V=canonical(zero);assert count==54 and D==expected_D and V==expected_V and Dnames==names+[inverse] and Vnames==[n for n in names if n!=pivot] and sha(HERE/Drec['path'])==Drec['sha256'] and sha(HERE/Vrec['path'])==Vrec['sha256']
det=result['determinant_rank_split'];assert det['complete_3x3_blocks']==['a12','a15','a24','a67'] and det['two_by_two_minors']==36 and det['three_by_three_determinants']==4 and len(det['candidate_ledger'])==40 and all(not x['exact_generator_up_to_sign'] and x['divisible_generators']==0 and not x['constant_or_monomial'] for x in det['candidate_ledger'])
hostiles=json.loads((HERE/'results_hostiles.json').read_text());assert hostiles['status']=='PASS_19_HOSTILES' and len(hostiles['tests'])==19 and all(hostiles['tests'].values()) and hostiles['solver_runs']==0
out={'schema':'KRENN_X5_REP5_SMALLEST67_FACTOR_DETERMINANT_REFEREE_V1','status':'PASS_EXACT_STRICT_FACTOR_COVER_DESIGN_ONLY','producer_result_sha256':sha(HERE/'results_design.json'),'input_sha256':sha(SOURCE),'exact_tests':{'grading_rank_nullity':[67,0],'linear_rank_over_Q':40,'inactive':0,'unit_monic':0,'components':[67],'minor_determinant_candidates':40,'literal_minor_factors':0},'cover':{'coordinate':pivot,'divided_generators':54,'D_sha256':Drec['sha256'],'V_sha256':Vrec['sha256'],'forward_reverse_exact':True,'root_free':True,'exhaustive':True},'hostiles':19,'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'coordinate':pivot,'minor_tests':40,'hostiles':19,'solves':0},sort_keys=True))
