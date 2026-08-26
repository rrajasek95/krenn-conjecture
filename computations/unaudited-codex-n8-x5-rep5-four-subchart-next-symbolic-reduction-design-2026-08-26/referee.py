#!/usr/bin/env python3
"""Independent exact replay of the four-to-eight symbolic refinement."""
from __future__ import annotations
import hashlib,json,re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations';PARENT=C/'unaudited-codex-n8-x5-rep5-selected72-both-branch-further-reduction-design-2026-08-26'
INPUTS={'closed_D35_21':PARENT/'sources/closed_q0_D_a35_21_Q_design.sing','closed_V35_21':PARENT/'sources/closed_q0_V_a35_21_Q_design.sing','open_D04_20':PARENT/'sources/open_q1_D_a04_20_Q_design.sing','open_V04_20':PARENT/'sources/open_q1_V_a04_20_Q_design.sing'};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def split(path):
 t=path.read_text();n=t.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');b=t.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return n,b.split(',\n')
universe=[]
for p in list(INPUTS.values())+sorted((HERE/'sources').glob('*.sing')):
 for x in split(p)[0]:
  if x not in universe:universe.append(x)
index={x:i for i,x in enumerate(universe)}
def parse(path):
 names,expr=split(path);out=[]
 for e in expr:
  p={}
  for raw in re.findall(r'[+-]?[^+-]+',e):
   sign=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');c=sign
   if parts[0].isdigit():c*=int(parts.pop(0))
   m=tuple(sorted(index[x] for x in parts if x));p[m]=p.get(m,0)+c
  p={m:c for m,c in p.items() if c};assert p;out.append(p)
 return names,out
def canonical(polys):
 out=[];seen=set()
 for p in polys:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  key=tuple(sorted(p.items()))
  if key not in seen:seen.add(key);out.append(p)
 return out
def specialize(polys,x,value):
 out=[]
 for p in polys:
  q={}
  for m,c in p.items():
   if value==0 and x in m:continue
   n=tuple(i for i in m if not(value==1 and i==x));q[n]=q.get(n,0)+c
  out.append(q)
 return canonical(out)
def stats(names,polys):return {'variables':len(names),'generators':len(polys),'total_terms':sum(map(len,polys)),'degree_mass':sum(len(m) for p in polys for m in p)}
parents={k:parse(p) for k,p in INPUTS.items()};result=json.loads((HERE/'results_design.json').read_text());assert result['status']=='PASS_EXACT_NEXT_REDUCTION_ON_ALL_FOUR_BRANCHES'
ranking=sorted([{'branch':k,'algebraic_size':stats(*parents[k]),'rank_key':[stats(*parents[k])['variables'],stats(*parents[k])['generators'],stats(*parents[k])['total_terms'],stats(*parents[k])['degree_mass'],k]} for k in parents],key=lambda x:x['rank_key']);assert [x['branch'] for x in ranking]==[x['branch'] for x in result['ranking']['ordered']]
factor_replay=[]
for cover in result['factor_localizations']:
 names,polys=parents[cover['branch']];x=index[cover['selected_coordinate']];Drec=next(s for s in cover['sources'] if s['identity']['kind']=='factor_D');Vrec=next(s for s in cover['sources'] if s['identity']['kind']=='factor_V');Dnames,Dactual=parse(HERE/Drec['path']);Vnames,Vactual=parse(HERE/Vrec['path']);divided=[];count=0
 for p in polys:
  if all(x in m for m in p):
   count+=1;q={}
   for m,c in p.items():w=list(m);w.remove(x);q[tuple(w)]=c
   divided.append(q)
  else:divided.append(p)
 inv=index[Drec['identity']['inverse']];Dexpect=canonical(divided+[{():1,tuple(sorted((x,inv))):-1}]);Vexpect=specialize(polys,x,0);assert count==cover['divided_generators'] and Dactual==Dexpect and Vactual==Vexpect;assert Dnames==names+[Drec['identity']['inverse']] and Vnames==[n for n in names if n!=cover['selected_coordinate']];assert sha(HERE/Drec['path'])==Drec['sha256'] and sha(HERE/Vrec['path'])==Vrec['sha256'];factor_replay.append({'branch':cover['branch'],'coordinate':cover['selected_coordinate'],'divided_generators':count,'D_sha256':Drec['sha256'],'V_sha256':Vrec['sha256'],'forward_reverse_exact':True})
torus=result['residual_torus'];names,polys=parents[torus['branch']];x=index[torus['selected_coordinate']];Drec=next(s for s in torus['sources'] if s['identity']['kind']=='torus_D');Vrec=next(s for s in torus['sources'] if s['identity']['kind']=='torus_V');Dnames,Dactual=parse(HERE/Drec['path']);Vnames,Vactual=parse(HERE/Vrec['path']);assert Dactual==specialize(polys,x,1) and Vactual==specialize(polys,x,0) and Dnames==Vnames==[n for n in names if n!=torus['selected_coordinate']]
weights={index[k]:v for k,v in torus['primitive_weights'].items()};rows=[]
for p in polys:
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
assert [rank_mod(rows,p) for p in (32003,65521)]==[70,70] and sha(HERE/Drec['path'])==Drec['sha256'] and sha(HERE/Vrec['path'])==Vrec['sha256']
hostiles=json.loads((HERE/'results_hostiles.json').read_text());assert hostiles['status']=='PASS_20_HOSTILES' and len(hostiles['tests'])==20 and all(hostiles['tests'].values()) and hostiles['solver_runs']==0
out={'schema':'KRENN_X5_REP5_FOUR_SUBCHART_NEXT_SYMBOLIC_REDUCTION_REFEREE_V1','status':'PASS_EXACT_EIGHT_SUBCHART_REFINEMENT_DESIGN_ONLY','producer_result_sha256':sha(HERE/'results_design.json'),'ranking':[x['branch'] for x in ranking],'factor_replay':factor_replay,'torus_replay':{'branch':torus['branch'],'coordinate':torus['selected_coordinate'],'weight':torus['selected_weight'],'grading_modular_ranks':[70,70],'explicit_weight_nullvector':torus['primitive_weights'],'D_sha256':Drec['sha256'],'V_sha256':Vrec['sha256'],'forward_reverse_exact':True},'combined':{'inputs':4,'outputs':8,'every_input_covered':True,'root_free':True},'hostiles':20,'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'inputs':4,'outputs':8,'hostiles':20,'solves':0},sort_keys=True))
