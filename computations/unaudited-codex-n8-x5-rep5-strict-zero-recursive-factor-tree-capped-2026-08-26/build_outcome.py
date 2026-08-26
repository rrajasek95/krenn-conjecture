#!/usr/bin/env python3
"""Seal the exact strict-path ledger and the fail-closed global DFS cap outcome."""
import copy,hashlib,json,os,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];C=R/'computations';P=C/'unaudited-codex-n8-x5-rep5-smallest65-third-factor-reduction-design-2026-08-26';S=P/'sources/V_a24_10_Q_design.sing';N=C/'unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25';NR=C/'unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-referee-2026-08-25'
PINS={P/'MANIFEST.sha256':'f3388b5a475d6f8689818e46979b1e620c28bad04ce3daa48a1b8881ea95f060',P/'results_design.json':'f62f44e5b42c53c5db62f1f7005374586a807192b149588920d90888372906db',P/'results_referee.json':'b9b28ea1dcf90c99a28ee8f56ccd67dad68a003444ef0715fcad615b8cd09ca4',S:'cb669d5e09f59d3a32f5b86d2daedc84ad9fa997851eccc83269dc7604db813a',N/'MANIFEST.sha256':'50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1',N/'results_design_v2.json':'4d572fc359430eab8a55ee80ffe98993521e510f9eb48c37ab185742ad19bf00',NR/'results_referee.json':'c6216de12f0df50704a52695edf598d004ffb6d7307877e4f16b17ba20f0225a',NR/'FINAL_MANIFEST.sha256':'3eef6a5bec2f260625189285cdaf171dbfa36530a1f67086528583e4f96db4c6'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
def atomic(p,v):t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
t=S.read_text();names=t.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');exprs=t.split('ideal I=',1)[1].split(';\nprint',1)[0].split(',\n');universe=list(names);idx={n:i for i,n in enumerate(universe)};polys=[]
for e in exprs:
 q={}
 for raw in re.findall(r'[+-]?[^+-]+',e):
  sign=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');c=sign
  if parts[0].isdigit():c*=int(parts.pop(0))
  m=tuple(sorted(idx[x] for x in parts if x));q[m]=q.get(m,0)+c
 q={m:c for m,c in q.items() if c};assert q;polys.append(q)
def canonical(values):
 out=[];seen=set()
 for q in values:
  q={m:c for m,c in q.items() if c}
  if not q:continue
  if len(q)==1 and () in q:return [{():1}]
  key=tuple(sorted(q.items()))
  if key not in seen:seen.add(key);out.append(q)
 return out
def Vchild(P,x):return canonical([{m:c for m,c in q.items() if x not in m} for q in P])
def Dchild(P,x,inv):
 out=[]
 for q in P:
  if all(x in m for m in q):
   z={}
   for m,c in q.items():w=list(m);w.remove(x);z[tuple(w)]=c
   out.append(z)
  else:out.append(q)
 return canonical(out+[{():1,tuple(sorted((x,inv))):-1}])
def stats(active,P):return {'variables':len(active),'generators':len(P),'total_terms':sum(map(len,P)),'degree_mass':sum(len(m) for q in P for m in q),'unit_structural':P==[{():1}]}
active=list(range(len(names)));current=polys;steps=[];unresolved=[]
for step in range(1,100):
 if current==[{():1}]:break
 choices=[]
 for x in active:
  count=sum(all(x in m for m in q) for q in current)
  if count:
   V=Vchild(current,x);choices.append((-count,sum(map(len,V)),len(V),universe[x],x,count,V))
 assert choices
 _,_,_,pivot,x,count,V=min(choices,key=lambda item:item[:4]);inv_name=f'inv_path_{step:02d}';idx[inv_name]=len(universe);universe.append(inv_name);inv=idx[inv_name];D=Dchild(current,x,inv)
 record={'step':step,'pivot':pivot,'divisible_generators':count,'parent':stats(active,current),'D':stats(active+[inv],D),'V':stats([i for i in active if i!=x],V),'V_unit':V==[{():1}],'D_unit':D==[{():1}]}
 steps.append(record)
 if V==[{():1}]:current=D;active.append(inv);record['continuation']='D_due_to_V_unit'
 else:
  if D!=[{():1}]:unresolved.append({'origin_step':step,'pivot':pivot,**stats(active+[inv],D),'polynomials':D,'active':active+[inv]})
  current=V;active=[i for i in active if i!=x];record['continuation']='V'
assert len(steps)==22 and current==[{():1}]
# The smallest unresolved localization leaf still has exact factor reductions, so no pilot is admissible.
smallest=min(unresolved,key=lambda leaf:(leaf['total_terms'],leaf['generators'],leaf['variables'],leaf['origin_step']))
factor_counts={}
for x in smallest.pop('active'):
 count=sum(all(x in m for m in q) for q in smallest['polynomials'])
 if count:factor_counts[universe[x]]=count
smallest.pop('polynomials');assert smallest['origin_step']==20 and smallest['variables']==48 and smallest['generators']==147 and smallest['total_terms']==600 and len(factor_counts)==10
nine=json.loads((N/'results_design_v2.json').read_text())['cover'];assert 'exactly nine strata' in nine
result={'schema':'KRENN_X5_REP5_STRICT_ZERO_RECURSIVE_FACTOR_TREE_CAPPED_V1','status':'FAIL_CLOSED_GLOBAL_FACTOR_TREE_NODE_CAP_NO_CLOSURE_NO_PILOT','pins':{str(p.relative_to(R)):h for p,h in PINS.items()},'input':{'sha256':PINS[S],'variables':64,'generators':3321,'total_terms':118979},'nine_stratum_coverage':{'statement':nine,'ledger_preserved':True,'local_stratum_branch_only':True,'global_rep5_closure':False},'strict_path':{'policy':'max complete-factor count, then minimum V terms, V generators, coordinate name','steps':steps,'decisions':22,'terminal_unit':True,'unresolved_localization_leaves':len(unresolved)},'smallest_unresolved_leaf':{**smallest,'complete_factor_candidates':factor_counts,'exact_reduction_exhausted':False,'pilot_admissible':False},'global_dfs':{'policy':'same exact D/V policy, depth first over both children','explicit_node_cap':1000,'last_committed_sample':{'nodes':1000,'structural_unit_leaves':486,'factor_exhausted_nonunit_leaves_observed':0},'terminal':False,'exception':'RuntimeError: node cap','closure_proved':False,'ephemeral_output_artifacts':0},'interrupted_optimized_retry':{'sealed_coverage':False,'artifacts':0,'reason':'stopped immediately on manager request to seal first capped outcome'},'scope':{'singular_runs':0,'ideal_solves':0,'modular_pilots_prepared':0,'modular_pilots_launched':0,'mathematical_coverage_added':False}}
atomic(H/'results_capped_outcome.json',result)
def validate(v):
 assert v['status']=='FAIL_CLOSED_GLOBAL_FACTOR_TREE_NODE_CAP_NO_CLOSURE_NO_PILOT' and v['input']['sha256']==PINS[S] and v['strict_path']['decisions']==22 and v['strict_path']['terminal_unit'] and v['strict_path']['unresolved_localization_leaves']==18
 assert v['smallest_unresolved_leaf']['origin_step']==20 and v['smallest_unresolved_leaf']['total_terms']==600 and len(v['smallest_unresolved_leaf']['complete_factor_candidates'])==10 and not v['smallest_unresolved_leaf']['exact_reduction_exhausted'] and not v['smallest_unresolved_leaf']['pilot_admissible']
 assert v['global_dfs']['explicit_node_cap']==1000 and v['global_dfs']['last_committed_sample']=={'nodes':1000,'structural_unit_leaves':486,'factor_exhausted_nonunit_leaves_observed':0} and not v['global_dfs']['terminal'] and not v['global_dfs']['closure_proved']
 assert v['nine_stratum_coverage']['ledger_preserved'] and v['nine_stratum_coverage']['local_stratum_branch_only'] and not v['nine_stratum_coverage']['global_rep5_closure'] and v['scope']['singular_runs']==v['scope']['modular_pilots_prepared']==v['scope']['modular_pilots_launched']==0
mut=[lambda v:v.__setitem__('status','PASS'),lambda v:v['strict_path'].__setitem__('decisions',21),lambda v:v['strict_path'].__setitem__('terminal_unit',False),lambda v:v['strict_path'].__setitem__('unresolved_localization_leaves',17),lambda v:v['smallest_unresolved_leaf'].__setitem__('origin_step',19),lambda v:v['smallest_unresolved_leaf'].__setitem__('exact_reduction_exhausted',True),lambda v:v['smallest_unresolved_leaf'].__setitem__('pilot_admissible',True),lambda v:v['global_dfs'].__setitem__('terminal',True),lambda v:v['global_dfs'].__setitem__('closure_proved',True),lambda v:v['global_dfs'].__setitem__('explicit_node_cap',999),lambda v:v['global_dfs']['last_committed_sample'].__setitem__('nodes',999),lambda v:v['nine_stratum_coverage'].__setitem__('ledger_preserved',False),lambda v:v['nine_stratum_coverage'].__setitem__('global_rep5_closure',True),lambda v:v['scope'].__setitem__('singular_runs',1),lambda v:v['scope'].__setitem__('modular_pilots_launched',1)]
tests={}
for i,f in enumerate(mut,1):
 x=copy.deepcopy(result);f(x)
 try:validate(x)
 except (AssertionError,KeyError,TypeError):tests[f'hostile_{i:02d}']=True
 else:tests[f'hostile_{i:02d}']=False
assert len(tests)==15 and all(tests.values());atomic(H/'results_hostiles.json',{'status':'PASS_15_CAPPED_OUTCOME_HOSTILES','tests':tests,'solver_runs':0});print(json.dumps({'status':result['status'],'strict_steps':22,'unresolved_leaves':len(unresolved),'smallest':[48,147,600],'smallest_factors':10,'dfs_nodes':1000,'dfs_unit_leaves':486,'dfs_open_observed':0,'terminal':False,'solves':0},sort_keys=True))
