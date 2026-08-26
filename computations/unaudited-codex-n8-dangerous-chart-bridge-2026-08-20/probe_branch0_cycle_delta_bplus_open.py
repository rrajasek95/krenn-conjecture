#!/usr/bin/env python3
"""Discovery probe for the remaining Delta=0, Bplus!=0 cycle branch."""

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


INTERFACE = load("n8_cycle_delta_bplus_open_source", INTERFACE_PATH)
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
    au = sp.factor(sp.diff(u, d4))
    d4_value = sp.cancel(-u.subs(d4, 0)/au)
    q = sp.factor(sp.resultant(u, v, d4)/b0)
    print("Au:", au)
    print("d4:", d4_value)
    print("Q terms/degree:", len(sp.Poly(q, b0, x, d1).terms()),
          sp.Poly(q, b0, x, d1).total_degree())
    print("Q:", q)
    check_v = sp.factor(sp.cancel(v.subs(d4, d4_value)))
    print("V/Q:", sp.factor(check_v/q))

    labels = ("t_012", "t_013", "cofactor_5_0", "t_023", "t_123",
              "cofactor_0_0", "cofactor_0_3")
    reduced = {label: sp.cancel(rows[label].subs(ratio).subs(p3_p4))
               for label in labels}
    a0_value = sp.solve(reduced["cofactor_5_0"], a0, dict=True,
                        simplify=False)[0][a0]
    current = {label: sp.cancel(value.subs(a0, a0_value)
                                .subs(d4, d4_value))
               for label, value in reduced.items()
               if label != "cofactor_5_0"}
    solved = {}
    solve_data = []
    for label, variable in (("t_012", p1), ("t_013", p2),
                            ("t_023", a5)):
        row = sp.cancel(current[label].subs(solved))
        coefficient = sp.cancel(sp.diff(row, variable))
        coefficient_top = coefficient.as_numer_denom()[0]
        value = sp.solve(row, variable, dict=True,
                         simplify=False)[0][variable]
        solved[variable] = sp.cancel(value.subs(solved))
        solve_data.append((label, variable, coefficient_top))
        print("solve", label, variable, "coefficient terms",
              len(sp.Poly(coefficient_top, b0, b1, x, d1).terms()),
              "degree", sp.Poly(coefficient_top, b0, b1, x, d1)
              .total_degree())
    for label in ("t_123", "cofactor_0_0", "cofactor_0_3"):
        top = sp.cancel(current[label].subs(solved)).as_numer_denom()[0]
        polynomial = sp.Poly(top, b0, b1, x, d1)
        print("final", label, "terms", len(polynomial.terms()),
              "total", polynomial.total_degree(),
              "b1-degree", polynomial.degree(b1))
        print("factor sizes", [(len(sp.Poly(factor, b0, b1, x, d1).terms()),
                                exponent,
                                sp.Poly(factor, b0, b1, x, d1).degree(b1))
                               for factor, exponent in sp.factor_list(top)[1]])


if __name__ == "__main__":
    main()
