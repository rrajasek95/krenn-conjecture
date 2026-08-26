#!/usr/bin/env python3
"""Independent exact descendant/cache audit of the terminal r1448→r1463 chain."""
from __future__ import annotations
import hashlib, importlib.util, json, os
from pathlib import Path

HERE=Path(__file__).resolve().parent; REPO=HERE.parents[1]
PLAN=json.loads((HERE/"AUDIT_PLAN.json").read_text()); PROD=REPO/PLAN["production_root"]
INPUT_CP=REPO/PLAN["input_checkpoint"]; INPUT_VEC=REPO/PLAN["input_vectors"]
FORMAT=REPO/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCH="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
LIMIT=36*1024*1024
def need(x,m):
 if not x: raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""): h.update(b)
 return h.hexdigest()
def load(p): return json.loads(p.read_text())
def arg(command,flag):
 need(command.count(flag)==1,"command flag "+flag); i=command.index(flag); need(i+1<len(command),"command value "+flag); return command[i+1]

need(sha(REPO/PLAN["input_manifest"])==PLAN["input_manifest_sha256"],"input manifest")
need(sha(REPO/PLAN["input_audit"])==PLAN["input_audit_sha256"],"input audit")
need(sha(REPO/PLAN["compaction_record"])==PLAN["compaction_record_sha256"],"compaction record")
need(sha(INPUT_CP)==PLAN["input_checkpoint_sha256"],"input checkpoint")
need(sha(INPUT_VEC)==PLAN["input_vectors_sha256"],"input vectors")
ia=load(REPO/PLAN["input_audit"]); need(ia["status"]=="PASS_EXACT_CAP2000_TO_CAP2250_EQUIVALENCE" and ia["checkpoint_sha256"]==PLAN["input_checkpoint_sha256"] and ia["vectors_sha256"]==PLAN["input_vectors_sha256"],"input audit contents")
need(sha(FORMAT)=="976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67","format parser")
sp=importlib.util.spec_from_file_location("fmt",FORMAT);fmt=importlib.util.module_from_spec(sp);sp.loader.exec_module(fmt)

dirs=sorted((p for p in PROD.glob("stage[0-9][0-9]") if (p/"result.json").is_file()),key=lambda p:int(p.name[5:]))
need(dirs and [d.name for d in dirs]==[f"stage{i:02d}" for i in range(1,len(dirs)+1)],"stage set")
stage_data=[]; rounds=[]; cols=PLAN["input_columns"]
for index,d in enumerate(dirs):
 r=load(d/"result.json");w=load(d/"watchdog.json");rr=r["rounds"]
 need(rr and rr[0]["round"]==(PLAN["input_round"]+1 if index==0 else stage_data[-1]["output_round"]+1),d.name+" first round")
 need([x["round"] for x in rr]==list(range(rr[0]["round"],rr[-1]["round"]+1)),d.name+" local rounds")
 need(r["rounds_completed"]==rr[-1]["round"] and r["cached_vectors_loaded"]==cols and r["vectors_materialized_on_restore"]==0,d.name+" restore census")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,PLAN["column_cap"]),d.name+" mode")
 expected_status=("INCOMPLETE_SEARCH_CAP","ROUND_CAP") if rr[-1]["round"]==PLAN["target_round"] else ("INCOMPLETE_RESOURCE_GATE","WALL_CAP")
 need((r["status"],r["incomplete_reason"])==expected_status,d.name+" status")
 for x in rr:
  need(x["new_columns"]>0 and x["selected_strategy"]=="cold" and x["selected_pivot"]=="rare",d.name+" record")
  cols+=x["new_columns"];need(x["columns"]==cols,d.name+" column recurrence")
 need((r["column_orbits_exposed"],r["dual_support"])==(cols,rr[-1]["dual_support"]),d.name+" terminal census")
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],d.name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),d.name+" pins")
 need(w["rss_limit_kib"]==LIMIT and w["peak_rss_kib"]<LIMIT and all(s["rss_kib"]<LIMIT for s in w["samples"]),d.name+" RSS")
 need(w["elapsed_seconds"]<110 and w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.5,d.name+" telemetry")
 for flag,value in (("--round-cap",str(PLAN["target_round"])),("--column-cap",str(PLAN["column_cap"])),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no")):
  need(arg(w["command"],flag)==value,d.name+" command "+flag)
 need(not any(d.glob("*.tmp")),d.name+" temporary output")
 stage_data.append({"stage":d.name,"input_round":rr[0]["round"]-1,"output_round":rr[-1]["round"],"input_columns":r["cached_vectors_loaded"],"output_columns":cols,"support":r["dual_support"],"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]})
 rounds+=rr
need([x["round"] for x in rounds]==list(range(PLAN["input_round"]+1,PLAN["target_round"]+1)),"global no-gap rounds")
need(stage_data[-1]["output_round"]==PLAN["target_round"],"terminal round")
need(sum(s["watchdog_elapsed_seconds"] for s in stage_data)<540,"aggregate wall budget")

def parse_checkpoint(path,round_number,columns,support):
 c=fmt.parse_checkpoint(path);need((c["round"],len(c["columns"]),c["support"],c["target_coefficient"])==(round_number,columns,support,1),"checkpoint header "+str(path));return c
def checkpoint_edge(oldp,newp,ir,ic,isup,orr,oc,osup):
 a=parse_checkpoint(oldp,ir,ic,isup);b=parse_checkpoint(newp,orr,oc,osup);i=j=0
 while i<len(a["columns"]):
  need(j<len(b["columns"]),"checkpoint omitted inherited column")
  if b["columns"][j]<a["columns"][i]: j+=1
  else: need(b["columns"][j]==a["columns"][i],"checkpoint inherited column mismatch");i+=1;j+=1
 return {"input_round":ir,"output_round":orr,"preserved":ic,"new_columns":oc-ic}
def vector_edge(oldp,newp,oldn,newn,ir,orr):
 with oldp.open("rb") as a,newp.open("rb") as b:
  ah,bh=fmt.vector_header(a,"old"),fmt.vector_header(b,"new");need((ah["count"],bh["count"])==(oldn,newn) and ah["provider_fingerprint"]==bh["provider_fingerprint"],"cache headers")
  x,y=fmt.vector_record(a,"old record"),fmt.vector_record(b,"new record");matched=extra=0
  while x is not None:
   need(y is not None,"lost cache suffix")
   if y[0]<x[0]:extra+=1;y=fmt.vector_record(b,"new record")
   elif y[0]==x[0]:need(y[1]==x[1],"inherited vector changed");matched+=1;x=fmt.vector_record(a,"old record");y=fmt.vector_record(b,"new record")
   else:need(False,"inherited vector omitted")
  while y is not None:extra+=1;y=fmt.vector_record(b,"new record")
  need(a.read(1)==b"" and b.read(1)==b"","cache trailing bytes")
 need((matched,extra)==(oldn,newn-oldn),"cache edge census")
 return {"input_round":ir,"output_round":orr,"preserved_byte_identically":matched,"new_records":extra,"provider_fingerprint":bh["provider_fingerprint"],"input_vector_fingerprint":ah["vector_fingerprint"],"output_vector_fingerprint":bh["vector_fingerprint"]}

cp_paths=[INPUT_CP]+[d/"checkpoint.bin" for d in dirs];vec_paths=[INPUT_VEC]+[d/"vectors.bin" for d in dirs]
states=[(PLAN["input_round"],PLAN["input_columns"],PLAN["input_support"])]+[(s["output_round"],s["output_columns"],s["support"]) for s in stage_data]
cp_edges=[];cache_edges=[]
for i in range(len(dirs)):
 cp_edges.append(checkpoint_edge(cp_paths[i],cp_paths[i+1],*states[i],*states[i+1]))
 cache_edges.append(vector_edge(vec_paths[i],vec_paths[i+1],states[i][1],states[i+1][1],states[i][0],states[i+1][0]))

replay=load(HERE/"results_round1463_all_column_replay.json")
need(replay["status"]=="PASS_ALL_COLUMNS" and replay["round"]==1463 and replay["columns_replayed"]==cols and replay["verification_failures"]==0 and replay["target_terms"]==2,"final all-column replay")
hashes={}
for d in dirs:
 for key,name in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")):hashes[d.name+"_"+key]=sha(d/name)
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1463_CAP2250_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1463_CAP2250_CHAIN","scope":"Accepted cap-equivalent r1448 state through exact rounds1449..1463; no round1464 continuation and no closure claim.","input":{"round":PLAN["input_round"],"columns":PLAN["input_columns"],"support":PLAN["input_support"],"checkpoint_sha256":PLAN["input_checkpoint_sha256"],"vectors_sha256":PLAN["input_vectors_sha256"]},"final":{"round":1463,"columns":cols,"new_columns":cols-PLAN["input_columns"],"support":stage_data[-1]["support"],"target_coefficient":1},"stage_summaries":stage_data,"checkpoint_edges":cp_edges,"cache_edges":cache_edges,"resources":{"aggregate_watchdog_seconds":sum(s["watchdog_elapsed_seconds"] for s in stage_data),"required_less_than":540,"maximum_peak_rss_kib":max(s["peak_rss_kib"] for s in stage_data),"rss_limit_kib":LIMIT},"all_column_replay":replay,"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH,"input_manifest_sha256":PLAN["input_manifest_sha256"],"input_audit_sha256":PLAN["input_audit_sha256"],"compaction_record_sha256":PLAN["compaction_record_sha256"],"replay_sha256":sha(HERE/"results_round1463_all_column_replay.json")},"verdict_note":"Round1463 is an exact resumable ROUND_CAP state, not a terminal global dual."}
tmp=HERE/"results_round1463_chain_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_round1463_chain_audit.json")
print(json.dumps(out,sort_keys=True))
