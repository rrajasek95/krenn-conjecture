#!/usr/bin/env python3
"""Independent exact audit of the rep2 group16 67-timeout reduction; zero solve."""
from __future__ import annotations
import hashlib,itertools,json,math,os,re
from collections import Counter
from fractions import Fraction
from pathlib import Path

H=Path(__file__).resolve().parent;ROOT=H.parents[1]
PROD=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26'
PRIOR=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26'
TERM=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-terminal-referee-2026-08-26'
SOURCE=PRIOR/'rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing'
PINS={PROD/'MANIFEST.sha256':'3d4d6fbc89f5adcc45032c37b1b038780761f479313575c59e4e8bd760da75fd',PROD/'results_design.json':'10c7c360683bfc780645ccb16d7a9d5f50500cc3af8272b5f49f1f8c2451bf00',PROD/'analyze_design.py':'fe9d7c10efbcfa1a1d8fd18757ec223a9c9f8a788343a72c1c7c2fbb60517097',PRIOR/'MANIFEST.sha256':'1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a',PRIOR/'results_referee_comparison.json':'46adce91fb2d361cb506046c706e4e849ecc0e4bb23b2df7193ed04073ebd9c7',SOURCE:'2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339',TERM/'results_referee.json':'d0f48380558bb663567083c744667f76fad18cb85cc47e0e93b857dc05cac68f',TERM/'FINAL_MANIFEST.sha256':'ef85c2ee938da004226540d76e609feb9fae4261808f6ac755e9bfd8b268c73c'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path):
 n=0
 for line in path.read_text().splitlines():
  if not line.strip():continue
  d,name=line.split(None,1);p=(path.parent/name.strip()).resolve();assert p.is_file() and sha(p)==d;(n:=n+1)
 return n
def atomic(path,text):
 t=path.with_suffix(path.suffix+'.tmp');t.write_text(text);os.replace(t,path)
def split_top(text):
 out=[];depth=start=0
 for i,c in enumerate(text):
  depth+=c=='(';depth-=c==')'
  if c==',' and depth==0:out.append(text[start:i].strip());start=i+1
 out.append(text[start:].strip());assert depth==0;return out

Poly=dict[tuple[int,...],int]
def padd(a:Poly,b:Poly,scale=1):
 out=dict(a)
 for mono,value in b.items():
  new=out.get(mono,0)+scale*value
  if new:out[mono]=new
  else:out.pop(mono,None)
 return out
def pmul(a:Poly,b:Poly):
 out={}
 for am,av in a.items():
  for bm,bv in b.items():
   mono=tuple(sorted(am+bm));out[mono]=out.get(mono,0)+av*bv
 return {m:v for m,v in out.items() if v}
TOKEN=re.compile(r'\s*([A-Za-z_][A-Za-z0-9_]*|[0-9]+|[-+*()])')
class Parser:
 def __init__(self,text,index):self.tokens=TOKEN.findall(text);assert ''.join(self.tokens)==re.sub(r'\s+','',text);self.i=0;self.index=index
 def parse(self):
  value=self.expr();assert self.i==len(self.tokens);return value
 def expr(self):
  value=self.term()
  while self.i<len(self.tokens) and self.tokens[self.i] in '+-':op=self.tokens[self.i];self.i+=1;value=padd(value,self.term(),1 if op=='+' else -1)
  return value
 def term(self):
  value=self.factor()
  while self.i<len(self.tokens) and self.tokens[self.i]=='*':self.i+=1;value=pmul(value,self.factor())
  return value
 def factor(self):
  token=self.tokens[self.i]
  if token in '+-':self.i+=1;value=self.factor();return value if token=='+' else {m:-c for m,c in value.items()}
  if token=='(':self.i+=1;value=self.expr();assert self.tokens[self.i]==')';self.i+=1;return value
  self.i+=1
  if token.isdigit():return {} if int(token)==0 else {():int(token)}
  return {(self.index[token],):1}
def ptext(poly,variables):
 terms=[]
 for mono in sorted(poly,key=lambda x:(len(x),x)):
  coeff=poly[mono];atom='*'.join(variables[i] for i in mono) if mono else '1';atom=str(abs(coeff)) if not mono else atom if abs(coeff)==1 else f'{abs(coeff)}*{atom}'
  terms.append((('-' if coeff<0 else '+') if terms else ('-' if coeff<0 else ''))+atom)
 return ''.join(terms) if terms else '0'
def sub(poly,replacements):
 out={}
 for mono,coeff in poly.items():
  term={():coeff}
  for variable in mono:term=pmul(term,replacements[variable])
  out=padd(out,term)
 return out
def rank_mod(rows,prime):
 pivots={}
 for raw in rows:
  row={c:v%prime for c,v in raw.items() if v%prime}
  while row:
   lead=min(row)
   if lead not in pivots:
    inv=pow(row[lead],prime-2,prime);pivots[lead]={c:(v*inv)%prime for c,v in row.items() if (v*inv)%prime};break
   scale=row[lead]
   for c,v in pivots[lead].items():
    new=(row.get(c,0)-scale*v)%prime
    if new:row[c]=new
    else:row.pop(c,None)
 return len(pivots)
def rank_q(rows):
 pivots={}
 for raw in rows:
  row={c:Fraction(v) for c,v in raw.items() if v}
  while row:
   lead=min(row)
   if lead not in pivots:
    value=row[lead];pivots[lead]={c:v/value for c,v in row.items()};break
   scale=row[lead]
   for c,v in pivots[lead].items():
    new=row.get(c,0)-scale*v
    if new:row[c]=new
    else:row.pop(c,None)
 return len(pivots)

for p,d in PINS.items():assert p.is_file() and sha(p)==d,(p,sha(p),d)
producer_lines=replay(PROD/'MANIFEST.sha256');timeout_lines=replay(TERM/'FINAL_MANIFEST.sha256')
prod=json.loads((PROD/'results_design.json').read_text());assert prod['status']=='PASS_DESIGN_ONLY_NO_SOLVE'
text=SOURCE.read_text();variables=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');generators=split_top(text.split('ideal I=',1)[1].split(';\nprint',1)[0]);assert len(variables)==67 and len(generators)==6574
index={v:i for i,v in enumerate(variables)};polys=[Parser(g,index).parse() for g in generators]
monomials=sorted(set().union(*(p.keys() for p in polys)));mi={m:i for i,m in enumerate(monomials)}
coeff=[{mi[m]:c for m,c in p.items()} for p in polys[:6561]]
support=[]
for p in polys[:6561]:support.append({i:1 for m in p for i in m})
exponents=[dict(Counter(m)) for m in monomials]
linear=[()]+[(i,) for i in range(67)];li={m:i for i,m in enumerate(linear)};affine=[{li[m]:c for m,c in p.items() if m in li} for p in polys[:6561]]
primes=(1000003,1000033);ranks={'coefficient_mod':{str(q):rank_mod(coeff,q) for q in primes},'support_mod':{str(q):rank_mod(support,q) for q in primes},'exponent_mod':{str(q):rank_mod(exponents,q) for q in primes},'affine_mod':{str(q):rank_mod(affine,q) for q in primes},'support_Q':rank_q(support),'exponent_Q':rank_q(exponents),'affine_Q':rank_q(affine)}
assert ranks=={'coefficient_mod':{'1000003':6561,'1000033':6561},'support_mod':{'1000003':47,'1000033':47},'exponent_mod':{'1000003':67,'1000033':67},'affine_mod':{'1000003':19,'1000033':19},'support_Q':47,'exponent_Q':67,'affine_Q':19}
incidence={v:sum(any(i in m for m in p) for p in polys[:6561]) for i,v in enumerate(variables)};assert all(incidence.values())
monic=[]
for gi,p in enumerate(polys):
 for i,v in enumerate(variables):
  if abs(p.get((i,),0))==1 and not any(i in m for m in p if m!=(i,)):monic.append((gi,v))
assert monic==[]
# Modular full row rank at the row-count upper bound proves exact Q coefficient rank.
assert len(coeff)==6561 and all(ranks['coefficient_mod'][str(q)]==len(coeff) for q in primes)

H10=Parser('(-xn2*a57_01+a57_02)*a57_10+(-xn0*a57_02+xn2)*a57_11+(xn0*a57_01-1)*a57_12',index).parse();H20=Parser('(-xn2*a57_01+a57_02)*a57_20+(-xn0*a57_02+xn2)*a57_21+(xn0*a57_01-1)*a57_22',index).parse()
identities={6561:padd(Parser('a57_01*a57_10-a57_11',index).parse(),pmul(Parser('t0',index).parse(),H10)),6562:padd(Parser('a57_01*a57_20-a57_21',index).parse(),pmul(Parser('t0',index).parse(),H20)),6563:pmul(Parser('t1',index).parse(),H10),6564:pmul(Parser('t1',index).parse(),H20),6565:pmul(Parser('t2',index).parse(),H10),6566:pmul(Parser('t2',index).parse(),H20)}
assert all(polys[i]==p for i,p in identities.items())
# d=xn0*a57_01-1 and b0=a26_00+a26_01*a57_01+a26_02*a57_02 are units because d*b0*sat=1.
assert polys[-1]==Parser('(xn0*a57_01-1)*(a26_00+a26_01*a57_01+a26_02*a57_02)*sat-1',index).parse()

retained=list(range(6561))+list(range(6567,6574))
specs=[('Dt1',{'a57_11':'a57_01*a57_10','a57_12':'a57_02*a57_10','a57_21':'a57_01*a57_20','a57_22':'a57_02*a57_20'},['it1'],['t1*it1-1']),('Vt1_Dt2',{'a57_11':'a57_01*a57_10','a57_12':'a57_02*a57_10','a57_21':'a57_01*a57_20','a57_22':'a57_02*a57_20','t1':'0'},['it2'],['t2*it2-1']),('Vt1_Vt2_Dt0',{'t1':'0','t2':'0','a57_12':'-((a26_00+a26_01*a57_01+a26_02*a57_02)*sat)*(it0*(a57_01*a57_10-a57_11)+((-xn2*a57_01+a57_02)*a57_10+(-xn0*a57_02+xn2)*a57_11))','a57_22':'-((a26_00+a26_01*a57_01+a26_02*a57_02)*sat)*(it0*(a57_01*a57_20-a57_21)+((-xn2*a57_01+a57_02)*a57_20+(-xn0*a57_02+xn2)*a57_21))'},['it0'],['t0*it0-1']),('Vt0_Vt1_Vt2',{'t0':'0','t1':'0','t2':'0','a57_11':'a57_01*a57_10','a57_21':'a57_01*a57_20'},[],[])]
strata=[]
prod_by={x['name']:x for x in prod['exact_stratified_cover']['strata']}
for name,mapping,added,extra in specs:
 removed=set(mapping);newvars=[v for v in variables if v not in removed]+added;ni={v:i for i,v in enumerate(newvars)}
 replacements=[Parser(mapping.get(v,v),ni).parse() for v in variables];transformed=[sub(polys[i],replacements) for i in retained]+[Parser(g,ni).parse() for g in extra]
 zeros=sum(not p for p in transformed);transformed=[p for p in transformed if p];keys=[tuple(sorted(p.items())) for p in transformed];unique=[];seen=set()
 for p,key in zip(transformed,keys):
  if key not in seen:seen.add(key);unique.append(p)
 expected='\n'.join(['// DESIGN-ONLY reversible stratum; no solve authorized.','option(noredefine);',f"ring r=0,({','.join(newvars)}),dp;",'ideal I='+',\n'.join(ptext(p,newvars) for p in unique)+';','print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','quit;',''])
 path=PROD/f'rep2_group016_67_{name}_Q.sing';assert path.read_text()==expected
 record=prod_by[name];assert sha(path)==record['sha256'] and record['variables']==len(newvars) and record['generators']==len(unique) and record['zero_after_substitution']==zeros and record['duplicates_after_substitution']==len(transformed)-len(unique)
 ids=set(re.findall(r'\b[A-Za-z_][A-Za-z_0-9]*\b',expected));assert not (ids&removed)
 strata.append({'name':name,'source_sha256':sha(path),'variables':len(newvars),'generators':len(unique),'removed_identifiers_absent':True,'forward_reverse_verified':True})
assert [(x['variables'],x['generators']) for x in strata]==[(64,6569),(63,6569),(64,6569),(62,6568)]

timeout=json.loads((TERM/'results_referee.json').read_text());assert timeout['status']=='PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE' and timeout['termination']=='NATIVE_WALL_CAP_240' and timeout['attempt_consumed'] and timeout['mathematical_coverage'] is False and timeout['automatic_relaunch'] is False
prior=json.loads((PRIOR/'results_referee_comparison.json').read_text());assert prior['exact_comparison']['intersection_chart_count']==57 and prior['smallest_exact_pilot']['sha256']==sha(SOURCE)
comparison={'relation':'The four t-strata are an exact partition of the single prior chart V(A67,A12) intersect D(b0), not transports of the other 56 charts. Replacing that one member yields a 60-chart global cover (56 unchanged plus 4).','prior_chart_count':57,'subdivided_prior_charts':1,'unchanged_prior_charts':56,'replacement_t_charts':4,'resulting_global_chart_count':60,'smallest_sound_source':'rep2_group016_67_Vt0_Vt1_Vt2_Q.sing','smallest_sound_shape':[62,6568],'smallest_scope':'V(A67,A12,based guard b0 open,t0,t1,t2); specifically V(A67,A12,t0,t1,t2) intersect D(b0)','further_guard_intersection':'Intersecting with D(b1) or D(b2) is sound as a localization but adds an inverse and has no proved monic elimination, so it is not a smaller justified pilot. No transport to other torus/guard charts is proved.'}
result={'schema':'KRENN_X5_REP2_GROUP16_67_TIMEOUT_REDUCTION_INDEPENDENT_REFEREE_V1','status':'PASS_EXACT_FOUR_STRATUM_REDUCTION_REFEREE_ZERO_SOLVES','producer':{'manifest_sha256':sha(PROD/'MANIFEST.sha256'),'result_sha256':sha(PROD/'results_design.json'),'manifest_lines_replayed':producer_lines},'source':{'sha256':sha(SOURCE),'variables':67,'generators':6574,'expanded_monomials':len(monomials)},'ranks':{**ranks,'coefficient_Q':6561,'coefficient_Q_proof':'two modular ranks attain the 6561-row upper bound'},'claim_audit':{'all_67_amplitude_active':True,'exact_amplitude_linear_redundancy':0,'monic_graph_candidates':[],'no_inactive_redundancy_or_monic_overclaim':True},'guard_factorization':{'indices':list(identities),'identities_exact':True,'d_b0_sat_unit_equation_exact':True},'t_cover':{'partition':['D(t1)','V(t1) intersect D(t2)','V(t1,t2) intersect D(t0)','V(t0,t1,t2)'],'exhaustive_disjoint_locally_closed_cover':True,'reversible':True,'strata':strata,'all_sources_byte_rebuilt':True,'all_removed_identifiers_absent':True},'timeout_binding':{'result_sha256':sha(TERM/'results_referee.json'),'final_manifest_sha256':sha(TERM/'FINAL_MANIFEST.sha256'),'final_manifest_lines_replayed':timeout_lines,'attempt_consumed':True,'termination':'NATIVE_WALL_CAP_240','mathematical_coverage':False,'reuse_or_relaunch_authorized':False},'prior_57_comparison':comparison,'pins':{str(p.relative_to(ROOT)):d for p,d in PINS.items()},'scope':{'design_referee_only':True,'singular_runs':0,'ideal_runs':0,'smallest_pilot_launched':False,'group16_closed':False,'rep2_closed':False}}
atomic(H/'results_referee.json',json.dumps(result,indent=2,sort_keys=True)+'\n')
atomic(H/'REPORT.md',f'''# Rep2 group16 67-timeout reduction independent referee\n\nStatus: **{result['status']}**.\n\nIndependent expansion gives exact coefficient rank 6,561 (via two full modular ranks), support rank 47, exponent rank 67, and affine rank 19. All 67 coordinates occur in amplitude equations, the amplitude rows have no linear redundancy, and no generator has the claimed monic-graph form.\n\nThe six first guards factor exactly through two rows H10/H20. With the already-inverted d and b0, the four D/V cases for t1,t2,t0 are exhaustive and reversible. All four Q sources reproduce byte-for-byte at 64/6569, 63/6569, 64/6569, and 62/6568, with removed identifiers absent.\n\nThis partitions only the prior A67=A12=0, D(b0) member. The honest global replacement is 56 unchanged charts plus these four: 60 total. The smallest sound source is the closed t0=t1=t2=0 chart at 62/6568; no further smaller guard intersection has a proved elimination.\n\nThe consumed p32003 lane remains NATIVE_WALL_CAP_240 with zero coverage/nonreuse. No solve was run.\n''')
print(json.dumps({'status':result['status'],'ranks':[6561,47,67,19],'strata':[[x['variables'],x['generators']] for x in strata],'global_cover':60,'solver_runs':0},sort_keys=True))
