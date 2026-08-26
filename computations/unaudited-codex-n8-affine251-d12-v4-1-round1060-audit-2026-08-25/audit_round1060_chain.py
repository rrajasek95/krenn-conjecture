#!/usr/bin/env python3
"""Independent five-stage no-gap/referee audit through D12 round1060."""
import hashlib, importlib.util, json, math, os
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PRODUCER=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
PROD=PRODUCER/"production_from_round961"; INPUT=PRODUCER/"bound_candidate_v4_1"
FORMAT=ROOT/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCHDOG="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
LIMIT=36*1024*1024
SPECS=[
 ("stage01",961,577645,985,608099,549,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
 ("stage02",985,608099,1008,639552,618,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
 ("stage03",1008,639552,1029,671916,733,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
 ("stage04",1029,671916,1047,704954,766,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
 ("stage05",1047,704954,1060,729800,826,"INCOMPLETE_SEARCH_CAP","ROUND_CAP")]

def need(x,m):
    if not x: raise SystemExit("REJECT: "+m)
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()
def load(p):return json.loads(p.read_text())
def format_module():
    need(sha(FORMAT)=="976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67","format parser pin")
    spec=importlib.util.spec_from_file_location("fmt",FORMAT);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def descend(fmt,oldp,newp,oldn,newn):
    with oldp.open("rb") as old,newp.open("rb") as new:
        oh,nh=fmt.vector_header(old,"old"),fmt.vector_header(new,"new")
        need((oh["count"],nh["count"])==(oldn,newn) and oh["provider_fingerprint"]==nh["provider_fingerprint"],"edge headers")
        a,b=fmt.vector_record(old,"old row"),fmt.vector_record(new,"new row");matched=extras=0
        while a is not None:
            need(b is not None,"lost suffix")
            if b[0]<a[0]:extras+=1;b=fmt.vector_record(new,"new row")
            elif b[0]==a[0]:need(b[1]==a[1],"inherited vector changed");matched+=1;a=fmt.vector_record(old,"old row");b=fmt.vector_record(new,"new row")
            else:need(False,"omitted inherited vector")
        while b is not None:extras+=1;b=fmt.vector_record(new,"new row")
        need(old.read(1)==b"" and new.read(1)==b"","trailing cache bytes")
    need((matched,extras)==(oldn,newn-oldn),"edge census")
    return {"input_records_preserved_byte_identically":matched,"new_records":extras,"input_fingerprint":oh["vector_fingerprint"],"output_fingerprint":nh["vector_fingerprint"],"provider_fingerprint":nh["provider_fingerprint"]}

fmt=format_module(); need(sha(INPUT/"checkpoint.bin")=="2fac10fb7b77f145e67a51a9f6ae4328fa31187d05f8d670fdc9d2564d5592cd","input checkpoint")
need(sha(INPUT/"vectors.bin")=="8bce26efb055cd9ea8aaf3f31b10d149eeff96816a0be58d5fef6f5254c5ca35","input cache")
checkpoints=[fmt.parse_checkpoint(INPUT/"checkpoint.bin")]+[fmt.parse_checkpoint(PROD/s[0]/"checkpoint.bin") for s in SPECS]
headers=[(961,577645,523)]+[(s[3],s[4],s[5]) for s in SPECS]
for cp,h in zip(checkpoints,headers):need((cp["round"],len(cp["columns"]),cp["support"],cp["target_coefficient"])==(*h,1),"checkpoint header/target")
cp_edges=[]
for a,b in zip(checkpoints,checkpoints[1:]):
    aa,bb=set(a["columns"]),set(b["columns"]);need(aa<=bb,"checkpoint descendant")
    cp_edges.append({"input_round":a["round"],"output_round":b["round"],"preserved":len(aa),"new_columns":len(bb-aa)})

rounds=[]; stages=[]; telemetry={}; artifacts={}; native_sum=watch_sum=0.0;max_rss=0
for name,ir,ic,oround,oc,support,status,reason in SPECS:
    d=PROD/name;r=load(d/"result.json");w=load(d/"watchdog.json")
    need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"])==(status,reason,oround,oc,support),name+" terminal")
    need((r["cached_vectors_loaded"],r["vectors_materialized_on_restore"])==(ic,0),name+" resume")
    need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"])==(16,"rare","cold","hierarchical",False),name+" modes")
    need([x["round"] for x in r["rounds"]]==list(range(ir+1,oround+1)),name+" rounds")
    cols=ic
    for x in r["rounds"]:
        need(x["new_columns"]>0 and x["selected_strategy"]=="cold" and x["selected_pivot"]=="rare",name+" record")
        cols+=x["new_columns"];need(x["columns"]==cols,name+" recurrence")
    need(cols==oc and r["rounds"][-1]["dual_support"]==support,name+" final recurrence")
    rounds.extend(r["rounds"]);native_sum+=r["elapsed_seconds"]
    need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],name+" watchdog")
    need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCHDOG),name+" pins")
    need(w["rss_limit_kib"]==LIMIT and w["contract_rss_limit_kib"]==LIMIT and w["peak_rss_kib"]<LIMIT,name+" limits")
    need(w["sample_count"]==len(w["samples"]) and all(x["rss_kib"]<LIMIT for x in w["samples"]),name+" samples")
    need(w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.35,name+" natural exit")
    need(not any((d/(f+".tmp")).exists() for f in ("result.json","checkpoint.bin","vectors.bin","stdout.log","stderr.log")),name+" tmp")
    watch_sum+=w["elapsed_seconds"];max_rss=max(max_rss,w["peak_rss_kib"])
    stages.append({"stage":name,"rounds":[ir+1,oround],"input_columns":ic,"output_columns":oc,"support":support,"result_status":status,"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]})
    for key,file in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")):
        artifacts[name+"_"+key]=sha(d/file)
need([x["round"] for x in rounds]==list(range(962,1061)),"global no-gap rounds")
cols=577645
for x in rounds:cols+=x["new_columns"];need(cols==x["columns"],"global column recurrence")
need(cols==729800 and len(rounds)==99,"global final")
need(abs(watch_sum-478.579028)<1e-6 and watch_sum<540 and max_rss==11883200 and max_rss<LIMIT,"aggregate resource")

paths=[INPUT/"vectors.bin"]+[PROD/s[0]/"vectors.bin" for s in SPECS];counts=[577645]+[s[4] for s in SPECS]
cache_edges=[{"input_round":headers[i][0],"output_round":headers[i+1][0],**descend(fmt,paths[i],paths[i+1],counts[i],counts[i+1])} for i in range(5)]
replay=load(HERE/"results_round1060_all_column_replay.json")
need((replay["status"],replay["round"],replay["columns_replayed"],replay["terms_replayed"],replay["verification_failures"])==("PASS_ALL_COLUMNS",1060,729800,74296977,0),"final replay")
need(artifacts["stage05_result"].startswith("ca3be36a"),"final result pin")
need(artifacts["stage05_checkpoint"]=="1bc0315d" or artifacts["stage05_checkpoint"].startswith("1bc0315d"),"final checkpoint pin")
need(artifacts["stage05_vectors"].startswith("0d71ab7b"),"final cache pin")
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1060_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1060_CHAIN","scope":"Audited round961 input through exact rounds962..1060; no round1061 continuation.","input":{"round":961,"columns":577645,"support":523,"checkpoint_sha256":"2fac10fb7b77f145e67a51a9f6ae4328fa31187d05f8d670fdc9d2564d5592cd","vectors_sha256":"8bce26efb055cd9ea8aaf3f31b10d149eeff96816a0be58d5fef6f5254c5ca35"},"final":{"round":1060,"columns":729800,"new_columns":152155,"support":826,"candidate_target_coefficient":1},"stage_summaries":stages,"checkpoint_edges":cp_edges,"cache_edges":cache_edges,"resource":{"watchdog_elapsed_seconds_sum":watch_sum,"native_elapsed_seconds_sum":native_sum,"required_sum_less_than":540,"maximum_peak_rss_kib":max_rss,"rss_limit_kib":LIMIT},"all_column_replay":replay,"artifact_sha256":artifacts,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCHDOG,"replay_sha256":sha(HERE/"results_round1060_all_column_replay.json")},"verdict_note":"Round1060 remains INCOMPLETE_SEARCH_CAP/ROUND_CAP; this is exact resumable state, not a terminal global dual."}
tmp=HERE/"results_round1060_chain_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_round1060_chain_audit.json")
