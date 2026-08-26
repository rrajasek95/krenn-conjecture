#!/usr/bin/env python3
"""W20 -- RESIDUAL 1 diagnostics: the site-linearity systems at m=26,27,28.
UNAUDITED.  Exact rational arithmetic only.

For every site t we record
  * dim K_c   (c = 0,1,2), the per-colour kernels,
  * dim K_cap, the kernel of the COMMON rows (words clean for all three
    colours at t) -- v_0, v_1, v_2 all lie in K_cap, so
        dim K_cap = 1  =>  SITE t FACTORS.
  * whether K_0 = K_1 = K_2,
at exact rational points of the clean layer produced by the descent from
several independent J-points (an explicit-point control at the same time).
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
from w20_forcing import (kernel_basis, haf_at, site_system, blocks_from_site,
                         site_vectors, factors_at, jpoint, rref)  # noqa: E402


def common_rows(T, fullm, t, clean):
    """rows from words w such that (w with site t recoloured) is clean for
    ALL three colours at t."""
    cl = set(clean)
    out = []
    for w in clean:
        if all(tuple(c if i == t else w[i] for i in range(8)) in cl
               for c in range(3)):
            out.append(w)
    return out


def subspace_eq(A, B, n):
    RA, _ = rref(A, n) if A else ([], [])
    RB, _ = rref(B, n) if B else ([], [])
    return RA == RB


def analyse(blocks, gam, T, fullm, clean, tag):
    out = {}
    for t in range(8):
        nbr, colid, ncols, rows = site_system(blocks, gam, t, clean)
        Ks = {c: kernel_basis(rows[c], ncols) for c in range(3)}
        cr = common_rows(T, fullm, t, clean)
        _, _, _, rows2 = site_system(blocks, gam, t, cr)
        allrows = rows2[0] + rows2[1] + rows2[2]
        # the common system: rows independent of the colour at t, so use the
        # deduplicated row set
        seen = set()
        uniq = []
        for r in allrows:
            k = tuple(r)
            if k not in seen:
                seen.add(k)
                uniq.append(r)
        Kcap = kernel_basis(uniq, ncols)
        _, vs = site_vectors(blocks, gam, t)
        # rank of the 3 x ncols matrix of the site vectors
        rk = len(rref(vs, ncols)[0])
        out[t] = dict(deg=len(nbr), ncols=ncols,
                      dimK=[len(Ks[c]) for c in range(3)],
                      K0_eq_K1=subspace_eq(Ks[0], Ks[1], ncols),
                      K0_eq_K2=subspace_eq(Ks[0], Ks[2], ncols),
                      n_common_words=len(cr), dim_Kcap=len(Kcap),
                      site_vector_rank=rk, factors=(rk <= 1))
    out["_tag"] = tag
    return out


def descent_point(m, seed, passes=3):
    T = C.W8_IMMUNE[m]
    gam = C.gamma_edges(T)
    fullm = C.full_pm_indices(T)
    clean = [w for w in C.MIXED if not C.extras_at(T, w, fullm)]
    rng = random.Random(seed)
    _, blocks = jpoint(gam, rng)
    trace = []
    for it in range(passes):
        for site in range(8):
            nbr, colid, ncols, rows = site_system(blocks, gam, site, clean)
            newv = {}
            ok = True
            for c in range(3):
                K = kernel_basis(rows[c], ncols)
                if not K:
                    ok = False
                    break
                for _ in range(80):
                    coef = [Fraction(rng.randint(-7, 7)) for _ in K]
                    v = [sum(coef[i] * K[i][j] for i in range(len(K)))
                         for j in range(ncols)]
                    if all(x != 0 for x in v):
                        break
                else:
                    ok = False
                    break
                newv[c] = v
            if ok:
                blocks_from_site(blocks, gam, site, nbr, newv)
        trace.append([s for s in range(8) if factors_at(blocks, gam, s)])
    return T, gam, fullm, clean, blocks, trace


def main():
    res = {"_header": "UNAUDITED W20 site-system diagnostics (residual 1). "
                      "Exact rational arithmetic only."}
    for m in (26, 27, 28):
        T = C.W8_IMMUNE[m]
        gam = C.gamma_edges(T)
        fullm = C.full_pm_indices(T)
        clean = [w for w in C.MIXED if not C.extras_at(T, w, fullm)]
        entry = {}
        # (a) at a raw J-point
        rng = random.Random(1000 + m)
        _, jb = jpoint(gam, rng)
        entry["at_J_point"] = analyse(jb, gam, T, fullm, clean, "J-point")
        print("m=%d  J-point:" % m, flush=True)
        for t in range(8):
            d = entry["at_J_point"][t]
            print("   site %d deg=%d n=%d dimK=%s Kcap=%d (common words %d) "
                  "site-vector rank %d factors=%s"
                  % (t, d["deg"], d["ncols"], d["dimK"], d["dim_Kcap"],
                     d["n_common_words"], d["site_vector_rank"], d["factors"]),
                  flush=True)
        # (b) at several descent points
        pts = []
        for seed in (11, 23, 37):
            T2, gam2, fullm2, clean2, blocks, trace = descent_point(m, seed)
            ok = all(C.phi_value(blocks, fullm2, w) == 0 for w in clean2)
            nz = all(blocks[e][i][j] != 0 for e in gam2 for i in range(3)
                     for j in range(3))
            a = analyse(blocks, gam2, T2, fullm2, clean2, "descent s=%d" % seed)
            a["clean_equations_hold"] = ok
            a["all_cells_nonzero"] = nz
            a["factoring_trace"] = trace
            a["block_ranks"] = {str(e): C.rank_of(blocks[e]) for e in gam2}
            a["point"] = {str(e): [[str(x) for x in r] for r in blocks[e]]
                          for e in gam2}
            pts.append(a)
            print("m=%d  descent seed %d: clean_ok=%s all_nonzero=%s "
                  "factoring=%s block ranks=%s"
                  % (m, seed, ok, nz,
                     [t for t in range(8) if a[t]["factors"]],
                     sorted(set(a["block_ranks"].values()))), flush=True)
            for t in range(8):
                d = a[t]
                print("     site %d deg=%d n=%d dimK=%s Kcap=%d rank=%d "
                      "factors=%s" % (t, d["deg"], d["ncols"], d["dimK"],
                                      d["dim_Kcap"], d["site_vector_rank"],
                                      d["factors"]), flush=True)
        entry["descent_points"] = pts
        res["m%d" % m] = entry
    json.dump(res, open(os.path.join(HERE, "results_sitesys.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
