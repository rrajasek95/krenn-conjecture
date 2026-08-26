#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
p=Path(__file__).with_name("results_referee.json")
x=json.loads(p.read_text())
assert x["status"] == "PASS_UNIT_IDEAL_EXACT_Q_GROUP15_ONLY"
assert (x["input_variables"],x["input_generators"],x["groebner_basis_size"],x["unit_remainder"]) == (91,6577,1,0)
assert x["preflight_no_overlap"] and x["atomic_no_tmp"] and x["resource_clear"]
assert not x["automatic_relaunch"] and not x["other_groups_run"]
print(json.dumps({"status":"PASS", "result_sha256":hashlib.sha256(p.read_bytes()).hexdigest()}))
