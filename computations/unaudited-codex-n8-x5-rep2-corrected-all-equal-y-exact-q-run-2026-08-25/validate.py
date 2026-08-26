#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads((HERE/"results_independent_referee.json").read_text())
assert x["status"]=="PASS_EXACT_Q_ONE_REFINED_CHART_ONLY" and x["same_chart_closed"]
assert not x["rep2_closed"] and not x["seven_block_family_closed"] and not x["conjecture_closed"]
assert x["variables"]==91 and x["generators"]==6577 and x["groebner_basis_size"]==1 and x["unit_remainder"]==0
assert x["attempt_result_sha256"]=="043bb1fb15fec4291248c62036ed6594b34c8322207b93b6160c6c846c8d25a3"
print(json.dumps({"status":"PASS_ONE_CHART_ONLY","audit_sha256":h(HERE/"results_independent_referee.json")},sort_keys=True))
