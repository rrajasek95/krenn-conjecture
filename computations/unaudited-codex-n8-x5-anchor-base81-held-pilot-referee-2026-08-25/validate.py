#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((here/"results_referee.json").read_text())
assert x["status"]=="PASS_APPROVE_HELD_ZERO_RUNS" and x["counts"]=={"variables":81,"generators":6561} and x["execution"]=={"solver_runs":0,"attempt_absent":True,"clearance_absent":True,"refusal_absent":True,"temporary_absent":True}
assert x["pilot_contract"]["native_wall_seconds"]==180 and x["pilot_contract"]["wrapper_wall_seconds"]==190 and x["pilot_contract"]["rss_cap_bytes"]==8589934592
print(json.dumps({"status":"PASS_HELD_ZERO_RUNS","result_sha256":h(here/"results_referee.json")}))
