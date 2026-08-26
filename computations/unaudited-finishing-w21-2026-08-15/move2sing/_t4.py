import sys, time
sys.dont_write_bytecode = True
import m2thm as T
cfgs = T.enum_configs((2,3))
for want in [(3,3,3,3),(2,3,3,3),(2,2,3,3),(2,2,2,3),(2,2,2,2)]:
    for k,c in sorted(cfgs.items()):
        if tuple(sorted(d for d,_ in c))==want:
            s,nv,ne = T.script_for(c, char=32003)
            print(want, "nvars",nv,"neqs",ne, flush=True)
            t0=time.time(); r=T.run_cfg(c, char=32003, timeout=60); print("  ",r, flush=True); break
