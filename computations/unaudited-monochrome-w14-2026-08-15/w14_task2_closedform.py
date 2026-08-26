#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 2: the CLOSED-FORM higher-layer laws.

  h = 2, degree 3 :  perp(J_3) = <det K>              (A-independent)
  h = 3, degree 4 :  perp(J_4(A)) = <phi_A>,  phi_A = q_A^2 - 4 * shat * det,
        q_A(K)  = sum_ij A_ij cof_ij(K)  = D_A det(K)   (quadratic in K)
        shat(K) = sum_ij cof_ij(A) K_ij  = <K, cof A>   (the COFACTOR cap form)
  equivalently phi_A = e_2(N)^2 - 4 e_1(N) e_3(N) with N = K adj(A), i.e. the
  discriminant of the truncated characteristic polynomial of N.

Verified here on random full-rank A: (i) the perp of the degree-4 layer is
exactly 1-dimensional and spanned by phi_A; (ii) the induced exclusion table
agrees with Singular's exact ideal membership.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)

from w14_core import (COLORS, NCAP, det3, kidx, l_monomials, mono_name,
                      mono_poly, poly_add, poly_mul, poly_pow, poly_row,
                      poly_scale, rank3, require, no_zero_row_or_col)
from w14_task2_obstruction import (apolar_pair, degree4_obstruction, det_poly,
                                   poly_from_row)
from w14_task2_layers import layer_query, parse, run_singular


def cof(A, i, j):
    r = [x for x in range(3) if x != i]
    c = [y for y in range(3) if y != j]
    v = A[r[0]][c[0]] * A[r[1]][c[1]] - A[r[0]][c[1]] * A[r[1]][c[0]]
    return v if (i + j) % 2 == 0 else -v


def cof_poly(i, j):
    """cof_ij(K) as a quadratic polynomial in K."""
    r = [x for x in range(3) if x != i]
    c = [y for y in range(3) if y != j]
    p = {tuple(sorted((kidx(r[0], c[0]), kidx(r[1], c[1])))): 1,
         tuple(sorted((kidx(r[0], c[1]), kidx(r[1], c[0])))): -1}
    return p if (i + j) % 2 == 0 else {m: -v for m, v in p.items()}


def phi_closed(A):
    """phi_A = q_A^2 - 4 * shat * det  (exact integer polynomial)."""
    q = {}
    for i in COLORS:
        for j in COLORS:
            if A[i][j]:
                q = poly_add(q, poly_scale(cof_poly(i, j), A[i][j]))
    shat = {(kidx(i, j),): cof(A, i, j) for i in COLORS for j in COLORS
            if cof(A, i, j)}
    return poly_add(poly_mul(q, q), poly_scale(poly_mul(shat, det_poly()), -4))


def main():
    t0 = time.time()
    rng = random.Random(9081726)
    out = []
    print("== W14 Task 2: closed form for the degree-4 obstruction (h = 3) ==")
    print("   phi_A = q_A^2 - 4 <K,cof A> det K,  q_A = sum A_ij cof_ij(K)\n")
    trials = 0
    while trials < 6:
        A = [[rng.randint(-5, 5) for _ in COLORS] for _ in COLORS]
        if rank3(A) != 3:
            continue
        trials += 1
        bad_dim, sols = degree4_obstruction(A)
        phi = phi_closed(A)
        prow = [Fraction(x) for x in poly_row(phi, 4)]
        ok_dim = (len(sols) == 1)
        prop = None
        if ok_dim:
            v = sols[0]
            ratio = None
            for a, b in zip(prow, v):
                if a != 0:
                    ratio = b / a
                    break
            prop = all(b == ratio * a for a, b in zip(prow, v))
        # exclusion table from the closed form
        excl = sorted(mono_name(a, b) for a, b in l_monomials(4)
                      if apolar_pair(phi, mono_poly(a, b,
                                                    [A[i][j] for i in COLORS
                                                     for j in COLORS]), 4) != 0)
        # Singular ground truth
        tag = f"rand{trials}"
        table = parse(run_singular(layer_query(3, A, (4,), tag)))[tag]
        sing_excl = sorted(m for m, v in table["mem"][4].items() if not v)
        agree = (excl == sing_excl)
        print(f"  A det {det3(A):6d}  no-zero-row/col {no_zero_row_or_col(A)}: "
              f"perp dim {len(sols)}, closed form spans it: {prop}, "
              f"exclusion table matches Singular: {agree} "
              f"({len(excl)} excluded)")
        if not agree:
            print(f"      closed form : {excl}")
            print(f"      Singular    : {sing_excl}")
        out.append({"A": A, "det": det3(A), "perp_dim": len(sols),
                    "closed_form_spans": prop, "excl_closed": excl,
                    "excl_singular": sing_excl, "agree": agree})
    with open(HERE + "/results_task2_closedform.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"\nwrote results_task2_closedform.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
