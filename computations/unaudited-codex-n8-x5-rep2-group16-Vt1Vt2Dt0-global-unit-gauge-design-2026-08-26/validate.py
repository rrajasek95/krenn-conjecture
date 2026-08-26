#!/usr/bin/env python3
"""Static replay of the unlaunched third-chart exact gauge design."""
from __future__ import annotations
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
UP=ROOT/"computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((HERE/"results_design.json").read_text())
assert d["status"]=="PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE"
assert d["source"]["sha256"]==sha(UP/"sources/rep2_group016_67_Vt1_Vt2_Dt0_runtime_Q.sing")=="819ba657d4e7ad27e0348613b72c84bfca517376bfab6158b50c07a09e87509b"
assert d["grading"]["rank"]==58 and d["grading"]["nullity"]==6
c=d["cover"]
assert c["maximal_primitive_global_gauge_coordinates"]==["it0","sat"]
assert c["maximal_primitive_global_gauge_weight_rows"]==[[0,0,0,0,0,1],[0,0,0,0,1,0]]
assert c["global_gauge_assignments_including_inverse_partners"]=={"it0":1,"sat":1,"t0":1}
assert set(c["global_unit_witnesses"])=={"it0","sat","t0"}
s=c["sources"][0];p=HERE/s["path"]
assert sha(p)==s["sha256"]=="bb9c275233ff981a5d3f5dbbe5ac20ed49bc652c1b7f35b34c9cc5eeab3c4884"
t=p.read_text();vs=t.split("ring r=0,(",1)[1].split("),dp;",1)[0].split(",");body=t.split("ideal I=",1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0]
depth=0;gens=1
for ch in body:
    if ch=="(":depth+=1
    elif ch==")":depth-=1
    elif ch=="," and depth==0:gens+=1
assert depth==0 and len(vs)==s["variables"]==61 and gens==s["generators"]==6568
assert not ({"it0","sat","t0"}&set(vs));assert s["total_terms"]==659385 and s["inactive"]==[]
b=d["batch_stop_binding"]
assert b["batch_result_sha256"]==sha(UP/"batch_result.json")=="5b3250c4ee21d1392e148f4094bf6095bd39e94a835799cc6b3d643a79e6b510"
assert b["terminal_manifest_sha256"]==sha(UP/"TERMINAL_MANIFEST.sha256")=="5d9fdcbfea5aab0245ffde35ab62b4ab3626c99d8b88d09b5a8554ae8bd49551"
assert b["skipped_after_stop"]==["Vt1_Vt2_Dt0"] and b["this_chart_previously_launched"] is False
subprocess.run([sys.executable,str(HERE/"test_design.py")],cwd=HERE,capture_output=True,text=True,check=True,timeout=15,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
h=json.loads((HERE/"results_hostiles.json").read_text());assert h["status"]=="PASS" and h["hostile_count"]==12 and h["solver_runs"]==0
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"))
print(json.dumps({"status":"PASS_EXACT_GLOBAL_UNIT_GAUGE_REPLAY","shape":[61,6568],"hostiles":12,"solver_runs":0},sort_keys=True))
