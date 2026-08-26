#!/usr/bin/env python3
"""W21 MOVE 1 -- the ZERO-FACTORING HUNT.  UNAUDITED.  Exact only.
A much larger exact search than W20's for a clean point (all Gamma cells
nonzero) with NO factoring site.  Any hit would be a genuine obstruction to
the residual-1 statement and is verified immediately."""
import json, os, random, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w21_core as K, w21_site as SI


def rank_max_step(blocks, gam, clean, t, rng, tries=60):
    nb, ncols, rows, _ = SI.coeff_rows(blocks, gam, t, clean)
    Ks = [K.kernel_basis(rows[c], ncols) for c in range(3)]
    if any(not Kb for Kb in Ks):
        return False
    best = None
    for _ in range(tries):
        vs = []
        ok = True
        for c in range(3):
            for _ in range(50):
                coef = [Fraction(rng.randint(-8, 8)) for _ in Ks[c]]
                v = [sum(coef[i]*Ks[c][i][j] for i in range(len(Ks[c])))
                     for j in range(ncols)]
                if all(z != 0 for z in v):
                    break
            else:
                ok = False
                break
            vs.append(v)
        if not ok:
            continue
        rk = K.rank_of(vs, ncols)
        if best is None or rk > best[0]:
            best = (rk, vs)
        if best[0] == 3:
            break
    if best is None:
        return False
    save = {e: [r[:] for r in blocks[e]] for e in gam}
    SI.write_site(blocks, gam, t, nb, {c: best[1][c] for c in range(3)})
    if not all(K.phi_value(blocks, gam, w) == 0 for w in clean):
        for e in gam:
            blocks[e] = save[e]
        return False
    return True

DEADLINE = time.time() + 4200
res = {"_header": "UNAUDITED W21 zero-factoring hunt. Exact only."}
for m in (28, 27, 26):
    best = 8; hist = {}; nseeds = 0; pts = []
    seed = 0
    T = K.W8_IMMUNE[m]; gam = K.gamma_edges(T); clean = K.clean_words(T)
    while time.time() < DEADLINE - (0 if m == 28 else 1400):
        seed += 1; nseeds += 1
        rng = random.Random(1000000 + 7919*seed + m)
        blocks = SI.jpoint(gam, rng)
        if blocks is None: continue
        for step in range(70):
            t = rng.randrange(8)
            rank_max_step(blocks, gam, clean, t, rng, tries=60)
            fac = [s for s in range(8) if K.factors_at(blocks, gam, s)]
            hist[len(fac)] = hist.get(len(fac), 0) + 1
            if len(fac) < best:
                best = len(fac)
                cok = all(K.phi_value(blocks, gam, w) == 0 for w in clean)
                nz = all(blocks[e][i][j] != 0 for e in gam for i in range(3) for j in range(3))
                pts.append(dict(seed=seed, step=step, n=len(fac), fac=fac, clean=cok, nonzero=nz,
                                point={str(e): [[str(x) for x in r] for r in blocks[e]] for e in gam}))
                print("m=%d NEW MIN %d factoring sites %s (seed %d step %d) clean=%s nz=%s"
                      % (m, len(fac), fac, seed, step, cok, nz), flush=True)
            if not fac: break
        if best == 0: break
    res["m%d" % m] = dict(seeds=nseeds, min_factoring=best,
                          visited_state_hist={str(k): v for k, v in sorted(hist.items())},
                          record_points=pts[-3:])
    print("m=%d: %d seeds, %d states visited, minimum factoring-site count %d, histogram %s"
          % (m, nseeds, sum(hist.values()), best, sorted(hist.items())), flush=True)
json.dump(res, open("results_hunt.json", "w"), indent=1, default=str)
