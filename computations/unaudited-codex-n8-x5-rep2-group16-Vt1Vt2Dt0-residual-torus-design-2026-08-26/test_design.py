#!/usr/bin/env python3
from __future__ import annotations
import copy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;base=json.loads((HERE/"results_design.json").read_text())
def ok(d):
    try:
        assert d["status"]=="PASS_EXACT_PRIMITIVE_TORUS_DV_COVER"
        assert d["source"]["variables"]==61 and d["source"]["generators"]==6568
        assert d["grading"]["rank"]==57 and d["grading"]["nullity"]==4
        c=d["cover"];assert c["identity"]=="D(q) union V(q)" and c["root_free"] is True
        assert c["selected"]=={"basis_index":2,"coordinate":"a57_01","objective":[659385,833792,6568],"weight":1}
        assert c["global_unit_witnesses"]=={} and len(c["sources"])==2
        assert [(s["branch"],s["variables"],s["generators"],s["total_terms"]) for s in c["sources"]]==[("D1",60,6568,659385),("V0",60,6568,174407)]
        assert d["parent_binding"]["parent_chart_previously_launched"] is False
        assert d["conclusion"]["exhaustive_two_chart_cover"] is True and d["conclusion"]["singular_runs"]==0
        return True
    except (AssertionError,KeyError,TypeError):return False
assert ok(base);bad=[]
def m(path,val):
    d=copy.deepcopy(base);q=d
    for k in path[:-1]:q=q[k]
    q[path[-1]]=val;bad.append(d)
m(("grading","rank"),56);m(("grading","nullity"),3);m(("cover","root_free"),False)
m(("cover","selected","basis_index"),1);m(("cover","selected","coordinate"),"a57_02");m(("cover","selected","weight"),2)
m(("cover","sources"),[]);m(("cover","sources",0,"variables"),61);m(("cover","sources",1,"generators"),6567)
m(("parent_binding","parent_chart_previously_launched"),True);m(("conclusion","exhaustive_two_chart_cover"),False);m(("conclusion","singular_runs"),1)
assert all(not ok(d) for d in bad)
out={"schema":"KRENN_X5_REP2_GROUP16_VT1VT2DT0_RESIDUAL_TORUS_HOSTILES_V1","status":"PASS","hostile_count":len(bad),"solver_runs":0}
(HERE/"results_hostiles.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
