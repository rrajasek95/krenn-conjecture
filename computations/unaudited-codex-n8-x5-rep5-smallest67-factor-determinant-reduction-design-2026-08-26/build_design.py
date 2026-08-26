#!/usr/bin/env python3
"""Exact factor and matrix-minor census of the smallest rep5 67-variable chart."""
from __future__ import annotations
import copy,hashlib,itertools,json,os,re
from collections import Counter,deque
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations';PARENT=C/'unaudited-codex-n8-x5-rep5-smallest70-global-three-torus-reduction-design-2026-08-26';SOURCE=PARENT/'sources/chart_a04_200_a04_210_a04_220_Q_design.sing';PINS={PARENT/'MANIFEST.sha256':'65485dd5f8a0994c0512e82a8ac8ef9e188f5b6fab0a1e1bb2cea3dc7aca6914',PARENT/'results_design.json':'8de18538a16a2e0a07a494a86479ee055aef58745a4e78a37a44048cbbbf69dc',PARENT/'results_referee.json':'ae67512b20dd8c7226082fd5bb760bdfb2588b52ef8a338c6bea9cafd91f978f',SOURCE:'7b8bded2eb861942dee706de682d9d29bdb62ce358f832ee6e59f9fa5c5a7f64'};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
def atomic(p,v):t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
def split(path):
 text=path.read_text();names=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');body=text.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return names,body.split(',\n')
names,expressions=split(SOURCE);inverse_name='inv_factor_pivot';universe=names+[inverse_name];index={x:i for i,x in enumerate(universe)}
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
ring,polys=parse(SOURCE);assert ring==names and len(names)==67 and len(polys)==len(set(tuple(sorted(p.items())) for p in polys))==3645
def canonical(values):
 out=[];seen=set()
 for p in values:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  if len(p)==1 and () in p:return [{():1}]
  key=tuple(sorted(p.items()))
  if key not in seen:seen.add(key);out.append(p)
 return out
def specialize(values,x,value):
 out=[]
 for p in values:
  q={}
  for m,c in p.items():
   if value==0 and x in m:continue
   n=tuple(i for i in m if not(value==1 and i==x));q[n]=q.get(n,0)+c
  out.append(q)
 return canonical(out)
def grading_rows(values):
 rows=[]
 for p in values:
  ms=sorted(p);base=Counter(ms[0])
  for m in ms[1:]:
   now=Counter(m);row={i:base[i]-now[i] for i in set(base)|set(now) if base[i]!=now[i]}
   if row:rows.append(row)
 return rows
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
def rank_q(rows):
 e={}
 for raw in rows:
  r={k:Fraction(v) for k,v in raw.items() if v}
  while r:
   p=min(r)
   if p not in e:
    scale=r[p];e[p]={k:v/scale for k,v in r.items()};break
   f=r[p];known=e[p];r={k:r.get(k,Fraction())-f*known.get(k,Fraction()) for k in set(r)|set(known)};r={k:v for k,v in r.items() if v}
 return len(e)
grows=grading_rows(polys);granks=[rank_mod(grows,p) for p in (32003,65521)];assert granks==[67,67]
active=set();monic=[];affine=0;linear_rows=[];adj=[set() for _ in names];factor_counts={x:0 for x in names}
for equation,p in enumerate(polys):
 maximum=max(map(len,p));affine+=maximum<=1;support={i for m in p for i in m};active|=support
 linear={m[0]:c for m,c in p.items() if len(m)==1}
 if linear:linear_rows.append(linear)
 for i in support:
  adj[i]|=support-{i}
  if all(i in m for m in p):factor_counts[names[i]]+=1
  if abs(p.get((i,),0))==1 and all(i not in m for m in p if m!=(i,)):monic.append([equation,names[i]])
linear_mod=[rank_mod(linear_rows,p) for p in (32003,65521)];linear_exact=rank_q(linear_rows);assert linear_mod==[40,40] and linear_exact==40
unseen=set(range(67));components=[]
while unseen:
 todo=deque([min(unseen)]);component=set()
 while todo:
  i=todo.popleft()
  if i in component:continue
  component.add(i);todo.extend(adj[i]-component)
 unseen-=component;components.append(component)
assert active==set(range(67)) and not monic and affine==0 and [len(x) for x in components]==[67]

# Exhaustive literal determinant/rank-split census for all complete 3x3 blocks.
complete_blocks=[]
for stem in ('a12','a15','a24','a67'):
 cells={(i,j):index[f'{stem}_{i}{j}'] for i in range(3) for j in range(3)};complete_blocks.append((stem,cells))
def permutation_sign(p):return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1
def determinant(cells,rows,cols):
 out={}
 for perm in itertools.permutations(cols):
  m=tuple(sorted(cells[(row,col)] for row,col in zip(rows,perm)));out[m]=out.get(m,0)+permutation_sign(tuple(cols.index(x) for x in perm))
 return {m:c for m,c in out.items() if c}
minor_candidates=[]
for stem,cells in complete_blocks:
 for rs in itertools.combinations(range(3),2):
  for cs in itertools.combinations(range(3),2):minor_candidates.append({'name':f'{stem}_minor_{rs[0]}{rs[1]}_{cs[0]}{cs[1]}','block':stem,'size':2,'polynomial':determinant(cells,rs,cs)})
 minor_candidates.append({'name':f'{stem}_det','block':stem,'size':3,'polynomial':determinant(cells,range(3),range(3))})
assert len(minor_candidates)==40 and all(len(x['polynomial']) in (2,6) for x in minor_candidates)
exponents={}
def exp(m):
 if m not in exponents:exponents[m]=tuple(m.count(i) for i in range(67))
 return exponents[m]
def lead(p):return max(p,key=lambda m:(len(m),exp(m)))
def quotient_monomial(a,b):
 # a / b, assuming b divides a
 work=list(a)
 for x in b:work.remove(x)
 return tuple(work)
def divisible_by(p,d):
 work=dict(p);lm_d=lead(d);lc_d=d[lm_d]
 while work:
  lm=lead(work);ea,eb=exp(lm),exp(lm_d)
  if any(x<y for x,y in zip(ea,eb)):return False
  qm=quotient_monomial(lm,lm_d);qc=Fraction(work[lm],lc_d)
  for dm,dc in d.items():
   target=tuple(sorted(qm+dm));work[target]=work.get(target,Fraction())-qc*dc
   if not work[target]:del work[target]
 return True
generator_keys={tuple(sorted(p.items())) for p in polys};minor_ledger=[]
for candidate in minor_candidates:
 d=candidate.pop('polynomial');exact_generator=tuple(sorted(d.items())) in generator_keys or tuple(sorted((m,-c) for m,c in d.items())) in generator_keys;divides=sum(divisible_by(p,d) for p in polys);minor_ledger.append({**candidate,'terms':len(d),'exact_generator_up_to_sign':exact_generator,'divisible_generators':divides,'constant_or_monomial':len(d)<=1})
assert all(not x['exact_generator_up_to_sign'] and x['divisible_generators']==0 and not x['constant_or_monomial'] for x in minor_ledger)
determinant_test={'complete_3x3_blocks':[x[0] for x in complete_blocks],'two_by_two_minors':36,'three_by_three_determinants':4,'candidates_tested':40,'all_nonconstant_nonmonomial':True,'exact_generator_matches':0,'exact_generator_factors':0,'literal_global_unit_constraints':0,'strict_smaller_cramer_or_rank_split_found':False,'scope':'exact source-literal equality and polynomial divisibility under a fixed admissible monomial order; no ideal-membership claim'}

# The only strict source-level reduction found is the coordinate factor cover.
factor_candidates=[]
for name,count in factor_counts.items():
 if count:
  x=index[name];zero=specialize(polys,x,0);factor_candidates.append({'coordinate':name,'divisible_generators':count,'zero_generators':len(zero),'zero_terms':sum(map(len,zero)),'zero_degree_mass':sum(len(m) for p in zero for m in p),'objective':[-count,sum(map(len,zero)),len(zero),name]})
choice=min(factor_candidates,key=lambda x:tuple(x['objective']));pivot=choice['coordinate'];x=index[pivot];divided=[];count=0
for p in polys:
 if all(x in m for m in p):
  count+=1;q={}
  for m,c in p.items():work=list(m);work.remove(x);q[tuple(work)]=c
  divided.append(q)
 else:divided.append(p)
inv=index[inverse_name];D=canonical(divided+[{():1,tuple(sorted((x,inv))):-1}]);V=specialize(polys,x,0);assert count==choice['divisible_generators']==54
def stats(ring_names,values):
 allowed={index[x] for x in ring_names};act={i for p in values for m in p for i in m if i in allowed};return {'variables':len(ring_names),'generators':len(values),'total_terms':sum(map(len,values)),'degree_mass':sum(len(m) for p in values for m in p),'maximum_terms':max(map(len,values)),'inactive':sorted(set(ring_names)-{universe[i] for i in act}),'unit_structural':values==[{():1}]}
def serialize(p):
 pieces=[]
 for m,c in sorted(p.items(),key=lambda item:(len(item[0]),item[0])):
  factors='*'.join(universe[i] for i in m);mag=abs(c);body=str(mag) if not factors else factors if mag==1 else f'{mag}*{factors}';pieces.append((('-' if c<0 else '+') if pieces else ('-' if c<0 else ''))+body)
 return ''.join(pieces)
def write(path,ring_names,values,comment):
 program='\n'.join(['// EXACT Q DESIGN INPUT ONLY: no Singular/ideal run authorized.','// '+comment,'option(noredefine);',f"ring r=0,({','.join(ring_names)}),dp;",'ideal I='+',\n'.join(serialize(p) for p in values)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','quit;','']);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(program);os.replace(tmp,path)
S=HERE/'sources';S.mkdir(exist_ok=True)
for stale in S.glob('*.sing'):stale.unlink()
specs=[('D',names+[inverse_name],D,f'D({pivot}): adjoin {inverse_name}*{pivot}=1 and divide all {count} complete {pivot} factors.'),('V',[n for n in names if n!=pivot],V,f'V({pivot}): set {pivot}=0 literally.')];source_records=[]
for kind,ring_names,values,comment in specs:
 path=S/f'{kind}_{pivot}_Q_design.sing';write(path,ring_names,values,comment);rebuilt_names,rebuilt=parse(path);assert rebuilt_names==ring_names and rebuilt==values;removed=[n for n in names if n not in ring_names];body=path.read_text().split('ideal I=',1)[1];assert all(not re.search(rf'\b{re.escape(n)}\b',body) for n in removed);source_records.append({'kind':kind,'path':str(path.relative_to(HERE)),'sha256':sha(path),'bytes':path.stat().st_size,'removed_identifiers':removed,**stats(ring_names,values)})
result={'schema':'KRENN_X5_REP5_SMALLEST67_FACTOR_DETERMINANT_REDUCTION_DESIGN_V1','status':'PASS_EXACT_STRICT_FACTOR_COVER_NO_LITERAL_DETERMINANT_REDUCTION','pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'input':{'sha256':PINS[SOURCE],**stats(names,polys)},'grading':{'constraint_rows':len(grows),'modular_ranks':granks,'rank_over_Q':67,'nullity_over_Q':0},'linear_rank':{'rows_with_linear_part':len(linear_rows),'modular_ranks':linear_mod,'exact_rank_over_Q':linear_exact},'inactive_monic':{'inactive_coordinates':[],'affine_linear_generators':affine,'unit_monic_graph_substitutions':monic},'block_structure':{'components':1,'component_sizes':[67]},'factor_structure':{'complete_factor_counts':factor_counts,'nonzero_coordinates':len(factor_candidates),'maximum_count':max(factor_counts.values()),'candidate_ledger':factor_candidates},'determinant_rank_split':{**determinant_test,'candidate_ledger':minor_ledger},'selected_cover':{'identity':'D(x) union V(x)','selected_coordinate':pivot,'divisible_generators':count,'forward_D':'adjoin inv*x=1 and divide all x-multiple generators by x','reverse_D':'forget unique inv=1/x and multiply divided generators by x','forward_V':'set x=0 literally','root_free':True,'exhaustive':True,'strictly_smaller_branch':True,'sources':source_records},'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False}}
atomic(HERE/'results_design.json',result)
def validate(v):
 assert v['status']=='PASS_EXACT_STRICT_FACTOR_COVER_NO_LITERAL_DETERMINANT_REDUCTION' and v['input']['sha256']==PINS[SOURCE] and v['grading']['rank_over_Q']==67 and v['grading']['nullity_over_Q']==0 and v['linear_rank']['exact_rank_over_Q']==40
 assert not v['inactive_monic']['inactive_coordinates'] and not v['inactive_monic']['unit_monic_graph_substitutions'] and v['block_structure']['component_sizes']==[67]
 assert v['determinant_rank_split']['candidates_tested']==40 and v['determinant_rank_split']['exact_generator_matches']==v['determinant_rank_split']['exact_generator_factors']==0 and v['determinant_rank_split']['strict_smaller_cramer_or_rank_split_found'] is False
 assert v['selected_cover']['divisible_generators']==54 and v['selected_cover']['root_free'] and v['selected_cover']['exhaustive'] and v['selected_cover']['strictly_smaller_branch'] and len(v['selected_cover']['sources'])==2 and v['scope']['singular_runs']==0 and v['scope']['mathematical_coverage_added'] is False
mutations=[lambda x:x.__setitem__('status','PASS'),lambda x:x['input'].__setitem__('sha256','0'*64),lambda x:x['grading'].__setitem__('rank_over_Q',66),lambda x:x['grading'].__setitem__('nullity_over_Q',1),lambda x:x['linear_rank'].__setitem__('exact_rank_over_Q',39),lambda x:x['inactive_monic']['inactive_coordinates'].append('fake'),lambda x:x['inactive_monic']['unit_monic_graph_substitutions'].append('fake'),lambda x:x['block_structure'].__setitem__('component_sizes',[66,1]),lambda x:x['determinant_rank_split'].__setitem__('candidates_tested',39),lambda x:x['determinant_rank_split'].__setitem__('exact_generator_matches',1),lambda x:x['determinant_rank_split'].__setitem__('exact_generator_factors',1),lambda x:x['determinant_rank_split'].__setitem__('strict_smaller_cramer_or_rank_split_found',True),lambda x:x['selected_cover'].__setitem__('divisible_generators',53),lambda x:x['selected_cover'].__setitem__('root_free',False),lambda x:x['selected_cover'].__setitem__('exhaustive',False),lambda x:x['selected_cover'].__setitem__('strictly_smaller_branch',False),lambda x:x['selected_cover']['sources'].pop(),lambda x:x['scope'].__setitem__('singular_runs',1),lambda x:x['scope'].__setitem__('mathematical_coverage_added',True)]
tests={}
for i,mutation in enumerate(mutations):
 value=copy.deepcopy(result);mutation(value)
 try:validate(value)
 except (AssertionError,KeyError,TypeError):tests[f'hostile_{i+1:02d}']=True
 else:tests[f'hostile_{i+1:02d}']=False
assert len(tests)==19 and all(tests.values());atomic(HERE/'results_hostiles.json',{'schema':'KRENN_X5_REP5_SMALLEST67_FACTOR_DETERMINANT_HOSTILES_V1','status':'PASS_19_HOSTILES','tests':tests,'solver_runs':0})
print(json.dumps({'status':result['status'],'grading':[67,0],'linear_rank':40,'minor_tests':40,'factor_choice':pivot,'sources':2,'hostiles':19,'solves':0},sort_keys=True))
