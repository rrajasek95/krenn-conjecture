#!/usr/bin/env python3
"""Export the full 0:31:15 R=J=U=0 characteristic-zero branch."""

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
INPUT = HERE / "face03115_R_J0_full_source_char0.msolve"
LABELS = HERE / "face03115_R_J0_full_source_char0_labels.json"
RESULT = HERE / "results_face03115_R_J0_char0_export.json"
ACTIVE = ("a0", "a1", "a3", "a4", "a5", "b3", "b4", "b5",
          "d1", "d2", "d3")
VARIABLES = ("z", *ACTIVE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face03115_R_J0_parent_source", SOURCE)
IO = load("face03115_R_J0_msolve_io", TOOLKIT)


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
    pivot = parent["a2"]
    P = sp.Poly(source[16], pivot)
    Q = sp.Poly(source[11], pivot)
    A, B = map(sp.expand, P.all_coeffs())
    C, D = map(sp.expand, Q.all_coeffs())
    require(sp.expand(A-parent["b4"]*(parent["d2"]-1)) == 0,
            "raw16 pivot changed")
    R = sp.expand(A*D-B*C)

    substitution = {parent[name]: active[name] for name in ACTIVE}
    A0 = sp.expand(A.subs(substitution))
    B0 = sp.expand(B.subs(substitution))
    substitution[pivot] = -B0/A0
    R0 = primitive_numerator(R.subs(substitution), active_symbols)[0]
    require(sp.cancel(source[16].subs(substitution)) == 0,
            "raw16 did not vanish under solve")

    retained = {}
    denominators = {}
    for index in range(6, 22):
        if index == 16:
            continue
        numerator, denominator = primitive_numerator(
            source[index].subs(substitution), active_symbols)
        retained[index] = numerator
        denominators[index] = denominator
        require(all(sp.expand(factor-active["b4"]) == 0 or
                    sp.expand(factor-(active["d2"]-1)) == 0
                    for factor, _ in sp.factor_list(denominator)[1]),
                ("non-pivot denominator", index, denominator))
    require(tuple(retained) == tuple(index for index in range(6, 22)
                                     if index != 16),
            "literal source packet was pruned")
    require(sp.expand(retained[11]-R0) == 0 or
            sp.expand(retained[11]+R0) == 0,
            "raw11 did not become R")

    a3, a4, a5 = active["a3"], active["a4"], active["a5"]
    b3, b4 = active["b3"], active["b4"]
    d3 = active["d3"]
    J = sp.expand(a4*b4*d3-b3)
    U = sp.expand(2*a3*d3+a5**2*b4**2*d3**2-2*a5*b4*d3+1)
    # Raw9 must be implied by J=U=0 using only already-live b3,d3.
    F = retained[9]
    b5 = active["b5"]
    S = sp.expand(a3*a4*b4*d3+a3*b3+a4*b4+
                  a5**2*b3*b4**2*d3-2*a5*b3*b4)
    require(sp.expand(F-a5*b3*J*b5-S) == 0 and
            sp.expand(d3*S-b3*U-J*(a3*d3+1)) == 0,
            "J/U source implication changed")

    h_dict = E.project(h, context, active_indices)
    h_num = primitive_numerator(
        expression(h_dict, parent_symbols).subs(substitution),
        active_symbols)[0]
    L = active["d2"]-1
    C2 = sp.expand(A0-B0*active["d2"])
    live_factors = [
        L, h_num, active["a5"], active["b3"], active["b4"],
        active["a0"], active["a1"], B0, active["a3"], active["d1"],
        active["d2"], active["d3"], 1+active["a0"],
        1+active["a1"]*active["d1"], C2,
        1+active["a3"]*active["d3"],
    ]
    localizer = primitive_numerator(sp.prod(live_factors),
                                    active_symbols)[0]
    source_rows = [(f"raw_{index}_{source_labels[index]}", retained[index])
                   for index in retained]
    branch_rows = [("branch_J", J), ("branch_U", U)]
    z = sp.symbols("z")
    labelled = [(label, encode(poly, active_symbols))
                for label, poly in source_rows+branch_rows]
    labelled.append(("RAB_surviving_original_live_times_L", encode(
        z*localizer-1, sp.symbols(" ".join(VARIABLES)))))
    INPUT.write_text(",".join(VARIABLES)+"\n0\n"+
                     ",\n".join(poly for _, poly in labelled)+"\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "raw_source_indices": list(retained),
        "solved_raw_index": 16,
        "branch_rows": ["J", "U"],
        "substitution": {"a2": "-B/[b4*(d2-1)]"},
        "localized_factors": ["d2-1(branch guard)", "H_numerator", "a5",
            "b3", "b4", "a0", "a1", "B(a2 numerator)", "a3", "d1",
            "d2", "d3", "1+a0", "1+a1*d1", "A-B*d2(c2 numerator)",
            "1+a3*d3"],
    }, indent=2, sort_keys=True)+"\n")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.variables == VARIABLES and parsed.characteristic == 0 and
            len(parsed.polynomials) == 18,
            "strict char0 input interface changed")
    require(IO.polynomial_sha256("-"+labelled[0][1]) !=
            parsed.polynomial_sha256[0], "source mutation did not fire")
    require(IO.polynomial_sha256(labelled[-1][1].replace("-1", "+1")) !=
            parsed.polynomial_sha256[-1], "Rabinowitsch mutation did not fire")

    result = {
        "status": "UNAUDITED exact full-source R=J=U=0 char0 export PASS",
        "state": "0:31:15", "branch": "d2-1!=0,R=0,J=0,U=0",
        "variables": list(VARIABLES),
        "pivot": {"A": encode(A0, active_symbols),
                  "B": encode(B0, active_symbols), "a2": "-B/A"},
        "retained_raw_indices": list(retained),
        "retained_labels": [source_labels[index] for index in retained],
        "raw11_is_R": True, "raw9_retained_despite_JU_implication": True,
        "branch_equations": {"J": encode(J, active_symbols),
                             "U": encode(U, active_symbols)},
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
        "must_fire": ["literal source leading-sign mutation",
                      "Rabinowitsch constant mutation",
                      "raw9 J/U implication"],
        "scope_guard": ("Only J=U=0 inside d2-1!=0,R=0 is exported. "
                        "J!=0 is untouched. Finite-field conclusions are "
                        "not accepted as characteristic-zero proofs."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("face03115 R=J=U=0 char0 export: PASS")
    print("rows/localizer terms", len(labelled)-1,
          result["localizer_terms"])
    print("input", result["input_file_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
