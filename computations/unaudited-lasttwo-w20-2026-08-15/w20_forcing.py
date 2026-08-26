#!/usr/bin/env python3
"""W20 -- RESIDUAL 1: forcing at m = 26, 27, 28.  UNAUDITED.  Exact only
(Fraction); floats appear nowhere.

THE SITE-LINEARITY REDUCTION (W20-L).  Every perfect matching of K_8 covers
site t by exactly ONE edge, so for any word w

    Phi_w  =  sum_{s in N_Gamma(t)}  A_ts[w_t][w_s] * C^t_s(w),
    C^t_s(w) = haf of Gamma - t - s at w   (independent of w_t !).

Hence, with the 3*deg(t) unknowns

    v_c = ( A_ts[c][d] )_{s in N(t), d in {0,1,2}}    (c = the colour at t),

the WHOLE clean layer is the union of THREE INDEPENDENT HOMOGENEOUS LINEAR
systems:  v_c in K_c^{(t)} := ker M_c^{(t)}, where M_c^{(t)} has one row per
effectively-clean word w with w_t = c, entry C^t_s(w) in column (s, w_s).
The coefficients depend only on the blocks AWAY from t.

  * "site t factors"  <=>  v_0, v_1, v_2 are pairwise proportional.
  * so: given the blocks away from t, forcing at t FAILS iff the kernels
    admit an all-nonzero non-proportional triple.

This gives (i) an exact one-site decision procedure, and (ii) an exact
"block coordinate descent" that never leaves the clean layer: re-solve site
by site, always landing exactly in the kernel, and watch which sites factor.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402


# ------------------------------------------------------------ linear algebra
def rref(rows, ncols):
    M = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c]:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def kernel_basis(rows, ncols):
    """exact basis of the kernel of the matrix with the given rows."""
    if not rows:
        return [[Fraction(int(i == k)) for i in range(ncols)]
                for k in range(ncols)]
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        basis.append(v)
    return basis


# ----------------------------------------------------------- the haf engine
def haf_at(blocks, edges, verts, w):
    """sum over perfect matchings of `edges` covering exactly `verts`."""
    verts = tuple(sorted(verts))
    if not verts:
        return Fraction(1)
    ES = set(edges)
    a = verts[0]
    tot = Fraction(0)
    for i in range(1, len(verts)):
        b = verts[i]
        e = (min(a, b), max(a, b))
        if e not in ES:
            continue
        rest = verts[1:i] + verts[i + 1:]
        tot += blocks[e][w[e[0]]][w[e[1]]] * haf_at(blocks, edges, rest, w)
    return tot


def site_system(blocks, gam, t, cleanwords):
    """the three matrices M_c^{(t)} (rows: clean words with w_t = c)."""
    nbr = sorted(s for e in gam for s in e if t in e and s != t)
    colid = {(s, d): 3 * k + d for k, s in enumerate(nbr) for d in range(3)}
    ncols = 3 * len(nbr)
    others = [e for e in gam if t not in e]
    rows = {0: [], 1: [], 2: []}
    for w in cleanwords:
        row = [Fraction(0)] * ncols
        for s in nbr:
            vs = [v for v in range(8) if v != t and v != s]
            row[colid[(s, w[s])]] += haf_at(blocks, others, vs, w)
        if any(row):
            rows[w[t]].append(row)
    return nbr, colid, ncols, rows


def blocks_from_site(blocks, gam, t, nbr, v):
    """write the vector v (indexed by (s,d)) back into the blocks at t."""
    for k, s in enumerate(nbr):
        e = (min(t, s), max(t, s))
        for c in range(3):
            for d in range(3):
                if e[0] == t:
                    blocks[e][c][d] = v[c][3 * k + d]
                else:
                    blocks[e][d][c] = v[c][3 * k + d]


def site_vectors(blocks, gam, t):
    nbr = sorted(s for e in gam for s in e if t in e and s != t)
    out = []
    for c in range(3):
        v = []
        for s in nbr:
            e = (min(t, s), max(t, s))
            for d in range(3):
                v.append(blocks[e][c][d] if e[0] == t else blocks[e][d][c])
        out.append(v)
    return nbr, out


def proportional(u, v):
    """u, v proportional as vectors (either may be zero)."""
    for i in range(len(u)):
        for j in range(i + 1, len(u)):
            if u[i] * v[j] - u[j] * v[i]:
                return False
    return True


def factors_at(blocks, gam, t):
    _, vs = site_vectors(blocks, gam, t)
    return all(proportional(vs[a], vs[b]) for a in range(3)
               for b in range(a + 1, 3))


# ------------------------------------------------------------- the J-point
def jpoint(gam, rng, tries=200):
    """rational t_e, all nonzero, with haf_Gamma(t) = 0 (a J-point)."""
    fullm = C.pms_inside(gam)
    for _ in range(tries):
        t = {e: Fraction(rng.randint(-9, 9) or 3, rng.randint(1, 4))
             for e in gam}
        e0 = gam[0]
        # solve haf = 0 linearly in t[e0]
        a = Fraction(0)
        b = Fraction(0)
        for mi in fullm:
            m = C.PMS[mi]
            p = Fraction(1)
            has = False
            for e in m:
                if e == e0:
                    has = True
                else:
                    p *= t[e]
            if has:
                a += p
            else:
                b += p
        if a == 0:
            continue
        t[e0] = -b / a
        if all(v != 0 for v in t.values()):
            blocks = {e: [[t[e]] * 3 for _ in range(3)] for e in gam}
            return t, blocks
    return None, None


# ------------------------------------------------------------- the search
def descent(m, seed=7, passes=8, verbose=True):
    T = C.W8_IMMUNE[m]
    gam = C.gamma_edges(T)
    fullm = C.full_pm_indices(T)
    clean = [w for w in C.MIXED if not C.extras_at(T, w, fullm)]
    rng = random.Random(seed)
    t, blocks = jpoint(gam, rng)
    if blocks is None:
        return dict(error="no J-point")
    log = []
    # sanity: the J-point satisfies every clean equation
    j_ok = all(C.phi_value(blocks, fullm, w) == 0 for w in clean)
    for it in range(passes):
        for site in range(8):
            nbr, colid, ncols, rows = site_system(blocks, gam, site, clean)
            Ks = {}
            newv = {}
            ok = True
            for c in range(3):
                K = kernel_basis(rows[c], ncols)
                Ks[c] = K
                if not K:
                    ok = False
                    break
                for _ in range(60):
                    coef = [Fraction(rng.randint(-6, 6)) for _ in K]
                    v = [sum(coef[i] * K[i][j] for i in range(len(K)))
                         for j in range(ncols)]
                    if all(x != 0 for x in v):
                        break
                else:
                    ok = False
                    break
                newv[c] = v
            if not ok:
                log.append(dict(iter=it, site=site, status="kernel too small",
                                dims=[len(Ks.get(c, [])) for c in range(3)]))
                continue
            save = {e: [row[:] for row in blocks[e]] for e in gam}
            blocks_from_site(blocks, gam, site, nbr, newv)
            if not all(C.phi_value(blocks, fullm, w) == 0 for w in clean):
                for e in gam:
                    blocks[e] = save[e]
                log.append(dict(iter=it, site=site, status="REJECT (bug?)"))
                continue
            log.append(dict(iter=it, site=site, status="ok",
                            kernel_dims=[len(Ks[c]) for c in range(3)],
                            factoring=[s for s in range(8)
                                       if factors_at(blocks, gam, s)]))
            if verbose:
                print("   m=%d it %d site %d: kernel dims %s -> factoring "
                      "sites %s" % (m, it, site, log[-1]["kernel_dims"],
                                    log[-1]["factoring"]), flush=True)
        fac = [s for s in range(8) if factors_at(blocks, gam, s)]
        if not fac:
            break
    fac = [s for s in range(8) if factors_at(blocks, gam, s)]
    allnz = all(blocks[e][i][j] != 0 for e in gam for i in range(3)
                for j in range(3))
    clean_ok = all(C.phi_value(blocks, fullm, w) == 0 for w in clean)
    return dict(m=m, jpoint_satisfies_clean=j_ok, n_clean=len(clean),
                final_factoring_sites=fac, all_gamma_cells_nonzero=allnz,
                all_clean_equations_hold=clean_ok,
                blocks={str(e): [[str(x) for x in r] for r in blocks[e]]
                        for e in gam},
                ranks={str(e): C.rank_of(blocks[e]) for e in gam},
                log=log[-24:])


def main():
    res = {"_header": "UNAUDITED W20 residual 1 (forcing at m=26,27,28). "
                      "Exact rational arithmetic only."}
    for m in (26, 27, 28):
        print("=== m = %d ===" % m, flush=True)
        r = descent(m)
        res["descent_m%d" % m] = r
        print("m=%d: J-point clean=%s | final factoring sites %s | all cells "
              "nonzero %s | clean eqs hold %s"
              % (m, r.get("jpoint_satisfies_clean"),
                 r.get("final_factoring_sites"),
                 r.get("all_gamma_cells_nonzero"),
                 r.get("all_clean_equations_hold")), flush=True)
    json.dump(res, open(os.path.join(HERE, "results_forcing.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
