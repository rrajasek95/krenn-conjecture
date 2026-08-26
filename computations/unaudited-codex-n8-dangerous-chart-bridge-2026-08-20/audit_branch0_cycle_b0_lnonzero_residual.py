#!/usr/bin/env python3
"""Exact sparse residual for the last B0=0, Delta!=0 cycle branch.

This is a reduction theorem, not a unit certificate.  It treats
Kplus!=0 and L!=0 after the two complementary audits closed Kplus=0 and
L=0.  Literal source rows reduce to F160=G84=0 and C9*C35=0 in three
parameters.  Exact resultants isolate the remaining finite elimination
tree without claiming that the tree is empty.
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
from sympy.polys.fields import field


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_b0_lnonzero_residual.json"
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "discover_branch0_k4_cycle_cramer_generic.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_cycle_b0_lnonzero_source", GENERIC)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(poly):
    return sha256(str(sp.expand(poly)).encode("ascii")).hexdigest()


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS

    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]
    base = {b1: -d1, d3: d4*(d1 + 1)/(d1 - 1)}
    base.update(sp.solve(sp.cancel(rows["cofactor_5_0"]
                                   .subs(p_solution).subs(base)),
                         a0, dict=True, simplify=False)[0])
    t5 = (2*a5*d1**2*d4 - 2*b0*d1**2 + 2*b0*d1
          + d1**2*d4 + d4)
    base.update(sp.solve(t5, a5, dict=True, simplify=False)[0])

    top_00 = sp.cancel(rows["cofactor_0_0"].subs(p_solution)
                       .subs(base)).as_numer_denom()[0]
    core_00 = max((factor for factor, exponent in
                   sp.factor_list(top_00)[1]),
                  key=lambda value: len(sp.Poly(value, b3).terms()))
    b3_solution = sp.solve(core_00, b3, dict=True, simplify=False)[0][b3]
    l_factor = (2*b0*d1**2 - 2*b0*d1
                - d4*(d1**3 + 3*d1**2 - d1 + 1))
    m_factor = (2*b0*d1**4 - 2*b0*d1**2 - d1**4*d4 - 2*d1**4
                - 2*d1**3*d4 - 2*d1**3 - 4*d1**2*d4 + 6*d1**2
                - 2*d1*d4 - 2*d1 + d4)
    expected_b3 = d1*m_factor/((d1 - 1)*l_factor)
    require(sp.cancel(b3_solution - expected_b3) == 0,
            "the L!=0 b3 solve changed")

    parameters = dict(base)
    parameters[b3] = b3_solution
    rational_field, _, _, _ = field("b0,d1,d4", QQ)
    values = [rational_field.from_expr(sp.cancel(
        p_solution[variable].subs(parameters))) for variable in SOURCE.P]
    values += [rational_field.from_expr(sp.cancel(
        base[a0].subs(parameters))),
               rational_field.from_expr(sp.cancel(
        base[a5].subs(parameters)))]
    values += [rational_field.from_expr(sp.cancel(
        parameters.get(variable, variable)))
        for variable in SOURCE.PARAMETERS]

    def evaluate(poly):
        answer = rational_field.zero
        for exponent, coefficient in poly.items():
            term = rational_field.from_expr(
                sp.Rational(coefficient.numerator, coefficient.denominator))
            for value, power in zip(values, exponent):
                term *= value**power
            answer += term
        return answer.numer.as_expr()

    factored_012 = sp.factor_list(evaluate(raw["t_012"]))[1]
    factored_013 = sp.factor_list(evaluate(raw["t_013"]))[1]
    factored_03 = sp.factor_list(evaluate(raw["cofactor_0_3"]))[1]
    f160 = max((factor for factor, exponent in factored_012),
               key=lambda value: len(sp.Poly(value, b0, d1, d4).terms()))
    g84 = max((factor for factor, exponent in factored_013),
              key=lambda value: len(sp.Poly(value, b0, d1, d4).terms()))
    c_factors = sorted((factor for factor, exponent in factored_03
                        if len(sp.Poly(factor, b0, d1, d4).terms()) > 2),
                       key=lambda value:
                       len(sp.Poly(value, b0, d1, d4).terms()))
    require([len(sp.Poly(value, b0, d1, d4).terms())
             for value in (f160, g84, *c_factors)] == [160, 84, 9, 35],
            "the L!=0 sparse core sizes changed")
    c9, c35 = c_factors
    require(any(sp.expand(factor - m_factor) == 0
                or sp.expand(factor + m_factor) == 0
                for factor, exponent in factored_012),
            "the live M factor disappeared from t012")

    qshared = d4*(d1 + 1)**2 - 2*d1

    # The linear C9 branch.
    rf9 = sp.resultant(f160, c9, b0)
    rg9 = sp.resultant(g84, c9, b0)
    gcd9 = sp.factor(sp.gcd(sp.Poly(rf9, d1, d4),
                           sp.Poly(rg9, d1, d4)).as_expr())
    expected_gcd9 = 4*d1**2*(d1 - 1)**4*qshared
    require(sp.expand(gcd9 - expected_gcd9) == 0,
            "the C9 resultant gcd changed")
    require(sp.factor(sp.cancel(c9.subs(
        d4, 2*d1/(d1 + 1)**2)/
        l_factor.subs(d4, 2*d1/(d1 + 1)**2))) == d1**2 + 1,
            "C9+Qshared ceased to force L=0")
    big9f = max((factor for factor, exponent in sp.factor_list(rf9)[1]),
                key=lambda value: len(sp.Poly(value, d1, d4).terms()))
    big9g = max((factor for factor, exponent in sp.factor_list(rg9)[1]),
                key=lambda value: len(sp.Poly(value, d1, d4).terms()))
    require(len(sp.Poly(big9f, d1, d4).terms()) == 80
            and len(sp.Poly(big9g, d1, d4).terms()) == 80,
            "the C9 big eliminants changed")
    univariate9 = sp.factor(sp.resultant(big9f, big9g, d4))
    qplus = d1**2 + 2*d1 - 1
    qa = d1**3 + d1**2 + 3*d1 - 1
    qlive = d1**3 + 3*d1**2 - d1 + 1
    qfour = d1**4 + 6*d1**2 + 1
    factors9 = sp.factor_list(univariate9)[1]
    require([(sp.degree(factor, d1), exponent)
             for factor, exponent in factors9] ==
            [(1, 9), (1, 9), (1, 36), (2, 1), (2, 18),
             (3, 1), (3, 1), (4, 4), (34, 1)],
            "the C9 univariate factor degree pattern changed")
    require(all(any(sp.expand(factor - expected) == 0
                    or sp.expand(factor + expected) == 0
                    for factor, exponent in factors9)
                for expected in (qplus, qa, qlive, qfour)),
            "a named C9 univariate factor changed")
    degree34 = next(factor for factor, exponent in factors9
                    if sp.degree(factor, d1) == 34)

    # The cubic C35 branch.
    rf35 = sp.resultant(f160, c35, b0)
    rg35 = sp.resultant(g84, c35, b0)
    gcd35 = sp.factor(sp.gcd(sp.Poly(rf35, d1, d4),
                            sp.Poly(rg35, d1, d4)).as_expr())
    shared35 = next(factor for factor, exponent in
                    sp.factor_list(gcd35)[1]
                    if len(sp.Poly(factor, d1, d4).terms()) == 13)
    require(sp.Poly(shared35, d1, d4).total_degree() == 8,
            "the C35 shared factor changed")
    factor_sizes_f35 = sorted(len(sp.Poly(factor, d1, d4).terms())
                              for factor, exponent in
                              sp.factor_list(rf35)[1]
                              if len(sp.Poly(factor, d1, d4).terms()) > 13)
    factor_sizes_g35 = sorted(len(sp.Poly(factor, d1, d4).terms())
                              for factor, exponent in
                              sp.factor_list(rg35)[1]
                              if len(sp.Poly(factor, d1, d4).terms()) > 13)
    require(factor_sizes_f35 == [140] and factor_sizes_g35 == [136],
            "the C35 distinct residual sizes changed")

    # Hostile literal source mutation destroys the C9*C35 split.
    mutated = dict(raw["cofactor_0_3"])
    key = sorted(mutated)[0]
    mutated[key] = -mutated[key]
    mutated_top = evaluate(mutated)
    require(sp.rem(sp.Poly(mutated_top, b0, d1, d4),
                   sp.Poly(c9*c35, b0, d1, d4)) != 0,
            "the Cof(0,3) hostile mutation did not fire")

    result = {
        "status": "UNAUDITED exact sharp residual for B0=0,L!=0",
        "assumptions": [
            "Delta != 0", "D0 != 0", "B0=0", "Kplus != 0",
            "L != 0", "all Laurent and selected-term factors live"],
        "core_term_counts": [160, 84, 9, 35],
        "core_sha256": {
            "F160": digest(f160), "G84": digest(g84),
            "C9": digest(c9), "C35": digest(c35)},
        "c9_shared_factor": str(qshared),
        "c9_shared_factor_scope": "C9+Qshared forces L=0",
        "c9_univariate_nonlocal_degrees": [2, 3, 4, 34],
        "c9_degree34_sha256": digest(degree34),
        "c35_shared_factor": str(shared35),
        "c35_distinct_residual_term_counts": [140, 136],
        "scope": (
            "This is not an emptiness theorem.  It is the exact remaining "
            "resultant tree for the final B0=0 subbranch."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 cycle B0=0,L!=0 sharp residual: PASS")
    print("core terms:", result["core_term_counts"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
