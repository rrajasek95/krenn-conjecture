#!/usr/bin/env python3
"""Exact raw16/raw11 fraction-free pivot for joint face 0:31:15."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import time

import sympy as sp


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_face03115_base12_f4sat.py"
OUT = HERE / "results_face03115_raw16_raw11_resultant.json"
PIVOT_ROW = 16
OMITTED_ROW = 11
PIVOT_VARIABLE = "a2"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face03115_resultant_source", EXPORTER)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def expression(poly, symbols):
    return sp.expand(sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(symbols, exponent, strict=True))
        for exponent, coefficient in poly.items())))


def encode(poly, symbols):
    polynomial = sp.Poly(sp.expand(poly), *symbols)
    pieces = []
    for position, (monomial, coefficient) in enumerate(polynomial.terms()):
        require(coefficient.q == 1, "encoded polynomial escaped Z")
        coefficient = int(coefficient)
        symbolic = [str(symbol) + (f"^{power}" if power != 1 else "")
                    for symbol, power in zip(symbols, monomial, strict=True)
                    if power]
        magnitude = abs(coefficient)
        factors = ([str(magnitude)] if magnitude != 1 or not symbolic else [])
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+")
                       if position else ("-" if coefficient < 0 else ""))
                      + body)
    return "".join(pieces)


def main():
    started = time.monotonic()
    context, rows, *_ = E.raw_source()
    active_indices = tuple(context.variable_names.index(name)
                           for name in E.ACTIVE_NAMES)
    symbols = sp.symbols(" ".join(E.ACTIVE_NAMES))
    symbol_map = dict(zip(E.ACTIVE_NAMES, symbols, strict=True))
    source = {index: E.project(poly, context, active_indices)
              for index, _, poly in rows if poly}
    labels = {index: label for index, label, poly in rows if poly}
    expressions = {index: expression(poly, symbols)
                   for index, poly in source.items()}
    pivot = symbol_map[PIVOT_VARIABLE]

    # Profile all core rows against variables that also occur in raw11.
    omitted_variables = {symbol for symbol in symbols
                         if sp.Poly(expressions[OMITTED_ROW], symbol).degree()
                         == 1}
    profiles = []
    for index in E.CORE:
        row = expressions[index]
        for symbol in sorted(omitted_variables, key=str):
            polynomial = sp.Poly(row, symbol)
            if polynomial.degree() != 1:
                continue
            coefficient = sp.factor(polynomial.LC())
            profiles.append({
                "raw_index": index, "label": labels[index],
                "row_terms": len(source[index]), "variable": str(symbol),
                "coefficient": str(coefficient).replace("**", "^"),
                "coefficient_terms": len(sp.Poly(coefficient, *symbols).terms()),
                "coefficient_degree": int(sp.total_degree(coefficient)),
            })
    require(min(len(source[index]) for index in E.CORE) == 8 and
            len(source[PIVOT_ROW]) == 8 and labels[PIVOT_ROW] ==
            "cofactor_3_0",
            "shortest core-row profile changed")

    P = sp.Poly(expressions[PIVOT_ROW], pivot)
    Q = sp.Poly(expressions[OMITTED_ROW], pivot)
    require(P.degree() == Q.degree() == 1,
            "raw16/raw11 stopped being linear in a2")
    A, B = map(sp.expand, P.all_coeffs())
    C, D = map(sp.expand, Q.all_coeffs())
    b4, d2 = symbol_map["b4"], symbol_map["d2"]
    require(sp.expand(A-b4*(d2-1)) == 0,
            "pivot coefficient changed")
    # b4 is in the declared selected-base live monomial.  Hence the only new
    # coefficient branch is L=d2-1.
    L = d2 - 1
    resultant = sp.expand(sp.resultant(P.as_expr(), Q.as_expr(), pivot))
    direct = sp.expand(A*D-B*C)
    require(sp.expand(resultant-direct) == 0 and
            sp.expand(A*Q.as_expr()-C*P.as_expr()-resultant) == 0,
            "fraction-free resultant identity failed")
    factor_coefficient, factors = sp.factor_list(resultant)
    require(factor_coefficient in (1, -1) and len(factors) == 1 and
            factors[0][1] == 1 and
            sp.expand(factor_coefficient*factors[0][0]-resultant) == 0,
            "resultant factor profile changed")
    residual_factor = sp.expand(factors[0][0])
    branch_zero = sp.factor(B.subs(d2, 1))
    expected_branch_zero = (symbol_map["a5"]*(symbol_map["d1"]+1)*
                            (b4-1)+b4+1)
    require(sp.expand(branch_zero-expected_branch_zero) == 0,
            "d2=1 residual changed")

    # Exact solution/reverse identities.  On L!=0, A is live and raw16=0
    # gives a2=-B/A; raw11 then vanishes iff the 29-term resultant vanishes.
    solved_substitution = -B/A
    require(sp.cancel(Q.as_expr().subs(pivot, solved_substitution) -
                      resultant/A) == 0,
            "solved raw11/resultant equivalence failed")
    # Must-fire controls.
    require(sp.expand(A*D+B*C-resultant) != 0,
            "resultant sign mutation did not fire")
    require(sp.expand(A-b4*(d2+1)) != 0,
            "coefficient-branch mutation did not fire")

    result_variables = tuple(symbol for symbol in symbols if symbol != pivot)
    result = {
        "status": "UNAUDITED exact fraction-free pivot/resultant PASS",
        "state": "0:31:15", "pivot_row": PIVOT_ROW,
        "pivot_label": labels[PIVOT_ROW],
        "omitted_row": OMITTED_ROW,
        "omitted_label": labels[OMITTED_ROW],
        "pivot_variable": PIVOT_VARIABLE,
        "core_linear_profiles": profiles,
        "selection_reason": (
            "raw16 is the unique shortest core row (8 terms); in shared "
            "raw11 variable a2 its coefficient is the declared-live b4 "
            "times the single new binomial d2-1"),
        "P_raw16": encode(P.as_expr(), symbols),
        "Q_raw11": encode(Q.as_expr(), symbols),
        "A_pivot_coefficient": encode(A, symbols),
        "B_pivot_constant": encode(B, symbols),
        "C_omitted_coefficient": encode(C, symbols),
        "D_omitted_constant": encode(D, symbols),
        "fraction_free_identity": "A*raw11-C*raw16=R",
        "new_factor_split": {
            "declared_live_factor": "b4",
            "new_factor": "d2-1",
            "open_branch": (
                "d2-1 != 0: a2=-B/(b4*(d2-1)); raw11=0 iff R=0"),
            "closed_branch": (
                "d2=1: raw16 reduces to "
                "a5*(d1+1)*(b4-1)+b4+1=0; a2 is not solved"),
        },
        "resultant": encode(resultant, result_variables),
        "resultant_terms": len(sp.Poly(resultant, *result_variables).terms()),
        "resultant_total_degree": int(sp.total_degree(resultant)),
        "factorization": {
            "content": int(factor_coefficient),
            "irreducible_factor_count": len(factors),
            "factors": [{"polynomial": encode(factor, result_variables),
                         "exponent": int(exponent),
                         "terms": len(sp.Poly(factor,
                                              *result_variables).terms()),
                         "degree": int(sp.total_degree(factor))}
                        for factor, exponent in factors],
        },
        "closed_branch_raw16": encode(branch_zero, result_variables),
        "source_sha256": sha256(EXPORTER.read_bytes()).hexdigest(),
        "must_fire": ["resultant cross-term sign flip",
                       "d2-1 to d2+1 coefficient mutation"],
        "scope_guard": (
            "This is one exact two-row elimination identity, not an ideal "
            "closure. The d2=1 branch remains explicit, and no GB/F4SAT "
            "calculation is performed."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    result["elapsed_seconds"] = round(time.monotonic()-started, 6)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03115 raw16/raw11 resultant: PASS")
    print("R terms/degree/factors", result["resultant_terms"],
          result["resultant_total_degree"], len(factors))
    print("closed branch", result["closed_branch_raw16"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
