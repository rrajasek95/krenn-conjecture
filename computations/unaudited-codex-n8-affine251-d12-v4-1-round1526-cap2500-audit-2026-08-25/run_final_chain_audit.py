#!/usr/bin/env python3
"""Independent exact one-edge audit of r1524→r1526."""
import hashlib,importlib.util,json,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];P=json.loads((H/"AUDIT_PLAN.json").read_text());D=R/P["production_root"]/"stage01_cap1526"
ICP=R/P["input_checkpoint"];IV=R/P["input_vectors"]
FMT=R/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59";BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048";WATCH="48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522";LIMIT=36*1024*1024
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def arg(c,f):need(c.count(f)==1,"command "+f);return c[c.index(f)+1]
for k,n in (("input_manifest_sha256","input_manifest"),("input_audit_sha256","input_audit"),("compaction_record_sha256","compaction_record"),("cap_stop_sha256","cap_stop")):need(sha(R/P[n])==P[k],k)
need(sha(ICP)==P["input_checkpoint_sha256"] and sha(IV)==P["input_vectors_sha256"],"input artifacts")
need(sha(R/P["production_root"]/"REPORT.md")==P["producer_report_sha256"] and sha(R/P["production_root"]/"MANIFEST.sha256")==P["producer_manifest_sha256"],"producer seal")
ia=load(R/P["input_audit"]);need(ia["status"]=="PASS_EXACT_FULLY_TELEMETERED_ROUND1524_CAP2500_CHAIN" and ia["final"]["round"]==1524 and ia["artifact_sha256"]["stage08_cap1524_checkpoint"]==P["input_checkpoint_sha256"] and ia["artifact_sha256"]["stage08_cap1524_vectors"]==P["input_vectors_sha256"],"input audit")
stop=load(R/P["cap_stop"]);need(stop["status"]=="PASS_STAGE01_STOPPED_FAIL_CLOSED_BEFORE_STAGE02" and stop["frozen_column_guard"]["shortfall"]==672 and stop["coverage"]["no_stage02_launched"] is True,"cap stop")
need(not (R/P["production_root"]/"stage02_cap1528").exists(),"stage02 absent")
r=load(D/"result.json");w=load(D/"watchdog.json");rr=r["rounds"]
need([x["round"] for x in rr]==[1525,1526] and r["rounds_completed"]==1526 and r["cached_vectors_loaded"]==P["input_columns"] and r["vectors_materialized_on_restore"]==0,"rounds/restore")
need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,2500000),"mode")
need((r["status"],r["incomplete_reason"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),"stop")
cols=P["input_columns"]
for x in rr:need(x["new_columns"]>0 and x["selected_strategy"]=="cold" and x["selected_pivot"]=="rare","round record");cols+=x["new_columns"];need(x["columns"]==cols,"column recurrence")
need((cols,r["column_orbits_exposed"],r["dual_support"])==(2393602,2393602,3341),"census")
need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],"watchdog")
need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),"pins")
need(w["elapsed_seconds"]<150 and w["peak_rss_kib"]<LIMIT and all(x["rss_kib"]<LIMIT for x in w["samples"]),"resources")
for f,v in (("--round-cap","1526"),("--column-cap","2500000"),("--wall-seconds","120"),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no")):need(arg(w["command"],f)==v,"command "+f)
need(not any(D.glob("*.tmp")),"temporary outputs")
sp=importlib.util.spec_from_file_location("fmt",FMT);fmt=importlib.util.module_from_spec(sp);sp.loader.exec_module(fmt)
def pc(p,round_,columns,support):
 x=fmt.parse_checkpoint(p);need((x["round"],len(x["columns"]),x["support"],x["target_coefficient"])==(round_,columns,support,1),"checkpoint header");return x
a=pc(ICP,1524,P["input_columns"],P["input_support"]);b=pc(D/"checkpoint.bin",1526,cols,3341);i=j=0
while i<len(a["columns"]):
 need(j<len(b["columns"]),"checkpoint lost suffix")
 if b["columns"][j]<a["columns"][i]:j+=1
 else:need(b["columns"][j]==a["columns"][i],"checkpoint inherited omission");i+=1;j+=1
with IV.open("rb") as f,(D/"vectors.bin").open("rb") as g:
 ah,bh=fmt.vector_header(f,"old"),fmt.vector_header(g,"new");need((ah["count"],bh["count"])==(P["input_columns"],cols) and ah["provider_fingerprint"]==bh["provider_fingerprint"],"cache headers")
 u,v=fmt.vector_record(f,"old"),fmt.vector_record(g,"new");same=extra=0
 while u is not None:
  need(v is not None,"cache lost suffix")
  if v[0]<u[0]:extra+=1;v=fmt.vector_record(g,"new")
  elif v[0]==u[0]:need(v[1]==u[1],"inherited vector changed");same+=1;u=fmt.vector_record(f,"old");v=fmt.vector_record(g,"new")
  else:need(False,"inherited vector omitted")
 while v is not None:extra+=1;v=fmt.vector_record(g,"new")
 need((same,extra)==(P["input_columns"],cols-P["input_columns"]) and f.read(1)==g.read(1)==b"","cache census")
replay=load(H/"results_round1526_all_column_replay.json");need(replay["status"]=="PASS_ALL_COLUMNS" and replay["round"]==1526 and replay["columns_replayed"]==cols and replay["verification_failures"]==0 and replay["target_terms"]==2,"replay")
hashes={n:sha(D/f) for n,f in (("stage01_result","result.json"),("stage01_checkpoint","checkpoint.bin"),("stage01_vectors","vectors.bin"),("stage01_watchdog","watchdog.json"),("stage01_stderr","stderr.log"))}
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1526_CAP2500_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1526_CAP2500_CHAIN","scope":"Accepted exact r1524→r1526 edge; stopped before r1527 by frozen column-headroom guard.","input":{"round":1524,"columns":P["input_columns"],"support":P["input_support"]},"final":{"round":1526,"columns":cols,"new_columns":cols-P["input_columns"],"support":3341,"target_coefficient":1},"checkpoint_edge":{"preserved":P["input_columns"],"new_columns":cols-P["input_columns"]},"cache_edge":{"preserved_byte_identically":same,"new_records":extra,"provider_fingerprint":bh["provider_fingerprint"]},"all_column_replay":replay,"resources":{"watchdog_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"],"rss_limit_kib":LIMIT},"cap_safety_stop":{"headroom":stop["frozen_column_guard"]["headroom_after_stage01"],"required":stop["frozen_column_guard"]["required_headroom"],"shortfall":672,"stage02_launched":False},"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH,"input_audit_sha256":P["input_audit_sha256"],"input_manifest_sha256":P["input_manifest_sha256"],"compaction_record_sha256":P["compaction_record_sha256"],"cap_stop_sha256":P["cap_stop_sha256"],"replay_sha256":sha(H/"results_round1526_all_column_replay.json")},"verdict_note":"Round1526 is exact and resumable only under separately audited higher-cap authority; no r1527 claim."}
t=H/"results_round1526_chain_audit.json.tmp";t.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(t,H/"results_round1526_chain_audit.json");print(json.dumps(out,sort_keys=True))
