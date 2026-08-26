#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent/"results_referee.json";x=json.loads(p.read_text())
assert x["status"]=="PASS_EXACT_EQUIVALENT_DESIGN_NO_SOLVE_NO_CLOSURE"
assert x["counts"]=={"variables":56,"generators":6563,"full_x5":6561,"saturations":2}
assert x["adjugate_entries_replayed"]==18 and x["variants"]["amplitude_and_guard_inactive"] is True
g=x["held_modular_diagnostic"];assert g["maximum_lane_count"]==1 and g["status"].startswith("HELD_NOT_RUN") and g["automatic_relaunch"] is False
assert x["scope"]=={"solver_launches":0,"rank3_closed":False,"A12_variants_closed":False}
print(json.dumps({"status":"PASS","result_sha256":hashlib.sha256(p.read_bytes()).hexdigest()},sort_keys=True))
