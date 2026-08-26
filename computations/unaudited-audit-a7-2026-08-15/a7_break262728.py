#!/usr/bin/env python3
"""A7 -- targeted search for a ZERO-factoring all-nonzero clean point at
m = 26, 27, 28 (W20's RESIDUAL 1).  Greedy: repeatedly re-solve a site that
currently factors, maximising the rank of its three site vectors; when a
factoring site has a 1-dimensional per-colour kernel (provably unbreakable
from there) perturb a NEIGHBOURING site first.  Exact arithmetic throughout;
every accepted state is re-verified against all clean equations."""
import os, sys, json, random
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import W8_IMMUNE, MIXED, F_gamma, k_of, gamma_edges
from a7_w20 import (jpoint, site_system, kernel, write_site, factors_at,
                    rref, phi_value, neighbours)

HERE = os.path.dirname(os.path.abspath(__file__))


def try_site(blocks, gam, t, clean, rng, tries=60):
    nbr, ncols, rows = site_system(blocks, gam, t, clean)
    Ks = [kernel(rows[c], ncols) for c in range(3)]
    if any(not K for K in Ks):
        return None, [len(K) for K in Ks]
    best = None
    for _ in range(tries):
        vs, ok = [], True
        for c in range(3):
            for _ in range(50):
                co = [Fr(rng.randint(-9, 9)) for _ in Ks[c]]
                v = [sum(co[i] * Ks[c][i][j] for i in range(len(Ks[c])))
                     for j in range(ncols)]
                if all(x != 0 for x in v):
                    break
            else:
                ok = False
                break
            vs.append(v)
        if not ok:
            break
        rk = len(rref(vs, ncols)[0])
        if best is None or rk > best[0]:
            best = (rk, vs, nbr)
        if rk == 3:
            break
    return best, [len(K) for K in Ks]


def search(m, seed, steps=700):
    T = W8_IMMUNE[m]
    gam = gamma_edges(T)
    Fg = F_gamma(T)
    clean = [w for w in MIXED if k_of(T, w, Fg) == 0]
    rng = random.Random(seed)
    blocks = jpoint(gam, rng)
    best = 9
    for step in range(steps):
        fac = [s for s in range(8) if factors_at(blocks, gam, s)]
        best = min(best, len(fac))
        if not fac:
            break
        t = rng.choice(fac)
        res, dims = try_site(blocks, gam, t, clean, rng)
        if res is None or res[0] == 1:
            # unbreakable here: perturb a neighbour instead
            s = rng.choice(neighbours(gam, t))
            r2, _ = try_site(blocks, gam, s, clean, rng)
            if r2 is not None:
                write_site(blocks, gam, s, r2[2], r2[1])
            continue
        write_site(blocks, gam, t, res[2], res[1])
    fac = [s for s in range(8) if factors_at(blocks, gam, s)]
    ok = all(phi_value(blocks, gam, w) == 0 for w in clean)
    nz = all(blocks[e][i][j] != 0 for e in gam for i in range(3)
             for j in range(3))
    return dict(m=m, seed=seed, final_factoring=fac, min_seen=best,
                clean_ok=ok, all_nonzero=nz,
                blocks={str(e): [[str(v) for v in r] for r in blocks[e]]
                        for e in gam} if not fac else None)


out = {}
for m in (27, 26, 28):
    rs = []
    for seed in (23, 101, 202, 303, 404, 505):
        r = search(m, seed)
        rs.append({k: v for k, v in r.items() if k != "blocks"})
        print("m=%d seed=%d -> final %s min_seen %d clean_ok=%s nz=%s"
              % (m, seed, r["final_factoring"], r["min_seen"], r["clean_ok"],
                 r["all_nonzero"]), flush=True)
        if not r["final_factoring"]:
            out["ZERO_FACTORING_POINT_m%d" % m] = r
            print("*** ZERO-FACTORING CLEAN POINT FOUND AT m=%d ***" % m,
                  flush=True)
    out["m%d" % m] = rs
json.dump(out, open(os.path.join(HERE, "results_break262728.json"), "w"),
          indent=1, default=str)
