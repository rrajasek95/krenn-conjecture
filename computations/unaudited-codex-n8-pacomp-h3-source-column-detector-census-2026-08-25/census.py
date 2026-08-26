#!/usr/bin/env python3
"""Bounded exhaustive eta/eta_r census of the pinned executable h=3 source."""
from fractions import Fraction as Q
import hashlib, importlib.util, itertools, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PINS={
 ROOT/"computations/verify_h3_gamma_star_executable_gen_phys_registry.py":"173ebdedcfdadd9891704223ea93731509c18a4d120aa34d6c7bc8a4f3aebddb",
 ROOT/"computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":"2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
 ROOT/"computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py":"3b2cf3aa1cd6ee46f60c0e3621342f4eb15420d6d5d302546b2403d966703ba8",
 ROOT/"computations/unaudited-codex-n8-pacomp-h3-switch-charge-nonimplication-referee-2026-08-25/FINAL_MANIFEST.sha256":"4ba7073930e2c59c5f760fb0e24309fe08b0086cb105f3d1ce1bae62b56f2800",
 ROOT/"computations/unaudited-codex-n8-pacomp-x23-total-carrier-et-construction-audit-2026-08-25/MANIFEST.sha256":"f4c40ad4801fcf2950af2871e46eb6971e3a5fee12f124a8f37367d6e343117b",
 ROOT/"computations/unaudited-codex-n8-pacomp-x23-et-dependency-circularity-audit-2026-08-25/MANIFEST.sha256":"42573cc253b38b66eee8324e671124657728373fbcb707fbf9df71a360116009",
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);assert spec and spec.loader
 mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
def dot(a,b):return sum((Q(x)*Q(y) for x,y in zip(a,b,strict=True)),Q(0))
def frac(x):return str(x)
def replay_manifest(path):
 n=0
 for line in path.read_text().splitlines():
  if not line.strip():continue
  expected,rel=line.split(None,1);rel=rel.strip();target=path.parent/rel
  if not target.exists():target=ROOT/rel
  assert sha(target)==expected,(target,sha(target),expected);n+=1
 return n
for p,d in PINS.items():assert sha(p)==d,(p,sha(p),d)
replayed={str(p.relative_to(ROOT)):replay_manifest(p) for p in PINS if p.name.endswith("MANIFEST.sha256")}

reg=load(ROOT/"computations/verify_h3_gamma_star_executable_gen_phys_registry.py","detector_registry")
fixed=load(ROOT/"computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py","detector_fixed")
phi=load(ROOT/"computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py","detector_reachability")
reg.pin_dependencies()
maximal=reg.load("computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py","det_maximal")
private_eq=reg.load("computations/verify_h3_balanced_square_private_eq_projection_gate.py","det_private")
response=reg.load("computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py","det_response")
first_pp=reg.load("computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py","det_firstpp")
bar=reg.load("computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py","det_bar")
provenance=reg.load("computations/verify_h3_uc4_beq_tie_source_provenance_audit.py","det_provenance")
registry=reg.build_registry(maximal,private_eq,fixed,response,first_pp,bar,provenance)
assert len(registry.entries)==128 and registry.arrows=={}

columns,detector,LH,Lr,packet=fixed.audit_cartesian_physical_packet()
assert len(columns)==100 and packet["internal_rank"]==46
eta=tuple(v/Q(3) for v in detector)       # eta(L01_H)=2
eta_r=tuple(v/Q(6) for v in detector)     # eta_r(R_ret lift)=1
assert dot(eta,LH)==2 and dot(eta_r,Lr)==1

records=[]
for entry in registry.entries:
 row={"name":entry.name,"family":entry.family,"degree":entry.degree,
      "grade":{"word":entry.grade.word,"fine":entry.grade.fine,"repeated":entry.grade.repeated,"operation":entry.grade.operation,"window":entry.grade.window}}
 if entry.grade==reg.FIXED_WINDOW:
  assert len(entry.native_boundary)==48
  row.update({"detector_admissible":True,"eta":frac(dot(eta,entry.native_boundary)),"eta_r":frac(dot(eta_r,entry.native_boundary)),"protected_hit":False})
  assert row["eta"]==row["eta_r"]=="0"
 else:
  row.update({"detector_admissible":False,"eta":None,"eta_r":None,"excluded_reason":"orthogonal word/fine/repeated/operation/window idempotent"})
 records.append(row)
assert sum(r["detector_admissible"] for r in records)==100
assert sum(not r["detector_admissible"] for r in records)==28

# Overclose the literal degree-zero reindexings: every permutation of the four
# fixed words and three tail matchings, and the B<->C endpoint involution.
# This contains the allowed root/reinsertion, cut-sigma and tau reindexings.
def transform(v,wp,mp,tau):
 out=[Q(0)]*48
 for w,c,m in itertools.product(range(4),range(3),range(3)):
  cc=(2 if c==1 else 1 if c==2 else 0) if tau else c
  out[fixed.x_index(wp[w],cc,mp[m])]+=v[fixed.x_index(w,c,m)]
 for w,c in itertools.product(range(4),range(3)):
  cc=(2 if c==1 else 1 if c==2 else 0) if tau else c
  out[fixed.r_index(wp[w],cc)]+=v[fixed.r_index(w,c)]
 return tuple(out)
composition_hasher=hashlib.sha256();composition_count=0;unique=set()
for name,value in columns:
 for wp in itertools.permutations(range(4)):
  for mp in itertools.permutations(range(3)):
   for tau in (False,True):
    image=transform(value,wp,mp,tau);ev=dot(eta,image);rv=dot(eta_r,image)
    assert ev==rv==0
    digest=hashlib.sha256(repr(image).encode()).hexdigest();unique.add(digest)
    composition_hasher.update(f"{name}|{wp}|{mp}|{int(tau)}|{ev}|{rv}|{digest}\n".encode());composition_count+=1
assert composition_count==28800

# Strong upper bounds already sealed: even granting all four formal switch
# mates and the face-complete retained-r rows yields no detector hit.
switch_cols=((1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1));eta4=(1,1,-1,-1);target4=(2,0,0,0)
face_cols=((1,1,1,0,0),(1,0,0,1,1),(1,1,0,1,0),(1,0,1,0,1));eta5=(Q(1),Q(-1,2),Q(-1,2),Q(-1,2),Q(-1,2));target5=(1,0,0,0,0)
assert all(dot(eta4,c)==0 for c in switch_cols) and dot(eta4,target4)==2
assert all(dot(eta5,c)==0 for c in face_cols) and dot(eta5,target5)==1

# Genuine endpoint-choice primitives are the nearest nonzero detector rows,
# but they retain forbidden tB/tC proper faces and hence are not fillers.
eta_chart=(Q(1),Q(0),Q(0),Q(0),Q(0));gB=(1,-1,0,1,0);gC=(1,0,-1,0,1);gBC=tuple(Q(a)+Q(b) for a,b in zip(gB,gC))
assert dot(eta_chart,gB)==dot(eta_chart,gC)==1 and dot(eta_chart,gBC)==2
assert gB[3:]==(1,0) and gC[3:]==(0,1) and gBC[3:]==(1,1)

# Replay the implemented-operation reachability closure.  Even every one-site
# root remains in the response operation sector; the degree-zero cross-sector
# Hom is empty, so no admissible degree-one composite exists.
phi_ledger,phi_digest=phi.audit();assert phi_digest==phi.EXPECTED_LEDGER_SHA256
assert phi_ledger["maximally_generous_root_closure"]["typed_cap_r0_reached_without_new_edge"] is False
assert phi_ledger["first_new_edge"]["existing_degree_zero_Hom_dimension"]==0
assert phi_ledger["fixed_window_operation_gate"]["cross_profile_edges_present_in_internal_constructor"]==0

result={
 "schema":"PACOMP_H3_EXISTING_SOURCE_COLUMN_DETECTOR_CENSUS_V1",
 "status":"PASS_NO_ADMISSIBLE_EXISTING_PRIMITIVE_HITS_L01_OR_R_RET",
 "pins":{str(p.relative_to(ROOT)):d for p,d in PINS.items()},"manifest_entries_replayed":replayed,
 "executable_registry":{"primitive_entries":128,"degree_one_entries":128,"admissible_fixed_window_entries":100,"off_grade_entries":28,"registered_degree_zero_cross_operation_arrows":0,"records":records},
 "detectors":{"eta_normalization":{"L01":2,"histogram_on_100_admissible":{"0":100}},"eta_r_normalization":{"R_ret":1,"histogram_on_100_admissible":{"0":100}}},
 "one_step_reindexing_overclosure":{"images_checked":composition_count,"unique_boundary_images":len(unique),"eta_histogram":{"0":composition_count},"eta_r_histogram":{"0":composition_count},"ledger_sha256":composition_hasher.hexdigest(),"includes":"all actual word/root/reinsertion and cut-sigma/tau reindexings as a subset","degree_guard":"composing two degree-one cells is degree two; the only admissible degree-one composites require a degree-zero arrow, and none is registered"},
 "generous_upper_bounds":{"four_formal_switch_mates":{"columns":4,"eta_values":[0,0,0,0],"L01_value":2},"face_complete_retained_rows":{"columns":4,"eta_r_values":[0,0,0,0],"R_ret_value":1}},
 "nearest_genuine_source_columns":{"Gamma_B":{"eta_chart":1,"forbidden_proper_face":"t_B"},"Gamma_C":{"eta_chart":1,"forbidden_proper_face":"t_C"},"Gamma_B_plus_Gamma_C":{"eta_chart":2,"forbidden_proper_face":"T=t_B+t_C"},"conclusion":"nonzero detector shadows exist only with protected proper faces; subtracting them requires the absent E_T/Lambda_01 filler and is not an admissible one-step construction"},
 "symmetry_and_labels":{"physical_grade_preserved":True,"root_labels_not_identified":True,"tau":"B/C endpoint swap included; balanced four-corner detector is anti-equivariant in its sealed orientation","cut_sigma":"all three H2345 tail matchings overclosed by S3 permutations","reinsertion":"all four fixed words overclosed; H-r graph columns remain detector-dark"},
 "reachability":{"ledger_sha256":phi_digest,"all_site_root_grant_still_cap_unreachable":True,"existing_cross_operation_Hom_dimension":0,"new_edge_required":"Phi_KS,r0 / physical DQ-to-PS switch schema"},
 "scope":{"h":3,"existing_pinned_executable_libraries_only":True,"hypothetical_placement_maps":False,"new_primitives_added":0,"promotion":"NONE"},
}
out=HERE/"results_source_column_detector_census.json";out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":result["status"],"result_sha256":sha(out),"primitives":128,"compositions":composition_count},sort_keys=True))
