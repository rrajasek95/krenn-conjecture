#!/usr/bin/env python3
"""Independent descendant/cache audit of the accepted r1504→r1524 chain."""
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
P=json.loads((HERE/"AUDIT_PLAN.json").read_text());PROD=REPO/P["production_root"]
ICP=REPO/P["input_checkpoint"];IV=REPO/P["input_vectors"]
FORMAT=REPO/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCH90="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
WATCH120="48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522"
LIMIT=36*1024*1024
OLD=set(P["aggregate_blocks"][0]);NEW=set(P["aggregate_blocks"][1])
CAPS={"stage01":1524,"stage02":1524,"stage03_recovery_cap1514":1514,"stage04_cap1516":1516,
      "stage05_recovery120_cap1518":1518,"stage06_cap1520":1520,"stage07_cap1522":1522,"stage08_cap1524":1524}
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def arg(c,f):need(c.count(f)==1,"command flag "+f);return c[c.index(f)+1]

for key,path in (("input_manifest_sha256",P["input_manifest"]),("input_audit_sha256",P["input_audit"]),("compaction_record_sha256",P["compaction_record"])):
 need(sha(REPO/path)==P[key],key)
need(sha(ICP)==P["input_checkpoint_sha256"],"input checkpoint")
need(sha(IV)==P["input_vectors_sha256"],"input vectors")
need(sha(FORMAT)=="976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67","format parser")
for n,k in (("PRODUCER_LEDGER.json","producer_ledger_sha256"),("REPORT.md","producer_report_sha256"),("MANIFEST.sha256","producer_manifest_sha256")):
 need(sha(PROD/n)==P[k],"producer "+n)
ia=load(REPO/P["input_audit"])
need(ia["status"]=="PASS_EXACT_FULLY_TELEMETERED_ROUND1504_CAP2500_CHAIN" and ia["final"]["round"]==P["input_round"] and ia["artifact_sha256"]["stage05_checkpoint"]==P["input_checkpoint_sha256"] and ia["artifact_sha256"]["stage05_vectors"]==P["input_vectors_sha256"],"input audit contents")

failed=PROD/"stage03";fe=load(failed/"FAILURE_EVIDENCE.json")
need(fe["status"]=="REJECT_WRAPPER_WALL_DURING_CACHE_PUBLICATION" and fe["attempt"]["result_present"] is False and fe["attempt"]["abort_final_output_absent"] is True and fe["acceptance"]["accepted_frontier_remains_round"]==1512 and not (failed/"result.json").exists(),"failed stage quarantine")
zero=PROD/"stage05_cap1518";ze=load(zero/"NO_PROGRESS_EVIDENCE.json");zr=load(zero/"result.json");zw=load(zero/"watchdog.json")
need(ze["status"]=="PASS_ATOMIC_IDENTITY_ZERO_COVERAGE" and ze["coverage_count"]==0 and ze["continuation_edge"] is False,"zero stage evidence")
need(zr["rounds"]==[] and zr["rounds_completed"]==1516 and zr["cached_vectors_loaded"]==zr["column_orbits_exposed"]==2329637,"zero stage result")
need(zw["status"]=="PASS" and zw["returncode"]==0 and zw["atomic_outputs_clean"],"zero stage watchdog")

sp=importlib.util.spec_from_file_location("fmt",FORMAT);fmt=importlib.util.module_from_spec(sp);sp.loader.exec_module(fmt)
dirs=[PROD/n for n in P["accepted_stage_dirs"]]
need(all((d/"result.json").is_file() for d in dirs),"accepted stage result set")
actual={d.name for d in PROD.iterdir() if d.is_dir() and (d/"result.json").is_file()}
need(actual==set(P["accepted_stage_dirs"])|{"stage05_cap1518"},"unexpected result-bearing stage")
stages=[];rounds=[];cols=P["input_columns"]
for i,d in enumerate(dirs):
 r=load(d/"result.json");w=load(d/"watchdog.json");rr=r["rounds"]
 first=P["input_round"]+1 if i==0 else stages[-1]["output_round"]+1
 need(rr and rr[0]["round"]==first and [x["round"] for x in rr]==list(range(first,rr[-1]["round"]+1)),d.name+" rounds")
 need(r["rounds_completed"]==rr[-1]["round"] and r["cached_vectors_loaded"]==cols and r["vectors_materialized_on_restore"]==0,d.name+" restore")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,P["column_cap"]),d.name+" mode")
 need((r["status"],r["incomplete_reason"]) in (("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),("INCOMPLETE_RESOURCE_GATE","WALL_CAP")),d.name+" status")
 need(rr[-1]["round"]<=CAPS[d.name],d.name+" cap")
 for x in rr:
  need(x["new_columns"]>0 and x["selected_strategy"]=="cold" and x["selected_pivot"]=="rare",d.name+" record")
  cols+=x["new_columns"];need(x["columns"]==cols,d.name+" recurrence")
 need((r["column_orbits_exposed"],r["dual_support"])==(cols,rr[-1]["dual_support"]),d.name+" census")
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],d.name+" watchdog")
 watch,wall,wrapper=(WATCH90,"90",115) if d.name in OLD else (WATCH120,"120",150)
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,watch),d.name+" pins")
 need(w["peak_rss_kib"]<LIMIT and w["elapsed_seconds"]<wrapper and all(x["rss_kib"]<LIMIT for x in w["samples"]),d.name+" resources")
 need(w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.5,d.name+" telemetry")
 for f,v in (("--round-cap",str(CAPS[d.name])),("--column-cap",str(P["column_cap"])),("--wall-seconds",wall),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no")):
  need(arg(w["command"],f)==v,d.name+" command "+f)
 need(not any(d.glob("*.tmp")),d.name+" temporary outputs")
 stages.append({"stage":d.name,"input_round":first-1,"output_round":rr[-1]["round"],"input_columns":r["cached_vectors_loaded"],"output_columns":cols,"support":r["dual_support"],"status":r["status"],"reason":r["incomplete_reason"],"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]});rounds+=rr
need([x["round"] for x in rounds]==list(range(P["input_round"]+1,P["target_round"]+1)),"global rounds")
blocks=[sum(next(s["watchdog_elapsed_seconds"] for s in stages if s["stage"]==n) for n in b) for b in P["aggregate_blocks"]]
need(all(x<540 for x in blocks),"block wall")

def pc(path,r,c,s):
 x=fmt.parse_checkpoint(path);need((x["round"],len(x["columns"]),x["support"],x["target_coefficient"])==(r,c,s,1),"checkpoint header");return x
def ce(a,b,x,y):
 aa=pc(a,*x);bb=pc(b,*y);i=j=0
 while i<len(aa["columns"]):
  need(j<len(bb["columns"]),"checkpoint lost suffix")
  if bb["columns"][j]<aa["columns"][i]:j+=1
  else:need(bb["columns"][j]==aa["columns"][i],"checkpoint omitted inherited");i+=1;j+=1
 return {"input_round":x[0],"output_round":y[0],"preserved":x[1],"new_columns":y[1]-x[1]}
def ve(a,b,x,y):
 with a.open("rb") as f,b.open("rb") as g:
  ah,bh=fmt.vector_header(f,"old"),fmt.vector_header(g,"new");need((ah["count"],bh["count"])==(x[1],y[1]) and ah["provider_fingerprint"]==bh["provider_fingerprint"],"cache headers")
  u,v=fmt.vector_record(f,"old"),fmt.vector_record(g,"new");same=extra=0
  while u is not None:
   need(v is not None,"cache lost suffix")
   if v[0]<u[0]:extra+=1;v=fmt.vector_record(g,"new")
   elif v[0]==u[0]:need(v[1]==u[1],"inherited vector changed");same+=1;u=fmt.vector_record(f,"old");v=fmt.vector_record(g,"new")
   else:need(False,"inherited vector omitted")
  while v is not None:extra+=1;v=fmt.vector_record(g,"new")
  need(f.read(1)==g.read(1)==b"","cache trailing")
 need((same,extra)==(x[1],y[1]-x[1]),"cache census")
 return {"input_round":x[0],"output_round":y[0],"preserved_byte_identically":same,"new_records":extra,"provider_fingerprint":bh["provider_fingerprint"],"input_vector_fingerprint":ah["vector_fingerprint"],"output_vector_fingerprint":bh["vector_fingerprint"]}
states=[(P["input_round"],P["input_columns"],P["input_support"])]+[(s["output_round"],s["output_columns"],s["support"]) for s in stages]
cps=[ICP]+[d/"checkpoint.bin" for d in dirs];vs=[IV]+[d/"vectors.bin" for d in dirs];cpedges=[];vedges=[]
for i in range(len(dirs)):
 cpedges.append(ce(cps[i],cps[i+1],states[i],states[i+1]));vedges.append(ve(vs[i],vs[i+1],states[i],states[i+1]))

need(sha(zero/"checkpoint.bin")==sha(PROD/"stage04_cap1516/checkpoint.bin")==ze["input_checkpoint_sha256"]==ze["output_checkpoint_sha256"],"zero checkpoint identity")
need(sha(zero/"vectors.bin")==sha(PROD/"stage04_cap1516/vectors.bin")==ze["input_cache_sha256"]==ze["output_cache_sha256"],"zero cache identity")
replay=load(HERE/"results_round1524_all_column_replay.json")
need(replay["status"]=="PASS_ALL_COLUMNS" and replay["round"]==1524 and replay["columns_replayed"]==cols and replay["verification_failures"]==0 and replay["target_terms"]==2,"replay")
hashes={}
for d in dirs:
 for k,n in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")):hashes[d.name+"_"+k]=sha(d/n)
for d,names in ((failed,("FAILURE_EVIDENCE.json","FAILURE_REPORT.md","watchdog.json","stderr.log")),(zero,("NO_PROGRESS_EVIDENCE.json","result.json","checkpoint.bin","vectors.bin","watchdog.json","stderr.log"))):
 for n in names:hashes[d.name+"_diagnostic_"+n]=sha(d/n)
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1524_CAP2500_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1524_CAP2500_CHAIN","scope":"Accepted r1504 cap2.5m state through exact rounds1505..1524; no r1525 continuation or closure claim.","input":{"round":P["input_round"],"columns":P["input_columns"],"support":P["input_support"],"checkpoint_sha256":P["input_checkpoint_sha256"],"vectors_sha256":P["input_vectors_sha256"]},"final":{"round":1524,"columns":cols,"new_columns":cols-P["input_columns"],"support":stages[-1]["support"],"target_coefficient":1},"stage_summaries":stages,"quarantined_diagnostics":{"failed_stage03":"zero accepted coverage; result absent","stage05_cap1518":"atomic byte-identical identity; zero accepted coverage"},"checkpoint_edges":cpedges,"cache_edges":vedges,"resources":{"aggregate_block_watchdog_seconds":blocks,"each_required_less_than":540,"maximum_peak_rss_kib":max(s["peak_rss_kib"] for s in stages),"rss_limit_kib":LIMIT},"all_column_replay":replay,"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog90_sha256":WATCH90,"watchdog120_sha256":WATCH120,"input_manifest_sha256":P["input_manifest_sha256"],"input_audit_sha256":P["input_audit_sha256"],"producer_manifest_sha256":P["producer_manifest_sha256"],"compaction_record_sha256":P["compaction_record_sha256"],"replay_sha256":sha(HERE/"results_round1524_all_column_replay.json")},"verdict_note":"Round1524 is an exact target-round resumable state, not a terminal global dual."}
tmp=HERE/"results_round1524_chain_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_round1524_chain_audit.json");print(json.dumps(out,sort_keys=True))
