import sys, time, json
sys.dont_write_bytecode = True
import m2thm as T
# FALSE-KILL CONTROL: dimension types that ARE feasible must come back non-unit.
tests = [((1,(0,)),(1,(0,)),(1,(0,)),(1,(0,))),          # (1,1,1,1)
         ((1,(0,)),(1,(1,)),(2,(0,1)),(2,(0,1))),        # (1,1,2,2)  = W20 type
         ((1,(0,)),(1,(1,)),(2,(0,2)),(2,(1,3))),        # (1,1,2,2) other charts
         ((1,(2,)),(1,(3,)),(2,(0,1)),(2,(2,3))),
         ((1,(0,)),(2,(0,1)),(2,(0,1)),(2,(0,1))),       # (1,2,2,2)
        ]
out=[]
for c in tests:
    r = T.run_cfg(c, char=0, timeout=90)
    r["dims"]=[d for d,_ in c]
    print(r["dims"], [list(rr) for _,rr in c], "->", r["status"], "unit=",r.get("unit"), "dim=",r.get("dim"), "%.1fs"%r["seconds"], flush=True)
    out.append(r)
json.dump(out, open("results_thm_falsekill.json","w"), indent=1, default=str)
nfalse = sum(1 for r in out if r.get("unit") is True)
print("FALSE KILLS on known-feasible dimension types: %d (must be 0); tested %d"%(nfalse,len(out)))
