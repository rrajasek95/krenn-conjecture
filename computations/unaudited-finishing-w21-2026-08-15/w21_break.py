#!/usr/bin/env python3
"""W21 MOVE 1 -- reproduce and DIAGNOSE minimal-factoring clean points.
UNAUDITED.  Exact rational arithmetic only.  Independent of W20's search."""
import json, os, random, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w21_core as K, w21_site as SI

def rank_max_step(blocks, gam, clean, t, rng, tries=200):
    nb, ncols, rows, _ = SI.coeff_rows(blocks, gam, t, clean)
    Ks = [K.kernel_basis(rows[c], ncols) for c in range(3)]
    if any(not Kb for Kb in Ks): return False
    best = None
    for _ in range(tries):
        vs = []; ok = True
        for c in range(3):
            for _ in range(50):
                coef = [Fraction(rng.randint(-8, 8)) for _ in Ks[c]]
                v = [sum(coef[i]*Ks[c][i][j] for i in range(len(Ks[c]))) for j in range(ncols)]
                if all(x != 0 for x in v): break
            else:
                ok = False; break
            vs.append(v)
        if not ok: continue
        rk = K.rank_of(vs, ncols)
        if best is None or rk > best[0]: best = (rk, vs)
        if best[0] == 3: break
    if best is None: return False
    save = {e: [r[:] for r in blocks[e]] for e in gam}
    SI.write_site(blocks, gam, t, nb, {c: best[1][c] for c in range(3)})
    if not all(K.phi_value(blocks, gam, w) == 0 for w in clean):
        for e in gam: blocks[e] = save[e]
        return False
    return True

def search(m, seed, steps=48):
    T = K.W8_IMMUNE[m]; gam = K.gamma_edges(T); clean = K.clean_words(T)
    rng = random.Random(seed)
    blocks = SI.jpoint(gam, rng)
    best = (8, None)
    for step in range(steps):
        t = rng.randrange(8)
        rank_max_step(blocks, gam, clean, t, rng)
        fac = [s for s in range(8) if K.factors_at(blocks, gam, s)]
        if len(fac) < best[0]:
            best = (len(fac), {e: [r[:] for r in blocks[e]] for e in gam}, fac)
        if not fac: break
    return T, gam, clean, best

res = {"_header": "UNAUDITED W21 minimal-factoring clean points, exact only."}
for m in (26, 27, 28):
    out = []
    for seed in (2, 5, 13, 29, 41, 97, 5150, 777):
        T, gam, clean, best = search(m, seed)
        nfac, blocks, fac = best
        cok = all(K.phi_value(blocks, gam, w) == 0 for w in clean)
        nz = all(blocks[e][i][j] != 0 for e in gam for i in range(3) for j in range(3))
        rec = dict(seed=seed, n_factoring=nfac, factoring=fac, clean_ok=cok, all_nonzero=nz)
        print("m=%d seed %-5d min factoring %d %s clean=%s nz=%s" % (m, seed, nfac, fac, cok, nz), flush=True)
        if nfac <= 2 and cok and nz:
            rep = [SI.site_report(blocks, gam, t, clean) for t in range(8)]
            rec["sites"] = rep
            rec["point"] = {str(e): [[str(x) for x in r] for r in blocks[e]] for e in gam}
            for r in rep:
                print("    site %d deg=%d dimW=%2d Kcap=%2d factors=%-5s pats=%2d reg=%2d merge=%d "
                      "colclasses=%s blockranks=%s" % (r["site"], r["deg"], r["dimW"], r["dim_Kcap"],
                      r["factors"], r["n_patterns"], r["n_regular"], r["regular_merge_components"],
                      r["column_class_sizes"], sorted(r["block_ranks"].values())), flush=True)
            for r in rep:
                if not r["factors"]:
                    print("      site %d classes %s" % (r["site"], r["column_classes"]), flush=True)
        out.append(rec)
    res["m%d" % m] = out
json.dump(res, open("results_break.json", "w"), indent=1, default=str)
