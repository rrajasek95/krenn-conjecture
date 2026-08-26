#!/usr/bin/env python3
"""Independent fail-closed direct cold/rare r1464 cap equivalence audit."""
from __future__ import annotations
import hashlib,json,os,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
PLAN=json.loads((HERE/"AUDIT_PLAN.json").read_text());ROOT=REPO/PLAN["producer_root"]
LABELS=["control_cap2250","candidate_cap2500"];CAPS={LABELS[0]:PLAN["control_cap"],LABELS[1]:PLAN["candidate_cap"]}
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59";BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048";WATCH="48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522";PRIME=1073741827;LIMIT=36*1024*1024
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def arg(c,f):need(c.count(f)==1,"command flag "+f);i=c.index(f);need(i+1<len(c),"command value "+f);return c[i+1]
def header(p):
 with p.open("rb") as f:d=f.read(44)
 need(d[:12]==b"AFF12CEG1\0\0\0","checkpoint magic");prime,r,c,s=struct.unpack_from("<QQQQ",d,12);need(p.stat().st_size==44+15*c+21*s,"checkpoint length");return {"prime":prime,"round":r,"columns":c,"support":s,"bytes":p.stat().st_size}
def norm(c,label):return [x.replace(f"/{label}/","/RUN/") for x in c]

need(sha(REPO/"computations/unaudited-codex-n8-affine251-d12-v4-1-round1463-cap2250-audit-2026-08-25/results_round1463_chain_audit.json")==PLAN["input_audit_sha256"],"input audit")
need(sha(REPO/"computations/unaudited-codex-n8-affine251-d12-v4-1-round1463-cap2250-audit-2026-08-25/FINAL_MANIFEST.sha256")==PLAN["input_manifest_sha256"],"input manifest")
need(sha(REPO/PLAN["portfolio_failure_audit"])==PLAN["portfolio_failure_audit_sha256"],"portfolio failure audit")
need(sha(REPO/PLAN["portfolio_failure_report"])==PLAN["portfolio_failure_report_sha256"],"portfolio failure report")
failure=load(REPO/PLAN["portfolio_failure_audit"])
need(failure["status"]=="PASS_FAIL_CLOSED_ZERO_COVERAGE" and failure["portfolio_tasks_accepted"]==0 and not failure["fixed_replay_run"] and not failure["cap2500_candidate_run"],"portfolio zero coverage")
need(failure["watchdog"]["sha256"]==PLAN["portfolio_lane_watchdog_sha256"] and failure["watchdog"]["status"]=="FAIL" and failure["watchdog"]["breach"]=="WALL_CAP" and failure["watchdog"]["returncode"]==-15,"portfolio failure telemetry")

for label in LABELS:
 for name in ("result.json","checkpoint.bin","vectors.bin","watchdog.json","stderr.log"):
  need((ROOT/label/name).is_file(),f"terminal artifact absent {label}/{name}")
 need(not any((ROOT/label).glob("*.tmp")),f"temporary output remains {label}")
results={x:load(ROOT/x/"result.json") for x in LABELS};watches={x:load(ROOT/x/"watchdog.json") for x in LABELS}
records={};semantics={};watchdog_source_hashes=set()
record_fields=["round","columns","new_columns","dual_support","new_support_rows","selected_strategy","selected_pivot"]
semantic_fields=["schema","status","incomplete_reason","degree","prime","group_order","provider_equations","provider_terms_parsed","provider_distinct_terms","seed_support","column_orbits_exposed","dual_support","rounds_completed","global_annihilation","target_pairing","workers","pivot_mode","strategy","elimination_kernel","incremental_basis","portfolio_period","portfolio_parallel","support_cap","wall_limit_seconds","rss_limit_gib","cached_vectors_loaded","vectors_materialized_on_restore","vector_cache_bytes"]
for label in LABELS:
 r,w=results[label],watches[label]
 need((r["status"],r["incomplete_reason"],r["rounds_completed"],len(r["rounds"]))==("INCOMPLETE_SEARCH_CAP","ROUND_CAP",1464,1),label+" status")
 need(r["cached_vectors_loaded"]==PLAN["input_columns"] and r["vectors_materialized_on_restore"]==0,label+" restore")
 need(r["column_cap"]==CAPS[label],label+" result cap")
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],label+" watchdog")
 need(w["elapsed_seconds"]<150 and w["peak_rss_kib"]<LIMIT,label+" resources")
 need(w["source_sha256"]==SOURCE and w["binary_sha256"]==BINARY,label+" source/binary")
 need(w["watchdog_sha256"]==WATCH and w["wall_limit_seconds"]==150,label+" watchdog pin");watchdog_source_hashes.add(w["watchdog_sha256"])
 need(w["result_sha256"]==sha(ROOT/label/"result.json"),label+" result telemetry pin")
 c=w["command"]
 for flag,value in (("--round-cap","1464"),("--column-cap",str(CAPS[label])),("--wall-seconds","120"),("--rss-gib","36"),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no"),("--prime",str(PRIME))):need(arg(c,flag)==value,label+" command "+flag)
 records[label]={k:r["rounds"][0][k] for k in record_fields};semantics[label]={k:r[k] for k in semantic_fields}
need(len(watchdog_source_hashes)==1,"watchdog source differs")
control,candidate=LABELS;need(records[control]==records[candidate],"round record differs");need(semantics[control]==semantics[candidate],"semantic fields differ")
left,right=norm(watches[control]["command"],control),norm(watches[candidate]["command"],candidate);need(len(left)==len(right),"command length")
diff=[(i,a,b) for i,(a,b) in enumerate(zip(left,right)) if a!=b];need(diff==[(left.index("2250000"),"2250000","2500000")],"not cap-only command diff: "+repr(diff))
cph={x:sha(ROOT/x/"checkpoint.bin") for x in LABELS};vch={x:sha(ROOT/x/"vectors.bin") for x in LABELS};need(len(set(cph.values()))==1 and len(set(vch.values()))==1,"output bytes differ")
heads={x:header(ROOT/x/"checkpoint.bin") for x in LABELS};need(heads[control]==heads[candidate],"checkpoint headers differ");h=heads[control]
need((h["prime"],h["round"],h["columns"],h["support"])==(PRIME,1464,records[control]["columns"],records[control]["dual_support"]),"endpoint header")
need(all(not (ROOT/x/"dual.tsv").exists() for x in LABELS),"dual must be absent")
out={"schema":"KRENN_AFFINE251_D12_ROUND1464_DIRECT_CAP2500_AUDIT_V1","status":"PASS_EXACT_DIRECT_CAP2250_TO_CAP2500_EQUIVALENCE","input":{"round":1463,"columns":PLAN["input_columns"],"support":PLAN["input_support"],"audit_sha256":PLAN["input_audit_sha256"],"manifest_sha256":PLAN["input_manifest_sha256"]},"round_record":records[control],"checkpoint_header":h,"checkpoint_sha256":cph[control],"vectors_sha256":vch[control],"control_result_sha256":sha(ROOT/control/"result.json"),"candidate_result_sha256":sha(ROOT/candidate/"result.json"),"control_watchdog_sha256":sha(ROOT/control/"watchdog.json"),"candidate_watchdog_sha256":sha(ROOT/candidate/"watchdog.json"),"watchdog_source_sha256":next(iter(watchdog_source_hashes)),"maximum_elapsed_seconds":max(watches[x]["elapsed_seconds"] for x in LABELS),"maximum_peak_rss_kib":max(watches[x]["peak_rss_kib"] for x in LABELS),"only_normalized_command_difference_is_cap":True,"exact_byte_equality":{"checkpoint":True,"vectors":True},"portfolio_nonpromotion":{"status":"REJECT_OPTIMIZATION_NOT_PROMOTED_ZERO_ACCEPTED_COVERAGE","failure_audit_sha256":PLAN["portfolio_failure_audit_sha256"],"failure_report_sha256":PLAN["portfolio_failure_report_sha256"],"correctness_effect":"none; direct cold/rare equivalence is independent","selection_status":"deferred"},"dual_outputs_absent":True,"continued_beyond_round1464":False,"production_mutated":False}
tmp=HERE/"results_round1464_direct_cap2500_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_round1464_direct_cap2500_audit.json");print(json.dumps(out,sort_keys=True))
