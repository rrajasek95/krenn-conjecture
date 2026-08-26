#!/usr/bin/env python3
"""Build an exact torus-gauge decomposition of consumed rep2 group16; never solve."""
from __future__ import annotations
import hashlib,importlib.util,itertools,json,os,re,sys
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent; ROOT=H.parents[1]
RUN=ROOT/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25'
DES=ROOT/'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25'
PINS={
 RUN/'TERMINAL_MANIFEST.sha256':'1aad2a2c87918d4ac1b931d97e5da09447b31fb7527fa35c7932fad52d7a2117',
 RUN/'batch_result.json':'1eb6d08fb79b44c76035dba1ed2542b8c006ab9cb4b8217452c01e3223c4ca05',
 RUN/'results/group016.json':'f26a09796fc02e930d069a6acd0a8d77bcefe29b7e35517c1f8ae0634fc5d760',
 RUN/'sources/rep2_group016_Q.sing':'79a2cf5c70cf939e434cf445c98d7a5e132f68ddd2253f7757d06d4450da01c8',
 RUN/'canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',
 RUN/'source_ledger.json':'20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e',
 DES/'MANIFEST.sha256':'ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2',
 DES/'generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic_text(p,s):
 t=p.with_suffix(p.suffix+'.tmp'); t.parent.mkdir(parents=True,exist_ok=True); t.write_text(s); os.replace(t,p)
def replay(m):
 n=0
 for line in m.read_text().splitlines():
  if not line.strip(): continue
  d,x=line.split(None,1); p=(m.parent/x.strip()).resolve(); assert p.is_file() and sha(p)==d,(p,d); n+=1
 return n
for p,d in PINS.items(): assert sha(p)==d,(p,sha(p),d)
terminal_entries=replay(RUN/'TERMINAL_MANIFEST.sha256')
census=json.loads((RUN/'canonical_census.json').read_text()); rec=census['groups'][16]
assert rec['canonical_chart']==[0,0,0,1,'z',2,0,1] and rec['exact_Q_source_sha256']==PINS[RUN/'sources/rep2_group016_Q.sing'] and rec['exact_Q_source_bytes']==1834840
lane=json.loads((RUN/'results/group016.json').read_text()); assert lane['status']=='FAIL_CLOSED_RESOURCE' and lane['termination']=='NATIVE_WALL_CAP_240' and lane['automatic_relaunch'] is False and lane['source_sha256']==rec['exact_Q_source_sha256']
batch=json.loads((RUN/'batch_result.json').read_text()); assert batch['completed'][-1]=={'group_id':16,'result_sha256':PINS[RUN/'results/group016.json'],'status':'FAIL_CLOSED_RESOURCE'} and batch['stop']=={'group_id':16,'status':'FAIL_CLOSED_RESOURCE'} and batch['relaunch'] is False
# Regenerate the canonical source independently from the pinned exact builder.
spec=importlib.util.spec_from_file_location('rep2_g16_builder',DES/'generate_design.py'); assert spec and spec.loader
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); engine=m.load_engine(); m.configure_engine(engine)
base=m.build_program(engine,tuple(rec['canonical_chart'])); assert base.endswith('quit;\n')
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
rebuilt=(base[:-len('quit;\n')]+ep).encode(); assert hashlib.sha256(rebuilt).hexdigest()==rec['exact_Q_source_sha256'] and rebuilt==(RUN/'sources/rep2_group016_Q.sing').read_bytes()
source=rebuilt.decode(); variables=source.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(','); equations=source.split('ideal I=',1)[1].split(';\nprint',1)[0].split(',\n')
assert len(variables)==91 and len(equations)==len(set(equations))==6577
# Four exact edge-scaling characters. Every supported matching has total weight zero,
# and both guard sums are homogeneous under the corresponding physical edge weights.
bases={
 'lambda35':{'04':-1,'06':-1,'23':1,'35':1},
 'lambda56':{'06':1,'14':-1,'17':-1,'26':1,'56':1},
 'lambda57':{'17':1,'23':-1,'26':-1,'57':1},
 'lambda67':{'12':-1,'67':1},
}
for weights in bases.values():
 for matching in m.SUPPORTED: assert sum(weights.get(''.join(map(str,e)),0) for e in matching)==0
 assert weights.get('57',0)==weights.get('17',0)+weights.get('56',0)
 assert weights.get('56',0)==weights.get('26',0)+weights.get('57',0)
# Derive chart-variable weights for the z chart, then parse every polynomial exactly.
edge_names=tuple(bases); edge_vectors={edge:tuple(bases[b].get(edge,0) for b in edge_names) for edge in ('04','06','12','14','17','23','26','35','56','57','67')}
weights={}
for v in variables:
 q=re.fullmatch(r'a(\d\d)_\d\d',v); weights[v]=edge_vectors[q.group(1)] if q else (0,0,0,0)
for v in variables:
 if v.startswith('yn'): weights[v]=(0,0,1,0)
 if v=='abar' or v.startswith('t'): weights[v]=(-1,1,-1,0)
 if v=='beta': weights[v]=(1,0,0,0)
 if v=='sat': weights[v]=(0,-1,-1,0)
add=lambda a,b:tuple(x+y for x,y in zip(a,b))
class Parser:
 def __init__(self,text): self.tokens=re.findall(r'[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]',text); self.i=0
 def expr(self):
  z=self.term()
  while self.i<len(self.tokens) and self.tokens[self.i] in '+-': self.i+=1; z|=self.term()
  return z
 def term(self):
  z=self.factor()
  while self.i<len(self.tokens) and self.tokens[self.i]=='*':
   self.i+=1; q=self.factor(); z={add(a,b) for a in z for b in q}
  return z
 def factor(self):
  x=self.tokens[self.i]
  if x=='-': self.i+=1; return self.factor()
  if x=='(':
   self.i+=1; z=self.expr(); assert self.tokens[self.i]==')'; self.i+=1; return z
  self.i+=1; return {(0,0,0,0)} if x.isdigit() else {weights[x]}
poly_weights=[]
for equation in equations:
 p=Parser(equation); ws=p.expr(); assert p.i==len(p.tokens) and len(ws)==1; poly_weights.append(next(iter(ws)))
hist=[dict(sorted(Counter(w[i] for w in poly_weights).items())) for i in range(4)]
assert hist==[{ -1:6,0:6571},{0:6571,1:6},{0:6562,1:15},{0:6577}]
# Saturation makes beta, abar, and v0=a57_00 nonzero. Their character matrix
# has determinant one; lambda1=beta^-1, lambda3=v0^-1,
# lambda2=(abar*beta*v0)^-1 sends all three to 1 without roots.
gauge_matrix=[[1,0,0],[-1,1,-1],[0,0,1]]
det=(gauge_matrix[0][0]*(gauge_matrix[1][1]*gauge_matrix[2][2]-gauge_matrix[1][2]*gauge_matrix[2][1]))
assert det==1 and weights['beta'][:3]==tuple(gauge_matrix[0]) and weights['abar'][:3]==tuple(gauge_matrix[1]) and weights['a57_00'][:3]==tuple(gauge_matrix[2])
def substitute(text,mapping):
 pattern=r'\b(?:'+'|'.join(map(re.escape,mapping))+r')\b'; return re.sub(pattern,lambda q:mapping[q.group()],text)
base_gauge={'beta':'1','abar':'1','a57_00':'1'}
a67=[f'a67_{i}{j}' for i,j in itertools.product(range(3),repeat=2)]; a12=[f'a12_{i}{j}' for i,j in itertools.product(range(3),repeat=2)]
strata=[]
def emit(name,mapping,kind,pivot):
 newvars=[v for v in variables if v not in mapping]; neweq=[substitute(e,mapping) for e in equations]
 assert len(neweq)==len(set(neweq))==6577 and all(e not in ('0','1','-1') for e in neweq)
 text='\n'.join(['// REP2 GROUP16 TORUS-GAUGE DESIGN INPUT ONLY: zero ideal runs authorized.','option(noredefine);',f"ring r=0,({','.join(newvars)}),dp;",'ideal I='+',\n'.join(neweq)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','quit;',''])
 path=H/'sources'/name; atomic_text(path,text)
 strata.append({'kind':kind,'pivot':pivot,'path':str(path.relative_to(H)),'sha256':sha(path),'bytes':path.stat().st_size,'variables':len(newvars),'generators':len(neweq),'unique_generators':len(set(neweq)),'trivial_generators':0})
for v in a67: emit(f'group16_A67open_{v[-2:]}_Q_design.sing',{**base_gauge,v:'1'},'A67_entry_open',v)
zero67={v:'0' for v in a67}
for v in a12: emit(f'group16_A67zero_A12open_{v[-2:]}_Q_design.sing',{**base_gauge,**zero67,v:'1'},'A67_zero_A12_entry_open',v)
emit('group16_A67zero_A12zero_Q_design.sing',{**base_gauge,**zero67,**{v:'0' for v in a12}},'A67_zero_A12_zero',None)
assert Counter(x['variables'] for x in strata)==Counter({87:9,78:9,70:1})
# There is no source-labelled vertex automorphism and no simultaneous-S3 map to groups0..15.
fixed={(0,3),(1,6),(2,7),(4,5)}; variable={(0,4),(1,2),(3,5),(6,7)}; added={(0,6),(1,4),(1,7),(2,3),(2,6),(5,6),(5,7)}
image=lambda S,p:{tuple(sorted((p[a],p[b]))) for a,b in S}
autos=[p for p in itertools.permutations(range(8)) if image(fixed,p)==fixed and image(variable,p)==variable and image(added,p)==added]
assert autos==[tuple(range(8))]
raw16={tuple(x) for x in rec['raw_members']}; assert all(raw16.isdisjoint({tuple(x) for x in census['groups'][gid]['raw_members']}) for gid in range(16))
timings=[]
for gid in range(1,17):
 r=json.loads((RUN/'results'/f'group{gid:03d}.json').read_text()); timings.append({'group_id':gid,'chart':census['groups'][gid]['canonical_chart'],'source_sha256':r['source_sha256'],'status':r['status'],'wall_seconds':r['wall_seconds'],'peak_group_rss_bytes':r['peak_group_rss_bytes'],'groebner_size':1 if 'GROEBNER_SIZE=1' in r.get('stdout','') else None})
fast=[x for x in timings if x['group_id']<16]; assert len(fast)==15 and all(x['status']=='UNIT_IDEAL_EXACT_Q' and x['groebner_size']==1 for x in fast)
result={'schema':'KRENN_X5_REP2_GROUP16_TORUS_GAUGE_DECOMPOSITION_DESIGN_V1','status':'PASS_EXACT_19_STRATUM_DESIGN_ZERO_SOLVES','consumed_attempt':{'group_id':16,'chart':rec['canonical_chart'],'source_sha256':rec['exact_Q_source_sha256'],'result_sha256':PINS[RUN/'results/group016.json'],'status':lane['status'],'termination':lane['termination'],'wall_seconds':lane['wall_seconds'],'peak_group_rss_bytes':lane['peak_group_rss_bytes'],'relaunch_authorized':False},'comparison_groups0_15':{'group0_sealed_separately':True,'groups1_15_unit':True,'min_wall_seconds':min(x['wall_seconds'] for x in fast),'max_wall_seconds':max(x['wall_seconds'] for x in fast),'max_peak_rss_bytes':max(x['peak_group_rss_bytes'] for x in fast),'lanes':timings},'canonical_metadata':{'raw_charts':972,'canonical_groups':162,'members_each':6,'group16_raw_members':rec['raw_members']},'source_rebuild':{'variables':91,'generators':6577,'bytes':len(rebuilt),'sha256':hashlib.sha256(rebuilt).hexdigest(),'byte_identical':True},'torus':{'edge_character_bases':bases,'matching_products_weight_zero':True,'guard_character_relations':True,'polynomial_weight_histograms':dict(zip(edge_names,hist)),'unit_gauge_coordinates':['beta','abar','a57_00'],'unit_gauge_character_matrix':gauge_matrix,'unit_gauge_determinant':det,'gauge_parameters':{'lambda35':'beta^-1','lambda57':'a57_00^-1','lambda56':'(abar*beta*a57_00)^-1'},'base_gauge_variables':88,'residual_character':'lambda67: A12 weight -1, A67 weight +1'},'decomposition':{'cover_identity':'union_{i,j} D(A67_ij) plus V(A67) intersect union_{i,j} D(A12_ij) plus V(A67,A12)','forward':'apply the three rational unit gauges, then use lambda67 to set the selected nonzero pivot entry to 1','reverse':'every emitted gauge slice is a literal specialization inside the original saturated chart; undoing torus parameters restores the source-labelled point','stratum_count':19,'variable_histogram':dict(sorted(Counter(x['variables'] for x in strata).items())),'sources':strata},'symmetry_obstruction':{'source_labelled_vertex_automorphism_count':len(autos),'only_vertex_automorphism':list(autos[0]),'group16_simultaneous_s3_orbit_disjoint_from_closed_groups0_15':True,'transport_to_closed_group_found':False},'order_scope':{'original_order':'dp','emitted_order':'dp','alternative_order_proved_faster':False,'block_order_claimed':False},'pins':{str(p.relative_to(ROOT)):d for p,d in PINS.items()},'scope':{'design_only':True,'singular_runs':0,'ideal_runs':0,'group16_closed':False,'rep2_closed':False,'performance_claim':False,'relaunch_or_reuse_authorized':False,'next_valid_step':'independent design audit, then fresh held pilots per stratum only if separately cleared'}}
atomic_text(H/'results_design.json',json.dumps(result,indent=2,sort_keys=True)+'\n')
assert not (H/'__pycache__').exists()
print(json.dumps({'status':result['status'],'strata':19,'variables':result['decomposition']['variable_histogram'],'runs':0},sort_keys=True))
