#!/usr/bin/env python3
"""A7 SUB-AUDIT -- symbolic backing for my PROOF of Lemma W20-P4c, case 2.

Case 2 of the proof is: if all three normals have FULL support, choose a
coordinate r, solve each hyperplane constraint for the r-entry
    v^k_r = -sum_{i != r} m_{ki} v^k_i ,   m_{ki} = nv_k[i]/nv_k[r] != 0,
and expand per(u, v^1, v^2, v^3) as a polynomial in the 9 FREE entries
v^k_i (i != r).  We check exactly, with sympy, that

  * with u all-nonzero, "that polynomial is identically 0" is a linear system
    in the 9 unknowns m_{ki} whose ONLY solution is m = 0 -- contradicting
    full support, so case 2 cannot occur;
  * MUTATION CONTROL: if u has a zero coordinate the system acquires a
    nonzero solution space (the statement is then false), so the check is not
    vacuous.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import permutations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp                                                # noqa: E402


def case2_system(uvec, n=4, r=3):
    """returns (n_unknowns, nullity of the linear system on the m's)."""
    free = [i for i in range(n) if i != r]
    M = {(k, i): sp.Symbol("M_%d_%d" % (k, i))
         for k in range(n - 1) for i in free}
    m = {(k, i): sp.Symbol("m_%d_%d" % (k, i))
         for k in range(n - 1) for i in free}
    cols = [list(uvec)]
    for k in range(n - 1):
        col = []
        for i in range(n):
            if i == r:
                col.append(-sum(m[(k, i2)] * M[(k, i2)] for i2 in free))
            else:
                col.append(M[(k, i)])
        cols.append(col)
    P = 0
    for p in permutations(range(n)):
        t = 1
        for j in range(n):
            t *= cols[j][p[j]]
        P += t
    P = sp.expand(P)
    Mv = sorted(M.values(), key=lambda s: s.name)
    poly = sp.Poly(P, *Mv)
    mv = sorted(m.values(), key=lambda s: s.name)
    # each permanent term uses at most one r-row entry, so every coefficient
    # is AFFINE in the m's:  coef = const + sum_t row[t]*m_t.
    rows, rhs, homrows = [], [], []
    for _, coef in poly.terms():
        c = sp.expand(coef)
        row = [sp.expand(sp.diff(c, v)) for v in mv]
        const = sp.expand(c - sum(row[t] * mv[t] for t in range(len(mv))))
        if sp.expand(sp.diff(c, mv[0], mv[0])) != 0:
            return dict(error="coefficient not affine in m")
        rows.append(row)
        rhs.append(-const)
        if const == 0 and any(x != 0 for x in row):
            homrows.append(row)
    A = sp.Matrix(rows)
    b = sp.Matrix(len(rhs), 1, rhs)
    Ab = A.row_join(b)
    H = sp.Matrix(homrows) if homrows else sp.zeros(0, len(mv))
    rA, rAb = A.rank(), Ab.rank()
    return dict(u=[str(x) for x in uvec], n_unknowns=len(mv),
                n_equations=A.rows, rank_A=rA, rank_A_augmented=rAb,
                system_is_INCONSISTENT=(rAb > rA),
                n_homogeneous_equations=H.rows,
                rank_homogeneous_part=(H.rank() if H.rows else 0),
                homogeneous_part_forces_m_zero=(H.rows and H.rank() == len(mv)))


def main():
    res = {"_header": "A7 SUB-AUDIT -- symbolic proof check for W20-P4c "
                      "case 2 (all three normals of full support)."}
    res["all_nonzero_u_generic"] = case2_system((1, 2, 3, 5))
    res["all_nonzero_u_generic2"] = case2_system((7, -3, 2, -11))
    res["all_nonzero_u_symbolic"] = case2_system(sp.symbols("u0 u1 u2 u3"))
    res["MUTATION_u_has_a_zero"] = case2_system((0, 2, 3, 5))
    res["MUTATION_u_has_a_zero_at_r"] = case2_system((1, 2, 3, 0))
    for k, v in res.items():
        if k != "_header":
            print(k, v, flush=True)
    json.dump(res, open(os.path.join(HERE, "a7_results_A6_symbolic.json"),
                        "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
