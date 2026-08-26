#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((here/"results_referee.json").read_text())
assert x["status"]=="PASS_DESIGN_AND_APPROVE_HELD_ONE_MODULAR_DIAGNOSTIC" and x["execution"]["modular_runs"]==0 and x["execution"]["clearance_files_absent"]
assert x["corrected_carrier"]=="A06^T*K*[A23^T|A35]" and x["counts"]=={"variables":91,"generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1}
assert x["pilot_contract"]=={"field":"F_32003","maximum_lanes":1,"native_wall_seconds":180,"wrapper_wall_seconds":195,"rss_cap_bytes":8589934592,"atomic_result":True,"runner_refuses_without_two_clearances":True}
print(json.dumps({"status":"PASS_HELD_ZERO_RUN","result_sha256":h(here/"results_referee.json")}))
