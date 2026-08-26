#!/usr/bin/env python3
"""W15 TASK 2/3 -- Phi-forcing over the (R) family, compressed model,
monomial-multiplier certificates (decide_pow)."""
import json, os, sys, time
from itertools import product
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import W8_IMMUNE, single_cell_activity, is_clean
from w15_forcing import full_matchings, extras, y_free, x_ok
from w15_compressed import decide_pow

HERE = os.path.dirname(os.path.abspath(__file__))
L4 = tuple(product(range(3), repeat=4))
res = {}
ms = [int(a) for a in sys.argv[1:]] or sorted(W8_IMMUNE)

for m in ms:
    T = W8_IMMUNE[m]; act = single_cell_activity(T); fm = full_matchings(T)
    YF = y_free(T, act)
    cands = []
    for c in range(3):
        if not extras(T, (c,)*4, (c,)*4, fm):
            cands.append((((c,)*4, (c,)*4), "constant", 0))
    for k in (1, 2):
        if cands: break
        got = [(x, y) for x in L4 for y in L4
               if len(set(tuple(x)+tuple(y))) > 1 and len(extras(T,x,y,fm)) == k]
        got.sort(key=lambda t: -len(x_ok(T, act, t[1])))
        cands += [(t, f"mixed-{k}extra", k) for t in got[:8]]
    entry = {"n_full_matchings": len(fm), "trials": [], "verdict": "open"}
    print(f"=== m={m} |F|={len(fm)} candidate targets={len(cands)}", flush=True)
    hit = False
    for (tgt, kind, k) in cands:
        XO = [x for x in x_ok(T, act, tgt[1]) if x != tgt[0]]
        for nx in (2, 4, 8, 16):
            if nx > len(XO): continue
            X0 = [tgt[0]] + XO[:nx]; Y0 = [tgt[1]] + [y for y in YF if y != tgt[1]]
            eqw = [tuple(x)+tuple(y) for x in X0 for y in Y0
                   if (tuple(x), tuple(y)) != (tuple(tgt[0]), tuple(tgt[1]))]
            eqw = [w for w in eqw if is_clean(T, w, act)]
            t0 = time.time()
            try:
                kf, na, nc, ne, raw = decide_pow(T, eqw, tuple(tgt[0])+tuple(tgt[1]),
                                                 kmax=6, timeout=900)
            except Exception as e:
                print("   ERR", e, flush=True); kf, na, nc, ne = None, -1, -1, -1
            dt = time.time()-t0
            print(f"   {kind} x*={tgt[0]} y*={tgt[1]} nx={nx}: k={kf} "
                  f"atoms={na} cells={nc} eqs={ne} {dt:.1f}s", flush=True)
            entry["trials"].append(dict(kind=kind, xstar=list(tgt[0]), ystar=list(tgt[1]),
                                        extras=k, nx=nx, k_certificate=kf, atoms=na,
                                        cells=nc, eqs=ne, seconds=round(dt,1)))
            if kf:
                hit = True
                entry["verdict"] = ("killed:constant-word-vanishes" if kind=="constant"
                                    else ("killed:single-extra-monomial-vanishes" if k==1
                                          else "phi-forced:binomial-collapse"))
                entry["killing_target"] = dict(x=list(tgt[0]), y=list(tgt[1]), kind=kind,
                                               extras=k, k_certificate=kf,
                                               eq_words=[list(w) for w in eqw])
                break
        if hit: break
    print(f"   VERDICT m={m}: {entry['verdict']}", flush=True)
    res[m] = entry
    json.dump(res, open(os.path.join(HERE,"results_task2_family.json"),"w"), indent=1)
print("DONE")
