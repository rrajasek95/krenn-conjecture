#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((H/"results_referee.json").read_text())
assert x["status"]=="PASS_ONE_MODULAR_UNIT_DIAGNOSTIC_ONLY" and x["result_sha256"]=="ee2e2f35cb247bd8d2af6483b8757530baa2146a5df0372408188e458709bf3e"
assert x["variables"]==91 and x["generators"]==6577 and x["groebner_basis_size"]==1 and x["unit_remainder"]==0
assert not x["mathematical_coverage"] and not x["rep4_closed"] and not x["family_closed"] and not x["conjecture_closed"]
print(json.dumps({"status":"PASS_MODULAR_DIAGNOSTIC_ONLY","audit_sha256":h(H/"results_referee.json")},sort_keys=True))
