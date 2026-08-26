#!/usr/bin/env python3
"""Exact maximal three-torus reduction of the smallest rep5 70-variable chart."""
from __future__ import annotations
import copy,hashlib,itertools,json,os,re
from collections import Counter,deque
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations';PARENT=C/'unaudited-codex-n8-x5-rep5-four-subchart-next-symbolic-reduction-design-2026-08-26';SOURCE=PARENT/'sources/closed_V35_21_V_a35_22_Q_design.sing';PINS={PARENT/'MANIFEST.sha256':'d347c3bd4ed99764d103435d25cdaf9b676875d9f90b988ff9cb38073fb585a1',PARENT/'results_design.json':'05de1591d9ffbdb3c382f015c52f04823a67ad4e59d41c5a4a41571abef1cca2',PARENT/'results_referee.json':'f786301b3ba2dbf8957bde9b045f7cfad8c45335cd0f66bcc042eb4ac2ebd0e9',SOURCE:'56b8e22fb1a9e77fa795464f936f5627f0a5dba752ee3e4355345fa02c34dfdc'};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
def atomic(p,v):t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
def split(path):
 text=path.read_text();names=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');body=text.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return names,body.split(',\n')
names,expressions=split(SOURCE);index={x:i for i,x in enumerate(names)}
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
ring,polys=parse(SOURCE);assert ring==names and len(names)==70 and len(polys)==len(set(tuple(sorted(p.items())) for p in polys))==5103
def canonical(values):
 out=[];seen=set()
 for p in values:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  if len(p)==1 and () in p:return [{():1}]
  key=tuple(sorted(p.items()))
  if key not in seen:seen.add(key);out.append(p)
 return out
def specialize(values,assignments):
 out=[];zero={x for x,v in assignments.items() if v==0};one=set(assignments)-zero
 for p in values:
  q={}
  for m,c in p.items():
   if zero.intersection(m):continue
   n=tuple(i for i in m if i not in one);q[n]=q.get(n,0)+c
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
rows=grading_rows(polys);ranks=[rank_mod(rows,p) for p in (32003,65521)];assert ranks==[67,67]
torus_names=['a04_20','a04_21','a04_22'];torus=[index[x] for x in torus_names]
for p in polys:
 for coordinate in torus:
  exponents={m.count(coordinate) for m in p};assert len(exponents)==1
# The three coordinate unit vectors are independent rational nullvectors.  Together with modular rank 67 they prove rank_Q=67/nullity=3.

active=set();monic=[];affine=0;adj=[set() for _ in names];factor_counts={x:0 for x in names}
for equation,p in enumerate(polys):
 maximum=max(map(len,p));affine+=maximum<=1;support={i for m in p for i in m};active|=support
 for i in support:adj[i]|=support-{i}
 for i in support:
  if all(i in m for m in p):factor_counts[names[i]]+=1
  if abs(p.get((i,),0))==1 and all(i not in m for m in p if m!=(i,)):monic.append([equation,names[i]])
unseen=set(range(70));components=[]
while unseen:
 todo=deque([min(unseen)]);component=set()
 while todo:
  i=todo.popleft()
  if i in component:continue
  component.add(i);todo.extend(adj[i]-component)
 unseen-=component;components.append(component)
assert active==set(range(70)) and not monic and affine==0 and [len(x) for x in components]==[70]
assert [factor_counts[x] for x in torus_names]==[486,486,486]
global_unit_test={'literal_inverse_variable_names':[x for x in names if x.startswith('inv') or x in ('sat','beta','abar')],'affine_linear_generators':affine,'unit_monic_graph_substitutions':monic,'constant_unit_generator':any(p=={():1} for p in polys),'detected_global_units':[]};assert not global_unit_test['literal_inverse_variable_names'] and not global_unit_test['constant_unit_generator']
def stats(ring_names,values):
 allowed={index[x] for x in ring_names};act={i for p in values for m in p for i in m if i in allowed};return {'variables':len(ring_names),'generators':len(values),'total_terms':sum(map(len,values)),'degree_mass':sum(len(m) for p in values for m in p),'maximum_terms':max(map(len,values)),'inactive':sorted(set(ring_names)-{names[i] for i in act}),'unit_structural':values==[{():1}]}
def serialize(p):
 pieces=[]
 for m,c in sorted(p.items(),key=lambda item:(len(item[0]),item[0])):
  factors='*'.join(names[i] for i in m);mag=abs(c);body=str(mag) if not factors else factors if mag==1 else f'{mag}*{factors}';pieces.append((('-' if c<0 else '+') if pieces else ('-' if c<0 else ''))+body)
 return ''.join(pieces)
def write_source(path,ring_names,values,bits):
 program='\n'.join(['// EXACT Q DESIGN INPUT ONLY: no Singular/ideal run authorized.','// Maximal residual (G_m)^3 chart; each A04[2j] is independently set to 0 or gauge-fixed to 1.',f"// assignments: {dict(zip(torus_names,bits))}",'option(noredefine);',f"ring r=0,({','.join(ring_names)}),dp;",'ideal I='+',\n'.join(serialize(p) for p in values)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','quit;','']);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(program);os.replace(tmp,path)
S=HERE/'sources';S.mkdir(exist_ok=True)
for stale in S.glob('*.sing'):stale.unlink()
source_records=[]
for bits in itertools.product((0,1),repeat=3):
 assignments={coordinate:value for coordinate,value in zip(torus,bits)};values=specialize(polys,assignments);ring_names=[x for x in names if x not in torus_names];filename='chart_'+'_'.join(f'{x}{value}' for x,value in zip(torus_names,bits))+'_Q_design.sing';path=S/filename;write_source(path,ring_names,values,bits);rebuilt_names,rebuilt=parse(path);assert rebuilt_names==ring_names and rebuilt==values;body=path.read_text().split('ideal I=',1)[1];assert all(not re.search(rf'\b{re.escape(x)}\b',body) for x in torus_names);chart_rows=grading_rows(values);chart_ranks=[rank_mod(chart_rows,p) for p in (32003,65521)];record={'bits':list(bits),'assignment':dict(zip(torus_names,bits)),'open_coordinates':[x for x,v in zip(torus_names,bits) if v==1],'closed_coordinates':[x for x,v in zip(torus_names,bits) if v==0],'path':str(path.relative_to(HERE)),'sha256':sha(path),'bytes':path.stat().st_size,'grading_modular_ranks':chart_ranks,'grading_nullity_upper_bounds':[67-r for r in chart_ranks],**stats(ring_names,values)};source_records.append(record)
assert len(source_records)==8 and all(x['variables']==67 and not x['unit_structural'] for x in source_records)

result={'schema':'KRENN_X5_REP5_SMALLEST70_GLOBAL_THREE_TORUS_REDUCTION_DESIGN_V1','status':'PASS_EXACT_MAXIMAL_THREE_TORUS_EIGHT_CHART_COVER','pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'input':{'sha256':PINS[SOURCE],**stats(names,polys)},'grading':{'constraint_rows':len(rows),'modular_ranks':ranks,'rank_over_Q':67,'nullity_over_Q':3,'explicit_basis':[{x:1} for x in torus_names],'basis_support':torus_names,'basis_primitive':True,'basis_independent':True},'global_unit_test':global_unit_test,'linear_monic_test':{'inactive_coordinates':[],'affine_linear_generators':affine,'unit_monic_graph_substitutions':monic},'factor_structure':{'complete_factor_counts':factor_counts,'maximum_count':486,'maximizers':torus_names},'block_structure':{'components':1,'component_sizes':[70]},'three_torus_cover':{'identity':'product_i (D(x_i) union V(x_i))','coordinates':torus_names,'strata':8,'root_free':True,'exhaustive':True,'forward':'for each nonzero x_i use its independent primitive G_m factor to set x_i=1; set every remaining x_i=0','reverse':'restore each open x_i by its independent weight parameter; no root extraction','sources':source_records},'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False,'held_modular_plan_needed':False}}
atomic(HERE/'results_design.json',result)
def validate(v):
 assert v['status']=='PASS_EXACT_MAXIMAL_THREE_TORUS_EIGHT_CHART_COVER' and v['input']['sha256']==PINS[SOURCE] and v['grading']['rank_over_Q']==67 and v['grading']['nullity_over_Q']==3 and v['grading']['basis_support']==torus_names and v['grading']['basis_primitive'] is True
 assert not v['global_unit_test']['detected_global_units'] and not v['linear_monic_test']['inactive_coordinates'] and not v['linear_monic_test']['unit_monic_graph_substitutions'] and v['block_structure']['component_sizes']==[70]
 assert v['factor_structure']['maximizers']==torus_names and v['three_torus_cover']['strata']==8 and v['three_torus_cover']['root_free'] and v['three_torus_cover']['exhaustive'] and len(v['three_torus_cover']['sources'])==8 and v['scope']['singular_runs']==0 and v['scope']['mathematical_coverage_added'] is False and v['scope']['held_modular_plan_needed'] is False
mutations=[lambda x:x.__setitem__('status','PASS'),lambda x:x['input'].__setitem__('sha256','0'*64),lambda x:x['grading'].__setitem__('rank_over_Q',66),lambda x:x['grading'].__setitem__('nullity_over_Q',2),lambda x:x['grading'].__setitem__('basis_support',[]),lambda x:x['grading'].__setitem__('basis_primitive',False),lambda x:x['global_unit_test']['detected_global_units'].append('fake'),lambda x:x['linear_monic_test']['inactive_coordinates'].append('fake'),lambda x:x['linear_monic_test']['unit_monic_graph_substitutions'].append('fake'),lambda x:x['factor_structure'].__setitem__('maximizers',[]),lambda x:x['block_structure'].__setitem__('component_sizes',[69,1]),lambda x:x['three_torus_cover'].__setitem__('strata',7),lambda x:x['three_torus_cover'].__setitem__('root_free',False),lambda x:x['three_torus_cover'].__setitem__('exhaustive',False),lambda x:x['three_torus_cover']['sources'].pop(),lambda x:x['scope'].__setitem__('singular_runs',1),lambda x:x['scope'].__setitem__('mathematical_coverage_added',True),lambda x:x['scope'].__setitem__('held_modular_plan_needed',True)]
tests={}
for i,mutation in enumerate(mutations):
 value=copy.deepcopy(result);mutation(value)
 try:validate(value)
 except (AssertionError,KeyError,TypeError):tests[f'hostile_{i+1:02d}']=True
 else:tests[f'hostile_{i+1:02d}']=False
assert len(tests)==18 and all(tests.values());atomic(HERE/'results_hostiles.json',{'schema':'KRENN_X5_REP5_SMALLEST70_THREE_TORUS_HOSTILES_V1','status':'PASS_18_HOSTILES','tests':tests,'solver_runs':0})
print(json.dumps({'status':result['status'],'grading':[67,3],'charts':8,'variables_each':67,'generator_range':[min(x['generators'] for x in source_records),max(x['generators'] for x in source_records)],'hostiles':18,'solves':0},sort_keys=True))
