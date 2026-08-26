#!/usr/bin/env python3
"""W20 -- RESIDUAL 1: a HARD exact search for a clean point with NO factoring
site (m = 26,27,28).  UNAUDITED.  Exact rational arithmetic only.

Strategy: random walk on the clean layer through exact site re-solves,
targeting the currently-factoring sites, never increasing the number of
factoring sites except to escape a plateau, with restarts.  At every visited
point we also record dim K_cap(t) at each FACTORING site -- dim K_cap(t) = 1
is a certificate that the site cannot be broken from the current
configuration (all three site vectors lie in the same line).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402
from w20_forcing import (kernel_basis, site_system, blocks_from_site,
                         site_vectors, factors_at, jpoint, rref)  # noqa: E402
from w20_sitesys import common_rows                              # noqa: E402


def rand_in_kernel(K, ncols, rng, rng_amp=9):
    for _ in range(60):
        coef = [Fraction(rng.randint(-rng_amp, rng_amp)) for _ in K]
        v = [sum(coef[i] * K[i][j] for i in range(len(K)))
             for j in range(ncols)]
        if all(x != 0 for x in v):
            return v
    return None


def try_site(blocks, gam, clean, site, rng, tries=200):
    """re-solve site exactly; return the best (rank, vectors) triple."""
    nbr, colid, ncols, rows = site_system(blocks, gam, site, clean)
    Ks = [kernel_basis(rows[c], ncols) for c in range(3)]
    if any(not K for K in Ks):
        return None
    best = None
    for _ in range(tries):
        vs = []
        ok = True
        for c in range(3):
            v = rand_in_kernel(Ks[c], ncols, rng)
            if v is None:
                ok = False
                break
            vs.append(v)
        if not ok:
            break
        rk = len(rref(vs, ncols)[0])
        if best is None or rk > best[0]:
            best = (rk, vs)
        if best[0] == 3:
            break
    return (nbr, ncols, [len(K) for K in Ks], best)


def hard_search(m, seed, steps=400):
    T = C.W8_IMMUNE[m]
    gam = C.gamma_edges(T)
    fullm = C.full_pm_indices(T)
    clean = [w for w in C.MIXED if not C.extras_at(T, w, fullm)]
    crows = {t: common_rows(T, fullm, t, clean) for t in range(8)}
    rng = random.Random(seed)
    _, blocks = jpoint(gam, rng)
    bestfac = list(range(8))
    kcap_at_factoring = {}
    for step in range(steps):
        fac = [s for s in range(8) if factors_at(blocks, gam, s)]
        if len(fac) < len(bestfac):
            bestfac = list(fac)
        if not fac:
            break
        # record dim K_cap at every factoring site
        for t in fac:
            _, _, ncols, rows2 = site_system(blocks, gam, t, crows[t])
            uniq = []
            seen = set()
            for r in rows2[0] + rows2[1] + rows2[2]:
                if tuple(r) not in seen:
                    seen.add(tuple(r))
                    uniq.append(r)
            d = len(kernel_basis(uniq, ncols))
            kcap_at_factoring[d] = kcap_at_factoring.get(d, 0) + 1
        site = fac[rng.randrange(len(fac))] if rng.random() < 0.75 \
            else rng.randrange(8)
        r = try_site(blocks, gam, clean, site, rng)
        if r is None or r[3] is None:
            continue
        nbr, ncols, dims, (rk, vs) = r
        save = {e: [row[:] for row in blocks[e]] for e in gam}
        blocks_from_site(blocks, gam, site, nbr, {c: vs[c] for c in range(3)})
        newfac = [s for s in range(8) if factors_at(blocks, gam, s)]
        # accept if it does not worsen; else accept with small probability
        if len(newfac) > len(fac) and rng.random() > 0.25:
            for e in gam:
                blocks[e] = save[e]
    fac = [s for s in range(8) if factors_at(blocks, gam, s)]
    ok = all(C.phi_value(blocks, fullm, w) == 0 for w in clean)
    nz = all(blocks[e][i][j] != 0 for e in gam for i in range(3)
             for j in range(3))
    return dict(m=m, seed=seed, best_factoring_seen=bestfac,
                n_best=len(bestfac), final=fac, clean_ok=ok, all_nonzero=nz,
                dimKcap_histogram_at_factoring_sites=kcap_at_factoring,
                point=({str(e): [[str(x) for x in r] for r in blocks[e]]
                        for e in gam} if not fac else None))


def main():
    res = {"_header": "UNAUDITED W20 hard search for a non-factoring clean "
                      "point. Exact only."}
    for m in (28, 27, 26):
        out = []
        for seed in (101, 202, 303, 404, 505, 606, 707, 808):
            r = hard_search(m, seed)
            out.append(r)
            print("m=%d seed %d: best %d factoring sites %s | final %s | "
                  "clean=%s nz=%s | dimKcap hist at factoring sites %s"
                  % (m, seed, r["n_best"], r["best_factoring_seen"],
                     r["final"], r["clean_ok"], r["all_nonzero"],
                     r["dimKcap_histogram_at_factoring_sites"]), flush=True)
            if not r["best_factoring_seen"]:
                print("*** ESCALATION: a clean point with NO factoring site "
                      "at m=%d ***" % m, flush=True)
        res["m%d" % m] = out
        res["m%d_min_factoring_sites" % m] = min(r["n_best"] for r in out)
    json.dump(res, open(os.path.join(HERE, "results_break2.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
