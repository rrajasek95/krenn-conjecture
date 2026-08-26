#!/usr/bin/env python3
"""A11 STEP 0 -- engine self-test.  UNAUDITED.

Positive controls, mutation controls and the identities my own engine has to
reproduce before any verdict is worth anything:

  S0  census      Gamma / singles / live / clean / Gamma-PM / degrees
                  rebuilt from the masks alone, matched against the recorded
                  census, AND the m=25 neighbour set N(6) computed exactly.
  S1  Phi routes  raw 105-matching enumeration vs the sigma decomposition (1)
                  at RANDOM blocks (an identity, so random blocks are the
                  right test bed).
  S2  master (M)  hafL*Phi(t) = <B, ROW(t)> at RANDOM blocks, both sides
                  independent (LHS by the raw 105-matching route).
  S3  cofactor    Phi(w|v=t) = <S'(tau)_t, Q(w)> at RANDOM blocks, LHS raw.
  S4  MUT-A       perturbing one Gamma cell must BREAK (C) against the
                  unperturbed Phi.
  S5  MUT-B       perturbing one Gamma cell must BREAK (M).
  S6  neg-ctrl    a deliberately WRONG slice matrix (columns permuted /
                  sigma column dropped) must break (C).
"""
from __future__ import annotations

import json
import os
import random
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a11_lib as A  # noqa: E402

DECL = ["S0_census", "S1_phi_two_routes", "S2_master_relation",
        "S3_cofactor_identity", "S4_mutA_cofactor", "S5_mutB_master",
        "S6_wrong_slice_negative_control"]

CENSUS = {
    25: dict(n_gamma=13, n_live=10, n_clean=2624, n_gamma_pms=8,
             deg=(4, 4, 4, 3, 3, 3, 2, 3)),
    26: dict(n_gamma=14, n_live=12, n_clean=2152, n_gamma_pms=11,
             deg=(4, 4, 4, 4, 3, 3, 3, 3)),
    27: dict(n_gamma=15, n_live=12, n_clean=2152, n_gamma_pms=12,
             deg=(4, 4, 4, 4, 4, 3, 4, 3)),
    28: dict(n_gamma=16, n_live=12, n_clean=2152, n_gamma_pms=16,
             deg=(4, 4, 4, 4, 4, 4, 4, 4)),
}

FIELDS = [A.Rat, A.Modp(13), A.Modp(31)]


def main():
    man = A.Manifest(DECL)
    rng = random.Random(20260820)

    # ---------------------------------------------------------- S0 census
    cen = {}
    mism = []
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        got = dict(n_gamma=len(tm.gamma), n_live=len(tm.live),
                   n_clean=len(tm.clean_words),
                   n_gamma_pms=len(tm.gamma_pms),
                   deg=tuple(tm.deg(v) for v in range(8)))
        cen[m] = dict(got, absent=sorted(tm.absent),
                      nbr6=list(tm.nbr[6]), nbr5=list(tm.nbr[5]),
                      gamma=[list(e) for e in sorted(tm.gamma)],
                      live=[list(e) for e in sorted(tm.live)],
                      singles={str(e): v for e, v in
                               sorted(tm.single.items())})
        for k, v in CENSUS[m].items():
            if got[k] != v:
                mism.append((m, k, got[k], v))
    n6 = A.T(25).nbr[6]
    man.record("S0_census", dict(
        census=cen, mismatches=mism, ok=(not mism),
        m25_N6=list(n6), m25_N6_is_5_7=(tuple(n6) == (5, 7)),
        note="rebuilt from the 28-entry masks alone"))
    print("S0 census mismatches=%d  N(6)@25=%s" % (len(mism), n6))

    # ------------------------------------------------------- S1 Phi routes
    n1 = v1 = 0
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for K in FIELDS:
            for _ in range(4):
                bl = A.random_blocks(tm, K, rng)
                for _w in range(6):
                    w = tuple(rng.randrange(3) for _ in range(8))
                    n1 += 1
                    if not K.iszero(K.sub(A.phi_raw(tm, bl, w, K),
                                          A.phi_decomp(tm, bl, w, K))):
                        v1 += 1
    man.record("S1_phi_two_routes", dict(tests=n1, violations=v1, ok=v1 == 0))
    print("S1 phi two routes %d tests %d violations" % (n1, v1))

    # ---------------------------------------------------- S2 master relation
    n2 = v2 = 0
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for K in FIELDS:
            for _ in range(3):
                bl = A.random_blocks(tm, K, rng)
                for lab in A.VLAB:
                    kind, v = A.vsplit(lab)
                    for _w in range(3):
                        w = tuple(rng.randrange(3) for _ in range(8))
                        rows, coef, scale, cols = A.master_rows(
                            tm, bl, kind, v, w, K)
                        for t in range(3):
                            ww = tuple(w[:v] + (t,) + w[v + 1:])
                            lhs = K.mul(scale, A.phi_raw(tm, bl, ww, K))
                            rhs = K.zero
                            for j in range(3):
                                rhs = K.add(rhs, K.mul(coef[j], rows[t][j]))
                            n2 += 1
                            if not K.iszero(K.sub(lhs, rhs)):
                                v2 += 1
    man.record("S2_master_relation",
               dict(tests=n2, violations=v2, ok=v2 == 0,
                    note="RANDOM blocks, no cleanness; LHS by raw 105-matching"))
    print("S2 master relation %d tests %d violations" % (n2, v2))

    # -------------------------------------------------- S3 cofactor identity
    n3 = v3 = 0
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for K in FIELDS:
            for _ in range(3):
                bl = A.random_blocks(tm, K, rng)
                for v in range(8):
                    ns = tm.nbr[v]
                    for _w in range(3):
                        w = tuple(rng.randrange(3) for _ in range(8))
                        tau = tuple(w[s] for s in ns)
                        Sm = A.slice_S(tm, bl, v, tau, K)
                        Q = A.cofactorQ(tm, bl, v, w, K)
                        for t in range(3):
                            ww = tuple(w[:v] + (t,) + w[v + 1:])
                            lhs = A.phi_raw(tm, bl, ww, K)
                            rhs = K.zero
                            for j in range(len(ns)):
                                rhs = K.add(rhs, K.mul(Sm[t][j], Q[j]))
                            n3 += 1
                            if not K.iszero(K.sub(lhs, rhs)):
                                v3 += 1
    man.record("S3_cofactor_identity",
               dict(tests=n3, violations=v3, ok=v3 == 0,
                    note="RANDOM (hence non-clean) blocks; LHS raw"))
    print("S3 cofactor identity %d tests %d violations" % (n3, v3))

    # ------------------------------------------------------------- S4 MUT-A
    fired = tot = 0
    for m in (25, 28):
        tm = A.T(m)
        for K in FIELDS:
            bl = A.random_blocks(tm, K, rng)
            base = {v: {} for v in range(8)}
            wlist = [tuple(rng.randrange(3) for _ in range(8))
                     for _ in range(4)]
            for v in range(8):
                for w in wlist:
                    base[v][w] = [A.phi_raw(tm, bl, tuple(
                        w[:v] + (t,) + w[v + 1:]), K) for t in range(3)]
            for _ in range(6):
                # LOAD-BEARING perturbation: the cell must be one the tested
                # words actually use, else non-detection is meaningless.
                w0 = wlist[rng.randrange(len(wlist))]
                e = sorted(tm.gamma)[rng.randrange(len(tm.gamma))]
                a, b = w0[e[0]], w0[e[1]]
                old = bl[e][a][b]
                delta = K.zero
                while K.iszero(delta):
                    delta = K.of(1 + rng.randrange(50))
                bl[e][a][b] = K.add(old, delta)
                brk = False
                for v in range(8):
                    ns = tm.nbr[v]
                    for w in wlist:
                        tau = tuple(w[s] for s in ns)
                        Sm = A.slice_S(tm, bl, v, tau, K)
                        Q = A.cofactorQ(tm, bl, v, w, K)
                        for t in range(3):
                            rhs = K.zero
                            for j in range(len(ns)):
                                rhs = K.add(rhs, K.mul(Sm[t][j], Q[j]))
                            if not K.iszero(K.sub(base[v][w][t], rhs)):
                                brk = True
                bl[e][a][b] = old
                tot += 1
                fired += 1 if brk else 0
    man.record("S4_mutA_cofactor",
               dict(perturbations=tot, detected=fired, ok=fired == tot,
                    note="one perturbed Gamma cell must break (C) vs the "
                         "unperturbed Phi"))
    print("S4 MUT-A %d/%d fired" % (fired, tot))

    # ------------------------------------------------------------- S5 MUT-B
    fired = tot = 0
    for m in (25, 27):
        tm = A.T(m)
        for K in FIELDS:
            bl = A.random_blocks(tm, K, rng)
            wlist = [tuple(rng.randrange(3) for _ in range(8))
                     for _ in range(4)]
            base = {}
            for lab in A.VLAB:
                kind, v = A.vsplit(lab)
                for w in wlist:
                    _r, _c, sc, _co = A.master_rows(tm, bl, kind, v, w, K)
                    base[(lab, w)] = [
                        K.mul(sc, A.phi_raw(tm, bl, tuple(
                            w[:v] + (t,) + w[v + 1:]), K)) for t in range(3)]
            for _ in range(6):
                w0 = wlist[rng.randrange(len(wlist))]
                e = sorted(tm.gamma)[rng.randrange(len(tm.gamma))]
                a, b = w0[e[0]], w0[e[1]]
                old = bl[e][a][b]
                delta = K.zero
                while K.iszero(delta):
                    delta = K.of(1 + rng.randrange(50))
                bl[e][a][b] = K.add(old, delta)
                brk = False
                for lab in A.VLAB:
                    kind, v = A.vsplit(lab)
                    for w in wlist:
                        rows, coef, sc, cols = A.master_rows(
                            tm, bl, kind, v, w, K)
                        for t in range(3):
                            rhs = K.zero
                            for j in range(3):
                                rhs = K.add(rhs, K.mul(coef[j], rows[t][j]))
                            if not K.iszero(K.sub(base[(lab, w)][t], rhs)):
                                brk = True
                bl[e][a][b] = old
                tot += 1
                fired += 1 if brk else 0
    man.record("S5_mutB_master",
               dict(perturbations=tot, detected=fired, ok=fired == tot))
    print("S5 MUT-B %d/%d fired" % (fired, tot))

    # ------------------------------------------------- S6 wrong-slice control
    bad = 0
    tot6 = 0
    for m in (25, 27, 28):
        tm = A.T(m)
        K = A.Modp(31)
        bl = A.random_blocks(tm, K, rng)
        for v in range(8):
            ns = tm.nbr[v]
            if len(ns) < 2:
                continue
            for _w in range(3):
                w = tuple(rng.randrange(3) for _ in range(8))
                tau = tuple(w[s] for s in ns)
                Q = A.cofactorQ(tm, bl, v, w, K)
                # WRONG object 1: drop the last column (the predecessor S)
                # WRONG object 2: reverse the column order
                for variant in (0, 1):
                    tot6 += 1
                    ok_all = True
                    for t in range(3):
                        Sm = A.slice_S(tm, bl, v, tau, K)
                        if variant == 0:
                            row = Sm[t][:-1] + [K.zero]
                        else:
                            row = list(reversed(Sm[t]))
                        rhs = K.zero
                        for j in range(len(ns)):
                            rhs = K.add(rhs, K.mul(row[j], Q[j]))
                        if not K.iszero(K.sub(A.phi_raw(tm, bl, tuple(
                                w[:v] + (t,) + w[v + 1:]), K), rhs)):
                            ok_all = False
                    if ok_all:
                        bad += 1
    man.record("S6_wrong_slice_negative_control",
               dict(variants_tested=tot6, variants_that_still_satisfied_C=bad,
                    ok=bad < tot6,
                    note="a mangled slice matrix must break (C) -- if it did "
                         "not, the identity test would be vacuous"))
    print("S6 wrong-slice: %d/%d mangled variants still satisfied (C)"
          % (bad, tot6))

    man.finish(os.path.join(HERE, "results_t0.json"),
               extra={"_header": "UNAUDITED A11 engine self-test"})
    print("T0 DONE")


if __name__ == "__main__":
    main()
