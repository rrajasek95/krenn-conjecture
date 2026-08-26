#!/usr/bin/env python3
import hashlib, json, os
from pathlib import Path

HERE=Path(__file__).resolve().parent; REPO=HERE.parents[1]
PROD=REPO/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1601_cap3500_to1613"
STAGE=PROD/"stage01_cap1603"; SEALED=PROD.parent/"sealed_v4_1"
def need(x,m):
 if not x: raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p): return json.loads(p.read_text())

pins={
 "input_audit":(REPO/"computations/unaudited-codex-n8-affine251-d12-round1601-direct-cap3500-gate-audit-2026-08-25/results_round1601_direct_cap3500_audit.json","ab839af1011cf3416628627739db8063066ff636b74557df39236c87d177f576"),
 "input_manifest":(REPO/"computations/unaudited-codex-n8-affine251-d12-round1601-direct-cap3500-gate-audit-2026-08-25/FINAL_MANIFEST.sha256","6dad4784871c8041a528dacd7f4b3fd3605d7a45451d9c15cd672a68e7f469d7"),
 "compaction":(REPO/"computations/unaudited-codex-n8-affine251-d12-v4-1-round1463-cap2000-audit-2026-08-25/COMPACTION_EXECUTION.md","1765261cf397498f6ba2efabffaa1ec64b2978e498af6ee4c278107aa07c8da1"),
 "source":(SEALED/"main.rs","3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"),
 "binary":(SEALED/"sparse_d12_dual","79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"),
 "plan_amended":(PROD/"PLAN.json","540956f18d3aae13e3b35854f4aa194d187f14750dfb686785314a14e25bd7cd"),
 "result":(STAGE/"result.json","07faace270f124d1a0c0eaf8a5757388d7aec4ce73695eaba633f03480020633"),
 "watchdog":(STAGE/"watchdog.json","344d91239476321420d7b95fc589a2384bbec985b7003d55ac683043a290c4b0"),
}
for n,(p,h) in pins.items(): need(sha(p)==h,"pin "+n)
r=load(STAGE/"result.json"); w=load(STAGE/"watchdog.json"); inheritance=load(HERE/"results_stage01_inheritance.json"); large=load(HERE/"results_stage01_large_sha256.json")
need((r["status"],r["incomplete_reason"],r["rounds_completed"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP",1603),"result status")
need([(q["round"],q["columns"],q["new_columns"]) for q in r["rounds"]]==[(1602,3119803,15048),(1603,3133635,13832)],"round chain")
need(r["cached_vectors_loaded"]==3104755 and r["vectors_materialized_on_restore"]==0 and r["column_orbits_exposed"]==3133635 and r["dual_support"]==5517,"state")
need(r["elapsed_seconds"]==126.429282 and r["wall_limit_seconds"]==120,"native elapsed")
need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"] and w["elapsed_seconds"]==128.306338 and w["elapsed_seconds"]<150,"hard watchdog")
need(w["peak_rss_kib"]==22083840 and max(x["rss_kib"] for x in w["samples"])==22083840 and w["peak_rss_kib"]<37748736,"rss")
need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==("3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59","79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522"),"executable pins")
need(w["result_sha256"]==pins["result"][1] and not any(STAGE.glob("*.tmp")) and not (STAGE/"dual.tsv").exists(),"atomic artifacts")
need(inheritance["status"]=="PASS_EXACT_CHECKPOINT_AND_CACHE_DESCENDANT" and inheritance["parent_round"]==1601 and inheritance["child_round"]==1603 and inheritance["parent_columns"]==inheritance["inherited_records_byte_identical"]==3104755 and inheritance["child_columns"]==3133635 and inheritance["new_child_records"]==28880 and not inheritance["final_candidate_pairing_replayed"],"inheritance")
need(large=={"schema":"KRENN_AFFINE251_D12_ROUND1603_STAGE01_LARGE_SHA256_V1","input_checkpoint_sha256":"83955dbcc460c5fe39623e25b8337eb80bcfc9921eeafb4c1a887cfa6f5abb01","input_vectors_sha256":"c9d850754e9451015a3bf4fa6b51d6f0bb8c3ecdaeecbdef456abaa5fae7b046","output_checkpoint_sha256":"0979e0a2b7c53425394d846062d5a9a78aca519eb656f625ccc1d72698e36c63","output_vectors_sha256":"9148e9105eae5a63623f0b37eb0972e1f0d0af70d324d18234b8fd8374eb628b","independently_hashed_after_producer_clear":True},"large hashes")
source=(SEALED/"main.rs").read_text()
need("loop {\n        if let Err(reason) = gate.check()" in source and "if completed_rounds >= config.round_cap {" in source and source.index("if let Err(reason) = gate.check()")<source.index("if completed_rounds >= config.round_cap {") and 'Some("ROUND_CAP")' in source,"source loop semantics")
out={"schema":"KRENN_AFFINE251_D12_ROUND1603_STAGE01_EDGE_AUDIT_V1","status":"PASS_EXACT_EDGE_HARD_RESOURCE_PASS_COOPERATIVE_NATIVE_OVERSHOOT","input":{"round":1601,"columns":3104755,"support":6070,"checkpoint_sha256":large["input_checkpoint_sha256"],"vectors_sha256":large["input_vectors_sha256"]},"output":{"round":1603,"columns":3133635,"support":5517,"checkpoint_sha256":large["output_checkpoint_sha256"],"vectors_sha256":large["output_vectors_sha256"]},"inheritance":inheritance,"native_timer":{"configured_seconds":120,"result_elapsed_seconds":126.429282,"classification":"COOPERATIVE_TOP_OF_LOOP_OVERSHOOT_NOT_HARD_RESOURCE_FAILURE","source_semantics":"Gate::check at loop top; after the completed round, ROUND_CAP checkpoint/cache/result publishing has no second native wall check"},"hard_watchdog":{"limit_seconds":150,"elapsed_seconds":128.306338,"status":"PASS","returncode":0,"breach":None,"atomic_outputs_clean":True,"peak_rss_kib":22083840,"rss_limit_kib":37748736},"pins":{n:h for n,(_p,h) in pins.items()},"plan_amendment":{"sha256":pins["plan_amended"][1],"remaining_stages_one_round":True},"final_all_column_pairing_replayed":False,"continued":False}
t=HERE/"results_stage01_edge_audit.json.tmp";t.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(t,HERE/"results_stage01_edge_audit.json");print(json.dumps({"status":out["status"],"output":out["output"],"inherited":inheritance["inherited_records_byte_identical"]},sort_keys=True))
