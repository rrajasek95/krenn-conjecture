#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();x=json.loads((H/"results_referee.json").read_text())
assert x["status"]=="PASS_ALL_TEN_EXACT_Q_UNIT_IDEALS" and x["groups_closed"]==list(range(1,11)) and x["new_groups_closed"]==10
assert x["batch_result_sha256"]=="ee3d1d0e77c8aa2a5a07f7187a05e785f57ca2c8f5a753ccf40af3c8dc99d86f"
assert x["strict_order"] and not x["parallel"] and not x["relaunch"] and not x["skipped"] and not x["groups_beyond_10_launched"]
assert not x["rep1_representative_closed"] and not x["seven_block_family_closed"] and not x["conjecture_closed"]
print(json.dumps({"status":"PASS_GROUPS_1_TO_10_ONLY","audit_sha256":h(H/"results_referee.json")},sort_keys=True))
