#!/usr/bin/env python3
"""Prepare the missing p32003 solver source; no process launch."""
import hashlib, json, os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
Q=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25/rank1_orbit0_i0_I0_J0_Q.sing"
PLAN=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25/STAGED_PILOT_HELD_PLAN.json"
PINS={Q:"1d9875cab81417094d51193862f40097b1c03e4816aedd8ceaf07a917eeb248b",PLAN:"95120b83be0d16fb16b7814556c676caa7a01c1436e85ed884db98a210571c34"}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for path,expected in PINS.items():assert sha(path)==expected,(path,sha(path),expected)
text=Q.read_text();assert text.count("ring r=0,")==1 and text.count("quit;\n")==1
pinned=text.replace("ring r=0,","ring r=32003,")
assert hashlib.sha256(pinned.encode()).hexdigest()=="b70098251cfe8aceb845c1a3c2af92a5ae944e9bfcb1c611d21adada8edd44cb"
epilogue='''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
execution=pinned.replace("quit;\n",epilogue);assert execution.count("slimgb(I)")==1
path=HERE/"rank1_orbit0_p32003_execute.sing";tmp=path.with_suffix(".sing.tmp");tmp.write_text(execution);os.replace(tmp,path)
record={"schema":"KRENN_X5_RECTANGLE_RANK1_ORBIT0_EXECUTION_SOURCE_AMENDMENT_V1","status":"PREPARED_NOT_RUN_REQUIRES_SUPERSEDING_CLEARANCE","held_plan_sha256":PINS[PLAN],"Q_source_sha256":PINS[Q],"held_p32003_no_solve_sha256":"b70098251cfe8aceb845c1a3c2af92a5ae944e9bfcb1c611d21adada8edd44cb","sole_semantic_diff":"replace terminal quit with slimgb/reduce/status epilogue","execution_source":path.name,"execution_source_sha256":sha(path),"execution_source_bytes":path.stat().st_size,"solver_launches":0}
out=HERE/"EXECUTION_SOURCE_AMENDMENT.json";tmp=out.with_suffix(".json.tmp");tmp.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n");os.replace(tmp,out)
print(json.dumps(record,sort_keys=True))
