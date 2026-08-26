#!/usr/bin/env python3
"""Discovery probe for Au=0 in Delta=0, Bplus!=0."""

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
INTERFACE_PATH = HERE / "audit_branch0_cycle_delta_zero_linear_interface.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INTERFACE = load("n8_cycle_delta_au_source", INTERFACE_PATH)
SOURCE = INTERFACE.SOURCE


def main():
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in SOURCE.SOURCE.data()[0]}
    p1, p2, p3, p4 = SOURCE.P
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    ratio = {b3: x*b1, d3: -x*d1*d4}
    upper = [sp.factor(rows[f"cofactor_{edge}_0"].subs(ratio))
             for edge in range(1, 5)]
    p3_p4 = sp.solve([upper[2], upper[3]], [p4, p3], dict=True,
                     simplify=False)[0]
    u = sp.factor(-sp.cancel(upper[0].subs(p3_p4))/d4)
    v = sp.factor(sp.cancel(upper[1].subs(p3_p4))
                  /(b1**2*d1*d4*x))
    branch = {
        b0: -d1,
        x: 1/d1**2,
        d4: -d1**3*(d1 + 1)/(d1 - 1),
    }
    print("U:", sp.factor(sp.cancel(u.subs(branch))))
    print("V:", sp.factor(sp.cancel(v.subs(branch))))

    labels = ("t_012", "t_013", "cofactor_5_0", "t_023", "t_123",
              "cofactor_0_0", "cofactor_0_3")
    reduced = {label: sp.cancel(rows[label].subs(ratio).subs(p3_p4))
               for label in labels}
    a0_row = sp.cancel(reduced["cofactor_5_0"].subs(branch))
    a0_value = sp.solve(a0_row, a0, dict=True, simplify=False)[0][a0]
    current = {label: sp.cancel(value.subs(branch).subs(a0, a0_value))
               for label, value in reduced.items()
               if label != "cofactor_5_0"}
    unknowns = (p1, p2, a5)
    for label, value in current.items():
        entries = [sp.cancel(sp.diff(value, variable))
                   for variable in unknowns]
        entries.append(sp.cancel(value.subs({variable: 0
                                             for variable in unknowns})))
        print("linear", label, [len(sp.Poly(
            entry.as_numer_denom()[0], b1, d1).terms())
            if entry else 0 for entry in entries])

    solved = {}
    solve_coefficients = {}
    for label, variable in (("t_012", p1), ("t_013", p2),
                            ("t_023", a5)):
        row = sp.cancel(current[label].subs(solved))
        coefficient = sp.factor(sp.diff(row, variable))
        solve_coefficients[label] = coefficient
        print("solve", label, variable, "coefficient", coefficient)
        solved[variable] = sp.cancel(sp.solve(
            row, variable, dict=True, simplify=False)[0][variable]
            .subs(solved))
    finals = []
    for label in ("t_123", "cofactor_0_0", "cofactor_0_3"):
        top = sp.cancel(current[label].subs(solved)).as_numer_denom()[0]
        core = max((factor for factor, _ in sp.factor_list(top)[1]),
                   key=lambda factor: sp.Poly(factor, b1, d1).total_degree())
        finals.append(core)
        print("final", label, sp.factor(top))
    resultants = []
    for left in range(3):
        for right in range(left + 1, 3):
            value = sp.factor(sp.resultant(finals[left], finals[right], b1))
            resultants.append(value)
            print("resultant", left, right, value)
    common = sp.factor(sp.gcd(sp.gcd(resultants[0], resultants[1]),
                              resultants[2]))
    print("common resultant gcd", common)
    for factor, exponent in sp.factor_list(common)[1]:
        if sp.Poly(factor, d1).degree() == 1 and factor in (d1, d1-1, d1+1):
            continue
        gb = sp.groebner([factor, *finals], b1, d1, order="lex")
        print("candidate", factor, "gb")
        for polynomial in gb.polys:
            print(sp.factor(polynomial.as_expr()))

    candidate = d1**2 + 3*d1 - 1
    b1_value = (3*d1 - 2)/13
    qpoly = sp.Poly(candidate, d1, domain="QQ")

    for label, coefficient in solve_coefficients.items():
        top = sp.cancel(coefficient.subs(b1, b1_value)).as_numer_denom()[0]
        print("candidate coefficient", label,
              sp.factor(sp.rem(sp.Poly(top, d1, domain="QQ"),
                               qpoly).as_expr()))

    for label, variable in (("t_012", p1), ("t_013", p2)):
        row = current[label]
        coefficient_top = sp.cancel(sp.diff(row, variable)) \
            .as_numer_denom()[0]
        constant_top = sp.cancel(row.subs(variable, 0)) \
            .as_numer_denom()[0]
        print("exception", label, "resultant",
              sp.factor(sp.resultant(coefficient_top, constant_top, b1)))
        exception_rows = [sp.cancel(value).as_numer_denom()[0]
                          for value in current.values()]
        if label == "t_013":
            for factor in (d1**2 + 2*d1 - 1, d1**3 + 2*d1 - 1):
                factor_gb = sp.groebner(
                    [factor, coefficient_top, *exception_rows],
                    p1, p2, a5, b1, d1, order="grevlex")
                print("exception", label, "factor", factor,
                      "unit", any(polynomial.as_expr() == 1
                                  for polynomial in factor_gb.polys),
                      "size", len(factor_gb.polys))
                if len(factor_gb.polys) <= 8:
                    for polynomial in factor_gb.polys:
                        print("  ", sp.factor(polynomial.as_expr()))
                if factor == d1**2 + 2*d1 - 1:
                    q2_values = {p1: -1, p2: -1, a5: 0,
                                 b1: (d1 - 1)/2}
                    raw_h = SOURCE.SOURCE.data()[1]
                    h = SOURCE.expression(raw_h)
                    hq = sp.cancel(h.subs(ratio).subs(p3_p4).subs(branch)
                                   .subs(a0, a0_value.subs(branch))
                                   .subs(q2_values))
                    print("  q2 H", sp.factor(hq))
            continue
        exception_gb = sp.groebner([coefficient_top, *exception_rows],
                                   p1, p2, a5, b1, d1, order="grevlex")
        print("exception", label, "GB size", len(exception_gb.polys),
              "unit", exception_gb.is_zero_dimensional
              and any(polynomial.as_expr() == 1
                      for polynomial in exception_gb.polys))
        if len(exception_gb.polys) <= 12:
            for polynomial in exception_gb.polys:
                print(sp.factor(polynomial.as_expr()))
        if label == "t_012":
            print("t012 live target reductions")
            for target in (b1, d1, d1 + 1, b1 + d1):
                print(sp.factor(target), "->",
                      sp.factor(exception_gb.reduce(target)[1]))

    special_rows = [sp.cancel(current[label].subs(b1, b1_value))
                    .as_numer_denom()[0]
                    for label in current]
    special_gb = sp.groebner([candidate, *special_rows],
                             p1, p2, a5, d1, order="lex")
    print("candidate unsolved linear GB")
    for polynomial in special_gb.polys:
        print(sp.factor(polynomial.as_expr()))
    return

    def reduce_candidate(value):
        top, bottom = sp.cancel(value.subs(b1, b1_value)).as_numer_denom()
        inverse = sp.invert(sp.Poly(bottom, d1, domain="QQ"), qpoly)
        return sp.factor(sp.rem(sp.Poly(top, d1, domain="QQ")*inverse,
                                qpoly).as_expr())

    p3_value = sp.cancel(p3_p4[p3].subs(branch).subs(solved))
    p4_value = sp.cancel(p3_p4[p4].subs(branch).subs(solved))
    print("candidate q2 values")
    for name, value in (("p1", solved[p1]), ("p2", solved[p2]),
                        ("p3", p3_value), ("p4", p4_value),
                        ("a0", a0_value.subs(branch)),
                        ("a5", solved[a5])):
        print(name, reduce_candidate(value),
              "plus1", reduce_candidate(value + 1)
              if name.startswith("p") else "")
    raw_h = SOURCE.SOURCE.data()[1]
    h = SOURCE.expression(raw_h)
    h_value = sp.cancel(h.subs(ratio).subs(p3_p4).subs(branch)
                        .subs(a0, a0_value.subs(branch)).subs(solved))
    print("H", reduce_candidate(h_value))


if __name__ == "__main__":
    main()
