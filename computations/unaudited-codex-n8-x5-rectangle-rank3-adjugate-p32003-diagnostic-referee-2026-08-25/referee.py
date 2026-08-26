#!/usr/bin/env python3
"""Independent referee of the one-shot modular adjugate diagnostic; no solve."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROD=ROOT/"computations/unaudited-codex-n8-x5-rectangle-rank3-adjugate-ideal-referee-2026-08-25"
RUN=PROD/"modular_p32003_run"
Q_SOURCE=PROD/"rectangle_rank3_adjugate_Q.sing"
OUT=Path(__file__).resolve().parent/"results_referee.json"
PINS={
 RUN/"MANIFEST.sha256":"922604a9b3ae34f8fded694eb28a6d0c2736e463839bd7381740f0a9327742c4",
 RUN/"RESULT.json":"1c67f97a20ba88964b5f6d82d34eebc9cd221cb8ecda7e0c42f12d4e001dd346",
 RUN/"rectangle_rank3_adjugate_p32003.sing":"a6170f8e48329830d371bf0365067511642f4802576302f43e6edae2b734df3c",
 Q_SOURCE:"e2739688ea9986d59c56e17e6f0058154d9ddb7930bf9617a1d3a3a8167538f5",
 RUN/"watchdog.json":"0825361a313d15cecd8291ece9d155c588bc2e5bdb7dce3b0cc60e83f9241dd7",
 RUN/"LAUNCH_RECORD.json":"dbaf2f7bef57318ca93f534597d553622a2f27e6c5a0e481eca631fdb884d353",
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path):
 n=0
 for line in path.read_text().splitlines():
  if not line.strip():continue
  d,r=line.split(None,1);assert sha(path.parent/r.strip())==d;n+=1
 return n
def count_top(body):
 depth=0;n=1 if body.strip() else 0
 for c in body:
  if c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0
  elif c==',' and depth==0:n+=1
 assert depth==0;return n
for p,d in PINS.items():assert sha(p)==d,(p,sha(p),d)
manifest_entries=replay(RUN/"MANIFEST.sha256")
q=Q_SOURCE.read_text();p=(RUN/"rectangle_rank3_adjugate_p32003.sing").read_text()
assert q.count("ring r=0,")==1 and p==q.replace("ring r=0,","ring r=32003,",1)
assert p.count("ring r=32003,")==1 and "ring r=0," not in p
r0=p.index("ring r=32003,(")+len("ring r=32003,(");r1=p.index("),dp;",r0)
variables=p[r0:r1].split(',');assert len(variables)==len(set(variables))==56
i0=p.index("ideal I=")+len("ideal I=");i1=p.index(";\nprint(\"INPUT_VARIABLES=",i0)
assert count_top(p[i0:i1])==6563

result=json.loads((RUN/"RESULT.json").read_text());wd=json.loads((RUN/"watchdog.json").read_text());launch=json.loads((RUN/"LAUNCH_RECORD.json").read_text())
assert result["status"]=="PASS_MODULAR_UNIT_IDEAL_DIAGNOSTIC_ONLY"
assert result["scope"]=={"field_prime":32003,"singular_lanes":1,"q_lanes":0,"relaunches":0,"rank3_closed_over_q":False}
assert result["singular_result"]["input_variables"]==56 and result["singular_result"]["input_generators"]==6563
assert result["singular_result"]["groebner_size"]==1 and result["singular_result"]["unit_remainder"]==0 and result["singular_result"]["terminal_status"]=="UNIT_IDEAL"
stdout=(RUN/"stdout.log").read_text();assert stdout=="INPUT_VARIABLES=56\nINPUT_GENERATORS=6563\nGROEBNER_SIZE=1\nUNIT_REMAINDER=0\nSTATUS=UNIT_IDEAL\n"
assert (RUN/"stderr.log").read_bytes()==b""
assert wd["status"]=="PASS" and wd["returncode"]==0 and wd["terminal_reason"] is None
assert wd["elapsed_seconds"]==22.93639 and wd["peak_rss_kib"]==1104100
assert wd["peak_rss_kib"]<wd["rss_limit_kib"]==8388608 and wd["elapsed_seconds"]<wd["native_wall_seconds"]==180
assert wd["logs_atomic"] is True and wd["q_lane_launched"] is False and wd["automatic_relaunch"] is False
assert not any(RUN.glob("*.tmp"))
assert launch["scope"]=="Exactly one p=32003 Singular diagnostic; no Q lane, second lane, or relaunch."
assert launch["terminal_rule"].startswith("Stop and seal after any outcome")

audit={
 "schema":"KRENN_X5_RECTANGLE_RANK3_ADJUGATE_P32003_INDEPENDENT_REFEREE_V1",
 "status":"PASS_MODULAR_UNIT_DIAGNOSTIC_ONLY_NO_Q_PROMOTION",
 "producer_manifest_sha256":PINS[RUN/"MANIFEST.sha256"],"producer_result_sha256":PINS[RUN/"RESULT.json"],"manifest_entries_replayed":manifest_entries,
 "source":{"Q_sha256":PINS[Q_SOURCE],"p32003_sha256":PINS[RUN/"rectangle_rank3_adjugate_p32003.sing"],"unique_ring_token_substitution":True,"variables":56,"generators":6563},
 "result":{"field_prime":32003,"groebner_basis_size":1,"unit_remainder":0,"terminal_status":"UNIT_IDEAL","returncode":0},
 "resources":{"elapsed_seconds":22.93639,"peak_rss_kib":1104100,"native_wall_seconds":180,"wrapper_wall_seconds":190,"rss_limit_kib":8388608,"atomic_logs":True,"tmp_absent":True},
 "run_scope":{"modular_lanes":1,"Q_lanes":0,"second_lane":False,"relaunch":False},
 "interpretation":"unit ideal only over F_32003; no exact-Q or rank3 closure",
 "exact_Q_held_plan":{
  "schema":"KRENN_X5_RECTANGLE_RANK3_ADJUGATE_EXACT_Q_ONE_LANE_HELD_PLAN_V1","status":"HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE",
  "source_sha256":PINS[Q_SOURCE],"source":"fresh byte-identical copy of canonical rectangle_rank3_adjugate_Q.sing","field":"Q","expected_variables":56,"expected_generators":6563,
  "maximum_lane_count":1,"native_wall_seconds":480,"wrapper_wall_seconds":510,"rss_cap_bytes":8*1024**3,"direct_libproc_process_group_rss":True,"atomic_stdout_stderr_result":True,
  "fresh_output_directory":True,"no_second_lane":True,"no_relaunch":True,"stop_after_any_terminal_outcome":True,
  "acceptance":"normal rc0 plus INPUT_VARIABLES=56, INPUT_GENERATORS=6563, GROEBNER_SIZE=1, UNIT_REMAINDER=0, STATUS=UNIT_IDEAL",
  "unit_scope":"would close only this exact rank(A47)=3 adjugate chart (both amplitude-inactive A12 lifts), not rank<=2, unmapped16, seven-block, or the conjecture",
  "nonunit_or_failure_scope":"no closure; terminal hold",
 },
}
OUT.write_text(json.dumps(audit,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":audit["status"],"result_sha256":sha(OUT)},sort_keys=True))
