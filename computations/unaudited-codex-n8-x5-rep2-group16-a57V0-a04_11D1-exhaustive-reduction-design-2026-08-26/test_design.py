#!/usr/bin/env python3
from __future__ import annotations
import copy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;base=json.loads((HERE/"results_design.json").read_text())
def ok(r):
 try:
  assert r["status"]=="HELD_EXACT_TWO_BRANCH_PRIMITIVE_TORUS_COVER" and r["parent"]["source_shape"]==[59,6568,174407]
  assert len(r["ledger"])==10 and all(s["kind"]=="monic_graph" for s in r["ledger"])
  assert [s["variable"] for s in r["ledger"]]==["a26_00","a14_11","a14_12","a14_21","a14_22","a14_01","a14_02","a14_10","a14_20","a14_00"]
  assert [r["final"][k] for k in ("variables","generators","terms")]==[49,6558,148912]
  p=r["final_probe"];assert p["status"]=="PASS_EXACT_PRIMITIVE_TORUS_DV_COVER" and p["grading"]["rank"]==46 and p["grading"]["nullity"]==3
  assert p["cover"]["selected"]=={"basis_index":2,"coordinate":"a04_12","objective":[140394,266710,5994],"weight":-1}
  assert [(s["branch"],s["variables"],s["generators"],s["total_terms"],s["unit_ideal_structural"]) for s in p["cover"]["sources"]]==[("D1",48,5994,140394,False),("V0",48,5913,126316,False)]
  g=r["global_cover"];assert g["strict_leaf_closed"] is False and g["nonempty_leaf_count_before_after"]==[2,3] and len(g["remaining_nonempty_leaves"])==3
  assert r["conclusion"]["all_monic_graph_reductions_exhausted"] is True and r["conclusion"]["mathematical_coverage"] is False and r["conclusion"]["singular_runs"]==0
  return True
 except (AssertionError,KeyError,TypeError):return False
assert ok(base);bad=[]
def m(p,v):
 r=copy.deepcopy(base);q=r
 for k in p[:-1]:q=q[k]
 q[p[-1]]=v;bad.append(r)
m(("status",),"PASS");m(("parent","source_shape"),[59,6567,174407]);m(("ledger",0,"variable"),"a26_01");m(("final","variables"),50)
m(("final_probe","grading","rank"),45);m(("final_probe","cover","selected","coordinate"),"a04_21");m(("final_probe","cover","sources",0,"unit_ideal_structural"),True)
m(("global_cover","strict_leaf_closed"),True);m(("global_cover","nonempty_leaf_count_before_after"),[2,2]);m(("conclusion","all_monic_graph_reductions_exhausted"),False);m(("conclusion","mathematical_coverage"),True);m(("conclusion","singular_runs"),1)
assert all(not ok(r) for r in bad)
out={"schema":"KRENN_X5_REP2_GROUP16_A57V0_A04_11D1_EXHAUSTIVE_REDUCTION_HOSTILES_V1","status":"PASS","hostile_count":len(bad),"solver_runs":0}
(HERE/"results_hostiles.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
