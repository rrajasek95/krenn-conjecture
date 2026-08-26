#!/usr/bin/env python3
"""Independent rep2 source rebuild plus exact guard-minor contraction; no solve."""
from __future__ import annotations
import copy, hashlib, importlib.util, itertools, json, os
from pathlib import Path

if not __debug__:raise RuntimeError("fail closed: assertions required")
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
EXH=ROOT/"computations/unaudited-codex-n8-x5-seven-block-rep2-exhaustive-carrier-closure-2026-08-25"
OBL_DIR=ROOT/"computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25";OBL=OBL_DIR/"results_full_family_obligation.json"
ENGINE_DIR=ROOT/"computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25";ENGINE=ENGINE_DIR/"generate_design.py"
PINS={EXH/"MANIFEST.sha256":"8fe367273a44dd33c485d5c80976226138c920f64fe412245067b5fdc429b966",
      EXH/"results_rep2_exhaustive_carrier.json":"6ad0d0c171ffebf8825cd12b71ffca9dc8abbe8ecd26956c02b90ebcad53d7da",
      OBL_DIR/"MANIFEST.sha256":"21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf",
      OBL:"22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
      ENGINE_DIR/"MANIFEST.sha256":"7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02",
      ENGINE:"b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a"}
COLORS=tuple(range(3));FIXED=frozenset(((0,3),(1,6),(2,7),(4,5)));VARIABLE=frozenset(((0,4),(1,2),(3,5),(6,7)))
ADDED=frozenset(((0,6),(1,4),(1,7),(2,3),(2,6),(5,6),(5,7)));ELIMINATED=(5,6);OUTSIDE=(5,7)
NONFIXED=tuple(sorted(VARIABLE|ADDED));RETAINED=tuple(edge for edge in NONFIXED if edge!=ELIMINATED);SUPPORT=FIXED|set(NONFIXED)
TINY_Y=(0,0,0,0,"y",0,0,1);TINY_Z=(0,0,0,0,"z",0,0,1)

def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  while chunk:=stream.read(1<<20):h.update(chunk)
 return h.hexdigest()
def load_engine():
 spec=importlib.util.spec_from_file_location("sealed_cramer_engine",ENGINE);assert spec and spec.loader
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def independent_matchings(vertices):
 if not vertices:yield ();return
 first=vertices[0]
 for pos in range(1,len(vertices)):
  for tail in independent_matchings(vertices[1:pos]+vertices[pos+1:]):yield tuple(sorted(((first,vertices[pos]),)+tail))
PM8=tuple(sorted(independent_matchings(tuple(range(8)))));SUPPORTED=tuple(m for m in PM8 if set(m)<=SUPPORT)
assert len(PM8)==105 and len(SUPPORTED)==13 and len(RETAINED)==10

def configure_engine(engine):
 # Only the generic exact Cramer implementation is reused. All source sets are overwritten and rederived here.
 engine.FIXED=FIXED;engine.VARIABLE=VARIABLE;engine.ADDED=ADDED;engine.ELIMINATED=ELIMINATED;engine.OUTSIDE=OUTSIDE
 engine.NONFIXED=NONFIXED;engine.RETAINED=RETAINED;engine.SUPPORT=SUPPORT;engine.SUPPORTED=SUPPORTED

def carrier_replay():
 # cap03/star4 forbidden responses: pair26 switched and pair56 switched.
 cap=(0,3);center=4;residual=tuple(v for v in range(8) if v not in cap)
 terms=[]
 for a,b in itertools.combinations(residual,2):
  if center in (a,b):continue
  direct=(tuple(sorted((cap[0],a))),tuple(sorted((cap[1],b))))
  switched=(tuple(sorted((cap[0],b))),tuple(sorted((cap[1],a))))
  if set(direct)<=SUPPORT:terms.append((a,b,"direct",direct))
  if set(switched)<=SUPPORT:terms.append((a,b,"switched",switched))
 assert terms==[(2,6,"switched",((0,6),(2,3))),(5,6,"switched",((0,6),(3,5)))]
 return {"cap":"03","center":4,"terms":["R26=A06^T*K*A23^T","R56=A06^T*K*A35"],"factorization":"A06^T*K*[A23^T|A35]"}

def build_program(engine,record):
 entry,variables,determinant,outside_entry=engine.build_context(record);equations=[]
 for word in itertools.product(COLORS,repeat=8):
  value=engine.amplitude(entry,word);equations.append(engine.difference(value,"1") if len(set(word))==1 else value)
 p=record[1]
 for i,j in itertools.product(COLORS,repeat=2):
  if j!=p:equations.append(engine.summation(engine.product(entry((0,6),i,k),entry(OUTSIDE,j,k)) for k in COLORS))
 for i,j in itertools.product(COLORS,repeat=2):
  correction=engine.summation(engine.product(entry((1,7),i,k),entry((2,6),k,l),entry(OUTSIDE,j,l)) for k,l in itertools.product(COLORS,repeat=2))
  equations.append(engine.difference(entry(OUTSIDE,j,i),correction))
 equations.append(engine.product("abar","beta",outside_entry,determinant,"sat")+"-1")
 assert len(variables)==91 and len(equations)==6577 and len(set(equations))==6577 and all(x not in ("0","1","-1") for x in equations)
 return "\n".join(["// REP2 DESIGN INPUT ONLY: zero ideal runs authorized.","option(noredefine);",f"ring r=0,({','.join(variables)}),dp;","ideal I="+",\n".join(equations)+";",'print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));',"quit;",""])

def validate(result):
 assert result["schema"]=="KRENN_X5_REP2_CORRECTED_GUARD_MINOR_CONTRACTION_DESIGN_V1"
 assert result["status"]=="PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN"
 assert result["counts"]=={"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1}
 assert result["chart_census"]=={"raw":972,"S3_orbits":162,"orbit_size":6,"y_orbits":81,"z_orbits":81}
 assert result["scope"]=={"materialized_design_inputs":2,"ideal_runs":0,"rep2_closed":False,"support_transport_claimed":False}
def hostile(result,mutation):
 candidate=copy.deepcopy(result);mutation(candidate)
 try:validate(candidate)
 except (AssertionError,KeyError,TypeError):return True
 return False

def main():
 for path,expected in PINS.items():assert sha(path)==expected,(path,sha(path),expected)
 obligation=json.loads(OBL.read_text())["six_full_family_representatives"][2]
 assert obligation["added"]==["06","14","17","23","26","56","57"]
 assert obligation["guard"]["derived"]==["A56^T=-A26*A57^T","(I-A17*A26)*A57^T=0","A06*A57^T=0"]
 exhaustive=json.loads((EXH/"results_rep2_exhaustive_carrier.json").read_text())
 assert exhaustive["support"]["added_nonzero"]==obligation["added"]
 selected=exhaustive["closing_carrier"]
 assert selected["cap"]=="03" and selected["star_center"]==4
 assert selected["expanded_ledger_factor"]=="A06^T*K*[A23^T|A35]"
 assert carrier_replay()["factorization"]==selected["expanded_ledger_factor"]
 engine=load_engine();configure_engine(engine)
 digest,census=engine.parent_digest_and_census();assert digest==obligation["full_x5_6561_equation_sha256"]=="46a64a3e1ab088b6121430b229ae89503f93c9473d693fdef9af294c4af8a81d"
 assert {str(k):v for k,v in census.items()}==obligation["full_x5_term_count_census"]
 raw,groups=engine.orbit_ledger();assert engine.cramer_symbolic_replay()==12
 inputs={}
 for kind,chart in (("y",TINY_Y),("z",TINY_Z)):
  assert engine.orbit_representative(chart)==chart
  program=build_program(engine,chart);path=HERE/f"rep2_corrected_guard_minor_tiny_{kind}_Q.sing";tmp=path.with_suffix(".sing.tmp");tmp.write_text(program);os.replace(tmp,path)
  inputs[kind]={"chart":list(chart),"path":path.name,"sha256":hashlib.sha256(program.encode()).hexdigest(),"bytes":len(program.encode())}
 ledger={"raw":len(raw),"groups":[{"representative":list(rep),"size":len(members),"members":[list(x) for x in sorted(members)]} for rep,members in sorted(groups.items())]}
 lp=HERE/"chart_orbit_ledger.json";tmp=lp.with_suffix(".json.tmp");tmp.write_text(json.dumps(ledger,indent=2,sort_keys=True)+"\n");os.replace(tmp,lp)
 result={"schema":"KRENN_X5_REP2_CORRECTED_GUARD_MINOR_CONTRACTION_DESIGN_V1","status":"PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN",
  "independent_source_reconstruction":{"fixed":["03","16","27","45"],"variable":["04","12","35","67"],"added":["06","14","17","23","26","56","57"],"supported_matchings":["|".join(f"{a}{b}" for a,b in m) for m in SUPPORTED],"supported_matching_count":13,"full_x5_digest":digest,"term_census":census},
  "corrected_system":{"original_guard":["A06*A57^T=0","A57^T+A17*A56^T=0","A26*A57^T+A56^T=0"],"elimination":"A56=-A57*A26^T","reduced_guard":["A06*A57^T=0","(I-A17*A26)*A57^T=0"],"carrier":carrier_replay(),"incidence":["A06*x=e_i","A23^T*y+A35*z=e_i"],"superseded_carrier":"A04^T*K*[A23^T|A35] is not the guard-controlled corrected system"},
  "chart_cover":{"outside":"choose A57[p,q]!=0 and v=row_p(A57)","x":"choose x_r!=0; w=x/x_r and A06*w=abar*e_i","minor":"A06*v=0 and abar!=0 make w,v independent; v_q!=0 gives a nonzero w/v minor d involving q","partner":"choose nonzero y_s or z_s; y solves row s of A23, z solves column s of A35","saturation":"abar*beta*A57[p,q]*d*sat-1","reverse":"all factors are invertible on the chart, so Cramer reconstruction exactly restores guard and incidence"},
  "substitution":{"A06":"all nine entries solved","partner_y":"row s of A23 solved","partner_z":"column s of A35 solved","A56":"-A57*A26^T","tautologies_removed":["six incidence equations","three row-p A06*A57^T equations"]},
  "reuse_audit":{"generic_cramer_engine_sha256":PINS[ENGINE],"source_sets_overwritten_and_recomputed":True,"rep2_semantic_digest_independently_replayed":True,"support_transport_used":False,"generic_cramer_identities_replayed":12},
  "counts":{"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1},
  "chart_census":{"raw":len(raw),"S3_orbits":len(groups),"orbit_size":6,"y_orbits":sum(k[4]=="y" for k in groups),"z_orbits":sum(k[4]=="z" for k in groups)},"orbit_ledger":{"path":lp.name,"sha256":sha(lp)},"materialized_inputs":inputs,"pins":{str(p.relative_to(ROOT)):v for p,v in PINS.items()},"scope":{"materialized_design_inputs":2,"ideal_runs":0,"rep2_closed":False,"support_transport_claimed":False}}
 validate(result);tests={"count_mutation":hostile(result,lambda x:x["counts"].__setitem__("new_variables",90)),"orbit_mutation":hostile(result,lambda x:x["chart_census"].__setitem__("S3_orbits",161)),"run_injection":hostile(result,lambda x:x["scope"].__setitem__("ideal_runs",1)),"transport_overclaim":hostile(result,lambda x:x["scope"].__setitem__("support_transport_claimed",True))};assert all(tests.values());result["hostile_tests"]=tests
 out=HERE/"results_rep2_corrected_contraction_design.json";tmp=out.with_suffix(".json.tmp");tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");os.replace(tmp,out)
 print(json.dumps({"status":result["status"],"variables":91,"generators":6577,"orbits":162,"runs":0},sort_keys=True))
if __name__=="__main__":main()
