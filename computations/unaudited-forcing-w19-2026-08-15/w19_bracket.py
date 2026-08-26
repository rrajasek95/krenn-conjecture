#!/usr/bin/env python3
"""W19 -- THE RANK-TWO (Plucker / bracket) OBSTRUCTION TEST.

WHY.  The forcing claim is "the clean layer forces some site to factor",
i.e. every solution of {Phi_w = 0 : w effectively clean} has a site whose
Gamma blocks are all rank one with a common t-vector.  Before trying to
prove it one must ask what the natural NON-factoring solutions look like.

THE CANDIDATE FAMILY.  Give every site t three vectors p_t(0), p_t(1),
p_t(2) in a TWO-dimensional space, and set

    A_uv[i][j] = s_uv * det( p_u(i), p_v(j) )        (u < v)

with scalars s_uv != 0.  Then every block has rank 2 (so NO site factors,
generically) and every cell is nonzero as soon as no p_u(i) is parallel to
a p_v(j).  Phi becomes

    Phi(w) = sum_{M in F(Gamma)} ( prod_{e in M} s_e ) * prod_{uv in M}
             det(p_u(w_u), p_v(w_v)).

Phi(w) is MULTILINEAR in (p_0(w_0), ..., p_7(w_7)) -- degree one in each
site -- so, because the three vectors at each site span the 2-space,
"Phi = 0 on all 3^8 words" is EQUIVALENT to the identity
sum_M z_M [M] = 0 in the bracket algebra, with z_M = prod_{e in M} s_e.
(That equivalence is checked here, not assumed: CTRL-MULTILIN.)

For Gamma = K_4 this identity is exactly the Grassmann-Plucker relation
[01][23] - [02][13] + [03][12] = 0, so at N = 4 the family is NON-EMPTY:
a rank-two, no-factoring-site, all-cells-nonzero solution of Phi == 0.
That is the POSITIVE CONTROL for this module (and the explicit-point
control for the infeasibility verdicts it reports).

THE QUESTION for N = 8: for which Gamma does a multiplicative z (all
s_e != 0) lie in the kernel?
"""
from __future__ import annotations
import os
import sys
import json
import itertools
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w19_core import (EDGES, EIDX, PMS, MIXED, WORDS, W8_IMMUNE, gamma_edges,
                      pms_inside, full_pm_indices, extras_at, spanning_2conn)
from w19_sing import run_singular, check_no_shadowing

# ------------------------------------------------------------ exact linalg


def rref(rows, ncols):
    """exact reduced row echelon; returns (rows, pivot columns)."""
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
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][f]
        basis.append(v)
    return basis


# ------------------------------------------------------------- the p data

def pdata(n, seed=1):
    """three generic 2-vectors per site, exact, deterministic."""
    s = seed
    out = []
    for t in range(n):
        vs = []
        for c in range(3):
            s = (1103515245 * s + 12345) % (1 << 31)
            a = Fraction((s % 17) - 8 or 3)
            s = (1103515245 * s + 12345) % (1 << 31)
            b = Fraction((s % 13) - 6 or 5)
            vs.append((a, b))
        out.append(vs)
    return out


def det2(p, q):
    return p[0] * q[1] - p[1] * q[0]


def matchings_of(edges, n):
    """all perfect matchings of the graph (edges) on vertex set range(n)."""
    E = set(tuple(sorted(e)) for e in edges)
    out = []

    def rec(rem, acc):
        if not rem:
            out.append(tuple(acc))
            return
        a = rem[0]
        for i in range(1, len(rem)):
            b = rem[i]
            if (a, b) in E:
                rec(rem[1:i] + rem[i + 1:], acc + [(a, b)])
    rec(tuple(range(n)), [])
    return out


def bracket_matrix(edges, n, P, words):
    Ms = matchings_of(edges, n)
    rows = []
    for w in words:
        row = []
        for M in Ms:
            v = Fraction(1)
            for (u, x) in M:
                v *= det2(P[u][w[u]], P[x][w[x]])
            row.append(v)
        rows.append(row)
    return Ms, rows


# --------------------------------------------- the multiplicative question

def spanning_tree(edges, n):
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    tree = []
    for (u, v) in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            par[ru] = rv
            tree.append((u, v))
    return tree


def multiplicative_in_kernel(edges, n, Ms, rows, timeout=1800, tag=""):
    """Is there s: E -> K^* with sum_M (prod_{e in M} s_e) X_M(w) = 0 for
    every sampled word w?   Gauge: s_e = 1 on a spanning tree (s_uv ->
    lam_u lam_v s_uv scales every matching monomial by prod lam, so it is a
    genuine gauge of the homogeneous system)."""
    tree = set(spanning_tree(edges, n))
    free = [e for e in edges if e not in tree]
    nm = {e: ("1" if e in tree else "s%d_%d" % e) for e in edges}
    ring = [nm[e] for e in free]
    if not ring:
        ring = ["dummyv"]
    eqs = []
    seen = set()
    R, _ = rref(rows, len(Ms))          # compress: only independent rows
    for row in R:
        terms = []
        for k, M in enumerate(Ms):
            if not row[k]:
                continue
            c = row[k]
            assert c.denominator != 0
            mon = "*".join(nm[e] for e in M if nm[e] != "1") or "1"
            num, den = c.numerator, c.denominator
            sg = "+" if num > 0 else "-"
            terms.append("%s%d/%d*%s" % (sg, abs(num), den, mon))
        e = "".join(terms).lstrip("+")
        if e and e not in seen:
            seen.add(e)
            eqs.append(e)
    prod = "*".join(nm[e] for e in free) if free else "1"
    gens = ["zzg%d" % i for i in range(1, len(eqs) + 1)]
    check_no_shadowing(ring, gens + ["zzI", "zzGB", "uu"])
    ll = ['LIB "elim.lib";', "ring r = 0,(%s,uu),dp;" % ",".join(ring)]
    for i, e in enumerate(eqs, 1):
        ll.append("poly zzg%d = %s;" % (i, e))
    ll.append("ideal zzI = %s,uu*(%s)-1;" % (",".join(gens), prod))
    ll.append("ideal zzGB = groebner(zzI);")
    ll.append('"UNIT:"; (zzGB[1]==1);')
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    if st == "TIMEOUT":
        return dict(tag=tag, verdict=None, secs=timeout, n_eqs=len(eqs),
                    n_free=len(free))
    unit = out.split("UNIT:")[1].strip().split()[0] == "1"
    return dict(tag=tag, n_eqs=len(eqs), n_free=len(free),
                free_edges=[list(e) for e in free],
                empty=unit, feasible=(not unit),
                secs=round(time.time() - t0, 1))


# ------------------------------------------------------------------ runner

def analyse(edges, n, name, words=None, timeout=1800, do_solve=True):
    P = pdata(n, seed=7)
    if words is None:
        words = list(itertools.product(range(3), repeat=n))
    Ms, rows = bracket_matrix(edges, n, P, words)
    ker = kernel_basis(rows, len(Ms))
    # CTRL-MULTILIN: restricting to two words per site must give the same
    # kernel (multilinearity + spanning), and adding a third must not shrink.
    w2 = [w for w in words if all(c < 2 for c in w)]
    _, rows2 = bracket_matrix(edges, n, P, w2)
    ker2 = kernel_basis(rows2, len(Ms))
    res = dict(name=name, n=n, n_edges=len(edges), n_matchings=len(Ms),
               kernel_dim=len(ker), kernel_dim_2words=len(ker2),
               multilin_control_ok=(len(ker) == len(ker2)))
    if do_solve and len(ker) > 0:
        res["multiplicative"] = multiplicative_in_kernel(
            edges, n, Ms, rows, timeout=timeout, tag=name)
    elif len(ker) == 0:
        res["multiplicative"] = dict(empty=True, feasible=False,
                                     reason="kernel is zero")
    return res


def main():
    out = {}
    # ---- POSITIVE CONTROL: K_4 must be feasible (Grassmann-Plucker) -------
    K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    out["CONTROL_K4"] = analyse(K4, 4, "K4 (positive control)")
    print("CONTROL K4:", out["CONTROL_K4"], flush=True)
    # ---- NEGATIVE CONTROL: a 4-cycle C_4 (2 matchings, no relation) ------
    C4 = [(0, 1), (1, 2), (2, 3), (0, 3)]
    out["CONTROL_C4"] = analyse(C4, 4, "C4 (negative control)")
    print("CONTROL C4:", out["CONTROL_C4"], flush=True)
    # ---- K_6 -------------------------------------------------------------
    K6 = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    out["K6"] = analyse(K6, 6, "K6")
    print("K6:", out["K6"], flush=True)
    # ---- the W8 (R) ladder Gammas ---------------------------------------
    for m in (25, 26, 27, 28):
        ge = gamma_edges(W8_IMMUNE[m])
        out["W8_m%d" % m] = analyse(ge, 8, "W8 Gamma m=%d" % m, timeout=2400)
        print("W8 m=%d:" % m, out["W8_m%d" % m], flush=True)
    # ---- K_8 -------------------------------------------------------------
    K8 = list(EDGES)
    out["K8"] = analyse(K8, 8, "K8", timeout=2400)
    print("K8:", out["K8"], flush=True)
    json.dump(out, open(os.path.join(HERE, "results_bracket.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
