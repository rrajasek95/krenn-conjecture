#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here = Path(__file__).resolve().parent
p = here / "results_referee.json"
x = json.loads(p.read_text())
assert x["status"] == "PASS_EXACT_Q_UNIT_IDEAL_ONE_REFINED_ORBIT_ONLY"
assert x["source_Q_sha256"] == "53f741ca9173877ef1bc21dba2546a82102a32140221068de1301d0b4635dadb"
assert (x["variables"], x["input_generators"], x["groebner_basis_size"], x["unit_remainder"]) == (91, 6577, 1, 0)
assert x["wall_seconds"] == 9.307639292092063 and x["peak_rss_bytes"] == 267988992
assert x["approved_exact_q_lane_count"] == 1 and x["observed_second_lane_or_relaunch"] is False
assert x["scope"]["refined_orbits_closed"] == 1 and x["scope"]["refined_orbits_total"] == 162
assert x["scope"]["representative_1_closed"] is False and x["scope"]["seven_block_family_closed"] is False
print(json.dumps({"status":"PASS", "result_sha256":hashlib.sha256(p.read_bytes()).hexdigest()}, sort_keys=True))
