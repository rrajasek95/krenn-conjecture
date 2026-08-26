#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((HERE/"results_referee.json").read_text())
assert r["status"]=="PASS_APPROVED_HELD_ZERO_RUNS" and r["producer"]=={"plan_sha256":"0b0751748c3f19daa7635dae395d109c441a64c57243336d9e19c44546189b2f","manifest_sha256":"61b90e0976729a61a576aee55af309b3c17adac1973349821bd34b7f3c408dff"}
assert [x["orbit"] for x in r["lanes"]]==[0,1,2,3,4] and [x["raw_orbit_size"] for x in r["lanes"]]==[6,6,6,6,3]
assert all(x["field"]=="Q" and x["variables"]==80 and x["generators"]==6574 and x["execution_source_bytes"]==553541 for x in r["lanes"])
assert r["schedule"]=={"exact_orbit_order":[0,1,2,3,4],"sequential":True,"maximum_lanes":5,"parallel_lanes":1,"stop_first_nonunit_timeout_resource_process_observer_or_mismatch":True,"skip_or_reorder":False,"automatic_relaunch":False,"rank1_authorized":False}
assert r["held_state"]=={"solver_runs":0,"execution_sources_materialized":False,"runner_present":False,"fresh_clearance_present":False,"launch_authorized":False,"requires_new_manager_clearance":True} and all(r["hostile_tests"].values())
print(json.dumps({"status":"PASS","result_sha256":h(HERE/"results_referee.json")},sort_keys=True))
