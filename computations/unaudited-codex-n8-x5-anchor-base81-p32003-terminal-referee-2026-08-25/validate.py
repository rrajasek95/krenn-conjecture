#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((H/"results_referee.json").read_text())
assert x["status"]=="PASS_ONE_MODULAR_UNIT_DIAGNOSTIC_ONLY" and x["variables"]==81 and x["generators"]==6561 and x["groebner_basis_size"]==1 and x["unit_remainder"]==0
assert x["result_sha256"]=="116254d745e80ffe323d046cd958ef12ab598cf7ac80d32a37b739b2426f98c5" and not x["mathematical_coverage"] and not x["anchor_family_closed"] and not x["conjecture_closed"]
print(json.dumps({"status":"PASS_MODULAR_DIAGNOSTIC_ONLY","audit_sha256":h(H/"results_referee.json")},sort_keys=True))
