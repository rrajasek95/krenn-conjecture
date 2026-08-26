#!/usr/bin/env python3
"""Small-file-only referee for landed r1524→r1538 production stages."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
P=json.loads((HERE/"AUDIT_PLAN.json").read_text());PROD=REPO/P["production_root"]
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCH="48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522"
LIMIT=36*1024*1024
CAPS={n:1526+2*i for i,n in enumerate(P["accepted_stage_dirs"])}
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def arg(c,f):need(c.count(f)==1,"command flag "+f);return c[c.index(f)+1]
need(sha(REPO/P["input_manifest"])==P["input_manifest_sha256"],"input manifest")
need(sha(REPO/P["input_audit"])==P["input_audit_sha256"],"input audit")
need(sha(REPO/P["compaction_record"])==P["compaction_record_sha256"],"compaction record")
stages=[];nr=P["input_round"]+1;cols=P["input_columns"]
for name in P["accepted_stage_dirs"]:
 d=PROD/name
 if not (d/"result.json").is_file() or not (d/"watchdog.json").is_file():break
 need(not any(d.glob("*.tmp")),name+" temporary outputs")
 r=load(d/"result.json");w=load(d/"watchdog.json");rr=r["rounds"]
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,P["column_cap"]),name+" mode")
 need(r["vectors_materialized_on_restore"]==0 and r["cached_vectors_loaded"]==cols,name+" restore")
 need(rr and [x["round"] for x in rr]==[nr,nr+1] and rr[-1]["round"]==CAPS[name],name+" exact two rounds")
 need((r["status"],r["incomplete_reason"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),name+" stop")
 for x in rr:
  need(x["new_columns"]>0 and x["selected_strategy"]=="cold" and x["selected_pivot"]=="rare",name+" record")
  cols+=x["new_columns"];need(x["columns"]==cols,name+" recurrence")
 need((r["column_orbits_exposed"],r["dual_support"])==(cols,rr[-1]["dual_support"]),name+" census")
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),name+" pins")
 need(w["peak_rss_kib"]<LIMIT and w["elapsed_seconds"]<150 and all(x["rss_kib"]<LIMIT for x in w["samples"]),name+" resources")
 need(w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.5,name+" telemetry")
 for f,v in (("--round-cap",str(CAPS[name])),("--column-cap",str(P["column_cap"])),("--wall-seconds","120"),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no")):
  need(arg(w["command"],f)==v,name+" command "+f)
 stages.append({"stage":name,"first_round":nr,"last_round":nr+1,"input_columns":r["cached_vectors_loaded"],"output_columns":cols,"support":r["dual_support"],"elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"],"result_sha256":sha(d/"result.json"),"watchdog_sha256":sha(d/"watchdog.json")})
 nr+=2
need(stages,"no terminal stage")
actual={d.name for d in PROD.iterdir() if d.is_dir() and (d/"result.json").is_file()}
need(actual==set(s["stage"] for s in stages),"unexpected result-bearing stage")
blocks=[]
for block in P["aggregate_blocks"]:
 vals=[next((s["elapsed_seconds"] for s in stages if s["stage"]==n),None) for n in block]
 if all(v is not None for v in vals):blocks.append(sum(vals))
need(all(x<540 for x in blocks),"completed block wall")
status="PASS_TERMINAL_METADATA" if stages[-1]["last_round"]==P["target_round"] else "PASS_PARTIAL_METADATA"
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1538_CAP2500_LANDED_METADATA_V1","status":status,"accepted_through_round":stages[-1]["last_round"],"next_expected_round":nr,"accepted_columns":cols,"stages":stages,"completed_block_seconds":blocks,"large_io_performed":False,"production_final_state_claimed":status=="PASS_TERMINAL_METADATA"}
tmp=HERE/"results_landed_metadata_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_landed_metadata_audit.json");print(json.dumps(out,sort_keys=True))
