#!/usr/bin/env python3
"""Freeze the future terminal-promotion acceptance surface."""
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
props={
 "schema":{"const":"KRENN_X5_REP2_ALL162_TERMINAL_PROMOTION_ACCEPTANCE_V1"},
 "status":{"const":"PASS_PROMOTE_REP2_ALL_162_CANONICAL_GROUPS_ONLY"},
 "held_design_manifest_sha256":{"type":"string","pattern":"^[0-9a-f]{64}$"},
 "promotion_design_sha256":{"const":sha(H/"results_terminal_promotion_design.json")},
 "future_dependencies_sha256":{"const":sha(H/"future_dependencies.json")},
}
for label in ("groups1_25","groups26_75","groups76_125_v2","groups126_161"):
 props[label+"_manifest_sha256"]={"type":"string","pattern":"^[0-9a-f]{64}$"}; props[label+"_result_sha256"]={"type":"string","pattern":"^[0-9a-f]{64}$"}
props.update({"closed_group_ids":{"const":list(range(162))},"raw_charts_closed":{"const":972},"canonical_groups_closed":{"const":162},"y_groups_closed":{"const":81},"z_groups_closed":{"const":81},"rank_zero_branch_closed":{"const":True},"representative":{"const":"rep2"},"cross_representative_transport":{"const":False},"full_conjecture":{"const":False}})
s={"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","additionalProperties":False,"properties":props,"required":list(props)}
t=H/"terminal_promotion_acceptance.schema.json.tmp"; t.write_text(json.dumps(s,indent=2,sort_keys=True)+"\n"); os.replace(t,H/"terminal_promotion_acceptance.schema.json")
print(json.dumps({"status":"SCHEMA_FROZEN","properties":len(props)},sort_keys=True))
