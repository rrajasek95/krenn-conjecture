#!/usr/bin/env python3
"""Independent algebra/source referee of the rep5 rank-stratified quotient."""
from __future__ import annotations
import collections, hashlib, json, re
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DES=ROOT/'computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-2026-08-25'
PIV=ROOT/'computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25'
PIV_REF=ROOT/'computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25'
K0=ROOT/'computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-terminal-referee-2026-08-25'
PINS={
 DES/'MANIFEST.sha256':'f28dbb2bd003e8ebcfae4eba7945b29507c2a39c417700c17653131cd6674221',
 DES/'generate_design.py':'29953ca4b04b25900d60aee2780300427e693b84f09e7c9bc08713015a7ea650',
 DES/'results_design.json':'d2f7bc1d82781d887e5b1cfe8fb31ee32bbd294c64c6b35f40a838d3b6b2b68c',
 PIV/'MANIFEST.sha256':'00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9',
 PIV/'rep5_p00_guardpivot_k0_Q.sing':'d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1',
 PIV/'rep5_p00_guardpivot_k1_Q.sing':'cdf782ee92b0a019c2a77d6ccc980828c7d0279ebcc3592cced648306fd95e6c',
 PIV/'rep5_p00_guardpivot_k2_Q.sing':'ef6fec2e4ba4baf44c07e9d90e0a1b7fb2624d99c838d901d388e3041bf6aa6d',
 PIV_REF/'FINAL_MANIFEST.sha256':'af4bee0ca8db5391aac9f59cb1e52051d32e66fdb2974a126468b054ca3f5a4b',
 K0/'FINAL_MANIFEST.sha256':'a5dcd93bc79154bce1af90557c8496ca5aa38052f9e6b6206266e498c198e9cf',
 K0/'results_referee.json':'37358baa478e6d220a19cdf955effab940c8b560bc93242e1ed52511c5db31c8',
}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while c:=f.read(1<<20):h.update(c)
 return h.hexdigest()
def replay(manifest):
 count=0
 for line in manifest.read_text().splitlines():
  if not line.strip():continue
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (manifest.parent/p).resolve();assert p.is_file() and sha(p)==d,p;count+=1
 return count
for p,d in PINS.items():assert sha(p)==d,(p,sha(p),d)
manifest_counts={'design':replay(DES/'MANIFEST.sha256'),'pivot':replay(PIV/'MANIFEST.sha256'),'pivot_referee':replay(PIV_REF/'FINAL_MANIFEST.sha256'),'k0_terminal':replay(K0/'FINAL_MANIFEST.sha256')}

# Sparse exact polynomial arithmetic for an independent Cramer replay.
def C(n):return collections.Counter({():n}) if n else collections.Counter()
def V(n):return collections.Counter({(n,):1})
def add(*ps):
 out=collections.Counter()
 for p in ps:out.update(p)
 return collections.Counter({m:c for m,c in out.items() if c})
def neg(p):return collections.Counter({m:-c for m,c in p.items()})
def mul(*ps):
 out=C(1)
 for p in ps:
  nxt=collections.Counter()
  for a,x in out.items():
   for b,y in p.items():nxt[tuple(sorted(a+b))]+=x*y
  out=collections.Counter({m:c for m,c in nxt.items() if c})
 return out
def dot(a,b):return add(*(mul(x,y) for x,y in zip(a,b)))
def cross(a,b):return [add(mul(a[1],b[2]),neg(mul(a[2],b[1]))),add(mul(a[2],b[0]),neg(mul(a[0],b[2]))),add(mul(a[0],b[1]),neg(mul(a[1],b[0])))]
w=[C(1),V('x1'),V('x2')];v=[V('v0'),V('v1'),V('v2')];abar=V('abar');t0=V('t0')
d=add(v[1],neg(mul(w[1],v[0])));reduced=add(abar,neg(mul(t0,w[2])))
u0=[add(mul(reduced,v[1]),mul(w[1],t0,v[2])),neg(add(mul(t0,v[2]),mul(reduced,v[0]))),mul(d,t0)]
n=cross(w,v)
assert dot(u0,v)==C(0) and dot(u0,w)==mul(d,abar)
for m_idx in (1,2):
 tm=V(f't{m_idx}');um=[mul(tm,x) for x in n]
 assert dot(um,v)==C(0) and dot(um,w)==C(0)
 assert cross(u0,um)==[neg(mul(tm,d,abar,x)) for x in v]
 assert add(mul(u0[1],um[2]),neg(mul(u0[2],um[1])))==neg(mul(tm,d,abar,v[0]))

def parse(path):
 text=path.read_text();ring=next(x for x in text.splitlines() if x.startswith('ring r='));variables=ring.split(',(',1)[1].rsplit('),dp;',1)[0].split(',')
 body=text.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];depth=0;start=0;eq=[]
 for i,c in enumerate(body):
  if c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0
  elif c==',' and depth==0:eq.append(body[start:i].strip());start=i+1
 eq.append(body[start:].strip());assert depth==0
 return text,variables,eq

design=json.loads((DES/'results_design.json').read_text());assert design['status']=='PASS_EXACT_SECOND_QUOTIENT_NINE_STRATA_ZERO_SOLVES'
assert design['parent_guard_pivot']=={'charts':3,'variables':88,'generators':6574,'q_source_sha256':[PINS[PIV/f'rep5_p00_guardpivot_k{k}_Q.sing'] for k in range(3)]}
assert len(design['sources'])==9
source_census=[]
for record in design['sources']:
 path=DES/record['path'];assert sha(path)==record['sha256'] and path.stat().st_size==record['bytes']
 text,variables,equations=parse(path);assert text.startswith('// DESIGN INPUT ONLY: zero ideal runs authorized.\n') and 'ring r=0,' in text
 assert len(variables)==len(set(variables))==record['variables'] and len(equations)==len(set(equations))==record['generators']
 assert all(x not in ('0','1','-1') for x in equations)
 k=record['pivot_k'];eliminated_a17={f'a17_{i}{k}' for i in range(3)}
 assert eliminated_a17.isdisjoint(variables)
 parent_text,parent_vars,parent_eq=parse(PIV/f'rep5_p00_guardpivot_k{k}_Q.sing')
 assert len(parent_vars)==88 and len(parent_eq)==6574
 if record['rank_branch']=='rank2_open':
  m_idx=record['t_open'];assert m_idx in (1,2) and len(variables)==84 and len(equations)==6562
  eliminated_a37={'a37_11','a37_12','a37_21','a37_22'};assert eliminated_a37.isdisjoint(variables)
  assert set(record['removed_variables'])==eliminated_a17|eliminated_a37
  assert equations[-1]==parent_eq[-1].replace('*sat-1',f'*t{m_idx}*sat-1')
  assert f't{m_idx}*sat' in equations[-1]
  # Load-bearing materialization defect: the direct A37 entry override was
  # not propagated through already-expanded A35/A36 expressions.
  undeclared={name:len(re.findall(rf'\b{re.escape(name)}\b',text)) for name in sorted(eliminated_a37)}
  assert all(count>0 for count in undeclared.values())
  assert all(not re.search(rf'\b{re.escape(name)}\b',text) for name in eliminated_a17)
 else:
  assert record['rank_branch']=='rank1_closed' and record['t_open'] is None
  assert len(variables)==86 and len(equations)==6570 and 't1' not in variables and 't2' not in variables
  assert set(record['removed_variables'])==eliminated_a17 and equations[-1]==parent_eq[-1]
  assert not re.search(r'\bt[12]\b',text) and all(not re.search(rf'\b{re.escape(name)}\b',text) for name in eliminated_a17)
  undeclared={}
 source_census.append({'pivot_k':k,'branch':record['rank_branch'],'t_open':record['t_open'],'sha256':record['sha256'],'variables':len(variables),'generators':len(equations),'undeclared_eliminated_a37_occurrences':undeclared,'literal_source_valid':not undeclared})

# Exact algebra behind all guard deletion.
# Saturation makes v0, d, abar, beta, b_k and t_m units.  The replayed minor
# is consequently a unit, so rows u0,um are independent while both kill v.
# Hence ker(A06)=span(v).  Writing r_j=rho_j*v gives:
#   A06*r_j^T = rho_j*A06*v^T = 0,
#   A26*r_j^T = rho_j*b,
#   r_j^T-A17*A26*r_j^T = rho_j*(v^T-A17*b).
assert design['rank_lemma']['minor_identity']=='u_0 cross u_m=-t_m*d*abar*v, hence det(rows 0,m; columns 1,2)=-t_m*d*abar*v_0'
assert design['rank_lemma']['inverse_identity']=='v_0*(abar*beta*d*b_k*t_m*sat)=1'
assert design['rank2_open_strata']['generators_breakdown']=={'full_x5':6561,'combined_saturation':1,'guards':0}
assert design['rank1_closed_strata']['generators_breakdown']=={'full_x5':6561,'first_guards':2,'second_guards':6,'combined_saturation':1}
assert design['rank2_open_strata']['forward'].endswith('sat_new=sat_old/t_m and use the forced proportional-row formulas')
assert design['rank2_open_strata']['reverse']=='reconstruct the four eliminated A37 entries and set sat_old=t_m*sat_new'

# Cover logic: on each b_k chart, a point lies in D(t1), D(t2), or in the
# closed quotient V(t1,t2).  Saturation-unit certificates give powers of t1
# and t2 in the ideal; a unit certificate modulo (t1,t2) then forces 1.
assert design['rank2_open_strata']['count']==6 and design['rank1_closed_strata']['count']==3
assert {(x['pivot_k'],x['rank_branch'],x['t_open']) for x in design['sources']}=={(k,'rank2_open',m) for k in range(3) for m in (1,2)}|{(k,'rank1_closed',None) for k in range(3)}
assert design['cover'].startswith('for every b_k chart, D(t1) union D(t2) union V(t1,t2) is exhaustive')

k0=json.loads((K0/'results_referee.json').read_text());assert k0['status']=='PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE' and k0['mathematical_coverage'] is False
assert design['scope']=={'solver_runs':0,'consumed_k0_reused':False,'mathematical_coverage':False,'rep5_closed':False,'performance_claim':False}
for forbidden in ('result.json','ATTEMPT.json','launch_clearance.json','watchdog.json','stdout.log','stderr.log'):
 assert not (DES/forbidden).exists(),forbidden
assert not list(DES.rglob('*.tmp'))

assert sum(x['literal_source_valid'] for x in source_census)==3
out={'schema':'KRENN_X5_REP5_RANK_STRATIFIED_GUARD_PIVOT_DESIGN_REFEREE_V1','status':'REJECT_LITERAL_RANK2_SOURCES_REFERENCE_UNDECLARED_ELIMINATED_A37','producer_manifest_sha256':PINS[DES/'MANIFEST.sha256'],'producer_result_sha256':PINS[DES/'results_design.json'],'abstract_algebra':{'cramer_identities_replayed':True,'rank2_kernel_implication':True,'proportional_a37_rows':True,'cover_decomposition_sound':True},'materialization_defect':'rank2 entry override replaces direct A37 edge requests but not raw A37 names already embedded in expanded A35 partner and A36 reconstruction expressions','rank2_open_strata':{'claimed_count':6,'literal_valid_count':0,'claimed_variables':84,'claimed_generators':6562},'rank1_closed_strata':{'count':3,'literal_valid_count':3,'variables':86,'generators':6570},'executable_cover_all_three_b_k_charts':False,'repair_required':'regenerate the full dependency graph with proportional A37 rows substituted before A35 partner-column and A36 reconstruction expansion, then independently recount and rehash','sources':source_census,'manifest_counts':manifest_counts,'scope':{'design_only':True,'solver_runs':0,'consumed_k0_reused':False,'mathematical_coverage':False,'rep5_closed':False}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'result_sha256':sha(HERE/'results_referee.json')},sort_keys=True))
