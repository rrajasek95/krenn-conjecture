#!/usr/bin/env python3
"""Exact residual-torus analysis of the 61-variable V(t1,t2) D(t0) gauge slice."""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
TEMPLATE=ROOT/"computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/analyze.py"
TEMPLATE_MANIFEST=ROOT/"computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/MANIFEST.sha256"
PARENT=ROOT/"computations/unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-global-unit-gauge-design-2026-08-26"
SOURCE=PARENT/"sources/rep2_group16_Dt1_it0_GLOBAL_UNIT_GAUGE_Q_design.sing"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(TEMPLATE_MANIFEST)=="aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be"
assert sha(PARENT/"MANIFEST.sha256")=="02e228e1f8eaaea3abf063c1c9534a1245b98f50743155c85eae619dc59cfbfe"
assert sha(SOURCE)=="bb9c275233ff981a5d3f5dbbe5ac20ed49bc652c1b7f35b34c9cc5eeab3c4884"
program=TEMPLATE.read_text()
program=program.replace("HERE = Path(__file__).resolve().parent",f"HERE = Path({str(HERE)!r})",1)
program=program.replace("ROOT = HERE.parents[1]",f"ROOT = Path({str(ROOT)!r})",1)
program=program.replace('UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"',f"UPSTREAM = Path({str(PARENT)!r})",1)
program=program.replace('SOURCE = UPSTREAM / "sources/rep2_group016_67_Dt1_runtime_Q.sing"','SOURCE = UPSTREAM / "sources/rep2_group16_Dt1_it0_GLOBAL_UNIT_GAUGE_Q_design.sing"',1)
program=program.replace('SOURCE_SHA = "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244"','SOURCE_SHA = "bb9c275233ff981a5d3f5dbbe5ac20ed49bc652c1b7f35b34c9cc5eeab3c4884"',1)
program=program.replace('assert sha(UPSTREAM / "results/lane2_Dt1.json") == TIMEOUT_RESULT_SHA','',1)
program=program.replace('assert sha(UPSTREAM / "TERMINAL_MANIFEST.sha256") == TIMEOUT_MANIFEST_SHA','',1)
program=program.replace('assert len(variables) == 64 and len(equations) == len(set(equations)) == 6569','assert len(variables) == 61 and len(equations) == len(set(equations)) == 6568',1)
program=program.replace('"timeout_binding": {"result_sha256": sha(UPSTREAM / "results/lane2_Dt1.json"), "terminal_manifest_sha256": sha(UPSTREAM / "TERMINAL_MANIFEST.sha256"), "rerun": False},','"timeout_binding": {"result_sha256": "not_applicable", "terminal_manifest_sha256": "not_applicable", "rerun": False},',1)
namespace={"__name__":"__rep2_residual_exact_analyzer__","__file__":str(HERE/"_pinned_template_replay.py")}
exec(compile(program,namespace["__file__"],"exec"),namespace)
p=HERE/"results_design.json";d=json.loads(p.read_text())
assert d["status"]=="PASS_EXACT_PRIMITIVE_TORUS_DV_COVER"
d["schema"]="KRENN_X5_REP2_GROUP16_VT1VT2DT0_RESIDUAL_TORUS_DESIGN_V1"
d.pop("timeout_binding")
d["parent_binding"]={"manifest_sha256":sha(PARENT/"MANIFEST.sha256"),"source_sha256":sha(SOURCE),"parent_chart_previously_launched":False}
d["conclusion"]={"singular_runs":0,"mathematical_coverage":False,"parent_chart_previously_launched":False,"exhaustive_two_chart_cover":True}
tmp=p.with_suffix(".json.tmp");tmp.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n");os.replace(tmp,p)
print(json.dumps({"status":d["status"],"grading":[d["grading"]["rank"],d["grading"]["nullity"]],"selected":d["cover"]["selected"],"sources":[[s["variables"],s["generators"],s["total_terms"]] for s in d["cover"]["sources"]],"solver_runs":0},sort_keys=True))
