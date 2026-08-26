#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent/"results_referee.json"; x=json.loads(p.read_text())
assert x["status"]=="PASS_EXACT_972_TO_162_CENSUS_NO_IDEALS"
assert (x["raw_charts"],x["common_s3_groups"],x["members_per_group"],x["remaining_groups"])==(972,162,6,161)
assert x["support_graph_automorphisms"]==[list(range(8))] and x["distinct_Q_source_hashes"]==162
assert x["closed_source_sha256"]=="53f741ca9173877ef1bc21dba2546a82102a32140221068de1301d0b4635dadb"
assert x["ideal_launches"]==0 and x["scope"]["representative_1_closed"] is False
assert x["held_staged_plan"]["broad_161_launch_authorized"] is False
print(json.dumps({"status":"PASS","result_sha256":hashlib.sha256(p.read_bytes()).hexdigest()},sort_keys=True))
