#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(here/"BATCH_RESULT.json")=="e1934a0faaad654fb60e9178883781927b6bb78ab4a0d720fbfe3969dac679e6"
manifests={0:"63b4a008b98a8e3b140428f81ae41c2dfff465de758896edd7ff0ccd85840e21",1:"29befbab455563cdc653c40c8d459cb10ea25379bb44fb9f4483f73743a00bd3",2:"f54a81572b3029d4c9ad52b107e8198035f4ef371e5489ff233ab264100d9cb9",3:"8e33fa61c6478f78787f262dc452cc9dd996be0e44f5d9e501da7f45188efe9f",4:"ab4453b1e0924a3eb6df4d2a58f7b69ea154ac9b58c325bbcf365167fe048575"}
for o,mh in manifests.items():
 att=here/f"attempt_orbit{o}";assert h(att/"FINAL_MANIFEST.sha256")==mh
 pre=json.loads((att/"preflight.json").read_text());res=json.loads((att/"result.json").read_text());wd=json.loads((att/"watchdog.json").read_text())
 assert pre["orbit"]==o and pre["census"]["pass"] and pre["census"]["matches"]==[]
 assert res["rank"]==2 and res["orbit"]==o and res["unit_ideal"] and res["status"]==f"UNIT_IDEAL_EXACT_Q_ORBIT{o}"
 assert res["parsed_stdout"]=={"INPUT_VARIABLES":"80","INPUT_GENERATORS":"6574","GROEBNER_SIZE":"1","UNIT_REMAINDER":"0","STATUS":"UNIT_IDEAL"}
 assert wd["status"]=="PASS" and wd["returncode"]==0 and wd["breach"] is None and wd["logs_atomic"]
 assert (wd["native_wall_seconds"],wd["wrapper_wall_seconds"],wd["rss_limit_kib"])==(480,510,8388608) and not wd["automatic_relaunch"] and not wd["parallel"]
batch=json.loads((here/"BATCH_RESULT.json").read_text());audit=json.loads((here/"FINAL_AUDIT.json").read_text())
assert batch["status"]=="PASS_ALL_FIVE_UNIT_IDEALS" and batch["attempted_orbits"]==[0,1,2,3,4] and batch["unattempted_orbits"]==[] and batch["all_five_closed"] and not batch["rank1_run"]
assert audit["status"]=="PASS_ALL_FIVE_EXACT_Q_UNIT_IDEALS" and audit["rank2_canonical_family_closed"] and not audit["rank1_run"] and audit["resource_clear"]
assert sorted(p.name for p in here.glob("attempt_orbit*"))==[f"attempt_orbit{x}" for x in range(5)] and not list(here.rglob("*.tmp"))
print(json.dumps({"status":"PASS","audit_sha256":h(here/"FINAL_AUDIT.json")}))
