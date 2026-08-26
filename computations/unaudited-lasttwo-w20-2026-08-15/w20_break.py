#!/usr/bin/env python3
"""W20 -- RESIDUAL 1: can EVERY site be broken simultaneously?  UNAUDITED.
Exact rational arithmetic only (Fraction); floats nowhere.

Aggressive exact search on the clean layer of m = 26,27,28:
  * start at a random J-point (all Gamma cells nonzero, Phi_w = 0 for every
    effectively-clean w);
  * repeatedly pick a site, compute the three exact kernels K_c of the
    site-linear system, and replace the site data by kernel vectors chosen
    to MAXIMISE the rank of (v_0, v_1, v_2)  -- i.e. to break factoring at
    that site as hard as possible;
  * every step keeps the point exactly on the clean layer (verified), so any
    point produced is an explicit exact witness.

If a point with NO factoring site were found, the forcing statement would be
FALSE at that m.  Random site orders, greedy rank maximisation, restarts.
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


def best_triple(K, ncols, rng, tries=120):
    """pick v_0,v_1,v_2 in the kernel K, all coordinates nonzero, maximising
    the rank of the 3 x ncols matrix."""
    best = None
    for _ in range(tries):
        vs = []
        ok = True
        for _c in range(3):
            for _ in range(40):
                coef = [Fraction(rng.randint(-8, 8)) for _ in K]
                v = [sum(coef[i] * K[i][j] for i in range(len(K)))
                     for j in range(ncols)]
                if all(x != 0 for x in v):
                    break
            else:
                ok = False
                break
            vs.append(v)
        if not ok:
            continue
        rk = len(rref(vs, ncols)[0])
        if best is None or rk > best[0]:
            best = (rk, vs)
        if best[0] == min(3, len(K)):
            break
    return best


def search(m, seed, n_steps=60):
    T = C.W8_IMMUNE[m]
    gam = C.gamma_edges(T)
    fullm = C.full_pm_indices(T)
    clean = [w for w in C.MIXED if not C.extras_at(T, w, fullm)]
    rng = random.Random(seed)
    _, blocks = jpoint(gam, rng)
    if blocks is None:
        return dict(error="no J-point")
    hist = []
    best = 8
    for step in range(n_steps):
        site = rng.randrange(8)
        nbr, colid, ncols, rows = site_system(blocks, gam, site, clean)
        Ks = [kernel_basis(rows[c], ncols) for c in range(3)]
        if any(not K for K in Ks):
            continue
        # kernels can differ per colour; take v_c from its own K_c
        vs = []
        ok = True
        for c in range(3):
            r = best_triple(Ks[c], ncols, rng, tries=1)
            if r is None:
                ok = False
                break
            vs.append(r[1][0])
        if not ok:
            continue
        # try to maximise the rank of (v_0,v_1,v_2)
        bestrk, bestvs = len(rref(vs, ncols)[0]), vs
        for _ in range(150):
            trial = []
            good = True
            for c in range(3):
                for _ in range(40):
                    coef = [Fraction(rng.randint(-8, 8)) for _ in Ks[c]]
                    v = [sum(coef[i] * Ks[c][i][j] for i in range(len(Ks[c])))
                         for j in range(ncols)]
                    if all(x != 0 for x in v):
                        break
                else:
                    good = False
                    break
                trial.append(v)
            if not good:
                continue
            rk = len(rref(trial, ncols)[0])
            if rk > bestrk:
                bestrk, bestvs = rk, trial
            if bestrk == 3:
                break
        blocks_from_site(blocks, gam, site, nbr, {c: bestvs[c]
                                                 for c in range(3)})
        fac = [s for s in range(8) if factors_at(blocks, gam, s)]
        hist.append(dict(step=step, site=site,
                         dimK=[len(K) for K in Ks], rank=bestrk, fac=fac))
        best = min(best, len(fac))
        if not fac:
            break
    fac = [s for s in range(8) if factors_at(blocks, gam, s)]
    ok = all(C.phi_value(blocks, fullm, w) == 0 for w in clean)
    nz = all(blocks[e][i][j] != 0 for e in gam for i in range(3)
             for j in range(3))
    return dict(m=m, seed=seed, final_factoring=fac,
                min_factoring_count_seen=best,
                clean_equations_hold=ok, all_cells_nonzero=nz,
                hist=hist[-10:],
                point=({str(e): [[str(x) for x in r] for r in blocks[e]]
                        for e in gam} if not fac else None))


def main():
    res = {"_header": "UNAUDITED W20: attempt to break factoring at EVERY "
                      "site on the clean layer (residual 1). Exact only."}
    for m in (26, 27, 28):
        out = []
        for seed in (2, 5, 13, 29, 41, 97):
            r = search(m, seed)
            out.append(r)
            print("m=%d seed %d -> final factoring sites %s (min seen %d) "
                  "clean=%s nonzero=%s"
                  % (m, seed, r["final_factoring"],
                     r["min_factoring_count_seen"], r["clean_equations_hold"],
                     r["all_cells_nonzero"]), flush=True)
        res["m%d" % m] = out
        never = all(r["final_factoring"] for r in out)
        res["m%d_always_some_factoring_site" % m] = never
    json.dump(res, open(os.path.join(HERE, "results_break.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
