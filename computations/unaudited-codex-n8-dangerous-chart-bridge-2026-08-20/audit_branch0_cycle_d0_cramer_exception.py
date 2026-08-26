#!/usr/bin/env python3
"""Exact closure of the C0=0 exception inside the D0=0 cycle branch.

Assume the upper Cramer determinant Delta is nonzero and set
``D0=d1*d4+d3=0``.  Cof(0,0) and Cof(5,0) are linear in b1,b3 with
determinant ``-2*b0*d1*C0``, where ``C0=b0^2+d4^2``.  This audit closes
the exceptional C0=0 branch over characteristic zero.  The generic C0!=0
branch is exported separately and remains to be decided.
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
OUT = HERE / "results_branch0_cycle_d0_cramer_exception.json"
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "discover_branch0_k4_cycle_cramer_generic.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_cycle_d0_exception_source", GENERIC)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS

    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]
    d0_substitution = {d3: -d1*d4}

    def residual_core(label):
        top = sp.cancel(rows[label].subs(p_solution)
                        .subs(d0_substitution)).as_numer_denom()[0]
        return max((factor for factor, exponent in sp.factor_list(top)[1]),
                   key=lambda value:
                   len(sp.Poly(value, b0, b1, b3, d1, d4).terms()))

    e0 = residual_core("cofactor_0_0")
    e5 = residual_core("cofactor_5_0")
    matrix, rhs = sp.linear_eq_to_matrix([e0, e5], [b1, b3])
    c0 = b0**2 + d4**2
    require(sp.factor(matrix.det()) == -2*b0*d1*c0,
            "the D0 branch b1,b3 determinant changed")

    augmented = matrix.row_join(rhs)
    consistency_1 = augmented[:, (0, 2)].det()
    consistency_2 = augmented[:, (1, 2)].det()
    reduced_1 = sp.factor(sp.rem(consistency_1, c0, b0))
    reduced_2 = sp.factor(sp.rem(consistency_2, c0, b0))
    expected_1 = -2*b0*d4*(d1**2 + 1)*(d4 - 1)
    expected_2 = -2*b0*d4**2*(d1**2 + 1)*(d4 - 1)
    require(sp.expand(reduced_1 - expected_1) == 0
            and sp.expand(reduced_2 - expected_2) == 0,
            "the C0=0 consistency split changed")

    # A small quotient-ring evaluator for a monic quadratic in one variable.
    def quadratic_reducer(variable, polynomial):
        qpoly = sp.Poly(polynomial, variable, domain="EX")

        def reduce(expression):
            top, bottom = sp.fraction(sp.together(expression))
            inverse = sp.invert(sp.Poly(bottom, variable, domain="EX"),
                                qpoly)
            return sp.rem(sp.Poly(top, variable, domain="EX")*inverse,
                          qpoly).as_expr()
        return reduce

    def evaluate(poly, values, reduce):
        def multiply(left, right):
            return reduce(left*right)

        def power(value, exponent):
            answer = sp.Integer(1)
            for _ in range(exponent):
                answer = multiply(answer, value)
            return answer

        answer = sp.Integer(0)
        for exponent, coefficient in poly.items():
            term = sp.Rational(coefficient.numerator,
                               coefficient.denominator)
            for value, degree in zip(values, exponent):
                term = multiply(term, power(value, degree))
            answer = reduce(answer + term)
        return sp.factor(answer)

    # First consistency branch: d4=1 and b0^2+1=0.
    reduce_b0 = quadratic_reducer(b0, b0**2 + 1)
    branch_one = {d3: -d1, d4: 1}
    e5_one = sp.cancel(e5.subs(branch_one))
    branch_one[b1] = sp.solve(e5_one, b1, dict=True,
                              simplify=False)[0][b1]
    values_one = [reduce_b0(p_solution[variable].subs(branch_one))
                  for variable in SOURCE.P]
    values_one += [a0, a5]
    values_one += [reduce_b0(branch_one.get(variable, variable))
                   for variable in SOURCE.PARAMETERS]
    t012_one = evaluate(raw["t_012"], values_one, reduce_b0)
    t013_one = evaluate(raw["t_013"], values_one, reduce_b0)
    core_012 = a0*b0 - a0 + 2*b0 + 2
    core_013 = a0*b0*d1 + a0*d1 + 2*b0*b3 - 2*b3
    require(sp.cancel(t012_one/core_012) != 0
            and sp.cancel(t013_one/core_013) != 0,
            "the d4=1 triangle cores changed")
    a0_resultant = reduce_b0(sp.resultant(core_012, core_013, a0))
    require(sp.expand(a0_resultant + 4*b0*(b3 + d1)) == 0,
            "the d4=1 a0 compatibility changed")

    # The live factors force b3=-d1.  Then b1=d1 and t023,t123 are
    # incompatible with exact resultant -8*d1^5.
    branch_one[b3] = -d1
    branch_one[b1] = d1
    values_one = [reduce_b0(p_solution[variable].subs(branch_one))
                  for variable in SOURCE.P]
    values_one += [a0, a5]
    values_one += [reduce_b0(branch_one.get(variable, variable))
                   for variable in SOURCE.PARAMETERS]
    t023_one = evaluate(raw["t_023"], values_one,
                        reduce_b0).as_numer_denom()[0]
    t123_one = evaluate(raw["t_123"], values_one,
                        reduce_b0).as_numer_denom()[0]
    final_one = sp.factor(sp.resultant(t023_one, t123_one, a5))
    require(final_one == -8*d1**5,
            "the d4=1 final a5 resultant changed")

    # Second consistency branch: d1^2+1=0.  Modulo this relation C0 splits
    # as (b0-d1*d4)(b0+d1*d4), giving two exact signs.
    reduce_d1 = quadratic_reducer(d1, d1**2 + 1)
    sign_results = []
    for sign in (1, -1):
        signed = {d3: -d1*d4, b0: sign*d1*d4}
        signed[b1] = sp.solve(e5.subs(signed), b1, dict=True,
                              simplify=False)[0][b1]
        signed_values = [reduce_d1(p_solution[variable].subs(signed))
                         for variable in SOURCE.P]
        signed_values += [a0, a5]
        signed_values += [reduce_d1(signed.get(variable, variable))
                          for variable in SOURCE.PARAMETERS]
        triangle_left = evaluate(raw["t_012"], signed_values, reduce_d1)
        triangle_right = evaluate(raw["t_013"], signed_values, reduce_d1)

        if sign == 1:
            left_core = (a0*d1*d4 - a0*d4 + d1*d4 + d1 + d4 + 1)
            right_core = a0*d4 + 2*b3*d4 - d4 + 1
            compatibility = b3*d1*d4 - b3*d4 - d1*d4 - 1
            b3_value = (d1*d4 + 1)/(d4*(d1 - 1))
            a0_value = -(2*b3*d4 - d4 + 1)/d4
        else:
            left_core = (a0*d1*d4 + a0*d4 + d1*d4 + d1 - d4 - 1)
            right_core = a0*d4 - 2*b3*d4 - d4 + 1
            compatibility = b3*d1*d4 + b3*d4 + d1*d4 - 1
            b3_value = (1 - d1*d4)/(d4*(d1 + 1))
            a0_value = (2*b3*d4 + d4 - 1)/d4
        require(sp.cancel(triangle_left/left_core) != 0
                and sp.cancel(triangle_right/right_core) != 0,
                "a signed d1^2+1 triangle core changed")
        compatibility_value = reduce_d1(
            sp.resultant(left_core, right_core, a0))
        expected = (2*d4*compatibility if sign == 1
                    else -2*d4*compatibility)
        require(sp.expand(compatibility_value - expected) == 0,
                "a signed a0 compatibility changed")

        signed[b3] = b3_value
        signed[a0] = a0_value.subs(b3, b3_value)
        signed[b1] = signed[b1].subs(b3, b3_value)
        signed_values = [reduce_d1(p_solution[variable].subs(signed))
                         for variable in SOURCE.P]
        signed_values += [reduce_d1(signed[a0]), a5]
        signed_values += [reduce_d1(signed.get(variable, variable))
                          for variable in SOURCE.PARAMETERS]
        equations = [evaluate(raw[label], signed_values, reduce_d1)
                     .as_numer_denom()[0]
                     for label in ("t_023", "t_123", "cofactor_0_3")]
        pair_values = [reduce_d1(sp.resultant(equations[left],
                                              equations[right], a5))
                       for left, right in ((0, 1), (0, 2), (1, 2))]
        # Away from the common denominator norm P, the three compatibility
        # factors have no solution: their exact ideal forces P itself.
        cores = []
        for index, value in enumerate(pair_values):
            factors = sp.factor_list(value)[1]
            cores.append(max((factor for factor, exponent in factors),
                             key=lambda factor:
                             len(sp.Poly(factor, d1, d4).terms())))
        gb_pairs = sp.groebner([d1**2 + 1, *cores], d1, d4,
                               order="lex")
        norm_delta = d4**4 + 6*d4**2 + 1
        signed_relation = (2*d1 + d4**3 + 5*d4 if sign == 1
                           else 2*d1 - d4**3 - 5*d4)
        require(any(sp.expand(poly.as_expr() - norm_delta) == 0
                    for poly in gb_pairs.polys)
                and any(sp.expand(poly.as_expr() - signed_relation) == 0
                        for poly in gb_pairs.polys),
                "the signed pair-compatibility ideal changed")

        # At norm_delta=0, redo the literal source substitution without the
        # now-invalid quadratic-field denominator.  This leaves one variable
        # h=d4 with d1 determined by the signed relation.
        h = sp.Symbol("h")
        quartic = h**4 + 6*h**2 + 1
        d_value = (-(h**3 + 5*h)/2 if sign == 1
                   else (h**3 + 5*h)/2)
        direct_b3 = (d_value*h + 1)/(h*(d_value - 1)) if sign == 1 \
            else (1 - d_value*h)/(h*(d_value + 1))
        direct_b1 = (-direct_b3*h + h - 1 if sign == 1
                     else -direct_b3*h - h + 1)
        direct_a0 = (-(2*direct_b3*h - h + 1)/h if sign == 1
                     else (2*direct_b3*h + h - 1)/h)
        direct = {
            d1: d_value, d4: h, d3: -d_value*h,
            b0: sign*d_value*h, b3: direct_b3, b1: direct_b1,
            a0: direct_a0,
        }
        reduce_h = quadratic_reducer(h, quartic)
        direct_values = [reduce_h(p_solution[variable].subs(direct))
                         for variable in SOURCE.P]
        direct_values += [reduce_h(direct_a0), a5]
        direct_values += [reduce_h(direct.get(variable, variable))
                          for variable in SOURCE.PARAMETERS]
        direct_023 = evaluate(raw["t_023"], direct_values,
                              reduce_h).as_numer_denom()[0]
        direct_123 = evaluate(raw["t_123"], direct_values,
                              reduce_h).as_numer_denom()[0]
        direct_pair = reduce_h(sp.resultant(direct_023, direct_123, a5))
        direct_norm = sp.resultant(quartic,
                                   direct_pair.as_numer_denom()[0], h)
        require(abs(direct_norm) == 42467328,
                "the signed norm-delta direct contradiction changed")
        sign_results.append(int(abs(direct_norm)))

    # Mutating a literal t123 coefficient destroys the d4=1 resultant.
    mutated = dict(raw["t_123"])
    key = sorted(mutated)[0]
    mutated[key] = -mutated[key]
    mutated_123 = evaluate(mutated, values_one,
                           reduce_b0).as_numer_denom()[0]
    require(sp.resultant(t023_one, mutated_123, a5) != final_one,
            "the t123 hostile mutation did not fire")

    result = {
        "status": "UNAUDITED exact closure of D0=0,C0=0",
        "assumptions": [
            "Delta != 0", "D0=d1*d4+d3=0", "C0=b0^2+d4^2=0",
            "all Laurent and selected-term factors live"],
        "b1_b3_determinant": "-2*b0*d1*(b0^2+d4^2)",
        "consistency_split": "(d1^2+1)*(d4-1)=0",
        "d4_one_final_resultant": str(final_one),
        "d1_square_minus_one_direct_norms": sign_results,
        "scope": (
            "This closes only the C0=0 exception in the D0=0 branch.  "
            "The C0!=0 D0 branch and Delta=0 remain open."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 cycle D0=0,C0=0: PASS")
    print("resultants / norms:", final_one, sign_results)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
