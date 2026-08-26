#!/usr/bin/env python3
"""Exact closure of the L=0 subbranch in the B0 cycle denominator chart.

This continues ``audit_branch0_cycle_b0_denominator_kplus.py``.  Under
Delta,D0 nonzero and B0=0, take the complementary Kplus!=0 factor of t123,
so t123 solves a5.  Cof(0,0), after removing the live b3 factor, is linear
in b3.  This audit closes the exceptional branch on which that new solve
coefficient L vanishes.  The still-complementary L!=0 branch is not decided.
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
OUT = HERE / "results_branch0_cycle_b0_kplus_complement_lzero.json"
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "discover_branch0_k4_cycle_cramer_generic.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_cycle_b0_lzero_source", GENERIC)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sparse_value(poly, values, reducer=lambda value: sp.factor(sp.cancel(value))):
    answer = sp.Integer(0)
    for exponent, coefficient in poly.items():
        term = sp.Rational(coefficient.numerator, coefficient.denominator)
        for value, power in zip(values, exponent):
            term *= value**power
        answer += term
    return reducer(answer)


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    p1, p2, p3, p4 = SOURCE.P
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS

    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]
    base = {b1: -d1, d3: d4*(d1 + 1)/(d1 - 1)}
    base.update(sp.solve(sp.cancel(rows["cofactor_5_0"]
                                   .subs(p_solution).subs(base)),
                         a0, dict=True, simplify=False)[0])

    # Kplus!=0 makes the second t123 factor vanish and solves a5.
    a5_equation = (2*a5*d1**2*d4 - 2*b0*d1**2 + 2*b0*d1
                   + d1**2*d4 + d4)
    base.update(sp.solve(a5_equation, a5, dict=True, simplify=False)[0])

    cofactor_00 = sp.cancel(rows["cofactor_0_0"].subs(p_solution).subs(base))
    top_00 = sp.expand(cofactor_00.as_numer_denom()[0])
    factors_00 = sp.factor_list(top_00)[1]
    core_00 = max((factor for factor, exponent in factors_00),
                  key=lambda value: len(sp.Poly(value, b3).terms()))
    coefficient = sp.factor(sp.Poly(core_00, b3).coeff_monomial(b3))
    constant = sp.factor(sp.Poly(core_00, b3).coeff_monomial(1))

    lzero = (2*b0*d1**2 - 2*b0*d1
             - d4*(d1**3 + 3*d1**2 - d1 + 1))
    mzero = (2*b0*d1**4 - 2*b0*d1**2 - d1**4*d4 - 2*d1**4
             - 2*d1**3*d4 - 2*d1**3 - 4*d1**2*d4 + 6*d1**2
             - 2*d1*d4 - 2*d1 + d4)
    require(sp.expand(coefficient - (d1 - 1)*lzero) == 0,
            "the Cof(0,0) solve coefficient L changed")
    require(sp.expand(constant + d1*mzero) == 0,
            "the Cof(0,0) constant M changed")

    # On L=0, the live b3 factor and Cof(0,0)=0 force M=0.
    lm_resultant = sp.factor(sp.resultant(lzero, mzero, b0))
    qplus = d1**2 + 2*d1 - 1
    expected_lm = (2*d1*(d1 - 1)**2*qplus
                   * (d1**2*d4 + 2*d1*d4 - 2*d1 + d4))
    require(sp.expand(lm_resultant - expected_lm) == 0,
            "the L,M resultant changed")

    # Degenerate determinant qplus=0: L=M imply b0=-(d1+2)d4,
    # and the four upper Cramer solutions all have p_i=-1.
    gb_degenerate = sp.groebner([lzero, mzero, qplus], b0, d4, d1,
                                order="lex")
    require(any(sp.expand(poly.as_expr() - (b0 + d1*d4 + 2*d4)) == 0
                for poly in gb_degenerate.polys),
            "the qplus L,M relation changed")
    degenerate = dict(base)
    degenerate[b0] = -(d1 + 2)*d4
    for variable in SOURCE.P:
        value = sp.cancel(p_solution[variable].subs(degenerate))
        top, bottom = value.as_numer_denom()
        require(sp.rem(sp.expand(top + bottom), qplus, d1) == 0,
                f"qplus ceased to force 1+{variable}=0")

    # Away from qplus, solve L=M for b0,d4.  Every denominator below is a
    # stated Laurent/D0/Delta/b0/qplus factor.
    solved_lm = {
        b0: (d1**3 + 3*d1**2 - d1 + 1)/((d1 - 1)*(d1 + 1)**2),
        d4: 2*d1/(d1 + 1)**2,
    }
    require(sp.cancel(lzero.subs(solved_lm)) == 0
            and sp.cancel(mzero.subs(solved_lm)) == 0,
            "the generic L=M parametrization changed")
    parameters = dict(base)
    parameters.update(solved_lm)
    parameters[d3] = 2*d1/((d1 - 1)*(d1 + 1))

    values = [sp.factor(sp.cancel(p_solution[variable].subs(parameters)))
              for variable in SOURCE.P]
    values += [sp.factor(sp.cancel(base[a0].subs(parameters))),
               sp.factor(sp.cancel(base[a5].subs(parameters)))]
    values += [sp.factor(sp.cancel(parameters.get(variable, variable)))
               for variable in SOURCE.PARAMETERS]

    triangle_012 = sparse_value(raw["t_012"], values)
    triangle_013 = sparse_value(raw["t_013"], values)
    cofactor_03 = sparse_value(raw["cofactor_0_3"], values)
    f = max((factor for factor, exponent in
             sp.factor_list(triangle_012.as_numer_denom()[0])[1]),
            key=lambda value: len(sp.Poly(value, b3, d1).terms()))
    g = max((factor for factor, exponent in
             sp.factor_list(triangle_013.as_numer_denom()[0])[1]),
            key=lambda value: len(sp.Poly(value, b3, d1).terms()))
    c_factors = [factor for factor, exponent in
                 sp.factor_list(cofactor_03.as_numer_denom()[0])[1]
                 if len(sp.Poly(factor, b3, d1).terms()) > 1]
    require(len(c_factors) == 2, "Cof(0,3) ceased to split into two factors")
    c1, c2 = sorted(c_factors,
                    key=lambda value: len(sp.Poly(value, b3, d1).terms()))
    require(len(sp.Poly(f, b3, d1).terms()) == 34
            and len(sp.Poly(g, b3, d1).terms()) == 24,
            "the generic triangle cores changed")

    # First Cof(0,3) factor: the two triangle resultants are coprime.
    f1 = sp.resultant(f, c1, b3)
    g1 = sp.resultant(g, c1, b3)
    norm_c1 = sp.resultant(f1, g1, d1)
    expected_norm_c1 = 38973380220162416179749905447126040576
    require(norm_c1 == expected_norm_c1,
            "the first Cof(0,3) factor norm changed")

    # Second factor: two apparent common factors remain after eliminating b3.
    # The cubic is a leading-coefficient artefact; C2 has zero b3 coefficient
    # but a constant of norm -256 there.  The quartic forces Delta=0 and is
    # therefore outside this Cramer branch.
    f2 = sp.resultant(f, c2, b3)
    g2 = sp.resultant(g, c2, b3)
    qthree = d1**3 + 3*d1**2 - d1 + 1
    qfour = d1**4 + 2*d1**3 + 6*d1**2 - 2*d1 + 1
    require(sp.factor(sp.gcd(f2, g2)) == qthree*qfour,
            "the second Cof(0,3) elimination gcd changed")
    c2_poly = sp.Poly(c2, b3)
    c2_lead = c2_poly.coeff_monomial(b3)
    c2_constant = c2_poly.coeff_monomial(1)
    require(sp.rem(c2_lead, qthree, d1) == 0,
            "the cubic leading-coefficient degeneration changed")
    require(sp.resultant(qthree, c2_constant, d1) == -256,
            "the cubic C2 constant norm changed")

    gb_four = sp.groebner([f, g, c2, qfour], b3, d1, order="lex")
    b3_relation = 4*b3 + d1**3 + 3*d1**2 + 9*d1 + 3
    require(any(sp.expand(poly.as_expr() - b3_relation) == 0
                for poly in gb_four.polys),
            "the quartic b3 relation changed")
    kminus = b3*d1 - b3 - d1 - 1
    require(gb_four.reduce(kminus)[1] == 0,
            "the quartic component ceased to force Delta=0")

    # Hostile mutation of the literal Cof(0,3) row must destroy its certified
    # two-factor numerator.
    mutated = dict(raw["cofactor_0_3"])
    key = sorted(mutated)[0]
    mutated[key] = -mutated[key]
    mutated_cofactor = sparse_value(mutated, values)
    mutated_top = mutated_cofactor.as_numer_denom()[0]
    require(sp.rem(sp.Poly(mutated_top, b3, d1),
                   sp.Poly(c1*c2, b3, d1)) != 0,
            "the Cof(0,3) hostile mutation did not fire")

    result = {
        "status": "UNAUDITED exact closure of B0=0, Kplus!=0, L=0",
        "source_rows": [
            "cofactor_1_0", "cofactor_2_0", "cofactor_3_0",
            "cofactor_4_0", "t_023", "cofactor_5_0", "t_123",
            "cofactor_0_0", "t_012", "t_013", "cofactor_0_3",
        ],
        "assumptions": [
            "Delta != 0", "D0 != 0", "B0=b1+d1=0",
            "Kplus=b3*d1-b3+d1+1 != 0", "L=0",
            "all Laurent and p_i*(1+p_i) factors are live"],
        "lm_resultant": str(expected_lm),
        "degenerate_qplus_obstruction": "1+p_i=0 for all four i",
        "generic_triangle_terms": [34, 24],
        "first_factor_norm": int(norm_c1),
        "second_factor_cubic_norm": -256,
        "second_factor_quartic_obstruction": "Delta=0",
        "scope": (
            "This closes the L=0 branch after B0=0 and Kplus!=0.  The "
            "L!=0 branch, D0=0 branch, and Delta=0 branch remain open."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 cycle B0=0, Kplus!=0, L=0: PASS")
    print("norms / obstruction:", norm_c1, -256, "Delta=0")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
