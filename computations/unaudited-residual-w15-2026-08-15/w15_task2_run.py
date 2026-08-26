#!/usr/bin/env python3
"""W15 -- Phi-forcing search over m=20..28 using EFFECTIVELY-CLEAN words
(fibre contained in the full-block matchings) and monomial-multiplier
certificates.  char=32003 is a labelled SEARCH screen; every reported kill
is re-decided over Q."""
import json, os, sys, time
from itertools import product
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import W8_IMMUNE, single_cell_activity
from w15_forcing import full_matchings, extras
from w15_compressed import decide_pow, eff_clean_words

HERE = os.path.dirname(os.path.abspath(__file__))
L4 = tuple(product(range(3), repeat=4))
res = {}
ms = [int(a) for a in sys.argv[1:]] or sorted(W8_IMMUNE)
SCREEN = 32003

for m in ms:
    T = W8_IMMUNE[m]; fm = full_matchings(T); EC = set(eff_clean_words(T))
    yfree = [y for y in L4 if all(tuple(x)+tuple(y) in EC for x in L4)]
    cands = []
    for c in range(3):
        if not extras(T, (c,)*4, (c,)*4, fm):
            cands.append((((c,)*4, (c,)*4), "constant", 0))
    for k in (1, 2):
        if cands: break
        got = [(x, y) for x in L4 for y in L4
               if len(set(tuple(x)+tuple(y))) > 1 and len(extras(T,x,y,fm)) == k]
        got.sort(key=lambda t: -sum(1 for x in L4 if tuple(x)+tuple(t[1]) in EC))
        cands += [(t, f"mixed-{k}extra", k) for t in got[:6]]
    entry = {"n_full_matchings": len(fm), "n_eff_clean_mixed":
             sum(1 for w in EC if len(set(w)) > 1), "n_yfree": len(yfree),
             "trials": [], "verdict": "open"}
    print(f"=== m={m} |F|={len(fm)} yfree={len(yfree)} targets={len(cands)}", flush=True)
    hit = False
    for (tgt, kind, k) in cands:
        XO = [x for x in L4 if x != tgt[0] and tuple(x)+tuple(tgt[1]) in EC]
        for nx, ny in ((2,2),(3,3),(4,4),(6,4),(8,6)):
            if nx > len(XO) or ny > len(yfree): continue
            X0 = [tgt[0]] + XO[:nx]; Y0 = [tgt[1]] + [y for y in yfree if y != tgt[1]][:ny]
            eqw = [tuple(x)+tuple(y) for x in X0 for y in Y0
                   if (tuple(x),tuple(y)) != (tuple(tgt[0]),tuple(tgt[1]))
                   and tuple(x)+tuple(y) in EC and len(set(tuple(x)+tuple(y))) > 1]
            t0 = time.time()
            kf, na, nc, ne, raw = decide_pow(T, eqw, tuple(tgt[0])+tuple(tgt[1]),
                                             kmax=4, timeout=400, char=SCREEN)
            dt = time.time()-t0
            kq = None
            if kf:
                kq, na, nc, ne, raw = decide_pow(T, eqw, tuple(tgt[0])+tuple(tgt[1]),
                                                 kmax=max(4,kf+2), timeout=900, char=0)
            print(f"   {kind} x*={tgt[0]} y*={tgt[1]} nx={nx} ny={ny}: "
                  f"k_Fp={kf} k_Q={kq} atoms={na} cells={nc} eqs={ne} {dt:.1f}s", flush=True)
            entry["trials"].append(dict(kind=kind, xstar=list(tgt[0]), ystar=list(tgt[1]),
                                        extras=k, nx=nx, ny=ny, k_screen=kf, k_exact=kq,
                                        atoms=na, cells=nc, eqs=ne, seconds=round(dt,1)))
            if kq:
                hit = True
                entry["verdict"] = ("killed:constant-word-vanishes" if kind=="constant"
                                    else ("killed:single-extra-monomial-vanishes" if k==1
                                          else "phi-forced:binomial-collapse"))
                entry["killing_target"] = dict(x=list(tgt[0]), y=list(tgt[1]), kind=kind,
                                               extras=k, k_exact=kq,
                                               eq_words=[list(w) for w in eqw])
                break
        if hit: break
    print(f"   VERDICT m={m}: {entry['verdict']}", flush=True)
    res[m] = entry
    json.dump(res, open(os.path.join(HERE,"results_task2_run_%s.json"%("_".join(map(str,ms)))),"w"), indent=1)
print("DONE")
