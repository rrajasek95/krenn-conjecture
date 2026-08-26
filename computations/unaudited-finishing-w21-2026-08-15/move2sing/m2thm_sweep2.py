#!/usr/bin/env python3
"""Sweep the chart-orbits whose dim type contains at least one 3 (tractable),
over Q.  These give a DIRECT end-to-end verification of the W21-M2 theorem for
every dimension type except (2,2,2,2)."""
import sys, json, time
sys.dont_write_bytecode = True
import m2thm as T
char = int(sys.argv[1]); tmo = int(sys.argv[2])
cfgs = {k:c for k,c in T.enum_configs((2,3)).items() if any(d==3 for d,_ in c)}
res=[]
for n,(k,c) in enumerate(sorted(cfgs.items()),1):
    r = T.run_cfg(c, char=char, timeout=tmo); r["dims"]=[d for d,_ in c]
    res.append(r)
    print("[%2d/%2d] dims=%s charts=%s -> %s unit=%s dim=%s %.2fs"
          %(n,len(cfgs),r["dims"],[list(rr) for _,rr in c],r["status"],r.get("unit"),r.get("dim"),r["seconds"]), flush=True)
    json.dump(res, open("results_thm_sweep3_c%d.json"%char,"w"), indent=1, default=str)
nu=sum(1 for r in res if r.get("unit")); nt=sum(1 for r in res if r["status"]!="OK")
print("SWEEP(with a dim-3 site) char=%d: %d configs, %d UNIT(infeasible), %d non-unit, %d timeout"%(char,len(res),nu,len(res)-nu-nt,nt))
