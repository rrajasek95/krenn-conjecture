#!/usr/bin/env python3
"""Exact number-field closure of the degree-24/153 C35 factors.

The distinct C35 resultant branch reduces to two bivariate eliminants R140
and R136.  After localized/low-degree factors are removed, their resultant
has irreducible factors q24 and q153.  This audit works in the exact fields
Q[a]/(q):

* q24 gives a unique common d4 and then a unique common b0 for F,G,C35,
  but every unused lower cofactor is nonzero at that point;
* q153 gives a unique common d4 for R140,R136, but F,G,C35 have gcd one in
  b0, so the eliminant point does not lift to the original core.

Together with the shared-S13 H-death and the low-factor audit, this closes
the entire C35 half of the B0=0,L!=0 cycle tree.
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
PROBE = HERE / "probe_branch0_cycle_b0_lnonzero_c35.py"
OUT = HERE / "results_branch0_cycle_b0_lnonzero_c35_high_factors.json"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_c35_high", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(PROBE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial_digest(value):
    return sha256(str(sp.expand(value)).encode("ascii")).hexdigest()


def rational_digest(value):
    value = sp.Rational(value)
    return sha256(f"{value.p}/{value.q}".encode("ascii")).hexdigest()


def main():
    variables, f, g, c35, _, rf, rg, unused, live = P.derive()
    b0, d1, d4 = variables
    resultant = sp.resultant(rf, rg, d4)
    factor_list = sp.factor_list(resultant)[1]
    q24 = next(value for value, exponent in factor_list
               if sp.degree(value, d1) == 24)
    q153 = next(value for value, exponent in factor_list
                if sp.degree(value, d1) == 153)
    require(all(exponent == 1 for value, exponent in factor_list
                if sp.degree(value, d1) in (24, 153)),
            "high-factor multiplicities changed")

    records = {}
    for degree, q in ((24, q24), (153, q153)):
        qpoly = sp.Poly(q, d1, domain=QQ)
        field = QQ.alg_field_from_poly(qpoly, "a")

        def coefficient(value):
            remainder = sp.Poly(value, d1, domain=QQ).rem(qpoly)
            return field(remainder.all_coeffs())

        def polynomial_d4(value):
            return sp.Poly.from_list(
                [coefficient(term)
                 for term in sp.Poly(value, d4).all_coeffs()],
                gens=d4, domain=field)

        d4_gcd = sp.gcd(polynomial_d4(rf), polynomial_d4(rg)).monic()
        require(d4_gcd.degree() == 1,
                f"q{degree} d4 gcd ceased to be linear")
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
                        polynomial_b0(c35)).monic()
        record = {
            "factor_sha256": polynomial_digest(q),
            "factor_terms": len(qpoly.terms()),
            "d4_gcd_degree": d4_gcd.degree(),
            "b0_gcd_degree": b0_gcd.degree(),
        }
        if degree == 153:
            require(b0_gcd.degree() == 0,
                    "q153 unexpectedly lifted to the original core")
            records[str(degree)] = record
            continue

        require(b0_gcd.degree() == 1,
                "q24 common b0 ceased to be unique")
        b0_value = -b0_gcd.rep.TC()

        def evaluate(value):
            answer = field.zero
            for term in sp.Poly(value, b0).all_coeffs():
                answer = answer*b0_value + evaluate_d4(term)
            return answer

        require(all(evaluate(value) == field.zero
                    for value in (f, g, c35, rf, rg)),
                "q24 point ceased to solve the resultant core")
        live_zero = [name for name, value in live
                     if evaluate(value) == field.zero]
        require(not live_zero, "q24 point left the declared open chart")
        lower_values = [(name, evaluate(value)) for name, value in unused]
        require(all(value != field.zero for name, value in lower_values),
                "a q24 lower cofactor unexpectedly vanished")

        def element_polynomial(value):
            terms = value.to_list()
            return sum(sp.Rational(term)*d1**(len(terms)-index-1)
                       for index, term in enumerate(terms))

        norms = {}
        for name, value in lower_values:
            norm = sp.factor(sp.resultant(
                q, element_polynomial(value), d1))
            require(norm != 0, f"{name} norm unexpectedly vanished")
            norms[name] = {
                "sha256": rational_digest(norm),
                "numerator_digits": len(str(abs(sp.numer(norm)))),
                "denominator_digits": len(str(sp.denom(norm))),
            }
        record.update({
            "core_zero_count": 5,
            "live_factor_count": len(live),
            "live_zero_count": 0,
            "lower_cofactor_nonzero_count": len(lower_values),
            "lower_cofactor_norms": norms,
        })
        records[str(degree)] = record

    # Must-fire guards: q24 really is a lifted point until a lower cofactor
    # is imposed, whereas q153 really fails before any lower row is needed.
    require(records["24"]["b0_gcd_degree"] == 1
            and records["24"]["lower_cofactor_nonzero_count"] == 5,
            "q24 lift/lower-row must-fire failed")
    require(records["153"]["d4_gcd_degree"] == 1
            and records["153"]["b0_gcd_degree"] == 0,
            "q153 spurious-eliminant must-fire failed")

    result = {
        "status": "UNAUDITED exact closure of distinct-C35 high factors",
        "assumptions": [
            "B0=0", "Kplus!=0", "L!=0", "Delta!=0", "D0!=0",
            "all selected-term factors and H are live",
            "all five unused lower cofactors are source equations"],
        "core_sha256": {
            name: polynomial_digest(value) for name, value in
            (("F", f), ("G", g), ("C35", c35),
             ("R140", rf), ("R136", rg))},
        "records": records,
        "scope": (
            "Exact algebraic-number gcds close q24 and q153. Combined with "
            "the separately audited shared-S13 and degree-2/2/4 branches, "
            "this closes C35 but says nothing about the C9 degree-34 factor."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("branch-0 cycle C35 high-factor closure: PASS")
    print("records:", {key: (value["d4_gcd_degree"],
                             value["b0_gcd_degree"])
                       for key, value in records.items()})
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
