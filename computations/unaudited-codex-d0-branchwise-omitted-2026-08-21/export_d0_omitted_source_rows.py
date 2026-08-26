#!/usr/bin/env python3
"""Derive omitted literal rows on the D0,C0,pivot chart exactly.

The frozen D0 eliminant uses four upper cofactor equations, two endpoint
cofactor solves, and the six-row packet

  t012,t013,t023,t123,Cof(0,3),Cof(5,3).

This independent exporter evaluates the four omitted literal lower
cofactors Cof(e,3), e=1..4, after the same exact solves.  Rows t013 and
Cof(0,3) have a selected nonzero coefficient pivot.  We substitute their
exact Cramer solution inside the rational-function field QQ(b0,d1,d4),
avoiding a large generic-expression cancellation.  The primitive numerator
is equivalent to the omitted literal row on the declared pivot-open chart.
No unproved denominator factor is removed.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_PATH = (ROOT / "unaudited-codex-root-integration-2026-08-20" /
               "probe_branch0_cycle_d0_c0_generic.py")
ROWS_OUT = HERE / "d0_omitted_rows.json"
RESULT = HERE / "results_d0_omitted_source_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load("d0_omitted_generic_source", SOURCE_PATH)
sp = P.sp


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def profile(poly, variables):
    value = sp.Poly(poly, *variables)
    encoded = encode(value.as_expr())
    return {"terms": len(value.terms()),
            "total_degree": value.total_degree(),
            "multidegree": [value.degree(variable) for variable in variables],
            "sha256": sha256(encoded.encode("ascii")).hexdigest()}


def derive():
    source = P.SOURCE
    raw_rows, raw_hafnian = source.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: source.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = source.A0, source.A5
    b0, b1, b3, d1, d3, d4 = source.PARAMETERS

    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, source.P, dict=True, simplify=False)[0]
    d0 = {d3: -d1*d4}

    def endpoint_core(label):
        top = sp.cancel(rows[label].subs(p_solution).subs(d0)) \
            .as_numer_denom()[0]
        return max((factor for factor, _ in sp.factor_list(top)[1]),
                   key=lambda value:
                   len(sp.Poly(value, b0, b1, b3, d1, d4).terms()))

    endpoint_rows = [endpoint_core(label)
                     for label in ("cofactor_0_0", "cofactor_5_0")]
    endpoint_matrix, _ = sp.linear_eq_to_matrix(endpoint_rows, [b1, b3])
    endpoint_determinant = sp.factor(endpoint_matrix.det())
    require(endpoint_determinant == -2*b0*d1*(b0**2+d4**2),
            "endpoint determinant changed")
    endpoint = sp.solve(endpoint_rows, [b1, b3], dict=True,
                        simplify=False)[0]

    rational_field, _, _, _, _, _ = P.field("b0,d1,d4,a0,a5", P.QQ)
    substitutions = {**d0, **endpoint}
    values = [rational_field.from_expr(sp.cancel(
        p_solution[variable].subs(substitutions))) for variable in source.P]
    values += [rational_field.from_expr(a0), rational_field.from_expr(a5)]
    values += [rational_field.from_expr(sp.cancel(
        substitutions.get(variable, variable)))
        for variable in source.PARAMETERS]

    def evaluate(poly):
        answer = rational_field.zero
        for exponent, coefficient in poly.items():
            term = rational_field.from_expr(sp.Rational(
                coefficient.numerator, coefficient.denominator))
            for value, power in zip(values, exponent, strict=True):
                term *= value**power
            answer += term
        return sp.primitive(sp.Poly(answer.numer.as_expr(),
                                    b0, d1, d4, a0, a5))[1].as_expr()

    packet_labels = ("t_012", "t_013", "t_023", "t_123",
                     "cofactor_0_3", "cofactor_5_3")
    packet = {label: evaluate(raw[label]) for label in packet_labels}
    coefficient, right = sp.linear_eq_to_matrix(
        [packet["t_013"], packet["cofactor_0_3"]], [a0, a5])
    pivot = sp.primitive(sp.Poly(coefficient.det(), b0, d1, d4))[1].as_expr()
    require(len(sp.Poly(pivot, b0, d1, d4).terms()) == 320,
            "selected pivot changed")

    base_field, _, _, _ = P.field("b0,d1,d4", P.QQ)
    a00 = base_field.from_expr(coefficient[0, 0])
    a01 = base_field.from_expr(coefficient[0, 1])
    a10 = base_field.from_expr(coefficient[1, 0])
    a11 = base_field.from_expr(coefficient[1, 1])
    r0 = base_field.from_expr(right[0])
    r1 = base_field.from_expr(right[1])
    determinant = a00*a11 - a01*a10
    solved_a0 = (r0*a11 - a01*r1) / determinant
    solved_a5 = (a00*r1 - r0*a10) / determinant

    def cramer_numerator(expression):
        polynomial = sp.Poly(expression, a0, a5)
        answer = base_field.zero
        for (power0, power5), coefficient_value in polynomial.terms():
            answer += (base_field.from_expr(coefficient_value) *
                       solved_a0**power0 * solved_a5**power5)
        numerator = sp.primitive(sp.Poly(answer.numer.as_expr(),
                                         b0, d1, d4))[1].as_expr()
        denominator = sp.primitive(sp.Poly(answer.denom.as_expr(),
                                           b0, d1, d4))[1].as_expr()
        # Every cleared factor must already be live: the endpoint factors
        # b0,d1,d4,C0 and the Cramer determinant all divide the selected
        # pivot.  This prevents a numerator-only export from hiding a new
        # localization.
        for factor, _ in sp.factor_list(denominator)[1]:
            require(sp.rem(pivot, factor, b0, d1, d4) == 0,
                    f"unproved cleared denominator factor: {factor}")
        return numerator, sp.factor(denominator)

    output = []
    for label in tuple(f"cofactor_{edge}_3" for edge in range(1, 5)):
        print("evaluating", label, flush=True)
        evaluated = evaluate(raw[label])
        numerator, denominator = cramer_numerator(evaluated)
        output.append((label, numerator, denominator))
        print("completed", label,
              len(sp.Poly(numerator, b0, d1, d4).terms()), flush=True)
    return (b0, d1, d4), pivot, output


def main():
    variables, pivot, rows = derive()
    encoded_rows = []
    for label, polynomial, denominator in rows:
        encoded_rows.append({
            "source_label": label,
            "polynomial": encode(polynomial),
            "profile": profile(polynomial, variables),
            "cleared_denominator_factorization": str(denominator),
        })
    ROWS_OUT.write_text(json.dumps({
        "variables": [str(value) for value in variables],
        "rows": encoded_rows,
    }, indent=2, sort_keys=True) + "\n")
    result = {
        "status": "UNAUDITED exact omitted literal source export PASS",
        "source_path": str(SOURCE_PATH),
        "source_sha256": sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "pivot_profile": profile(pivot, variables),
        "rows": [{"source_label": row["source_label"], **row["profile"]}
                 for row in encoded_rows],
        "rows_path": ROWS_OUT.name,
        "rows_file_sha256": sha256(ROWS_OUT.read_bytes()).hexdigest(),
        "scope": (
            "The exported numerators are exact restrictions of four "
            "literal omitted lower cofactors on the "
            "declared D0=0,C0!=0,selected-pivot!=0 chart. A modular unit "
            "after adjoining one row is discovery until an exact branchwise "
            "Bezout/resultant certificate is replayed."
        ),
        "mutation_control": (
            "The pivot term count and endpoint determinant factorization "
            "are must-fire source-interface guards."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 omitted source export: PASS")
    print("profiles:", [(row["source_label"], row["profile"])
                         for row in encoded_rows])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
