#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
here=Path(__file__).resolve().parent; att=here/"attempt_exact_q"
pins={
 here/"rank1_orbit0_Q.sing":"c062396aa8835e9c31d0e845a997d89f3b1d151f6494d36d5ba990cdadf9c44f",
 att/"rank1_orbit0_Q.sing":"c062396aa8835e9c31d0e845a997d89f3b1d151f6494d36d5ba990cdadf9c44f",
 att/"result.json":"cef4024431eaf91cd1a39b91dd728b4a1d9098e2c0af419eacf58bcf6a751c6a",
 att/"watchdog.json":"0f48d9c5e0aa2164b6cea68d387dc1f2f3081ba74ad9a7182b697ae64004f676",
 att/"preflight.json":"b3464b8ffd143d2883e65a85665df9caa224c9561c06b7ceb49a73cea13dadf4",
 att/"stdout.log":"fcfdaa6e2ccf723fb9b2ea3226200b25155b1d70cc93c20c34843c19af3ff685",
 att/"stderr.log":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}
for p,x in pins.items(): assert h(p)==x,(p,h(p))
assert sorted(p.name for p in here.glob("attempt*"))==["attempt_exact_q"] and not list(here.rglob("*.tmp"))
pre=json.loads((att/"preflight.json").read_text()); wd=json.loads((att/"watchdog.json").read_text()); res=json.loads((att/"result.json").read_text()); aud=json.loads((here/"AUDIT_RESULT.json").read_text())
assert pre["census"]["pass"] and pre["census"]["matches"]==[]
assert wd["status"]=="PASS" and wd["returncode"]==0 and wd["breach"] is None and wd["logs_atomic"]
assert (wd["native_wall_seconds"],wd["wrapper_wall_seconds"],wd["rss_limit_kib"])==(480,510,8388608)
assert not wd["automatic_relaunch"] and not wd["second_lane"]
assert res["status"]=="UNIT_IDEAL_EXACT_Q_RANK1_ORBIT0" and res["unit_ideal"] and res["rank1_orbit0_closed"]
assert not res["rank12_family_closed"] and not res["automatic_relaunch"] and not res["second_lane"]
assert res["parsed_stdout"]=={"INPUT_VARIABLES":"76","INPUT_GENERATORS":"6571","GROEBNER_SIZE":"1","UNIT_REMAINDER":"0","STATUS":"UNIT_IDEAL"}
assert aud["status"]=="PASS_UNIT_IDEAL_EXACT_Q_RANK1_ORBIT0_ONLY" and not aud["rank12_family_closed"]
print(json.dumps({"status":"PASS","audit_sha256":h(here/"AUDIT_RESULT.json")}))
