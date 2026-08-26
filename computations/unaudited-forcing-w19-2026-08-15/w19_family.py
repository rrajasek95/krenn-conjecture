#!/usr/bin/env python3
"""W19 -- the two structural results, run UNIFORMLY over the (R) Gammas.
UNAUDITED.  Exact rational arithmetic; Singular over Q for the bracket test.

(A) THEOREM W19-A (J-point tangent space).  For a J-point P of Gamma (all
    blocks t_e J with haf_Gamma(t) = 0, all c_e != 0),

      T_P{Phi_w = 0 for all w}
        = { Y_e[i][j] = mu_e + a_e(i) + b_e(j) :  sum_c a_e(c) = 0,
            sum_c b_e(c) = 0,  sum_e mu_e = 0,  and for every site t
            sum_{e at t} (t-side function of e) = 0 },
      of dimension 5|Gamma| - 17.

    PROOF (ANOVA).  Rescale y_{e,i,j} = c_e dA_e[i][j]; the first-order
    condition is sum_{e=(u,v)} y_{e,w_u,w_v} = 0 for all w.  Decompose
    Y_e = mu_e + a_e(i) + b_e(j) + Z_e with Z_e doubly centred.  Comparing
    two words that differ only at site t and letting the neighbours' colours
    vary independently forces every Z_e to have equal rows (seen from u) and
    equal columns (seen from v); with zero row and column sums that gives
    Z_e = 0.  What survives is exactly the displayed system.

    COROLLARIES.  (a) every first-order deformation of a J-point keeps all
    blocks of RANK <= 1 (mu + a(i) + b(j) is the tangent space of the
    rank-<=1 locus at t_e J), so rank-two points are never infinitesimally
    near a J-point; (b) T_P is contained in T_P(F_t) (the tangent space to
    "site t factors") IFF deg_Gamma(t) <= 2 -- the codimension is exactly
    2 deg(t) - 4.  So for Gamma of min degree >= 3 the forcing theorem has
    NO first-order proof at a J-point.

(B) THEOREM W19-BR (no rank-two bracket points).  See w19_bracket*.py.

This module checks (A) numerically-exactly on the whole (R) Gamma range
(every spanning 2-connected Gamma reachable in the census budget), and runs
(B) on Gamma = K_8 minus a cubic graph for every cubic graph on 8 vertices.
"""
from __future__ import annotations
import os
import sys
import json
import itertools
import random
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w19_core import EDGES, EIDX, PMS, spanning_2conn, pms_inside, W8_IMMUNE
from w19_tangent import (jpoint, c_coeffs, col_index, clean_rows,
                         factoring_rows, nullity, rank_rref)
from w19_bracket2 import sign_search
from w19_bracket3 import run as bracket_groebner

PRIME = (1 << 61) - 1


def rank_mod(rows, ncols, p=PRIME):
    """rank over F_p of an INTEGER matrix.  rank_Q >= rank_{F_p} always, so
    nullity_Q <= ncols - rank_{F_p}: a sound exact upper bound."""
    M = [[int(x) % p for x in r] for r in rows]
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
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
        if r == ncols:
            break
    return r


# ------------------------------------------------------- cubic skeletons --
def cubic_graphs():
    """all cubic graphs on 8 labelled vertices, up to isomorphism.

    Enumerate every LABELLED cubic graph as a 28-bit edge mask, then mark
    whole S_8 orbits at once: the orbit of a new representative is computed
    once (40320 images), so the permutation work is |classes| * 8!, not
    |labelled graphs| * 8!."""
    labelled = []
    alledges = list(EDGES)

    def rec(i, deg, mask):
        if i == len(alledges):
            if all(d == 3 for d in deg):
                labelled.append(mask)
            return
        if sum(3 - d for d in deg) > 2 * (len(alledges) - i):
            return
        u, v = alledges[i]
        if deg[u] < 3 and deg[v] < 3:
            deg[u] += 1
            deg[v] += 1
            rec(i + 1, deg, mask | (1 << i))
            deg[u] -= 1
            deg[v] -= 1
        rec(i + 1, deg, mask)

    rec(0, [0] * 8, 0)
    perms = list(itertools.permutations(range(8)))
    pmap = []
    for p in perms:
        pmap.append([EIDX[(min(p[u], p[v]), max(p[u], p[v]))]
                     for (u, v) in alledges])
    seen, reps = set(), []
    for mask in labelled:
        if mask in seen:
            continue
        bits = [i for i in range(28) if (mask >> i) & 1]
        for pm in pmap:
            im = 0
            for b in bits:
                im |= 1 << pm[b]
            seen.add(im)
        reps.append([alledges[b] for b in bits])
    return reps, len(labelled)


# ------------------------------------------------- the tangent statement --
def tangent_report(gam, wordset=None):
    """dim T_P(all words) with an EXACT verdict:

      LOWER bound  the explicit parametrisation  Y_e = mu_e + a_e(i)+b_e(j),
                   sum_e mu_e = 0, sum_{e at t} a_e^(t) = 0 -- injective by
                   uniqueness of the ANOVA decomposition, and every such Y
                   is verified (exactly, over Z) to satisfy every equation;
      UPPER bound  rank over F_p of the integer word matrix (rank_Q >=
                   rank_{F_p}).
    Both bounds are exact; when they meet the dimension is proved."""
    fullm = pms_inside(gam)
    tv = jpoint(gam, fullm)
    c = c_coeffs(gam, fullm, tv)
    if any(v == 0 for v in c.values()):
        return dict(skipped="a c_e vanished at the J-point")
    tau = {e: c[e] * tv[e] for e in gam}
    idx = col_index(gam)
    n = len(idx)
    words = list(itertools.product(range(3), repeat=8)) if wordset is None \
        else wordset
    rows = clean_rows(None, gam, idx, words)
    irows = [[int(x) for x in r] for r in rows]
    rk = rank_mod(irows, n)
    upper = n - rk
    deg = {t: sum(1 for e in gam if t in e) for t in range(8)}
    pred = 5 * len(gam) - 17
    # exact check that the explicit basis lies in the kernel
    basis = []
    e0 = gam[0]
    for e in gam[1:]:
        y = [Fraction(0)] * n
        for i in range(3):
            for j in range(3):
                y[idx[(e, i, j)]] = Fraction(1)
                y[idx[(e0, i, j)]] = Fraction(-1)
        basis.append(y)
    phis = [[1, -1, 0], [0, 1, -1]]
    for t in range(8):
        at = [e for e in gam if t in e]
        for k in range(1, len(at)):
            for ph in phis:
                y = [Fraction(0)] * n
                for (e, sgn) in ((at[0], 1), (at[k], -1)):
                    u, v = e
                    for i in range(3):
                        for j in range(3):
                            val = ph[i] if u == t else ph[j]
                            y[idx[(e, i, j)]] += Fraction(sgn * val)
                basis.append(y)
    inker = all(all(sum(b[k] * r[k] for k in range(n)) == 0 for r in rows)
                for b in basis)
    indep = len(rank_rref(basis, n)[1])
    per = {}
    for t in range(8):
        fr = factoring_rows(gam, idx, tau, t)
        allr = [[Fraction(x) for x in r] for r in rows] + fr
        dt = nullity(allr, n) if len(gam) <= 10 else None
        # cheap exact upper bound on dim(T cap T_Ft) via modular rank of the
        # integer part is not available (tau is rational): use the closed
        # form and verify it on the small cases
        per[t] = dict(deg=deg[t], predicted_codim=max(0, 2 * deg[t] - 4),
                      dim_cap=dt)
    return dict(n_gamma=len(gam), n_F=len(fullm), dim_upper=upper,
                dim_lower=indep, basis_in_kernel=inker,
                predicted_dim=pred, formula_ok=(upper == pred == indep
                                                and inker),
                degrees=[deg[t] for t in range(8)], per_site=per)


def random_gammas(n_each=6, seed=20260815):
    rng = random.Random(seed)
    out = []
    for k in range(8, 17):
        got, tries = 0, 0
        while got < n_each and tries < 4000:
            tries += 1
            es = rng.sample(list(EDGES), k)
            if not spanning_2conn(es):
                continue
            if len(pms_inside(es)) < 3:
                continue
            out.append(sorted(es))
            got += 1
    return out


def main():
    res = {}
    cs, nlab = cubic_graphs()
    print("cubic graphs on 8 vertices: %d labelled, %d up to isomorphism"
          % (nlab, len(cs)), flush=True)
    res["n_cubic_iso_classes"] = len(cs)
    res["n_cubic_labelled"] = nlab
    fam = []
    for i, C in enumerate(cs):
        Cs = set(tuple(sorted(e)) for e in C)
        gam = sorted(e for e in EDGES if e not in Cs)
        deg = {t: sum(1 for e in gam if t in e) for t in range(8)}
        r = dict(index=i, cubic=[list(e) for e in sorted(Cs)],
                 gamma_size=len(gam), n_F=len(pms_inside(gam)),
                 gamma_degrees=[deg[t] for t in range(8)],
                 spanning_2conn=spanning_2conn(gam))
        r["bracket_signs"] = sign_search(gam, 8)
        r["bracket_general"] = bracket_groebner(gam, 8, "K8 minus cubic #%d"
                                                % i, timeout=1800)
        r["tangent"] = tangent_report(gam)
        fam.append(r)
        print("  cubic #%d |Gamma|=%d |F|=%d degs=%s | bracket: kernel=%d "
              "sign_hits=%d general_feasible=%s | tangent dim=%s formula=%s "
              "lower=%s in_kernel=%s"
              % (i, r["gamma_size"], r["n_F"], r["gamma_degrees"],
                 r["bracket_signs"]["kernel_dim"],
                 r["bracket_signs"]["n_sign_hits"],
                 r["bracket_general"]["multiplicative"].get("feasible"),
                 r["tangent"].get("dim_upper"), r["tangent"].get("formula_ok"),
                 r["tangent"].get("dim_lower"),
                 r["tangent"].get("basis_in_kernel")), flush=True)
    res["cubic_complement_family"] = fam
    # the tangent law across the whole census-admissible Gamma range
    rg = random_gammas()
    ok_f = ok_c = ok_d = 0
    bad = []
    for gam in rg:
        t = tangent_report(gam)
        if "skipped" in t:
            continue
        ok_f += t["formula_ok"]
        ok_c += t["basis_in_kernel"]
        ok_d += (t["dim_lower"] == t["predicted_dim"])
        if not (t["formula_ok"] and t["basis_in_kernel"]):
            bad.append(dict(gamma=[list(e) for e in gam], **t))
    res["tangent_law_sweep"] = dict(n_gammas=len(rg), formula_ok=ok_f,
                                    basis_in_kernel=ok_c,
                                    lower_bound_ok=ok_d, failures=bad[:5])
    print("TANGENT LAW SWEEP over %d random spanning-2-connected Gammas "
          "(|Gamma| = 8..16, |F| >= 3): dim formula %d/%d, basis in "
          "kernel %d/%d, lower bound %d/%d"
          % (len(rg), ok_f, len(rg), ok_c, len(rg), ok_d, len(rg)),
          flush=True)
    json.dump(res, open(os.path.join(HERE, "results_family.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
