#!/usr/bin/env python3
"""Small-file-only audit of landed r1538→r1550 cap-2.75m stages."""
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];P=json.loads((H/"AUDIT_PLAN.json").read_text());ROOT=R/P["production_root"]
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
for k,n in (("input_audit_sha256","input_audit"),("input_manifest_sha256","input_manifest"),("compaction_record_sha256","compaction_record")):need(sha(R/P[n])==P[k],k)
stages=[];cols=P["input_columns"]
for spec in P["stages"]:
 d=ROOT/spec["name"]
 if not (d/"result.json").is_file() or not (d/"watchdog.json").is_file():break
 need(not any(d.glob("*.tmp")),spec["name"]+" temp")
 r=load(d/"result.json");w=load(d/"watchdog.json");rr=r["rounds"]
 need([x["round"] for x in rr]==spec["rounds"] and r["rounds_completed"]==spec["cap"] and r["cached_vectors_loaded"]==cols and r["vectors_materialized_on_restore"]==0,spec["name"]+" rounds/restore")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,P["column_cap"]),spec["name"]+" mode")
 need((r["status"],r["incomplete_reason"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),spec["name"]+" stop")
 for x in rr:need(x["new_columns"]>0 and x["selected_strategy"]=="cold" and x["selected_pivot"]=="rare",spec["name"]+" record");cols+=x["new_columns"];need(x["columns"]==cols,spec["name"]+" recurrence")
 need((r["column_orbits_exposed"],r["dual_support"])==(cols,rr[-1]["dual_support"]),spec["name"]+" census")
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],spec["name"]+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),spec["name"]+" pins")
 need(w["elapsed_seconds"]<150 and w["peak_rss_kib"]<LIMIT and all(x["rss_kib"]<LIMIT for x in w["samples"]),spec["name"]+" resources")
 for f,v in (("--round-cap",str(spec["cap"])),("--column-cap",str(P["column_cap"])),("--wall-seconds","120"),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no")):need(arg(w["command"],f)==v,spec["name"]+" "+f)
 stages.append({"stage":spec["name"],"first_round":spec["rounds"][0],"last_round":spec["rounds"][-1],"input_columns":r["cached_vectors_loaded"],"output_columns":cols,"support":r["dual_support"],"elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"],"result_sha256":sha(d/"result.json"),"watchdog_sha256":sha(d/"watchdog.json")})
actual={d.name for d in ROOT.iterdir() if d.is_dir() and (d/"result.json").is_file()} if ROOT.exists() else set();need(actual==set(s["stage"] for s in stages),"unexpected result stage")
blocks=[]
for block in P["aggregate_blocks"]:
 vals=[next((s["elapsed_seconds"] for s in stages if s["stage"]==n),None) for n in block]
 if all(x is not None for x in vals):blocks.append(sum(vals))
need(all(x<540 for x in blocks),"block wall")
status="PASS_TERMINAL_METADATA" if stages and stages[-1]["last_round"]==P["target_round"] else "PASS_PARTIAL_METADATA"
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1550_CAP2750_METADATA_V1","status":status,"accepted_through_round":stages[-1]["last_round"] if stages else P["input_round"],"accepted_columns":cols,"stages":stages,"completed_block_seconds":blocks,"large_io_performed":False,"production_final_state_claimed":status=="PASS_TERMINAL_METADATA"}
t=H/"results_landed_metadata_audit.json.tmp";t.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(t,H/"results_landed_metadata_audit.json");print(json.dumps(out,sort_keys=True))
