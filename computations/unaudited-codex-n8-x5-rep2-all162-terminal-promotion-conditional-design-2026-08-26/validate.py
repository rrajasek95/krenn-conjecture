#!/usr/bin/env python3
"""Fail-closed validation of the rep2 conditional terminal design."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda n:json.loads((H/n).read_text())
r,f,h,s=map(load,["results_terminal_promotion_design.json","future_dependencies.json","results_hostile_tests.json","terminal_promotion_acceptance.schema.json"])
assert r["status"]=="HELD_PROMOTION_FOUR_FUTURE_PASS_SEALS_ABSENT" and r["scope"]["solver_runs"]==0
assert r["scope"]["representative"]=="rep2 only" and r["scope"]["cross_representative_transport"] is False and r["scope"]["full_conjecture"] is False
assert r["rank_zero_structural_branch"]["closed_rank_scope"]==[0] and r["rank_zero_structural_branch"]["nonzero_rank_scope_not_claimed"]==[1,2,3]
expected=[[0],list(range(1,26)),list(range(26,76)),list(range(76,126)),list(range(126,162))]
assert [x["group_ids"] for x in r["closure_shards"]]==expected
assert r["prospective_union_proof"]=={"group_count":162,"union":list(range(162)),"duplicates":[],"missing":[],"extra":[],"all_four_future_batches_required":True}
raw=[tuple(v) for x in r["raw_s3_transport"] for v in x["raw_s3_members"]]; assert len(raw)==len(set(raw))==972
assert f["satisfied"] is False and all(x["manifest_sha256"] is x["result_sha256"] is None for x in f["dependencies"])
for x in f["dependencies"]: assert not (ROOT/x["manifest_path"]).exists() and not (ROOT/x["result_path"]).exists()
assert h["status"]=="PASS_EXACT_LEDGER_AND_13_HOSTILES" and h["hostile_count"]==13 and all(h["hostile_tests"].values())
assert h["design_sha256"]==sha(H/"results_terminal_promotion_design.json") and h["future_dependencies_sha256"]==sha(H/"future_dependencies.json")
assert s["additionalProperties"] is False and set(s["required"])==set(s["properties"])
assert s["properties"]["closed_group_ids"]["const"]==list(range(162)) and s["properties"]["representative"]["const"]=="rep2"
for rel,digest in r["pins"].items(): assert (ROOT/rel).is_file() and sha(ROOT/rel)==digest
for forbidden in ("terminal_promotion_acceptance.json","results_terminal_promotion.json","future_terminal_seals.json"): assert not (H/forbidden).exists()
assert not list(H.glob("*.tmp")) and not list(H.glob("*.sing")) and not list(H.glob("*.log"))
manifest=H/"MANIFEST.sha256"; checked=0
if manifest.exists():
 for line in manifest.read_text().splitlines():
  digest,rel=line.split("  ",1); p=(H/rel).resolve(); assert p.is_file() and sha(p)==digest; checked+=1
print(json.dumps({"status":"PASS_HELD_ZERO_RUN_FOUR_FUTURE_SEALS_REQUIRED","canonical_groups":162,"raw_s3_members":972,"current_exact_q_closed":[0],"future_exact_q_required":list(range(1,162)),"manifest_lines_checked":checked,"solver_runs":0},sort_keys=True))
