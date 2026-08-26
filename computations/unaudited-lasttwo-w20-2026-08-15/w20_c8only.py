#!/usr/bin/env python3
"""W20 -- the C_8 member alone under the constants-pinned probe (leaner run).
UNAUDITED.  FLOATS FOR SEARCH ONLY."""
import os,sys,json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w20_core as C
from w20_c8search2 import run
res={"_header":"UNAUDITED W20 C_8 constants-pinned probe (lean). FLOATS FOR SEARCH ONLY."}
res["C8"]=run(C.C8_MEMBER,list(C.MIXED),"C_8 member",(1,2,3,4,5,6),iters=70)
res["best"]=min(r["min_residual"] for r in res["C8"])
res["any_converged"]=any(r["converged"] for r in res["C8"])
print("C_8: best %.4e  any converged %s"%(res["best"],res["any_converged"]),flush=True)
json.dump(res,open(os.path.join(HERE,"results_c8only.json"),"w"),indent=1,default=str)
