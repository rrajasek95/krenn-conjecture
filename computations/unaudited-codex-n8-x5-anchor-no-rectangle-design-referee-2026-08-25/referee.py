#!/usr/bin/env python3
"""Independent finite referee and held smallest-pilot design; no solves."""
from __future__ import annotations
import collections,hashlib,itertools,json,os,re
from pathlib import Path
if not __debug__:raise RuntimeError('assertions required')
H=Path(__file__).resolve().parent;ROOT=H.parents[1];C=ROOT/'computations'
P=C/'unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25';B=C/'unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25'
def sha(p):
 d=hashlib.sha256()
 with p.open('rb') as f:
  while x:=f.read(1<<20):d.update(x)
 return d.hexdigest()
PINS={P/'MANIFEST.sha256':'4a15e9a2dd807b21169ca57b5e2aa7925db60bff804a1afc4227f2fd34822d75',P/'results_anchor_no_rectangle_design.json':'237fd1c51283174f579ce68574a8b30d26fbb9673a76f2ab363ea613927cd274',P/'all_carriers_ledger.json':'f924a661d04adc93b9dd5a8dac56b501da95bea61e93e33ae8657ae3413946ad',P/'canonical_reduced_full_x5_Q.sing':'25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3',B/'MANIFEST.sha256':'5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe',B/'results_unmapped16_design.json':'2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008'}
S=tuple(range(8));P8=tuple(itertools.permutations(S));COL=tuple(range(3));S3=tuple(itertools.permutations(COL));F=frozenset({(0,3),(1,6),(2,7),(4,5)});VF=frozenset({(0,4),(1,2),(3,5),(6,7)})
def edge(x):return tuple(map(int,x))
def lab(e):return f'{e[0]}{e[1]}'
def me(e,p):return tuple(sorted((p[e[0]],p[e[1]])))
def mes(es,p):return frozenset(me(e,p) for e in es)
def add(r):return frozenset(edge(x) for x in r['added'])
def var(r,reduced=False):return frozenset(edge(x) for x in r['nonzero_variable_blocks'])-({(1,2)} if reduced else set())
def support(r,reduced=False):return F|add(r)|var(r,reduced)
def maps(a,b,reduced=False):return [p for p in P8 if mes(F,p)==F and mes(VF,p)==VF and mes(add(a),p)==add(b) and mes(var(a,reduced),p)==var(b,reduced)]
def matchings(v):
 if not v:yield ();return
 a=v[0]
 for i in range(1,len(v)):
  for t in matchings(v[1:i]+v[i+1:]):yield tuple(sorted(((a,v[i]),)+t))
PM=tuple(sorted(matchings(S)));assert len(PM)==105
def sms(r):return tuple(m for m in PM if set(m)<=support(r))
def amp(r,w):
 out=collections.Counter()
 for m in sms(r):
  fs=[]
  for e in m:
   i,j=w[e[0]],w[e[1]]
   if e in F:
    if i!=j:break
   else:fs.append((e,i,j))
  else:out[tuple(sorted(fs))]+=1
 return out
def mw(w,p,c):
 o=[None]*8
 for i in S:o[p[i]]=c[w[i]]
 return tuple(o)
def mf(x,p,c):
 e,i,j=x;a,b=p[e[0]],p[e[1]]
 return ((a,b),c[i],c[j]) if a<b else ((b,a),c[j],c[i])
def ma(a,p,c):
 o=collections.Counter()
 for m,n in a.items():o[tuple(sorted(mf(x,p,c) for x in m))]+=n
 return o
def atom(e,i,j):return ((e,i,j),)
def mul(a,b):
 o=collections.Counter()
 for x,c in a.items():
  for y,d in b.items():o[tuple(sorted(x+y))]+=c*d
 return o
def fact(w):
 a,b,c,d,e,f,g,h=w;R=collections.Counter();Sx=collections.Counter();T=collections.Counter();U=collections.Counter()
 if a==d and e==f:R[()]+=1
 R[tuple(sorted(atom((0,4),a,e)+atom((3,5),d,f)))]+=1
 if b==g and c==h:Sx[()]+=1
 Sx[tuple(sorted(atom((1,7),b,h)+atom((2,6),c,g)))]+=1
 if e==f:T[atom((1,3),b,d)]+=1
 T[tuple(sorted(atom((1,4),b,e)+atom((3,5),d,f)))]+=1
 if c==h:U[atom((0,6),a,g)]+=1
 U[tuple(sorted(atom((0,7),a,h)+atom((2,6),c,g)))]+=1
 return +(mul(R,Sx)+mul(T,U))
def oriented(cap,res):
 e=tuple(sorted((cap,res)));return 'A'+lab(e)+('^T' if cap<res else '')
def trans(x):return x[:-2] if x.endswith('^T') else x+'^T'
def response(sup,cap,pair):
 p,q=cap;a,b=pair;out=[]
 for kind,x,y,k in [('direct',a,b,'K'),('switched',b,a,'K^T')]:
  left=tuple(sorted((p,x)));right=tuple(sorted((q,y)))
  if left in sup and right in sup:
   formula=(f'{oriented(p,x)}*K*{trans(oriented(q,y))}' if kind=='direct' else f'{oriented(q,a)}*K^T*{trans(oriented(p,b))}')
   out.append({'response_pair':lab(pair),'orientation':kind,'left_block':lab(left),'right_block':lab(right),'formula':formula,'cross_edges':sorted((lab(left),lab(right)))})
 return out
def carrier(sup,kind,cap,defining):
 residual=tuple(x for x in S if x not in cap)
 internal=set(itertools.combinations(defining,2)) if kind=='triangle' else {tuple(sorted((defining[0],x))) for x in residual if x!=defining[0]}
 terms=[]
 for pair in itertools.combinations(residual,2):
  if pair not in internal:terms+=response(sup,cap,pair)
 return {'kind':kind,'cap':lab(cap),'defining_sites':list(defining),'identity_cap':cap in F,'response_term_count':len(terms),'response_pairs':sorted({x['response_pair'] for x in terms}),'terms':terms}
def chart(rank):
 subsets=tuple(itertools.combinations(COL,rank));raw=tuple((i,r,c) for i in COL for r in subsets for c in subsets);rem=set(raw);sizes=[]
 while rem:
  x=min(rem);orb={(p[x[0]],tuple(sorted(p[y] for y in x[1])),tuple(sorted(p[y] for y in x[2]))) for p in S3};rem-=orb;sizes.append(len(orb))
 return len(raw),len(sizes),sizes
def write(p,x):
 q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');os.replace(q,p)
def main():
 for p,w in PINS.items():assert sha(p)==w,(p,sha(p),w)
 prod=json.loads((P/'results_anchor_no_rectangle_design.json').read_text());base=json.loads((B/'results_unmapped16_design.json').read_text());ledger=json.loads((P/'all_carriers_ledger.json').read_text())
 assert prod['status']=='PASS_EXACT_ONE_REDUCED_REPRESENTATIVE_RANK_DESIGN_NO_SOLVE' and prod['scope']=={'solver_runs':0,'mathematically_closed_full_records':0,'full_conjecture':False}
 rec=base['records'][12:];assert [x['record_index'] for x in rec]==[12,13,14,15] and all(x['classification']=='NO_OUTSIDE_R6_R7_RECTANGLE' for x in rec)
 literal={};reduced={};trials=0
 for a in rec:
  literal[str(a['record_index'])]={};reduced[str(a['record_index'])]={}
  for b in rec:
   lm=maps(a,b);rm=maps(a,b,True);trials+=2*40320;literal[str(a['record_index'])][str(b['record_index'])]=len(lm);reduced[str(a['record_index'])][str(b['record_index'])]=len(rm)
 assert literal==prod['source_symmetry']['literal_site_map_counts'] and reduced==prod['source_symmetry']['reduced_site_map_counts']
 assert all(literal[str(a)][str(b)]==1 for cls in ([12,13],[14,15]) for a in cls for b in cls) and all(literal[str(a)][str(b)]==0 for a in [12,13] for b in [14,15])
 assert all(reduced[str(a)][str(b)]==1 for a in range(12,16) for b in range(12,16))
 assert prod['source_symmetry']['unique_mirror']==[0,2,1,3,4,5,7,6]
 checks=0
 for target in rec:
  p=maps(rec[0],target,True)[0]
  for c in S3:
   for w in itertools.product(COL,repeat=8):assert ma(amp(rec[0],w),p,c)==amp(target,mw(w,p,c));checks+=1
 assert checks==157464==prod['census']['word_transport_checks']
 for r in rec:
  assert len(sms(r))==8 and all((1,2) not in m for m in sms(r))
 for w in itertools.product(COL,repeat=8):assert amp(rec[0],w)==fact(w)
 allc={}
 for r in rec:
  built=[]
  for cap in itertools.combinations(S,2):
   residual=tuple(x for x in S if x not in cap)
   for d in itertools.combinations(residual,3):built.append(carrier(support(r),'triangle',cap,d))
   for center in residual:built.append(carrier(support(r),'star',cap,(center,)))
  assert len(built)==728 and collections.Counter(x['kind'] for x in built)=={'triangle':560,'star':168}
  sealed=ledger['records'][str(r['record_index'])];assert len(sealed)==728
  for a,b in zip(built,sealed):
   for k in ('kind','cap','defining_sites','identity_cap','response_term_count','response_pairs','terms'):assert a[k]==b[k],(r['record_index'],k)
  allc[str(r['record_index'])]={'all':728,'triangle':560,'star':168,'identity_cap_two_sandwich':sum(bool(x['two_sandwich']) and x['two_sandwich']['identity_cap'] for x in sealed)}
 selected=next(x for x in ledger['records']['12'] if x['kind']=='star' and x['cap']=='27' and x['defining_sites']==[1]);assert selected['two_sandwich']['factorization_up_to_response_transposes']=='[A25^T|A26^T]*K*A07^T' and [x['formula'] for x in selected['terms']]==['A07*K^T*A25','A07*K^T*A26']
 rank0=prod['selected_rank_design']['rank0'];assert rank0['status']=='CLOSED_BY_ZERO_RESPONSE_MAP' and 'A07=0' in prod['selected_rank_design']['rank0']['condition']
 assert chart(1)==(27,5,[3,6,6,6,6]) and chart(2)==(27,5,[6,6,6,6,3])
 rd=prod['selected_rank_design'];assert (rd['rank1']['variables'],rd['rank1']['generators'],rd['rank1']['raw_charts'],rd['rank1']['S3_orbits'])==(85,6568,27,5);assert (rd['rank2']['variables'],rd['rank2']['generators'],rd['rank2']['raw_charts'],rd['rank2']['S3_orbits'])==(89,6568,27,5);assert (rd['rank3']['variables'],rd['rank3']['generators'])==(82,6562)
 src=(P/'canonical_reduced_full_x5_Q.sing').read_text();m=re.search(r'^ring r=([^,]+),\(([^\n]+)\),dp;$',src,re.M);assert m and m.group(1)=='0' and len(m.group(2).split(','))==81 and src.split('ideal I=',1)[1].split(';',1)[0].count(',\n')+1==6561 and 'slimgb' not in src
 ep='ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\n'
 assert src.count('quit;')==1;head,tail=src.rsplit('quit;',1);q=(head+ep+'quit;'+tail).encode();ptext=(head.replace('ring r=0,','ring r=32003,',1)+ep+'quit;'+tail).encode()
 pilot={'schema':'KRENN_X5_ANCHOR_NO_RECTANGLE_SMALLEST_STAGED_PILOT_HELD_V1','status':'HELD_ZERO_RUNS_REQUIRES_CLEARANCE','why_smallest':'The unsolved canonical reduced full-X5 ideal is 81 variables/6561 generators, smaller than rank3 82/6562, rank1 85/6568, and rank2 89/6568.','input_source_sha256':PINS[P/'canonical_reduced_full_x5_Q.sing'],'lanes':[{'stage':1,'field':'p32003','source_sha256':hashlib.sha256(ptext).hexdigest(),'bytes':len(ptext),'native_wall_seconds':180,'wrapper_wall_seconds':190,'rss_cap_bytes':8589934592,'purpose':'modular diagnostic only'},{'stage':2,'field':'Q','source_sha256':hashlib.sha256(q).hexdigest(),'bytes':len(q),'native_wall_seconds':480,'wrapper_wall_seconds':510,'rss_cap_bytes':8589934592,'purpose':'exact closure test only after separate stage1 audit and fresh manager clearance'}],'execution':{'sequential':True,'maximum_lanes':2,'parallel':False,'fresh_libproc':True,'atomic':True,'stop_first':True,'automatic_relaunch':False,'stage2_automatic':False,'solver_runs':0,'launch_authorized':False}}
 write(H/'HELD_PILOT_PLAN.json',pilot)
 result={'schema':'KRENN_X5_ANCHOR_NO_RECTANGLE_DESIGN_REFEREE_V1','status':'PASS_EXACT_DESIGN_AND_HELD_SMALLEST_PILOT_NO_SOLVE','producer':{'manifest_sha256':PINS[P/'MANIFEST.sha256'],'result_sha256':PINS[P/'results_anchor_no_rectangle_design.json'],'carrier_ledger_sha256':PINS[P/'all_carriers_ledger.json'],'ideal_sha256':PINS[P/'canonical_reduced_full_x5_Q.sing']},'symmetry':{'literal_classes':[[12,13],[14,15]],'reduced_class':[[12,13,14,15]],'unique_mirror':[0,2,1,3,4,5,7,6],'A12_inactive':True,'site_map_trials':trials},'word_checks':checks,'factorization_words':6561,'full_x5':{'variables':81,'generators':6561},'carrier_census':allc,'selected_carrier':{'record':12,'cap':'27','kind':'star','center':1,'factorization':'[A25^T|A26^T]*K*A07^T'},'rank_design':{'rank0':'CLOSED_BY_ZERO_RESPONSE_MAP','rank1':{'variables':85,'generators':6568,'raw':27,'orbits':5,'solved':False},'rank2':{'variables':89,'generators':6568,'raw':27,'orbits':5,'solved':False},'rank3':{'variables':82,'generators':6562,'solved':False}},'pilot':{'path':'HELD_PILOT_PLAN.json','sha256':sha(H/'HELD_PILOT_PLAN.json')},'scope':{'solver_runs':0,'closed_full_records':0,'rank0_branch_closed':True,'rank1_rank2_rank3_closed':False,'full_conjecture':False},'pins':{str(k.relative_to(ROOT)):v for k,v in PINS.items()}}
 write(H/'results_referee.json',result);print(json.dumps({'status':result['status'],'words':checks,'carriers':4*728,'rank0':'closed','solves':0},sort_keys=True))
if __name__=='__main__':main()
