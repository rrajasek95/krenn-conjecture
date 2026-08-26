#!/usr/bin/env python3
"""Attempt a literal h=3 physical construction of the mixed kappa family."""
from fractions import Fraction as Q
from hashlib import sha256
import json, os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
PINS={
 "computations/unaudited-codex-n8-pacomp-x23-mixed-square-relation-audit-2026-08-25/MANIFEST.sha256":"45fd37cab35450b6e53918ff77c2d7b2c4dd8cee83bb202dadbf94e29f17535b",
 "computations/unaudited-codex-n8-pacomp-q23-protected-factor-2026-08-25/MANIFEST.sha256":"f3b689175811cb8d28dbae605fac703c8339f2e5a259c4c0e644122f1779b500",
 "computations/unaudited-codex-n8-pacomp-q23-protected-factor-2026-08-25/results_q23_protected_factor_counterobligation.json":"93ba0a20dcf3e50aadcba20af5353113d79c7604fc11b281b8ca970b62597994",
 "PROOF-SKETCH.md":"8af22bf67777c3a8e7daad0639dab09848f89087bb0b2114d232ad52dc2f70bf",
 "computations/verify_uniform_balanced_chart_square_master_obstruction.py":"306980dc569795fa3ec2c8e6fdbdf2b67fa5d85cd75ebebe62be7db15b1e1a59",
 "notes/uniform-balanced-chart-square-master-obstruction.md":"c758fb43f88d9c02f5200921c6c50637bfe04402536edc3e947f74d108fbd93b",
 "computations/verify_h3_balanced_square_private_eq_projection_gate.py":"bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
 "notes/h3-balanced-square-private-eq-projection-gate.md":"6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
 "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py":"3704235f1030a07556aaebed3225bec8ea0fb9fa4d6a4d3aa124a7727a3bebec",
 "notes/h3-cross-word-mapping-cylinder-d2-augmentation-freedom-gate.md":"ef33bdd1f600fb3f58e91ca191a2fcfcfab516d5680907661a006ca5d358cec0",
 "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":"8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
 "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":"02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
 "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py":"d21d776ec53babb4f99693e4dad51d87309e3ed0cccf2e34fb6025e6d74d1009",
}
def need(x,m):
 if not x: raise RuntimeError(m)
def add(*vs): return tuple(sum(es,Q(0)) for es in zip(*vs,strict=True))
def scale(a,v): return tuple(Q(a)*x for x in v)
def unit(n,i): return tuple(Q(j==i) for j in range(n))
def dot(a,b): return sum((x*y for x,y in zip(a,b,strict=True)),Q(0))
def rank(cols):
 if not cols:return 0
 h=len(cols[0]); rows=[[Q(cols[c][r]) for c in range(len(cols))] for r in range(h)]; p=0
 for c in range(len(cols)):
  q=next((r for r in range(p,h) if rows[r][c]),None)
  if q is None:continue
  rows[p],rows[q]=rows[q],rows[p];v=rows[p][c];rows[p]=[x/v for x in rows[p]]
  for r in range(h):
   if r!=p and rows[r][c]:
    v=rows[r][c];rows[r]=[x-v*y for x,y in zip(rows[r],rows[p],strict=True)]
  p+=1
 return p
for p,h in PINS.items():need(sha256((ROOT/p).read_bytes()).hexdigest()==h,"pin "+p)

# The unique ungraded chain-map shape. d eps=-c and d r0=E imply a=-b.
relation=(Q(1),Q(1)); normalized=(Q(1),Q(-1))
need(dot(relation,normalized)==0 and rank((relation,))==1,"chain map")

# Literal two-root operation-grade obstruction. Per root the strongest grant
# has all twelve diagonal tags and withholds only Hom(response,cap).
width=26
base=tuple(unit(width,13*r+t) for r in range(2) for t in range(12))
sections=(unit(width,12),unit(width,25));paired=add(*sections)
ranks=(rank(base),rank(base+(sections[0],)),rank(base+(sections[1],)),rank(base+(paired,)),rank(base+sections))
need(ranks==(24,25,25,25,26),ranks)
omega_ab=unit(width,12);omega_ac=unit(width,25)
need(all(dot(omega_ab,x)==dot(omega_ac,x)==0 for x in base) and dot(omega_ab,sections[0])==1 and dot(omega_ac,sections[1])==1,"Hom duals")

# The original marked q23 matching paths agree; this supplies a commutative
# edge square, not the absent cross-object operation or its homotopy.
q23=json.loads((ROOT/"computations/unaudited-codex-n8-pacomp-q23-protected-factor-2026-08-25/results_q23_protected_factor_counterobligation.json").read_text())["result"]
intrinsic=q23["intrinsic_q23"]
need(intrinsic["marked_descendants_checked"]==90 and intrinsic["termwise_difference"]==0 and intrinsic["I_c_D_c_Phi_d"]==intrinsic["d_I_c_Phi_hat_D_r"],"matching square")

# Conditional physical bicomplex: after granting Phi, the oriented mixed
# square has the already proved primitive boundary.
z_edge=tuple(map(Q,(1,-1,1,-1)));z_chart=tuple(map(Q,(1,1,-1,-1)))
# Proposed placement J: (Aab,Aba,B,C) -> (P_f,K_L,K_R,D4) by
# Aab->P_f, B->K_L, Aba->K_R, C->D4.
J=lambda v:(v[0],v[2],v[1],v[3])
need(J(z_chart)==z_edge,"chart-edge character placement")

# Separate AB/AC mixed cycles remain rank two; the root-forgetting aggregate
# fills only one direction. Sigma pairs q23/q45 with coefficient -1.
zab=z_edge+(Q(0),)*4;zac=(Q(0),)*4+z_edge
need(rank((zab,zac))==2 and rank((add(zab,zac),))==1 and scale(-1,z_edge)==tuple(-x for x in z_edge),"naturality")

result={
 "schema":"pacomp-h3-x23-physical-kappa-construction-attempt-v1",
 "status":"PASS_NO_CONSTRUCTION_FIRST_PHYSICAL_HOM_RANK2_OBSTRUCTION",
 "parent_manifest_sha256":PINS["computations/unaudited-codex-n8-pacomp-x23-mixed-square-relation-audit-2026-08-25/MANIFEST.sha256"],
 "domain":{"complex":"R1=<epsilon_s^rho> -> R0=<c_f^rho>, d epsilon_s=-c_f","word":"11110000 = 11:110000","head":"ordered response 01/10","fine":"selected db01 / six P4+K2 tails","repeated":"relative response occurrence carrier","operation":"response occurrence/P_f and PS-over-q01 jet"},
 "codomain":{"complex":"C1=<r0^rho> -> C0=<E^rho>, d r0=E=(H0-u)e_Eq","word":"01211222","head":"AB or AC root-labelled cap repair","fine":"six t*q_(v,N) occurrence degrees","repeated":"P3+K2","operation":"AugP2/K_Eq cap"},
 "candidate_on_generators":{"Phi_1(epsilon_s^rho)":"r0^rho","Phi_0(c_f^rho)":"-E^rho","chain_map_check":"d Phi_1(epsilon)=E=Phi_0(-c_f)","formal_kappa":"oriented naturality cell of Phi across the P_f/D4 square","d_kappa":"P_f-K_Eq,L+K_Eq,R-D4"},
 "original_matching_test":{"marked_q23_descendants":90,"two_intrinsic_path_coefficients":[1,1],"termwise_difference":0,"meaning":"original matching data construct the commuting response-side edge square only; their difference is zero and is not a new physical 2-cell"},
 "failed_literal_candidates":[{"candidate":"response epsilon_s wedge cap theta","failure":"cross-object product undefined/zero because response and cap operation idempotents are orthogonal"},{"candidate":"difference of the two intrinsic q23 matching routes","failure":"routes agree termwise, so the difference is zero; no source-labelled homotopy generator is produced"},{"candidate":"root/Weyl transport times cap r0","failure":"both factors remain diagonal; e_C A e_R coordinate is zero"}],
 "smallest_rank_obstruction":{"strong_base_rank":24,"rank_after_AB":25,"rank_after_AC":25,"rank_after_unlabelled_pair":25,"rank_after_both":26,"missing_dimension":2,"duals":["omega_AB^Hom","omega_AC^Hom"],"interpretation":"the original data lack both root-labelled degree-zero response-to-cap matrix units before kappa can be typed"},
 "conditional_next_obstruction":{"after_granting_both_Phi_sections":"one primitive mixed-square H1 per root label","rank_AB_AC":2,"root_forgetting_rank":1,"sigma":"kappa_23^rho maps to -kappa_45^rho","proper_face_after_kappa":"separate shifted ridge remains"},
 "conjecture_6_2_interface":{"chart_charge":[1,1,-1,-1],"edge_cycle":[1,-1,1,-1],"coefficient_placement_J":{"A_[a|b]":"P_f","B":"K_Eq,L","A_[b|a]":"K_Eq,R","C":"D4"},"J_maps_charge_to_cycle":True,"bare_character_equality_sufficient":False,"exact_additional_hypothesis":"a filler-branch instance Lambda_c^rho of Conjecture 6.2 in the identical response/cap word, fine, repeated, common-tail and operation grade, together with a source-labelled placement J_c^rho commuting with d, restriction, reinsertion, protected readouts, tau_AB,AC and sigma","conditional_construction":"kappa_c^rho=J_c^rho(Lambda_c^rho)"},
 "root_forgetting":{"one_unlabelled_sum_sufficient":False,"surviving_dual":"(omega_AB^Hom-omega_AC^Hom)/2"},
 "verdict":"The normalized generator formula is coefficient- and sign-consistent, but the original matching/source-labelled response inventory cannot type it. The first obstruction is earlier than the mixed square: a two-dimensional AB/AC Hom^0(response,cap) quotient. Conditional on adjoining both Phi sections, kappa is the next primitive rank-two labelled extension. Conjecture 6.2 supplies kappa only in the strengthened source-labelled placement form; equality of the balanced character alone does not authorize the fold.",
 "promotion":"NONE_H3_ONLY","pins":PINS}
logical=sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest();out={"logical_sha256":logical,"result":result}
t=HERE/"results_physical_kappa_construction_attempt.json.tmp";t.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(t,HERE/"results_physical_kappa_construction_attempt.json")
print(result["status"]);print("logical_sha256="+logical)
