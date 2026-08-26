#!/usr/bin/env python3
"""Independent design referee for the rank-3 adjugate ideal; no solve."""
import collections, hashlib, itertools, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROD=ROOT/"computations/unaudited-codex-n8-x5-rectangle-rank3-adjugate-ideal-referee-2026-08-25"
PARENT=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank3-reduction-2026-08-25/results_rank3_reduction.json"
OUT=Path(__file__).resolve().parent/"results_referee.json"
PINS={
 PROD/"MANIFEST.sha256":"c2fbb2ba00a1dc854b66ea7791cfb0fdad7b3b1747ee71b01e7c9f62a65ee8e5",
 PROD/"results_adjugate_referee.json":"6cf2d19e4e9a65348a7792227055be14d415f4a1a205b71ad417f2b7b90d7b08",
 PROD/"rectangle_rank3_adjugate_Q.sing":"e2739688ea9986d59c56e17e6f0058154d9ddb7930bf9617a1d3a3a8167538f5",
 PARENT:"ffacbff0a12d414d09a437597fb9f41083a8369894849b7891bd6e60a43c559d",
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(p):
 n=0
 for line in p.read_text().splitlines():
  if not line.strip():continue
  d,r=line.split(None,1);assert sha(p.parent/r.strip())==d;n+=1
 return n
def add(counter,coef,monomial):
 monomial=tuple(sorted(monomial));counter[monomial]+=coef
 if counter[monomial]==0:del counter[monomial]
def det_poly():
 out=collections.Counter()
 for p in itertools.permutations(range(3)):
  inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
  add(out,-1 if inv%2 else 1,tuple((i,p[i]) for i in range(3)))
 return out
def adj(i,j):
 rows=[x for x in range(3) if x!=j];cols=[x for x in range(3) if x!=i]
 out=collections.Counter();sgn=-1 if (i+j)%2 else 1
 add(out,sgn,((rows[0],cols[0]),(rows[1],cols[1])))
 add(out,-sgn,((rows[0],cols[1]),(rows[1],cols[0])))
 return out
def mul(poly,atom):
 out=collections.Counter()
 for monomial,coef in poly.items():add(out,coef,monomial+(atom,))
 return out
def count_top(body):
 depth=0;count=1 if body.strip() else 0
 for c in body:
  if c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0
  elif c==',' and depth==0:count+=1
 assert depth==0;return count

for p,d in PINS.items():assert sha(p)==d,(p,sha(p),d)
entries=replay(PROD/"MANIFEST.sha256")
producer=json.loads((PROD/"results_adjugate_referee.json").read_text())
parent=json.loads(PARENT.read_text())
source=(PROD/"rectangle_rank3_adjugate_Q.sing").read_text()
assert source.count("ring r=0,")==1 and "ring r=32003," not in source
ring0=source.index("ring r=0,(")+len("ring r=0,(");ring1=source.index("),dp;",ring0)
variables=source[ring0:ring1].split(',')
expected=[f"a{b}_{i}{j}" for b in ("01","04","15","26","35","47") for i in range(3) for j in range(3)]+["u26","u47"]
assert variables==expected and len(set(variables))==56
ideal0=source.index("ideal I=")+len("ideal I=");ideal1=source.index(";\nprint(\"INPUT_VARIABLES=",ideal0)
assert count_top(source[ideal0:ideal1])==6563
assert "a12_" not in source and "a23_" not in source

# Independent 18-entry proof of adj(A)A=Aadj(A)=det(A)I.
det=det_poly();checks=0
for side in ("adjA","Aadj"):
 for i,j in itertools.product(range(3),repeat=2):
  got=collections.Counter()
  for k in range(3):
   poly=adj(i,k) if side=="adjA" else adj(k,j)
   atom=(k,j) if side=="adjA" else (i,k)
   got.update(mul(poly,atom))
  got=collections.Counter({m:c for m,c in got.items() if c})
  assert got==(det if i==j else collections.Counter());checks+=1
assert checks==18

guard=parent["guard_rank3"]
assert guard["original"]==["A47^T+A17*A46^T=0","A26*A47^T+A46^T=0"]
assert guard["elimination"]=="A46=-A47*A26^T"
assert guard["reduced_guard"]=="(I-A17*A26)*A47^T=0"
assert set(guard["consequences"])>={"A17*A26=I","A26*A17=I"}
assert producer["parameterization"]["A17"]=="u26*adj(A26)"
assert producer["parameterization"]["A46"]=="-A47*A26^T"
assert producer["parameterization"]["saturations"]==["u26*det(A26)-1","u47*det(A47)-1"]
assert producer["counts"]=={"matrix_variables":54,"scalar_variables":2,"variables":56,"full_x5_generators":6561,"saturation_generators":2,"generators":6563}
for variant in ("A12_absent","A12_present"):
 assert parent["variants"][variant]["full_x5_depends_on_A12"] is False
 assert parent["variants"][variant]["full_x5_depends_on_A23"] is False

modular_source=source.replace("ring r=0,","ring r=32003,",1).encode()
audit={
 "schema":"KRENN_X5_RECTANGLE_RANK3_ADJUGATE_INDEPENDENT_REFEREE_V1",
 "status":"PASS_EXACT_EQUIVALENT_DESIGN_NO_SOLVE_NO_CLOSURE",
 "producer_manifest_sha256":PINS[PROD/"MANIFEST.sha256"],"producer_result_sha256":PINS[PROD/"results_adjugate_referee.json"],
 "manifest_entries_replayed":entries,"Q_source_sha256":PINS[PROD/"rectangle_rank3_adjugate_Q.sing"],
 "counts":{"variables":56,"generators":6563,"full_x5":6561,"saturations":2},
 "adjugate_entries_replayed":18,
 "forward_lift":"A17*A26=I forces det(A26)!=0; u26=det(A26)^-1 gives A17=u26*adj(A26); u47=det(A47)^-1; A46 unchanged",
 "reverse_lift":"the two determinant saturations make A26,A47 invertible; the adjugate definition yields both inverse identities and A46=-A47*A26^T satisfies both oriented guards",
 "variants":{"A12_absent":"A12=0,A23=I","A12_present":"A12=I,A23=I","amplitude_and_guard_inactive":True},
 "held_modular_diagnostic":{
  "status":"HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE","field_prime":32003,
  "derivation":"unique ring-token substitution r=0 to r=32003","expected_source_sha256":hashlib.sha256(modular_source).hexdigest(),"expected_source_bytes":len(modular_source),
  "maximum_lane_count":1,"native_wall_seconds":180,"wrapper_wall_seconds":195,"rss_cap_bytes":8*1024**3,
  "fresh_source_atomic_result":True,"stop_after_any_terminal_outcome":True,"automatic_relaunch":False,
  "unit_scope":"modular diagnostic only; exact-Q closure forbidden from this lane alone",
 },
 "scope":{"solver_launches":0,"rank3_closed":False,"A12_variants_closed":False},
}
OUT.write_text(json.dumps(audit,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":audit["status"],"result_sha256":sha(OUT)},sort_keys=True))
