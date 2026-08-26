#!/usr/bin/env python3
"""Small-file-only audit of landed r1464→r1484 production stages."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];PLAN=json.loads((HERE/"AUDIT_PLAN.json").read_text());PROD=REPO/PLAN["production_root"]
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59";BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048";WATCH="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97";LIMIT=36*1024*1024
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
need(sha(REPO/PLAN["input_manifest"])==PLAN["input_manifest_sha256"],"input manifest");need(sha(REPO/PLAN["input_audit"])==PLAN["input_audit_sha256"],"input audit");need(sha(REPO/PLAN["compaction_record"])==PLAN["compaction_record_sha256"],"compaction record")
stages=[]
for d in sorted((p for p in PROD.glob("stage[0-9][0-9]") if p.is_dir()),key=lambda p:int(p.name[5:])):
 if not (d/"result.json").is_file() or not (d/"watchdog.json").is_file():continue
 need(not any(d.glob("*.tmp")),d.name+" temporary outputs");r=load(d/"result.json");w=load(d/"watchdog.json")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,PLAN["column_cap"]),d.name+" mode")
 need(r["vectors_materialized_on_restore"]==0,d.name+" restore");need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],d.name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),d.name+" pins");need(w["peak_rss_kib"]<LIMIT and w["elapsed_seconds"]<115,d.name+" resources")
 rr=r["rounds"];need(rr and [x["round"] for x in rr]==list(range(rr[0]["round"],r["rounds_completed"]+1)),d.name+" local no-gap")
 stages.append({"stage":d.name,"first_round":rr[0]["round"],"last_round":rr[-1]["round"],"input_columns":r["cached_vectors_loaded"],"output_columns":r["column_orbits_exposed"],"support":r["dual_support"],"status":r["status"],"reason":r["incomplete_reason"],"elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"],"result_sha256":sha(d/"result.json"),"watchdog_sha256":sha(d/"watchdog.json")})
need(stages,"no terminal stage");need([s["stage"] for s in stages]==[f"stage{i:02d}" for i in range(1,len(stages)+1)],"stage numbering")
nr=PLAN["input_round"]+1;cols=PLAN["input_columns"]
for s in stages:need(s["first_round"]==nr and s["input_columns"]==cols,"global continuity");nr=s["last_round"]+1;cols=s["output_columns"];need(s["last_round"]<=PLAN["target_round"],"past target")
if stages[-1]["last_round"]==PLAN["target_round"]:need((stages[-1]["status"],stages[-1]["reason"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),"terminal stop")
status="PASS_TERMINAL_METADATA" if stages[-1]["last_round"]==PLAN["target_round"] else "PASS_PARTIAL_METADATA"
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1484_CAP2500_LANDED_METADATA_V1","status":status,"accepted_through_round":stages[-1]["last_round"],"next_expected_round":nr,"accepted_columns":cols,"stages":stages,"large_io_performed":False,"production_final_state_claimed":status=="PASS_TERMINAL_METADATA"}
tmp=HERE/"results_landed_metadata_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_landed_metadata_audit.json");print(json.dumps(out,sort_keys=True))
