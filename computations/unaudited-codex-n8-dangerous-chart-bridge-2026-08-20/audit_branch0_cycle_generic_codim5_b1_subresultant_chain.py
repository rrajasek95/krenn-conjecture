#!/usr/bin/env python3
"""Exact unsaturated b1 subresultant chain for the three smallest core rows."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sys


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp
from flint import fmpz_mpoly_ctx


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_codim5_b1_subresultant_chain.json"
POLYS = HERE / "branch0_cycle_generic_codim5_b1_subresultant_polynomials.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def split_rows(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text().splitlines()
    body = "\n".join(lines[2:]).strip()
    return lines[0].split(","), body.split(",\n")


def fast_poly(encoded: str, variables) -> sp.Poly:
    """Parse the strict coefficient-first msolve syntax without sympify."""
    names = {str(variable): index for index, variable in enumerate(variables)}
    terms = {}
    for raw in re.findall(r"[+-]?[^+-]+", encoded.replace(" ", "")):
        sign = -1 if raw.startswith("-") else 1
        body = raw[1:] if raw[:1] in "+-" else raw
        coefficient = sign
        monomial = [0]*len(variables)
        for factor in body.split("*"):
            if re.fullmatch(r"\d+", factor):
                coefficient *= int(factor)
                continue
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", factor)
            require(match is not None and match.group(1) in names,
                    f"unsupported strict factor {factor!r}")
            monomial[names[match.group(1)]] += int(match.group(2) or 1)
        key = tuple(monomial)
        terms[key] = terms.get(key, 0)+coefficient
    return sp.Poly.from_dict(terms, variables, domain=sp.ZZ)


def primitive(poly: sp.Expr, variables) -> sp.Expr:
    return sp.Poly(sp.expand(poly), *variables, domain=sp.ZZ).primitive()[1].as_expr()


def encode(poly: sp.Expr, variables) -> str:
    value = sp.Poly(poly, *variables, domain=sp.ZZ).primitive()[1]
    pieces = []
    for monomial, coefficient in value.terms():
        coefficient = int(coefficient)
        factors = [] if abs(coefficient) == 1 else [str(abs(coefficient))]
        for variable, power in zip(variables, monomial, strict=True):
            if power:
                factors.append(str(variable) if power == 1
                               else f"{variable}^{power}")
        body = "*".join(factors) or "1"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def record(poly: sp.Expr, variables) -> dict:
    value = sp.Poly(poly, *variables, domain=sp.ZZ).primitive()[1]
    encoded = encode(value.as_expr(), variables)
    return {"terms": len(value.terms()),
            "degree": int(value.total_degree()),
            "sha256": sha256(encoded.encode("ascii")).hexdigest()}


def flint_encode(poly) -> str:
    pieces = []
    for monomial, coefficient in sorted(
            poly.to_dict().items(), reverse=True):
        coefficient = int(coefficient)
        factors = [] if abs(coefficient) == 1 else [str(abs(coefficient))]
        for name, power in zip(poly.context().names(), monomial, strict=True):
            if power:
                factors.append(name if power == 1 else f"{name}^{power}")
        body = "*".join(factors) or "1"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def flint_record(poly) -> dict:
    encoded = flint_encode(poly.primitive()[1])
    return {"terms": len(poly), "degree": int(poly.total_degree()),
            "sha256": sha256(encoded.encode("ascii")).hexdigest()}


def at_linear_root(poly: sp.Expr, variable: sp.Symbol,
                   leading: sp.Expr, constant: sp.Expr) -> sp.Expr:
    source = sp.Poly(poly, variable)
    degree = source.degree()
    return sp.expand(sum(
        coefficient*(-constant)**power*leading**(degree-power)
        for (power,), coefficient in source.terms()))


def main() -> None:
    names, encoded_rows = split_rows(SOURCE)
    require(names == ["b0", "b1", "d1", "d3", "d4", "z"]
            and len(encoded_rows) == 10,
            "corrected source header/row count changed")
    b0, b1, d1, d3, d4, z = sp.symbols(" ".join(names))
    variables5 = (b0, b1, d1, d3, d4)
    parameters = (b0, d1, d3, d4)
    p851 = fast_poly(encoded_rows[0], variables5).as_expr()
    p1342 = fast_poly(encoded_rows[1], variables5).as_expr()
    p324 = fast_poly(encoded_rows[2], variables5).as_expr()
    require([record(poly, variables5)["terms"]
             for poly in (p851, p1342, p324)] == [851, 1342, 324],
            "retained row profiles changed")
    print("subresultant: three rows parsed", flush=True)

    q324 = sp.Poly(p324, b1)
    q851 = sp.Poly(p851, b1)
    q1342 = sp.Poly(p1342, b1)
    require((q324.degree(), q851.degree(), q1342.degree()) == (2, 2, 3),
            "b1 degree pattern changed")
    a2, a1, a0 = (q324.coeff_monomial(b1**2),
                   q324.coeff_monomial(b1), q324.coeff_monomial(1))
    c2, c1, c0 = (q851.coeff_monomial(b1**2),
                   q851.coeff_monomial(b1), q851.coeff_monomial(1))
    # This is the fraction-free degree-one member of the quadratic PRS.
    ell_leading = primitive(c2*a1-a2*c1, parameters)
    ell_constant = primitive(c2*a0-a2*c0, parameters)
    ell = sp.expand(ell_leading*b1+ell_constant)
    combination = sp.expand(c2*p324-a2*p851)
    combination_primitive = primitive(combination, variables5)
    require(sp.expand(combination_primitive-ell) == 0
            or sp.expand(combination_primitive+ell) == 0,
            "quadratic cancellation/linear PRS identity changed")
    print("subresultant: linear common-root relation built", flush=True)

    l6 = (b0**2*d1*d4 + 2*b0**2*d3 - b0*d1*d4
          + b0*d3*d4 + 2*d1*d4**2 + d3*d4)
    c4 = (-b0**2*d1**2*d4-b0*d1**2*d4-b0*d1*d3*d4+d1*d3*d4)
    d10_compare = primitive(
        sp.expand(c4*ell_leading-l6*ell_constant), parameters)
    require(d10_compare != 0,
            "linear common-root relation already forces D10 identically")
    print("subresultant: D10 comparison built", flush=True)

    # Do not substitute the cubic directly at -E0/E1: that creates E1^3.
    # First fraction-free pseudo-divide P1342 by P324 to degree one.
    u3, u2, u1, u0 = (q1342.coeff_monomial(b1**3),
                       q1342.coeff_monomial(b1**2),
                       q1342.coeff_monomial(b1), q1342.coeff_monomial(1))
    r2 = sp.expand(a2*u2-u3*a1)
    r1 = sp.expand(a2*u1-u3*a0)
    r0 = sp.expand(a2*u0)
    f_leading = primitive(sp.expand(a2*r1-r2*a1), parameters)
    f_constant = primitive(sp.expand(a2*r0-r2*a0), parameters)
    f_linear = sp.expand(f_leading*b1+f_constant)
    require(f_linear != 0, "P1342/P324 linear PRS vanished")
    print("subresultant: P1342/P324 linear PRS built", flush=True)
    ctx = fmpz_mpoly_ctx.get([str(v) for v in parameters], ordering="lex")
    def to_flint(poly):
        values = sp.Poly(poly, *parameters, domain=sp.ZZ).as_dict()
        return ctx.from_dict({monomial: int(coefficient)
                              for monomial, coefficient in values.items()})
    e1_flint, e0_flint = to_flint(ell_leading), to_flint(ell_constant)
    f1_flint, f0_flint = to_flint(f_leading), to_flint(f_constant)
    common_linear_determinant = (e1_flint*f0_flint-e0_flint*f1_flint).primitive()[1]
    require(not common_linear_determinant.is_zero(),
            "the two linear PRS relations became associates")
    print("subresultant: two-linear common-root determinant built", flush=True)
    j_flint = to_flint(d10_compare).primitive()[1]
    jk_gcd = j_flint.gcd(common_linear_determinant).primitive()[1]
    print("subresultant: gcd(J,K) built", flush=True)

    result = {
        "status": "UNAUDITED exact unsaturated b1 subresultant chain",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "row_profiles": {"P324": record(p324, variables5),
                         "P851": record(p851, variables5),
                         "P1342": record(p1342, variables5)},
        "b1_degrees": {"P324": 2, "P851": 2, "P1342": 3},
        "linear_PRS_identity": (
            "primitive(lc(P851)*P324-lc(P324)*P851)=E1*b1+E0"),
        "E1": record(ell_leading, parameters),
        "E0": record(ell_constant, parameters),
        "linear_root": "b1=-E0/E1 on E1-open",
        "D10_root_comparison_identity": (
            "E1*D10|b1=-E0/E1 = C4*E1-L6*E0 = J"),
        "J": record(d10_compare, parameters),
        "P324_leading_coefficient": record(a2, parameters),
        "P851_leading_coefficient": record(c2, parameters),
        "P1342_leading_coefficient": record(u3, parameters),
        "P1342_P324_linear_PRS": {
            "F1": record(f_leading, parameters),
            "F0": record(f_constant, parameters),
            "identity": (
                "F1*b1+F0 is the primitive degree-one fraction-free "
                "pseudo-remainder of P1342 by P324"),
        },
        "two_linear_root_determinant": {
            "K": flint_record(common_linear_determinant),
            "identity": "K=E1*F0-E0*F1",
        },
        "J_K_gcd": flint_record(jk_gcd),
        "generic_branch_target": (
            "Prove J radical/ideal-zero on the projection cut by the "
            "quadratic resultant and K, then replay the "
            "remaining six rows. E1=0 is the first exceptional divisor."),
        "scope": (
            "No D10 equation or localization is adjoined. These are exact "
            "fraction-free identities in the unsaturated P324/P851/P1342 "
            "rows. No containment claim is made until J is killed."),
    }
    polys = {"variables": [str(v) for v in parameters],
             "E1": encode(ell_leading, parameters),
             "E0": encode(ell_constant, parameters),
             "J": encode(d10_compare, parameters),
             "F1": encode(f_leading, parameters),
             "F0": encode(f_constant, parameters),
             "K": flint_encode(common_linear_determinant),
             "gcd_J_K": flint_encode(jk_gcd)}
    POLYS.write_text(json.dumps(polys, separators=(",", ":"))+"\n")
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["polynomial_payload"] = POLYS.name
    result["polynomial_payload_sha256"] = sha256(POLYS.read_bytes()).hexdigest()
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("unsaturated b1 subresultant chain: PASS")
    print("E1/E0/J:", result["E1"], result["E0"], result["J"])
    print("F1/F0/K:", result["P1342_P324_linear_PRS"]["F1"],
          result["P1342_P324_linear_PRS"]["F0"],
          result["two_linear_root_determinant"]["K"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
