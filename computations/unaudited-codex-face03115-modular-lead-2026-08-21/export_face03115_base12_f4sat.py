#!/usr/bin/env python3
"""Export the literal normalized (B,T,D)=(0,31,15) base12 F4SAT gate."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
FACE_DIR = (HERE.parent /
            "unaudited-codex-branch0-offdiag-support-strata-2026-08-21")
BUILDER_PATH = FACE_DIR / "build_recursive_face_charts.py"
ROUTING = (HERE.parent / "unaudited-codex-k56-boundary-routing-2026-08-21" /
           "results_k56_recursive_boundary_routing.json")
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
INPUT = HERE / "face03115_base12_full_live_p1073741827.msolve"
LABELS = HERE / "face03115_base12_full_live_labels.json"
RESULT = HERE / "results_face03115_base12_full_live_export.json"
STATE = (0, 31, 15)
CORE = (7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)
OMITTED = (6, 9, 10, 11)
PRIME = 1_073_741_827
ACTIVE_NAMES = ("a0", "a1", "a2", "a3", "a4", "a5",
                "b3", "b4", "b5", "d1", "d2", "d3")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BUILD = load("face03115_literal_builder", BUILDER_PATH)
BASE = BUILD.BASE
MSOLVE_IO = load("face03115_msolve_io", TOOLKIT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def primitive_integer(poly, context):
    require(poly, "zero polynomial")
    denominator = math.lcm(*(value.denominator for value in poly.values()))
    integers = [value.numerator * (denominator // value.denominator)
                for value in poly.values()]
    content = math.gcd(*map(abs, integers))
    value = context.scale(poly, Fraction(denominator, content))
    if value[min(value)] < 0:
        value = context.scale(value, -1)
    require(all(coefficient.denominator == 1
                for coefficient in value.values()),
            "primitive polynomial escaped Z")
    return value


def project(poly, context, active_indices):
    answer = {}
    for exponent, coefficient in primitive_integer(poly, context).items():
        require(all(exponent[index] == 0 for index in range(context.n)
                    if index not in active_indices),
                ("polynomial escaped active normalized variables", exponent))
        key = tuple(exponent[index] for index in active_indices)
        require(key not in answer, "projected monomial collision")
        answer[key] = int(coefficient)
    return answer


def encode(poly):
    pieces = []
    for position, exponent in enumerate(sorted(
            poly, key=lambda item: (sum(item), item), reverse=True)):
        coefficient = poly[exponent]
        symbolic = [name + (f"^{power}" if power != 1 else "")
                    for name, power in zip(ACTIVE_NAMES, exponent, strict=True)
                    if power]
        magnitude = abs(coefficient)
        factors = ([str(magnitude)] if magnitude != 1 or not symbolic else [])
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+")
                       if position else ("-" if coefficient < 0 else ""))
                      + body)
    encoded = "".join(pieces)
    require(encoded and "(" not in encoded and ")" not in encoded and
            "**" not in encoded, "noncanonical msolve syntax")
    return encoded


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
            "permanent row survived solved face specialization")
    h, _ = context.clear_denominators(context.substitute(raw_h))

    tree = BUILD.spanning_tree(STATE[1])
    first_full = min(context.support)
    gauge = {index: context.variable(index) for index in range(context.n)}
    for edge in tree:
        gauge[6 + edge] = context.one
    gauge[context.d_index[first_full]] = context.one
    rows = [(index, label, BUILD.substitute(context, value, gauge))
            for index, label, value in rows]
    h = BUILD.substitute(context, h, gauge)

    base_factors = [context.variable(6 + edge)
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
    return (context, rows, h, selected_base, both_live, c_live, full_live,
            tree, first_full)


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    routing = json.loads(ROUTING.read_text())
    require("0:31:15" in routing["starts"]["k5"]["first_boundary_targets"]
            and next(row for row in routing["starts"]["k5"]["records"]
                     if row["key"] == "0:31:15")[
                         "labelled_zero_subset_count"] == 4,
            "frozen routing of face 0:31:15 changed")
    (context, rows, h, selected_base, both_live, c_live, full_live,
     tree, first_full) = raw_source()
    require(tree == (0, 1, 2) and first_full == 0,
            "canonical torus gauge changed")
    active_indices = tuple(context.variable_names.index(name)
                           for name in ACTIVE_NAMES)
    nonzero = [(index, label, poly) for index, label, poly in rows if poly]
    require(tuple(index for index, _, _ in nonzero) == tuple(range(6, 22)),
            "nonzero literal source-row support changed")
    projected = {index: project(poly, context, active_indices)
                 for index, _, poly in nonzero}
    source_labels = {index: label for index, label, _ in nonzero}

    # Exact constant-coefficient independence: this is the only safe
    # source-row pruning before a polynomial ideal computation.
    monomials = sorted({exponent for poly in projected.values()
                        for exponent in poly})
    matrix = sp.zeros(len(monomials), len(projected))
    monomial_index = {exponent: row for row, exponent in enumerate(monomials)}
    for column, index in enumerate(projected):
        for exponent, coefficient in projected[index].items():
            matrix[monomial_index[exponent], column] = coefficient
    require(matrix.rank() == 16, "literal nonzero rows lost linear independence")

    factors = {
        "H": project(h, context, active_indices),
        "selected_base": project(selected_base, context, active_indices),
        "both_live_a_d": project(both_live, context, active_indices),
        "remaining_c_numerators": project(c_live, context, active_indices),
        "full_live_product": project(full_live, context, active_indices),
    }
    labelled = [(f"raw_{index}_{source_labels[index]}",
                 encode(projected[index])) for index in CORE]
    labelled.append(("SAT_full_exact_live_product",
                     encode(factors["full_live_product"])))
    INPUT.write_text(",".join(ACTIVE_NAMES) + f"\n{PRIME}\n" +
                     ",\n".join(poly for _, poly in labelled) + "\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "core_raw_indices": list(CORE), "omitted_raw_indices": list(OMITTED),
    }, indent=2, sort_keys=True) + "\n")
    parsed = MSOLVE_IO.read_msolve_input(INPUT, strict=True)
    require(parsed.variables == ACTIVE_NAMES and parsed.characteristic == PRIME
            and len(parsed.polynomials) == 13,
            "strict F4SAT input interface changed")
    # Mutation guards localize independently to a source row and saturator.
    mutated_source = dict(projected[CORE[0]])
    mutated_source[max(mutated_source)] *= -1
    mutated_sat = dict(factors["full_live_product"])
    mutated_sat[max(mutated_sat)] *= -1
    require(MSOLVE_IO.polynomial_sha256(encode(mutated_source)) !=
            parsed.polynomial_sha256[0] and
            MSOLVE_IO.polynomial_sha256(encode(mutated_sat)) !=
            parsed.polynomial_sha256[-1],
            "source/saturator coefficient mutations did not fire")

    term_counts = {index: len(projected[index]) for index in projected}
    cofactor_order = sorted(range(10, 22),
                            key=lambda index: (term_counts[index], index))
    require(cofactor_order[:4] == [16, 11, 15, 20],
            "small cofactor profile changed")
    result = {
        "status": "UNAUDITED exact source export; modular gate pending",
        "state": "0:31:15", "characteristic": PRIME,
        "literal_source_rows": list(range(6, 22)),
        "literal_source_rank_over_Q": matrix.rank(),
        "core_kind": "square nonpivot-cofactor compatibility reverse core",
        "core_raw_indices": list(CORE),
        "core_labels": [source_labels[index] for index in CORE],
        "omitted_raw_indices": list(OMITTED),
        "omitted_labels": [source_labels[index] for index in OMITTED],
        "first_omitted_cofactor_to_reverse": {
            "raw_index": 11, "label": source_labels[11],
            "terms": term_counts[11],
        },
        "cofactor_term_order": [{"raw_index": index,
                                  "label": source_labels[index],
                                  "terms": term_counts[index]}
                                 for index in cofactor_order],
        "torus_gauge": ["b0=1", "b1=1", "b2=1", "d0=1"],
        "torus_gauge_scope": (
            "Edges 01,02,03 form a selected-offdiagonal spanning tree. "
            "Their live b entries fix the three site ratios; the residual "
            "common scale sets the live d01 to one over the algebraic "
            "closure, preserving all source zeros and live conditions."),
        "active_variables": list(ACTIVE_NAMES),
        "factor_profiles": {name: {"terms": len(poly),
                                    "degree": max(map(sum, poly)),
                                    "expanded": encode(poly)}
                            for name, poly in factors.items()},
        "exact_live_factorization": (
            "H * (a5*b3*b4) * "
            "(a0*a1*a2*a3*d1*d2*d3) * "
            "(1+a0)*(1+a1*d1)*(1+a2*d2)*(1+a3*d3)"),
        "localized_factors": ["H", "a5", "b3", "b4", "a0", "a1",
                              "a2", "a3", "d1", "d2", "d3",
                              "1+a0", "1+a1*d1", "1+a2*d2",
                              "1+a3*d3"],
        "input_path": INPUT.name,
        "input_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "input_polynomial_sha256": list(parsed.polynomial_sha256),
        "labels_path": LABELS.name,
        "source_hashes": {
            "literal_builder": sha256(BUILDER_PATH.read_bytes()).hexdigest(),
            "routing": sha256(ROUTING.read_bytes()).hexdigest(),
        },
        "must_fire": ["strict coefficient-first parser",
                       "source row7 coefficient sign mutation",
                       "full-live saturator coefficient sign mutation"],
        "scope_guard": (
            "The final row is an F4SAT saturator, not a source equation. "
            "A finite-field UNIT is discovery only. This file concerns only "
            "state 0:31:15 and makes no claim on 0:31:30 or k6."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03115 base12 full-live export: PASS")
    print("core / factor terms", len(CORE),
          {name: len(poly) for name, poly in factors.items()})
    print("input", result["input_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
