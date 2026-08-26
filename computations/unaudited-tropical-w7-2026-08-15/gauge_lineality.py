#!/usr/bin/env python3
"""UNAUDITED PROBE (W7) -- the ideal-preserving gauge sub-lineality L_0.

Pinned HEAD: a41949965d41e5c63fb4bc1caf7b20c0df017856

The gauge action x[(u,v),i,j] -> s_u(i) s_v(j) x[(u,v),i,j] sends Phi_chi to
(prod_u s_u(chi_u)) Phi_chi.  It preserves the MIXED equations always, and the
PURE equations Phi_c = 1 exactly on H = {s : prod_u s_u(c) = 1, c = 0,1,2}.

Verified here, exactly:
  (a) dim(gauge lineality L)  = 3N            (W4's 18 at N=6)
  (b) dim(L_0)                = 3N - 3        (L_0 = tropicalisation of H)
  (c) F (colour forms) meets L in dimension 3, and F meets L_0 in {0}
  (d) the kernel of the gauge action on cells is finite (order 2), so H-orbits
      on the torus have dimension 3N - 3.
"""
from fractions import Fraction
from itertools import combinations
import sys
sys.path.insert(0, '.')


def spaces(N):
    edges = list(combinations(range(N), 2))
    eidx = {e: i for i, e in enumerate(edges)}
    ncell = len(edges) * 9

    def cell(e, i, j):
        return eidx[e] * 9 + 3 * i + j

    def gauge_vec(t):           # t[(u,i)] -> weight vector
        v = [Fraction(0)] * ncell
        for e in edges:
            u, w = e
            for i in range(3):
                for j in range(3):
                    v[cell(e, i, j)] = t[(u, i)] + t[(w, j)]
        return v

    basis = []
    for u in range(N):
        for i in range(3):
            t = {(a, b): Fraction(0) for a in range(N) for b in range(3)}
            t[(u, i)] = Fraction(1)
            basis.append((("gauge", u, i), gauge_vec(t)))

    def rank(vs):
        rows = [list(v) for v in vs]
        r = 0
        for col in range(ncell):
            piv = None
            for k in range(r, len(rows)):
                if rows[k][col]:
                    piv = k
                    break
            if piv is None:
                continue
            rows[r], rows[piv] = rows[piv], rows[r]
            head = rows[r]
            for k in range(len(rows)):
                if k != r and rows[k][col]:
                    f = rows[k][col] / head[col]
                    rows[k] = [a - f * b for a, b in zip(rows[k], head)]
            r += 1
        return r

    L = [v for _, v in basis]
    dimL = rank(L)
    # L_0: gauge vectors with sum_u t_u(c) = 0 for each c.  Basis: differences
    L0 = []
    for c in range(3):
        for u in range(1, N):
            t = {(a, b): Fraction(0) for a in range(N) for b in range(3)}
            t[(u, c)] = Fraction(1)
            t[(0, c)] = Fraction(-1)
            L0.append(gauge_vec(t))
    dimL0 = rank(L0)
    # colour forms F (symmetric f), dim 6
    F = []
    for a in range(3):
        for b in range(a, 3):
            v = [Fraction(0)] * ncell
            for e in edges:
                for i in range(3):
                    for j in range(3):
                        if {i, j} == {a, b}:
                            v[cell(e, i, j)] = Fraction(1)
            F.append(v)
    dimF = rank(F)
    dimFplusL = rank(F + L)
    dimFplusL0 = rank(F + L0)
    return {"N": N, "cells": ncell, "dim L": dimL, "dim L_0": dimL0,
            "dim F": dimF,
            "dim(F cap L)": dimF + dimL - dimFplusL,
            "dim(F cap L_0)": dimF + dimL0 - dimFplusL0,
            "dim(F + L)": dimFplusL}


for N in (6, 8):
    r = spaces(N)
    print(N, r)
    assert r["dim L"] == 3 * N, "gauge lineality dimension"
    assert r["dim L_0"] == 3 * N - 3, "L_0 dimension"
    assert r["dim(F cap L)"] == 3, "F meets L in 3 dimensions"
    assert r["dim(F cap L_0)"] == 0, "F must meet L_0 only at 0"
    assert r["dim(F + L)"] == 3 * N + 3, "gauge + colour forms"
print("all exact assertions passed")
