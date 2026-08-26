#!/usr/bin/env python3
"""Fail-closed small-file referee for the independently replayed r1627->1639 chain."""
import copy, hashlib, json, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1627_cap4000_to1639"
CAP = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1627-direct-cap4000-gate-audit-2026-08-25"
CAP_P = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1627-direct-cap4000-gate-2026-08-25"
PRE = ROOT / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1603-stage01-edge-audit-2026-08-25"
CENTRAL = ROOT / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1463-cap2000-audit-2026-08-25/COMPACTION_EXECUTION.md"
OLD_WD = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1262-portfolio-cap1500-gate-2026-08-25/run_with_macos_rss_watchdog_v2_155.py"
NEW_WD = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1262-internal-sequential-portfolio-cap1500-2026-08-25/run_with_macos_rss_watchdog_v2_540.py"

P = {
"ia":"c43b18138cbca585e5256ee5809e94ed16d96eefa3771b695cd93850c53d039b",
"im":"20441719604745ddcdb7c12a75111bb27aa3ee4477d12c4b135c76fc5069530f",
"icp":"40a76f726f40fb022909f219b6ace5d8ee5f04fb5847cb1e37a3cea2829e308e",
"iv":"4ae60b262d5bdcea3488ed0bb194e95d338bb962beb172cec33e9ddc76de8eeb",
"icomp":"c4ed752ab191f5e41eb5259d0f13c7ddbfdaf8783c0c4f245769c984e7e0ed71",
"ledger":"7c56ae5e1dabd3d50ad1889dc8f0e2a64e11c2570e600fb6fe9b635e3fa4b260",
"report":"eb5480229479005145949c176cd7ce212a43f6fe6488edf334242e5912b5e596",
"manifest":"8d95f913df573c65596916dddf6c691157fd4dcae10a581c5721144627c9c56c",
"plan":"15f4d1217e0e66b364347673bcbae7aa3109b0e25461e36587631a40bca08483",
"orig":"04d91e1c7880a82baf0ede84b287b4cab1eb2aae228aa9f72c39c328cbf3bd51",
"a32":"3d0c6faa4d2fb21239a3a0aa647aae4c8e7a1078cc7aa6f9c75ac435b8d7827d",
"a35":"6005fff1b5a1926bbee092e4d3e18e3dbfbb09a47ef875442db862dda74a7433",
"a36":"fd535a1f686524a077c969260548c3b19b2bcfa72b1e58928b3adaf4050e0153",
"a38":"dad3d23eae1ade3da7a62c93cd2ee22ef588e0dcf41a64ab5949199ca2ebc53d",
"storage":"65c682d57b3d4a83b35d7c4e37d0cf952a1e1e07e2623a72357600cc894f8e6b",
"central":"56d57f28b7196695a394216648090cca3d1a57f60a0f05147499175ff405bf09",
"src":"3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59",
"bin":"79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048",
"owd":"48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522",
"nwd":"75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997",
"pre":"a3d7b91a40ac51a74af8bbf747971d48e8dbc64bdc986584de2bd793094bfb7a",
"prem":"3820aae7c7da84cfbb60e99c5363baa2cfe611d376637468208f4bc3d1289466",
"fres":"fa13a36deac596f3b01cb1781208f6e4459c5cd1ade1ceb071f64f30cf60423b",
"fwd":"1841fed59e55911fdca24c5b4b6d115a412b611a01dfc6b5e23163cd1039fc6c",
"fcp":"ab63c22095dd44d771525af9ba218ee36c9e6f4236a80addbc15692165c531a5",
"fv":"4d342801fa9e6d25aff95d7b1172f5bff803e8436c01f9237b79e5a42bf6999e"}

def need(x, m):
    if not x: raise AssertionError(m)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def pin(path, value): need(path.is_file() and sha(path)==value, f"pin {path}")
def load(path): return json.loads(path.read_text())

small=[
(CAP/"results_round1627_direct_cap4000_audit.json",P["ia"]),(CAP/"FINAL_MANIFEST.sha256",P["im"]),
(CAP_P/"POST_AUDIT_COMPACTION.md",P["icomp"]),(PROD/"PRODUCER_LEDGER.json",P["ledger"]),
(PROD/"REPORT.md",P["report"]),(PROD/"MANIFEST.sha256",P["manifest"]),(PROD/"PLAN.json",P["plan"]),
(HERE/"ORIGINAL_PLAN_SNAPSHOT.json",P["orig"]),(PROD/"PLAN_AMENDMENT_R1632.md",P["a32"]),
(PROD/"PLAN_AMENDMENT_R1635.md",P["a35"]),(PROD/"PLAN_AMENDMENT_R1636.md",P["a36"]),
(PROD/"PLAN_AMENDMENT_AFTER_R1638.json",P["a38"]),(PROD/"STORAGE_AUDIT_R1636.md",P["storage"]),
(CENTRAL,P["central"]),(OLD_WD,P["owd"]),(NEW_WD,P["nwd"]),
(PRE/"results_stage01_edge_audit.json",P["pre"]),(PRE/"FINAL_MANIFEST.sha256",P["prem"])]
for path,value in small: pin(path,value)

# v2_540 differs only in the accepted upper bound and matching error text.
old,new=OLD_WD.read_text().splitlines(),NEW_WD.read_text().splitlines()
diff=[(a,b) for a,b in zip(old,new) if a!=b]
need(len(old)==len(new) and diff==[
("    if not command or args.rss_gib != 36 or args.wall_seconds > 155:","    if not command or args.rss_gib != 36 or args.wall_seconds > 540:"),
('        raise SystemExit("watchdog accepts only the sealed 36-GiB, <=155-second gate")','        raise SystemExit("watchdog accepts only the sealed 36-GiB, <=540-second gate")')],"watchdog diff")

# All final PLAN changes reconstruct exactly to the frozen original.
plan,orig=load(PROD/"PLAN.json"),load(HERE/"ORIGINAL_PLAN_SNAPSHOT.json")
rec=copy.deepcopy(plan)
for k in ("amendment_after_round1632","amendment_after_round1635","amendment_after_round1636","amendment_after_round1638"): rec.pop(k)
rec["contract"].update(watchdog_sha256=P["owd"],native_wall_seconds=120,wrapper_wall_seconds=150)
rec["stages"][-1]["block"]="D"; rec["guards"]["maximum_conservative_new_columns_per_round"]=25000
rec["guards"].pop("maximum_conservative_new_columns_scope")
need(rec==orig,"amendment reconstruction")
need(plan["amendment_after_round1632"]["remaining_rounds"]*40000==280000<331941,"r1632 guard")
need(plan["amendment_after_round1636"]["remaining_rounds"]*50000==150000<201729,"r1636 guard")
need(plan["amendment_after_round1638"]["remaining_rounds"]*75000==75000<98089,"r1638 guard")
need(plan["amendment_after_round1635"]["accepted_exception"]["exact_target_round_only"],"r1635 scope")
need(not plan["amendment_after_round1635"]["accepted_exception"]["generic_semantic_relaxation"],"status relaxation")

L=load(PROD/"PRODUCER_LEDGER.json")
need(L["status"]=="PASS_PRODUCER_EXACT_CHAIN_HELD_FOR_INDEPENDENT_AUDIT","ledger status")
need((L["input"]["cap_audit_sha256"],L["input"]["cap_manifest_sha256"],L["input"]["checkpoint_sha256"],L["input"]["vector_cache_sha256"])==(P["ia"],P["im"],P["icp"],P["iv"]),"input pins")
cols=[3568617,3592570,3615418,3638697,3668059,3701722,3726609,3756136,3798271,3845743,3901911,3968369]
supp=[8614,8287,8388,10208,11507,8937,10435,14074,15825,18425,21067,32704]
newc=[21455,23953,22848,23279,29362,33663,24887,29527,42135,47472,56168,66458]
names=[f"stage{i:02d}_cap{1627+i}" for i in range(1,13)]
coop={"stage06_cap1633","stage07_cap1634","stage11_cap1638","stage12_cap1639"}; wall={"stage08_cap1635"}
need(len(L["stages"])==12,"stage count"); parent=3547162; stages=[]
for i,(name,decl) in enumerate(zip(names,L["stages"]),1):
    d=PROD/name; rp,wp=d/"result.json",d/"watchdog.json"; pin(rp,decl["result_sha256"]); pin(wp,decl["watchdog_sha256"])
    r,w=load(rp),load(wp); rnd=1627+i; nl,wl=((120,150) if i<=8 else (150,180))
    need((decl["round"],r["rounds_completed"],r["rounds"][0]["round"])==(rnd,rnd,rnd) and len(r["rounds"])==1,"round")
    need((r["column_orbits_exposed"],decl["columns"],r["dual_support"],decl["support"])==(cols[i-1],cols[i-1],supp[i-1],supp[i-1]),"census")
    need((r["cached_vectors_loaded"],decl["cached"],r["rounds"][0]["new_columns"],decl["new_columns"])==(parent,parent,newc[i-1],newc[i-1]),"edge census")
    need((r["prime"],r["column_cap"],r["workers"],r["strategy"],r["pivot_mode"],r["elimination_kernel"],r["incremental_basis"])==(1073741827,4000000,16,"cold","rare","hierarchical",False),"config")
    need(r["global_annihilation"] is None and r["target_pairing"] is None,"nonterminal")
    expected=("INCOMPLETE_RESOURCE_GATE","WALL_CAP") if name in wall else ("INCOMPLETE_SEARCH_CAP","ROUND_CAP")
    need((r["status"],r["incomplete_reason"])==expected,"status")
    need(r["wall_limit_seconds"]==nl and w["wall_limit_seconds"]==wl,"wall contract")
    need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],"watchdog")
    need(w["peak_rss_kib"]<37748736 and w["source_sha256"]==P["src"] and w["binary_sha256"]==P["bin"],"resource/provenance")
    need(w["watchdog_sha256"]==(P["owd"] if i<=8 else P["nwd"]),"watchdog pin")
    need(w["command"][w["command"].index("--round-cap")+1]==str(rnd),"command round")
    need((r["elapsed_seconds"]>nl)==(name in coop or name in wall) and w["elapsed_seconds"]<wl,"exception set")
    need(not any(d.glob("*.tmp")),"temporary output")
    stages.append({"stage":name,"round":rnd,"columns":cols[i-1],"support":supp[i-1],"new_columns":newc[i-1],"result_sha256":decl["result_sha256"],"watchdog_sha256":decl["watchdog_sha256"],"classification":decl["classification"]})
    parent=cols[i-1]
need(set(x.name for x in PROD.glob("stage*_cap*"))==set(names),"accepted stage set")
need(not any(PROD.rglob("*1640*")),"r1640 artifact")
ref=PROD/"stage09_refused_wrapper155_attempt"
need({x.name for x in ref.iterdir()}=={"checkpoint.bin","vectors.bin"},"refused zero coverage")
need((ref/"checkpoint.bin").stat().st_size==(PROD/"stage08_cap1635/checkpoint.bin").stat().st_size and (ref/"vectors.bin").stat().st_size==(PROD/"stage08_cap1635/vectors.bin").stat().st_size,"refused clone")

B=L["resource_blocks"]
sums=[sum(x["watchdog_seconds"] for x in L["stages"][a:b]) for a,b in [(0,3),(3,6),(6,9),(9,11),(11,12)]]
declared=[B[k] for k in ("A_1628_1630_watchdog_seconds","B_1631_1633_watchdog_seconds","C_1634_1636_watchdog_seconds","D_1637_1638_watchdog_seconds","E_1639_watchdog_seconds")]
need(all(abs(a-b)<1e-6 and a<540 for a,b in zip(sums,declared)),"resource blocks")
need(B["all_below_540"] and B["maximum_peak_rss_kib"]==max(x["peak_rss_kib"] for x in L["stages"])<B["rss_cap_kib"]==37748736,"RSS")

R=load(HERE/"results_round1639_single_pass_replay.json")
need(R["status"]=="PASS_ALL_DESCENDANT_EDGES_AND_ALL_COLUMNS" and R["rounds"]==list(range(1627,1640)),"replay")
need(R["columns"]==[3547162]+cols and R["supports"]==[7888]+supp and R["new_records_by_origin"]==[3547162]+newc,"replay census")
need(R["checkpoint_descendant_edges"]==R["cache_descendant_edges"]==12 and R["inherited_vectors_byte_identical"],"replay edges")
need(R["terms_replayed"]==403999306 and R["target_terms"]==2 and R["verification_failures"]==0,"all-column replay")
hashes=dict(line.split(maxsplit=1)[::-1] for line in (HERE/"FINAL_ENDPOINT_HASHES.sha256").read_text().splitlines())
need(hashes=={"checkpoint.bin":P["fcp"],"vectors.bin":P["fv"]},"endpoint hashes")
O=L["output"]
need((O["round"],O["columns"],O["dual_support"],O["result_sha256"],O["watchdog_sha256"],O["checkpoint_sha256"],O["vector_cache_sha256"],O["no_round_1640"])==(1639,3968369,32704,P["fres"],P["fwd"],P["fcp"],P["fv"],True),"endpoint")

out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1639_CAP4000_INDEPENDENT_CHAIN_AUDIT_V1","status":"PASS_EXACT_ROUND1639_CAP4000_CHAIN","scope":"Accepted cap-equivalent r1627 through exact r1628..r1639; no r1640, closure, or conjecture claim.",
"input":{"round":1627,"columns":3547162,"support":7888,"cap_audit_sha256":P["ia"],"cap_manifest_sha256":P["im"],"checkpoint_sha256":P["icp"],"vector_cache_sha256":P["iv"],"compaction_sha256":P["icomp"]},
"producer":{"ledger_sha256":P["ledger"],"report_sha256":P["report"],"manifest_sha256":P["manifest"],"plan_sha256":P["plan"]},"stages":stages,
"exceptions":{"cooperative_native_overshoot_exact_set":sorted(coop),"exact_target_wall_cap_exact_set":sorted(wall),"refused_wrapper_attempt":"zero outputs/coverage","generic_native_limit_relaxation":False,"generic_status_relaxation":False,"precedent_audit_sha256":P["pre"],"precedent_manifest_sha256":P["prem"]},
"amendments":{"original_plan_sha256":P["orig"],"r1632_sha256":P["a32"],"r1635_sha256":P["a35"],"r1636_sha256":P["a36"],"r1638_sha256":P["a38"],"storage_audit_sha256":P["storage"],"central_compaction_sha256":P["central"],"watchdog_old_sha256":P["owd"],"watchdog_new_sha256":P["nwd"],"watchdog_diff_only_bound_and_error_text":True},
"resource_blocks":B,"replay":{"sha256":sha(HERE/"results_round1639_single_pass_replay.json"),"scanner_source_sha256":"8593fb69a16c8348f171c1d4423c8fd361aa2f165eaaf801ac893ae4894aa1b1","scanner_binary_sha256":"9d86e743658d6f9e9cc5a653a4fc4521f3d47c47a77ec47130526e7fcf63da9e","checkpoint_edges":12,"cache_edges":12,"columns":3968369,"terms":403999306,"candidate_hit_terms":R["candidate_hit_terms"],"verification_failures":0,"seconds":R["seconds"]},
"output":{"round":1639,"columns":3968369,"support":32704,"result_sha256":P["fres"],"watchdog_sha256":P["fwd"],"checkpoint_sha256":P["fcp"],"vector_cache_sha256":P["fv"],"no_round1640":True}}
tmp=HERE/"results_round1639_chain_audit.json.tmp"; tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); os.replace(tmp,HERE/"results_round1639_chain_audit.json")
print("PASS exact r1627->r1639 chain; 12 edges; 3,968,369 columns; no r1640")
