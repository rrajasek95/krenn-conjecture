#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_rank3_reduction.json"
x = json.loads(path.read_text())
assert x["schema"] == "KRENN_X5_RECTANGLE_4647_RANK3_REDUCTION_V1"
assert x["status"] == "PASS_EXACT_REDUCTION_NO_SOLVE"
assert x["factorization"]["verified_words"] == 6561
assert x["reduced_ideal"]["variables"] == 64 and x["reduced_ideal"]["generators"] == 6571
assert x["variants"]["A12_present"]["carrier_census"] == {"total":24,"forced_injective_inactive":10,"guard_undecided":14}
assert x["variants"]["A12_absent"]["carrier_census"] == {"total":40,"forced_injective_inactive":22,"guard_undecided":18}
assert x["scope"] == {"groebner_launches":0,"rank3_closed":False,"transported_records":0}
assert all(x["hostile_tests"].values())
print(json.dumps({"status":"PASS","result_sha256":hashlib.sha256(path.read_bytes()).hexdigest()},sort_keys=True))
