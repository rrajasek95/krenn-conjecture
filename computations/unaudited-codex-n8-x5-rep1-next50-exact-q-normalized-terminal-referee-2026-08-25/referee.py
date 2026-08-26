#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25"
REF=ROOT/"computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-referee-2026-08-25"
IDS=list(range(38,88))
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(REF/"FINAL_MANIFEST.sha256")=="950e504da1e64a4056cce58b0440165f5f8e5be4c159e2431f5010c5e06fbdc2";replay(REF/"FINAL_MANIFEST.sha256",REF)
assert h(REF/"results_referee.json")=="1b303cb18146e5cadb4da5bf765fc9c2dd03f6593742652f34f5808691194a87"
assert h(REF/"HELD_APPROVAL.json")=="d303477e571e9da2d8682050dbbbea63660a39586a122fa9c3d07cf3d42cbc2a"
assert h(RUN/"MANIFEST.sha256")=="7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da";replay(RUN/"MANIFEST.sha256",RUN);replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
assert h(RUN/"run_next50_v2.py")=="b9fc730669e6e5fc4799e9efbf4e6f12b1f443acc004af9bc536be851c4d8388"
assert h(RUN/"source_ledger.json")=="1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172"
assert h(RUN/"normalized_next25_dependency.json")=="29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76"
ledger=json.loads((RUN/"source_ledger.json").read_text());assert [x["group_id"] for x in ledger["lanes"]]==IDS and [x["ordinal"] for x in ledger["lanes"]]==list(range(1,51))
attempt=json.loads((RUN/"BATCH_ATTEMPT.json").read_text());assert attempt["status"]=="CONSUMED_SINGLE_USE" and attempt["group_ids"]==IDS
assert attempt["normalized_dependency_sha256"]=="29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76"
batch=json.loads((RUN/"batch_result.json").read_text());assert batch["status"]=="PASS_ALL_50_UNIT" and batch["stop"] is None and batch["skipped_after_stop"]==[]
assert batch["strict_order"]==IDS and not batch["parallel"] and not batch["relaunch"]
walls=[];peaks=[];expected_tail=["INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL","Auf Wiedersehen."]
for ordinal,(gid,lane,item) in enumerate(zip(IDS,ledger["lanes"],batch["completed"]),1):
 p=RUN/f"results/group{gid:03d}.json";x=json.loads(p.read_text())
 assert item=={"group_id":gid,"status":"UNIT_IDEAL_EXACT_Q","result_sha256":h(p)}
 assert x["group_id"]==gid and x["ordinal"]==ordinal and x["chart"]==lane["canonical_chart"] and x["source_sha256"]==lane["source_sha256"]
 assert x["status"]=="UNIT_IDEAL_EXACT_Q" and x["termination"] is None and x["wrapper_returncode"]==0 and x["stderr"]==""
 assert x["stdout"].splitlines()[-5:]==expected_tail and x["diagnostic_scope_one_group"] and not x["automatic_relaunch"]
 assert x["wall_seconds"]<240 and x["peak_group_rss_bytes"]<8589934592
 walls.append(x["wall_seconds"]);peaks.append(x["peak_group_rss_bytes"])
files=list((RUN/"results").glob("group*.json"));assert len(files)==50 and sorted(json.loads(p.read_text())["group_id"] for p in files)==IDS
assert not list(RUN.rglob("*.tmp"))
out={"schema":"KRENN_X5_REP1_NEXT50_NORMALIZED_EXACT_Q_TERMINAL_REFEREE_V1","status":"PASS_ALL_50_EXACT_Q_UNIT_IDEALS","groups_closed":IDS,"closed_union_after_batch":list(range(88)),"variables_each":91,"generators_each":6577,"groebner_basis_size_each":1,"unit_remainder_each":0,"aggregate_lane_wall_seconds":sum(walls),"maximum_lane_wall_seconds":max(walls),"maximum_peak_rss_bytes":max(peaks),"strict_order":True,"parallel":False,"relaunch":False,"skipped":False,"groups_beyond_87_launched":False,"new_groups_closed":50,"rep1_closed_count":88,"rep1_total_groups":162,"rep1_representative_closed":False,"seven_block_family_closed":False,"conjecture_closed":False,"batch_result_sha256":h(RUN/"batch_result.json"),"terminal_manifest_sha256":h(RUN/"TERMINAL_MANIFEST.sha256")}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
