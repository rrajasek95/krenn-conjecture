#!/usr/bin/env python3
"""Rank and exactly refine all four rep5 subcharts without invoking a solver."""
from __future__ import annotations
import copy,hashlib,json,os,re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/'computations';PARENT=C/'unaudited-codex-n8-x5-rep5-selected72-both-branch-further-reduction-design-2026-08-26'
INPUTS=[PARENT/'sources/closed_q0_D_a35_21_Q_design.sing',PARENT/'sources/closed_q0_V_a35_21_Q_design.sing',PARENT/'sources/open_q1_D_a04_20_Q_design.sing',PARENT/'sources/open_q1_V_a04_20_Q_design.sing']
INPUT_SHA=['849807535cc05c47cc71a5afee504a538ae1f437efe41a98daaba11c2f2bbe6f','a5cc89b0ac785e1a93bda4e936d97479a69a54b4e477fd968dfa68e4ae0118e7','d0284f7417818dacb2829d51851413d56c38299bf5733d85a82725b4cb10b82d','556119066b14ac491a4c4c3c87fbd1f435b4000be2501028420518e4c9495108']
PINS={PARENT/'MANIFEST.sha256':'142f351a5c77f69b1e025e112e9036b125a22215cf5a0652a4187a153c365bf1',PARENT/'results_design.json':'3498302c9056896a23139b0da26fd0eb5ae65d2af0256d0d82a11c0ef885deac',PARENT/'results_referee.json':'feb359eec14d441ededea9dd4e1019222d58faf20262bbe49ff26064b9a26cc4',**{p:h for p,h in zip(INPUTS,INPUT_SHA)}};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
def atomic(p,v):t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
def split(path):
 text=path.read_text();names=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');body=text.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];return names,body.split(',\n')
input_names=[split(p)[0] for p in INPUTS];universe=[]
for names in input_names:
 for x in names:
  if x not in universe:universe.append(x)
new_inverses=['inv2_a04_21_openD','inv_a04_21_openV','inv_a35_22_closedD']
for x in new_inverses:assert x not in universe;universe.append(x)
index={x:i for i,x in enumerate(universe)}
def parse(path):
 names,expr=split(path);out=[]
 for e in expr:
  p={}
  for raw in re.findall(r'[+-]?[^+-]+',e):
   sign=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');coefficient=sign
   if parts[0].isdigit():coefficient*=int(parts.pop(0))
   m=tuple(sorted(index[x] for x in parts if x));p[m]=p.get(m,0)+coefficient
  p={m:c for m,c in p.items() if c};assert p;out.append(p)
 return names,out
parsed=[parse(p)[1] for p in INPUTS];assert [len(x) for x in parsed]==[6561,6075,6562,6075]
def canonical(polys):
 out=[];seen=set()
 for p in polys:
  p={m:c for m,c in p.items() if c}
  if not p:continue
  if len(p)==1 and () in p:return [{():1}]
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
def stats(names,polys):
 allowed={index[x] for x in names};active={i for p in polys for m in p for i in m if i in allowed};monic=[]
 for ei,p in enumerate(polys):
  for i in active:
   if abs(p.get((i,),0))==1 and all(i not in m for m in p if m!=(i,)):monic.append([ei,universe[i]])
 return {'variables':len(names),'generators':len(polys),'total_terms':sum(map(len,polys)),'degree_mass':sum(len(m) for p in polys for m in p),'maximum_terms':max(map(len,polys)),'inactive':sorted(set(names)-{universe[i] for i in active}),'unit_monic':monic,'unit_structural':polys==[{():1}]}
def factor_candidates(names,polys):
 rows=[]
 for name in names:
  x=index[name];count=sum(all(x in m for m in p) for p in polys)
  if count:
   zero=specialize(polys,x,0);rows.append({'coordinate':name,'divisible_generators':count,'zero_generators':len(zero),'zero_terms':sum(map(len,zero)),'zero_degree_mass':sum(len(m) for p in zero for m in p),'objective':[-count,sum(map(len,zero)),len(zero),name]})
 return rows
def factor_cover(names,polys,coordinate,inverse):
 x=index[coordinate];divided=[];count=0
 for p in polys:
  if all(x in m for m in p):
   count+=1;q={}
   for m,c in p.items():work=list(m);work.remove(x);q[tuple(work)]=c
   divided.append(q)
  else:divided.append(p)
 inv=index[inverse];D=canonical(divided+[{():1,tuple(sorted((x,inv))):-1}]);V=specialize(polys,x,0);return names+[inverse],D,[n for n in names if n!=coordinate],V,count
def grading_rows(polys):
 rows=[]
 for p in polys:
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
def serialize(p):
 pieces=[]
 for m,c in sorted(p.items(),key=lambda item:(len(item[0]),item[0])):
  factors='*'.join(universe[i] for i in m);mag=abs(c);body=str(mag) if not factors else factors if mag==1 else f'{mag}*{factors}';pieces.append((('-' if c<0 else '+') if pieces else ('-' if c<0 else ''))+body)
 return ''.join(pieces)
def write_source(path,names,polys,comments):
 program='\n'.join(['// EXACT Q DESIGN INPUT ONLY: no Singular/ideal run authorized.',*['// '+x for x in comments],'option(noredefine);',f"ring r=0,({','.join(names)}),dp;",'ideal I='+',\n'.join(serialize(p) for p in polys)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','quit;','']);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(program);os.replace(tmp,path);return program

labels=['closed_D35_21','closed_V35_21','open_D04_20','open_V04_20'];input_stats=[stats(n,p) for n,p in zip(input_names,parsed)];ranking=sorted([{'branch':label,'sha256':h,'algebraic_size':s,'rank_key':[s['variables'],s['generators'],s['total_terms'],s['degree_mass'],label]} for label,h,s in zip(labels,INPUT_SHA,input_stats)],key=lambda x:x['rank_key'])

# Three grading-rigid branches: use exhaustive complete-factor localization.
factor_jobs=[]
for branch_i,inverse in ((0,'inv_a35_22_closedD'),(2,'inv2_a04_21_openD'),(3,'inv_a04_21_openV')):
 candidates=factor_candidates(input_names[branch_i],parsed[branch_i]);choice=min(candidates,key=lambda x:tuple(x['objective']));Dnames,D,Vnames,V,count=factor_cover(input_names[branch_i],parsed[branch_i],choice['coordinate'],inverse);factor_jobs.append({'input_index':branch_i,'candidates':candidates,'choice':choice,'Dnames':Dnames,'D':D,'Vnames':Vnames,'V':V,'count':count,'inverse':inverse})

# Smallest branch has exact residual one-torus; quotient it rather than adding an inverse.
torus_i=1;torus_names=input_names[torus_i];torus_polys=parsed[torus_i];weights_by_name={'a04_20':1,'a04_21':1,'a04_22':1,'a35_22':-1};weights={index[k]:v for k,v in weights_by_name.items()};rows=grading_rows(torus_polys);ranks=[rank_mod(rows,p) for p in (32003,65521)];assert ranks==[70,70]
for p in torus_polys:
 values={sum(weights.get(i,0)*n for i,n in Counter(m).items()) for m in p};assert len(values)==1
torus_candidates=[]
for coordinate in sorted(weights_by_name):
 x=index[coordinate];D=specialize(torus_polys,x,1);V=specialize(torus_polys,x,0);objective=[max(sum(map(len,D)),sum(map(len,V))),sum(map(len,D))+sum(map(len,V)),max(len(D),len(V)),len(D)+len(V)]
 torus_candidates.append({'coordinate':coordinate,'weight':weights_by_name[coordinate],'D_generators':len(D),'D_terms':sum(map(len,D)),'V_generators':len(V),'V_terms':sum(map(len,V)),'objective':objective})
torus_choice=min(torus_candidates,key=lambda x:(*x['objective'],x['coordinate']));tx=index[torus_choice['coordinate']];torus_D=specialize(torus_polys,tx,1);torus_V=specialize(torus_polys,tx,0);torus_Dnames=torus_Vnames=[n for n in torus_names if n!=torus_choice['coordinate']]

S=HERE/'sources';S.mkdir(exist_ok=True)
for stale in S.glob('*.sing'):stale.unlink()
records=[]
for job in factor_jobs:
 label=labels[job['input_index']];coord=job['choice']['coordinate']
 specs=[(f'{label}_D_{coord}_Q_design.sing',job['Dnames'],job['D'],[f'{label}: D({coord}), adjoin {job["inverse"]}*{coord}=1 and divide all {job["count"]} {coord}-multiple generators.'],{'branch':label,'kind':'factor_D','coordinate':coord,'inverse':job['inverse'],'divided_generators':job['count']}),(f'{label}_V_{coord}_Q_design.sing',job['Vnames'],job['V'],[f'{label}: literal V({coord}), {coord}=0.'],{'branch':label,'kind':'factor_V','coordinate':coord})]
 for filename,names,polys,comments,identity in specs:
  path=S/filename;write_source(path,names,polys,comments);rebuilt_names,rebuilt=parse(path);assert rebuilt_names==names and rebuilt==polys;removed=[x for x in input_names[job['input_index']] if x not in names];body=path.read_text().split('ideal I=',1)[1];assert all(not re.search(rf'\b{re.escape(x)}\b',body) for x in removed);records.append({'path':str(path.relative_to(HERE)),'sha256':sha(path),'bytes':path.stat().st_size,'identity':identity,'removed_identifiers':removed,**stats(names,polys)})
for kind,names,polys,value in (('D',torus_Dnames,torus_D,1),('V',torus_Vnames,torus_V,0)):
 coord=torus_choice['coordinate'];path=S/f'{labels[torus_i]}_{kind}_{coord}_Q_design.sing';write_source(path,names,polys,[f'{labels[torus_i]}: residual-torus {kind}({coord}), set {coord}={value}.']);rebuilt_names,rebuilt=parse(path);assert rebuilt_names==names and rebuilt==polys;body=path.read_text().split('ideal I=',1)[1];assert not re.search(rf'\b{re.escape(coord)}\b',body);records.append({'path':str(path.relative_to(HERE)),'sha256':sha(path),'bytes':path.stat().st_size,'identity':{'branch':labels[torus_i],'kind':'torus_'+kind,'coordinate':coord,'value':value,'weight':torus_choice['weight']},'removed_identifiers':[coord],**stats(names,polys)})

factor_summary=[]
for job in factor_jobs:
 factor_summary.append({'branch':labels[job['input_index']],'grading_modular_rank':[len(input_names[job['input_index']])]*2,'grading_nullity':0,'candidate_ledger':job['candidates'],'selected_coordinate':job['choice']['coordinate'],'divided_generators':job['count'],'identity':'D(x) union V(x)','forward_D':'adjoin inv*x=1 and divide every x-multiple generator by x','reverse_D':'forget unique inv=1/x and multiply divided generators by x','forward_V':'set x=0 literally','root_free':True,'exhaustive':True,'sources':[x for x in records if x['identity']['branch']==labels[job['input_index']]]})
result={'schema':'KRENN_X5_REP5_FOUR_SUBCHART_NEXT_SYMBOLIC_REDUCTION_DESIGN_V1','status':'PASS_EXACT_NEXT_REDUCTION_ON_ALL_FOUR_BRANCHES','pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'ranking':{'metric':'lexicographic (variables,generators,total_terms,degree_mass,branch); lower is smaller','ordered':ranking},'factor_localizations':factor_summary,'residual_torus':{'branch':labels[torus_i],'grading_modular_ranks':ranks,'rank_over_Q':70,'nullity_over_Q':1,'primitive_weights':weights_by_name,'candidate_ledger':torus_candidates,'selected_coordinate':torus_choice['coordinate'],'selected_weight':torus_choice['weight'],'identity':'D(r) union V(r)','forward_D':f'use primitive weight {torus_choice["weight"]} action to set {torus_choice["coordinate"]}=1 without roots','reverse_D':'restore omitted coordinate by weight action','forward_V':f'set {torus_choice["coordinate"]}=0 literally','root_free':True,'exhaustive':True,'sources':[x for x in records if x['identity']['branch']==labels[torus_i]]},'combined':{'input_branches':4,'output_subcharts':8,'every_input_branch_refined':True,'every_input_point_covered':True,'all_sources_exact_Q':True},'scope':{'singular_runs':0,'ideal_solves':0,'mathematical_coverage_added':False,'rep5_closed':False,'no_consumed_attempt_reuse':True}}
atomic(HERE/'results_design.json',result)
def validate(v):
 assert v['status']=='PASS_EXACT_NEXT_REDUCTION_ON_ALL_FOUR_BRANCHES' and len(v['ranking']['ordered'])==4 and len(v['factor_localizations'])==3 and all(x['root_free'] and x['exhaustive'] and len(x['sources'])==2 for x in v['factor_localizations'])
 assert [x['selected_coordinate'] for x in v['factor_localizations']]==[x['choice']['coordinate'] for x in factor_jobs] and [x['divided_generators'] for x in v['factor_localizations']]==[x['count'] for x in factor_jobs]
 assert v['residual_torus']['rank_over_Q']==70 and v['residual_torus']['nullity_over_Q']==1 and v['residual_torus']['primitive_weights']==weights_by_name and v['residual_torus']['root_free'] and v['residual_torus']['exhaustive'] and len(v['residual_torus']['sources'])==2
 assert v['combined']['input_branches']==4 and v['combined']['output_subcharts']==8 and v['combined']['every_input_point_covered'] and v['scope']['singular_runs']==0 and v['scope']['mathematical_coverage_added'] is False
mutations=[lambda x:x.__setitem__('status','PASS'),lambda x:x['ranking']['ordered'].pop(),lambda x:x['factor_localizations'].pop(),lambda x:x['factor_localizations'][0].__setitem__('selected_coordinate','bad'),lambda x:x['factor_localizations'][0].__setitem__('root_free',False),lambda x:x['factor_localizations'][0].__setitem__('exhaustive',False),lambda x:x['factor_localizations'][0]['sources'].pop(),lambda x:x['factor_localizations'][1].__setitem__('divided_generators',0),lambda x:x['factor_localizations'][2]['sources'].pop(),lambda x:x['residual_torus'].__setitem__('rank_over_Q',69),lambda x:x['residual_torus'].__setitem__('nullity_over_Q',0),lambda x:x['residual_torus'].__setitem__('primitive_weights',{}),lambda x:x['residual_torus'].__setitem__('root_free',False),lambda x:x['residual_torus'].__setitem__('exhaustive',False),lambda x:x['residual_torus']['sources'].pop(),lambda x:x['combined'].__setitem__('input_branches',3),lambda x:x['combined'].__setitem__('output_subcharts',7),lambda x:x['combined'].__setitem__('every_input_point_covered',False),lambda x:x['scope'].__setitem__('singular_runs',1),lambda x:x['scope'].__setitem__('mathematical_coverage_added',True)]
tests={}
for i,mutation in enumerate(mutations):
 value=copy.deepcopy(result);mutation(value)
 try:validate(value)
 except (AssertionError,KeyError,TypeError):tests[f'hostile_{i+1:02d}']=True
 else:tests[f'hostile_{i+1:02d}']=False
assert len(tests)==20 and all(tests.values());atomic(HERE/'results_hostiles.json',{'schema':'KRENN_X5_REP5_FOUR_SUBCHART_NEXT_REDUCTION_HOSTILES_V1','status':'PASS_20_HOSTILES','tests':tests,'solver_runs':0})
print(json.dumps({'status':result['status'],'ranking':[x['branch'] for x in ranking],'factor_choices':[[x['branch'],x['selected_coordinate']] for x in factor_summary],'torus_choice':torus_choice['coordinate'],'sources':8,'hostiles':20,'solves':0},sort_keys=True))
