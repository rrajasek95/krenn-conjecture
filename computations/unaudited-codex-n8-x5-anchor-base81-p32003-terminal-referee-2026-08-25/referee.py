#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25"
PRE=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-held-pilot-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else base/p;assert h(p)==d,(p,h(p),d)
assert h(PRE/"FINAL_MANIFEST.sha256")=="ccec5ada97ededb05e0d24ccbe01a1b013dcf087748b373e926ef3b82da6b76f";replay(PRE/"FINAL_MANIFEST.sha256",PRE)
assert h(RUN/"MANIFEST.sha256")=="f7e20f50dd921f600e993d361e4cdcf8a58a83b62b443533384562c0da13779b";replay(RUN/"MANIFEST.sha256",RUN)
replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
att=RUN/"attempt_p32003";pre=json.loads((att/"preflight.json").read_text());assert pre["census"]["pass"] and pre["census"]["matches"]==[]
wd=json.loads((att/"watchdog.json").read_text());assert wd["status"]=="PASS" and wd["returncode"]==0 and wd["breach"] is None
assert wd["native_wall_seconds"]==180 and wd["wrapper_wall_seconds"]==190 and wd["rss_limit_kib"]==8388608
assert wd["elapsed_seconds"]==37.46379 and wd["peak_rss_kib"]==914352 and wd["logs_atomic"]
assert not wd["automatic_relaunch"] and not wd["second_lane"]
assert (att/"stdout.log").read_text().splitlines()==["INPUT_VARIABLES=81","INPUT_GENERATORS=6561","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"]
assert (att/"stderr.log").read_bytes()==b""
x=json.loads((att/"result.json").read_text());assert x["status"]=="UNIT_IDEAL_P32003_BASE81" and x["unit_ideal"] and x["modular_diagnostic_only"]
assert x["returncode"]==0 and x["breach"] is None and not x["q_lane"] and not x["second_lane"] and not x["automatic_relaunch"]
assert not (RUN/"refusal.json").exists() and not list(RUN.glob("attempt_*_2")) and not list(RUN.glob("*.tmp"))
out={"schema":"KRENN_X5_ANCHOR_BASE81_P32003_TERMINAL_REFEREE_V1","status":"PASS_ONE_MODULAR_UNIT_DIAGNOSTIC_ONLY","field":"F_32003","variables":81,"generators":6561,"groebner_basis_size":1,"unit_remainder":0,"elapsed_seconds":wd["elapsed_seconds"],"peak_rss_bytes":wd["peak_rss_kib"]*1024,"result_sha256":h(att/"result.json"),"watchdog_sha256":h(att/"watchdog.json"),"source_sha256":h(att/"base81_p32003.sing"),"q_lane_launched":False,"second_lane_launched":False,"automatic_relaunch":False,"mathematical_coverage":False,"anchor_family_closed":False,"conjecture_closed":False}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
