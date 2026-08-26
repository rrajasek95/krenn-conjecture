#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent/"results_referee.json";x=json.loads(p.read_text())
assert x["status"]=="PASS_MODULAR_UNIT_DIAGNOSTIC_ONLY_NO_Q_PROMOTION"
assert x["source"]["p32003_sha256"]=="a6170f8e48329830d371bf0365067511642f4802576302f43e6edae2b734df3c"
assert (x["source"]["variables"],x["source"]["generators"])==(56,6563)
assert x["result"]["groebner_basis_size"]==1 and x["result"]["unit_remainder"]==0
assert x["resources"]["elapsed_seconds"]==22.93639 and x["resources"]["peak_rss_kib"]==1104100
assert x["run_scope"]=={"modular_lanes":1,"Q_lanes":0,"second_lane":False,"relaunch":False}
q=x["exact_Q_held_plan"];assert q["status"].startswith("HELD_NOT_RUN") and q["maximum_lane_count"]==1 and q["no_relaunch"] is True
print(json.dumps({"status":"PASS","result_sha256":hashlib.sha256(p.read_bytes()).hexdigest()},sort_keys=True))
