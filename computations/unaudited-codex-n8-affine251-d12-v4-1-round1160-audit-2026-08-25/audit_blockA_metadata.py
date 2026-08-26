#!/usr/bin/env python3
"""Cheap metadata-only pre-audit while round1160 production remains active."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROD=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1061_portfolio"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59";BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048";WATCHDOG="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97";LIMIT=36*1024*1024
SPECS=[("stage01",1061,731908,1077,764938,908),("stage02",1077,764938,1092,796858,852),("stage03",1092,796858,1107,830076,974),("stage04",1107,830076,1122,867821,1109),("stage05",1122,867821,1137,904967,991)]
def need(x,m):
    if not x:raise SystemExit("REJECT: "+m)
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def load(p):return json.loads(p.read_text())
rounds=[];stages=[];wall=0;peak=0;hashes={}
for name,ir,ic,orr,oc,support in SPECS:
 d=PROD/name;r=load(d/"result.json");w=load(d/"watchdog.json")
 need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"])==("INCOMPLETE_RESOURCE_GATE","WALL_CAP",orr,oc,support),name+" result")
 need((r["cached_vectors_loaded"],r["vectors_materialized_on_restore"])==(ic,0),name+" resume")
 need([x["round"] for x in r["rounds"]]==list(range(ir+1,orr+1)),name+" rounds")
 cols=ic
 for x in r["rounds"]:cols+=x["new_columns"];need(cols==x["columns"] and x["new_columns"]>0,name+" recurrence")
 need(cols==oc and r["rounds"][-1]["dual_support"]==support,name+" terminal")
 rounds+=r["rounds"]
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCHDOG),name+" pins")
 need(w["rss_limit_kib"]==LIMIT and w["peak_rss_kib"]<LIMIT and all(s["rss_kib"]<LIMIT for s in w["samples"]),name+" RSS")
 need(w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.35,name+" telemetry")
 need(not any((d/(f+".tmp")).exists() for f in ("result.json","checkpoint.bin","vectors.bin","stdout.log","stderr.log")),name+" tmp")
 wall+=w["elapsed_seconds"];peak=max(peak,w["peak_rss_kib"]);stages.append({"stage":name,"rounds":[ir+1,orr],"input_columns":ic,"output_columns":oc,"support":support,"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]})
 for k,f in (("result","result.json"),("watchdog","watchdog.json"),("stderr","stderr.log")):hashes[name+"_"+k]=sha(d/f)
need([x["round"] for x in rounds]==list(range(1062,1138)),"BlockA no-gap")
cols=731908
for x in rounds:cols+=x["new_columns"];need(cols==x["columns"],"BlockA global recurrence")
need(cols==904967 and abs(wall-509.806545)<1e-6 and peak==12500592,"BlockA aggregate")
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1160_BLOCKA_METADATA_AUDIT_V1","status":"PASS_BLOCKA_METADATA_NO_GAP_TELEMETRY","scope":"Small JSON/log audit only; checkpoint/cache hashing and descendant scans explicitly held during active production.","rounds":[1062,1137],"records":76,"input_columns":731908,"output_columns":904967,"stages":stages,"watchdog_elapsed_seconds_sum":wall,"maximum_peak_rss_kib":peak,"rss_limit_kib":LIMIT,"artifact_sha256":hashes,"large_io_performed":False,"production_final_state_claimed":False}
tmp=HERE/"results_blockA_metadata_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_blockA_metadata_audit.json")
