#!/usr/bin/env python3
"""W19 -- THE CLEAN-LAYER TANGENT SPACE AT A J-POINT, and its position
relative to the factoring loci.  UNAUDITED.  Exact rational arithmetic.

THE J-POINT.  Put A_e = t_e * J (J = all-ones 3x3) on every Gamma edge,
with the scalars chosen so that haf_Gamma(t) := sum_{M in F(Gamma)}
prod_{e in M} t_e = 0.  Then Phi_w = haf_Gamma(t) = 0 for EVERY word, so P
satisfies the clean layer (this is W16's non-vacuity control, reproduced).
Every site factors at P (all blocks are rank one with the common vector
(1,1,1)), so P lies on ALL the factoring loci F_t.

THE JACOBIAN AT P HAS A PURELY COMBINATORIAL FORM.
  d Phi_w / d A_e[i][j]  =  [w_u = i][w_v = j] * c_e,
      c_e := sum_{M in F(Gamma), e in M} prod_{e' in M \\ e} t_{e'}
so after the (invertible, c_e != 0) rescaling y_{e,i,j} = c_e * dA_e[i][j],

      T_P(clean layer) = { y : sum_{e=(u,v) in Gamma} y_{e, w_u, w_v} = 0
                               for every effectively clean mixed word w }.

A pure 0/1 incidence system on 9|Gamma| unknowns.

THE FACTORING LOCUS F_t = {every Gamma block at t is rank one with a
common t-vector}.  Writing the block at t with the t-colour as ROW index,
its points are A_ts[i][j] = gamma_i * u^(s)_j; differentiating at P
(gamma = (1,1,1), u^(s) = t_e (1,1,1)) gives
      dA_e[i][j] = t_e * g_i + v^(e)_j ,  g COMMON to all e at t,
i.e. in y-coordinates (tau_e := c_e t_e)
      y_e[i][j] = tau_e * g_i + u^(e)_j .
So T_P(F_t) = { y : for each Gamma edge e at t, all 2x2 second differences
of y_e (t-index first) vanish, and the row-difference d_e(i,i')/tau_e is
independent of e }.

WHY THIS IS A TEST OF FORCING.  If V(clean) is contained in the union of
the F_t then the TANGENT CONE of V(clean) at P is contained in the union
of the tangent cones of the F_t.  A LINEAR space inside a finite union of
linear spaces lies in one of them.  So if T_P(clean) is not contained in
any T_P(F_t), then either P is a singular point of V(clean) (tangent cone
strictly smaller than the Zariski tangent space) or forcing FAILS.  Either
way the first-order picture is exactly what a proof must overcome, and the
escaping directions are the candidate counterexample directions.
"""
from __future__ import annotations
import os
import sys
import json
import itertools
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w19_core import (EDGES, PMS, W8_IMMUNE, gamma_edges, full_pm_indices,
                      extras_at, MIXED, pms_inside)


# --------------------------------------------------------- exact linalg ---

def rank_rref(rows, ncols):
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


def nullity(rows, ncols):
    if not rows:
        return ncols
    R, piv = rank_rref(rows, ncols)
    return ncols - len(piv)


# ------------------------------------------------------------- J-point ----

def jpoint(gam, fullm, seed=0):
    """t_e in Q^*, haf_Gamma(t) = 0, no coordinate zero."""
    base = [Fraction(1 + ((seed + 3 * k) % 5)) for k in range(len(gam))]
    tv = {e: base[i] for i, e in enumerate(gam)}

    def haf(tv):
        tot = Fraction(0)
        for mi in fullm:
            p = Fraction(1)
            for e in PMS[mi]:
                p *= tv[e]
            tot += p
        return tot
    for e0 in gam:                     # haf is affine-linear in t_{e0}
        save = tv[e0]
        tv[e0] = Fraction(0)
        c0 = haf(tv)
        tv[e0] = Fraction(1)
        c1 = haf(tv) - c0
        if c1 != 0 and -c0 / c1 != 0:
            tv[e0] = -c0 / c1
            assert haf(tv) == 0
            return tv
        tv[e0] = save
    raise RuntimeError("no J-point found")


def c_coeffs(gam, fullm, tv):
    c = {}
    for e in gam:
        tot = Fraction(0)
        for mi in fullm:
            M = PMS[mi]
            if e not in M:
                continue
            p = Fraction(1)
            for f in M:
                if f != e:
                    p *= tv[f]
            tot += p
        c[e] = tot
    return c


# --------------------------------------------------- the tangent spaces ---

def col_index(gam):
    idx = {}
    for e in gam:
        for i in range(3):
            for j in range(3):
                idx[(e, i, j)] = len(idx)
    return idx


def clean_rows(T, gam, idx, wordset):
    rows = []
    for w in wordset:
        r = [Fraction(0)] * len(idx)
        for (u, v) in gam:
            r[idx[((u, v), w[u], w[v])]] += 1
        rows.append(r)
    return rows


def factoring_rows(gam, idx, tau, t):
    """linear conditions cutting out T_P(F_t) inside the y-space."""
    at = [e for e in gam if t in e]
    rows = []

    def yv(e, ci, cj):
        """y_e with the t-colour FIRST."""
        u, v = e
        return (e, ci, cj) if u == t else (e, cj, ci)

    # (a) second differences vanish on every block at t
    for e in at:
        for i in range(1, 3):
            for j in range(1, 3):
                r = [Fraction(0)] * len(idx)
                r[idx[yv(e, 0, 0)]] += 1
                r[idx[yv(e, i, j)]] += 1
                r[idx[yv(e, 0, j)]] -= 1
                r[idx[yv(e, i, 0)]] -= 1
                rows.append(r)
    # (b) row differences proportional to tau_e, common g
    if len(at) >= 2:
        e0 = at[0]
        for e in at[1:]:
            for i in (1, 2):
                r = [Fraction(0)] * len(idx)
                r[idx[yv(e0, i, 0)]] += tau[e]
                r[idx[yv(e0, 0, 0)]] -= tau[e]
                r[idx[yv(e, i, 0)]] -= tau[e0]
                r[idx[yv(e, 0, 0)]] += tau[e0]
                rows.append(r)
    return rows


def analyse(T, name, use_clean_only=True):
    gam = gamma_edges(T)
    fullm = full_pm_indices(T)
    tv = jpoint(gam, fullm)
    c = c_coeffs(gam, fullm, tv)
    assert all(v != 0 for v in c.values()), "a c_e vanished"
    tau = {e: c[e] * tv[e] for e in gam}
    idx = col_index(gam)
    n = len(idx)
    clean = [w for w in MIXED if not extras_at(T, w, fullm)]
    allw = list(itertools.product(range(3), repeat=8))
    rows_clean = clean_rows(T, gam, idx, clean)
    rows_all = clean_rows(T, gam, idx, allw)
    d_clean = nullity(rows_clean, n)
    d_all = nullity(rows_all, n)
    out = dict(name=name, n_gamma=len(gam), n_vars=n, n_clean_words=len(clean),
               dim_T_clean=d_clean, dim_T_Phi_identically_zero=d_all)
    per_t = {}
    for t in range(8):
        fr = factoring_rows(gam, idx, tau, t)
        d_ft = nullity(rows_clean + fr, n)
        d_ft_all = nullity(rows_all + fr, n)
        per_t[t] = dict(dim_T_clean_cap_Ft=d_ft, contained=(d_ft == d_clean),
                        dim_T_all_cap_Ft=d_ft_all,
                        contained_all=(d_ft_all == d_all))
    out["per_site"] = per_t
    out["contained_in_some_Ft_clean"] = any(p["contained"] for p in
                                            per_t.values())
    out["contained_in_some_Ft_allwords"] = any(p["contained_all"] for p in
                                               per_t.values())
    # sanity: the gauge directions must lie in T_P(clean) AND in every T_P(F_t)
    #   y_{e,i,j} = tau_e (lam_{u,i} + lam_{v,j})
    gauge = []
    for t0 in range(8):
        for c0 in range(3):
            y = [Fraction(0)] * n
            for e in gam:
                u, v = e
                for i in range(3):
                    for j in range(3):
                        s = Fraction(0)
                        if u == t0 and i == c0:
                            s += 1
                        if v == t0 and j == c0:
                            s += 1
                        y[idx[(e, i, j)]] = tau[e] * s
            gauge.append(y)
    out["gauge_dirs_in_T_clean"] = all(
        all(sum(g[k] * r[k] for k in range(n)) == 0 for r in rows_all)
        for g in gauge)
    out["dim_gauge_span"] = len(rank_rref(gauge, n)[1])
    # the J-family directions y_{e,i,j} = rho_e with sum rho_e = 0
    jdirs = []
    for e in gam[1:]:
        y = [Fraction(0)] * n
        for i in range(3):
            for j in range(3):
                y[idx[(e, i, j)]] = Fraction(1)
                y[idx[(gam[0], i, j)]] = Fraction(-1)
        jdirs.append(y)
    out["Jfamily_dirs_in_T_clean"] = all(
        all(sum(g[k] * r[k] for k in range(n)) == 0 for r in rows_all)
        for g in jdirs)
    out["dim_gauge_plus_J"] = len(rank_rref(gauge + jdirs, n)[1])
    return out


def main():
    res = {}
    for m in (25, 26, 27, 28):
        r = analyse(W8_IMMUNE[m], "W8 m=%d" % m)
        res["m%d" % m] = r
        print("m=%d |G|=%d vars=%d clean=%d  dim T(clean)=%d  "
              "dim T(Phi==0)=%d  gauge+J=%d"
              % (m, r["n_gamma"], r["n_vars"], r["n_clean_words"],
                 r["dim_T_clean"], r["dim_T_Phi_identically_zero"],
                 r["dim_gauge_plus_J"]), flush=True)
        for t in range(8):
            p = r["per_site"][t]
            print("    site %d: dim(T_clean cap T_Ft)=%d contained=%s | "
                  "dim(T_all cap T_Ft)=%d contained=%s"
                  % (t, p["dim_T_clean_cap_Ft"], p["contained"],
                     p["dim_T_all_cap_Ft"], p["contained_all"]), flush=True)
        print("    contained in SOME F_t (clean layer): %s ; (Phi==0): %s"
              % (r["contained_in_some_Ft_clean"],
                 r["contained_in_some_Ft_allwords"]), flush=True)
        print("    controls: gauge dirs in T=%s, J dirs in T=%s"
              % (r["gauge_dirs_in_T_clean"], r["Jfamily_dirs_in_T_clean"]),
              flush=True)
    json.dump(res, open(os.path.join(HERE, "results_tangent.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
