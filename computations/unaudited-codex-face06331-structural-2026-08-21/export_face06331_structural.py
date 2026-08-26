#!/usr/bin/env python3
"""Freeze the normalized literal source interface for k5 interior 0:63:31."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-face03115-modular-lead-2026-08-21"
PARENT_SOURCE = PARENT / "export_face03115_base12_f4sat.py"
ROUTING = (HERE.parent / "unaudited-codex-k56-boundary-routing-2026-08-21" /
           "results_k56_recursive_boundary_routing.json")
OUT = HERE / "results_face06331_structural.json"
STATE = (0, 63, 31)
ACTIVE = ("a0", "a1", "a2", "a3", "a4", "a5",
          "b3", "b4", "b5", "d1", "d2", "d3", "d4")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face06331_parent_interface", PARENT_SOURCE)
BUILD, BASE = E.BUILD, E.BASE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def expression(poly, symbols):
    return sp.expand(sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(symbols, exponent, strict=True))
        for exponent, coefficient in poly.items())))


def encode(poly, symbols):
    pieces = []
    value = sp.Poly(sp.expand(poly), *symbols, domain=sp.ZZ)
    for position, (exponent, coefficient) in enumerate(value.terms()):
        coefficient = int(coefficient)
        symbolic = [str(symbol) + (f"^{power}" if power != 1 else "")
                    for symbol, power in zip(symbols, exponent, strict=True)
                    if power]
        magnitude = abs(coefficient)
        factors = ([str(magnitude)] if magnitude != 1 or not symbolic else [])
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+") if position else
                       ("-" if coefficient < 0 else "")) + body)
    return "".join(pieces)


def raw_source():
    context = BUILD.FaceContext(STATE[1], STATE[2])
    equations, raw_h = BASE.PROBE.equations((0,) * 6)
    labels = BASE.raw_labels()
    rows = []
    for index, (label, equation) in enumerate(zip(labels, equations,
                                                   strict=True)):
        value = context.substitute(equation)
        if value:
            value, _ = context.clear_denominators(value)
        rows.append((index, label, value))
    require(not any(poly for _, _, poly in rows[:6]),
            "permanent row survived solved face")
    h, _ = context.clear_denominators(context.substitute(raw_h))
    tree = BUILD.spanning_tree(STATE[1])
    first_full = min(context.support)
    gauge = {index: context.variable(index) for index in range(context.n)}
    for edge in tree:
        gauge[6 + edge] = context.one
    gauge[context.d_index[first_full]] = context.one
    rows = [(index, label, BUILD.substitute(context, poly, gauge))
            for index, label, poly in rows]
    h = BUILD.substitute(context, h, gauge)
    base_factors = [context.variable(6+edge)
                    if STATE[1] >> edge & 1 else context.variable(edge)
                    for edge in range(6)]
    selected_base = BUILD.substitute(
        context, context.multiply(*base_factors), gauge)
    both_live = BUILD.substitute(context, context.multiply(*(
        context.multiply(context.variable(edge),
                         context.variable(context.d_index[edge]))
        for edge in context.support)), gauge)
    c_live = BUILD.substitute(context, context.multiply(*(
        context.add(context.one,
                    context.multiply(context.variable(edge),
                                     context.variable(context.d_index[edge])))
        for edge in context.support)), gauge)
    full_live = context.multiply(h, selected_base, both_live, c_live)
    return context, rows, h, selected_base, both_live, c_live, full_live, tree


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    routing = json.loads(ROUTING.read_text())
    require(routing["starts"]["k5"]["start_key"] == "0:63:31",
            "frozen k5 start changed")
    context, rows, h, selected, both, c_live, full, tree = raw_source()
    require(tree == (0, 1, 2) and tuple(context.support) == (0, 1, 2, 3, 4),
            "canonical gauge/support changed")
    active_indices = tuple(context.variable_names.index(name) for name in ACTIVE)
    require(tuple(context.variable_names[index] for index in active_indices) ==
            ACTIVE, "active variable interface changed")
    nonzero = [(index, label, poly) for index, label, poly in rows if poly]
    require(tuple(index for index, _, _ in nonzero) == tuple(range(6, 22)),
            "literal source row support changed")
    projected = {index: E.project(poly, context, active_indices)
                 for index, _, poly in nonzero}
    labels = {index: label for index, label, _ in nonzero}
    factors = {"H": E.project(h, context, active_indices),
               "selected_base": E.project(selected, context, active_indices),
               "both_live": E.project(both, context, active_indices),
               "remaining_c": E.project(c_live, context, active_indices),
               "full_live": E.project(full, context, active_indices)}
    symbols = sp.symbols(" ".join(ACTIVE))
    expressions = {index: expression(poly, symbols)
                   for index, poly in projected.items()}

    monomials = sorted({exponent for poly in projected.values()
                        for exponent in poly})
    matrix = sp.zeros(len(monomials), len(projected))
    row_of = {monomial: row for row, monomial in enumerate(monomials)}
    for column, index in enumerate(projected):
        for exponent, coefficient in projected[index].items():
            matrix[row_of[exponent], column] = coefficient
    require(matrix.rank() == 16, "literal row rank changed")

    linear = []
    for index, poly in expressions.items():
        for variable in symbols:
            value = sp.Poly(poly, variable)
            if value.degree() != 1:
                continue
            coefficient, constant = map(sp.expand, value.all_coeffs())
            coefficient_factor = sp.factor(coefficient)
            linear.append({
                "raw_index": index, "label": labels[index],
                "row_terms": len(projected[index]),
                "variable": str(variable),
                "coefficient": encode(coefficient, symbols),
                "coefficient_factorization": str(coefficient_factor).replace(
                    "**", "^"),
                "coefficient_terms": len(sp.Poly(coefficient, *symbols).terms()),
                "coefficient_degree": int(sp.total_degree(coefficient)),
                "constant": encode(constant, symbols),
                "constant_terms": len(sp.Poly(constant, *symbols).terms()),
            })
    linear.sort(key=lambda row: (row["coefficient_terms"], row["row_terms"],
                                 row["constant_terms"], row["raw_index"],
                                 row["variable"]))
    best = linear[0]
    # Exact replay of the chosen P=coefficient*variable+constant identity.
    variable = next(symbol for symbol in symbols
                    if str(symbol) == best["variable"])
    polynomial = sp.Poly(expressions[best["raw_index"]], variable)
    coefficient, constant = map(sp.expand, polynomial.all_coeffs())
    require(sp.expand(expressions[best["raw_index"]]-
                      coefficient*variable-constant) == 0,
            "best linear pivot replay failed")
    require(best["raw_index"] == 8 and best["variable"] == "a1" and
            sp.expand(coefficient-(symbols[9]-symbols[10])) == 0,
            "canonical shortest pivot changed")
    a1, a2, a5 = symbols[1], symbols[2], symbols[5]
    b5, d1, d2 = symbols[8], symbols[9], symbols[10]
    delta = sp.expand(d1-d2)
    tail = sp.expand(a5*b5*(d1+d2)-b5**2-2*b5+1)
    closed = sp.expand(2*a5*b5*d1-b5**2-2*b5+1)
    require(sp.expand(expressions[8]-delta*(a1+a2*b5**2)-tail) == 0 and
            sp.expand(tail.subs(d2, d1)-closed) == 0,
            "raw8 delta-split identity failed")

    result = {
        "status": "UNAUDITED exact structural source interface PASS",
        "state": "0:63:31", "kind": "k5 full interior",
        "support_edges": list(context.support),
        "selected_term_mask": 63,
        "torus_gauge": ["b0=1", "b1=1", "b2=1", "d0=1"],
        "gauge_scope": ("The all-offdiagonal selected graph contains the "
                        "tree 01,02,03; its live b entries fix three site "
                        "ratios and the common scale fixes live d01."),
        "active_variables": list(ACTIVE),
        "literal_source_rows": list(range(6, 22)),
        "literal_source_rank_over_Q": int(matrix.rank()),
        "row_profiles": [{"raw_index": index, "label": labels[index],
                          "terms": len(projected[index]),
                          "degree": max(map(sum, projected[index]))}
                         for index in projected],
        "factor_profiles": {name: {"terms": len(poly),
                                    "degree": max(map(sum, poly)),
                                    "polynomial": encode(expression(poly,
                                                                     symbols),
                                                         symbols)}
                            for name, poly in factors.items()},
        "exact_live_factorization": (
            "H * (b3*b4*b5) * "
            "(a0*a1*a2*a3*a4*d1*d2*d3*d4) * "
            "(1+a0)*(1+a1*d1)*(1+a2*d2)*(1+a3*d3)*(1+a4*d4)"),
        "linear_profiles": linear,
        "shortest_linear_pivot": best,
        "shortest_sound_split": {
            "delta": encode(delta, symbols),
            "identity": (
                "raw8=(d1-d2)*(a1+a2*b5^2)+"
                "a5*b5*(d1+d2)-b5^2-2*b5+1"),
            "delta_nonzero": "solve a1 from the nine-term raw8 equation",
            "delta_zero": encode(closed, symbols),
            "delta_zero_terms": 4,
        },
        "source_hashes": {"parent_interface": sha256(
            PARENT_SOURCE.read_bytes()).hexdigest(),
                          "routing": sha256(ROUTING.read_bytes()).hexdigest()},
        "must_fire": ["literal 16-row rank", "best linear pivot replay"],
        "scope_guard": ("Structural export only. No GB/F4SAT/msolve/rank "
                        "membership or emptiness computation was launched."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("face06331 structural export: PASS")
    print("rows/live terms", len(projected),
          {name: len(poly) for name, poly in factors.items()})
    print("best", best["raw_index"], best["variable"],
          best["coefficient_terms"], best["row_terms"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
