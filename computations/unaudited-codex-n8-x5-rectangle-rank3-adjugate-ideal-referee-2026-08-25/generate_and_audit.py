#!/usr/bin/env python3
"""Independent exact adjugate reduction and one canonical Q input; no solve."""
from __future__ import annotations

import collections, copy, hashlib, itertools, json, os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PARENT=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank3-reduction-2026-08-25"
DESIGN=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank3-referee-2026-08-25"
PINS={
 PARENT/"MANIFEST.sha256":"b07d0fe2969bed87bd791c7c5680fe840f5f09221bc1e7cfd5b2ddeb0f057aa1",
 PARENT/"results_rank3_reduction.json":"ffacbff0a12d414d09a437597fb9f41083a8369894849b7891bd6e60a43c559d",
 DESIGN/"FINAL_MANIFEST.sha256":"5661d23ec6fb0bf2a04a604769fae7dd116354903de2807d2cb87da9ba38cf7d",
 DESIGN/"results_referee.json":"629bae2bd5fb7bafba7f4bd0c92b6716100d12c63d68492c1e59f8aa9fb80c2a",
}
BLOCKS=("01","04","15","26","35","47")
COLORS=range(3)


def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  while chunk:=stream.read(1<<20): h.update(chunk)
 return h.hexdigest()


def wrapped(value):
 return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*values):
 if any(value=="0" for value in values): return "0"
 values=[wrapped(value) for value in values if value!="1"]
 return "*".join(values) if values else "1"


def summation(values):
 values=[value for value in values if value!="0"]
 return "+".join(values).replace("+-","-") if values else "0"


def difference(left,right):
 if right=="0": return left
 if left=="0": return f"-({right})"
 return f"{left}-({right})"


def entry(block,i,j): return f"a{block}_{i}{j}"


def det3(block):
 terms=[]
 for permutation in itertools.permutations(COLORS):
  inversions=sum(permutation[i]>permutation[j] for i in COLORS for j in range(i+1,3))
  term=product(*(entry(block,i,permutation[i]) for i in COLORS))
  terms.append(term if inversions%2==0 else f"-({term})")
 return summation(terms)


def adj_entry(block,i,j):
 # adj(A)[i,j] is cofactor(A)[j,i].
 rows=[value for value in COLORS if value!=j]
 columns=[value for value in COLORS if value!=i]
 value=difference(product(entry(block,rows[0],columns[0]),entry(block,rows[1],columns[1])),
                  product(entry(block,rows[0],columns[1]),entry(block,rows[1],columns[0])))
 return value if (i+j)%2==0 else f"-({value})"


def a17(i,j): return product("u26",adj_entry("26",i,j))


def amplitude(word):
 a,b,c,d,e,f,g,h=word
 X=summation([product(entry("01",a,b),entry("35",d,f)), entry("15",b,f) if a==d else "0"])
 contraction=summation(product(entry("47",e,t),entry("26",g,t)) for t in COLORS)
 Q=difference(product(entry("26",c,g),entry("47",e,h)),contraction if c==h else "0")
 R=summation(["1" if a==d and e==f else "0",product(entry("04",a,e),entry("35",d,f))])
 S=summation(["1" if b==g and c==h else "0",product(a17(b,h),entry("26",c,g))])
 return summation([product(X,Q),product(R,S)])


def poly_add(target,coefficient,monomial):
 monomial=tuple(sorted(monomial)); target[monomial]+=coefficient
 if target[monomial]==0: del target[monomial]


def determinant_poly():
 result=collections.Counter()
 for permutation in itertools.permutations(COLORS):
  inversions=sum(permutation[i]>permutation[j] for i in COLORS for j in range(i+1,3))
  poly_add(result,-1 if inversions%2 else 1,((0,permutation[0]),(1,permutation[1]),(2,permutation[2])))
 return result


def adj_poly(i,j):
 rows=[value for value in COLORS if value!=j]; columns=[value for value in COLORS if value!=i]
 result=collections.Counter(); sign=-1 if (i+j)%2 else 1
 poly_add(result,sign,((rows[0],columns[0]),(rows[1],columns[1])))
 poly_add(result,-sign,((rows[0],columns[1]),(rows[1],columns[0])))
 return result


def multiply_entry_polys(left,right_atom):
 result=collections.Counter()
 for monomial,coefficient in left.items(): poly_add(result,coefficient,monomial+(right_atom,))
 return result


def adjugate_replay():
 determinant=determinant_poly(); checks=[]
 for side in ("adj_times_A","A_times_adj"):
  for i,j in itertools.product(COLORS,repeat=2):
   value=collections.Counter()
   for k in COLORS:
    adj=adj_poly(i,k) if side=="adj_times_A" else adj_poly(k,j)
    atom=(k,j) if side=="adj_times_A" else (i,k)
    value.update(multiply_entry_polys(adj,atom))
   value=collections.Counter({m:c for m,c in value.items() if c})
   expected=determinant if i==j else collections.Counter()
   assert value==expected,(side,i,j,value,expected)
   checks.append([side,i,j])
 return checks


def build_program():
 variables=[entry(block,i,j) for block in BLOCKS for i,j in itertools.product(COLORS,repeat=2)]+["u26","u47"]
 assert len(variables)==len(set(variables))==56
 equations=[]
 amplitude_hasher=hashlib.sha256()
 for word in itertools.product(COLORS,repeat=8):
  value=amplitude(word); target="1" if len(set(word))==1 else "0"
  equation=difference(value,target); equations.append(equation)
  amplitude_hasher.update(("".join(map(str,word))+":"+equation+"\n").encode())
 equations.extend([difference(product("u26",det3("26")),"1"),difference(product("u47",det3("47")),"1")])
 assert len(equations)==6563
 assert len(set(equations))==6563 and all(value not in ("0","1","-1") for value in equations)
 program="\n".join([
  "option(noredefine);",f"ring r=0,({','.join(variables)}),dp;","ideal I="+",\n".join(equations)+";",
  'print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));',
  "ideal G=slimgb(I);",'print("GROEBNER_SIZE="+string(size(G)));',"poly remainder=reduce(1,G);",
  'print("UNIT_REMAINDER="+string(remainder));',
  'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',"quit;",""])
 return program,variables,equations,amplitude_hasher.hexdigest()


def validate(result):
 assert result["schema"]=="KRENN_X5_RECTANGLE_RANK3_ADJUGATE_IDEAL_REFEREE_V1"
 assert result["status"]=="PASS_EXACT_EQUIVALENT_DESIGN_NO_SOLVE"
 assert result["counts"]=={"matrix_variables":54,"scalar_variables":2,"variables":56,"full_x5_generators":6561,"saturation_generators":2,"generators":6563}
 assert result["variants"]=={"A12_absent":"lift with A12=0 and A23=I","A12_present":"lift with A12=I and A23=I"}
 assert result["scope"]=={"inputs_materialized":1,"solver_launches":0,"rank3_closed":False}


def hostile(result,mutation):
 candidate=copy.deepcopy(result);mutation(candidate)
 try:validate(candidate)
 except (AssertionError,KeyError,TypeError):return True
 return False


def main():
 for path,expected in PINS.items():assert sha256(path)==expected,(path,sha256(path),expected)
 parent=json.loads((PARENT/"results_rank3_reduction.json").read_text())
 assert parent["reduced_ideal"]["variables"]==64 and parent["reduced_ideal"]["generators"]==6571
 assert parent["factorization"]["verified_words"]==6561
 design=json.loads((DESIGN/"results_referee.json").read_text())["smallest_sound_next_ideal"]
 assert design["status"]=="HELD_NOT_MATERIALIZED_NOT_RUN"
 assert design["matrices"]==["A01","A04","A15","A26","A35","A47"]
 assert design["variables"]==56 and design["generators"]==6563
 assert design["substitutions"]==["A17=u26*adj(A26)","A46=-A47*A26^T"]
 checks=adjugate_replay();assert len(checks)==18
 program,variables,equations,amplitude_sha=build_program()
 source=HERE/"rectangle_rank3_adjugate_Q.sing"; temporary=source.with_suffix(".sing.tmp")
 temporary.write_text(program);os.replace(temporary,source)
 result={
  "schema":"KRENN_X5_RECTANGLE_RANK3_ADJUGATE_IDEAL_REFEREE_V1",
  "status":"PASS_EXACT_EQUIVALENT_DESIGN_NO_SOLVE",
  "parameterization":{
   "retained_matrices":list(BLOCKS),"scalars":["u26","u47"],
   "A17":"u26*adj(A26)","A46":"-A47*A26^T",
   "saturations":["u26*det(A26)-1","u47*det(A47)-1"],
  },
  "forward_equivalence":"from the 64-variable branch, det(A26)!=0 follows from A17*A26=I; set u26=det(A26)^-1 and u47=det(A47)^-1. The adjugate identity gives the existing A17=u26*adj(A26), while A46 is unchanged.",
  "reverse_equivalence":"the two saturations make A26,A47 invertible. Define A17=u26*adj(A26), A46=-A47*A26^T. Then A17*A26=A26*A17=I and both oriented cap67 guards hold; every factorized amplitude is identical.",
  "adjugate_replay":{"polynomial_matrix_entries_checked":len(checks),"identities":["adj(A26)*A26=det(A26)*I","A26*adj(A26)=det(A26)*I"]},
  "variants":{"A12_absent":"lift with A12=0 and A23=I","A12_present":"lift with A12=I and A23=I"},
  "variant_reason":"A12 and A23 occur in none of the eight supported perfect matchings and neither rank3 guard; choosing the stated free lifts treats the two source variants separately.",
  "counts":{"matrix_variables":54,"scalar_variables":2,"variables":56,"full_x5_generators":6561,"saturation_generators":2,"generators":6563},
  "canonical_input":{"path":source.name,"sha256":hashlib.sha256(program.encode()).hexdigest(),"bytes":len(program.encode()),"ring":"Q","variable_order":variables,"amplitude_ledger_sha256":amplitude_sha},
  "pins":{str(path.relative_to(ROOT)):digest for path,digest in PINS.items()},
  "scope":{"inputs_materialized":1,"solver_launches":0,"rank3_closed":False},
 }
 validate(result)
 tests={
  "variable_mutation":hostile(result,lambda x:x["counts"].__setitem__("variables",55)),
  "generator_mutation":hostile(result,lambda x:x["counts"].__setitem__("generators",6562)),
  "launch_injection":hostile(result,lambda x:x["scope"].__setitem__("solver_launches",1)),
  "variant_collapse":hostile(result,lambda x:x["variants"].__setitem__("A12_absent","same")),
 }
 assert all(tests.values());result["hostile_tests"]=tests
 output=HERE/"results_adjugate_referee.json";temporary=output.with_suffix(".json.tmp")
 temporary.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");os.replace(temporary,output)
 print(json.dumps({"status":result["status"],"variables":56,"generators":6563,"source_sha256":result["canonical_input"]["sha256"],"launches":0},sort_keys=True))


if __name__=="__main__":main()
