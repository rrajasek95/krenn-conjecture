#!/usr/bin/env python3
"""Independent rep5 guard-minor/Cramer contraction; generate only, never solve."""
from __future__ import annotations

import collections, copy, hashlib, itertools, json, os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PARENT=ROOT/"computations/unaudited-codex-n8-x5-seven-block-rep5-diagonal-incidence-gate-2026-08-25"
OBLIGATION=ROOT/"computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/results_full_family_obligation.json"
PINS={
 PARENT/"MANIFEST.sha256":"b73583e0b7a3a9c78003433802571cc7c306807ce311118acbe299c6c9fb7d71",
 PARENT/"generate_rep5.py":"a02d55e4fb9dbc9dfab3044c7900c6fc9b0bd72ca68a78388958b57dd7d177f8",
 PARENT/"gate_metadata.json":"e34d3650a7d60121882c55884b7ded9654089f10bda8a2212ef9c2cc62723712",
 OBLIGATION:"22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
}
COLORS=tuple(range(3))
FIXED=frozenset(((0,3),(1,6),(2,7),(4,5)))
VARIABLE=frozenset(((0,4),(1,2),(3,5),(6,7)))
ADDED=frozenset(((0,6),(1,5),(1,7),(2,4),(2,6),(3,6),(3,7)))
ELIMINATED=(3,6); OUTSIDE=(3,7)
NONFIXED=tuple(sorted(VARIABLE|ADDED)); RETAINED=tuple(edge for edge in NONFIXED if edge!=ELIMINATED)
SUPPORT=FIXED|set(NONFIXED)
TINY_Y=(0,0,0,0,"y",0,0,1)
TINY_Z=(0,0,0,0,"z",0,0,1)


def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  while chunk:=stream.read(1<<20):h.update(chunk)
 return h.hexdigest()


def matchings(vertices):
 if not vertices:
  yield ();return
 first=vertices[0]
 for position in range(1,len(vertices)):
  second=vertices[position];rest=vertices[1:position]+vertices[position+1:]
  for tail in matchings(rest):yield tuple(sorted(((first,second),)+tail))


PM8=tuple(sorted(matchings(tuple(range(8)))))
SUPPORTED=tuple(value for value in PM8 if set(value)<=SUPPORT)
assert len(PM8)==105 and len(SUPPORTED)==12 and len(RETAINED)==10


def wrapped(value):return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*values):
 if any(value=="0" for value in values):return "0"
 values=[wrapped(value) for value in values if value!="1"]
 return "*".join(values) if values else "1"


def summation(values):
 values=[value for value in values if value!="0"]
 return "+".join(values).replace("+-","-") if values else "0"


def difference(left,right):
 if right=="0":return left
 if left=="0":return f"-({right})"
 return f"{left}-({right})"


def orbit_representative(record):
 coordinate,p,q,r,kind,s,a,b=record; candidates=[]
 for permutation in itertools.permutations(COLORS):
  aa,bb=sorted((permutation[a],permutation[b]))
  candidates.append((permutation[coordinate],permutation[p],permutation[q],permutation[r],kind,permutation[s],aa,bb))
 return min(candidates)


def orbit_ledger():
 raw=[]
 for coordinate,p,q,r,s in itertools.product(COLORS,repeat=5):
  for kind in ("y","z"):
   for other in COLORS:
    if other!=q:
     a,b=sorted((q,other));raw.append((coordinate,p,q,r,kind,s,a,b))
 groups={}
 for value in raw:groups.setdefault(orbit_representative(value),[]).append(value)
 assert len(raw)==972 and len(groups)==162 and set(map(len,groups.values()))=={6}
 return raw,groups


def build_context(record):
 coordinate,p,q,r,kind,s,a,b=record;c=next(value for value in COLORS if value not in (a,b))
 solved={(0,6,i,j) for i,j in itertools.product(COLORS,repeat=2)}
 partner=(3,5) if kind=="y" else (3,7)
 solved|={(partner[0],partner[1],i,s) for i in COLORS}
 source={(edge,i,j):f"a{edge[0]}{edge[1]}_{i}{j}" for edge in RETAINED for i,j in itertools.product(COLORS,repeat=2)
         if (edge[0],edge[1],i,j) not in solved}
 assert len(source)==78
 xn={j:f"xn{j}" for j in COLORS if j!=r}
 yn={j:f"yn{j}" for j in COLORS if not(kind=="y" and j==s)}
 zn={j:f"zn{j}" for j in COLORS if not(kind=="z" and j==s)}

 def raw(edge,i,j):return source[edge,i,j]
 def w(j):return "1" if j==r else xn[j]
 def qy(j):return "1" if kind=="y" and j==s else yn[j]
 def qz(j):return "1" if kind=="z" and j==s else zn[j]

 def partner_entry(edge,i,j):
  if kind=="y" and edge==(3,5) and j==s:
   tail=summation([product(raw((3,5),i,k),qy(k)) for k in COLORS if k!=s]+
                  [product(raw((3,7),i,k),qz(k)) for k in COLORS])
   return difference("beta" if i==coordinate else "0",tail)
  if kind=="z" and edge==(3,7) and j==s:
   tail=summation([product(raw((3,5),i,k),qy(k)) for k in COLORS]+
                  [product(raw((3,7),i,k),qz(k)) for k in COLORS if k!=s])
   return difference("beta" if i==coordinate else "0",tail)
  return raw(edge,i,j)

 def outside(i,j):return partner_entry(OUTSIDE,i,j)
 def v(j):return outside(p,j)
 determinant=difference(product(w(a),v(b)),product(w(b),v(a)))

 def entry(edge,i,j):
  if edge in FIXED:return "1" if i==j else "0"
  if edge==ELIMINATED:
   return f"-({summation(product(outside(i,k),raw((2,6),j,k)) for k in COLORS)})"
  if edge==(0,6):
   reduced=difference("abar" if i==coordinate else "0",product(f"t{i}",w(c)))
   if j==a:return summation((product(reduced,v(b)),product(w(b),f"t{i}",v(c))))
   if j==b:return f"-({summation((product(w(a),f't{i}',v(c)),product(reduced,v(a))))})"
   assert j==c;return product(determinant,f"t{i}")
  if edge in ((3,5),(3,7)):return partner_entry(edge,i,j)
  return raw(edge,i,j)

 variables=list(source.values())+list(xn.values())+["abar"]+list(yn.values())+list(zn.values())+["beta"]+[f"t{i}" for i in COLORS]+["sat"]
 assert len(variables)==len(set(variables))==91
 return entry,variables,determinant,outside(p,q)


def amplitude(entry,word):
 terms=[]
 for matching in SUPPORTED:
  factors=[]
  for edge in matching:
   value=entry(edge,word[edge[0]],word[edge[1]])
   if value=="0":break
   factors.append(value)
  else:terms.append(product(*factors))
 return summation(terms)


def build_program(record,ring="32003"):
 entry,variables,determinant,outside_entry=build_context(record);equations=[]
 for word in itertools.product(COLORS,repeat=8):
  value=amplitude(entry,word);equations.append(difference(value,"1") if len(set(word))==1 else value)
 p=record[1]
 for i,j in itertools.product(COLORS,repeat=2):
  if j!=p:equations.append(summation(product(entry((0,6),i,k),entry((3,7),j,k)) for k in COLORS))
 for i,j in itertools.product(COLORS,repeat=2):
  correction=summation(product(entry((1,7),i,k),entry((2,6),k,l),entry((3,7),j,l)) for k,l in itertools.product(COLORS,repeat=2))
  equations.append(difference(entry((3,7),j,i),correction))
 equations.append(product("abar","beta",outside_entry,determinant,"sat")+"-1")
 assert len(equations)==6577 and len(variables)==91
 assert len(set(equations))==6577 and all(value not in ("0","1","-1") for value in equations)
 lines=["option(noredefine);",f"ring r={ring},({','.join(variables)}),dp;","ideal I="+",\n".join(equations)+";",
        'print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));',"ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',"poly remainder=reduce(1,G);",'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',"quit;",""]
 return "\n".join(lines)


def parent_digest_and_census():
 records=[];census=collections.Counter()
 for word in itertools.product(COLORS,repeat=8):
  terms=[]
  for matching in SUPPORTED:
   factors=[]
   for edge in matching:
    i,j=word[edge[0]],word[edge[1]]
    if edge in FIXED:
     if i!=j:break
    else:factors.append(f"A{edge[0]}{edge[1]}[{i}{j}]")
   else:terms.append("*".join(factors) or "1")
  target=1 if len(set(word))==1 else 0;census[len(terms)]+=1
  records.append(("".join(map(str,word)),target,tuple(terms)))
 payload=json.dumps(records,sort_keys=True,separators=(",",":")).encode()
 return hashlib.sha256(payload).hexdigest(),dict(sorted(census.items()))


def cramer_symbolic_replay():
 # Exact coefficient dictionaries in generic commuting symbols.
 def var(name):return collections.Counter({(name,):1})
 def add(*polys):
  out=collections.Counter()
  for poly in polys:out.update(poly)
  return collections.Counter({m:c for m,c in out.items() if c})
 def mul(*polys):
  out=collections.Counter({():1})
  for poly in polys:
   nxt=collections.Counter()
   for m,c in out.items():
    for n,d in poly.items():nxt[tuple(sorted(m+n))]+=c*d
   out=collections.Counter({m:c for m,c in nxt.items() if c})
  return out
 def neg(poly):return collections.Counter({m:-c for m,c in poly.items()})
 checks=0
 for a,b in itertools.combinations(COLORS,2):
  c=next(value for value in COLORS if value not in (a,b))
  w=[var(f"w{j}") for j in COLORS];v=[var(f"v{j}") for j in COLORS];t=var("t");abar=var("abar")
  d=add(mul(w[a],v[b]),neg(mul(w[b],v[a])))
  for delta in (0,1):
   reduced=add(abar if delta else collections.Counter(),neg(mul(t,w[c])))
   row=[None]*3
   row[a]=add(mul(reduced,v[b]),mul(w[b],t,v[c]))
   row[b]=neg(add(mul(w[a],t,v[c]),mul(reduced,v[a])))
   row[c]=mul(d,t)
   guard=add(*(mul(row[j],v[j]) for j in COLORS))
   incidence=add(*(mul(row[j],w[j]) for j in COLORS))
   assert guard==collections.Counter()
   assert incidence==(mul(d,abar) if delta else collections.Counter())
   checks+=2
 return checks


def validate(result):
 assert result["schema"]=="KRENN_X5_REP5_GUARD_MINOR_CONTRACTION_DESIGN_V1"
 assert result["status"]=="PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN"
 assert result["counts"]=={"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1}
 assert result["chart_census"]=={"raw":972,"S3_orbits":162,"orbit_size":6,"y_orbits":81,"z_orbits":81}
 assert result["scope"]=={"materialized_design_inputs":2,"ideal_runs":0,"rep5_closed":False,"transport_claimed":False}


def hostile(result,mutation):
 candidate=copy.deepcopy(result);mutation(candidate)
 try:validate(candidate)
 except (AssertionError,KeyError,TypeError):return True
 return False


def main():
 for path,expected in PINS.items():assert sha256(path)==expected,(path,sha256(path),expected)
 parent=json.loads((PARENT/"gate_metadata.json").read_text());assert parent["representative_id"]==5
 obligation=json.loads(OBLIGATION.read_text())["six_full_family_representatives"][5]
 assert obligation["added"]==["06","15","17","24","26","36","37"]
 digest,census=parent_digest_and_census();assert digest==parent["parent_full_x5_digest"]=="e8015349824f6851fba73d9ec57f4d8b59ea4ac686925415ff61c89b45df5f3a"
 assert {str(k):v for k,v in census.items()}=={str(k):v for k,v in parent["parent_term_census"].items()}
 raw,groups=orbit_ledger();assert cramer_symbolic_replay()==12
 programs={}
 for name,record in (("y",TINY_Y),("z",TINY_Z)):
  assert orbit_representative(record)==record
  program=build_program(record,"32003");path=HERE/f"rep5_guard_minor_tiny_{name}_p32003.sing"
  temporary=path.with_suffix(".sing.tmp");temporary.write_text(program);os.replace(temporary,path)
  programs[name]={"chart":list(record),"path":path.name,"sha256":hashlib.sha256(program.encode()).hexdigest(),"bytes":len(program.encode())}
 result={
  "schema":"KRENN_X5_REP5_GUARD_MINOR_CONTRACTION_DESIGN_V1","status":"PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN",
  "source_reconstruction":{"fixed":["03","16","27","45"],"variable":["04","12","35","67"],"added":["06","15","17","24","26","36","37"],
                           "elimination":"A36=-A37*A26^T","guard":["A06*A37^T=0","(I-A17*A26)*A37^T=0"],
                           "carrier":"A06^T*K*[A35|A37]","incidence":["A06*x=e_i","A35*y+A37*z=e_i"],"full_x5_digest":digest},
  "chart_cover":{"outside":"choose A37[p,q]!=0 and v=row_p(A37)","x":"choose x_r!=0; w=x/x_r and A06*w=alpha*e_i",
                 "independence":"A06*v=0 and alpha!=0 make w,v independent; v_q!=0 implies a nonzero 2x2 minor d involving q",
                 "partner":"choose a nonzero component of y or z, normalize it, and write A35*y+A37*z=beta*e_i",
                 "reverse":"divide by every factor in abar*beta*A37[p,q]*d*sat-1; Cramer reconstruction recovers the original witnesses",
                 "z_specific":"when z_s is the pivot, solve column s of A37 first; its substituted row-p entry is then used in v,d and the same saturation, with no cyclic definition"},
  "substitution":{"A06":"all nine entries solved by the w/v Cramer formulas with A06*w=d*abar*e_i and A06*v=0",
                  "partner_y":"solve column s of A35","partner_z":"solve column s of A37","A36":"reconstruct after the partner substitution",
                  "tautologies_removed":["six incidence equations","three guard equations against row p of A37"]},
  "symbolic_replay":{"generic_cramer_polynomial_identities":12,"parent_semantic_digest_replayed":True},
  "counts":{"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1},
  "chart_census":{"raw":len(raw),"S3_orbits":len(groups),"orbit_size":6,"y_orbits":sum(key[4]=="y" for key in groups),"z_orbits":sum(key[4]=="z" for key in groups)},
  "materialized_inputs":programs,
  "pins":{str(path.relative_to(ROOT)):value for path,value in PINS.items()},
  "scope":{"materialized_design_inputs":2,"ideal_runs":0,"rep5_closed":False,"transport_claimed":False},
 }
 validate(result)
 tests={"count_mutation":hostile(result,lambda x:x["counts"].__setitem__("new_variables",90)),
        "orbit_collapse":hostile(result,lambda x:x["chart_census"].__setitem__("S3_orbits",161)),
        "launch_injection":hostile(result,lambda x:x["scope"].__setitem__("ideal_runs",1)),
        "transport_overclaim":hostile(result,lambda x:x["scope"].__setitem__("transport_claimed",True))}
 assert all(tests.values());result["hostile_tests"]=tests
 output=HERE/"results_rep5_contraction_design.json";temporary=output.with_suffix(".json.tmp")
 temporary.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");os.replace(temporary,output)
 print(json.dumps({"status":result["status"],"variables":91,"generators":6577,"orbits":162,"runs":0},sort_keys=True))


if __name__=="__main__":main()
