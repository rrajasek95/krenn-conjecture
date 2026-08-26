#!/usr/bin/env python3
"""Exact closure of one B0=0 solve-denominator branch of the k4 cycle.

The generic Cramer reduction solves the four upper cofactor rows for
``p1,...,p4``.  This audit treats the exceptional solve denominator
``B0=b1+d1=0`` while retaining ``Delta != 0`` and ``D0 != 0``.  The row
``t023`` first forces a small relation.  On the subsequent ``Kplus=0``
factor of ``t123``, literal source rows reduce the problem to two quadratic
equations.  Their exact resultant has three non-local factors; two are
killed by a lower cofactor and the third makes a selected term ``1+p_i``
zero.  Thus this precisely delimited branch is empty over characteristic
zero.

Nothing here closes the complementary Kplus!=0 branch, Delta=0, or D0=0.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

# Keep the hostile ``python -I -S`` replay independent of ambient import
# variables while still using the interpreter's own pinned venv package.
_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_b0_denominator_kplus.json"
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "discover_branch0_k4_cycle_cramer_generic.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_cycle_b0_kplus_source", GENERIC)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def numerator(expression):
    return sp.expand(sp.cancel(expression).as_numer_denom()[0])


def primitive(expression, variables):
    return sp.primitive(sp.Poly(sp.expand(expression), *variables))[1].as_expr()


def main():
    row_data, hafnian_data = SOURCE.SOURCE.data()
    rows = {label: SOURCE.expression(poly) for label, poly, _ in row_data}
    hafnian = SOURCE.expression(hafnian_data)
    p1, p2, p3, p4 = SOURCE.P
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS

    upper_labels = tuple(f"cofactor_{edge}_0" for edge in range(1, 5))
    upper = [rows[label] for label in upper_labels]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]
    delta = b1 * d3 + b3 * d1 * d4

    # On B0=0, t023 has a completely factored compatibility numerator.
    t023_b0 = sp.factor(SOURCE.numerator(rows["t_023"], p_solution)
                       .subs(b1, -d1))
    e_relation = d1 * d3 - d1 * d4 - d3 - d4
    expected_t023 = 2 * b0**2 * d1**3 * (b3 * d4 - d3) * e_relation
    require(sp.expand(t023_b0 - expected_t023) == 0,
            "the B0=0 t023 factorization changed")

    # Delta!=0 and the Laurent factors force E=0.  In characteristic zero,
    # E=0 with d4!=0 also forces d1!=1, so solve for d3.
    base = {b1: -d1, d3: d4 * (d1 + 1) / (d1 - 1)}
    delta_reduced = sp.factor(delta.subs(base))
    d0_reduced = sp.factor((d1 * d4 + d3).subs(base))
    require(delta_reduced == d1 * d4 * (b3*d1 - b3 - d1 - 1)/(d1 - 1),
            "the reduced Delta changed")
    require(d0_reduced == d4 * (d1**2 + 1)/(d1 - 1),
            "the reduced D0 changed")

    # Cof(5,0) solves a0 because D0 remains live.
    cofactor_50 = sp.cancel(rows["cofactor_5_0"].subs(p_solution).subs(base))
    a0_solution = sp.solve(cofactor_50, a0, dict=True, simplify=False)[0]
    base.update(a0_solution)

    # The Kplus factor is the first factor of t123 after B0=E=0.
    kplus = b3 * d1 - b3 + d1 + 1
    t123 = numerator(rows["t_123"].subs(p_solution).subs(base))
    require(sp.rem(sp.Poly(t123, b3, a5, b0, d1, d4),
                   sp.Poly(kplus, b3, a5, b0, d1, d4)) == 0,
            "Kplus ceased to divide t123")
    branch = dict(base)
    branch[b3] = -(d1 + 1) / (d1 - 1)

    # Cof(0,0) now solves a5; its coefficient is live under the stated
    # D0/Laurent hypotheses.
    cofactor_00 = sp.cancel(rows["cofactor_0_0"].subs(p_solution)
                            .subs(branch))
    coefficient_a5 = sp.factor(sp.diff(cofactor_00, a5))
    require(coefficient_a5 != 0, "Cof(0,0) lost its a5 coefficient")
    a5_solution = sp.solve(cofactor_00, a5, dict=True, simplify=False)[0]
    branch.update(a5_solution)

    # Cof(0,3) forces d4=b0^2(d1^2-1)/(2d1).
    cofactor_03 = numerator(rows["cofactor_0_3"].subs(p_solution)
                            .subs(branch))
    d4_relation = b0**2 * (d1**2 - 1) - 2*d1*d4
    quotient_03 = sp.factor(sp.cancel(cofactor_03 / d4_relation))
    require(sp.expand(cofactor_03 - quotient_03*d4_relation) == 0,
            "the Cof(0,3) d4 relation changed")
    require(quotient_03 != 0, "the Cof(0,3) live prefactor vanished")
    branch[d4] = b0**2 * (d1**2 - 1)/(2*d1)

    # The two remaining triangle rows are quadratic in b0.  Work with their
    # primitive numerators so the resultant is independent of live scalars.
    f = primitive(numerator(rows["t_012"].subs(p_solution).subs(branch)),
                  (b0, d1))
    g = primitive(numerator(rows["t_013"].subs(p_solution).subs(branch)),
                  (b0, d1))
    # Remove the remaining live monomial factors from t012.
    f = max((factor for factor, exponent in sp.factor_list(f)[1]),
            key=lambda value: len(sp.Poly(value, b0, d1).terms()))
    g = max((factor for factor, exponent in sp.factor_list(g)[1]),
            key=lambda value: len(sp.Poly(value, b0, d1).terms()))
    require(sp.Poly(f, b0).degree() == 2 and sp.Poly(g, b0).degree() == 2,
            "the final triangle rows ceased to be quadratic in b0")

    qminus = d1**2 - 2*d1 - 1
    qplus = d1**2 + 2*d1 - 1
    qfour = d1**4 + 2*d1**3 + 2*d1**2 - 2*d1 + 1
    resultant = sp.factor(sp.resultant(f, g, b0))
    expected_resultant = (16*d1**5*(d1 - 1)*(d1 + 1)**5
                          * (d1**2 + 1)**2*qminus**2*qplus**2*qfour**2)
    require(sp.expand(resultant - expected_resultant) == 0,
            "the final triangle resultant factorization changed")

    # qplus gives b0=d1, and then every selected offdiagonal factor 1+p_i
    # vanishes.  Checking p1 is enough for the contradiction.
    gb_plus = sp.groebner([b0 - d1, qplus], b0, d1, order="lex")
    p1_value = sp.cancel(p_solution[p1].subs(branch))
    p1_top, p1_bottom = p1_value.as_numer_denom()
    require(gb_plus.reduce(sp.expand(p1_top + p1_bottom))[1] == 0,
            "qplus no longer forces 1+p1=0")

    # qminus gives b0^2+2b0-1=0.  Cof(3,3) supplies a linear separator;
    # two exact univariate resultants give the constant -128.
    bquad_minus = b0**2 + 2*b0 - 1
    gb_minus = sp.groebner([bquad_minus, qminus], b0, d1, order="lex")
    lower_33 = numerator(rows["cofactor_3_3"].subs(p_solution)
                         .subs(branch))
    remainder_minus = sp.factor(gb_minus.reduce(lower_33)[1])
    separator_minus = 425*b0*d1 + 176*b0 - 128*d1 - 53
    require(sp.expand(remainder_minus + 128*separator_minus) == 0,
            "the qminus Cof(3,3) separator changed")
    norm_minus = sp.resultant(bquad_minus, separator_minus, b0)
    constant_minus = sp.resultant(qminus, norm_minus, d1)
    require(constant_minus == -128,
            "the qminus norm ceased to be a characteristic-zero unit")

    # The quartic factor gives the displayed quadratic relation in b0.
    # The same lower cofactor has nonzero algebraic norm 119563878400.
    bquad_four = (4*b0**2 - b0*d1**3 - 3*b0*d1**2 - b0*d1 + b0
                  - 2*d1**3 - 2*d1)
    gb_four = sp.groebner([bquad_four, qfour], b0, d1, order="lex")
    remainder_four = sp.factor(gb_four.reduce(lower_33)[1])
    separator_four = (45*b0*d1**3 + 105*b0*d1**2 - 89*b0*d1 + 37*b0
                      + 175*d1**3 - 221*d1**2 + 115*d1 - 25)
    require(sp.expand(remainder_four - 8*separator_four) == 0,
            "the quartic Cof(3,3) separator changed")
    norm_four = sp.resultant(bquad_four, separator_four, b0)
    constant_four = sp.resultant(qfour, norm_four, d1)
    require(constant_four == 119563878400,
            "the quartic norm ceased to be a characteristic-zero unit")

    # Hostile source mutation: flip one literal t013 monomial.  Repeating the
    # final substitution must destroy the certified resultant.
    term = rows["t_013"].as_ordered_terms()[0]
    mutated_t013 = rows["t_013"] - 2*term
    mutated_g = primitive(numerator(mutated_t013.subs(p_solution)
                                    .subs(branch)), (b0, d1))
    mutated_factors = sp.factor_list(mutated_g)[1]
    mutated_g = max((factor for factor, exponent in mutated_factors),
                    key=lambda value: len(sp.Poly(value, b0, d1).terms()))
    require(sp.expand(sp.resultant(f, mutated_g, b0)
                      - expected_resultant) != 0,
            "the t013 hostile mutation did not fire")

    result = {
        "status": "UNAUDITED exact closure of B0=0, Kplus=0 cycle branch",
        "source_rows": list(upper_labels) + [
            "t_023", "cofactor_5_0", "t_123", "cofactor_0_0",
            "cofactor_0_3", "t_012", "t_013", "cofactor_3_3"],
        "assumptions": [
            "b0*b1*b3*d1*d3*d4 != 0", "Delta != 0", "D0 != 0",
            "p_i*(1+p_i) != 0 for i=1,2,3,4", "B0=b1+d1=0",
            "Kplus=b3*d1-b3+d1+1=0"],
        "forced_t023_relation": str(e_relation),
        "triangle_term_counts": [len(sp.Poly(f, b0, d1).terms()),
                                 len(sp.Poly(g, b0, d1).terms())],
        "triangle_resultant": str(expected_resultant),
        "nonlocal_resultant_factors": [str(qminus), str(qplus), str(qfour)],
        "qplus_obstruction": "1+p1=0",
        "qminus_lower_separator_norm": int(constant_minus),
        "qfour_lower_separator_norm": int(constant_four),
        "hafnian_source_term_count": len(hafnian_data),
        "scope": (
            "This proves emptiness only for the Delta!=0, D0!=0, B0=0, "
            "Kplus=0 solve-denominator subbranch.  The complementary "
            "Kplus!=0 branch, Delta=0 branch, and D0=0 branch remain open."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 cycle B0=0, Kplus=0: PASS")
    print("triangle resultant factors: 3 nonlocal")
    print("lower norms:", constant_minus, constant_four)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
