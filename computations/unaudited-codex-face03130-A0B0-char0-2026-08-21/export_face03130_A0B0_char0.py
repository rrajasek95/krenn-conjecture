#!/usr/bin/env python3
"""Export the exact 0:31:30 closed-pivot branch A=B=0 over Q."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FACE_DIR = (HERE.parent /
            "unaudited-codex-branch0-offdiag-support-strata-2026-08-21")
BUILDER_PATH = FACE_DIR / "build_recursive_face_charts.py"
PARENT_DIR = HERE.parent / "unaudited-codex-face03130-structural-2026-08-21"
PARENT_RESULT = PARENT_DIR / "results_face03130_reverse_interface_standard.json"
ROUTING = (HERE.parent / "unaudited-codex-k56-boundary-routing-2026-08-21" /
           "results_k56_recursive_boundary_routing.json")
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
INPUT = HERE / "face03130_A0B0_base_live_char0.msolve"
RESULT = HERE / "results_face03130_A0B0_char0_export.json"
STATE = (0, 31, 30)
ACTIVE_NAMES = ("a0", "a1", "a2", "a3", "a4", "a5",
                "b3", "b4", "b5", "d2", "d3", "d4")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


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
                for coefficient in value.values()), "escaped Z")
    return value


def project(poly, context, active_indices):
    answer = {}
    for exponent, coefficient in primitive_integer(poly, context).items():
        require(all(exponent[index] == 0 for index in range(context.n)
                    if index not in active_indices),
                f"polynomial escaped gauge: {exponent}")
        key = tuple(exponent[index] for index in active_indices)
        require(key not in answer, "projected monomial collision")
        answer[key] = int(coefficient)
    return answer


def encode(poly, names=ACTIVE_NAMES):
    pieces = []
    for position, exponent in enumerate(sorted(
            poly, key=lambda item: (sum(item), item), reverse=True)):
        coefficient = poly[exponent]
        symbolic = [name + (f"^{power}" if power != 1 else "")
                    for name, power in zip(names, exponent, strict=True)
                    if power]
        magnitude = abs(coefficient)
        factors = ([str(magnitude)] if magnitude != 1 or not symbolic else [])
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+")
                       if position else ("-" if coefficient < 0 else ""))
                      + body)
    value = "".join(pieces)
    require(value and "(" not in value and ")" not in value and
            "**" not in value, "noncanonical msolve polynomial")
    return value


def multiply(left, right):
    answer = {}
    for a, ca in left.items():
        for b, cb in right.items():
            exponent = tuple(x + y for x, y in zip(a, b, strict=True))
            answer[exponent] = answer.get(exponent, 0) + ca * cb
    return {exponent: coefficient for exponent, coefficient in answer.items()
            if coefficient}


def source_chart(BUILD):
    context = BUILD.FaceContext(STATE[1], STATE[2])
    equations, raw_h = BUILD.BASE.PROBE.equations((0,) * 6)
    labels = BUILD.BASE.raw_labels()
    rows = []
    for index, (label, equation) in enumerate(zip(labels, equations,
                                                   strict=True)):
        value = context.substitute(equation)
        if value:
            value, shift = context.clear_denominators(value)
        else:
            shift = context.zero_exponent
        rows.append((index, label, value, shift))
    require(not any(poly for _, _, poly, _ in rows[:6]),
            "permanent row survived solved substitution")
    h, h_shift = context.clear_denominators(context.substitute(raw_h))

    tree = BUILD.spanning_tree(STATE[1])
    first_full = min(context.support)
    gauge = {index: context.variable(index) for index in range(context.n)}
    for edge in tree:
        gauge[6 + edge] = context.one
    gauge[context.d_index[first_full]] = context.one
    rows = [(index, label, BUILD.substitute(context, value, gauge), shift)
            for index, label, value, shift in rows]
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
    base_live = context.multiply(selected_base, both_live, c_live)
    return (context, rows, h, h_shift, selected_base, both_live, c_live,
            base_live, tree, first_full)


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((REPO / ".venv/lib").glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp
    BUILD = load("face03130_A0B0_builder", BUILDER_PATH)
    IO = load("face03130_A0B0_msolve_io", TOOLKIT)
    parent = json.loads(PARENT_RESULT.read_text())
    require(parent["logical_sha256"] ==
            "96052061416f3e47eb5d2b051ba92f3e6d2f34d7bdc2198778697ba7670418ba",
            "frozen structural interface changed")
    routing = json.loads(ROUTING.read_text())
    require("0:31:30" in routing["starts"]["k5"]["first_boundary_targets"],
            "routing changed")
    (context, rows, h, h_shift, selected_base, both_live, c_live, base_live,
     tree, first_full) = source_chart(BUILD)
    require(tree == (0, 1, 2) and first_full == 1,
            "canonical torus gauge changed")
    active_indices = tuple(context.variable_names.index(name)
                           for name in ACTIVE_NAMES)
    nonzero = [(index, label, poly, shift)
               for index, label, poly, shift in rows if poly]
    require(tuple(index for index, _, _, _ in nonzero) == tuple(range(6, 22)),
            "literal source support changed")
    projected = {index: project(poly, context, active_indices)
                 for index, _, poly, _ in nonzero}
    labels = {index: label for index, label, _, _ in nonzero}
    factors = {
        "H": project(h, context, active_indices),
        "selected_base": project(selected_base, context, active_indices),
        "both_live_a_d": project(both_live, context, active_indices),
        "remaining_c_numerators": project(c_live, context, active_indices),
        "base_live_without_H": project(base_live, context, active_indices),
    }

    symbols = sp.symbols(" ".join(ACTIVE_NAMES))
    by_name = dict(zip(ACTIVE_NAMES, symbols))

    def expression(poly):
        return sp.Add(*(coefficient * sp.prod(
            symbol ** power for symbol, power in zip(symbols, exponent,
                                                       strict=True))
            for exponent, coefficient in poly.items()))

    raw7 = sp.Poly(expression(projected[7]), by_name["a4"])
    require(raw7.degree() == 1, "raw7 lost a4-linearity")
    A_expr, B_expr = raw7.nth(1), raw7.nth(0)
    A = sp.Poly(A_expr, *symbols, domain=sp.QQ)
    B = sp.Poly(B_expr, *symbols, domain=sp.QQ)

    def poly_dict(value):
        answer = {}
        for exponent, coefficient in value.terms():
            require(coefficient.q == 1, "branch polynomial escaped Z")
            answer[exponent] = int(coefficient.p)
        return answer

    A_dict, B_dict = poly_dict(A), poly_dict(B)
    packet = parent["best_fraction_free_packet"]
    require(str(A_expr) == packet["pivot_coefficient"] and
            str(B_expr) == packet["pivot_residual"],
            "A/B no longer match frozen fraction-free packet")
    require(sp.expand(A_expr * by_name["a4"] + B_expr - raw7.as_expr()) == 0,
            "literal raw7=A*a4+B replay failed")

    # Exact constant-coefficient source rank; no source row is discarded.
    monomials = sorted({exponent for poly in projected.values()
                        for exponent in poly})
    matrix = sp.zeros(len(monomials), len(projected))
    mindex = {exponent: row for row, exponent in enumerate(monomials)}
    for column, index in enumerate(projected):
        for exponent, coefficient in projected[index].items():
            matrix[mindex[exponent], column] = coefficient
    require(matrix.rank() == 16, "literal source rows lost rank")

    labelled = [("branch_A", encode(A_dict)),
                ("branch_B", encode(B_dict))]
    labelled.extend((f"raw_{index}_{labels[index]}", encode(projected[index]))
                    for index in range(6, 22))
    live_with_z = {(1,) + exponent: coefficient
                   for exponent, coefficient in
                   factors["base_live_without_H"].items()}
    live_with_z[(0,) * (len(ACTIVE_NAMES) + 1)] = -1
    labelled.append(("RAB_base_live_without_H",
                     encode(live_with_z, ("z",) + ACTIVE_NAMES)))
    INPUT.write_text("z," + ",".join(ACTIVE_NAMES) + "\n0\n" +
                     ",\n".join(poly for _, poly in labelled) + "\n")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.variables == ("z",) + ACTIVE_NAMES and
            parsed.characteristic == 0 and len(parsed.polynomials) == 19,
            "strict input replay failed")
    require("(" not in INPUT.read_text() and ")" not in INPUT.read_text(),
            "parenthesis parser guard failed")
    mutated = dict(A_dict); mutated[max(mutated)] *= -1
    require(IO.polynomial_sha256(encode(mutated)) !=
            parsed.polynomial_sha256[0], "A mutation failed to fire")

    result = {
        "status": "exact Q A=B=0 full-source export PASS; gate pending",
        "state": "0:31:30", "branch": "A=0,B=0",
        "torus_gauge": ["b0=1", "b1=1", "b2=1", "d1=1"],
        "active_variables": list(ACTIVE_NAMES),
        "branch_polynomials": {"A": encode(A_dict), "B": encode(B_dict)},
        "literal_source_indices": list(range(6, 22)),
        "literal_source_labels": [labels[index] for index in range(6, 22)],
        "literal_source_rank_over_Q": int(matrix.rank()),
        "source_denominator_shifts": {
            str(index): list(shift) for index, _, _, shift in nonzero},
        "factor_profiles": {name: {
            "terms": len(poly), "degree": max(map(sum, poly)),
            "expanded": encode(poly)} for name, poly in factors.items()},
        "localized_factors_stage1": [
            "selected_base", "both_live_a_d", "remaining_c_numerators"],
        "explicitly_not_localized_stage1": ["H", "A"],
        "input": INPUT.name, "input_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "row_labels": [label for label, _ in labelled],
        "row_sha256": list(parsed.polynomial_sha256),
        "source_hashes": {
            "builder": digest(BUILDER_PATH), "routing": digest(ROUTING),
            "parent_interface": digest(PARENT_RESULT), "toolkit": digest(TOOLKIT)},
        "must_fire": ["strict parser", "parentheses", "A coefficient mutation",
                      "literal raw7=A*a4+B", "all 16 source rows rank16"],
        "scope_guard": (
            "This is only the closed pivot branch A=B=0. The stage-1 "
            "Rabinowitsch row contains exactly the original selected-base, "
            "both-live a*d, and remaining-c live factors. H is deliberately "
            "not localized until a positive-dimensional source-faithful "
            "stage-1 result is verified. No A-open/R25 claim is made."),
    }
    result["logical_sha256"] = logical_hash(result)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03130 A=B=0 exact export PASS", result["logical_sha256"])
    print("rows", len(labelled), "input", parsed.file_sha256)
    print("factor terms", {key: len(value) for key, value in factors.items()})


if __name__ == "__main__":
    main()
