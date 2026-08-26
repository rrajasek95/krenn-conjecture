#!/usr/bin/env python3
from __future__ import annotations
import copy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;base=json.loads((HERE/"results_design.json").read_text())
def accepted(r):
    try:
        assert r["status"]=="STRUCTURAL_UNIT_AFTER_GRAPH_ELIMINATION"
        assert r["parent"]["source_shape"]==[57,6015,111546]
        ledger=r["ledger"];assert len(ledger)==11
        assert [s["kind"] for s in ledger]==["forced_zero","forced_zero","monic_graph","monic_graph","monic_graph","monic_graph","monic_graph","monic_graph","global_unit_torus_gauge","forced_zero","forced_zero"]
        assert [s.get("variable") for s in ledger[:8]]==["a14_11","a14_21","a14_12","a14_22","a14_02","a14_10","a14_20","a14_00"]
        assert ledger[8]["coordinates"]==["a17_01"] and ledger[8]["assignments"]=={"a17_01":1}
        assert ledger[8]["grading_rank_nullity"]==[45,4]
        assert ledger[9]["variable"]=="a26_11" and ledger[10]["variable"]=="a26_01"
        assert ledger[10]["unit_after"] is True
        assert [r["final"][k] for k in ("variables","generators","terms","maximum_terms")]==[46,1,1,1]
        assert r["final"]["sha256"]=="d2fa03ba377d019d8fcfe20a8cb61894afd32f3e0cfe9d2f5db316d2d83f8df0"
        g=r["global_cover"];assert g["strict_leaf_closed"] is True and g["nonempty_leaf_count_before_after"]==[3,2]
        assert len(g["remaining_nonempty_leaves"])==2
        c=r["conclusion"];assert c["all_monic_graph_reductions_exhausted"] is True and c["mathematical_coverage"] is True and c["singular_runs"]==0
        return True
    except (AssertionError,KeyError,TypeError):return False
assert accepted(base);bad=[]
def m(path,value):
    r=copy.deepcopy(base);q=r
    for key in path[:-1]:q=q[key]
    q[path[-1]]=value;bad.append(r)
m(("status",),"HELD");m(("parent","source_shape"),[57,6014,111546]);m(("ledger",0,"kind"),"monic_graph")
m(("ledger",1,"variable"),"a14_22");m(("ledger",8,"coordinates"),["a17_02"]);m(("ledger",8,"grading_rank_nullity"),[44,4])
m(("ledger",9,"variable"),"a26_01");m(("ledger",10,"unit_after"),False);m(("final","variables"),47)
m(("final","generators"),2);m(("final","terms"),2);m(("final","sha256"),"0"*64)
m(("global_cover","strict_leaf_closed"),False);m(("global_cover","nonempty_leaf_count_before_after"),[3,3])
m(("conclusion","all_monic_graph_reductions_exhausted"),False);m(("conclusion","mathematical_coverage"),False);m(("conclusion","singular_runs"),1)
assert all(not accepted(r) for r in bad)
out={"schema":"KRENN_X5_REP2_GROUP16_STRICT_SURVIVOR_EXHAUSTIVE_REDUCTION_HOSTILES_V1","status":"PASS","hostile_count":len(bad),"solver_runs":0}
(HERE/"results_hostiles.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
