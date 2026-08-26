#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/"results_referee.json").read_text())
assert r["status"]=="PASS_APPROVED_HELD_ZERO_RUNS"
assert r["producer"]=={"plan_sha256":"e85c4db6414a47d9fb76e4310ab4bd114fc787cda2d766e032a77f9312b08575","manifest_sha256":"2fce75e1cd35178e03a42ae02aa60ac981529d229d28e0ab77d0eb51c1b7870f"}
assert [x["orbit"] for x in r["lanes"]]==[1,2,3,4]
assert all(x["field"]=="Q" and x["variables"]==76 and x["generators"]==6571 and x["execution_source_bytes"]==519397 for x in r["lanes"])
assert r["schedule"]=={"exact_orbit_order":[1,2,3,4],"sequential":True,"maximum_lanes":4,"parallel_lanes":1,"stop_first_nonunit_timeout_resource_process_or_mismatch":True,"skip_or_reorder":False,"automatic_relaunch":False,"rank2_authorized":False}
assert r["resource_contract"]["native_wall_seconds"]==480 and r["resource_contract"]["wrapper_wall_seconds"]==510 and r["resource_contract"]["rss_cap_bytes"]==8589934592
assert r["held_state"]=={"solver_runs":0,"execution_sources_materialized":False,"runner_present":False,"fresh_clearance_present":False,"launch_authorized":False,"requires_new_manager_clearance":True}
assert all(r["hostile_tests"].values())
print(json.dumps({"status":"PASS","result_sha256":h(HERE/"results_referee.json")},sort_keys=True))
