#!/usr/bin/env python3
"""Independent exact six-edge audit of r1527→r1538 at cap 2.75m."""
import hashlib,importlib.util,json,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];P=json.loads((H/"AUDIT_PLAN.json").read_text());ROOT=R/P["production_root"];ICP=R/P["input_checkpoint"];IV=R/P["input_vectors"]
FMT=R/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py";SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59";BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048";WATCH="48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522";LIMIT=36*1024*1024
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def arg(c,f):need(c.count(f)==1,"command "+f);return c[c.index(f)+1]
for k,n in (("input_audit_sha256","input_audit"),("input_manifest_sha256","input_manifest"),("compaction_record_sha256","compaction_record")):need(sha(R/P[n])==P[k],k)
need(sha(ICP)==P["input_checkpoint_sha256"] and sha(IV)==P["input_vectors_sha256"],"input artifacts")
for n,k in (("PRODUCER_LEDGER.json","producer_ledger_sha256"),("REPORT.md","producer_report_sha256"),("MANIFEST.sha256","producer_manifest_sha256")):need(sha(ROOT/n)==P[k],"producer "+n)
ia=load(R/P["input_audit"]);need(ia["status"]=="PASS_EXACT_DIRECT_CAP2500_TO_CAP2750_EQUIVALENCE" and ia["accepted_candidate"]=="candidate_cap2750" and ia["checkpoint_sha256"]==P["input_checkpoint_sha256"] and ia["vectors_sha256"]==P["input_vectors_sha256"],"input audit")
sp=importlib.util.spec_from_file_location("fmt",FMT);fmt=importlib.util.module_from_spec(sp);sp.loader.exec_module(fmt)
dirs=[ROOT/s["name"] for s in P["stages"]];need(all((d/"result.json").is_file() for d in dirs),"stage set")
need({d.name for d in ROOT.iterdir() if d.is_dir() and (d/"result.json").is_file()}==set(d.name for d in dirs),"unexpected result stage")
stages=[];rounds=[];cols=P["input_columns"]
for spec,d in zip(P["stages"],dirs):
 r=load(d/"result.json");w=load(d/"watchdog.json");rr=r["rounds"]
 need([x["round"] for x in rr]==spec["rounds"] and r["rounds_completed"]==spec["cap"] and r["cached_vectors_loaded"]==cols and r["vectors_materialized_on_restore"]==0,d.name+" rounds/restore")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,P["column_cap"]),d.name+" mode")
 need((r["status"],r["incomplete_reason"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),d.name+" stop")
 for x in rr:need(x["new_columns"]>0 and x["selected_strategy"]=="cold" and x["selected_pivot"]=="rare",d.name+" record");cols+=x["new_columns"];need(x["columns"]==cols,d.name+" recurrence")
 need((r["column_orbits_exposed"],r["dual_support"])==(cols,rr[-1]["dual_support"]),d.name+" census")
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],d.name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),d.name+" pins")
 need(w["elapsed_seconds"]<150 and w["peak_rss_kib"]<LIMIT and all(x["rss_kib"]<LIMIT for x in w["samples"]),d.name+" resources")
 for f,v in (("--round-cap",str(spec["cap"])),("--column-cap",str(P["column_cap"])),("--wall-seconds","120"),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no")):need(arg(w["command"],f)==v,d.name+" "+f)
 need(not any(d.glob("*.tmp")),d.name+" temp")
 stages.append({"stage":d.name,"input_round":spec["rounds"][0]-1,"output_round":spec["rounds"][-1],"input_columns":r["cached_vectors_loaded"],"output_columns":cols,"support":r["dual_support"],"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]});rounds+=rr
need([x["round"] for x in rounds]==list(range(1528,1539)),"global rounds")
blocks=[sum(next(x["watchdog_elapsed_seconds"] for x in stages if x["stage"]==n) for n in b) for b in P["aggregate_blocks"]];need(all(x<540 for x in blocks),"block wall")
def pc(p,r,c,s):
 x=fmt.parse_checkpoint(p);need((x["round"],len(x["columns"]),x["support"],x["target_coefficient"])==(r,c,s,1),"checkpoint header");return x
def ce(a,b,x,y):
 aa=pc(a,*x);bb=pc(b,*y);i=j=0
 while i<len(aa["columns"]):
  need(j<len(bb["columns"]),"checkpoint lost suffix")
  if bb["columns"][j]<aa["columns"][i]:j+=1
  else:need(bb["columns"][j]==aa["columns"][i],"checkpoint omitted inherited");i+=1;j+=1
 return {"input_round":x[0],"output_round":y[0],"preserved":x[1],"new_columns":y[1]-x[1]}
def ve(a,b,x,y):
 with a.open("rb") as f,b.open("rb") as g:
  ah,bh=fmt.vector_header(f,"old"),fmt.vector_header(g,"new");need((ah["count"],bh["count"])==(x[1],y[1]) and ah["provider_fingerprint"]==bh["provider_fingerprint"],"cache header")
  u,v=fmt.vector_record(f,"old"),fmt.vector_record(g,"new");same=extra=0
  while u is not None:
   need(v is not None,"cache lost suffix")
   if v[0]<u[0]:extra+=1;v=fmt.vector_record(g,"new")
   elif v[0]==u[0]:need(v[1]==u[1],"inherited vector changed");same+=1;u=fmt.vector_record(f,"old");v=fmt.vector_record(g,"new")
   else:need(False,"inherited vector omitted")
  while v is not None:extra+=1;v=fmt.vector_record(g,"new")
  need((same,extra)==(x[1],y[1]-x[1]) and f.read(1)==g.read(1)==b"","cache census")
 return {"input_round":x[0],"output_round":y[0],"preserved_byte_identically":same,"new_records":extra,"provider_fingerprint":bh["provider_fingerprint"]}
states=[(P["input_round"],P["input_columns"],P["input_support"])]+[(s["output_round"],s["output_columns"],s["support"]) for s in stages];cps=[ICP]+[d/"checkpoint.bin" for d in dirs];vs=[IV]+[d/"vectors.bin" for d in dirs]
cpedges=[];vedges=[]
for i in range(len(dirs)):cpedges.append(ce(cps[i],cps[i+1],states[i],states[i+1]));vedges.append(ve(vs[i],vs[i+1],states[i],states[i+1]))
replay=load(H/"results_round1538_all_column_replay.json");need(replay["status"]=="PASS_ALL_COLUMNS" and replay["round"]==1538 and replay["columns_replayed"]==cols and replay["verification_failures"]==0 and replay["target_terms"]==2,"replay")
hashes={}
for d in dirs:
 for k,n in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")):hashes[d.name+"_"+k]=sha(d/n)
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1538_CAP2750_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1538_CAP2750_CHAIN","scope":"Accepted r1527 cap2.75m state through exact rounds1528..1538; no r1539 or closure claim.","input":{"round":1527,"columns":P["input_columns"],"support":P["input_support"]},"final":{"round":1538,"columns":cols,"new_columns":cols-P["input_columns"],"support":stages[-1]["support"],"target_coefficient":1},"stage_summaries":stages,"checkpoint_edges":cpedges,"cache_edges":vedges,"resources":{"aggregate_block_watchdog_seconds":blocks,"each_required_less_than":540,"maximum_peak_rss_kib":max(x["peak_rss_kib"] for x in stages),"rss_limit_kib":LIMIT},"all_column_replay":replay,"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH,"input_audit_sha256":P["input_audit_sha256"],"input_manifest_sha256":P["input_manifest_sha256"],"compaction_record_sha256":P["compaction_record_sha256"],"producer_manifest_sha256":P["producer_manifest_sha256"],"replay_sha256":sha(H/"results_round1538_all_column_replay.json")},"verdict_note":"Round1538 is exact and resumable, not a terminal global dual."}
t=H/"results_round1538_chain_audit.json.tmp";t.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(t,H/"results_round1538_chain_audit.json");print(json.dumps(out,sort_keys=True))
