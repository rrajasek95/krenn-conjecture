#!/usr/bin/env python3
"""Exploratory exact reductions on the Delta=0 cycle branch.

This is a discovery probe only.  It prints factorized consistency equations
for the rank-deficient four-row upper cofactor system and does not certify an
emptiness theorem.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "discover_branch0_k4_cycle_cramer_generic.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_cycle_delta_zero_source", GENERIC)


def main():
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in SOURCE.SOURCE.data()[0]}
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    a0 = SOURCE.A0
    x = sp.Symbol("x")
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    matrix, rhs = sp.linear_eq_to_matrix(upper, SOURCE.P)
    delta = b1*d3 + b3*d1*d4
    delta_sub = {d3: -b3*d1*d4/b1}
    reduced_matrix = matrix.subs(delta_sub)
    reduced_rhs = rhs.subs(delta_sub)
    augmented = reduced_matrix.row_join(reduced_rhs)

    print("reduced upper matrix")
    print(reduced_matrix)
    print("reduced upper rhs")
    print(reduced_rhs)

    print("rank-2 minors after Delta=0")
    minors2 = set()
    for row0 in range(4):
        for row1 in range(row0 + 1, 4):
            for col0 in range(4):
                for col1 in range(col0 + 1, 4):
                    value = sp.factor(reduced_matrix.extract(
                        [row0, row1], [col0, col1]).det())
                    if value:
                        minors2.add(str(value))
    for value in sorted(minors2):
        print(value)

    print("augmented rank-3 consistency cores")
    cores = set()
    for row_indices in ((0, 1, 2), (0, 1, 3),
                        (0, 2, 3), (1, 2, 3)):
        for col_indices in ((0, 1, 4), (0, 2, 4), (0, 3, 4),
                            (1, 2, 4), (1, 3, 4), (2, 3, 4)):
            top = sp.cancel(augmented.extract(
                row_indices, col_indices).det()).as_numer_denom()[0]
            if not top:
                continue
            factors = sp.factor_list(top)[1]
            core = max((factor for factor, _ in factors),
                       key=lambda factor: len(sp.Poly(
                           factor, b0, b1, b3, d1, d4).terms()))
            cores.add(str(sp.factor(core)))
    for value in sorted(cores):
        print(value)

    # The two nonproportional consistency cores obtained above simplify
    # substantially in the ratio b3=x*b1.
    u = (b0**2*b3*d1 - b0**2*b3 + b0*b1
         - b0*b3*d1*d4 - b0*b3*d1 - b0*b3*d4
         - b1*d4 - b3*d1*d4)
    v = (b0**2*b1*b3*d1 + b0**2*b1*b3 - b0*b1**2
         - b0*b1*b3*d1 - b0*b3**2*d1*d4
         + b0*b3**2*d4 + b1*b3*d4 - b3**2*d1*d4)
    ur = sp.factor(u.subs(b3, x*b1)/b1)
    vr = sp.factor(v.subs(b3, x*b1)/b1**2)
    print("U ratio:", ur)
    print("V ratio:", vr)
    print("Res_b0(U,V):", sp.factor(sp.resultant(ur, vr, b0)))
    print("Res_x(U,V):", sp.factor(sp.resultant(ur, vr, x)))
    print("U d4 coefficient:", sp.factor(sp.diff(ur, d4)))
    print("V d4 coefficient:", sp.factor(sp.diff(vr, d4)))
    print("Res_d4(U,V):", sp.factor(sp.resultant(ur, vr, d4)))
    print("b0 subresultants U,V:")
    for polynomial in sp.subresultants(ur, vr, b0):
        print("degree", sp.Poly(polynomial, b0).degree(),
              "terms", len(sp.Poly(polynomial, b0, x, d1, d4).terms()),
              sp.factor(polynomial))

    # Generic Bplus=b1+d1 branch: solve one row in each parity block for
    # p3,p4, leaving p1,p2 free.  Rows 1 and 2 then recover U,V.
    ratio_sub = {b3: x*b1, d3: -x*d1*d4}
    upper_ratio = [sp.factor(poly.subs(ratio_sub)) for poly in upper]
    solved_p = sp.solve([upper_ratio[2], upper_ratio[3]],
                        [SOURCE.P[3], SOURCE.P[2]], dict=True,
                        simplify=False)[0]
    print("generic Delta solve p3:", sp.factor(solved_p[SOURCE.P[2]]))
    print("generic Delta solve p4:", sp.factor(solved_p[SOURCE.P[3]]))
    for index in (0, 1):
        value = sp.factor(sp.cancel(upper_ratio[index].subs(solved_p)))
        print(f"remaining upper {index}:", value)
    labels = ("t_012", "t_013", "cofactor_5_0", "t_023", "t_123",
              "cofactor_0_0", "cofactor_0_3")
    free_variables = (SOURCE.P[0], SOURCE.P[1], SOURCE.A0, SOURCE.A5)
    for label in labels:
        top = sp.cancel(rows[label].subs(ratio_sub).subs(solved_p)) \
            .as_numer_denom()[0]
        polynomial = sp.Poly(top, *free_variables)
        print("residual", label, "terms", len(polynomial.terms()),
              "degree-free", polynomial.total_degree(),
              "degrees", [polynomial.degree(variable)
                           for variable in free_variables])

    reduced = {label: sp.cancel(rows[label].subs(ratio_sub).subs(solved_p))
               for label in labels}
    a0_row = reduced["cofactor_5_0"]
    a0_coefficient = sp.factor(sp.diff(a0_row, SOURCE.A0))
    a0_value = sp.cancel(-(a0_row.subs(SOURCE.A0, 0))/a0_coefficient)
    print("solve cofactor_5_0 for a0 coefficient:", a0_coefficient)
    linear_labels = ("t_012", "t_013", "t_023", "t_123",
                     "cofactor_0_0", "cofactor_0_3")
    unknowns = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    linear_rows = []
    for label in linear_labels:
        value = sp.cancel(reduced[label].subs(SOURCE.A0, a0_value))
        entries = [sp.cancel(sp.diff(value, variable))
                   for variable in unknowns]
        entries.append(sp.cancel(value.subs({variable: 0
                                             for variable in unknowns})))
        linear_rows.append(entries)
        stats = []
        for entry in entries:
            top, bottom = entry.as_numer_denom()
            stats.append((len(sp.Poly(top, b0, b1, x, d1, d4).terms()),
                          len(sp.Poly(bottom, b0, b1, x, d1, d4).terms())))
        print("linear", label, stats)
    # Exceptional Bplus=0 branch uses the complementary two pivots.
    minus_sub = {b1: -d1}
    upper_minus = [sp.factor(poly.subs(minus_sub))
                   for poly in upper_ratio]
    solved_minus = sp.solve([upper_minus[2], upper_minus[3]],
                            [SOURCE.P[1], SOURCE.P[0]], dict=True,
                            simplify=False)[0]
    print("minus p1:", sp.factor(solved_minus[SOURCE.P[0]]))
    print("minus p2:", sp.factor(solved_minus[SOURCE.P[1]]))
    print("minus remaining0/U:", sp.factor(sp.cancel(
        upper_minus[0].subs(solved_minus))/ur))
    print("minus remaining1/V:", sp.factor(sp.cancel(
        upper_minus[1].subs(solved_minus))/vr))
    minus_reduced = {label: sp.cancel(rows[label].subs(ratio_sub)
                                      .subs(minus_sub).subs(solved_minus))
                     for label in labels}
    minus_a0_row = minus_reduced["cofactor_5_0"]
    minus_a0 = sp.solve(minus_a0_row, a0, dict=True,
                        simplify=False)[0][a0]
    for label in labels:
        if label == "cofactor_5_0":
            continue
        value = sp.factor(sp.cancel(minus_reduced[label].subs(a0, minus_a0)))
        print("minus row", label, value)
    x_value = -(d1 + 1)/(d1*(d1 - 1))
    print("minus W solve U:", sp.factor(sp.cancel(ur.subs(x, x_value))))
    print("minus W solve V:", sp.factor(sp.cancel(vr.subs(x, x_value))))
    print("minus W solve Res_b0:", sp.factor(sp.resultant(
        sp.cancel(ur.subs(x, x_value)).as_numer_denom()[0],
        sp.cancel(vr.subs(x, x_value)).as_numer_denom()[0], b0)))
    u_w = sp.cancel(ur.subs(x, x_value)).as_numer_denom()[0]
    v_w = sp.cancel(vr.subs(x, x_value)).as_numer_denom()[0]
    qplus = d1**2 + 2*d1 - 1
    gb_qplus = sp.groebner([qplus, u_w, v_w], b0, d4, d1,
                           order="lex")
    print("minus qplus GB:")
    for polynomial in gb_qplus.polys:
        print(sp.factor(polynomial.as_expr()))
    print("minus W subresultants:")
    for polynomial in sp.subresultants(u_w, v_w, b0):
        print("degree", sp.Poly(polynomial, b0).degree(),
              "terms", len(sp.Poly(polynomial, b0, d1, d4).terms()),
              sp.factor(polynomial))
    p_big = (d1**6*d4**2 + 4*d1**6*d4 + 4*d1**6
             + 4*d1**5*d4**2 + 16*d1**5*d4
             + 7*d1**4*d4**2 + 16*d1**4*d4 + 4*d1**4
             + 8*d1**3*d4**2 + 7*d1**2*d4**2
             - 4*d1**2*d4 + 4*d1*d4**2 + d4**2)
    a_lead = (d1**4*d4 + 2*d1**4 + 4*d1**3*d4
              + 4*d1**2*d4 + 2*d1**2 - d4)
    b0_value = -4*d1**2*d4*(d1 + 1)/a_lead
    deep = {x: x_value, b0: b0_value}
    after_a0 = {label: sp.cancel(minus_reduced[label].subs(a0, minus_a0))
                for label in labels if label != "cofactor_5_0"}
    a5_value = sp.solve(sp.cancel(after_a0["t_123"].subs(deep)),
                        SOURCE.A5, dict=True, simplify=False)[0][SOURCE.A5]
    deep[SOURCE.A5] = a5_value
    p3_value = sp.solve(sp.cancel(after_a0["t_012"].subs(deep)),
                        SOURCE.P[2], dict=True,
                        simplify=False)[0][SOURCE.P[2]]
    p4_value = sp.solve(sp.cancel(after_a0["t_013"].subs(deep)),
                        SOURCE.P[3], dict=True,
                        simplify=False)[0][SOURCE.P[3]]
    p3_branch_row = sp.cancel(after_a0["t_012"].subs(deep))
    p4_branch_row = sp.cancel(after_a0["t_013"].subs(deep))
    for name, row, variable in (("D3", p3_branch_row, SOURCE.P[2]),
                                ("D4", p4_branch_row, SOURCE.P[3])):
        coeff_top = sp.cancel(sp.diff(row, variable)).as_numer_denom()[0]
        const_top = sp.cancel(row.subs(variable, 0)).as_numer_denom()[0]
        rc = sp.factor(sp.resultant(p_big, coeff_top, d4))
        rn = sp.factor(sp.resultant(p_big, const_top, d4))
        print(name, "exception coefficient terms",
              len(sp.Poly(coeff_top, d1, d4).terms()),
              "constant terms", len(sp.Poly(const_top, d1, d4).terms()))
        print(name, "exception resultant coeff", rc)
        print(name, "exception resultant const", rn)
        print(name, "exception resultant gcd", sp.factor(sp.gcd(rc, rn)))
    deep[SOURCE.P[2]] = p3_value
    deep[SOURCE.P[3]] = p4_value
    den_a5 = sp.cancel(a5_value).as_numer_denom()[1]
    den_p3 = sp.cancel(p3_value).as_numer_denom()[1]
    den_p4 = sp.cancel(p4_value).as_numer_denom()[1]
    print("minus P solve denominator a5:", sp.factor(den_a5))
    print("minus P solve denominator p3:", sp.factor(den_p3))
    print("minus P solve denominator p4:", sp.factor(den_p4))
    final_tops = {}
    for label in ("cofactor_0_0", "cofactor_0_3"):
        top = sp.cancel(after_a0[label].subs(deep)).as_numer_denom()[0]
        final_tops[label] = top
        print("minus P final", label, "terms",
              len(sp.Poly(top, d1, d4).terms()), "factor", sp.factor(top))
        print("minus P final resultant", label,
              sp.factor(sp.resultant(p_big, top, d4)))
    qi = d1**2 + 1
    reduce_i = lambda value: sp.factor(sp.rem(
        sp.Poly(value, d1, domain="EX"),
        sp.Poly(qi, d1, domain="EX")).as_expr())
    print("minus P modulo d1^2+1:", reduce_i(p_big))
    print("minus A modulo d1^2+1:", reduce_i(a_lead))
    print("minus den p3 modulo d1^2+1:", reduce_i(den_p3))
    print("minus den p4 modulo d1^2+1:", reduce_i(den_p4))
    print("minus cof00 modulo d1^2+1:",
          reduce_i(final_tops["cofactor_0_0"]))
    print("minus cof03 modulo d1^2+1:",
          reduce_i(final_tops["cofactor_0_3"]))


if __name__ == "__main__":
    main()
