#!/usr/bin/env python3
"""Independent exact seven-stage audit from accepted round1061 through round1160."""
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PARENT=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25";PROD=PARENT/"production_from_round1061_portfolio"
INPUTPKG=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25";INPUT=INPUTPKG/"portfolio"
FORMAT=ROOT/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59";BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048";WATCH="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97";LIMIT=36*1024*1024
SPECS=[("stage01",1061,731908,1077,764938,908,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage02",1077,764938,1092,796858,852,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage03",1092,796858,1107,830076,974,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage04",1107,830076,1122,867821,1109,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage05",1122,867821,1137,904967,991,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage06",1137,904967,1151,939177,1055,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage07",1151,939177,1160,959506,990,"INCOMPLETE_SEARCH_CAP","ROUND_CAP")]
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
need(sha(INPUTPKG/"MANIFEST.sha256").startswith("ff434b07"),"input manifest pin")
need(sha(INPUT/"checkpoint.bin")=="9927bfa11b6505d106348ebdd76c7f95714947970535a2bccde3708ea90c57a4","input checkpoint")
need(sha(INPUT/"vectors.bin")=="acc0f960b0021b0adcd4dcc0efcf4141e1ae51bf54b30332316b33311eeacd1d","input vectors")
ia=load(INPUTPKG/"results_round1061_audit.json");need(ia["status"].startswith("PASS") and ia["output_checkpoint_sha256"].startswith("9927bfa1") and ia["output_vectors_sha256"].startswith("acc0f960"),"input audit")
need(sha(FORMAT)=="976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67","format parser")
sp=importlib.util.spec_from_file_location("fmt",FORMAT);fmt=importlib.util.module_from_spec(sp);sp.loader.exec_module(fmt)
def edge(oldp,newp,oldn,newn):
 with oldp.open("rb") as a,newp.open("rb") as b:
  ah,bh=fmt.vector_header(a,"old"),fmt.vector_header(b,"new");need((ah["count"],bh["count"])==(oldn,newn) and ah["provider_fingerprint"]==bh["provider_fingerprint"],"cache headers")
  x,y=fmt.vector_record(a,"old record"),fmt.vector_record(b,"new record");matched=extra=0
  while x is not None:
   need(y is not None,"lost cache suffix")
   if y[0]<x[0]:extra+=1;y=fmt.vector_record(b,"new record")
   elif y[0]==x[0]:need(y[1]==x[1],"inherited vector changed");matched+=1;x=fmt.vector_record(a,"old record");y=fmt.vector_record(b,"new record")
   else:need(False,"inherited vector omitted")
  while y is not None:extra+=1;y=fmt.vector_record(b,"new record")
  need(a.read(1)==b"" and b.read(1)==b"","cache trailing")
 need((matched,extra)==(oldn,newn-oldn),"cache edge census")
 return {"preserved_byte_identically":matched,"new_records":extra,"input_fingerprint":ah["vector_fingerprint"],"output_fingerprint":bh["vector_fingerprint"],"provider_fingerprint":bh["provider_fingerprint"]}
checkpoints=[fmt.parse_checkpoint(INPUT/"checkpoint.bin")]+[fmt.parse_checkpoint(PROD/s[0]/"checkpoint.bin") for s in SPECS];headers=[(1061,731908,785)]+[(s[3],s[4],s[5]) for s in SPECS]
for c,h in zip(checkpoints,headers):need((c["round"],len(c["columns"]),c["support"],c["target_coefficient"])==(*h,1),"checkpoint header")
cpedges=[]
for a,b in zip(checkpoints,checkpoints[1:]):
 aa,bb=set(a["columns"]),set(b["columns"]);need(aa<=bb,"checkpoint descendant");cpedges.append({"input_round":a["round"],"output_round":b["round"],"preserved":len(aa),"new_columns":len(bb-aa)})
rounds=[];stages=[];hashes={};walls=[];maxrss=0
for name,ir,ic,orr,oc,sup,status,reason in SPECS:
 d=PROD/name;r=load(d/"result.json");w=load(d/"watchdog.json")
 need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"],r["cached_vectors_loaded"],r["vectors_materialized_on_restore"])==(status,reason,orr,oc,sup,ic,0),name+" result")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"])==(16,"rare","cold","hierarchical",False),name+" mode")
 need([x["round"] for x in r["rounds"]]==list(range(ir+1,orr+1)),name+" no gap");cols=ic
 for x in r["rounds"]:need(x["new_columns"]>0 and x["selected_pivot"]=="rare" and x["selected_strategy"]=="cold",name+" record");cols+=x["new_columns"];need(cols==x["columns"],name+" recurrence")
 need(cols==oc and r["rounds"][-1]["dual_support"]==sup,name+" final");rounds+=r["rounds"]
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),name+" pins")
 need(w["rss_limit_kib"]==LIMIT and w["peak_rss_kib"]<LIMIT and all(s["rss_kib"]<LIMIT for s in w["samples"]),name+" RSS")
 need(w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.35,name+" telemetry")
 need(not any((d/(f+".tmp")).exists() for f in ("result.json","checkpoint.bin","vectors.bin","stdout.log","stderr.log")),name+" tmp")
 walls.append(w["elapsed_seconds"]);maxrss=max(maxrss,w["peak_rss_kib"]);stages.append({"stage":name,"rounds":[ir+1,orr],"input_columns":ic,"output_columns":oc,"support":sup,"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]})
 for k,f in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")):hashes[name+"_"+k]=sha(d/f)
need([x["round"] for x in rounds]==list(range(1062,1161)),"global rounds");cols=731908
for x in rounds:cols+=x["new_columns"];need(cols==x["columns"],"global columns")
need(cols==959506 and len(rounds)==99,"global final")
blockA=sum(walls[:5]);blockB=sum(walls[5:]);need(abs(blockA-509.806545)<1e-6 and blockA<540 and blockB<540 and maxrss==13165296,"resource blocks")
paths=[INPUT/"vectors.bin"]+[PROD/s[0]/"vectors.bin" for s in SPECS];counts=[731908]+[s[4] for s in SPECS]
edges=[{"input_round":headers[i][0],"output_round":headers[i+1][0],**edge(paths[i],paths[i+1],counts[i],counts[i+1])} for i in range(7)]
replay=load(HERE/"results_round1160_all_column_replay.json");need((replay["status"],replay["round"],replay["columns_replayed"],replay["terms_replayed"],replay["verification_failures"])==("PASS_ALL_COLUMNS",1160,959506,97784365,0),"final replay")
need(hashes["stage07_result"].startswith("0022c43b") and hashes["stage07_checkpoint"].startswith("23d91d21") and hashes["stage07_watchdog"].startswith("f6b81fbf"),"final pins")
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1160_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1160_CHAIN","scope":"Accepted round1061 portfolio through exact rounds1062..1160; no round1161 continuation.","input":{"round":1061,"columns":731908,"support":785,"checkpoint_sha256":"9927bfa11b6505d106348ebdd76c7f95714947970535a2bccde3708ea90c57a4","vectors_sha256":"acc0f960b0021b0adcd4dcc0efcf4141e1ae51bf54b30332316b33311eeacd1d"},"final":{"round":1160,"columns":959506,"new_columns":227598,"support":990,"target_coefficient":1},"stage_summaries":stages,"checkpoint_edges":cpedges,"cache_edges":edges,"resources":{"blockA_watchdog_seconds":blockA,"blockB_watchdog_seconds":blockB,"each_block_required_less_than":540,"maximum_peak_rss_kib":maxrss,"rss_limit_kib":LIMIT},"all_column_replay":replay,"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH,"input_manifest_sha256":sha(INPUTPKG/"MANIFEST.sha256"),"replay_sha256":sha(HERE/"results_round1160_all_column_replay.json")},"verdict_note":"Round1160 remains INCOMPLETE_SEARCH_CAP/ROUND_CAP: exact resumable state, not a terminal global dual."}
tmp=HERE/"results_round1160_chain_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_round1160_chain_audit.json")
