#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent/"results_source_column_detector_census.json";x=json.loads(p.read_text())
assert x["status"]=="PASS_NO_ADMISSIBLE_EXISTING_PRIMITIVE_HITS_L01_OR_R_RET"
assert x["executable_registry"]["primitive_entries"]==128 and x["executable_registry"]["admissible_fixed_window_entries"]==100
assert x["detectors"]["eta_normalization"]["histogram_on_100_admissible"]=={"0":100}
assert x["detectors"]["eta_r_normalization"]["histogram_on_100_admissible"]=={"0":100}
assert x["one_step_reindexing_overclosure"]["images_checked"]==28800
assert x["reachability"]["existing_cross_operation_Hom_dimension"]==0
assert x["scope"]["promotion"]=="NONE" and x["scope"]["new_primitives_added"]==0
print(json.dumps({"status":"PASS","result_sha256":hashlib.sha256(p.read_bytes()).hexdigest()},sort_keys=True))
