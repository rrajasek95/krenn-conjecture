#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(here/"BATCH_RESULT.json")=="f49758f2522ab427542706df07775f54d0d2a3c04a537776f6623cb9d0a23ab2"
expected_manifests={1:"fd192885e77f8494d29ceaf546c5456574c099c28efffd5ccb3e0155b6dbebfe",2:"97b5579385dc7f58e3580d5c235b57a3fb1f30f4720cb0ba05b6e77dfe8a272e",3:"4597466d8bbcdf9b7254916937556c7653f9c926df94cff7d9e0ce0a10673044",4:"c08f7fac596b0780f4dd444030c003ad0e1c63da93135e9f36f560212f827196"}
for o,mh in expected_manifests.items():
 att=here/f"attempt_orbit{o}"; assert h(att/"FINAL_MANIFEST.sha256")==mh
 pre=json.loads((att/"preflight.json").read_text()); res=json.loads((att/"result.json").read_text()); wd=json.loads((att/"watchdog.json").read_text())
 assert pre["orbit"]==o and pre["census"]["pass"] and pre["census"]["matches"]==[]
 assert res["orbit"]==o and res["unit_ideal"] and res["status"]==f"UNIT_IDEAL_EXACT_Q_ORBIT{o}"
 assert res["parsed_stdout"]=={"INPUT_VARIABLES":"76","INPUT_GENERATORS":"6571","GROEBNER_SIZE":"1","UNIT_REMAINDER":"0","STATUS":"UNIT_IDEAL"}
 assert wd["status"]=="PASS" and wd["returncode"]==0 and wd["breach"] is None and wd["logs_atomic"]
 assert (wd["native_wall_seconds"],wd["wrapper_wall_seconds"],wd["rss_limit_kib"])==(480,510,8388608)
 assert not wd["automatic_relaunch"] and not wd["parallel"]
batch=json.loads((here/"BATCH_RESULT.json").read_text());audit=json.loads((here/"FINAL_AUDIT.json").read_text())
assert batch["status"]=="PASS_ALL_FOUR_UNIT_IDEALS" and batch["attempted_orbits"]==[1,2,3,4] and batch["unattempted_orbits"]==[] and batch["all_four_closed"]
assert audit["status"]=="PASS_ALL_FOUR_EXACT_Q_UNIT_IDEALS" and audit["rank1_canonical_family_closed"] and not audit["rank2_closed"] and audit["resource_clear"]
assert sorted(p.name for p in here.glob("attempt_orbit*"))==[f"attempt_orbit{x}" for x in range(1,5)] and not list(here.rglob("*.tmp"))
print(json.dumps({"status":"PASS","audit_sha256":h(here/"FINAL_AUDIT.json")}))
