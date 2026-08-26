#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((H/"results_referee.json").read_text())
assert x["status"]=="PASS_EXACT_Q_UNIT_IDEAL_CANONICAL_BASE81_CHART" and x["field"]=="Q" and x["variables"]==81 and x["generators"]==6561
assert x["groebner_basis_size"]==1 and x["unit_remainder"]==0 and x["same_chart_closed"] and not x["anchor_family_closed"] and not x["conjecture_closed"]
assert x["result_sha256"]=="d654c02c299638111c9d5498948165d9f76f8c6a3e79c9d2da35ce0c661ae1b9"
print(json.dumps({"status":"PASS_EXACT_Q_SAME_CHART_ONLY","audit_sha256":h(H/"results_referee.json")},sort_keys=True))
