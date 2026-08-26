#!/usr/bin/env python3
"""Independent, no-run referee of the r1640 cap-exhaustion proof contract."""
import hashlib, json, os, re
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
DESIGN=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-design-2026-08-25"
SRC=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/src/main.rs"
CHAIN=ROOT/"computations/unaudited-codex-n8-affine251-d12-v4-1-round1639-cap4000-audit-2026-08-25"
P={
"design_manifest":"1a111b26b76eb3d931143f9d9d794c6b2c650a096f3af008be6740cd7dc4a9da",
"plan":"9b52095413c633e31f918cdf349ad14af8c8cc4f59136a5cea82066e42413159",
"checker":"b029ba545621edd5794a3538d5cd9e4dba2848f86174a5a6f887e10860020c31",
"static":"1cab0b83362ab8a984f4ee81c480c79d04bf80c035c53e60ce0f425e29fe79e2",
"report":"a818d1e857cd3ada4fd3e18ea9c2f1a93631f3a45345ec94488dba00b503cb2d",
"source":"3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59",
"chain_audit":"a99a307f99bd88f8b363ca73bbc3af631a333bab228fbdb43c3e604382150387",
"chain_replay":"4996c85de7aedf853ba6428e948b69e88a5a07d170614ce9fea5f98714d3c5e5",
"chain_manifest":"de3d1a5e390e0545d5f4c5bca7b7f20fa9205056a772bbd8d1ca841e7ae98b0c",
"checkpoint":"ab63c22095dd44d771525af9ba218ee36c9e6f4236a80addbc15692165c531a5",
"cache":"4d342801fa9e6d25aff95d7b1172f5bff803e8436c01f9237b79e5a42bf6999e"}

def need(x,m):
    if not x: raise AssertionError(m)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def pin(path,digest): need(path.is_file() and sha(path)==digest,f"pin {path}")
def load(path): return json.loads(path.read_text())

for path,key in [(DESIGN/"MANIFEST.sha256","design_manifest"),(DESIGN/"PLAN.json","plan"),
 (DESIGN/"audit_column_cap_source.py","checker"),(DESIGN/"results_static_column_cap_audit.json","static"),
 (DESIGN/"REPORT.md","report"),(SRC,"source"),(CHAIN/"results_round1639_chain_audit.json","chain_audit"),
 (CHAIN/"results_round1639_single_pass_replay.json","chain_replay"),(CHAIN/"FINAL_MANIFEST.sha256","chain_manifest")]: pin(path,P[key])

# Replay producer design manifest independently (small files only).
for line in (DESIGN/"MANIFEST.sha256").read_text().splitlines():
    digest,name=line.split(maxsplit=1); pin(DESIGN/name,digest)

text=SRC.read_text()
expected=["column_cap: usize,","let column_cap = values","|| column_cap < 17","column_cap,",
 'writeln!(out, "  \\\"column_cap\\\": {},", config.column_cap).unwrap();',
 "if columns.len() + new_columns.len() > config.column_cap {"]
occ=[line.strip() for line in text.splitlines() if re.search(r"\bcolumn_cap\b",line)]
need(occ==expected and text.count("config.column_cap")==2,"column_cap occurrence census")

# Independently inspect the complete capacity branch and its ordered context.
census="let mut new_columns: Vec<_> = incident.difference(&columns).copied().collect();"
sort="new_columns.sort_unstable();"; guard="if columns.len() + new_columns.len() > config.column_cap {"
arith="let values =\n            parallel_invariant_columns"
p={k:text.index(v) for k,v in [("census",census),("sort",sort),("guard",guard),("arith",arith)]}
need(p["census"]<p["sort"]<p["guard"]<p["arith"],"guard ordering")
branch=text[p["guard"]:p["arith"]]
for token in ["sparse_write_checkpoint(\n                &config.checkpoint,\n                config.prime,\n                completed_rounds,\n                &columns,\n                &candidate,",
 "sparse_maybe_write_vectors(","&vectors,","sparse_write_result(", 'Some("COLUMN_CAP")',"columns.len(),","candidate.len(),","return;"]:
    need(token in branch,f"capacity branch missing {token}")
for token in ["parallel_invariant_columns(","columns.insert(","columns.extend(","vectors.insert(","candidate =","rank_equations_sharded("]:
    need(token not in branch,f"capacity branch mutation {token}")
need("columns.extend(new_columns.iter().copied());" in text[p["arith"]:],"whole-set admission absent")

static=load(DESIGN/"results_static_column_cap_audit.json")
need(static["status"]=="PASS_COLUMN_CAP_ONLY_PRE_ARITHMETIC_CAPACITY_GUARD" and static["source_sha256"]==P["source"],"static result")
need(all(static["proof"].values()) and len(static["selftests"])==5,"static theorem/selftests")

plan=load(DESIGN/"PLAN.json")
need(plan["status"].startswith("HELD_") and not plan["arithmetic_launched"] and not plan["large_endpoint_read_performed"],"held/no run")
need(plan["proof_contract"]=="CAP_EXHAUSTION_AND_EXACT_DESCENDANT_PROMOTION_NOT_BYTE_EQUIVALENCE","proof contract")
i=plan["input"]
need((i["round"],i["columns"],i["dual_support"],i["checkpoint_sha256"],i["vector_cache_sha256"])==(1639,3968369,32704,P["checkpoint"],P["cache"]),"input state")
need(i["independent_audit_sha256"] is None and i["independent_replay_sha256"] is None and i["independent_manifest_sha256"] is None,"expected pre-referee null binding")
c=plan["frozen_contract"]
need((c["source_sha256"],c["binary_sha256"],c["watchdog_sha256"],c["prime"],c["round_cap"])==(P["source"],"79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997",1073741827,1640),"frozen contract")
need((c["native_wall_seconds"],c["wrapper_wall_seconds"],c["rss_limit_gib"],c["workers"],c["strategy"],c["pivot"],c["elimination"],c["incremental"],c["portfolio"])==(150,180,36,16,"cold","rare","hierarchical","no",False),"frozen mode")

control,candidate=plan["sequential_runs"]
need(control["column_cap"]==4000000 and control["required_reason"]=="COLUMN_CAP" and control["required_rounds_completed"]==1639,"control exhaustion")
need(control["required_checkpoint_byte_equal_input"] and control["required_vector_cache_byte_equal_input"] and control["required_round1640_record_absent"] and control["required_tmp_absent"],"control unchanged")
need(candidate["column_cap"]==4250000 and candidate["required_reason"]=="ROUND_CAP" and candidate["required_rounds_completed"]==candidate["required_single_round_record"]==1640,"candidate round")
need(candidate["required_inherited_record_count"]==3968369 and candidate["required_inherited_records_byte_identical_and_same_order"],"candidate inheritance")
need(candidate["required_full_cache_replay_target"]==1 and candidate["required_full_cache_replay_failures"]==0,"candidate replay")
need(plan["command_identity"]["sole_command_argument_diff"]=="--column-cap 4000000 vs 4250000" and plan["command_identity"]["hostile_any_extra_diff_rejected"],"command identity")
need(plan["storage"]["minimum_prelaunch_free_kib"]==88080384 and plan["storage"]["fail_closed_below_floor"],"storage gate")
need(not plan["post_promotion_geometry_only"]["arithmetic_authorized"] and "launch round1641 from this design" in plan["forbidden"],"no continuation")

# The logical implication is sound only with these post-run observations.
required_postrun=[
"commands normalized equal except literal column cap and output directories",
"control returns COLUMN_CAP at r1639, has no r1640 record/tmp, and cp/cache hash exactly to audited input",
"candidate returns ROUND_CAP with exactly one r1640 record and clean atomic watchdog",
"candidate checkpoint is a strict ordered descendant of r1639 with origin census final-minus-3968369",
"all 3968369 inherited vectors are byte-identical in canonical order",
"candidate checkpoint target is normalized to 1 and every final cached column pairs to zero",
"independent result/manifest replay PASS and no r1641 launch"]

out={"schema":"KRENN_AFFINE251_D12_R1640_CAP4250_EXHAUSTION_CONTRACT_REFEREE_V1",
"status":"PASS_PRELAUNCH_PROOF_CONTRACT_APPROVED_HELD",
"design":{"plan_sha256":P["plan"],"checker_sha256":P["checker"],"static_result_sha256":P["static"],"report_sha256":P["report"],"manifest_sha256":P["design_manifest"]},
"accepted_input_binding":{"round":1639,"columns":3968369,"support":32704,"audit_sha256":P["chain_audit"],"replay_sha256":P["chain_replay"],"manifest_sha256":P["chain_manifest"],"checkpoint_sha256":P["checkpoint"],"vector_cache_sha256":P["cache"]},
"source_theorem":{"source_sha256":P["source"],"column_cap_occurrences":6,"config_reads":2,"enumeration_and_sort_before_guard":True,"guard_before_column_arithmetic":True,"failure_branch_writes_unchanged_columns_candidate_and_returns":True,"whole_new_set_admitted_together":True,"cap_has_no_arithmetic_scoring_ranking_elimination_backsolve_or_verification_read":True},
"proof_contract":{"sound":True,"kind":"cap-exhaustion plus exact deterministic descendant; explicitly not byte equivalence","required_postrun_evidence":required_postrun,"control_candidate_byte_equality_required":False,"inherited_prefix_byte_equality_required":True},
"prelaunch":{"proof_contract_approved":True,"arithmetic_authorized_by_this_referee":False,"remaining_fail_closed_gates":["bind this referee manifest because producer PLAN intentionally has null independent-input fields","rehash/measure the declared 88080384-KiB storage floor immediately before each lane","manager clearance","candidate forbidden unless every control guard passes"]},
"scope":"Approval of the held r1640 two-lane proof contract only; no run, r1640 state, D12 certificate, r1641, or conjecture claim."}
tmp=HERE/"results_contract_referee.json.tmp"; tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); os.replace(tmp,HERE/"results_contract_referee.json")
print("PASS held cap-exhaustion proof contract; no arithmetic authorized")
