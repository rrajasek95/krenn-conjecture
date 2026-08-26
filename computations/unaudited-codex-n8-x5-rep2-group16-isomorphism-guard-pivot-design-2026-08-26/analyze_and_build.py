#!/usr/bin/env python3
"""Group16 exact transport census and three-chart guard-pivot quotient; zero solve."""
from __future__ import annotations
import collections,hashlib,importlib.util,itertools,json,os,re
from array import array
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
DES=R/'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25'
BATCH=R/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25'
TERM=R/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-terminal-referee-2026-08-26'
GROUP0=R/'computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25/rep2_corrected_all_equal_y_Q.sing'
PINS={DES/'MANIFEST.sha256':'ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2',DES/'generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc',BATCH/'MANIFEST.sha256':'d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c',BATCH/'TERMINAL_MANIFEST.sha256':'1aad2a2c87918d4ac1b931d97e5da09447b31fb7527fa35c7932fad52d7a2117',TERM/'FINAL_MANIFEST.sha256':'066347c8af9a579b8f09d1c1eebf0197e819753da839f30708616287c4336196',TERM/'results_referee.json':'4fd305ebb3ed3766cbe61b9bccceb5c3b2bb75caecae39111229e9651d8f0c8e',GROUP0:'5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf'}
RECORD=(0,0,0,1,'z',2,0,1);GROUP16_SHA='79a2cf5c70cf939e434cf445c98d7a5e132f68ddd2253f7757d06d4450da01c8'
SUPPORT={(0,3),(1,6),(2,7),(4,5),(0,4),(1,2),(3,5),(6,7),(0,6),(1,4),(1,7),(2,3),(2,6),(5,6),(5,7)};FIXED={(0,3),(1,6),(2,7),(4,5)};ELIMINATED=(5,6)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,text):t=p.with_suffix(p.suffix+'.tmp');t.write_text(text);os.replace(t,p)
def load_rep2():
 s=importlib.util.spec_from_file_location('sealed_rep2_design',DES/'generate_design.py');assert s and s.loader
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def parse(path):
 text=path.read_text();ring=next(x for x in text.splitlines() if x.startswith('ring r='));variables=ring.split(',(',1)[1].rsplit('),dp;',1)[0].split(',');body=text.split('ideal I=',1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0];equations=[];depth=start=0
 for pos,ch in enumerate(body):
  depth+=ch=='(';depth-=ch==')'
  if ch==',' and depth==0:equations.append(body[start:pos].strip());start=pos+1
 equations.append(body[start:].strip());assert depth==0
 return variables,equations
def rows(variables,equations):
 token=re.compile(r'\b(?:'+'|'.join(map(re.escape,sorted(variables,key=len,reverse=True)))+r')\b');out={v:array('I',[0])*6561 for v in variables}
 for i,equation in enumerate(equations[:6561]):
  for v,n in collections.Counter(token.findall(equation)).items():out[v][i]=n
 return out
def word(i):
 out=[0]*8
 for j in range(7,-1,-1):out[j],i=i%3,i//3
 return tuple(out)
def wi(w):
 out=0
 for x in w:out=3*out+x
 return out
words=[word(i) for i in range(6561)];perms=list(itertools.permutations(range(3)));maps={''.join(map(str,p)):[wi(tuple(p[x] for x in w)) for w in words] for p in perms}
def signature(row,mapping):return array('I',(row[i] for i in mapping)).tobytes()
def multiset(rs,mapping):return collections.Counter(signature(row,mapping) for row in rs.values())
for path,digest in PINS.items():assert sha(path)==digest,(path,sha(path),digest)
assert sha(BATCH/'sources/rep2_group016_Q.sing')==GROUP16_SHA
terminal=json.loads((TERM/'results_referee.json').read_text());assert terminal['failed_group_id']==16 and terminal['failure_classification']=='NATIVE_WALL_CAP_240_ZERO_MATHEMATICAL_COVERAGE' and terminal['closed_union']==list(range(16))
# Source-labelled support permits no nonidentity site permutation.
site=[]
for p in itertools.permutations(range(8)):
 im=lambda edges:{tuple(sorted((p[i],p[j]))) for i,j in edges}
 if im(SUPPORT)==SUPPORT and im(FIXED)==FIXED and tuple(sorted((p[5],p[6])))==ELIMINATED:site.append(p)
assert site==[tuple(range(8))]
paths={0:GROUP0};paths.update({i:BATCH/f'sources/rep2_group{i:03d}_Q.sing' for i in range(1,17)})
parsed={i:(*parse(path),) for i,path in paths.items()};occ={i:rows(*parsed[i]) for i in parsed};identity=list(range(6561));source_signature=multiset(occ[16],identity);transport=[]
for target in range(17):
 matches=[key for key,mapping in maps.items() if source_signature==multiset(occ[target],mapping)]
 assert matches==(['012'] if target==16 else [])
 witness=None
 if not matches:
  target_sigs=collections.Counter(signature(row,identity) for row in occ[target].values())
  source_by=collections.defaultdict(list)
  for name,row in occ[16].items():source_by[signature(row,identity)].append(name)
  for packed,names in sorted(source_by.items()):
   if len(names)>target_sigs[packed]:witness={'source_variables':sorted(names),'signature_sha256':hashlib.sha256(packed).hexdigest(),'source_multiplicity':len(names),'target_multiplicity':target_sigs[packed]};break
 transport.append({'target_group_id':target,'color_permutations_tested':6,'exact_occurrence_multiset_matches':matches,'mismatch_witness':witness})
# Strict smaller three-chart localization, independently materialized from the sealed engine.
m=load_rep2();engine=m.load_engine();m.configure_engine(engine);old_entry,old_variables,det,outside=engine.build_context(RECORD);p=RECORD[1];P=engine.product('abar','beta',outside,det)
def b(h):return engine.summation(engine.product(old_entry((2,6),h,l),old_entry(m.OUTSIDE,p,l)) for l in m.COLORS)
bs=[b(h) for h in m.COLORS]
def build(k):
 def solved(i):
  numerator=engine.difference(old_entry(m.OUTSIDE,p,i),engine.summation(engine.product(old_entry((1,7),i,h),bs[h]) for h in m.COLORS if h!=k))
  return engine.product(numerator,P,'sat')
 def entry(edge,i,j):return solved(i) if edge==(1,7) and j==k else old_entry(edge,i,j)
 variables=[v for v in old_variables if v not in {f'a17_{i}{k}' for i in m.COLORS}];equations=[]
 for tensor_word in itertools.product(m.COLORS,repeat=8):
  value=engine.amplitude(entry,tensor_word);equations.append(engine.difference(value,'1') if len(set(tensor_word))==1 else value)
 for i,j in itertools.product(m.COLORS,repeat=2):
  if j!=p:equations.append(engine.summation(engine.product(entry((0,6),i,l),entry(m.OUTSIDE,j,l)) for l in m.COLORS))
 for i,j in itertools.product(m.COLORS,repeat=2):
  if j==p:continue
  correction=engine.summation(engine.product(entry((1,7),i,h),entry((2,6),h,l),entry(m.OUTSIDE,j,l)) for h,l in itertools.product(m.COLORS,repeat=2))
  equations.append(engine.difference(entry(m.OUTSIDE,j,i),correction))
 equations.append(engine.product(P,bs[k],'sat')+'-1')
 assert len(variables)==len(set(variables))==88 and len(equations)==len(set(equations))==6574 and all(x not in ('0','1','-1') for x in equations)
 program='\n'.join(['// REP2 GROUP16 STRICT GUARD-PIVOT DESIGN ONLY: zero ideal runs authorized.','option(noredefine);',f"ring r=0,({','.join(variables)}),dp;",'ideal I='+',\n'.join(equations)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','ideal G=slimgb(I);','print("GROEBNER_SIZE="+string(size(G)));','poly remainder=reduce(1,G);','print("UNIT_REMAINDER="+string(remainder));','if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }','quit;',''])
 return program,variables,equations
inputs=[]
for k in range(3):
 program,variables,equations=build(k);path=H/f'rep2_group016_guardpivot_k{k}_Q.sing';atomic(path,program);inputs.append({'pivot_k':k,'path':path.name,'sha256':sha(path),'bytes':path.stat().st_size,'variables':88,'generators':6574,'solver_runs':0})
proof={'definitions':{'v':'row_p(A57)','b_h':'sum_l A26[h,l]*A57[p,l]','P':'abar*beta*A57[p,q]*d','N_i':'A57[p,i]-sum_{h!=k}A17[i,h]*b_h','substitution':'A17[i,k]=N_i*P*sat','new_saturation':'P*b_k*sat-1'},'removed_guard_identity':'A57[p,i]-sum_h A17[i,h]*b_h=N_i*(1-P*b_k*sat)','cover':'the old j=p,i=q guard gives nonzero A57[p,q]=sum_h A17[q,h]b_h, hence at least one b_k is nonzero','forward':'on D(b_k), sat_new=sat_old/b_k and the three column-k A17 entries are solved monically','reverse':'sat_old=b_k*sat_new restores P*sat_old=1; the displayed identity restores all three removed guards','chart_union':'D(b0) union D(b1) union D(b2) covers the full group16 chart; no symmetry identification is used'}
out={'schema':'KRENN_X5_REP2_GROUP16_ISOMORPHISM_GUARD_PIVOT_DESIGN_V1','status':'PASS_NO_PREFIX_TRANSPORT_STRICT_88_6574_THREE_CHART_QUOTIENT_ZERO_SOLVES','group16':{'chart':list(RECORD),'source_sha256':GROUP16_SHA,'parent_variables':91,'parent_generators':6577,'termination':'NATIVE_WALL_CAP_240','mathematical_coverage':False},'transport':{'comparison_groups':list(range(17)),'site_permutations_enumerated':40320,'source_label_preserving_site_automorphisms':[list(x) for x in site],'color_permutations_each':6,'ledger':transport,'group16_covers':[16],'closed_prefix_transportable_to_group16':[],'arbitrary_ring_variable_bijection_filter':'exact variable occurrence vectors across all 6561 source-labelled amplitude generators'},'quotient':{'chart_count':3,'variables_each':88,'generators_each':6574,'removed_variables_each':3,'removed_guards_each':3,'new_variables':0,'full_x5':6561,'remaining_first_guards':6,'remaining_second_guards':6,'combined_saturation':1,'proof':proof,'inputs':inputs},'pins':{str(path.relative_to(R)):digest for path,digest in PINS.items()},'scope':{'singular_runs':0,'ideal_runs':0,'mathematical_coverage':False,'group16_closed':False,'rep2_closed':False}}
atomic(H/'results_group16_design.json',json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'transport':0,'charts':3,'variables':88,'generators':6574,'runs':0},sort_keys=True))
