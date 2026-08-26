#!/usr/bin/env python3
"""Exact number-field closure of the residual C9 degree-34 factor.

The C9 branch has two bivariate eliminants after eliminating b0.  Their last
univariate factor q34 determines a unique d4 in Q[a]/(q34), and the original
F/G/C9 core then determines a unique b0.  This audit checks that point against
the full source interface: every open-chart factor is nonzero, but all five
previously unused lower cofactors are nonzero as well.  Hence the eliminant
point does not solve the literal source system.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
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
OUT = HERE / "results_branch0_cycle_b0_lnonzero_c9_degree34.json"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_c9_d34_audit", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(SOURCE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial_digest(value):
    return sha256(str(sp.expand(value)).encode("ascii")).hexdigest()


def rational_digest(value):
    value = sp.Rational(value)
    return sha256(f"{value.p}/{value.q}".encode("ascii")).hexdigest()


def main():
    variables, f, g, c9, named, unused, live = P.derive()
    b0, d1, d4 = variables
    q34 = named["deg34"]
    qpoly = sp.Poly(q34, d1, domain=QQ)
    require(qpoly.degree() == 34 and len(qpoly.terms()) == 35,
            "q34 size changed")

    rf = sp.resultant(f, c9, b0)
    rg = sp.resultant(g, c9, b0)
    bigf = max((factor for factor, _ in sp.factor_list(rf)[1]),
               key=lambda value: len(sp.Poly(value, d1, d4).terms()))
    bigg = max((factor for factor, _ in sp.factor_list(rg)[1]),
               key=lambda value: len(sp.Poly(value, d1, d4).terms()))
    require([len(sp.Poly(value, d1, d4).terms())
             for value in (bigf, bigg)] == [80, 80],
            "C9 bivariate eliminant sizes changed")

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
    require(d4_gcd.degree() == 1,
            "q34 common d4 ceased to be unique")
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
    require(b0_gcd.degree() == 1,
            "q34 common b0 ceased to be unique")
    b0_value = -b0_gcd.rep.TC()

    def evaluate(value):
        answer = field.zero
        for term in sp.Poly(value, b0).all_coeffs():
            answer = answer*b0_value + evaluate_d4(term)
        return answer

    require(all(evaluate(value) == field.zero
                for value in (f, g, c9, bigf, bigg)),
            "q34 point ceased to solve the elimination core")
    live_values = [(name, evaluate(value)) for name, value in live]
    require(all(value != field.zero for name, value in live_values),
            "q34 point left the declared open chart")
    lower_values = [(name, evaluate(value)) for name, value in unused]
    require(len(lower_values) == 5
            and all(value != field.zero for name, value in lower_values),
            "a q34 lower cofactor unexpectedly vanished")

    def element_polynomial(value):
        terms = value.to_list()
        return sum(sp.Rational(term)*d1**(len(terms)-index-1)
                   for index, term in enumerate(terms))

    lower_norms = {}
    for name, value in lower_values:
        norm = sp.factor(sp.resultant(q34, element_polynomial(value), d1))
        require(norm != 0, f"{name} norm unexpectedly vanished")
        lower_norms[name] = {
            "sha256": rational_digest(norm),
            "numerator_digits": len(str(abs(sp.numer(norm)))),
            "denominator_digits": len(str(sp.denom(norm))),
        }

    # Must-fire: the point really exists before the omitted literal rows, so
    # the closure is not a vacuous failure of the algebraic-number interface.
    require(d4_gcd.degree() == b0_gcd.degree() == 1
            and len(live_values) > 0 and len(lower_norms) == 5,
            "q34 lifted-point must-fire failed")

    result = {
        "status": "UNAUDITED exact closure of the C9 degree-34 factor",
        "assumptions": [
            "B0=0", "Kplus!=0", "L!=0", "Delta!=0", "D0!=0",
            "all selected-term factors and H are live",
            "all five unused lower cofactors are literal source equations"],
        "core_sha256": {
            name: polynomial_digest(value) for name, value in
            (("F", f), ("G", g), ("C9", c9),
             ("R80_F", bigf), ("R80_G", bigg), ("q34", q34))},
        "q34_terms": len(qpoly.terms()),
        "d4_gcd_degree": d4_gcd.degree(),
        "b0_gcd_degree": b0_gcd.degree(),
        "core_zero_count": 5,
        "live_factor_count": len(live_values),
        "live_zero_count": 0,
        "lower_cofactor_nonzero_count": len(lower_values),
        "lower_cofactor_norms": lower_norms,
        "scope": (
            "Exact algebraic-number gcds show that the sole q34 eliminant "
            "point lies on the open chart but violates every omitted lower "
            "cofactor. Together with the separate low-factor audit, this "
            "closes C9; it makes no claim about other cycle branches."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("branch-0 cycle C9 degree-34 closure: PASS")
    print("gcd degrees:", d4_gcd.degree(), b0_gcd.degree())
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
