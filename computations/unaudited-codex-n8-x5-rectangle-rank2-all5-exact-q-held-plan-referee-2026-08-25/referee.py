#!/usr/bin/env python3
"""Independent static referee for the held all-five rank-two schedule."""
from __future__ import annotations
import copy,hashlib,json,os,re
from pathlib import Path
if not __debug__:raise RuntimeError("assertions required")
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];COMP=ROOT/"computations"
PLAN=COMP/"unaudited-codex-n8-x5-rectangle-rank2-all5-exact-q-held-plan-2026-08-25"
DESIGN=COMP/"unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25"
DESIGN_REF=COMP/"unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25"
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
PINS={PLAN/"HELD_PLAN.json":"0b0751748c3f19daa7635dae395d109c441a64c57243336d9e19c44546189b2f",PLAN/"FINAL_MANIFEST.sha256":"61b90e0976729a61a576aee55af309b3c17adac1973349821bd34b7f3c408dff",DESIGN/"MANIFEST.sha256":"743f3e526b21890509e32077ed5bf0c38b1240d25d475e71e2e78520445c85cf",DESIGN/"results_rank12_incidence_design.json":"96b13ad342acd0fb02c37015b86303c9d6d7d880abe0e2a4e21f5e9e1aea5a28",DESIGN_REF/"FINAL_MANIFEST.sha256":"e3e7974ae201f5915e7eeec95f7b01e3db37f0ddfe69619d00a4c1a84a92838f",DESIGN_REF/"results_referee.json":"74394ce3858867c5221743483f7b765f49c9980c9e010e9d64262b56d09c03b4"}
def census(text):
 m=re.search(r"^ring r=([^,]+),\(([^\n]+)\),dp;$",text,re.M);assert m
 variables=m.group(2).split(",");assert len(variables)==len(set(variables))==80
 body=text.split("ideal I=",1)[1].split(";",1)[0];assert body.count(",\n")+1==6574
 return m.group(1),len(variables),6574
def validate(p):
 assert p["schema"]=="KRENN_X5_RECTANGLE_RANK2_ALL5_EXACT_Q_HELD_PLAN_V1"
 assert p["status"]=="HELD_NOT_RUN_REQUIRES_INDEPENDENT_APPROVAL_AND_MANAGER_CLEARANCE" and not p["launch_authorized"]
 assert [x["ordinal"] for x in p["lanes"]]==[1,2,3,4,5] and [x["orbit"] for x in p["lanes"]]==[0,1,2,3,4]
 assert [x["raw_orbit_size"] for x in p["lanes"]]==[6,6,6,6,3] and all(x["rank"]==2 and x["diagonal"]==0 for x in p["lanes"])
 c=p["common_lane_contract"];assert c=={"field":"Q","variables":80,"generators":6574,"execution_source_bytes":553541,"native_wall_seconds":480,"wrapper_wall_seconds":510,"rss_cap_bytes":8589934592,"fresh_libproc_census_before_each_lane":True,"fresh_atomic_attempt_directory":True,"refuse_overwrite":True,"process_group_rss_observer":True,"observer_failure_terminal":True}
 e=p["execution"];assert e=={"sequential":True,"maximum_lanes":5,"exact_orbit_order":[0,1,2,3,4],"parallel_lanes":1,"stop_on_first_nonunit":True,"stop_on_first_resource_failure":True,"stop_on_first_process_failure":True,"stop_on_first_observer_failure":True,"stop_on_first_mismatch":True,"automatic_relaunch":False,"skip_or_reorder":False}
 assert p["acceptance_per_lane"]=={"returncode":0,"breach":None,"INPUT_VARIABLES":80,"INPUT_GENERATORS":6574,"GROEBNER_SIZE":1,"UNIT_REMAINDER":0,"STATUS":"UNIT_IDEAL"}
 assert p["rank1_launches_authorized"]==p["solver_launches"]==0 and not p["execution_sources_materialized"] and not p["runner_present"] and not p["fresh_clearance_present"]
def hostile(p,fn):
 q=copy.deepcopy(p);fn(q)
 try:validate(q)
 except (AssertionError,KeyError,TypeError):return True
 return False
def write(path,value):
 tmp=path.with_suffix(path.suffix+".tmp");tmp.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n");os.replace(tmp,path)
def main():
 for path,want in PINS.items():assert sha(path)==want,(path,sha(path),want)
 p=json.loads((PLAN/"HELD_PLAN.json").read_text());validate(p)
 assert p["dependencies"]=={"rank12_design_manifest_sha256":PINS[DESIGN/"MANIFEST.sha256"],"rank12_design_result_sha256":PINS[DESIGN/"results_rank12_incidence_design.json"],"rank12_referee_manifest_sha256":PINS[DESIGN_REF/"FINAL_MANIFEST.sha256"],"rank12_referee_result_sha256":PINS[DESIGN_REF/"results_referee.json"]}
 d=json.loads((DESIGN/"results_rank12_incidence_design.json").read_text());dr=json.loads((DESIGN_REF/"results_referee.json").read_text())
 assert d["status"]=="PASS_EXACT_MATERIALIZATION_NO_SOLVE" and d["scope"]=={"inputs_materialized":10,"records_closed":0,"solver_launches":0}
 assert d["counts"]["rank2"]=={"variables":80,"generators":6574,"canonical_inputs":5}
 assert dr["status"]=="PASS_EXACT_FINITE_DESIGN_NO_SOLVE_NO_CLOSURE" and dr["solver_launches"]==0 and dr["orbit_census"]["rank2_sizes"]==[6,6,6,6,3]
 entries={x["orbit_index"]:x for x in d["canonical_inputs"] if x["rank"]==2};assert sorted(entries)==[0,1,2,3,4]
 ep=p["source_derivation"]["epilogue"];assert ep==["ideal G=slimgb(I);",'print("GROEBNER_SIZE="+string(size(G)));',"poly remainder=reduce(1,G);",'print("UNIT_REMAINDER="+string(remainder));','if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }']
 lanes=[]
 for lane in p["lanes"]:
  e=entries[lane["orbit"]];assert e["row_chart"]==lane["I"] and e["column_chart"]==lane["J"] and e["raw_orbit_size"]==lane["raw_orbit_size"]
  src=DESIGN/e["path"];assert sha(src)==e["sha256"]==lane["design_source_sha256"]
  text=src.read_text();field,nv,ng=census(text);assert field=="0" and text.count("quit;")==1 and "slimgb(I)" not in text
  head,tail=text.rsplit("quit;",1);assert not tail.strip();derived=head+"\n".join(ep)+"\nquit;"+tail;raw=derived.encode()
  got=hashlib.sha256(raw).hexdigest();assert len(raw)==553541 and got==lane["execution_source_sha256"]
  lanes.append({"ordinal":lane["ordinal"],"orbit":lane["orbit"],"I":lane["I"],"J":lane["J"],"raw_orbit_size":lane["raw_orbit_size"],"field":"Q","variables":nv,"generators":ng,"design_source_sha256":sha(src),"execution_source_sha256":got,"execution_source_bytes":len(raw)})
 assert sorted(x.name for x in PLAN.iterdir())==["FINAL_MANIFEST.sha256","HELD_PLAN.json","REPORT.md","validate_plan.py"]
 tests={"reorder":hostile(p,lambda x:x["lanes"].reverse()),"skip":hostile(p,lambda x:x["lanes"].pop()),"parallel":hostile(p,lambda x:x["execution"].__setitem__("parallel_lanes",2)),"relaunch":hostile(p,lambda x:x["execution"].__setitem__("automatic_relaunch",True)),"rank1":hostile(p,lambda x:x.__setitem__("rank1_launches_authorized",1)),"premature_clearance":hostile(p,lambda x:x.__setitem__("launch_authorized",True)),"wall":hostile(p,lambda x:x["common_lane_contract"].__setitem__("wrapper_wall_seconds",511)),"observer":hostile(p,lambda x:x["execution"].__setitem__("stop_on_first_observer_failure",False))};assert all(tests.values())
 result={"schema":"KRENN_X5_RECTANGLE_RANK2_ALL5_EXACT_Q_HELD_PLAN_REFEREE_V1","status":"PASS_APPROVED_HELD_ZERO_RUNS","producer":{"plan_sha256":PINS[PLAN/"HELD_PLAN.json"],"manifest_sha256":PINS[PLAN/"FINAL_MANIFEST.sha256"]},"dependencies":p["dependencies"],"lanes":lanes,"schedule":{"exact_orbit_order":[0,1,2,3,4],"sequential":True,"maximum_lanes":5,"parallel_lanes":1,"stop_first_nonunit_timeout_resource_process_observer_or_mismatch":True,"skip_or_reorder":False,"automatic_relaunch":False,"rank1_authorized":False},"resource_contract":{"native_wall_seconds":480,"wrapper_wall_seconds":510,"rss_cap_bytes":8589934592,"fresh_libproc_census_before_each_lane":True,"atomic_distinct_attempt_per_lane":True,"observer_failure_terminal":True},"held_state":{"solver_runs":0,"execution_sources_materialized":False,"runner_present":False,"fresh_clearance_present":False,"launch_authorized":False,"requires_new_manager_clearance":True},"scope_if_executed_and_all_pass":"Closes exactly all five canonical rank-two orbits and both A12 amplitude-inactive lifts; no rank-one or broader conjecture promotion.","hostile_tests":tests,"pins":{str(k.relative_to(ROOT)):v for k,v in PINS.items()}}
 write(HERE/"results_referee.json",result);print(json.dumps({"status":result["status"],"orbits":[0,1,2,3,4],"execution_source_hashes":[x["execution_source_sha256"] for x in lanes],"solver_runs":0},sort_keys=True))
if __name__=="__main__":main()
