#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here=Path(__file__).resolve().parent
result_path=here/"results_adjugate_referee.json"; source_path=here/"rectangle_rank3_adjugate_Q.sing"
x=json.loads(result_path.read_text()); source=source_path.read_text()
assert x["schema"]=="KRENN_X5_RECTANGLE_RANK3_ADJUGATE_IDEAL_REFEREE_V1"
assert x["status"]=="PASS_EXACT_EQUIVALENT_DESIGN_NO_SOLVE"
assert x["counts"]=={"matrix_variables":54,"scalar_variables":2,"variables":56,"full_x5_generators":6561,"saturation_generators":2,"generators":6563}
assert len(x["adjugate_replay"]["identities"])==2 and x["adjugate_replay"]["polynomial_matrix_entries_checked"]==18
assert x["variants"]=={"A12_absent":"lift with A12=0 and A23=I","A12_present":"lift with A12=I and A23=I"}
assert x["scope"]=={"inputs_materialized":1,"solver_launches":0,"rank3_closed":False}
assert all(x["hostile_tests"].values())
assert hashlib.sha256(source_path.read_bytes()).hexdigest()==x["canonical_input"]["sha256"]=="e2739688ea9986d59c56e17e6f0058154d9ddb7930bf9617a1d3a3a8167538f5"
assert source.startswith("option(noredefine);\nring r=0,") and source.count("ideal G=slimgb(I);")==1
ideal=source.split("ideal I=",1)[1].split(";\nprint",1)[0]
assert len(ideal.split(",\n"))==6563
variables=source.split("ring r=0,(",1)[1].split("),dp;",1)[0].split(",")
assert len(variables)==len(set(variables))==56
assert not (here/"result.json").exists() and not (here/"stdout.txt").exists()
print(json.dumps({"status":"PASS_NO_SOLVE","source_sha256":x["canonical_input"]["sha256"],"result_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest()},sort_keys=True))
