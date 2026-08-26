#!/usr/bin/env python3
"""Exact guard-pivot refinement of consumed rep5 p00; generate only, never solve."""
from __future__ import annotations
import hashlib,importlib.util,itertools,json,os
from pathlib import Path

H=Path(__file__).resolve().parent;R=H.parents[1]
BASE=R/'computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25'
RUN=R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25'
REF=R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-v2-terminal-referee-2026-08-25'
PINS={BASE/'MANIFEST.sha256':'33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c',BASE/'generate_design.py':'3844eadf4a9e21c2feb012cbd684c22ca7611f4d22f87659e19952d0381614f4',BASE/'results_rep5_contraction_design.json':'b2ba095f4f702ac2138cb40d45b7721a8df9b338900282020e83b791264df59b',BASE/'rep5_guard_minor_tiny_y_p32003.sing':'33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97',RUN/'result.json':'d3f1fcdfc61695c0f3557d99efb5ad79c777cc74aa85643f92e6cce7e13a22eb',RUN/'ATTEMPT.json':'4b7825188f47cacb18e55adb2c26d4b6516ea391d581f46a7d05c37f71268388',REF/'FINAL_MANIFEST.sha256':'69b6e61f2a493a5c0fb1edd589105d2d3b38d0bec3450314fa56a1411a80241a',REF/'results_referee.json':'0cf977520416ab3de81748195b824913a9ad159d7660d059f5f3e03767199875'}
RECORD=(0,0,0,0,'y',0,0,1)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load():
 s=importlib.util.spec_from_file_location('sealed_rep5',BASE/'generate_design.py');assert s and s.loader
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def atomic(p,text):t=p.with_suffix(p.suffix+'.tmp');t.write_text(text);os.replace(t,p)
for p,x in PINS.items():assert sha(p)==x,(p,sha(p),x)
terminal=json.loads((REF/'results_referee.json').read_text());assert terminal['status']=='PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE' and terminal['termination']=='NATIVE_WALL_CAP_180'
m=load();old_entry,old_variables,det,outside=m.build_context(RECORD);p=RECORD[1]
P=m.product('abar','beta',outside,det)
def b(h):return m.summation(m.product(old_entry((2,6),h,l),old_entry((3,7),p,l)) for l in m.COLORS)
bs=[b(h) for h in m.COLORS]
def build(k,ring='0'):
 def solved(i):
  numerator=m.difference(old_entry((3,7),p,i),m.summation(m.product(old_entry((1,7),i,h),bs[h]) for h in m.COLORS if h!=k))
  return m.product(numerator,P,'sat')
 def entry(edge,i,j):
  if edge==(1,7) and j==k:return solved(i)
  return old_entry(edge,i,j)
 variables=[v for v in old_variables if v not in {f'a17_{i}{k}' for i in m.COLORS}]
 equations=[]
 for word in itertools.product(m.COLORS,repeat=8):
  value=m.amplitude(entry,word);equations.append(m.difference(value,'1') if len(set(word))==1 else value)
 for i,j in itertools.product(m.COLORS,repeat=2):
  if j!=p:equations.append(m.summation(m.product(entry((0,6),i,l),entry((3,7),j,l)) for l in m.COLORS))
 for i,j in itertools.product(m.COLORS,repeat=2):
  if j==p:continue
  correction=m.summation(m.product(entry((1,7),i,h),entry((2,6),h,l),entry((3,7),j,l)) for h,l in itertools.product(m.COLORS,repeat=2))
  equations.append(m.difference(entry((3,7),j,i),correction))
 equations.append(m.product(P,bs[k],'sat')+'-1')
 assert len(variables)==88 and len(set(variables))==88
 assert len(equations)==6574 and len(set(equations))==6574 and all(x not in ('0','1','-1') for x in equations)
 lines=['option(noredefine);',f"ring r={ring},({','.join(variables)}),dp;",'ideal I='+',\n'.join(equations)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','ideal G=slimgb(I);','print("GROEBNER_SIZE="+string(size(G)));','poly remainder=reduce(1,G);','print("UNIT_REMAINDER="+string(remainder));','if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }','quit;','']
 return '\n'.join(lines),variables,equations

inputs=[]
for k in range(3):
 program,variables,equations=build(k,'0');path=H/f'rep5_p00_guardpivot_k{k}_Q.sing';atomic(path,program)
 inputs.append({'pivot_k':k,'path':path.name,'sha256':sha(path),'bytes':path.stat().st_size,'variables':len(variables),'generators':len(equations),'ring':'Q'})

# Exact algebraic proof ledger.  The removed j=p guard for each row i is
# N_i*(1-P*b_k*sat), hence belongs to the new saturation ideal.
proof={
 'definitions':{'b_h':'sum_l A26[h,l]*A37[p,l]','P':'abar*beta*A37[p,q]*d','N_i':'A37[p,i]-sum_{h!=k} A17[i,h]*b_h','substitution':'A17[i,k]=N_i*P*sat','new_saturation':'P*b_k*sat-1'},
 'removed_guard_identity':'A37[p,i]-sum_h A17[i,h]*b_h = N_i*(1-P*b_k*sat)',
 'cover':'old j=p,i=q guard gives A37[p,q]=sum_h A17[q,h]*b_h; old saturation makes A37[p,q] nonzero, so at least one of b_0,b_1,b_2 is nonzero',
 'forward':'on b_k!=0 set sat_new=sat_old/b_k and use the monic formulas for the three eliminated A17 column-k entries',
 'reverse':'set sat_old=b_k*sat_new; new saturation gives P*sat_old=1 and the removed guards follow from the displayed identity',
 'chart_union':'three k charts cover the full original p00 chart; no symmetry identification is assumed',
}
result={'schema':'KRENN_X5_REP5_POST_TIMEOUT_GUARD_PIVOT_QUOTIENT_DESIGN_V1','status':'PASS_STRICT_SMALLER_EXACT_THREE_CHART_DESIGN_ZERO_SOLVES','consumed_parent':{'chart':list(RECORD),'variables':91,'generators':6577,'termination':'NATIVE_WALL_CAP_180','result_sha256':PINS[RUN/'result.json'],'attempt_consumed':True,'relaunch_authorized':False},'reduction':{'variables':88,'generators':6574,'variables_removed':[f'A17[i,{k}] for i=0,1,2 (per k chart)'],'guards_removed':3,'new_variables':0,'full_x5_equations':6561,'remaining_first_guard':6,'remaining_second_guard':6,'combined_saturation':1},'proof':proof,'inputs':inputs,'alternative_order':{'tested_by_solver':False,'recommended_future_order':'block remaining A17/A26/A37 guard variables before other source variables only after independent symbolic order audit','claim':'no performance claim; strict quotient is the promoted design improvement'},'pins':{str(p.relative_to(R)):x for p,x in PINS.items()},'scope':{'design_inputs_materialized':3,'solver_runs':0,'parent_relaunched':False,'mathematical_coverage':False,'rep5_closed':False}}
atomic(H/'results_design.json',json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'variables':88,'generators':6574,'charts':3,'runs':0},sort_keys=True))
