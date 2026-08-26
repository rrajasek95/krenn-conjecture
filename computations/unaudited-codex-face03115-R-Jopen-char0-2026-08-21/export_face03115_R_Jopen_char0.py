#!/usr/bin/env python3
"""Export the full 0:31:15 R=0,J!=0 characteristic-zero branch."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PARENT = HERE.parent / "unaudited-codex-face03115-modular-lead-2026-08-21"
SOURCE = PARENT / "export_face03115_base12_f4sat.py"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
INPUT = HERE / "face03115_R_Jopen_full_source_char0.msolve"
LABELS = HERE / "face03115_R_Jopen_full_source_char0_labels.json"
RESULT = HERE / "results_face03115_R_Jopen_char0_export.json"
ACTIVE = ("a0", "a1", "a3", "a4", "a5", "b3", "b4", "d1", "d2", "d3")
VARIABLES = ("z", *ACTIVE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face03115_R_Jopen_parent_source", SOURCE)
IO = load("face03115_R_Jopen_msolve_io", TOOLKIT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def expression(poly, symbols):
    return sp.expand(sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(symbols, exponent, strict=True))
        for exponent, coefficient in poly.items())))


def primitive_numerator(poly, symbols):
    numerator, denominator = sp.fraction(sp.cancel(poly))
    value = sp.Poly(sp.expand(numerator), *symbols, domain=sp.QQ)
    common = math.lcm(*(int(coefficient.q)
                        for _, coefficient in value.terms()))
    integer = sp.Poly(value.as_expr()*common, *symbols, domain=sp.ZZ)
    _, answer = integer.primitive()
    if answer.LC() < 0:
        answer = -answer
    return answer.as_expr(), sp.factor(denominator)


def encode(poly, symbols):
    pieces = []
    for position, (exponent, coefficient) in enumerate(
            sp.Poly(sp.expand(poly), *symbols, domain=sp.ZZ).terms()):
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
    encoded = "".join(pieces)
    require(encoded and "(" not in encoded and ")" not in encoded and
            "**" not in encoded, "noncanonical msolve syntax")
    return encoded


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    context, rows, h, *_ = E.raw_source()
    parent_symbols = sp.symbols(" ".join(E.ACTIVE_NAMES))
    parent = dict(zip(E.ACTIVE_NAMES, parent_symbols, strict=True))
    active_symbols = sp.symbols(" ".join(ACTIVE))
    active = dict(zip(ACTIVE, active_symbols, strict=True))
    active_indices = tuple(context.variable_names.index(name)
                           for name in E.ACTIVE_NAMES)
    projected = {index: E.project(poly, context, active_indices)
                 for index, _, poly in rows if poly}
    source_labels = {index: label for index, label, poly in rows if poly}
    source = {index: expression(poly, parent_symbols)
              for index, poly in projected.items()}

    a2 = parent["a2"]
    P = sp.Poly(source[16], a2)
    Q = sp.Poly(source[11], a2)
    A, B = map(sp.expand, P.all_coeffs())
    C, D = map(sp.expand, Q.all_coeffs())
    require(sp.expand(A-parent["b4"]*(parent["d2"]-1)) == 0,
            "raw16 pivot changed")
    R = sp.expand(A*D-B*C)
    first = {parent[name]: active[name] for name in ACTIVE}
    # b5 is eliminated only after the a2 substitution.
    first[parent["b5"]] = parent["b5"]
    A0 = sp.expand(A.subs(first))
    B0 = sp.expand(B.subs(first))
    first[a2] = -B0/A0

    raw9_first = primitive_numerator(source[9].subs(first),
                                     (*active_symbols, parent["b5"]))[0]
    a3, a4, a5 = active["a3"], active["a4"], active["a5"]
    b3, b4 = active["b3"], active["b4"]
    d3 = active["d3"]
    J = sp.expand(a4*b4*d3-b3)
    S = sp.expand(a3*a4*b4*d3+a3*b3+a4*b4+
                  a5**2*b3*b4**2*d3-2*a5*b3*b4)
    require(sp.expand(raw9_first-a5*b3*J*parent["b5"]-S) == 0,
            "raw9 b5 identity changed")
    b5_solution = -S/(a5*b3*J)
    substitution = dict(first)
    substitution[parent["b5"]] = b5_solution
    require(sp.cancel(source[16].subs(substitution)) == 0 and
            sp.cancel(source[9].subs(substitution)) == 0,
            "two solved source rows did not vanish")

    retained = {}
    denominators = {}
    allowed_denominators = (active["b4"], active["d2"]-1,
                            active["a5"], active["b3"], J)
    for index in range(6, 22):
        if index in (9, 16):
            continue
        numerator, denominator = primitive_numerator(
            source[index].subs(substitution), active_symbols)
        retained[index] = numerator
        denominators[index] = denominator
        require(all(any(sp.expand(factor-live) == 0
                        for live in allowed_denominators)
                    for factor, _ in sp.factor_list(denominator)[1]),
                ("non-live solve denominator", index, denominator))
    require(tuple(retained) == tuple(index for index in range(6, 22)
                                     if index not in (9, 16)),
            "literal source packet was pruned")
    R_after = primitive_numerator(R.subs(substitution), active_symbols)[0]
    require(sp.cancel(R.subs(substitution) /
                      source[11].subs(substitution)-A0) == 0,
            "exact A*raw11=R relation changed")

    h_dict = E.project(h, context, active_indices)
    h_num = primitive_numerator(
        expression(h_dict, parent_symbols).subs(substitution),
        active_symbols)[0]
    L = active["d2"]-1
    C2 = sp.expand(A0-B0*active["d2"])
    live_factors = [
        L, J, h_num, active["a5"], active["b3"], active["b4"],
        active["a0"], active["a1"], B0, active["a3"], active["d1"],
        active["d2"], active["d3"], 1+active["a0"],
        1+active["a1"]*active["d1"], C2,
        1+active["a3"]*active["d3"],
    ]
    localizer = primitive_numerator(sp.prod(live_factors),
                                    active_symbols)[0]
    source_rows = [(f"raw_{index}_{source_labels[index]}", retained[index])
                   for index in retained]
    z = sp.symbols("z")
    labelled = [(label, encode(poly, active_symbols))
                for label, poly in source_rows]
    labelled.append(("RAB_surviving_original_live_times_LJ", encode(
        z*localizer-1, sp.symbols(" ".join(VARIABLES)))))
    INPUT.write_text(",".join(VARIABLES)+"\n0\n"+
                     ",\n".join(poly for _, poly in labelled)+"\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "raw_source_indices": list(retained),
        "solved_raw_indices": [9, 16],
        "substitution": {"a2": "-B/[b4*(d2-1)]",
                         "b5": "-S/(a5*b3*J)"},
        "localized_factors": ["d2-1(branch guard)", "J(branch guard)",
            "H_numerator", "a5", "b3", "b4", "a0", "a1",
            "B(a2 numerator)", "a3", "d1", "d2", "d3", "1+a0",
            "1+a1*d1", "A-B*d2(c2 numerator)", "1+a3*d3"],
    }, indent=2, sort_keys=True)+"\n")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.variables == VARIABLES and parsed.characteristic == 0 and
            len(parsed.polynomials) == 15,
            "strict char0 input interface changed")
    require(IO.polynomial_sha256("-"+labelled[0][1]) !=
            parsed.polynomial_sha256[0], "source mutation did not fire")
    require(IO.polynomial_sha256(labelled[-1][1].replace("-1", "+1")) !=
            parsed.polynomial_sha256[-1], "Rabinowitsch mutation did not fire")

    result = {
        "status": "UNAUDITED exact full-source R=0,J!=0 char0 export PASS",
        "state": "0:31:15", "branch": "d2-1!=0,R=0,J!=0",
        "variables": list(VARIABLES),
        "substitutions": {"a2": "-B/[b4*(d2-1)]",
                          "b5": "-S/(a5*b3*J)"},
        "J": encode(J, active_symbols), "S": encode(S, active_symbols),
        "retained_raw_indices": list(retained),
        "retained_labels": [source_labels[index] for index in retained],
        "solved_raw_indices": [9, 16],
        "raw11_transformed_R_relation": (
            "A*raw11=R exactly; primitive numerators may cancel live A"),
        "row_profiles": [{"raw_index": index,
                          "label": source_labels[index],
                          "terms": len(sp.Poly(poly, *active_symbols).terms()),
                          "degree": int(sp.total_degree(poly)),
                          "cleared_denominator": str(denominators[index]).replace(
                              "**", "^")}
                         for index, poly in retained.items()],
        "localizer_terms": len(sp.Poly(localizer, *active_symbols).terms()),
        "localizer_degree": int(sp.total_degree(localizer)),
        "localized_factors": json.loads(LABELS.read_text())[
            "localized_factors"],
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "input_polynomial_sha256": list(parsed.polynomial_sha256),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "must_fire": ["raw16 solve", "raw9 b5 solve",
                      "literal source sign mutation",
                      "Rabinowitsch constant mutation"],
        "scope_guard": ("Only J!=0 inside d2-1!=0,R=0 is exported. "
                        "The d2=1 and J=0 branches are untouched."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("face03115 R=0,J!=0 char0 export: PASS")
    print("rows/localizer terms", len(retained), result["localizer_terms"])
    print("input", result["input_file_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
