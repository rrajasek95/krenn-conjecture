#!/usr/bin/env python3
"""W15 -- Phi-forcing decision at m = 25..28 (Rabinowitsch over Q).
Target: a mixed word with exactly ONE extra supported matching (m<28) or TWO
(m=28).  FORCED=True kills the template (a single occupied-cell monomial
would have to vanish); FORCED=False means the clean/effectively-clean layer
alone does not decide and the single-cell layer is needed."""
import json, os, sys, time
from itertools import product
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import W8_IMMUNE
from w15_forcing import full_matchings, extras
from w15_compressed import decide, eff_clean_words

HERE = os.path.dirname(os.path.abspath(__file__))
L4 = tuple(product(range(3), repeat=4))
res = {}
ms = [int(a) for a in sys.argv[1:]] or [25, 26, 27, 28]
for m in ms:
    T = W8_IMMUNE[m]; fm = full_matchings(T); EC = set(eff_clean_words(T))
    yfree = [y for y in L4 if all(tuple(x)+tuple(y) in EC for x in L4)]
    kk = 1 if m < 28 else 2
    ones = [(x, y) for x in L4 for y in L4
            if len(set(tuple(x)+tuple(y))) > 1 and len(extras(T,x,y,fm)) == kk]
    ones.sort(key=lambda t: -sum(1 for x in L4 if tuple(x)+tuple(t[1]) in EC))
    res[m] = []
    done = False
    for tgt in ones[:2]:
        XO = [x for x in L4 if x != tgt[0] and tuple(x)+tuple(tgt[1]) in EC]
        for nx, ny in ((2, 2), (3, 3), (4, 4)):
            if nx > len(XO) or ny > len(yfree): continue
            X0 = [tgt[0]] + XO[:nx]; Y0 = [tgt[1]] + [y for y in yfree if y != tgt[1]][:ny]
            eqw = [tuple(x)+tuple(y) for x in X0 for y in Y0
                   if (tuple(x), tuple(y)) != (tuple(tgt[0]), tuple(tgt[1]))
                   and tuple(x)+tuple(y) in EC and len(set(tuple(x)+tuple(y))) > 1]
            t0 = time.time()
            try:
                v, na, nc, ne, scr, raw = decide(T, eqw, tuple(tgt[0])+tuple(tgt[1]),
                                                 timeout=3000)
            except Exception:
                v, na, nc, ne = "TIMEOUT", -1, -1, len(eqw)
            print(f"m={m} target={tgt} extras={kk} nx={nx} ny={ny}: FORCED={v} "
                  f"atoms={na} cells={nc} eqs={ne} {time.time()-t0:.0f}s", flush=True)
            res[m].append(dict(target=[list(tgt[0]), list(tgt[1])], extras=kk,
                               nx=nx, ny=ny, forced=str(v), atoms=na, cells=nc, eqs=ne))
            json.dump(res, open(os.path.join(HERE, "results_m2528_forcing.json"), "w"),
                      indent=1)
            if v is True:
                done = True
                break
        if done: break
print("DONE")
