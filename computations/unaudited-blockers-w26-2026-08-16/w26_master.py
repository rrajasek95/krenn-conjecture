#!/usr/bin/env python3
"""W26 -- THEOREM W26-M: the R-vertex slice dichotomy.  UNAUDITED.  Exact.

NOTATION.  L={0,1,2,3}, R={4,5,6,7}, sigma = (0<->7,1<->4,2<->5,3<->6).
For a word w=(x,y):  l_ab = A_ab[x_a][x_b];  h = hafL = l01 l23 + l02 l13
+ l03 l12;  D_p = A_{p,sigma p}[x_p][y_{sigma p}]  (0 if absent);
r_jk = A_jk[y_j][y_k]  (0 if absent).

Phi is LINEAR in the y_k-slice of each Gamma block touching k, so
    Phi = Psi[D_p] * (A_{p,k}[x_p][.])  +  sum_{q != p} Psi_q * (A_{k,sigma q}
          slice),          p = sigma^{-1} k,
with, for {i,j} = L \\ {p,q},
    Psi_q      = l_pq D_i D_j + h * r_{sigma i, sigma j}
    Psi[D_p]   = prod_{q != p} D_q + sum_{q != p} D_q l_ij r_{sigma i sigma j}

MASTER RELATION (proved here symbolically, every m and k):
    h * Psi[D_p]  =  sum_{q != p}  D_q * l_ij * Psi_q .

Hence, multiplying the slice equation by h and substituting,
    sum_{q != p}  Psi_q * W_q  =  0,
    W_q := D_q * l_ij * (A_{p,k}[x_p][.])  +  h * (A_{k,sigma q} slice).
THREE vectors -- for every m and every k.  Therefore, along any clean-word
family in which y_k runs over all three letters:

    DICHOTOMY:   det[W_q1, W_q2, W_q3] = 0    OR    Psi_q = 0 for all q.

COROLLARY (unconditional determinant lemma).  If for some q the R-edge
(sigma i, sigma j), {i,j} = L\\{p,q}, is ABSENT from the R-graph, then
Psi_q = l_pq D_i D_j, a product of nonzero cells, so the second branch is
impossible and  det[W_q1,W_q2,W_q3] = 0  holds at EVERY clean point.
Missing R-edges: (4,6) at m=25,26 -> k in {5,7};  (5,7) at m=25,26,27 ->
k in {4,6}.  So m=25,26 are covered at all four R-vertices and m=27 at
k=4 and k=6.  m=28 has no missing R-edge (handled elsewhere).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_psi as PS                                              # noqa: E402
import sympy as sp                                                # noqa: E402

OUT = {"_header": "UNAUDITED W26 Theorem W26-M."}


def qdata(p, q):
    """({i,j} = L-{p,q}, l_ij, l_pq, the R-edge (sigma i, sigma j))."""
    i, j = [t for t in range(4) if t not in (p, q)]
    lij = PS.LL[(min(i, j), max(i, j))]
    lpq = PS.LL[(min(p, q), max(p, q))]
    e = (min(C.SIG[i], C.SIG[j]), max(C.SIG[i], C.SIG[j]))
    return (i, j), lij, lpq, e


def master_check():
    print("=" * 76)
    ok_all = True
    rec = {}
    for m in (25, 26, 27, 28):
        gs = set(C.gamma_edges(C.TEMPLATES[m]))
        PH = PS.phi_sym(m)
        # every absent block reads as 0 EVERYWHERE (including in the
        # coefficients of the relation) -- this substitution is the model.
        zsub = {PS.D[t]: 0 for t in range(4) if (t, C.SIG[t]) not in gs}
        zsub.update({PS.RS[e]: 0 for e in PS.RS if e not in gs})

        def Z(expr):
            return sp.expand(sp.expand(expr).subs(zsub))
        for k in C.R:
            p = C.SIGINV[k]
            PsiD = Z(sp.diff(PH, PS.D[p])) if (p, k) in gs else sp.Integer(0)
            rhs = sp.Integer(0)
            for q in range(4):
                if q == p:
                    continue
                (i, j), lij, lpq, e = qdata(p, q)
                ek = (min(k, C.SIG[q]), max(k, C.SIG[q]))
                Psq = Z(sp.diff(PH, PS.RS[ek])) if ek in gs \
                    else Z(lpq * PS.D[i] * PS.D[j]
                           + PS.H * (PS.RS[e] if e in gs else 0))
                rhs += Z(PS.D[q]) * lij * Psq
            ok = sp.simplify(sp.expand(PS.H * PsiD - rhs)) == 0
            ok_all &= ok
            rec["m%d_k%d" % (m, k)] = bool(ok)
            print("  m=%d k=%d  h*Psi[D%d] == sum_q D_q l_ij Psi_q : %s"
                  % (m, k, p, ok))
    OUT["master_relation_ok"] = rec
    OUT["master_relation_all_ok"] = bool(ok_all)
    # MUTATION control: wrong coefficient l_pq instead of l_ij must fail
    bad = 0
    for m in (26, 28):
        gs = set(C.gamma_edges(C.TEMPLATES[m]))
        PH = PS.phi_sym(m)
        for k in C.R:
            p = C.SIGINV[k]
            PsiD = sp.expand(sp.diff(PH, PS.D[p]))
            rhs = sp.Integer(0)
            for q in range(4):
                if q == p:
                    continue
                (i, j), lij, lpq, e = qdata(p, q)
                ek = (min(k, C.SIG[q]), max(k, C.SIG[q]))
                Psq = sp.expand(sp.diff(PH, PS.RS[ek])) if ek in gs \
                    else sp.expand(lpq * PS.D[i] * PS.D[j]
                                   + PS.H * (PS.RS[e] if e in gs else 0))
                rhs += PS.D[q] * lpq * Psq              # WRONG: l_pq
            bad += (sp.simplify(sp.expand(PS.H * PsiD - rhs)) != 0)
    print("  MUTATION (l_pq in place of l_ij): fails %d/8 (want 8)" % bad)
    OUT["master_mutation_fails"] = bad
    return ok_all


def Wvecs(bl, m, k, x, yfix):
    """the three W_q vectors (rows indexed by the letter of y_k), and the
    three Psi_q, at the given (x, other y-coordinates).
    yfix: dict {R-vertex: letter} for the three coordinates != k."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    p = C.SIGINV[k]
    ll = {(a, b): bl[(a, b)][x[a]][x[b]] for a, b in combinations(range(4), 2)}
    h = (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
         + ll[(0, 3)] * ll[(1, 2)])

    def Dv(t, ykval=None):
        e = (t, C.SIG[t])
        if e not in gs:
            return Fraction(0)
        yl = ykval if C.SIG[t] == k else yfix[C.SIG[t]]
        return bl[e][x[t]][yl]

    def rv(a, b, ykval=None):
        e = (min(a, b), max(a, b))
        if e not in gs:
            return Fraction(0)
        la = ykval if e[0] == k else yfix[e[0]]
        lb = ykval if e[1] == k else yfix[e[1]]
        return bl[e][la][lb]
    Ws, Psis, labs = [], [], []
    for q in range(4):
        if q == p:
            continue
        (i, j), _lij, _lpq, e = qdata(p, q)
        lij = ll[(min(i, j), max(i, j))]
        lpq = ll[(min(p, q), max(p, q))]
        Dq = Dv(q)
        Psi = lpq * Dv(i) * Dv(j) + h * rv(*e)
        W = []
        for t in range(3):
            gsl = bl[(p, k)][x[p]][t] if (p, k) in gs else Fraction(0)
            rsl = rv(k, C.SIG[q], t)
            W.append(Dq * lij * gsl + h * rsl)
        Ws.append(W)
        Psis.append(Psi)
        labs.append(q)
    return Ws, Psis, labs, h


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[1][0] * (M[0][1] * M[2][2] - M[0][2] * M[2][1])
            + M[2][0] * (M[0][1] * M[1][2] - M[0][2] * M[1][1]))


def full_yk_families(m, k):
    """(x, yfix) such that (x,y) is clean for all three letters of y_k."""
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    others = [t for t in C.R if t != k]
    out = []
    for x in product(range(3), repeat=4):
        forb = {t: set() for t in C.R}
        for e, (a, b) in sing.items():
            if e in lv and x[e[0]] == a:
                forb[e[1]].add(b)
        if forb[k]:
            continue
        cand = [sorted(set(range(3)) - forb[t]) for t in others]
        for combo in product(*cand):
            yfix = dict(zip(others, combo))
            w0 = tuple(x) + tuple(
                (0 if t == k else yfix[t]) for t in range(4, 8))
            if len(set(w0)) == 1:
                continue
            out.append((x, yfix))
    return out


def test_master_numeric(m, bl):
    """(1) sum Psi_q W_q == 0 at every full-y_k clean family;
       (2) det[W]==0 wherever the corollary applies."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    bad_sum = bad_det = n_sum = n_det = 0
    for k in C.R:
        p = C.SIGINV[k]
        # does the corollary apply at this k?
        corol = any((min(C.SIG[i], C.SIG[j]), max(C.SIG[i], C.SIG[j]))
                    not in gs
                    for q in range(4) if q != p
                    for (i, j) in [tuple(t for t in range(4)
                                         if t not in (p, q))])
        for x, yfix in full_yk_families(m, k):
            Ws, Psis, labs, h = Wvecs(bl, m, k, x, yfix)
            for t in range(3):
                s = sum(Psis[a] * Ws[a][t] for a in range(3))
                n_sum += 1
                bad_sum += (s != 0)
            if corol:
                n_det += 1
                bad_det += (det3([[Ws[a][t] for a in range(3)]
                                  for t in range(3)]) != 0)
    return dict(n_sum=n_sum, bad_sum=bad_sum, n_det=n_det, bad_det=bad_det,
                corollary_ks=[k for k in C.R
                              if any((min(C.SIG[i], C.SIG[j]),
                                      max(C.SIG[i], C.SIG[j])) not in gs
                                     for q in range(4)
                                     if q != C.SIGINV[k]
                                     for (i, j) in [tuple(
                                         t for t in range(4)
                                         if t not in (C.SIGINV[k], q))])])


def main():
    master_check()
    import w26_pts as PT
    import w26_fast as F
    print("=" * 76)
    print("NUMERIC: sum Psi_q W_q = 0 and det[W] = 0 at CLEAN points")
    recs = []
    for m, tag, bl in PT.stored_points():
        r = test_master_numeric(m, bl)
        r.update(m=m, tag=tag, van=PT.vanishing_stratum(m, bl))
        recs.append(r)
        print("  m=%d %-22s sumPsiW bad %d/%d | det[W] bad %d/%d (k=%s) "
              "van=%s" % (m, tag[:22], r["bad_sum"], r["n_sum"],
                          r["bad_det"], r["n_det"], r["corollary_ks"],
                          r["van"]), flush=True)
    OUT["stored"] = recs
    # ---- fresh points per m (own descent, fast engine)
    for m in (25, 26, 27, 28):
        mdl = F.Model(m)
        got = 0
        for kk in range(400):
            rng = random.Random(55_000_000 + 1000 * m + kk)
            order = list(range(8))
            rng.shuffle(order)
            bl = F.make_point(mdl, rng, passes=4, order=order)
            if bl is None:
                continue
            r = test_master_numeric(m, bl)
            r.update(m=m, tag="fresh%d" % kk, van=mdl.vanishing(bl))
            recs.append(r)
            print("  m=%d fresh%-4d          sumPsiW bad %d/%d | det[W] bad "
                  "%d/%d (k=%s) van=%s"
                  % (m, kk, r["bad_sum"], r["n_sum"], r["bad_det"],
                     r["n_det"], r["corollary_ks"], r["van"]), flush=True)
            got += 1
            if got >= 6:
                break
    OUT["all"] = recs
    # ---- OUT-OF-LOCUS CONTROL: random non-clean points must violate
    nbad = 0
    for m in (25, 26, 27):
        gam = C.gamma_edges(C.TEMPLATES[m])
        rng = random.Random(99 + m)
        for _ in range(3):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            r = test_master_numeric(m, bl)
            nbad += (r["bad_det"] > 0)
    print("OUT-OF-LOCUS CONTROL (random non-clean): det[W] violated at "
          "%d/9 points (want 9)" % nbad)
    OUT["out_of_locus_det_violations"] = nbad
    tot_bs = sum(r["bad_sum"] for r in recs)
    tot_bd = sum(r["bad_det"] for r in recs)
    print("TOTALS: sum Psi_q W_q violations %d ; det[W] violations %d"
          % (tot_bs, tot_bd))
    OUT["total_bad_sum"] = tot_bs
    OUT["total_bad_det"] = tot_bd
    json.dump(OUT, open(os.path.join(HERE, "results_master.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
