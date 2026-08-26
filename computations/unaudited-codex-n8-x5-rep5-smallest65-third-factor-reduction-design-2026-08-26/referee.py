#!/usr/bin/env python3
"""Independent reconstruction of the third exact rep5 factor cover."""
import hashlib,json,re
from collections import Counter,deque
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PARENT=ROOT/'computations/unaudited-codex-n8-x5-rep5-smallest66-second-factor-reduction-design-2026-08-26';SOURCE=PARENT/'sources/V_a04_00_Q_design.sing';D=json.loads((HERE/'results_design.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE)=='4cd663b6d7861c52681d42a6bc8ebaa4d8d77228e7e8aa4b4e9d3dbb1fdfd4bf' and D['scope']['singular_runs']==0
def split(p):
 t=p.read_text();n=t.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');b=t.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return n,b.split(',\n')
names,_=split(SOURCE);universe=names+['inv_third_factor'];idx={n:i for i,n in enumerate(universe)}
def parse(p):
 ring,exprs=split(p);out=[]
 for e in exprs:
  q={}
  for raw in re.findall(r'[+-]?[^+-]+',e):
   sign=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');c=sign
   if parts[0].isdigit():c*=int(parts.pop(0))
   m=tuple(sorted(idx[x] for x in parts if x));q[m]=q.get(m,0)+c
  q={m:c for m,c in q.items() if c};assert q;out.append(q)
 return ring,out
def canonical(values):
 out=[];seen=set()
 for p in values:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  if len(p)==1 and () in p:return [{():1}]
  key=tuple(sorted(p.items()))
  if key not in seen:seen.add(key);out.append(p)
 return out
ring,parent=parse(SOURCE);assert ring==names and len(names)==65 and len(parent)==3483
pivot_name=D['selected_cover']['selected_coordinate'];assert pivot_name=='a24_10';pivot=idx[pivot_name];divided=[];zero=[];count=0
for p in parent:
 if all(pivot in m for m in p):
  count+=1;q={}
  for m,c in p.items():w=list(m);w.remove(pivot);q[tuple(w)]=c
  divided.append(q)
 else:divided.append(p)
 zero.append({m:c for m,c in p.items() if pivot not in m})
assert count==162;inverse=idx['inv_third_factor'];expected_D=canonical(divided+[{():1,tuple(sorted((pivot,inverse))):-1}]);expected_V=canonical(zero)
records={x['kind']:x for x in D['selected_cover']['sources']};dp=HERE/records['D']['path'];vp=HERE/records['V']['path'];dr,actual_D=parse(dp);vr,actual_V=parse(vp)
assert dr==names+['inv_third_factor'] and actual_D==expected_D and vr==[n for n in names if n!=pivot_name] and actual_V==expected_V
assert sha(dp)==records['D']['sha256'] and sha(vp)==records['V']['sha256'];assert [records['D'][k] for k in ('variables','generators','total_terms')]==[66,3484,128233];assert [records['V'][k] for k in ('variables','generators','total_terms')]==[64,3321,118979]
def rank(rows,p):
 e={}
 for raw in rows:
  r={k:v%p for k,v in raw.items() if v%p}
  while r:
   k=min(r)
   if k not in e:z=pow(r[k],-1,p);e[k]={j:v*z%p for j,v in r.items()};break
   f=r[k];known=e[k];r={j:(r.get(j,0)-f*known.get(j,0))%p for j in set(r)|set(known)};r={j:v for j,v in r.items() if v}
 return len(e)
g=[];linear=[];adj=[set() for _ in names];active=set();monic=[]
for equation,p in enumerate(parent):
 ms=sorted(p);base=Counter(ms[0])
 for m in ms[1:]:
  now=Counter(m);row={i:base[i]-now[i] for i in set(base)|set(now) if base[i]!=now[i]}
  if row:g.append(row)
 lr={m[0]:c for m,c in p.items() if len(m)==1}
 if lr:linear.append(lr)
 support={i for m in p for i in m};active|=support
 for i in support:
  adj[i]|=support-{i}
  if abs(p.get((i,),0))==1 and all(i not in m for m in p if m!=(i,)):monic.append([equation,names[i]])
assert [rank(g,p) for p in (32003,65521)]==[65,65] and [rank(linear,p) for p in (32003,65521)]==[38,38] and active==set(range(65)) and not monic
unseen=set(range(65));components=[]
while unseen:
 q=deque([min(unseen)]);c=set()
 while q:
  i=q.popleft()
  if i in c:continue
  c.add(i);q.extend(adj[i]-c)
 unseen-=c;components.append(c)
assert [len(c) for c in components]==[65]
minor=D['minor_rank_split']['candidate_ledger'];assert len(minor)==45 and sum(x['size']==2 for x in minor)==42 and sum(x['size']==3 for x in minor)==3 and all(not x['exact_generator_up_to_sign'] and x['divisible_generators']==0 for x in minor)
cover=D['nine_stratum_coverage'];assert cover['ledger_preserved'] and cover['local_branch_only'] and not cover['global_closure_claim'] and 'exactly nine strata' in cover['cover_statement']
host=json.loads((HERE/'results_hostiles.json').read_text());assert host['status']=='PASS_20_HOSTILES' and len(host['tests'])==20 and all(host['tests'].values())
result={'schema':'KRENN_X5_REP5_SMALLEST65_THIRD_FACTOR_REFEREE_V1','status':'PASS_EXACT_THIRD_FACTOR_COVER_DESIGN_ONLY','input_sha256':sha(SOURCE),'design_sha256':sha(HERE/'results_design.json'),'coordinate':pivot_name,'factor_count':count,'source_hashes':{'D':sha(dp),'V':sha(vp)},'source_sizes':{'D':[66,3484,128233],'V':[64,3321,118979]},'grading_rank':65,'grading_nullity':0,'linear_rank':38,'component_sizes':[65],'minor_tests':45,'nine_stratum_ledger_preserved':True,'forward_reverse_reconstructed':True,'hostiles':20,'singular_runs':0,'closure_added':False}
tmp=HERE/'results_referee.json.tmp';tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');tmp.replace(HERE/'results_referee.json');print(json.dumps({k:result[k] for k in ('status','coordinate','factor_count','source_sizes','minor_tests','hostiles','singular_runs')},sort_keys=True))
