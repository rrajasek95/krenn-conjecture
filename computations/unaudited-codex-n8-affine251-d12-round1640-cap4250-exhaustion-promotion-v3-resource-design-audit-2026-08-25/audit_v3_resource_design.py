#!/usr/bin/env python3
"""Independent no-run referee of the r1640 v3 resource-only amendment."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
V3=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-v3-resource-design-2026-08-25"
V2=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-design-2026-08-25"
CON=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-design-audit-2026-08-25"
CTL=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4000-exhaustion-control-audit-2026-08-25"
CHAIN=ROOT/"computations/unaudited-codex-n8-affine251-d12-v4-1-round1639-cap4000-audit-2026-08-25"
SRC=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/src/main.rs"
BIN=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/sealed_v4_1/sparse_d12_dual"
WD=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1262-internal-sequential-portfolio-cap1500-2026-08-25/run_with_macos_rss_watchdog_v2_540.py"
FAIL=V2/"candidate_cap4250"
P={"plan":"bbb58965a0341292d5d83ddf674e4eaf712dc9b65f11b945f930994d27d1bc9b","diff":"24fa9ccb38c89d7561d167728c42a14713329f8671e0dbb9fae91b89ed9a4acf","manifest":"1c70a5af5c4e4ef605baf60bc41b74f636a26439055df700581838c09bf2c96b","report":"8c14cbdff07bc87653838f67c9d0e0bdc790d893b722d5056c7fa772789fe081","failure":"924da6890e8f870bf7d9424e37f94ef38149e4bd9e02390f7cf20009bf6c80ae","failure_report":"a2ca34fda70c47916f01e402cf20d6d7dfed9b773ad69c8aff448171a4b72302","failure_manifest":"8152ea7ed72e70bf0d8acf9992260f7b795ff714cd25004c364133dcd166c928","failure_watchdog":"074ea4b09bb11da50737b4dff59e73d5dea17aa1a86e665a9645b0c9c79f691f","launch1":"5e293263047427185c8ed489dfad9bb88ba8c89c0d80033443935851c991ba72","chain":"a99a307f99bd88f8b363ca73bbc3af631a333bab228fbdb43c3e604382150387","chain_manifest":"de3d1a5e390e0545d5f4c5bca7b7f20fa9205056a772bbd8d1ca841e7ae98b0c","contract":"109d7654df0692e6ff906ff1c13ea724fb0133a83d39324b6580710750b5d711","contract_manifest":"c14b6c3d836fcbf5d035aa01b3337164d7666556be9c94dd3b07361c0f291e94","control":"7c86a267c5dc13b1751f02ea98c0745c61ba1de20431d26068bb71d71dcbc618","control_manifest":"d6f4ed8763f430c780563b13de5dd360076fdc2bdec5daa9536bf7e13eb6f890","source":"3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59","binary":"79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","watchdog":"75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997","cp":"ab63c22095dd44d771525af9ba218ee36c9e6f4236a80addbc15692165c531a5","vec":"4d342801fa9e6d25aff95d7b1172f5bff803e8436c01f9237b79e5a42bf6999e"}
def need(x,m):
    if not x:raise AssertionError(m)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def pin(path,d):need(path.is_file() and sha(path)==d,f"pin {path}")
def load(path):return json.loads(path.read_text())
for path,key in [(V3/"PLAN.json","plan"),(V3/"RESOURCE_DIFF.json","diff"),(V3/"MANIFEST.sha256","manifest"),(V3/"REPORT.md","report"),(V2/"FAILURE_EVIDENCE_CANDIDATE_ATTEMPT1.json","failure"),(V2/"FAILURE_REPORT_CANDIDATE_ATTEMPT1.md","failure_report"),(V2/"FAILURE_MANIFEST_CANDIDATE_ATTEMPT1.sha256","failure_manifest"),(FAIL/"watchdog.json","failure_watchdog"),(V2/"LAUNCH_RECORD_CANDIDATE.json","launch1"),(CHAIN/"results_round1639_chain_audit.json","chain"),(CHAIN/"FINAL_MANIFEST.sha256","chain_manifest"),(CON/"results_contract_referee.json","contract"),(CON/"FINAL_MANIFEST.sha256","contract_manifest"),(CTL/"results_control_referee.json","control"),(CTL/"FINAL_MANIFEST.sha256","control_manifest"),(SRC,"source"),(BIN,"binary"),(WD,"watchdog")]:pin(path,P[key])
for line in (V3/"MANIFEST.sha256").read_text().splitlines():d,n=line.split(maxsplit=1);pin(V3/n,d)

# Failure manifest: replay small files, bind the two large unchanged clones by their sealed hashes.
for line in (V2/"FAILURE_MANIFEST_CANDIDATE_ATTEMPT1.sha256").read_text().splitlines():
    d,n=line.split(maxsplit=1)
    if n.endswith("checkpoint.bin"):need(d==P["cp"],"failure cp pin")
    elif n.endswith("vectors.bin"):need(d==P["vec"],"failure cache pin")
    else:pin(V2/n,d)
f=load(V2/"FAILURE_EVIDENCE_CANDIDATE_ATTEMPT1.json");w=load(FAIL/"watchdog.json")
need(f["status"]=="REJECT_HARD_WALL_ZERO_COVERAGE" and not f["accepted_round1640"] and f["accepted_coverage"]==0,"attempt1 coverage")
need(f["attempt"]["result_present"] is False and f["attempt"]["tmp_files"]==0 and f["attempt"]["abort_final_output_absent"],"attempt1 atomic absence")
need(f["unchanged_clone"]["checkpoint_sha256"]==P["cp"] and f["unchanged_clone"]["vector_cache_sha256"]==P["vec"],"attempt1 unchanged")
need(not f["classification"]["mathematical_state_changed"] and not f["classification"]["may_resume_from_attempt"] and f["classification"]["distinct_fresh_clone_required_for_any_authorized_retry"],"attempt1 excluded")
need(w["status"]=="FAIL" and w["breach"]=="WALL_CAP" and w["returncode"]==-15 and w["elapsed_seconds"]==181.729543,"attempt1 wall failure")
need(w["result_sha256"] is None and not w["atomic_outputs_clean"] and w["abort_final_output_absent"],"attempt1 no publication")
need({x.name for x in FAIL.iterdir()}=={"checkpoint.bin","vectors.bin","watchdog.json","stdout.log","stderr.log"},"attempt1 file set")

plan=load(V3/"PLAN.json");diff=load(V3/"RESOURCE_DIFF.json")
need(plan["status"].startswith("HELD_") and not plan["arithmetic_authorized"] and not plan["arithmetic_launched"] and not plan["attempt2_directory_created"],"held/no run")
need(not (V3/"candidate_cap4250_v3_attempt2").exists(),"attempt2 absent")
bind=plan["approved_v2_contract_binding"]
need((bind["contract_referee_sha256"],bind["contract_referee_manifest_sha256"],bind["control_referee_sha256"],bind["control_referee_manifest_sha256"])==(P["contract"],P["contract_manifest"],P["control"],P["control_manifest"]),"v2 approval binding")
fb=plan["failed_attempt1_binding"]
need((fb["failure_evidence_sha256"],fb["failure_report_sha256"],fb["failure_manifest_sha256"],fb["accepted_coverage"])==(P["failure"],P["failure_report"],P["failure_manifest"],0),"failure binding")
need(fb["result_absent"] and fb["tmp_absent"] and fb["checkpoint_and_cache_equal_input"] and not fb["may_resume_from_attempt1"] and fb["attempt1_excluded_from_promotion"],"failure scope")
eng=plan["frozen_engine"]
expected={"source_sha256":P["source"],"binary_sha256":P["binary"],"watchdog_source_sha256":P["watchdog"],"prime":1073741827,"column_cap":4250000,"round_cap":1640,"rss_limit_gib":36,"workers":16,"strategy":"cold","pivot":"rare","elimination":"hierarchical","incremental":"no","portfolio":False}
need(eng==expected,"frozen engine drift")
r=plan["resource_only_amendment"]
need(r=={"base_attempt1_native_wall_seconds":150,"v3_native_wall_seconds":210,"base_attempt1_wrapper_wall_seconds":180,"v3_wrapper_wall_seconds":240,"wrapper_source_changed":False,"source_changed":False,"binary_changed":False,"math_mode_strategy_cap_round_rss_changed":False,"rationale":"Attempt1 was killed at wrapper 180 after 181.729543 seconds; native 210 permits the projected near-200-second round, and wrapper 240 retains 30 seconds for atomic finalization.","generic_wall_relaxation":False,"hard_wrapper_breach_fails":True},"resource amendment fields")
need(diff["changed"]=={"solver_native_wall_seconds":{"before":150,"after":210},"watchdog_hard_wall_seconds":{"before":180,"after":240}},"diff changed set")
unchanged=dict(expected);unchanged.update(input_checkpoint_sha256=P["cp"],input_vector_cache_sha256=P["vec"])
need(diff["unchanged"]==unchanged and diff["attempt1_directory_forbidden_as_input"],"diff unchanged set")
a=plan["attempt2"]
need(a["fresh_distinct_apfs_clone_from_exact_audited_r1639"] and a["must_not_copy_or_resume_attempt1"],"fresh clone")
need((a["native_wall_seconds"],a["wrapper_wall_seconds"],a["required_rounds_completed"],a["required_exact_round_records"])==(210,240,1640,[1640]),"attempt2 resource/round")
need(a["required_round1641_absent"] and a["required_tmp_absent"] and a["required_watchdog_pass_atomic_no_breach"] and a["required_inherited_record_count"]==3968369 and a["required_inherited_records_byte_identical_same_canonical_order"] and a["required_checkpoint_strict_descendant_of_input"] and a["required_full_cache_replay_target"]==1 and a["required_full_cache_replay_failures"]==0 and a["required_independent_postrun_audit"],"postrun guards")

# Reconstruct the exact proposed solver command from failed attempt1: one native literal changes.
old=w["command"];new=list(old);new[new.index("--wall-seconds")+1]="210"
changed=[(i,x,y) for i,(x,y) in enumerate(zip(old,new)) if x!=y]
need(changed==[(new.index("--wall-seconds")+1,"150","210")],"solver command diff")
need(old[old.index("--column-cap")+1]==new[new.index("--column-cap")+1]=="4250000" and old[old.index("--round-cap")+1]==new[new.index("--round-cap")+1]=="1640","cap/round invariant")
need("args.wall_seconds > 540" in WD.read_text(),"watchdog accepts 240")
need(plan["storage"]["minimum_preclone_free_kib"]==88080384 and plan["storage"]["measure_immediately_before_fresh_clone"] and plan["storage"]["design_time_measurement_does_not_authorize_launch"],"storage gate")

out={"schema":"KRENN_AFFINE251_D12_R1640_CAP4250_V3_RESOURCE_DESIGN_REFEREE_V1","status":"PASS_PRELAUNCH_RESOURCE_ONLY_AMENDMENT_APPROVED_HELD","design":{"plan_sha256":P["plan"],"resource_diff_sha256":P["diff"],"manifest_sha256":P["manifest"]},"approved_v2":{"contract_referee_sha256":P["contract"],"contract_manifest_sha256":P["contract_manifest"],"control_referee_sha256":P["control"],"control_manifest_sha256":P["control_manifest"]},"failed_attempt1":{"failure_evidence_sha256":P["failure"],"failure_manifest_sha256":P["failure_manifest"],"watchdog_sha256":P["failure_watchdog"],"classification":"REJECT_HARD_WALL_ZERO_COVERAGE","accepted_coverage":0,"checkpoint_cache_equal_audited_input":True,"result_tmp_absent":True,"may_resume":False,"evidence_only":True},"amendment":{"exact_changes":["solver native wall 150 -> 210","hard watchdog wall 180 -> 240"],"source_binary_watchdog_math_cap_round_rss_mode_unchanged":True,"generic_wall_relaxation":False,"hard_wrapper_breach_rejects":True},"attempt2":{"directory_absent":True,"fresh_clone_from_audited_r1639_required":True,"attempt1_reuse_forbidden":True,"postrun_guards":True},"prelaunch":{"resource_contract_approved":True,"arithmetic_authorized_by_this_referee":False,"remaining_gates":["manager clearance","immediate >=88080384-KiB preclone measurement","fresh-clone provenance and exact command-diff launch record"]},"scope":"Resource-only prelaunch approval; no arithmetic, r1640 state, r1641, D12 certificate, or conjecture claim."}
tmp=HERE/"results_v3_resource_referee.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_v3_resource_referee.json")
print("PASS v3 resource-only amendment; arithmetic remains held")
