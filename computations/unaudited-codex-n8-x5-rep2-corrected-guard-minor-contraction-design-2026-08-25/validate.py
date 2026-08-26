#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/"results_rep2_corrected_contraction_design.json").read_text())
assert r["schema"]=="KRENN_X5_REP2_CORRECTED_GUARD_MINOR_CONTRACTION_DESIGN_V1"
assert r["status"]=="PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN"
assert r["corrected_system"]["carrier"]["factorization"]=="A06^T*K*[A23^T|A35]"
assert r["counts"]=={"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1}
assert r["chart_census"]=={"raw":972,"S3_orbits":162,"orbit_size":6,"y_orbits":81,"z_orbits":81}
assert r["scope"]=={"materialized_design_inputs":2,"ideal_runs":0,"rep2_closed":False,"support_transport_claimed":False}
lp=HERE/r["orbit_ledger"]["path"];ledger=json.loads(lp.read_text());assert sha(lp)==r["orbit_ledger"]["sha256"] and ledger["raw"]==972 and len(ledger["groups"])==162 and {x["size"] for x in ledger["groups"]}=={6}
for item in r["materialized_inputs"].values():
 p=HERE/item["path"];s=p.read_text();assert sha(p)==item["sha256"] and p.stat().st_size==item["bytes"]
 assert "slimgb" not in s and "std(" not in s and s.rstrip().endswith("quit;")
 assert len(s.split("ideal I=",1)[1].split(";",1)[0].split(",\n"))==6577
assert all(r["hostile_tests"].values())
print(json.dumps({"status":"PASS_STATIC_NO_SOLVE","result_sha256":sha(HERE/"results_rep2_corrected_contraction_design.json")},sort_keys=True))
