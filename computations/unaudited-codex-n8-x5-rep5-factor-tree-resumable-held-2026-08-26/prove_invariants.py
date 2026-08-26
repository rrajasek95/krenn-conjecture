#!/usr/bin/env python3
"""Small exhaustive model checks for the canonical state/key invariants; no rep5 traversal."""
import hashlib,itertools,json,math,os
from pathlib import Path
H=Path(__file__).resolve().parent;UNIT=((((),1),),)
def primitive(p):
 g=0
 for c in p.values():g=math.gcd(g,abs(c))
 q={m:c//g for m,c in p.items() if c};lead=min(q,key=lambda m:(len(m),m))
 if q[lead]<0:q={m:-c for m,c in q.items()}
 return tuple(sorted(q.items()))
def canonical(values):
 keys=set()
 for p in values:
  if not p:continue
  key=primitive(p)
  if len(key)==1 and key[0][0]==():return UNIT
  keys.add(key)
 return tuple(sorted(keys))
def reduce_order(base,z,u,order):
 values=[]
 for original in base:
  p={m:c for m,c in original.items() if not any((z>>x)&1 for x in m)}
  if not p:continue
  for x in order:
   if not (u>>x)&1:continue
   power=min(m.count(x) for m in p)
   if power:
    q={}
    for m,c in p.items():w=list(m)
    # Written separately to keep the mutation-sensitive loop obvious.
    for m,c in p.items():
     w=list(m)
     for _ in range(power):w.remove(x)
     q[tuple(w)]=q.get(tuple(w),0)+c
    p=q
  values.append(p)
 return canonical(values)
toy=[{(0,0,1):2,(0,1,2):-4},{(1,2):3,(0,2):6},{(0,):1,(1,):-1},{(2,2):5}]
assignments=0;order_checks=0
for states in itertools.product(range(3),repeat=3):
 z=sum((state==1)<<i for i,state in enumerate(states));u=sum((state==2)<<i for i,state in enumerate(states));assignments+=1;expected=None
 selected=[i for i in range(3) if (u>>i)&1]
 for order in itertools.permutations(selected):
  value=reduce_order(toy,z,u,order);expected=value if expected is None else expected;assert value==expected;order_checks+=1
base=canonical(toy);permuted=canonical([{m:-7*c for m,c in p.items()} for p in reversed(toy)]);assert base==permuted
def key(z,u,g):return hashlib.sha256(f'V1|{z}|{u}|{json.dumps(g,separators=(",",":"))}'.encode()).hexdigest()
keys=set()
for states in itertools.product(range(3),repeat=3):
 z=sum((state==1)<<i for i,state in enumerate(states));u=sum((state==2)<<i for i,state in enumerate(states));g=reduce_order(toy,z,u,tuple(range(3)));k=key(z,u,g);assert k not in keys;keys.add(k)
result={'schema':'KRENN_X5_REP5_FACTOR_TREE_INVARIANTS_V1','status':'PASS_TOY_EXHAUSTIVE_CANONICAL_STATE_INVARIANTS','toy_variables':3,'finite_assignments_checked':assignments,'localization_order_checks':order_checks,'unique_state_keys':len(keys),'scalar_generator_order_invariance':True,'zero_unit_disjoint':True,'general_finite_state_bound':'3^64','branch_depth_bound':64,'dedup_key_fields':['source_sha256','zero_bitmask','unit_bitmask','canonical_generator_sha256'],'coverage_identity':'Spec(I)=Spec(I[x^-1]) union Spec(I+(x))','rep5_nodes_expanded':0,'singular_runs':0};tmp=H/'results_invariants.json.tmp';tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');os.replace(tmp,H/'results_invariants.json');print(json.dumps(result,sort_keys=True))
