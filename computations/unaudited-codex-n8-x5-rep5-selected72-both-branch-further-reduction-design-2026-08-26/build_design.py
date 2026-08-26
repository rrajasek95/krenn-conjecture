#!/usr/bin/env python3
"""Exact further covers of both selected rep5 72-variable branches; never solve."""
from __future__ import annotations
import copy, hashlib, json, os, re
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations'
PARENT=C/'unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-2026-08-26'
PARENT_REF=C/'unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-referee-2026-08-26'
OPEN=PARENT/'sources/stage0_a37_201_Q_design.sing';CLOSED=PARENT/'sources/stage1_a37_200_closed_Q_design.sing'
PINS={PARENT/'MANIFEST.sha256':'a1be34a89dae7597ab06efe6eaba6e0e4fc12256949f667ac8124ee93c35690e',PARENT_REF/'FINAL_MANIFEST.sha256':'d87fe6724f8d1f4bf628eb01986339c86705e55adf9b471cfeed140e725b123e',OPEN:'1e49c2b4127f1a185f50dbacbc63a51b97c210cb5dd9bd16a97f914c897fac1f',CLOSED:'502b68d7c669708c4e0497c7c457793e584fb2a89e07f70e54e85e83b750dd19'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)

def atomic(path,value):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');os.replace(tmp,path)
def split_program(text):
 variables=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');body=text.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];eq=[];depth=0;start=0
 for i,ch in enumerate(body):
  if ch=='(':depth+=1
  elif ch==')':depth-=1
  elif ch==',' and depth==0:eq.append(body[start:i].strip());start=i+1
  assert depth>=0
 eq.append(body[start:].strip());assert depth==0;return variables,eq
def add(a,b,sign=1):
 out=dict(a)
 for m,c in b.items():
  out[m]=out.get(m,0)+sign*c
  if not out[m]:del out[m]
 return out
def mul(a,b):
 out={}
 for am,ac in a.items():
  for bm,bc in b.items():m=tuple(sorted(am+bm));out[m]=out.get(m,0)+ac*bc
 return {m:c for m,c in out.items() if c}
class Parser:
 def __init__(self,text,index):self.t=re.findall(r'[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]',text);self.i=0;self.index=index
 def expression(self):
  v=self.term()
  while self.i<len(self.t) and self.t[self.i] in ('+','-'):s=1 if self.t[self.i]=='+' else -1;self.i+=1;v=add(v,self.term(),s)
  return v
 def term(self):
  v=self.factor()
  while self.i<len(self.t) and self.t[self.i]=='*':self.i+=1;v=mul(v,self.factor())
  return v
 def factor(self):
  x=self.t[self.i]
  if x=='-':self.i+=1;return {m:-c for m,c in self.factor().items()}
  if x=='(':self.i+=1;v=self.expression();assert self.t[self.i]==')';self.i+=1;return v
  self.i+=1
  if x.isdigit():return {} if int(x)==0 else {():int(x)}
  return {(self.index[x],):1}
def parse(path,global_index=None):
 names,expr=split_program(path.read_text());index={x:i for i,x in enumerate(names)} if global_index is None else global_index;polys=[]
 for e in expr:
  p=Parser(e,index);v=p.expression();assert p.i==len(p.t) and v;polys.append(v)
 return names,polys
def canonical(polys):
 out=[];seen=set()
 for p in polys:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  if len(p)==1 and () in p:return [{():1}]
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
def rank_mod(rows,prime):
 echelon={}
 for raw in rows:
  row={k:v%prime for k,v in raw.items() if v%prime}
  while row:
   pivot=min(row)
   if pivot not in echelon:
    inv=pow(row[pivot],-1,prime);echelon[pivot]={k:v*inv%prime for k,v in row.items()};break
   f=row[pivot];known=echelon[pivot];row={k:(row.get(k,0)-f*known.get(k,0))%prime for k in set(row)|set(known)};row={k:v for k,v in row.items() if v}
 return len(echelon)
def grading_rows(polys):
 rows=[]
 for p in polys:
  ms=sorted(p);base=Counter(ms[0])
  for m in ms[1:]:
   now=Counter(m);row={i:base[i]-now[i] for i in set(base)|set(now) if base[i]!=now[i]}
   if row:rows.append(row)
 return rows
def stats(polys,nvars,allowed=None):
 allowed=set(range(nvars)) if allowed is None else set(allowed);active={i for p in polys for m in p for i in m if i in allowed};monic=[]
 for ei,p in enumerate(polys):
  for i in active:
   if abs(p.get((i,),0))==1 and all(i not in m for m in p if m!=(i,)):monic.append([ei,i])
 return {'variables':nvars,'generators':len(polys),'total_terms':sum(map(len,polys)),'degree_mass':sum(len(m) for p in polys for m in p),'maximum_terms':max(map(len,polys)),'inactive_count':len(allowed-active),'monic_count':len(monic),'unit_structural':polys==[{():1}]}
def serialize(p,names):
 pieces=[]
 for m,c in sorted(p.items(),key=lambda item:(len(item[0]),item[0])):
  factors='*'.join(names[i] for i in m);mag=abs(c);body=str(mag) if not factors else factors if mag==1 else f'{mag}*{factors}';pieces.append((('-' if c<0 else '+') if pieces else ('-' if c<0 else ''))+body)
 return ''.join(pieces)
def write_source(path,names,polys,comments,symbol_names):
 program='\n'.join(['// EXACT Q DESIGN INPUT ONLY: no Singular/ideal run authorized.',*['// '+x for x in comments],'option(noredefine);',f"ring r=0,({','.join(names)}),dp;",'ideal I='+',\n'.join(serialize(p,symbol_names) for p in polys)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','quit;',''])
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(program);os.replace(tmp,path);return program

open_names,open_polys=parse(OPEN);closed_names,closed_polys=parse(CLOSED);assert len(open_names)==len(closed_names)==72 and len(open_polys)==len(closed_polys)==6561

# OPEN q=1: exhaustive common-factor localization. Only coordinates that divide a generator are candidates.
factor_candidates=[]
for coordinate,name in enumerate(open_names):
 divisible=[i for i,p in enumerate(open_polys) if all(coordinate in m for m in p)]
 if not divisible:continue
 zero=specialize(open_polys,coordinate,0)
 factor_candidates.append({'coordinate':name,'divisible_generators':len(divisible),'zero_generators':len(zero),'zero_terms':sum(map(len,zero)),'zero_degree_mass':sum(len(m) for p in zero for m in p),'objective':[-len(divisible),sum(map(len,zero)),len(zero),name]})
assert [x['coordinate'] for x in factor_candidates]==['a04_20','a04_21','a04_22'] and all(x['divisible_generators']==486 for x in factor_candidates)
open_choice=min(factor_candidates,key=lambda x:tuple(x['objective']));assert open_choice['coordinate']=='a04_20';open_coordinate=open_names.index('a04_20')
divided=[];divided_count=0
for p in open_polys:
 if all(open_coordinate in m for m in p):
  q={};divided_count+=1
  for m,c in p.items():
   work=list(m);work.remove(open_coordinate);q[tuple(work)]=c
  divided.append(q)
 else:divided.append(p)
inv_index=len(open_names);open_D_names=open_names+['inv_a04_20'];open_D=canonical(divided+[{():1,tuple(sorted((open_coordinate,inv_index))):-1}]);open_V=specialize(open_polys,open_coordinate,0)
assert divided_count==486 and open_D!=[{():1}] and open_V!=[{():1}]

# CLOSED q=0: exact residual one-torus inherited from the parent homogeneous action.
closed_weight_names={'a04_20':1,'a04_21':1,'a04_22':1,'a35_21':-1,'a35_22':-1};closed_weights=[closed_weight_names.get(x,0) for x in closed_names]
rows=grading_rows(closed_polys);assert [rank_mod(rows,p) for p in (32003,65521)]==[71,71]
for p in closed_polys:
 ms=sorted(p);weights_here={sum(closed_weights[i]*n for i,n in Counter(m).items()) for m in ms};assert len(weights_here)==1
closed_candidates=[]
for name in sorted(closed_weight_names):
 coordinate=closed_names.index(name);opened=specialize(closed_polys,coordinate,1);zero=specialize(closed_polys,coordinate,0);objective=[max(sum(map(len,opened)),sum(map(len,zero))),sum(map(len,opened))+sum(map(len,zero)),max(len(opened),len(zero)),len(opened)+len(zero)]
 closed_candidates.append({'coordinate':name,'weight':closed_weights[coordinate],'open_terms':sum(map(len,opened)),'zero_terms':sum(map(len,zero)),'open_generators':len(opened),'zero_generators':len(zero),'objective':objective})
closed_choice=min(closed_candidates,key=lambda x:(*x['objective'],x['coordinate']));closed_coordinate=closed_names.index(closed_choice['coordinate']);closed_D=specialize(closed_polys,closed_coordinate,1);closed_V=specialize(closed_polys,closed_coordinate,0)

S=HERE/'sources';S.mkdir(exist_ok=True)
for stale in S.glob('*.sing'):stale.unlink()
global_names=open_names+['inv_a04_20'];global_index={x:i for i,x in enumerate(global_names)}
source_specs=[
 ('open_q1_D_a04_20_Q_design.sing',open_D_names,open_D,['Parent q=a37_20=1 branch; D(a04_20) with inv_a04_20*a04_20=1.','All 486 a04_20-divisible generators are divided by this certified unit.'],{'parent_branch':'q=1','cover':'D(a04_20)','inverse':'inv_a04_20','divided_generators':486},global_names),
 ('open_q1_V_a04_20_Q_design.sing',[x for x in open_names if x!='a04_20'],open_V,['Parent q=a37_20=1 branch; literal V(a04_20), a04_20=0.'],{'parent_branch':'q=1','cover':'V(a04_20)','zero':'a04_20'},open_names),
 ('closed_q0_D_'+closed_choice['coordinate']+'_Q_design.sing',[x for x in closed_names if x!=closed_choice['coordinate']],closed_D,[f"Parent q=a37_20=0 branch; residual-torus D({closed_choice['coordinate']}) gauge {closed_choice['coordinate']}=1."],{'parent_branch':'q=0','cover':f"D({closed_choice['coordinate']})",'unit':closed_choice['coordinate'],'weight':closed_choice['weight']},closed_names),
 ('closed_q0_V_'+closed_choice['coordinate']+'_Q_design.sing',[x for x in closed_names if x!=closed_choice['coordinate']],closed_V,[f"Parent q=a37_20=0 branch; literal V({closed_choice['coordinate']}), {closed_choice['coordinate']}=0."],{'parent_branch':'q=0','cover':f"V({closed_choice['coordinate']})",'zero':closed_choice['coordinate'],'weight':closed_choice['weight']},closed_names),
]
source_records=[]
for filename,names,polys,comments,identity,symbol_names in source_specs:
 path=S/filename;write_source(path,names,polys,comments,symbol_names);rebuilt_names,rebuilt=parse(path,global_index);assert rebuilt_names==names and rebuilt==polys
 removed=[x for x in open_names if x not in names];body=path.read_text().split('ideal I=',1)[1];assert all(not re.search(rf'\b{re.escape(x)}\b',body) for x in removed)
 source_records.append({'path':str(path.relative_to(HERE)),'sha256':sha(path),'bytes':path.stat().st_size,'identity':identity,'removed_identifiers':removed,**stats(polys,len(names),[global_index[x] for x in names])})

open_input=stats(open_polys,72);closed_input=stats(closed_polys,72)
result={
 'schema':'KRENN_X5_REP5_SELECTED72_BOTH_BRANCH_FURTHER_REDUCTION_DESIGN_V1','status':'PASS_EXACT_FURTHER_COVERS_BOTH_PARENT_BRANCHES',
 'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},
 'parents':{'open_q1':{'sha256':PINS[OPEN],**open_input},'closed_q0':{'sha256':PINS[CLOSED],**closed_input}},
 'open_q1_factor_localization':{'identity':'D(x) union V(x)','selected_coordinate':'a04_20','candidate_ledger':factor_candidates,'divisible_generator_count':486,'forward_D':'adjoin inv with inv*x=1, divide each x-multiple generator by x','reverse_D':'forget inv=1/x; multiplying divided generators by x recovers the parent equations','forward_V':'set x=0 literally','root_free':True,'exhaustive':True,'sources':source_records[:2]},
 'closed_q0_residual_torus':{'grading_modular_ranks':[71,71],'rank_over_Q':71,'nullity_over_Q':1,'primitive_weights':closed_weight_names,'identity':'D(r) union V(r)','selected_coordinate':closed_choice['coordinate'],'selected_weight':closed_choice['weight'],'candidate_ledger':closed_candidates,'forward_D':f"use the primitive torus to set {closed_choice['coordinate']}=1 without root extraction",'reverse_D':'restore the omitted coordinate by the weight action','forward_V':f"set {closed_choice['coordinate']}=0 literally",'root_free':True,'exhaustive':True,'sources':source_records[2:]},
 'combined_cover':{'parent_branches_covered':['q=1','q=0'],'subcharts':4,'direct_implication_between_parent_branches':False,'every_parent_point_covered':True,'all_sources_exact_Q_design_only':True},
 'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False,'no_parent_timeout_reuse':True},
}
atomic(HERE/'results_design.json',result)

def validate(v):
 assert v['status']=='PASS_EXACT_FURTHER_COVERS_BOTH_PARENT_BRANCHES' and v['parents']['open_q1']['sha256']==PINS[OPEN] and v['open_q1_factor_localization']['selected_coordinate']=='a04_20' and v['open_q1_factor_localization']['divisible_generator_count']==486
 assert v['open_q1_factor_localization']['root_free'] and v['open_q1_factor_localization']['exhaustive'] and len(v['open_q1_factor_localization']['sources'])==2
 assert v['closed_q0_residual_torus']['rank_over_Q']==71 and v['closed_q0_residual_torus']['nullity_over_Q']==1 and v['closed_q0_residual_torus']['primitive_weights']==closed_weight_names and len(v['closed_q0_residual_torus']['sources'])==2 and v['closed_q0_residual_torus']['root_free'] and v['closed_q0_residual_torus']['exhaustive']
 assert v['combined_cover']['subcharts']==4 and v['combined_cover']['every_parent_point_covered'] and v['scope']['singular_runs']==0 and v['scope']['mathematical_coverage_added'] is False
mutations=[lambda x:x.__setitem__('status','PASS'),lambda x:x['parents']['open_q1'].__setitem__('sha256','0'*64),lambda x:x['open_q1_factor_localization'].__setitem__('selected_coordinate','a04_21'),lambda x:x['open_q1_factor_localization'].__setitem__('divisible_generator_count',485),lambda x:x['open_q1_factor_localization'].__setitem__('root_free',False),lambda x:x['open_q1_factor_localization'].__setitem__('exhaustive',False),lambda x:x['open_q1_factor_localization']['sources'].pop(),lambda x:x['closed_q0_residual_torus'].__setitem__('rank_over_Q',70),lambda x:x['closed_q0_residual_torus'].__setitem__('nullity_over_Q',0),lambda x:x['closed_q0_residual_torus'].__setitem__('primitive_weights',{}),lambda x:x['closed_q0_residual_torus'].__setitem__('root_free',False),lambda x:x['closed_q0_residual_torus']['sources'].pop(),lambda x:x['combined_cover'].__setitem__('subcharts',3),lambda x:x['combined_cover'].__setitem__('every_parent_point_covered',False),lambda x:x['scope'].__setitem__('singular_runs',1),lambda x:x['scope'].__setitem__('mathematical_coverage_added',True)]
tests={}
for i,mutation in enumerate(mutations):
 v=copy.deepcopy(result);mutation(v)
 try:validate(v)
 except (AssertionError,KeyError,TypeError):tests[f'hostile_{i+1:02d}']=True
 else:tests[f'hostile_{i+1:02d}']=False
assert len(tests)==16 and all(tests.values());atomic(HERE/'results_hostiles.json',{'schema':'KRENN_X5_REP5_SELECTED72_BOTH_BRANCH_HOSTILES_V1','status':'PASS_16_HOSTILES','tests':tests,'solver_runs':0})
print(json.dumps({'status':result['status'],'open_selected':'a04_20','closed_selected':closed_choice['coordinate'],'sources':4,'hostiles':16,'solves':0},sort_keys=True))
