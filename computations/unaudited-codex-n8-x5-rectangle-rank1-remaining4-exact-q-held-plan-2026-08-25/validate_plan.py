#!/usr/bin/env python3
import hashlib,json,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[2]; here=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((here/"HELD_PLAN.json").read_text())
assert p["status"]=="HELD_NOT_RUN_REQUIRES_INDEPENDENT_APPROVAL_AND_MANAGER_CLEARANCE" and not p["launch_authorized"]
assert [x["orbit"] for x in p["lanes"]]==[1,2,3,4] and [x["ordinal"] for x in p["lanes"]]==[1,2,3,4]
design=root/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25"
for lane in p["lanes"]:
 src=next(design.glob(f"rank1_orbit{lane['orbit']}_*_Q.sing")); assert h(src)==lane["design_source_sha256"]
 text=src.read_text(); old='print("INPUT_GENERATORS="+string(size(I)));\nquit;'; assert text.count(old)==1
 ep='print("INPUT_GENERATORS="+string(size(I)));\n'+'\n'.join(p["source_derivation"]["epilogue"])+"\nquit;"
 derived=text.replace(old,ep); assert len(derived.encode())==p["common_lane_contract"]["execution_source_bytes"]
 assert hashlib.sha256(derived.encode()).hexdigest()==lane["execution_source_sha256"]
c=p["common_lane_contract"]; assert (c["variables"],c["generators"],c["native_wall_seconds"],c["wrapper_wall_seconds"],c["rss_cap_bytes"])==(76,6571,480,510,8589934592)
e=p["execution"]; assert e["sequential"] and e["maximum_lanes"]==4 and e["parallel_lanes"]==1 and e["stop_on_first_nonunit"] and e["stop_on_first_resource_failure"] and e["stop_on_first_process_failure"] and not e["automatic_relaunch"]
assert p["rank2_launches_authorized"]==p["solver_launches"]==0 and not p["execution_sources_materialized"] and not p["runner_present"] and not p["fresh_clearance_present"]
print(json.dumps({"status":"PASS_HELD_PLAN_ZERO_RUN", "plan_sha256":h(here/"HELD_PLAN.json")}))
