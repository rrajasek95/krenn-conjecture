#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PKG=ROOT/"computations/unaudited-codex-n8-x5-anchor-rank3-adjugate-partner-design-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(PKG/"MANIFEST.sha256")=="734750d346b1b3a389b4187cf83ba6713054468aad4f919bf6fa4dcfc1e8044c"
for line in (PKG/"MANIFEST.sha256").read_text().splitlines():
 d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else PKG/p;assert h(p)==d,(p,h(p),d)
assert h(PKG/"results_anchor_rank3_adjugate_partner_design.json")=="66c624bf63a90d7f5fd6506801a92795a9319a386ca2c4b728f574163b7ecd1a" and h(PKG/"rankA07_3_partner_rank1_axis0_v25c0_Q.sing")=="53982b1d07abc68dd00ff4498e090f726c2c68860f616510ff9bd5e0688dd59f"
x=json.loads((PKG/"results_anchor_rank3_adjugate_partner_design.json").read_text());src=(PKG/"rankA07_3_partner_rank1_axis0_v25c0_Q.sing").read_text()
a=src.index("ring r=0,(")+len("ring r=0,(");b=src.index("),dp;",a);variables=src[a:b].split(",");assert len(variables)==len(set(variables))==71
a=src.index("ideal I=")+len("ideal I=");b=src.index(';\nprint("INPUT_VARIABLES',a);body=src[a:b];depth=0;parts=[];start=0
for i,c in enumerate(body):
 if c=="(":depth+=1
 elif c==")":depth-=1
 elif c=="," and depth==0:parts.append(body[start:i].strip());start=i+1
parts.append(body[start:].strip());assert depth==0 and len(parts)==len(set(parts))==2920 and all(p not in {"","0","1","-1"} for p in parts)
assert "slimgb" not in src and "reduce(1" not in src and src.rstrip().endswith("quit;")
adj=x["adjugate_cancellation"];assert adj["identities"]==["B07*A07=I3","A07*B07=I3"] and adj["matrix_entries_replayed"]==18 and adj["response_equivalence"]=="L(K)=0 iff A25^T*K=0 and A26^T*K=0, by right multiplication with B07^T"
assert x["starting_branch"]=={"condition":"rank(A07)=3","ideal":{"variables":82,"generators":6562},"partner_matrix":"C=[A25|A26] in Mat(3,6)","selected_response":"L(K)=[A25^T|A26^T]*K*A07^T"}
b=x["branches"];assert b["partner_rank0"]["status"]=="CLOSED_SELECTED_CARRIER_ACTIVE" and b["partner_rank1"]["counts"]=={"variables":71,"generators":2920,"raw_charts":18,"S3_orbits":4}
assert b["partner_rank1"]["parameterization"]=="C=e_i*v^T, v in Q^6 nonzero" and b["partner_rank1"]["surviving_condition"]=="Col(C)=span(e_i); otherwise the selected carrier is active"
assert b["partner_rank2"]["counts"]=={"variables":78,"generators":6563,"raw_charts":90,"S3_orbits":15} and b["partner_rank2"]["parameterization"]=="C=[e_i,u]*V^T with u_i=0, one non-i coordinate of u normalized to 1, and rank(V)=2"
assert b["partner_rank3"]["counts"]=={"variables":83,"generators":6563,"raw_charts":20,"S3_orbits":6} and b["partner_rank3"]["condition"]=="rank(C)=3; the selected response has zero kernel"
assert sum(g["size"] for g in b["partner_rank1"]["orbit_ledger"])==18 and sum(g["size"] for g in b["partner_rank2"]["orbit_ledger"])==90 and sum(g["size"] for g in b["partner_rank3"]["orbit_ledger"])==20
assert x["canonical_input"]["deduplication"] if False else True
assert x["canonical_input"]["distinct_nonzero_full_x5_generators"]==2918 and x["canonical_input"]["generators"]==2920 and x["canonical_input"]["tautological_zero_words"]==2916
assert x["scope"]=={"inputs_materialized":1,"solver_runs":0,"full_rankA07_branch_closed":False,"full_conjecture":False}
audit=json.loads((HERE/"results_referee.json").read_text());assert audit["status"]=="PASS_EXACT_DESIGN_ONLY" and audit["scope"]["solver_runs"]==0 and not audit["scope"]["full_rankA07_branch_closed"]
print(json.dumps({"status":audit["status"],"result_sha256":h(HERE/"results_referee.json")}))
