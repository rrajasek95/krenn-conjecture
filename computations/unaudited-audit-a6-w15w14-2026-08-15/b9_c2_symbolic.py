#!/usr/bin/env python3
"""A6-B9 / C2 upgrade: prove  phi_A in perp(J_4(A))  SYMBOLICALLY in A.

W14 says "phi_A verified not proved".  Half of the claim can in fact be proved
outright by a finite exact computation: treat the nine entries A_ij as
indeterminates and check

    <phi_A, K_n * iota_3(mu,nu)>      = 0   in Z[A]   (9 x 100 identities)
    <phi_A, K_n * s_A * iota_2(mu,nu)> = 0  in Z[A]   (9 x  36 identities)

as identities of polynomials in the nine A-variables.  Together with
phi_A != 0 for A != 0 this proves codim J_4(A) >= 1 for EVERY nonzero
rational (indeed complex) A; only "codim <= 1" remains a genericity statement.

Also proves the three component identities behind the char-poly description
    e_1(K adj A) = shat_A,  e_2(K adj A) = det(A) q_A,
    e_3(K adj A) = det(A)^2 det K,
hence  e_2^2 - 4 e_1 e_3 = det(A)^2 (q_A^2 - 4 shat_A det K) = det(A)^2 phi_A.

Representation: a K-form with symbolic A-coefficients is
    {K-exponent (9-tuple): {A-exponent (9-tuple): int}}.
All integer arithmetic.
"""

from __future__ import annotations

import json
import sys
import time
from math import factorial

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-audit-a6-w15w14-2026-08-15")
import b9_core as B                                            # noqa: E402

HERE = "/Users/rishi/workplace/krenn-conjecture/computations/" \
       "unaudited-audit-a6-w15w14-2026-08-15"

Z9 = (0,) * 9


def aadd(f, g):
    out = dict(f)
    for m, c in g.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def amul(f, g):
    out = {}
    for a, ca in f.items():
        for b, cb in g.items():
            k = tuple(x + y for x, y in zip(a, b))
            out[k] = out.get(k, 0) + ca * cb
    return {m: c for m, c in out.items() if c}


def ascale(f, c):
    return {} if c == 0 else {m: v * c for m, v in f.items()}


# symbolic K-forms: {K-expo: A-poly}
def sadd(F, G):
    out = dict(F)
    for m, c in G.items():
        out[m] = aadd(out.get(m, {}), c)
    return {m: c for m, c in out.items() if c}


def smul(F, G):
    out = {}
    for a, ca in F.items():
        for b, cb in G.items():
            k = tuple(x + y for x, y in zip(a, b))
            out[k] = aadd(out.get(k, {}), amul(ca, cb))
    return {m: c for m, c in out.items() if c}


def lift(p):
    """integer K-form -> symbolic K-form"""
    return {m: {Z9: c} for m, c in p.items() if c}


def sscale(F, c):
    return {m: ascale(v, c) for m, v in F.items()}


def spair(F, G):
    """apolar pairing of two symbolic K-forms of the same degree -> A-poly."""
    tot = {}
    for m, cg in G.items():
        cf = F.get(m)
        if not cf:
            continue
        w = 1
        for e in m:
            w *= factorial(e)
        tot = aadd(tot, ascale(amul(cf, cg), w))
    return tot


def main():
    t0 = time.time()
    out = {}
    Avar = [{tuple(1 if t == n else 0 for t in range(9)): 1} for n in range(9)]

    # s_A = sum_n A_n K_n
    s_sym = {B.unit(n): Avar[n] for n in range(9)}
    # q_A = sum_ij A_ij cof_ij(K)
    q_sym = {}
    for i in B.COL:
        for j in B.COL:
            q_sym = sadd(q_sym, smul({Z9: Avar[B.vidx(i, j)]},
                                     lift(B.cof_poly(i, j))))
    # cof_ij(A) as A-polynomials
    def cofA(i, j):
        r = [x for x in range(3) if x != i]
        c = [y for y in range(3) if y != j]
        p = aadd(amul(Avar[B.vidx(r[0], c[0])], Avar[B.vidx(r[1], c[1])]),
                 ascale(amul(Avar[B.vidx(r[0], c[1])],
                             Avar[B.vidx(r[1], c[0])]), -1))
        return p if (i + j) % 2 == 0 else ascale(p, -1)
    shat_sym = {B.unit(B.vidx(i, j)): cofA(i, j) for i in B.COL for j in B.COL}
    detK = lift(B.det_poly())
    phi_sym = sadd(smul(q_sym, q_sym), sscale(smul(shat_sym, detK), -4))
    out["phi_K_terms"] = len(phi_sym)
    out["phi_max_A_terms_per_K_monomial"] = max(len(v)
                                                for v in phi_sym.values())
    print(f"phi_A symbolically: {len(phi_sym)} K-monomials, up to "
          f"{out['phi_max_A_terms_per_K_monomial']} A-terms each")

    # ---- the two generator families of J_4(A), symbolically
    n_bad, n_tot = 0, 0
    worst = None
    for n in range(9):
        Kn = {B.unit(n): {Z9: 1}}
        for mu, nu in B.sigma_basis(3):
            g = smul(Kn, lift(dict(B.iota(3, mu, nu))))
            p = spair(phi_sym, g)
            n_tot += 1
            if p:
                n_bad += 1
                worst = ("k=3", n, mu, nu, len(p))
        for mu, nu in B.sigma_basis(2):
            g = smul(Kn, smul(s_sym, lift(dict(B.iota(2, mu, nu)))))
            p = spair(phi_sym, g)
            n_tot += 1
            if p:
                n_bad += 1
                worst = ("k=2", n, mu, nu, len(p))
    out["symbolic_pairings_checked"] = n_tot
    out["symbolic_pairings_nonzero"] = n_bad
    out["PROVED_phi_in_perp_for_every_A"] = (n_bad == 0)
    print(f"symbolic pairings <phi_A, generator> checked: {n_tot}, "
          f"nonzero: {n_bad}  {worst if worst else ''}")

    # ---- MUTATION CONTROL: the same symbolic check must FAIL for q^2 - 3 shat
    #      det and for the transposed-cofactor variant
    def symbolic_bad(F):
        bad = 0
        for n in range(9):
            Kn = {B.unit(n): {Z9: 1}}
            for mu, nu in B.sigma_basis(3):
                if spair(F, smul(Kn, lift(dict(B.iota(3, mu, nu))))):
                    bad += 1
            for mu, nu in B.sigma_basis(2):
                if spair(F, smul(Kn, smul(s_sym,
                                          lift(dict(B.iota(2, mu, nu)))))):
                    bad += 1
        return bad
    mut3 = sadd(smul(q_sym, q_sym), sscale(smul(shat_sym, detK), -3))
    shatT = {B.unit(B.vidx(i, j)): cofA(j, i) for i in B.COL for j in B.COL}
    mutT = sadd(smul(q_sym, q_sym), sscale(smul(shatT, detK), -4))
    b3, bT = symbolic_bad(mut3), symbolic_bad(mutT)
    out["control_q2_minus_3shatdet_nonzero_pairings"] = b3
    out["control_transposed_cofactor_nonzero_pairings"] = bT
    out["symbolic_controls_fire"] = (b3 > 0 and bT > 0)
    print(f"CONTROL: q^2 - 3 shat det -> {b3}/1224 nonzero symbolic pairings; "
          f"transposed cofactors -> {bT}/1224")

    # ---- component identities for the characteristic-polynomial description
    adjA = [[cofA(j, i) for j in range(3)] for i in range(3)]     # adj = cof^T
    N = [[{} for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            acc = {}
            for t in range(3):
                acc = sadd(acc, {B.unit(B.vidx(i, t)): adjA[t][j]})
            N[i][j] = acc

    def e_of(N, r):
        if r == 1:
            o = {}
            for i in range(3):
                o = sadd(o, N[i][i])
            return o
        if r == 2:
            o = {}
            for i, j in ((0, 1), (0, 2), (1, 2)):
                o = sadd(o, sadd(smul(N[i][i], N[j][j]),
                                 sscale(smul(N[i][j], N[j][i]), -1)))
            return o
        o = {}
        from itertools import permutations
        for pi in permutations(range(3)):
            inv = sum(1 for a in range(3) for b in range(a + 1, 3)
                      if pi[a] > pi[b])
            t = {Z9: {Z9: 1}}
            for i in range(3):
                t = smul(t, N[i][pi[i]])
            o = sadd(o, sscale(t, -1 if inv % 2 else 1))
        return o

    detA = {}
    for j in range(3):
        detA = aadd(detA, amul(Avar[B.vidx(0, j)], cofA(0, j)))
    e1, e2, e3 = e_of(N, 1), e_of(N, 2), e_of(N, 3)
    id1 = (e1 == shat_sym)
    id2 = (e2 == {m: amul(detA, v) for m, v in q_sym.items()})
    d2 = amul(detA, detA)
    id3 = (e3 == {m: amul(d2, v) for m, v in detK.items()})
    out["e1_eq_shat"] = id1
    out["e2_eq_detA_times_q"] = id2
    out["e3_eq_detA2_times_detK"] = id3
    print(f"symbolic identities:  e_1(K adj A) = shat_A : {id1}\n"
          f"                      e_2(K adj A) = det(A) q_A : {id2}\n"
          f"                      e_3(K adj A) = det(A)^2 det K : {id3}")

    # ---- and the full discriminant identity, symbolically
    disc = sadd(smul(e2, e2), sscale(smul(e1, e3), -4))
    idfull = (disc == {m: amul(d2, v) for m, v in phi_sym.items()})
    out["disc_eq_detA2_phi_symbolic"] = idfull
    print(f"                      e_2^2 - 4 e_1 e_3 = det(A)^2 phi_A : "
          f"{idfull}")

    out["seconds"] = round(time.time() - t0, 1)
    with open(HERE + "/b9_c2_symbolic.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote b9_c2_symbolic.json [{out['seconds']}s]")


if __name__ == "__main__":
    main()
