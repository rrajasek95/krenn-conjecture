#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep1-next10-exact-q-held-2026-08-25"
REF=ROOT/"computations/unaudited-codex-n8-x5-rep1-next10-exact-q-held-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(REF/"FINAL_MANIFEST.sha256")=="eba68cfe5bc74151c4b0a4bd0e448af44002ce9ffbd4e8ecfafb8c55f068b948";replay(REF/"FINAL_MANIFEST.sha256",REF)
assert h(RUN/"MANIFEST.sha256")=="33ac399cf348e8bad9de4987369ee43d5839063eb70a15f3dca07e97e10fb04a";replay(RUN/"MANIFEST.sha256",RUN);replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
ledger=json.loads((RUN/"source_ledger.json").read_text());assert [x["group_id"] for x in ledger["lanes"]]==list(range(1,11))
attempt=json.loads((RUN/"BATCH_ATTEMPT.json").read_text());assert attempt["status"]=="CONSUMED_SINGLE_USE" and attempt["group_ids"]==list(range(1,11))
batch=json.loads((RUN/"batch_result.json").read_text());assert batch["status"]=="PASS_ALL_TEN_UNIT" and batch["stop"] is None and batch["skipped_after_stop"]==[]
assert batch["strict_order"]==list(range(1,11)) and not batch["parallel"] and not batch["relaunch"]
walls=[];peaks=[]
expected_tail=["INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL","Auf Wiedersehen."]
for gid,lane,item in zip(range(1,11),ledger["lanes"],batch["completed"]):
 p=RUN/f"results/group{gid:03d}.json";x=json.loads(p.read_text())
 assert item=={"group_id":gid,"status":"UNIT_IDEAL_EXACT_Q","result_sha256":h(p)}
 assert x["group_id"]==gid and x["ordinal"]==gid and x["chart"]==lane["canonical_chart"] and x["source_sha256"]==lane["source_sha256"]
 assert x["status"]=="UNIT_IDEAL_EXACT_Q" and x["termination"] is None and x["wrapper_returncode"]==0 and x["stderr"]==""
 assert x["stdout"].splitlines()[-5:]==expected_tail and x["diagnostic_scope_one_group"] and not x["automatic_relaunch"]
 assert x["wall_seconds"]<240 and x["peak_group_rss_bytes"]<8589934592
 walls.append(x["wall_seconds"]);peaks.append(x["peak_group_rss_bytes"])
assert len(list((RUN/"results").glob("group*.json")))==10 and not list(RUN.glob("*.tmp"))
out={"schema":"KRENN_X5_REP1_NEXT10_EXACT_Q_TERMINAL_REFEREE_V1","status":"PASS_ALL_TEN_EXACT_Q_UNIT_IDEALS","groups_closed":list(range(1,11)),"variables_each":91,"generators_each":6577,"groebner_basis_size_each":1,"unit_remainder_each":0,"aggregate_lane_wall_seconds":sum(walls),"maximum_lane_wall_seconds":max(walls),"maximum_peak_rss_bytes":max(peaks),"strict_order":True,"parallel":False,"relaunch":False,"skipped":False,"groups_beyond_10_launched":False,"new_groups_closed":10,"rep1_total_known_closed_increment":10,"rep1_representative_closed":False,"seven_block_family_closed":False,"conjecture_closed":False,"batch_result_sha256":h(RUN/"batch_result.json")}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
