import sys, time
sys.dont_write_bytecode = True
import m2thm as T
print("step1 identity:", T.check_step1_identity())
cfgs = T.enum_configs((2,3))
print("orbits (dims in {2,3}):", len(cfgs))
from collections import Counter
print(Counter(tuple(sorted(d for d,_ in c)) for c in cfgs.values()))
# time one (2,2,2,2) config and one (3,3,3,3) config
for want in [(2,2,2,2),(3,3,3,3),(2,2,3,3)]:
    for k,c in sorted(cfgs.items()):
        if tuple(sorted(d for d,_ in c))==want:
            t0=time.time(); r=T.run_cfg(c, char=0, timeout=300); print(want, r); break
