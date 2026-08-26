#!/usr/bin/env python3
"""Exact number-field discovery on the residual C9 degree-34 factor.

This intentionally prints structure and does not claim a theorem.  It works
in Q[a]/(q34), computes the common d4 branch of the two bivariate eliminants,
then tests whether that branch lifts to a common b0 of the literal F/G/C9
core.  If it lifts, every open-chart factor, lower cofactor, and H is evaluated
exactly at the resulting algebraic point.
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


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "probe_branch0_cycle_b0_lnonzero_c9_factor.py"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_c9_d34", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(SOURCE)


def main():
    variables, f, g, c9, named, unused, live = P.derive()
    b0, d1, d4 = variables
    q34 = named["deg34"]
    rf = sp.resultant(f, c9, b0)
    rg = sp.resultant(g, c9, b0)
    bigf = max((factor for factor, _ in sp.factor_list(rf)[1]),
               key=lambda value: len(sp.Poly(value, d1, d4).terms()))
    bigg = max((factor for factor, _ in sp.factor_list(rg)[1]),
               key=lambda value: len(sp.Poly(value, d1, d4).terms()))

    qpoly = sp.Poly(q34, d1, domain=QQ)
    field = QQ.alg_field_from_poly(qpoly, "a")

    def coefficient(value):
        remainder = sp.Poly(value, d1, domain=QQ).rem(qpoly)
        return field(remainder.all_coeffs())

    def polynomial_d4(value):
        return sp.Poly.from_list(
            [coefficient(term)
             for term in sp.Poly(value, d4).all_coeffs()],
            gens=d4, domain=field)

    d4_gcd = sp.gcd(polynomial_d4(bigf), polynomial_d4(bigg)).monic()
    print("q34 terms / d4 gcd degree:", len(qpoly.terms()), d4_gcd.degree())
    if d4_gcd.degree() != 1:
        print("d4 gcd terms:", len(d4_gcd.terms()))
        return
    d4_value = -d4_gcd.rep.TC()

    def evaluate_d4(value):
        answer = field.zero
        for term in sp.Poly(value, d4).all_coeffs():
            answer = answer*d4_value + coefficient(term)
        return answer

    def polynomial_b0(value):
        return sp.Poly.from_list(
            [evaluate_d4(term)
             for term in sp.Poly(value, b0).all_coeffs()],
            gens=b0, domain=field)

    b0_gcd = sp.gcd(sp.gcd(polynomial_b0(f), polynomial_b0(g)),
                    polynomial_b0(c9)).monic()
    print("b0 gcd degree / terms:", b0_gcd.degree(), len(b0_gcd.terms()))
    if b0_gcd.degree() != 1:
        return
    b0_value = -b0_gcd.rep.TC()

    def evaluate(value):
        answer = field.zero
        for term in sp.Poly(value, b0).all_coeffs():
            answer = answer*b0_value + evaluate_d4(term)
        return answer

    print("core zeros:", [evaluate(value) == field.zero
                           for value in (f, g, c9, bigf, bigg)])
    print("live zeros:", [name for name, value in live
                           if evaluate(value) == field.zero])
    print("lower zeros:", [name for name, value in unused
                            if evaluate(value) == field.zero])


if __name__ == "__main__":
    main()
