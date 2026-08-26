#!/usr/bin/env python3
"""Exact sparse discovery interface for D0=0, C0!=0 in the k4 cycle.

After the four upper cofactors are solved, D0=d1*d4+d3 is set to zero.
The two endpoint cofactors solve b1,b3 with determinant
-2*b0*d1*(b0^2+d4^2).  The remaining literal rows are evaluated directly
in a rational-function field, avoiding expensive expanded SymPy substitution.
They form a linear augmented system for (a0,a5); this probe reports its exact
rank-minor structure without claiming closure.
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
from sympy.polys.domains import QQ
from sympy.polys.fields import field


HERE = Path(__file__).resolve().parent
GENERIC = HERE / "discover_branch0_k4_cycle_cramer_generic.py"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_d0_generic", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(GENERIC)


def derive():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]
    d0 = {d3: -d1*d4}

    def endpoint_core(label):
        top = sp.cancel(rows[label].subs(p_solution).subs(d0)) \
            .as_numer_denom()[0]
        return max((factor for factor, _ in sp.factor_list(top)[1]),
                   key=lambda value:
                   len(sp.Poly(value, b0, b1, b3, d1, d4).terms()))

    e0 = endpoint_core("cofactor_0_0")
    e5 = endpoint_core("cofactor_5_0")
    matrix, _ = sp.linear_eq_to_matrix([e0, e5], [b1, b3])
    c0 = b0**2+d4**2
    if sp.factor(matrix.det()) != -2*b0*d1*c0:
        raise RuntimeError("endpoint determinant changed")
    endpoint = sp.solve([e0, e5], [b1, b3], dict=True,
                        simplify=False)[0]

    rational_field, _, _, _, _, _ = field("b0,d1,d4,a0,a5", QQ)
    substitutions = dict(d0)
    substitutions.update(endpoint)
    values = [rational_field.from_expr(sp.cancel(
        p_solution[variable].subs(substitutions))) for variable in SOURCE.P]
    values += [rational_field.from_expr(a0), rational_field.from_expr(a5)]
    values += [rational_field.from_expr(sp.cancel(
        substitutions.get(variable, variable)))
        for variable in SOURCE.PARAMETERS]

    def evaluate(poly):
        answer = rational_field.zero
        for exponent, coefficient in poly.items():
            term = rational_field.from_expr(sp.Rational(
                coefficient.numerator, coefficient.denominator))
            for value, power in zip(values, exponent):
                term *= value**power
            answer += term
        return sp.primitive(sp.Poly(answer.numer.as_expr(),
                                    b0, d1, d4, a0, a5))[1].as_expr()

    labels = ("t_012", "t_013", "t_023", "t_123",
              "cofactor_0_3", "cofactor_5_3")
    residual = [(label, evaluate(raw[label])) for label in labels]
    return (b0, d1, d4, a0, a5), residual, c0


def main():
    variables, residual, c0 = derive()
    b0, d1, d4, a0, a5 = variables
    print("C0:", c0)
    for label, value in residual:
        poly = sp.Poly(value, *variables)
        print(label, "terms", len(poly.terms()), "degree(a0,a5)",
              sp.Poly(value, a0, a5).total_degree())
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    augmented = matrix.row_join(rhs)
    for index in range(len(equations)):
        print("linear row", index,
              [len(sp.Poly(matrix[index, column], b0, d1, d4).terms())
               for column in range(2)],
              len(sp.Poly(rhs[index], b0, d1, d4).terms()))
    pair_sizes = []
    for rows in __import__("itertools").combinations(range(len(equations)), 2):
        value = sp.expand(matrix[list(rows), :].det())
        if value != 0:
            pair_sizes.append((rows, len(sp.Poly(value, b0, d1, d4).terms())))
    print("nonzero 2x2 coefficient minors:", sorted(pair_sizes,
                                                     key=lambda item: item[1]))
    nonzero = []
    for rows in __import__("itertools").combinations(range(len(equations)), 3):
        value = sp.expand(augmented[list(rows), :].det())
        if value != 0:
            nonzero.append((rows, value))
    print("nonzero 3x3 minors:", len(nonzero))
    for rows, value in nonzero:
        print(rows, "terms", len(sp.Poly(value, b0, d1, d4).terms()),
              "degree", sp.Poly(value, b0, d1, d4).total_degree())


if __name__ == "__main__":
    main()
