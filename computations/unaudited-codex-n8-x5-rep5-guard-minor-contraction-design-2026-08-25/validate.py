#!/usr/bin/env python3
import hashlib,json
from pathlib import Path

here=Path(__file__).resolve().parent
path=here/"results_rep5_contraction_design.json";x=json.loads(path.read_text())
assert x["schema"]=="KRENN_X5_REP5_GUARD_MINOR_CONTRACTION_DESIGN_V1"
assert x["status"]=="PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN"
assert x["counts"]=={"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1}
assert x["chart_census"]=={"raw":972,"S3_orbits":162,"orbit_size":6,"y_orbits":81,"z_orbits":81}
assert x["scope"]=={"materialized_design_inputs":2,"ideal_runs":0,"rep5_closed":False,"transport_claimed":False}
assert x["symbolic_replay"]=={"generic_cramer_polynomial_identities":12,"parent_semantic_digest_replayed":True}
assert all(x["hostile_tests"].values())
for record in x["materialized_inputs"].values():
 source_path=here/record["path"];source=source_path.read_text()
 assert hashlib.sha256(source_path.read_bytes()).hexdigest()==record["sha256"]
 assert len(source_path.read_bytes())==record["bytes"]
 variables=source.split("ring r=32003,(",1)[1].split("),dp;",1)[0].split(",")
 equations=source.split("ideal I=",1)[1].split(";\nprint",1)[0].split(",\n")
 assert len(variables)==len(set(variables))==91
 assert len(equations)==len(set(equations))==6577
 assert source.count("ideal G=slimgb(I);")==1
assert not (here/"result.json").exists() and not (here/"stdout.txt").exists()
print(json.dumps({"status":"PASS_DESIGN_ONLY","result_sha256":hashlib.sha256(path.read_bytes()).hexdigest()},sort_keys=True))
