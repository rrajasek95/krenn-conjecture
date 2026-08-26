#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();here=Path(__file__).resolve().parent;x=json.loads((here/"results_referee.json").read_text());p=json.loads((here/"EXACT_Q_SAME_CHART_HELD_PLAN.json").read_text())
assert x["status"]=="PASS_ONE_MODULAR_UNIT_DIAGNOSTIC_ONLY" and x["variables"]==91 and x["generators"]==6577 and x["groebner_basis_size"]==1 and x["unit_remainder"]==0 and not x["mathematical_coverage"]
assert not p["launch_authorized"] and p["solver_launches"]==0 and p["source"]["execution_Q_sha256"]=="5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf"
print(json.dumps({"status":"PASS", "result_sha256":h(here/"results_referee.json"),"held_q_plan_sha256":h(here/"EXACT_Q_SAME_CHART_HELD_PLAN.json")}))
