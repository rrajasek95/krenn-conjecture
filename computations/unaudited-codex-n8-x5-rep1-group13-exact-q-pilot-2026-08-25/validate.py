#!/usr/bin/env python3
import hashlib,json
from pathlib import Path

here=Path(__file__).resolve().parent
result_path=here/"result.json";source=here/"rep1_group13_Q.sing"
x=json.loads(result_path.read_text())
assert x["schema"]=="KRENN_X5_REP1_GROUP13_EXACT_Q_PILOT_V1"
assert x["status"]=="UNIT_IDEAL_EXACT_Q_GROUP13"
assert x["group_id"]==13 and x["chart"]==[0,0,0,1,"z",0,0,2]
assert x["group_closed"] is True and x["representative_closed"] is False
assert hashlib.sha256(source.read_bytes()).hexdigest()==x["source_sha256"]=="336bc28a4affecb31ce32fa468eadb1317efea5fb3ee2d5acbd24fc5f320790a"
assert len(source.read_bytes())==x["source_bytes"]==1841468
assert x["termination"] is None and x["returncode"]==0
assert x["wall_seconds"]<240 and x["observed_peak_rss_bytes"]<8*1024**3
assert all(token in x["stdout"] for token in ("INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"))
assert x["stderr"]==""
assert x["second_lane_launched"] is False and x["optional_microbatch_launched"] is False and x["automatic_relaunch"] is False
binding=json.loads((here/"RESOURCE_CLEAR_BINDING.json").read_text())
assert binding["terminal_rectangle_manifest_sha256"]=="922604a9b3ae34f8fded694eb28a6d0c2736e463839bd7381740f0a9327742c4"
print(json.dumps({"status":"PASS_GROUP13_ONLY","result_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest()},sort_keys=True))
