#!/usr/bin/env python3
"""Third exact factor-cover reduction on the rep5 strict-zero lineage."""
from __future__ import annotations
import copy, hashlib, itertools, json, os, re
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]; C=ROOT/'computations'
PARENT=C/'unaudited-codex-n8-x5-rep5-smallest66-second-factor-reduction-design-2026-08-26'
SOURCE=PARENT/'sources/V_a04_00_Q_design.sing'
COVER=C/'unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25'
COVER_REF=C/'unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-referee-2026-08-25'
PINS={
 PARENT/'MANIFEST.sha256':'4c34cf3bbb4ddfd5f69857f408c597a7353068dbb7de62f46190d8e43d6e2808',
 PARENT/'results_design.json':'76de19215a120023816fcbb6bdb4f652a9ae6d1158eab8f0980da7ec35d96b06',
 PARENT/'results_referee.json':'c6e7ceb2b1ec91fbac5987a1369d7771091bce5099120a8018a2e3a94f7ddf23',
 SOURCE:'4cd663b6d7861c52681d42a6bc8ebaa4d8d77228e7e8aa4b4e9d3dbb1fdfd4bf',
 COVER/'MANIFEST.sha256':'50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1',
 COVER/'results_design_v2.json':'4d572fc359430eab8a55ee80ffe98993521e510f9eb48c37ab185742ad19bf00',
 COVER_REF/'results_referee.json':'c6216de12f0df50704a52695edf598d004ffb6d7307877e4f16b17ba20f0225a',
 COVER_REF/'FINAL_MANIFEST.sha256':'3eef6a5bec2f260625189285cdaf171dbfa36530a1f67086528583e4f96db4c6',
}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in PINS.items(): assert sha(p)==h,(p,sha(p),h)
def atomic(p,v):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
def split(p):
 t=p.read_text();n=t.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');b=t.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return n,b.split(',\n')
names,_=split(SOURCE);inv_name='inv_third_factor';universe=names+[inv_name];idx={n:i for i,n in enumerate(universe)}
def parse(p):
 ring,exprs=split(p);out=[]
 for e in exprs:
  q={}
  for raw in re.findall(r'[+-]?[^+-]+',e):
   s=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');c=s
   if parts[0].isdigit(): c*=int(parts.pop(0))
   m=tuple(sorted(idx[x] for x in parts if x));q[m]=q.get(m,0)+c
  q={m:c for m,c in q.items() if c};assert q;out.append(q)
 return ring,out
ring,polys=parse(SOURCE);assert ring==names and len(names)==65 and len(polys)==3483 and len({tuple(sorted(p.items())) for p in polys})==3483
def canonical(values):
 out=[];seen=set()
 for p in values:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  if len(p)==1 and () in p:return [{():1}]
  k=tuple(sorted(p.items()))
  if k not in seen:seen.add(k);out.append(p)
 return out
def specialize(values,x):
 return canonical([{m:c for m,c in p.items() if x not in m} for p in values])
def rank_mod(rows,prime):
 echelon={}
 for raw in rows:
  r={k:v%prime for k,v in raw.items() if v%prime}
  while r:
   p=min(r)
   if p not in echelon:
    z=pow(r[p],-1,prime);echelon[p]={k:v*z%prime for k,v in r.items()};break
   f=r[p];known=echelon[p];r={k:(r.get(k,0)-f*known.get(k,0))%prime for k in set(r)|set(known)};r={k:v for k,v in r.items() if v}
 return len(echelon)
def rank_q(rows):
 echelon={}
 for raw in rows:
  r={k:Fraction(v) for k,v in raw.items() if v}
  while r:
   p=min(r)
   if p not in echelon:
    z=r[p];echelon[p]={k:v/z for k,v in r.items()};break
   f=r[p];known=echelon[p];r={k:r.get(k,Fraction())-f*known.get(k,Fraction()) for k in set(r)|set(known)};r={k:v for k,v in r.items() if v}
 return len(echelon)
grows=[];lrows=[];active=set();affine=0;monic=[];fcounts={n:0 for n in names};adj=[set() for _ in names]
for equation,p in enumerate(polys):
 ms=sorted(p);base=Counter(ms[0])
 for m in ms[1:]:
  now=Counter(m);r={i:base[i]-now[i] for i in set(base)|set(now) if base[i]!=now[i]}
  if r:grows.append(r)
 support={i for m in p for i in m};active|=support;affine+=max(map(len,p))<=1
 linear={m[0]:c for m,c in p.items() if len(m)==1}
 if linear:lrows.append(linear)
 for i in support:
  adj[i]|=support-{i}
  if all(i in m for m in p):fcounts[names[i]]+=1
  if abs(p.get((i,),0))==1 and all(i not in m for m in p if m!=(i,)):monic.append([equation,names[i]])
granks=[rank_mod(grows,p) for p in (32003,65521)];assert granks==[65,65]
lranks=[rank_mod(lrows,p) for p in (32003,65521)];lexact=rank_q(lrows);assert lranks==[lexact,lexact]
assert active==set(range(65)) and affine==0 and not monic
unseen=set(range(65));components=[]
while unseen:
 q=deque([min(unseen)]);component=set()
 while q:
  i=q.popleft()
  if i in component:continue
  component.add(i);q.extend(adj[i]-component)
 unseen-=component;components.append(component)
assert [len(c) for c in components]==[65]

# All literal matrix minors supported by the remaining coordinate set.
blocks={}
for n in names:
 m=re.fullmatch(r'(a\d+)_([012])([012])',n)
 if m:blocks.setdefault(m[1],{})[(int(m[2]),int(m[3]))]=idx[n]
def sgn(p):return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1
def det(cells,rows,cols):
 out={}
 for perm in itertools.permutations(cols):
  m=tuple(sorted(cells[(r,c)] for r,c in zip(rows,perm)));out[m]=out.get(m,0)+sgn(tuple(cols.index(c) for c in perm))
 return {m:c for m,c in out.items() if c}
candidates=[]
for stem,cells in sorted(blocks.items()):
 for rs in itertools.combinations(range(3),2):
  for cs in itertools.combinations(range(3),2):
   if all((r,c) in cells for r in rs for c in cs):candidates.append((f'{stem}_minor_{rs}_{cs}',stem,2,det(cells,rs,cs)))
 if len(cells)==9:candidates.append((f'{stem}_det',stem,3,det(cells,range(3),range(3))))
def exponent(m):return tuple(m.count(i) for i in range(65))
def lead(p):return max(p,key=lambda m:(len(m),exponent(m)))
def divide_monomial(a,b):
 w=list(a)
 for x in b:w.remove(x)
 return tuple(w)
def divisible(p,d):
 w={m:Fraction(c) for m,c in p.items()};ld=lead(d);lc=d[ld];ed=exponent(ld)
 while w:
  lm=lead(w)
  if any(a<b for a,b in zip(exponent(lm),ed)):return False
  q=divide_monomial(lm,ld);f=w[lm]/lc
  for m,c in d.items():
   target=tuple(sorted(q+m));w[target]=w.get(target,Fraction())-f*c
   if not w[target]:del w[target]
 return True
keys={tuple(sorted(p.items())) for p in polys};minor_ledger=[]
for n,stem,size,d in candidates:
 key=tuple(sorted(d.items()));neg=tuple(sorted((m,-c) for m,c in d.items()));minor_ledger.append({'name':n,'block':stem,'size':size,'terms':len(d),'exact_generator_up_to_sign':key in keys or neg in keys,'divisible_generators':sum(divisible(p,d) for p in polys)})
assert minor_ledger and all(not x['exact_generator_up_to_sign'] and x['divisible_generators']==0 for x in minor_ledger)
def stats(ring_names,values):
 allowed={idx[n] for n in ring_names};used={i for p in values for m in p for i in m if i in allowed};return {'variables':len(ring_names),'generators':len(values),'total_terms':sum(map(len,values)),'degree_mass':sum(len(m) for p in values for m in p),'maximum_terms':max(map(len,values)),'inactive':sorted(set(ring_names)-{universe[i] for i in used}),'unit_structural':values==[{():1}]}
factor_candidates=[]
for n,count in fcounts.items():
 if count:
  zero=specialize(polys,idx[n]);z=stats([x for x in names if x!=n],zero);factor_candidates.append({'coordinate':n,'divisible_generators':count,'zero_generators':z['generators'],'zero_terms':z['total_terms'],'zero_degree_mass':z['degree_mass'],'objective':[-count,z['total_terms'],z['generators'],n]})
assert factor_candidates
choice=min(factor_candidates,key=lambda x:tuple(x['objective']));pivot_name=choice['coordinate'];pivot=idx[pivot_name];divided=[];count=0
for p in polys:
 if all(pivot in m for m in p):
  count+=1;q={}
  for m,c in p.items():w=list(m);w.remove(pivot);q[tuple(w)]=c
  divided.append(q)
 else:divided.append(p)
assert count==choice['divisible_generators']
inverse=idx[inv_name];D=canonical(divided+[{():1,tuple(sorted((pivot,inverse))):-1}]);V=specialize(polys,pivot)
def serialize(p):
 out=[]
 for m,c in sorted(p.items(),key=lambda x:(len(x[0]),x[0])):
  fs='*'.join(universe[i] for i in m);mag=abs(c);body=str(mag) if not fs else fs if mag==1 else f'{mag}*{fs}';out.append((('-' if c<0 else '+') if out else ('-' if c<0 else ''))+body)
 return ''.join(out)
def write(path,ring_names,values,comment):
 text='\n'.join(['// EXACT Q DESIGN INPUT ONLY: no Singular/ideal run authorized.','// '+comment,'option(noredefine);',f"ring r=0,({','.join(ring_names)}),dp;",'ideal I='+',\n'.join(serialize(p) for p in values)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','quit;','']);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(text);os.replace(tmp,path)
S=HERE/'sources';S.mkdir(exist_ok=True)
for stale in S.glob('*.sing'):stale.unlink()
specs=[('D',names+[inv_name],D,f'D({pivot_name}): invert and divide {count} complete coordinate factors.'),('V',[n for n in names if n!=pivot_name],V,f'V({pivot_name}): set {pivot_name}=0 literally.')];records=[]
for kind,rn,values,comment in specs:
 path=S/f'{kind}_{pivot_name}_Q_design.sing';write(path,rn,values,comment);rr,rebuilt=parse(path);assert rr==rn and rebuilt==values;removed=[n for n in names if n not in rn];body=path.read_text().split('ideal I=',1)[1];assert all(not re.search(rf'\b{re.escape(n)}\b',body) for n in removed);records.append({'kind':kind,'path':str(path.relative_to(HERE)),'sha256':sha(path),'bytes':path.stat().st_size,'removed_identifiers':removed,**stats(rn,values)})
assert records[1]['variables']==64 and records[1]['generators']<3483 and records[1]['total_terms']<128231
nine=json.loads((COVER/'results_design_v2.json').read_text());assert nine['cover']=='for each k, D(t1) union D(t2) union V(t1,t2) is exhaustive; three k charts give exactly nine strata'
result={'schema':'KRENN_X5_REP5_SMALLEST65_THIRD_FACTOR_REDUCTION_DESIGN_V1','status':'PASS_EXACT_THIRD_FACTOR_COVER_NO_TORUS_MONIC_OR_LITERAL_MINOR_REDUCTION','pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'nine_stratum_coverage':{'ledger_preserved':True,'cover_statement':nine['cover'],'source_design_sha256':PINS[COVER/'results_design_v2.json'],'source_referee_sha256':PINS[COVER_REF/'results_referee.json'],'local_branch_only':True,'global_closure_claim':False},'input':{'sha256':PINS[SOURCE],**stats(names,polys)},'grading':{'constraint_rows':len(grows),'modular_ranks':granks,'rank_over_Q':65,'nullity_over_Q':0},'linear_rank':{'rows_with_linear_part':len(lrows),'modular_ranks':lranks,'exact_rank_over_Q':lexact},'inactive_monic':{'inactive_coordinates':[],'affine_linear_generators':affine,'unit_monic_graph_substitutions':monic},'block_structure':{'components':1,'component_sizes':[65]},'factor_structure':{'complete_factor_counts':fcounts,'nonzero_coordinates':len(factor_candidates),'maximum_count':max(fcounts.values()),'candidate_ledger':factor_candidates},'minor_rank_split':{'available_candidates':len(minor_ledger),'two_by_two_minors':sum(x['size']==2 for x in minor_ledger),'three_by_three_determinants':sum(x['size']==3 for x in minor_ledger),'exact_generator_matches':0,'exact_generator_factors':0,'strict_smaller_literal_rank_split_found':False,'scope':'literal equality/divisibility only; no ideal/radical-membership claim','candidate_ledger':minor_ledger},'selected_cover':{'identity':'D(x) union V(x)','selected_coordinate':pivot_name,'divisible_generators':count,'forward_D':'adjoin inv*x=1 and divide every x-multiple generator by x','reverse_D':'forget unique inv=1/x and multiply divided generators by x','forward_V':'set x=0 literally','root_free':True,'exhaustive':True,'strictly_smaller_V_branch':True,'sources':records},'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False}}
atomic(HERE/'results_design.json',result)
def validate(v):
 assert v['status']=='PASS_EXACT_THIRD_FACTOR_COVER_NO_TORUS_MONIC_OR_LITERAL_MINOR_REDUCTION' and v['input']['sha256']==PINS[SOURCE]
 assert v['grading']['rank_over_Q']==65 and v['grading']['nullity_over_Q']==0 and not v['inactive_monic']['inactive_coordinates'] and not v['inactive_monic']['unit_monic_graph_substitutions'] and v['block_structure']['component_sizes']==[65]
 assert v['minor_rank_split']['available_candidates']==len(minor_ledger) and v['minor_rank_split']['exact_generator_matches']==v['minor_rank_split']['exact_generator_factors']==0
 assert v['selected_cover']['divisible_generators']==count and v['selected_cover']['exhaustive'] and v['selected_cover']['root_free'] and v['selected_cover']['strictly_smaller_V_branch'] and len(v['selected_cover']['sources'])==2
 assert v['nine_stratum_coverage']['ledger_preserved'] and v['nine_stratum_coverage']['local_branch_only'] and v['nine_stratum_coverage']['global_closure_claim'] is False
 assert v['scope']['singular_runs']==0 and v['scope']['mathematical_coverage_added'] is False
mutations=[lambda v:v.__setitem__('status','PASS'),lambda v:v['input'].__setitem__('sha256','0'*64),lambda v:v['grading'].__setitem__('rank_over_Q',64),lambda v:v['grading'].__setitem__('nullity_over_Q',1),lambda v:v['inactive_monic']['inactive_coordinates'].append('fake'),lambda v:v['inactive_monic']['unit_monic_graph_substitutions'].append('fake'),lambda v:v['block_structure'].__setitem__('component_sizes',[64,1]),lambda v:v['minor_rank_split'].__setitem__('available_candidates',0),lambda v:v['minor_rank_split'].__setitem__('exact_generator_matches',1),lambda v:v['minor_rank_split'].__setitem__('exact_generator_factors',1),lambda v:v['selected_cover'].__setitem__('divisible_generators',count-1),lambda v:v['selected_cover'].__setitem__('exhaustive',False),lambda v:v['selected_cover'].__setitem__('root_free',False),lambda v:v['selected_cover'].__setitem__('strictly_smaller_V_branch',False),lambda v:v['selected_cover']['sources'].pop(),lambda v:v['nine_stratum_coverage'].__setitem__('ledger_preserved',False),lambda v:v['nine_stratum_coverage'].__setitem__('local_branch_only',False),lambda v:v['nine_stratum_coverage'].__setitem__('global_closure_claim',True),lambda v:v['scope'].__setitem__('singular_runs',1),lambda v:v['scope'].__setitem__('mathematical_coverage_added',True)]
tests={}
for i,mutation in enumerate(mutations,1):
 value=copy.deepcopy(result);mutation(value)
 try:validate(value)
 except (AssertionError,KeyError,TypeError):tests[f'hostile_{i:02d}']=True
 else:tests[f'hostile_{i:02d}']=False
assert len(tests)==20 and all(tests.values());atomic(HERE/'results_hostiles.json',{'schema':'KRENN_X5_REP5_SMALLEST65_THIRD_FACTOR_HOSTILES_V1','status':'PASS_20_HOSTILES','tests':tests,'solver_runs':0})
print(json.dumps({'status':result['status'],'grading':[65,0],'linear_rank':lexact,'factor_choice':pivot_name,'factor_count':count,'minor_tests':len(minor_ledger),'sources':2,'hostiles':20,'solves':0},sort_keys=True))
