#!/usr/bin/env python3
"""Atomic external six-lane r1464 portfolio with evidence-before-prune lifecycle."""
import hashlib, json, os, shutil, struct, subprocess, sys
from pathlib import Path

if not __debug__: raise RuntimeError("fail closed: assertions required")
HERE=Path(__file__).resolve().parent; REPO=HERE.parents[1]
S=json.loads((HERE/"SCHEDULE.json").read_text()); P=json.loads((HERE/"INPUT_PINS.json").read_text())
def sha(path):
 d=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""): d.update(b)
 return d.hexdigest()
def atomic(path,value):
 t=path.with_suffix(path.suffix+".tmp"); t.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n"); os.replace(t,path)
def arg(command,flag): assert command.count(flag)==1; return command[command.index(flag)+1]
E=S["engine"]; SOURCE=REPO/E["source"]; BINARY=REPO/E["binary"]; WATCH=REPO/E["watchdog"]
PROVIDER=REPO/E["provider"]; SCORER=HERE/S["scorer"]["binary"]
CP0=REPO/P["checkpoint"]; VEC0=REPO/P["vectors"]
def clone(label):
 d=HERE/label; assert not d.exists(); d.mkdir()
 subprocess.run(["cp","-c",str(CP0),str(d/"checkpoint.bin")],check=True)
 subprocess.run(["cp","-c",str(VEC0),str(d/"vectors.bin")],check=True)
def native(label,strategy,pivot,cap):
 d=HERE/label
 return [str(BINARY),"--input",str(PROVIDER),"--output",str(d/"result.json"),"--checkpoint",str(d/"checkpoint.bin"),"--vector-cache",str(d/"vectors.bin"),"--dual",str(d/"dual.tsv"),"--prime","1073741827","--wall-seconds","300","--rss-gib","36","--workers","16","--pivot",pivot,"--strategy",strategy,"--elimination","tree","--incremental","no","--portfolio-period","256","--portfolio-parallel","no","--support-cap","100000","--column-cap",str(cap),"--round-cap","1464"]
def run(label,strategy,pivot,cap,index):
 clone(label); d=HERE/label; cmd=native(label,strategy,pivot,cap)
 wrapper=[sys.executable,str(WATCH),"--rss-gib","36","--wall-seconds","330","--poll-seconds","0.25","--source",str(SOURCE),"--expected-source-sha256",E["source_sha256"],"--expected-binary-sha256",E["binary_sha256"],"--telemetry",str(d/"watchdog.json"),"--stdout",str(d/"stdout.log"),"--stderr",str(d/"stderr.log"),"--",*cmd]
 subprocess.run(wrapper,cwd=REPO,check=True)
 score_cmd=[str(SCORER),"--score-frontier","--input",str(PROVIDER),"--checkpoint",str(d/"checkpoint.bin"),"--output",str(d/"frontier_score.json"),"--prime","1073741827","--workers","16"]
 subprocess.run(score_cmd,cwd=REPO,check=True,timeout=45)
 result=json.loads((d/"result.json").read_text()); watch=json.loads((d/"watchdog.json").read_text()); score=json.loads((d/"frontier_score.json").read_text())
 assert result["status"]=="INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"]=="ROUND_CAP" and result["rounds_completed"]==1464 and len(result["rounds"])==1
 rr=result["rounds"][0]; assert rr["round"]==1464 and rr["selected_strategy"]==strategy and rr["selected_pivot"]==pivot
 assert result["cached_vectors_loaded"]==P["columns"] and result["vectors_materialized_on_restore"]==0
 assert watch["status"]=="PASS" and watch["returncode"]==0 and watch["breach"] is None and watch["elapsed_seconds"]<330 and watch["peak_rss_kib"]<36*1024*1024
 assert score["status"]=="PASS_EXACT_FRONTIER_SCORE" and score["round"]==1464 and score["columns"]==rr["columns"] and score["support"]==rr["dual_support"]
 assert not (d/"dual.tsv").exists()
 ev={"schema":"KRENN_AFFINE251_D12_R1464_EXTERNAL_LANE_EVIDENCE_V1","status":"PASS_SEALED_BEFORE_PRUNE","task_index":index,"strategy":strategy,"pivot":pivot,"command":cmd,"round_record":rr,"frontier":score["unseen_incident_frontier_count"],"selector_key":[score["unseen_incident_frontier_count"],rr["dual_support"],index],"result_sha256":sha(d/"result.json"),"watchdog_sha256":sha(d/"watchdog.json"),"frontier_score_sha256":sha(d/"frontier_score.json"),"checkpoint_sha256":sha(d/"checkpoint.bin"),"vectors_sha256":sha(d/"vectors.bin"),"pruned":False}
 atomic(d/"lane_evidence.json",ev); return ev
def prune(label):
 d=HERE/label; ev=json.loads((d/"lane_evidence.json").read_text()); assert ev["status"]=="PASS_SEALED_BEFORE_PRUNE" and not ev["pruned"]
 for name in ("checkpoint.bin","vectors.bin"): assert (d/name).exists(); (d/name).unlink()
 ev["pruned"]=True; atomic(d/"lane_evidence.json",ev)

assert S["status"]=="FROZEN_CLEARED_V2_300_330"
clear=HERE/"LAUNCH_CLEARANCE.json"; assert clear.exists(),"explicit launch clearance absent"
C=json.loads(clear.read_text()); assert C["status"]=="PASS_EXPLICIT_SINGLE_PROCESS_LAUNCH_CLEARANCE" and C["compaction_record_sha256"].startswith("14e32d19")
assert shutil.disk_usage(HERE).free>=S["disk_lifecycle"]["minimum_free_bytes_before_first_clone"]
for path,expected in [(SOURCE,E["source_sha256"]),(BINARY,E["binary_sha256"]),(WATCH,E["watchdog_sha256"]),(PROVIDER,E["provider_sha256"]),(SCORER,S["scorer"]["binary_sha256"]),(REPO/P["audit_result"],P["audit_result_sha256"]),(REPO/P["audit_manifest"],P["audit_manifest_sha256"]),(CP0,P["checkpoint_sha256"]),(VEC0,P["vectors_sha256"])]: assert sha(path)==expected
best=None; labels=[]
for task in S["ordered_tasks"]:
 label=f"lane{task['index']:02d}_{task['strategy']}_{task['pivot']}"; ev=run(label,task["strategy"],task["pivot"],2250000,task["index"]); labels.append(label)
 if best is None: best=(label,ev)
 elif tuple(ev["selector_key"])<tuple(best[1]["selector_key"]): prune(best[0]); best=(label,ev)
 else: prune(label)
assert len(labels)==6 and best is not None
winner_label,winner=best
fixed=run("fixed_winner",winner["strategy"],winner["pivot"],2250000,6)
assert fixed["checkpoint_sha256"]==winner["checkpoint_sha256"] and fixed["vectors_sha256"]==winner["vectors_sha256"] and fixed["round_record"]==winner["round_record"]
prune(winner_label)
cap_run=winner["strategy"]=="cold" and winner["pivot"]=="rare"
final_label="fixed_winner"; cap_ev=None
if cap_run:
 cap_ev=run("cap2500_candidate","cold","rare",2500000,7)
 assert cap_ev["checkpoint_sha256"]==fixed["checkpoint_sha256"] and cap_ev["vectors_sha256"]==fixed["vectors_sha256"] and cap_ev["round_record"]==fixed["round_record"]
 a=[x.replace("/fixed_winner/","/RUN/") for x in fixed["command"]]; b=[x.replace("/cap2500_candidate/","/RUN/") for x in cap_ev["command"]]
 diff=[(i,x,y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]; assert diff==[(a.index("2250000"),"2250000","2500000")]
 prune("fixed_winner"); final_label="cap2500_candidate"
summary={"schema":"KRENN_AFFINE251_D12_R1464_EXTERNAL_PORTFOLIO_RESULT_V1","status":"PASS_SIX_LANES_FIXED_REPLAY_AND_CONDITIONAL_CAP_EQUIVALENCE","winner":{"label":winner_label,"strategy":winner["strategy"],"pivot":winner["pivot"],"selector_key":winner["selector_key"]},"all_six_lanes":labels,"fixed_replay_byte_identical":True,"conditional_cap_run":cap_run,"conditional_cap_equivalence":cap_run,"final_retained_payload":final_label,"continued_beyond_round1464":False}
atomic(HERE/"runner_summary.json",summary); print(json.dumps(summary,sort_keys=True))
