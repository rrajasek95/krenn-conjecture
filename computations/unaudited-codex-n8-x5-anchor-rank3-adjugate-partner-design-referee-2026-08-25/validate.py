#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((here/"results_referee.json").read_text())
assert x["status"]=="PASS_EXACT_DESIGN_ONLY" and x["canonical_input"]=={"source_sha256":"53982b1d07abc68dd00ff4498e090f726c2c68860f616510ff9bd5e0688dd59f","variables":71,"generators":2920,"distinct_nonzero_full_x5":2918,"saturations":2}
assert x["scope"]=={"solver_runs":0,"partner_rank0_closed":True,"rank1_solved":False,"full_rankA07_branch_closed":False,"conjecture_closed":False}
print(json.dumps({"status":"PASS_DESIGN_ONLY","result_sha256":h(here/"results_referee.json")}))
