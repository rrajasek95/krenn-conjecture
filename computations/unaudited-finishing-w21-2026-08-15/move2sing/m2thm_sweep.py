#!/usr/bin/env python3
"""Sweep all 53 chart-orbits (dims in {2,3}) of the W21-M2 theorem."""
import sys, json, time
sys.dont_write_bytecode = True
import m2thm as T
char = int(sys.argv[1]); tmo = int(sys.argv[2])
cfgs = T.enum_configs((2,3))
res=[]
for n,(k,c) in enumerate(sorted(cfgs.items()),1):
    r = T.run_cfg(c, char=char, timeout=tmo)
    r["dims"]=[d for d,_ in c]
    res.append(r)
    print("[%2d/%2d] dims=%s charts=%s -> %s unit=%s dim=%s %.1fs"
          %(n,len(cfgs),r["dims"],[list(rr) for _,rr in c],r["status"],r.get("unit"),r.get("dim"),r["seconds"]), flush=True)
    json.dump(res, open("results_thm_sweep_c%d.json"%char,"w"), indent=1, default=str)
nu=sum(1 for r in res if r.get("unit")); nt=sum(1 for r in res if r["status"]!="OK")
print("SWEEP char=%d: %d configs, %d UNIT(infeasible), %d non-unit, %d timeout"%(char,len(res),nu,len(res)-nu-nt,nt))
