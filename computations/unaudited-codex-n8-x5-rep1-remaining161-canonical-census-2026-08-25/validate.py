#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here=Path(__file__).resolve().parent
path=here/"results_canonical_census.json"; x=json.loads(path.read_text())
gate=json.loads((here/"HELD_RESOURCE_GATE.json").read_text())
assert x["schema"]=="KRENN_X5_REP1_REMAINING161_CANONICAL_CENSUS_V1"
assert x["status"]=="PASS_EXACT_ENUMERATION_NO_IDEALS"
assert x["census"]=={"raw_refined_charts":972,"canonical_polynomial_groups":162,"closed_groups":1,"remaining_groups":161,"raw_members_per_group":6,"distinct_canonical_source_hashes":162}
assert x["canonicalization_contract"]["vertex_automorphism_count"]==1
assert x["source_size"]["remaining_161_total_bytes"]==286969760
assert x["scope"]=={"ideal_launches":0,"additional_charts_closed":0,"representative_closed":False}
assert all(x["hostile_tests"].values())
selected=x["enumeration"]["records"][gate["selected_group_id"]]
assert selected["canonical_chart"]==gate["canonical_chart"]
assert selected["exact_Q_source_sha256"]==gate["expected_exact_Q_source_sha256"]
assert selected["exact_Q_source_bytes"]==gate["expected_exact_Q_source_bytes"]==x["source_size"]["maximum_bytes"]
assert gate["status"]=="HELD_PENDING_INDEPENDENT_REFEREE_AND_EXPLICIT_CLEARANCE"
print(json.dumps({"status":"PASS_HELD","result_sha256":hashlib.sha256(path.read_bytes()).hexdigest()},sort_keys=True))
