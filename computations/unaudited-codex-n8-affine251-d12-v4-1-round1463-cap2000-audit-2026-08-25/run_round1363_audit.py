#!/usr/bin/env python3
"""Audit accepted r1363→r1447 chain, excluding failed stage15 and including recovery attempt2."""
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PARENT=ROOT/"computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"; PROD=PARENT/"production_from_round1363_portfolio_cap2000"
INPUTPKG=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1363-internal-sequential-portfolio-cap2000-design-2026-08-25"; INPUT=INPUTPKG/"cap2000_candidate"
FORMAT=ROOT/"computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"; BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"; WATCH="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"; LIMIT=36*1024*1024
SPECS=[
 ("stage01",1363,1587266,1369,1614524,2083),("stage02",1369,1614524,1375,1638734,1962),("stage03",1375,1638734,1381,1663877,2068),("stage04",1381,1663877,1387,1692330,2288),("stage05",1387,1692330,1393,1719971,2018),
 ("stage06",1393,1719971,1399,1747427,1908),("stage07",1399,1747427,1405,1775477,2282),("stage08",1405,1775477,1411,1805847,2392),("stage09",1411,1805847,1417,1835513,2488),("stage10",1417,1835513,1422,1858227,2178),
 ("stage11",1422,1858227,1427,1881111,2251),("stage12",1427,1881111,1432,1902942,2061),("stage13",1432,1902942,1437,1924285,2260),("stage14",1437,1924285,1442,1946624,2316),("stage15_recovery_attempt2",1442,1946624,1447,1970322,2136)]
def need(x,m):
 if not x: raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""): h.update(b)
 return h.hexdigest()
def load(p): return json.loads(p.read_text())
need(sha(INPUTPKG/"MANIFEST.sha256")=="bc359255b558a91a02fee4fc76aee9394b3a91d08aa24dd4ef96652bf1e80fd6","input manifest")
need(sha(INPUT/"checkpoint.bin")=="91d573bcfbb2e43f0832a595c899b7c5bd411845cb8323cbcff1c5d7728f92e1","input checkpoint")
need(sha(INPUT/"vectors.bin")=="5c39cf56b3504a44f8e002f9ad3e42b533855d6217e5e5f9967543f6d77e0e5e","input vectors")
ia=load(INPUTPKG/"results_round1363_audit.json"); need(ia["status"].startswith("PASS") and ia["output_checkpoint_sha256"].startswith("91d573bc") and ia["output_vectors_sha256"].startswith("5c39cf56"),"input audit")
need(sha(FORMAT)=="976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67","format parser")
need(sha(HERE/"COMPACTION_EXECUTION.md")=="70775a9cf541afad739bf3e41fc687f96d0384528a4127404634552ea0e64a03","compaction record")
failed=PROD/"stage15"; fe=load(failed/"FAILURE_EVIDENCE.json")
need(sha(failed/"FAILURE_EVIDENCE.json")=="98e0e7993007bf14b9fd96a32c1548f410fa325943f92fc1ff7b75b4a2175472","failure evidence")
need(fe["status"]=="REJECT_NO_SPACE_DURING_ATOMIC_CACHE_WRITE" and fe["acceptance"]["accepted_frontier_remains_round"]==1442 and not fe["acceptance"]["stage15_arithmetic_accepted"],"failure classification")
need(not (failed/"result.json").exists(),"failed result must be absent")
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
checkpoints=[fmt.parse_checkpoint(INPUT/"checkpoint.bin")]+[fmt.parse_checkpoint(PROD/s[0]/"checkpoint.bin") for s in SPECS]; headers=[(1363,1587266,2161)]+[(s[3],s[4],s[5]) for s in SPECS]
for c,h in zip(checkpoints,headers): need((c["round"],len(c["columns"]),c["support"],c["target_coefficient"])==(*h,1),"checkpoint header")
cpedges=[]
for a,b in zip(checkpoints,checkpoints[1:]):
 aa,bb=set(a["columns"]),set(b["columns"]); need(aa<=bb,"checkpoint descendant"); cpedges.append({"input_round":a["round"],"output_round":b["round"],"preserved":len(aa),"new_columns":len(bb-aa)})
rounds=[]; stages=[]; hashes={}; walls=[]; maxrss=0
for name,ir,ic,orr,oc,sup in SPECS:
 d=PROD/name; r=load(d/"result.json"); w=load(d/"watchdog.json")
 need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"],r["cached_vectors_loaded"],r["vectors_materialized_on_restore"])==("INCOMPLETE_RESOURCE_GATE","WALL_CAP",orr,oc,sup,ic,0),name+" result")
 need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"])==(16,"rare","cold","hierarchical",False,2000000),name+" mode")
 need([x["round"] for x in r["rounds"]]==list(range(ir+1,orr+1)),name+" no gap"); cols=ic
 for x in r["rounds"]: need(x["new_columns"]>0 and x["selected_pivot"]=="rare" and x["selected_strategy"]=="cold",name+" record"); cols+=x["new_columns"]; need(cols==x["columns"],name+" recurrence")
 need(cols==oc and r["rounds"][-1]["dual_support"]==sup,name+" final"); rounds+=r["rounds"]
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],name+" watchdog")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),name+" pins")
 need(w["rss_limit_kib"]==LIMIT and w["peak_rss_kib"]<LIMIT and all(s["rss_kib"]<LIMIT for s in w["samples"]),name+" RSS")
 need(w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.5,name+" telemetry")
 need(not any((d/(f+".tmp")).exists() for f in ("result.json","checkpoint.bin","vectors.bin","stdout.log","stderr.log")),name+" tmp")
 walls.append(w["elapsed_seconds"]); maxrss=max(maxrss,w["peak_rss_kib"]); stages.append({"stage":name,"rounds":[ir+1,orr],"input_columns":ic,"output_columns":oc,"support":sup,"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]})
 for k,f in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")): hashes[name+"_"+k]=sha(d/f)
need([x["round"] for x in rounds]==list(range(1364,1448)),"global rounds"); cols=1587266
for x in rounds: cols+=x["new_columns"]; need(cols==x["columns"],"global columns")
need(cols==1970322 and len(rounds)==84,"global final")
blocks=[sum(walls[:5]),sum(walls[5:10]),sum(walls[10:])]; need(all(x<540 for x in blocks) and abs(blocks[0]-510.337634)<1e-6 and abs(blocks[1]-522.671661)<1e-6 and abs(blocks[2]-515.460899)<1e-6 and maxrss==24894816,"resources")
paths=[INPUT/"vectors.bin"]+[PROD/s[0]/"vectors.bin" for s in SPECS]; counts=[1587266]+[s[4] for s in SPECS]
edges=[{"input_round":headers[i][0],"output_round":headers[i+1][0],**edge(paths[i],paths[i+1],counts[i],counts[i+1])} for i in range(15)]
replay=load(HERE/"results_round1447_all_column_replay.json"); need((replay["status"],replay["round"],replay["columns_replayed"],replay["terms_replayed"],replay["verification_failures"])==("PASS_ALL_COLUMNS",1447,1970322,201304537,0),"final replay")
need(hashes["stage15_recovery_attempt2_result"]=="a313bf00b597c3253edc32e33550ad4a0bb83d539e31eb77d3b34e6c617c22c6" and hashes["stage15_recovery_attempt2_checkpoint"]=="82d53e68e3f1bd483518996fed2dbffa80910163e8c7234f9ccce7c88afeb3cb" and hashes["stage15_recovery_attempt2_vectors"]=="b806d22cac98ce4dd45928baf01401a8a7afaa12fcbd6d9c56f07cb1f9dab091" and hashes["stage15_recovery_attempt2_watchdog"]=="81c27fe5f12c066645f64f5620570af8c2d463dcbc520e5b065ce7a959e650c7","recovery pins")
out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1447_CAP2000_RECOVERY_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1447_RECOVERED_CHAIN","scope":"Accepted r1363 cap2m state through exact rounds1364..1447 using stages01..14 and distinct stage15_recovery_attempt2; failed stage15 is explicitly excluded.","input":{"round":1363,"columns":1587266,"support":2161,"checkpoint_sha256":"91d573bcfbb2e43f0832a595c899b7c5bd411845cb8323cbcff1c5d7728f92e1","vectors_sha256":"5c39cf56b3504a44f8e002f9ad3e42b533855d6217e5e5f9967543f6d77e0e5e"},"final":{"round":1447,"columns":1970322,"new_columns":383056,"remaining_column_headroom":29678,"support":2136,"target_coefficient":1},"accepted_stage_summaries":stages,"checkpoint_edges":cpedges,"cache_edges":edges,"resources":{"block_watchdog_seconds":blocks,"each_block_required_less_than":540,"maximum_peak_rss_kib":maxrss,"rss_limit_kib":LIMIT},"excluded_failure":{"directory":"stage15","reason":"ENOSPC during atomic cache write","result_absent":True,"accepted_coverage":0,"failure_evidence_sha256":sha(failed/"FAILURE_EVIDENCE.json"),"failure_report_sha256":sha(failed/"FAILURE_REPORT.md")},"compaction_execution_sha256":sha(HERE/"COMPACTION_EXECUTION.md"),"all_column_replay":replay,"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH,"input_manifest_sha256":sha(INPUTPKG/"MANIFEST.sha256"),"replay_sha256":sha(HERE/"results_round1447_all_column_replay.json")},"verdict_note":"Round1447 is an exact recovered resumable state near the cap, not round1463 and not a terminal global dual."}
tmp=HERE/"results_round1447_chain_audit.json.tmp"; tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); os.replace(tmp,HERE/"results_round1447_chain_audit.json")
