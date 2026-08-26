import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lasttwo-w20-2026-08-15")
import w20_core as C
for m in (25,26,27,28):
    T = C.W8_IMMUNE[m]
    gam = C.gamma_edges(T)
    fullm = C.full_pm_indices(T)
    clean = [w for w in C.MIXED if not C.extras_at(T,w,fullm)]
    deg = {v: sum(1 for e in gam if v in e) for v in range(8)}
    print("m=%d |Gamma|=%d |F|=%d clean=%d degs=%s" % (m, len(gam), len(fullm), len(clean), [deg[v] for v in range(8)]))
    print("   Gamma:", gam)
    print("   matchings inside:", [C.PMS[i] for i in fullm])
# C8
T = C.C8_MEMBER
gam = C.gamma_edges(T); fullm=C.full_pm_indices(T)
clean=[w for w in C.MIXED if not C.extras_at(T,w,fullm)]
print("C8: |Gamma|=%d |F|=%d clean=%d" % (len(gam), len(fullm), len(clean)), gam)
