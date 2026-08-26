#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((H/"results_referee.json").read_text())
assert x["status"]=="PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE" and x["result_sha256"]=="d3f1fcdfc61695c0f3557d99efb5ad79c777cc74aa85643f92e6cce7e13a22eb"
assert not x["unit_or_nonunit_result"] and not x["mathematical_coverage"] and x["attempt_consumed"] and not x["automatic_relaunch"]
assert not x["rep5_closed"] and not x["family_closed"] and not x["conjecture_closed"]
print(json.dumps({"status":"PASS_ZERO_COVERAGE_STOP","audit_sha256":h(H/"results_referee.json")},sort_keys=True))
