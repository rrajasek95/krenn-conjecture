#!/usr/bin/env python3
"""Independent exact three-stage audit from accepted round1343 through round1362."""
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PARENT=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"; PROD=PARENT/"production_from_round1343_cap1750"
INPUTPKG=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1343-cap1750-gate-2026-08-25"; INPUT=INPUTPKG/"cap1750_candidate"
FORMAT=ROOT/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"; BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"; WATCH="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"; LIMIT=36*1024*1024
SPECS=[("stage01",1343,1496171,1350,1526329,2117,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage02",1350,1526329,1356,1554959,2214,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),("stage03",1356,1554959,1362,1582672,2043,"INCOMPLETE_SEARCH_CAP","ROUND_CAP")]
def need(x,m):
 if not x: raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""): h.update(b)
 return h.hexdigest()
def load(p): return json.loads(p.read_text())
need(sha(INPUTPKG/"MANIFEST.sha256")=="c07168d65ba9caa604bf38235b4ff9f5442b217fd82934c84f18f4f0c9665e9b","input manifest")
need(sha(INPUT/"checkpoint.bin")=="d2dbdee814cecca8f8528d84d2f386d3f042a54b62039a0350a834b5a1949dcf","input checkpoint")
need(sha(INPUT/"vectors.bin")=="d5517dfdc00cb7c2e0844b2459385576dd84211eceebe3a0cb94815a1cd7a2c6","input vectors")
ia=load(INPUTPKG/"results_round1343_cap_audit.json"); need(ia["status"].startswith("PASS") and ia["checkpoint_sha256"].startswith("d2dbdee8") and ia["vectors_sha256"].startswith("d5517dfd"),"input audit")
need(sha(FORMAT)=="976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67","format parser")
sp=importlib.util.spec_from_file_location("fmt",FORMAT); fmt=importlib.util.module_from_spec(sp); sp.loader.exec_module(fmt)
def edge(oldp,newp,oldn,newn):
 with oldp.open("rb") as a,newp.open("rb") as b:
  ah,bh=fmt.vector_header(a,"old"),fmt.vector_header(b,"new"); need((ah["count"],bh["count"])==(oldn,newn) and ah["provider_fingerprint"]==bh["provider_fingerprint"],"cache headers")
  x,y=fmt.vector_record(a,"old record"),fmt.vector_record(b,"new record"); matched=extra=0
  while x is not None:
   need(y is not None,"lost cache suffix")
   if y[0]<x[0]: extra+=1; y=fmt.vector_record(b,"new record")
   elif y[0]==x[0]: need(y[1]==x[1],"inherited vector changed"); matched+=1; x=fmt.vector_record(a,"old record"); y=fmt.vector_record(b,"new record")
   else: need(False,"inherited vector omitted")
  while y is not None: extra+=1; y=fmt.vector_record(b,"new record")
  need(a.read(1)==b"" and b.read(1)==b"","cache trailing")
 need((matched,extra)==(oldn,newn-oldn),"cache edge census")
 return {"preserved_byte_identically":matched,"new_records":extra,"input_fingerprint":ah["vector_fingerprint"],"output_fingerprint":bh["vector_fingerprint"],"provider_fingerprint":bh["provider_fingerprint"]}
checkpoints=[fmt.parse_checkpoint(INPUT/"checkpoint.bin")]+[fmt.parse_checkpoint(PROD/s[0]/"checkpoint.bin") for s in SPECS]; headers=[(1343,1496171,1949)]+[(s[3],s[4],s[5]) for s in SPECS]
for c,h in zip(checkpoints,headers): need((c["round"],len(c["columns"]),c["support"],c["target_coefficient"])==(*h,1),"checkpoint header")
cpedges=[]
for a,b in zip(checkpoints,checkpoints[1:]):
 aa,bb=set(a["columns"]),set(b["columns"]); need(aa<=bb,"checkpoint descendant"); cpedges.append({"input_round":a["round"],"output_round":b["round"],"preserved":len(aa),"new_columns":len(bb-aa)})
rounds=[]; stages=[]; hashes={}; walls=[]; maxrss=0
for name,ir,ic,orr,oc,sup,status,reason in SPECS:
 d=PROD/name; r=load(d/"result.json"); w=load(d/"watchdog.json")
 need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"],r["cached_vectors_loaded"],r["vectors_materialized_on_restore"])==(status,reason,orr,oc,sup,ic,0),name+" result")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,1750000),name+" mode")
 need([x["round"] for x in r["rounds"]]==list(range(ir+1,orr+1)),name+" no gap"); cols=ic
 for x in r["rounds"]: need(x["new_columns"]>0 and x["selected_pivot"]=="rare" and x["selected_strategy"]=="cold",name+" record"); cols+=x["new_columns"]; need(cols==x["columns"],name+" recurrence")
 need(cols==oc and r["rounds"][-1]["dual_support"]==sup,name+" final"); rounds+=r["rounds"]
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),name+" pins")
 need(w["rss_limit_kib"]==LIMIT and w["peak_rss_kib"]<LIMIT and all(s["rss_kib"]<LIMIT for s in w["samples"]),name+" RSS")
 # Natural child exit plus atomic log/telemetry finalization can span the next
 # poll boundary.  Require the frozen last sample and at most two 0.25 s polls.
 need(w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.5,name+" telemetry")
 need(not any((d/(f+".tmp")).exists() for f in ("result.json","checkpoint.bin","vectors.bin","stdout.log","stderr.log")),name+" tmp")
 walls.append(w["elapsed_seconds"]); maxrss=max(maxrss,w["peak_rss_kib"]); stages.append({"stage":name,"rounds":[ir+1,orr],"input_columns":ic,"output_columns":oc,"support":sup,"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]})
 for k,f in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")): hashes[name+"_"+k]=sha(d/f)
need([x["round"] for x in rounds]==list(range(1344,1363)),"global rounds"); cols=1496171
for x in rounds: cols+=x["new_columns"]; need(cols==x["columns"],"global columns")
need(cols==1582672 and len(rounds)==19,"global final"); total=sum(walls); need(abs(total-294.746940)<1e-6 and total<540 and maxrss==21280560,"resources")
paths=[INPUT/"vectors.bin"]+[PROD/s[0]/"vectors.bin" for s in SPECS]; counts=[1496171]+[s[4] for s in SPECS]
edges=[{"input_round":headers[i][0],"output_round":headers[i+1][0],**edge(paths[i],paths[i+1],counts[i],counts[i+1])} for i in range(3)]
replay=load(HERE/"results_round1362_all_column_replay.json"); need((replay["status"],replay["round"],replay["columns_replayed"],replay["terms_replayed"],replay["verification_failures"])==("PASS_ALL_COLUMNS",1362,1582672,161563157,0),"final replay")
need(hashes["stage03_result"].startswith("d2d460d5") and hashes["stage03_checkpoint"].startswith("ddf88735") and hashes["stage03_vectors"].startswith("25f42b9b") and hashes["stage03_watchdog"].startswith("8ef3d6b1"),"final pins")
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1362_CAP1750_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1362_CAP1750_CHAIN","scope":"Accepted round1343 cap1750 state through exact rounds1344..1362; no round1363 continuation.","input":{"round":1343,"columns":1496171,"support":1949,"checkpoint_sha256":"d2dbdee814cecca8f8528d84d2f386d3f042a54b62039a0350a834b5a1949dcf","vectors_sha256":"d5517dfdc00cb7c2e0844b2459385576dd84211eceebe3a0cb94815a1cd7a2c6"},"final":{"round":1362,"columns":1582672,"new_columns":86501,"support":2043,"target_coefficient":1},"stage_summaries":stages,"checkpoint_edges":cpedges,"cache_edges":edges,"resources":{"aggregate_watchdog_seconds":total,"required_less_than":540,"maximum_peak_rss_kib":maxrss,"rss_limit_kib":LIMIT},"all_column_replay":replay,"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH,"input_manifest_sha256":sha(INPUTPKG/"MANIFEST.sha256"),"replay_sha256":sha(HERE/"results_round1362_all_column_replay.json")},"verdict_note":"Round1362 remains INCOMPLETE_SEARCH_CAP/ROUND_CAP: exact resumable state, not a terminal global dual."}
tmp=HERE/"results_round1362_chain_audit.json.tmp"; tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); os.replace(tmp,HERE/"results_round1362_chain_audit.json")
