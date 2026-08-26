#!/usr/bin/env python3
"""Hostile checks for the exact V(t1,t2) intersect D(t0) gauge."""
from __future__ import annotations
import copy, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
base=json.loads((HERE/"results_design.json").read_text())
def accepts(d):
    try:
        assert d["status"]=="PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE"
        assert d["source"]["variables"]==64 and d["source"]["generators"]==6569
        assert d["grading"]["rank"]==58 and d["grading"]["nullity"]==6
        c=d["cover"]
        assert c["maximal_primitive_global_gauge_coordinates"]==["it0","sat"]
        assert c["maximal_primitive_global_gauge_weight_rows"]==[[0,0,0,0,0,1],[0,0,0,0,1,0]]
        assert c["global_gauge_assignments_including_inverse_partners"]=={"it0":1,"sat":1,"t0":1}
        assert c["global_unit_witnesses"]["sat"]["equation_indices"]==[6567]
        assert c["global_unit_witnesses"]["it0"]["equation_indices"]==[6568]
        assert len(c["sources"])==1 and c["sources"][0]["variables"]==61 and c["sources"][0]["generators"]==6568
        b=d["batch_stop_binding"]
        assert b["skipped_after_stop"]==["Vt1_Vt2_Dt0"] and b["this_chart_previously_launched"] is False
        assert d["conclusion"]["singular_runs"]==0 and d["conclusion"]["this_chart_previously_launched"] is False
        return True
    except (AssertionError,KeyError,TypeError): return False
assert accepts(base)
mut=[]
def m(path,value):
    d=copy.deepcopy(base); q=d
    for key in path[:-1]:q=q[key]
    q[path[-1]]=value;mut.append(d)
m(("grading","rank"),57);m(("grading","nullity"),5)
m(("cover","maximal_primitive_global_gauge_coordinates"),["sat"])
m(("cover","maximal_primitive_global_gauge_weight_rows"),[[0,0,0,0,2,0]])
m(("cover","global_gauge_assignments_including_inverse_partners"),{"it0":1,"sat":1})
m(("cover","global_unit_witnesses","sat","equation_indices"),[])
m(("cover","global_unit_witnesses","it0","equation_indices"),[0])
m(("cover","sources"),[]);m(("cover","sources",0,"variables"),62)
m(("batch_stop_binding","skipped_after_stop"),[])
m(("batch_stop_binding","this_chart_previously_launched"),True)
m(("conclusion","singular_runs"),1)
assert all(not accepts(d) for d in mut)
out={"schema":"KRENN_X5_REP2_GROUP16_VT1VT2DT0_GAUGE_HOSTILES_V1","status":"PASS","hostile_count":len(mut),"solver_runs":0}
(HERE/"results_hostiles.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps(out,sort_keys=True))
