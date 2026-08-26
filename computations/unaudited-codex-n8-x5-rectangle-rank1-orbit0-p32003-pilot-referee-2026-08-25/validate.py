#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent;p=here/"results_referee.json";x=json.loads(p.read_text())
assert x["status"]=="PASS_MODULAR_UNIT_IDEAL_ORBIT0_ONLY"
assert x["producer_manifest_sha256"]=="6e7f7683a40b2dc1d81939d13b4079da732a0921aea16998caa50eaeb4989858"
assert x["producer_result_sha256"]=="17e1ded6a6f42929f3ac8feb92874bc1c1b72725a57fecf3c8e84f23eac9df9a"
assert x["source_sha256"]=="7c34d1efbf74220f01a6ea150ede232b9f51f9168f15dd997ed2b204e8aacf9c"
assert x["runner_sha256"]=="bf92688cdf807776971834dcd3d3a84c90de738145edf3f618c09e7798640b19"
assert x["counts"]=={"variables":76,"generators":6571,"groebner_basis_size":1,"unit_remainder":0}
assert x["wall_seconds"]==14.562766416929662 and x["peak_rss_bytes"]==468594688
assert x["atomic_no_tmp"] is True and x["exact_Q_second_relaunch"] is False
print(json.dumps({"status":"PASS","result_sha256":hashlib.sha256(p.read_bytes()).hexdigest()},sort_keys=True))
