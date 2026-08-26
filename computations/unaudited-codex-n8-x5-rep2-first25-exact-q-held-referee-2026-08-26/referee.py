#!/usr/bin/env python3
from __future__ import annotations
import hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25"
DESIGN=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
CLOSED=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25"
CLOSED_REF=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-second-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(RUN/"MANIFEST.sha256")=="d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c";replay(RUN/"MANIFEST.sha256",RUN)
assert h(RUN/"source_ledger.json")=="20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e"
assert h(RUN/"run_first25.py")=="0727e5e5961f90cd14d3d79f836634bf7df9fff1b8d44bd463678db1f8f72ff2"
assert h(DESIGN/"generate_design.py")=="ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc"
assert h(CLOSED/"rep2_corrected_all_equal_y_Q.sing")=="5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf"
assert h(CLOSED/"FINAL_MANIFEST.sha256")=="c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a"
assert h(CLOSED_REF/"FINAL_MANIFEST.sha256")=="c856fae641e355a94684c1c9304ead831d213ecc90f579c0a751c93002c10562"
spec=importlib.util.spec_from_file_location("rep2_referee_design",DESIGN/"generate_design.py");assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
engine=module.load_engine();module.configure_engine(engine);raw,groups=engine.orbit_ledger();ordered=sorted(groups.items())
assert len(raw)==972 and len(ordered)==162 and all(len(m)==6 for _,m in ordered)
assert sum(rep[4]=="y" for rep,_ in ordered)==81 and sum(rep[4]=="z" for rep,_ in ordered)==81
census=json.loads((RUN/"canonical_census.json").read_text());assert census["counts"]=={"raw":972,"canonical_groups":162,"members_each":6,"y_groups":81,"z_groups":81}
epilogue='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
regenerated=[]
for gid,(representative,members) in enumerate(ordered):
 design=module.build_program(engine,representative);assert design.endswith("quit;\n") and design.count("quit;")==1
 q=design[:-len("quit;\n")]+epilogue;qb=q.encode()
 regenerated.append({"group_id":gid,"canonical_chart":list(representative),"family":representative[4],"raw_members":[list(x) for x in sorted(members)],"raw_member_count":len(members),"exact_Q_source_sha256":hashlib.sha256(qb).hexdigest(),"exact_Q_source_bytes":len(qb)})
assert regenerated==census["groups"]
matches=[x for x in regenerated if x["exact_Q_source_sha256"]==h(CLOSED/"rep2_corrected_all_equal_y_Q.sing")]
assert len(matches)==1 and matches[0]["group_id"]==0 and matches[0]["canonical_chart"]==[0,0,0,0,"y",0,0,1]
assert census["closed_group_identification"]=={"group_id":0,"method":"unique exact-Q source SHA match to independently sealed all-equal-y chart","chart":[0,0,0,0,"y",0,0,1],"source_sha256":"5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf","first_seal_manifest_sha256":"c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a","second_referee_manifest_sha256":"c856fae641e355a94684c1c9304ead831d213ecc90f579c0a751c93002c10562"}
ledger=json.loads((RUN/"source_ledger.json").read_text());lanes=ledger["lanes"]
assert ledger["selection"]=={"excluded_proven_group_ids":[0],"rule":"25 lowest canonical group IDs after excluding exactly the sealed all-equal-y group","selected_group_ids":list(range(1,26))}
assert [x["group_id"] for x in lanes]==list(range(1,26)) and [x["ordinal"] for x in lanes]==list(range(1,26))
for lane in lanes:
 source=RUN/lane["source_path"];gid=lane["group_id"];entry=regenerated[gid]
 assert lane["canonical_chart"]==entry["canonical_chart"] and lane["family"]==entry["family"]
 assert lane["variables"]==91 and lane["generators"]==6577
 assert h(source)==lane["source_sha256"]==entry["exact_Q_source_sha256"] and source.stat().st_size==lane["source_bytes"]==entry["exact_Q_source_bytes"]
 lines=source.read_text().splitlines();assert lines[2].startswith("ring r=0,") and lines[3].startswith("ideal I=")
 assert lines[-7:]==['print("INPUT_VARIABLES="+string(nvars(r)));','print("INPUT_GENERATORS="+string(size(I)));','ideal G=slimgb(I);','print("GROEBNER_SIZE="+string(size(G)));','poly remainder=reduce(1,G);','print("UNIT_REMAINDER="+string(remainder));','if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }','quit;'][-7:]
runner=(RUN/"run_first25.py").read_text()
for token in ('SELECTED = tuple(range(1, 26))','NATIVE_WALL = 240','WRAPPER_WALL = 250','RSS_CAP = 8 * 1024**3','if not unit:','"parallel": False','"relaunch": False','atomic(result_path, record)','exclusive(HERE / "BATCH_ATTEMPT.json"'):
 assert token in runner,token
for absent in ("independent_referee_acceptance.json","launch_clearance.json","BATCH_ATTEMPT.json","batch_result.json","results"):
 assert not (RUN/absent).exists(),absent
assert not list(RUN.rglob("*.tmp"))
schedule=json.loads((RUN/"held_schedule.json").read_text());assert schedule["scope"]["solver_launches"]==schedule["scope"]["result_files"]==schedule["scope"]["groups_newly_closed"]==0
out={"schema":"KRENN_X5_REP2_FIRST25_EXACT_Q_HELD_REFEREE_V1","status":"PASS_APPROVE_HELD_STRICT_REP2_FIRST25_ZERO_RUN","producer_manifest_sha256":h(RUN/"MANIFEST.sha256"),"canonical_census_sha256":h(RUN/"canonical_census.json"),"source_ledger_sha256":h(RUN/"source_ledger.json"),"runner_sha256":h(RUN/"run_first25.py"),"raw_charts":972,"canonical_groups":162,"members_each":6,"y_groups":81,"z_groups":81,"closed_group_id":0,"closed_source_sha256":h(CLOSED/"rep2_corrected_all_equal_y_Q.sing"),"selected_group_ids":list(range(1,26)),"sources_byte_identical":25,"variables_each":91,"generators_each":6577,"native_wall_seconds_each":240,"wrapper_wall_seconds_each":250,"rss_cap_bytes_each":8589934592,"strict_sequential":True,"stop_first":True,"parallel":False,"skip":False,"reorder":False,"relaunch":False,"solver_runs":0,"mathematical_coverage_added":False,"rep2_closed":False,"conjecture_closed":False,"approval":"HELD_ONLY_NO_LAUNCH"}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
