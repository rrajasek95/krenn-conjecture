#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-2026-08-25"
REF=ROOT/"computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-referee-2026-08-25"
IDS=[11,12,14]+list(range(16,38))
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(REF/"FINAL_MANIFEST.sha256")=="950e50ea1b1af733b5f20fad076357d29ee76a7b85009c7b93fcad76b1406c75";replay(REF/"FINAL_MANIFEST.sha256",REF)
assert h(REF/"independent_referee_acceptance.json")=="af739024d0006001caa4dd8c899dd902d352499adf81052ca49650cab2a3ca1d"
assert h(RUN/"MANIFEST.sha256")=="79052e97d726b5dfc6bf5c4831af27638548bf5cf3a79ade3948a94059470810";replay(RUN/"MANIFEST.sha256",RUN);replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
assert h(RUN/"run_next25.py")=="ad655676b830652681cddd7aa7af46987713984bb63db7dc68157bf88800c268"
assert h(RUN/"source_ledger.json")=="67376d9ddc96b65f0c34d0f746c85703417d0fb3be88ce5d2cf90a601945c833"
ledger=json.loads((RUN/"source_ledger.json").read_text());assert [x["group_id"] for x in ledger["lanes"]]==IDS
attempt=json.loads((RUN/"BATCH_ATTEMPT.json").read_text());assert attempt["status"]=="CONSUMED_SINGLE_USE" and attempt["group_ids"]==IDS
clear=json.loads((RUN/"launch_clearance.json").read_text());assert clear["selected_group_ids"]==IDS and clear["maximum_lane_count"]==25
batch=json.loads((RUN/"batch_result.json").read_text());assert batch["status"]=="PASS_ALL_25_UNIT" and batch["stop"] is None and batch["skipped_after_stop"]==[]
assert batch["strict_order"]==IDS and not batch["parallel"] and not batch["relaunch"]
walls=[];peaks=[]
expected_tail=["INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL","Auf Wiedersehen."]
for ordinal,(gid,lane,item) in enumerate(zip(IDS,ledger["lanes"],batch["completed"]),1):
 p=RUN/f"results/group{gid:03d}.json";x=json.loads(p.read_text())
 assert item=={"group_id":gid,"status":"UNIT_IDEAL_EXACT_Q","result_sha256":h(p)}
 assert x["group_id"]==gid and x["ordinal"]==ordinal and x["chart"]==lane["canonical_chart"] and x["source_sha256"]==lane["source_sha256"]
 assert x["status"]=="UNIT_IDEAL_EXACT_Q" and x["termination"] is None and x["wrapper_returncode"]==0 and x["stderr"]==""
 assert x["stdout"].splitlines()[-5:]==expected_tail and x["diagnostic_scope_one_group"] and not x["automatic_relaunch"]
 assert x["wall_seconds"]<240 and x["peak_group_rss_bytes"]<8589934592
 walls.append(x["wall_seconds"]);peaks.append(x["peak_group_rss_bytes"])
assert len(list((RUN/"results").glob("group*.json")))==25 and not list(RUN.rglob("*.tmp"))
assert not list((RUN/"results").glob("group0[3-9][8-9].json"))
out={"schema":"KRENN_X5_REP1_NEXT25_EXACT_Q_TERMINAL_REFEREE_V1","status":"PASS_ALL_25_EXACT_Q_UNIT_IDEALS","groups_closed":IDS,"variables_each":91,"generators_each":6577,"groebner_basis_size_each":1,"unit_remainder_each":0,"aggregate_lane_wall_seconds":sum(walls),"maximum_lane_wall_seconds":max(walls),"maximum_peak_rss_bytes":max(peaks),"strict_order":True,"parallel":False,"relaunch":False,"skipped":False,"groups_beyond_37_launched":False,"new_groups_closed":25,"rep1_representative_closed":False,"seven_block_family_closed":False,"conjecture_closed":False,"batch_result_sha256":h(RUN/"batch_result.json"),"terminal_manifest_sha256":h(RUN/"TERMINAL_MANIFEST.sha256")}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
