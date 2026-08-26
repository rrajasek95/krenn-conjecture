#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PARENT=ROOT/"computations/unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-global-unit-gauge-design-2026-08-26"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.loads((HERE/"results_design.json").read_text())
assert d["status"]=="PASS_EXACT_PRIMITIVE_TORUS_DV_COVER" and d["grading"]["rank"]==57 and d["grading"]["nullity"]==4
assert d["source"]["sha256"]==sha(PARENT/"sources/rep2_group16_Dt1_it0_GLOBAL_UNIT_GAUGE_Q_design.sing")=="bb9c275233ff981a5d3f5dbbe5ac20ed49bc652c1b7f35b34c9cc5eeab3c4884"
assert d["parent_binding"]["manifest_sha256"]==sha(PARENT/"MANIFEST.sha256")=="02e228e1f8eaaea3abf063c1c9534a1245b98f50743155c85eae619dc59cfbfe"
c=d["cover"];assert c["selected"]["coordinate"]=="a57_01" and c["selected"]["weight"]==1 and c["root_free"] is True
expected={"D1":("e7782a1ebac09701d8cba3ec0938cb5e2a935fa18e004ea3d7ca04dfba58e1cc",60,6568,659385),"V0":("15ee90435e4f6148c708525b757de4f8b6ff9a1aba0a66fc2402b8846ffb964c",60,6568,174407)}
for s in c["sources"]:
    h,n,g,t=expected[s["branch"]];p=HERE/s["path"];assert sha(p)==s["sha256"]==h and (s["variables"],s["generators"],s["total_terms"])==(n,g,t)
    text=p.read_text();vs=text.split("ring r=0,(",1)[1].split("),dp;",1)[0].split(",");body=text.split("ideal I=",1)[1].split(';\nprint("INPUT_VARIABLES=',1)[0]
    depth=0;gens=1
    for ch in body:
        if ch=="(":depth+=1
        elif ch==")":depth-=1
        elif ch=="," and depth==0:gens+=1
    assert depth==0 and len(vs)==n and gens==g and "a57_01" not in vs
subprocess.run([sys.executable,str(HERE/"test_design.py")],cwd=HERE,capture_output=True,text=True,check=True,timeout=15,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
h=json.loads((HERE/"results_hostiles.json").read_text());assert h["status"]=="PASS" and h["hostile_count"]==12 and h["solver_runs"]==0
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"));print(json.dumps({"status":"PASS_EXACT_RESIDUAL_TORUS_DV_REPLAY","sources":2,"hostiles":12,"solver_runs":0},sort_keys=True))
