#!/usr/bin/env python3
"""LEDGER 13(b): run the SAME pipeline on KNOWN-FEASIBLE relaxations and check
it never reports the unit ideal.  Known feasible because W20 exhibited an
all-nonzero (1,1,2,2) solution and because the (1,1,1,1) rank-one family
(A_ij = K (x) s with per of the 4x4 scalar matrix = 0) is all-nonzero."""
import sys, json
sys.dont_write_bytecode = True
import m2thm as T
tests = [((1,(0,)),(1,(0,)),(1,(0,)),(1,(0,))),
         ((1,(0,)),(1,(1,)),(2,(0,2)),(2,(1,3))),
         ((1,(2,)),(1,(3,)),(2,(0,1)),(2,(2,3))),
         ((1,(0,)),(1,(2,)),(3,(0,1,2)),(3,(0,1,3))),
        ]
out=[]
for c in tests:
    r = T.run_cfg(c, char=0, timeout=100); r["dims"]=[d for d,_ in c]
    print(r["dims"], [list(rr) for _,rr in c], "->", r["status"], "unit=",r.get("unit"),
          "dim=",r.get("dim"), "%.1fs"%r["seconds"], flush=True)
    out.append(r)
json.dump(out, open("results_thm_falsekill.json","w"), indent=1, default=str)
nf=sum(1 for r in out if r.get("unit") is True); nn=sum(1 for r in out if r.get("unit") is False)
print("FEASIBLE systems put through the pipeline: %d ; reported feasible: %d ; FALSE KILLS: %d"
      %(len(out), nn, nf))
