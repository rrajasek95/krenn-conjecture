#!/usr/bin/env python3
"""Independent exact descendant/full-cache referee of r1640 v3 attempt2."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
P=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-v3-resource-design-2026-08-25"
D=P/"candidate_cap4250_v3_attempt2"
V2=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-design-2026-08-25"
CHAIN=ROOT/"computations/unaudited-codex-n8-affine251-d12-v4-1-round1639-cap4000-audit-2026-08-25"
V3A=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-v3-resource-design-audit-2026-08-25"
PINS={"producer_validation":"ad2ce5c5b50aeebd2621abd10ea16c8364e1880812baf2b6b947c199195233b9","producer_manifest":"a33ad9c609a15698a98eb4673472be7a8c070240a858ad39be8e77cdfbbf4e19","producer_report":"e0e2ced7638d09cfc4e6695fd3052df72a6610465a82b154827329dd40db93af","launch":"de0cc1b29408983dd1e60f0e83b2564000b6af687798548e19181d70ca8bc83d","result":"896a0763c16bd8c3db96c5016de8d39e029297d00db63268508d75d804200af0","watchdog":"4f2218d49480841bf1ee6fcc5bc34aa1bd77cf55b944f2a72e8928a44694f361","checkpoint":"12f79c86f8d8d20d3f9b83c634e82d689461796df60f9cd63feed9d86545ca8d","cache":"1d7ce92a7df3a6382332f1af85af4dd1f4a9b7d49c6a6d206066dcce9d36de12","chain_audit":"a99a307f99bd88f8b363ca73bbc3af631a333bab228fbdb43c3e604382150387","chain_replay":"4996c85de7aedf853ba6428e948b69e88a5a07d170614ce9fea5f98714d3c5e5","chain_manifest":"de3d1a5e390e0545d5f4c5bca7b7f20fa9205056a772bbd8d1ca841e7ae98b0c","input_cp":"ab63c22095dd44d771525af9ba218ee36c9e6f4236a80addbc15692165c531a5","input_cache":"4d342801fa9e6d25aff95d7b1172f5bff803e8436c01f9237b79e5a42bf6999e","v3_referee":"d7b75e567f7073eb11b5b038867bed378d3cd2233a326ba684f6e19dd5536ba0","v3_manifest":"4bb520af95c52f3c880717a8d7fb58f0855f7f2dffc776dddcc838aec50cfbf4","failure_manifest":"8152ea7ed72e70bf0d8acf9992260f7b795ff714cd25004c364133dcd166c928","failure_watchdog":"074ea4b09bb11da50737b4dff59e73d5dea17aa1a86e665a9645b0c9c79f691f"}
def need(x,m):
    if not x:raise AssertionError(m)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def pin(path,d):need(path.is_file() and sha(path)==d,f"pin {path}")
def load(path):return json.loads(path.read_text())
for path,key in [(P/"results_attempt2_producer_validation.json","producer_validation"),(P/"ATTEMPT2_MANIFEST.sha256","producer_manifest"),(P/"ATTEMPT2_REPORT.md","producer_report"),(P/"LAUNCH_RECORD_ATTEMPT2.json","launch"),(D/"result.json","result"),(D/"watchdog.json","watchdog"),(CHAIN/"results_round1639_chain_audit.json","chain_audit"),(CHAIN/"results_round1639_single_pass_replay.json","chain_replay"),(CHAIN/"FINAL_MANIFEST.sha256","chain_manifest"),(V3A/"results_v3_resource_referee.json","v3_referee"),(V3A/"FINAL_MANIFEST.sha256","v3_manifest"),(V2/"FAILURE_MANIFEST_CANDIDATE_ATTEMPT1.sha256","failure_manifest"),(V2/"candidate_cap4250/watchdog.json","failure_watchdog")]:pin(path,PINS[key])

# Replay producer manifest with independent endpoint hashes for the two large files.
large=dict(line.split(maxsplit=1)[::-1] for line in (HERE/"FINAL_ENDPOINT_HASHES.sha256").read_text().splitlines())
need(large=={"checkpoint.bin":PINS["checkpoint"],"vectors.bin":PINS["cache"]},"endpoint hashes")
for line in (P/"ATTEMPT2_MANIFEST.sha256").read_text().splitlines():
    d,n=line.split(maxsplit=1)
    if n.endswith("checkpoint.bin"):need(d==large["checkpoint.bin"],"manifest checkpoint")
    elif n.endswith("vectors.bin"):need(d==large["vectors.bin"],"manifest cache")
    else:pin(P/n,d)

r,w,v,l=load(D/"result.json"),load(D/"watchdog.json"),load(P/"results_attempt2_producer_validation.json"),load(P/"LAUNCH_RECORD_ATTEMPT2.json")
need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP",1640,4069711,76616),"result endpoint")
need(len(r["rounds"])==1 and (r["rounds"][0]["round"],r["rounds"][0]["columns"],r["rounds"][0]["new_columns"])==(1640,4069711,101342),"exact r1640 record")
need(r["cached_vectors_loaded"]==3968369 and r["vectors_materialized_on_restore"]==0,"fresh restore")
need((r["prime"],r["column_cap"],r["wall_limit_seconds"],r["workers"],r["strategy"],r["pivot_mode"],r["elimination_kernel"],r["incremental_basis"])==(1073741827,4250000,210,16,"cold","rare","hierarchical",False),"engine mode")
need(r["global_annihilation"] is None and r["target_pairing"] is None,"nonterminal state")
need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],"watchdog")
need(w["elapsed_seconds"]==198.715821<240 and w["peak_rss_kib"]==21528480<37748736,"resource")
need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"],w["result_sha256"])==("3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59","79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997",PINS["result"]),"provenance")
cmd=w["command"];need(cmd[cmd.index("--wall-seconds")+1]=="210" and cmd[cmd.index("--column-cap")+1]=="4250000" and cmd[cmd.index("--round-cap")+1]=="1640","command literals")
old=load(V2/"candidate_cap4250/watchdog.json")["command"];normalized=list(cmd);normalized[normalized.index("--wall-seconds")+1]="150"
need(normalized==old,"attempt1/attempt2 sole solver diff")
need(w["wall_limit_seconds"]==240 and load(V2/"candidate_cap4250/watchdog.json")["wall_limit_seconds"]==180,"sole wrapper diff")
need({x.name for x in D.iterdir()}=={"checkpoint.bin","vectors.bin","result.json","watchdog.json","stdout.log","stderr.log"},"atomic file set")
need(not any(P.rglob("*1641*")),"r1641 artifact")

replay=load(HERE/"results_attempt2_single_pass_replay.json")
need(replay["status"]=="PASS_ALL_DESCENDANT_EDGES_AND_ALL_COLUMNS" and replay["rounds"]==[1639,1640],"replay status/rounds")
need(replay["columns"]==[3968369,4069711] and replay["supports"]==[32704,76616] and replay["new_records_by_origin"]==[3968369,101342],"replay census")
need(replay["checkpoint_descendant_edges"]==replay["cache_descendant_edges"]==1 and replay["inherited_vectors_byte_identical"],"strict descendant")
need(replay["provider_fingerprint"]==9218588987274412661 and replay["final_vector_fingerprint"]==16855404434860827212,"fingerprints")
need(replay["terms_replayed"]==414162800 and replay["candidate_hit_terms"]==164115 and replay["target_terms"]==2 and replay["verification_failures"]==0,"full replay")
need(v["status"]=="PASS_EXACT_R1640_DESCENDANT_HELD_FOR_INDEPENDENT_FULL_REPLAY" and v["held_guards"]["round1641_forbidden"] and not v["held_guards"]["continuation_authorized"],"producer hold")
need(l["input_binding"]["checkpoint_sha256"]==PINS["input_cp"] and l["input_binding"]["vector_cache_sha256"]==PINS["input_cache"] and l["candidate"]["fresh_apfs_clone_from_audited_r1639"],"fresh input")
need(l["approval_binding"]["v3_resource_referee_sha256"]==PINS["v3_referee"] and l["failed_attempt1_binding"]["failure_manifest_sha256"]==PINS["failure_manifest"] and l["failed_attempt1_binding"]["coverage"]==0 and l["failed_attempt1_binding"]["reuse_forbidden"],"approvals/failure exclusion")

out={"schema":"KRENN_AFFINE251_D12_R1640_CAP4250_V3_ATTEMPT2_INDEPENDENT_REFEREE_V1","status":"PASS_EXACT_R1640_CAP4250_DESCENDANT","scope":"Exact r1639->r1640 candidate promotion only; no r1641, terminal D12 certificate, or conjecture claim.","input":{"round":1639,"columns":3968369,"support":32704,"audit_sha256":PINS["chain_audit"],"replay_sha256":PINS["chain_replay"],"manifest_sha256":PINS["chain_manifest"],"checkpoint_sha256":PINS["input_cp"],"vector_cache_sha256":PINS["input_cache"]},"approvals":{"v3_resource_referee_sha256":PINS["v3_referee"],"v3_resource_manifest_sha256":PINS["v3_manifest"],"failed_attempt1_manifest_sha256":PINS["failure_manifest"],"failed_attempt1_coverage":0,"failed_attempt1_reuse":False},"producer":{"validation_sha256":PINS["producer_validation"],"manifest_sha256":PINS["producer_manifest"],"launch_sha256":PINS["launch"]},"replay":{"sha256":sha(HERE/"results_attempt2_single_pass_replay.json"),"scanner_source_sha256":"8593fb69a16c8348f171c1d4423c8fd361aa2f165eaaf801ac893ae4894aa1b1","scanner_binary_sha256":"9d86e743658d6f9e9cc5a653a4fc4521f3d47c47a77ec47130526e7fcf63da9e","checkpoint_edges":1,"cache_edges":1,"inherited_records":3968369,"new_records":101342,"final_columns":4069711,"terms":414162800,"target_normalized":True,"verification_failures":0,"seconds":replay["seconds"]},"output":{"round":1640,"columns":4069711,"support":76616,"result_sha256":PINS["result"],"watchdog_sha256":PINS["watchdog"],"checkpoint_sha256":PINS["checkpoint"],"vector_cache_sha256":PINS["cache"],"native_seconds":196.456243,"wrapper_seconds":198.715821,"peak_rss_kib":21528480,"atomic":True,"no_round1641":True},"continuation_authorized":False}
tmp=HERE/"results_attempt2_referee.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_attempt2_referee.json")
print("PASS exact r1640 cap4.25 descendant; no r1641")
