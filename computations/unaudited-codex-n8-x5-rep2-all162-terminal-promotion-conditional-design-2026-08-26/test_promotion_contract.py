#!/usr/bin/env python3
"""Exact-ledger hostile tests; no solver."""
import copy,hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent
R=json.loads((H/"results_terminal_promotion_design.json").read_text()); F=json.loads((H/"future_dependencies.json").read_text())
def validate(r,f):
 assert r["schema"]=="KRENN_X5_REP2_ALL162_TERMINAL_PROMOTION_CONDITIONAL_DESIGN_V1"
 assert r["status"]=="HELD_PROMOTION_FOUR_FUTURE_PASS_SEALS_ABSENT"
 assert r["authoritative_contraction"]["raw_charts"]==972 and r["authoritative_contraction"]["canonical_s3_charts"]==162
 assert r["authoritative_contraction"]["y_groups"]==r["authoritative_contraction"]["z_groups"]==81
 assert r["rank_zero_structural_branch"]["closed_rank_scope"]==[0]
 assert r["rank_zero_structural_branch"]["nonzero_rank_scope_not_claimed"]==[1,2,3]
 assert r["sealed_group0"]["group_id"]==0 and r["sealed_group0"]["independent_q_seals"]==2
 expected=[[0],list(range(1,26)),list(range(26,76)),list(range(76,126)),list(range(126,162))]
 assert [x["group_ids"] for x in r["closure_shards"]]==expected
 flat=[v for s in expected for v in s]; assert len(flat)==len(set(flat))==162 and sorted(flat)==list(range(162))
 tr=r["raw_s3_transport"]; assert [x["group_id"] for x in tr]==list(range(162))
 raw=[tuple(v) for x in tr for v in x["raw_s3_members"]]
 assert all(x["raw_member_count"]==len(x["raw_s3_members"])==6 for x in tr) and len(raw)==len(set(raw))==972
 assert sum(x["family"]=="y" for x in tr)==sum(x["family"]=="z" for x in tr)==81
 assert r["scope"]["representative"]=="rep2 only" and r["scope"]["cross_representative_transport"] is False and r["scope"]["full_conjecture"] is False
 assert f["status"]=="UNSATISFIED_FOUR_NULL_HASH_PAIRS" and f["satisfied"] is False
 assert [x["group_ids"] for x in f["dependencies"]]==expected[1:]
 assert all(x["manifest_sha256"] is x["result_sha256"] is None for x in f["dependencies"])
validate(R,F); out={}
def reject(name,fn):
 r,f=copy.deepcopy(R),copy.deepcopy(F); fn(r,f)
 try: validate(r,f)
 except (AssertionError,KeyError,TypeError): out[name]=True
 else: out[name]=False
reject("missing_group",lambda r,f:r["closure_shards"][2]["group_ids"].pop())
reject("duplicate_group",lambda r,f:r["closure_shards"][3]["group_ids"].append(125))
reject("extra_group",lambda r,f:r["closure_shards"][4]["group_ids"].append(162))
reject("missing_raw_member",lambda r,f:r["raw_s3_transport"][0]["raw_s3_members"].pop())
reject("duplicate_raw_member",lambda r,f:r["raw_s3_transport"][1]["raw_s3_members"].__setitem__(0,r["raw_s3_transport"][0]["raw_s3_members"][0]))
reject("drop_y_group",lambda r,f:r["raw_s3_transport"][0].__setitem__("family","z"))
reject("rank_zero_overclaim",lambda r,f:r["rank_zero_structural_branch"].__setitem__("nonzero_rank_scope_not_claimed",[]))
reject("group0_unsealed",lambda r,f:r["sealed_group0"].__setitem__("independent_q_seals",1))
reject("cross_rep",lambda r,f:r["scope"].__setitem__("cross_representative_transport",True))
reject("full_conjecture",lambda r,f:r["scope"].__setitem__("full_conjecture",True))
reject("null_treated_satisfied",lambda r,f:f.__setitem__("satisfied",True))
reject("future_hash_injected",lambda r,f:f["dependencies"][0].__setitem__("manifest_sha256","0"*64))
reject("wrong_v2_shard",lambda r,f:f["dependencies"][2]["group_ids"].pop())
assert len(out)==13 and all(out.values())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result={"schema":"KRENN_X5_REP2_ALL162_PROMOTION_HOSTILES_V1","status":"PASS_EXACT_LEDGER_AND_13_HOSTILES","design_sha256":sha(H/"results_terminal_promotion_design.json"),"future_dependencies_sha256":sha(H/"future_dependencies.json"),"hostile_tests":out,"hostile_count":13,"solver_runs":0}
t=H/"results_hostile_tests.json.tmp"; t.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); os.replace(t,H/"results_hostile_tests.json")
print(json.dumps({"status":result["status"],"hostiles":13},sort_keys=True))
