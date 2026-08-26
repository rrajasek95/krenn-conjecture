#!/usr/bin/env python3
"""Export a fraction-free literal Cof(1,3) condition on the finite residual.

The six retained rows are affine in ``p1,p2,a5``.  Using rows 0,1,2, let D
be their coefficient determinant and N_i the three Cramer numerators.  The
literal omitted row Cof(1,3) is quadratic, with only the mixed term p1*p2.
Multiplying its numerator by D^2 and replacing D*p_i by N_i gives a
parameter polynomial E that vanishes for every full packet solution even
when D=0.  Thus no pivot localization is used.  We remove only explicitly
chart-live monomials/Bplus, substitute the Au-open U solve for d4, and reduce
modulo Q.  The retained polynomial is appended before the unchanged F4SAT
live factor at two primes; a coefficient-first characteristic-zero
Rabinowitsch input is exported in parallel.
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


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"
BASE_P1 = HERE / "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve"
P1 = 1073741827
P2 = 1073741789
OUT_P1 = HERE / "branch0_cycle_delta_au_open_cofactor13_p1073741827.msolve"
OUT_P2 = HERE / "branch0_cycle_delta_au_open_cofactor13_p1073741789.msolve"
OUT_Q = HERE / "branch0_cycle_delta_au_open_cofactor13_char0.msolve"
RESULT = HERE / "results_branch0_cycle_delta_au_open_cofactor13_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("n8_cycle_delta_cofactor13_export_audit", AUDIT_PATH)
INTERFACE = AUDIT.INTERFACE
SOURCE = AUDIT.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def digest(poly):
    return sha256(encode(poly).encode("ascii")).hexdigest()


def parse_base():
    lines = BASE_P1.read_text().splitlines()
    require(lines[:2] == ["b0,b1,d1,x", str(P1)],
            "the canonical prime-one header changed")
    body = "\n".join(lines[2:]).strip()
    rows = tuple(value.strip() for value in body.split(",") if value.strip())
    require(len(rows) == 17, "the all-minor base lost a row")
    return rows


def canonical_rabinowitsch(live):
    b0, b1, d1, x, z = sp.symbols("b0 b1 d1 x z")
    expression = sp.sympify(live.replace("^", "**"), locals={
        "b0": b0, "b1": b1, "d1": d1, "x": x})
    value = sp.expand(z*expression-1)
    encoded = encode(value)
    require(sp.expand(sp.diff(value, z)-expression) == 0
            and sp.expand(value.subs(z, 0)+1) == 0,
            "the coefficient-first Rabinowitsch row failed replay")
    return encoded


def derive(rows):
    derived = AUDIT.derive(rows)
    interface = INTERFACE.derive(rows)
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    unknowns = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    matrix = sp.Matrix([interface[6][row][:3] for row in (0, 1, 2)])
    rhs = sp.Matrix([-interface[6][row][3] for row in (0, 1, 2)])
    determinant = sp.expand(matrix.det(method="domain-ge"))
    numerators = []
    for column in range(3):
        replaced = matrix.copy()
        replaced[:, column] = rhs
        numerators.append(sp.expand(replaced.det(method="domain-ge")))

    ratio = {b3: x*b1, d3: -x*d1*d4}
    omitted = sp.cancel(rows["cofactor_1_3"].subs(ratio)
                        .subs(interface[3]).subs(SOURCE.A0, interface[4]))
    omitted_numerator, omitted_denominator = omitted.as_numer_denom()
    omitted_poly = sp.Poly(omitted_numerator, *unknowns)
    expected_monomials = {
        (1, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)}
    require({monomial for monomial, _ in omitted_poly.terms()}
            == expected_monomials,
            "literal Cof(1,3) changed its quadratic-affine shape")
    coefficient = {monomial: omitted_poly.coeff_monomial(monomial)
                   for monomial in expected_monomials}
    n1, n2, n3 = numerators
    e_full = sp.expand(
        coefficient[(1, 1, 0)]*n1*n2
        + determinant*(coefficient[(1, 0, 0)]*n1
                       + coefficient[(0, 1, 0)]*n2
                       + coefficient[(0, 0, 1)]*n3)
        + coefficient[(0, 0, 0)]*determinant**2)
    # Direct fraction-free identity, before any allowed live division.
    formal = sp.expand(sum(
        term_coefficient*n1**monomial[0]*n2**monomial[1]
        * n3**monomial[2]*determinant**(2-sum(monomial))
        for monomial, term_coefficient in omitted_poly.terms()))
    require(sp.expand(e_full-formal) == 0,
            "the fraction-free Cramer substitution failed")

    declared_live = -8*b1**6*d1**7*d4**5*x**6*(b1+d1)**3
    quotient, remainder = sp.div(
        sp.Poly(e_full, b0, b1, d1, x, d4),
        sp.Poly(declared_live, b0, b1, d1, x, d4))
    require(remainder.is_zero, "declared live factor ceased to divide E")
    pre_u = quotient.as_expr()

    # Homogenized polynomial substitution avoids SymPy's catastrophic
    # expansion of a nested rational expression.  If pre_u has d4-degree m,
    # multiply by Au^m and substitute the U-solve numerator term by term.
    d4_numerator, d4_denominator = sp.cancel(
        derived["d4_value"]).as_numer_denom()
    pre_poly = sp.Poly(pre_u, d4)
    d4_degree = pre_poly.degree()
    sub_num = sp.expand(sum(
        coefficient*d4_numerator**power
        * d4_denominator**(d4_degree-power)
        for (power,), coefficient in pre_poly.terms()))
    sub_den = d4_denominator**d4_degree
    reduced = sp.rem(sp.Poly(sub_num, b0, domain="QQ(b1,d1,x)"),
                     sp.Poly(derived["q"], b0,
                             domain="QQ(b1,d1,x)")).as_expr()
    reduced = sp.cancel(reduced).as_numer_denom()[0]
    polynomial = sp.Poly(reduced, b0, b1, d1, x)
    content = tuple(min(monomial[index] for monomial, _ in polynomial.terms())
                    for index in range(4))
    monomial = b0**content[0]*b1**content[1]*d1**content[2]*x**content[3]
    reduced_core = polynomial.exquo(
        sp.Poly(monomial, b0, b1, d1, x)).as_expr()
    return {
        "q": derived["q"], "determinant": determinant,
        "numerators": numerators,
        "omitted_denominator": omitted_denominator,
        "e_full": e_full, "declared_live": declared_live,
        "pre_u": pre_u, "u_denominator": sub_den,
        "reduced": reduced_core, "removed_monomial": content,
    }


def write_prime(path, prime, equations, live):
    path.write_text("b0,b1,d1,x\n" + str(prime) + "\n"
                    + ",\n".join((*equations, live)) + "\n")


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    value = derive(rows)
    base = parse_base()
    equations = (*base[:-1], encode(value["reduced"]))
    live = base[-1]
    write_prime(OUT_P1, P1, equations, live)
    write_prime(OUT_P2, P2, equations, live)
    OUT_Q.write_text("b0,b1,d1,x,z\n0\n"
                     + ",\n".join((*equations,
                                     canonical_rabinowitsch(live))) + "\n")

    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    result = {
        "status": "UNAUDITED exact fraction-free Cof(1,3) export",
        "source_row": "cofactor_1_3",
        "cramer_rows": [0, 1, 2],
        "cramer_row_labels": ["t_012", "t_013", "t_023"],
        "cramer_determinant_terms": len(sp.Poly(
            value["determinant"], b0, b1, d1, x, d4).terms()),
        "cramer_numerator_terms": [len(sp.Poly(
            numerator, b0, b1, d1, x, d4).terms())
            for numerator in value["numerators"]],
        "literal_cofactor_denominator": str(sp.factor(
            value["omitted_denominator"])),
        "removed_declared_live_factor": str(value["declared_live"]),
        "u_solve_denominator": str(sp.factor(value["u_denominator"])),
        "post_u_removed_monomial_exponents": list(value["removed_monomial"]),
        "reduced_terms": len(sp.Poly(
            value["reduced"], b0, b1, d1, x).terms()),
        "reduced_total_degree": sp.Poly(
            value["reduced"], b0, b1, d1, x).total_degree(),
        "reduced_sha256": digest(value["reduced"]),
        "inputs": [
            {"prime": P1, "file": OUT_P1.name,
             "sha256": sha256(OUT_P1.read_bytes()).hexdigest()},
            {"prime": P2, "file": OUT_P2.name,
             "sha256": sha256(OUT_P2.read_bytes()).hexdigest()},
            {"prime": 0, "file": OUT_Q.name,
             "sha256": sha256(OUT_Q.read_bytes()).hexdigest()}],
        "scope": (
            "Every full source solution in the declared Delta=0, Bplus-, "
            "Au-, d4-open chart kills the exported reduced polynomial. "
            "The Cramer pivot determinant is never divided out: its factors "
            "remain in the polynomial, so the pivot-zero boundary is retained. "
            "The prime inputs are modular unit discovery only; an exact-Q "
            "unit still needs engine output and literal replay."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Cof(1,3) fraction-free export: PASS")
    print("reduced terms/degree:", result["reduced_terms"],
          result["reduced_total_degree"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
