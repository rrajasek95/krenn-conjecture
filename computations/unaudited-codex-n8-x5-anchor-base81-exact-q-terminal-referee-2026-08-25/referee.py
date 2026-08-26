#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-exact-q-held-plan-2026-08-25"
PLANREF=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-exact-q-held-plan-referee-2026-08-25"
CAN=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25/canonical_reduced_full_x5_Q.sing"
EPI=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25/SOLVER_EPILOGUE.sing"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(PLANREF/"FINAL_MANIFEST.sha256")=="165406e8d7663558ed000e871a6da06ebe9806a482865274346156d408e86208";replay(PLANREF/"FINAL_MANIFEST.sha256",PLANREF)
assert h(RUN/"MANIFEST.sha256")=="2a9818993a059993ab2510f188f5952af10245d8f75cb572405d4db77488ac8f";replay(RUN/"MANIFEST.sha256",RUN);replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
derived=CAN.read_text().replace("quit;\n",EPI.read_text(),1).encode();assert len(derived)==420121 and hashlib.sha256(derived).hexdigest()=="85f75e489e80a12109a82da607d6d1e21498f825f17eea8486f41078b73b39bc"
att=RUN/"attempt_exact_q";assert (att/"base81_exact_Q.sing").read_bytes()==derived
pre=json.loads((att/"preflight.json").read_text());assert pre["census"]["pass"] and pre["census"]["matches"]==[]
wd=json.loads((att/"watchdog.json").read_text());assert wd["status"]=="PASS" and wd["returncode"]==0 and wd["breach"] is None
assert wd["native_wall_seconds"]==480 and wd["wrapper_wall_seconds"]==510 and wd["rss_limit_kib"]==8388608
assert wd["elapsed_seconds"]==10.955532 and wd["peak_rss_kib"]==111084 and wd["logs_atomic"] and not wd["automatic_relaunch"] and not wd["second_lane"]
assert (att/"stdout.log").read_text().splitlines()==["INPUT_VARIABLES=81","INPUT_GENERATORS=6561","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"] and (att/"stderr.log").read_bytes()==b""
x=json.loads((att/"result.json").read_text());assert x["status"]=="UNIT_IDEAL_EXACT_Q_BASE81" and x["unit_ideal"] and x["same_chart_only"] and x["q_lane"]
assert x["returncode"]==0 and x["breach"] is None and not x["second_lane"] and not x["automatic_relaunch"]
assert not (RUN/"refusal.json").exists() and not list(RUN.glob("*.tmp")) and not list(RUN.glob("attempt_exact_q_*"))
out={"schema":"KRENN_X5_ANCHOR_BASE81_EXACT_Q_TERMINAL_REFEREE_V1","status":"PASS_EXACT_Q_UNIT_IDEAL_CANONICAL_BASE81_CHART","chart":"anchor/no-rectangle/base81/canonical-reduced-full-X5","field":"Q","variables":81,"generators":6561,"groebner_basis_size":1,"unit_remainder":0,"source_sha256":h(att/"base81_exact_Q.sing"),"result_sha256":h(att/"result.json"),"watchdog_sha256":h(att/"watchdog.json"),"elapsed_seconds":wd["elapsed_seconds"],"peak_rss_bytes":wd["peak_rss_kib"]*1024,"same_chart_closed":True,"second_lane_launched":False,"automatic_relaunch":False,"anchor_family_closed":False,"conjecture_closed":False}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
