#!/usr/bin/env python3
"""Export the full k5 interior 0:63:31, d1=d2 char0 source gate."""

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
STRUCT_DIR = HERE.parent / "unaudited-codex-face06331-structural-2026-08-21"
STRUCT = STRUCT_DIR / "export_face06331_structural.py"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
INPUT = HERE / "face06331_delta0_full_source_char0.msolve"
LABELS = HERE / "face06331_delta0_full_source_char0_labels.json"
RESULT = HERE / "results_face06331_delta0_char0_export.json"
ACTIVE = ("a0", "a1", "a2", "a3", "a4", "a5",
          "b3", "b4", "b5", "d1", "d3", "d4")
VARIABLES = ("z", *ACTIVE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


S = load("face06331_delta0_structural_source", STRUCT)
E = S.E
IO = load("face06331_delta0_msolve_io", TOOLKIT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def expression(poly, symbols):
    return sp.expand(sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(symbols, exponent, strict=True))
        for exponent, coefficient in poly.items())))


def primitive(poly, symbols):
    value = sp.Poly(sp.expand(poly), *symbols, domain=sp.QQ)
    denominator = math.lcm(*(int(coefficient.q)
                             for _, coefficient in value.terms()))
    integer = sp.Poly(value.as_expr()*denominator, *symbols, domain=sp.ZZ)
    _, answer = integer.primitive()
    if answer.LC() < 0:
        answer = -answer
    require(answer.as_expr() != 0, "zero source row")
    return answer.as_expr()


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
    context, rows, h, selected, both, c_live, full, tree = S.raw_source()
    require(tree == (0, 1, 2), "canonical gauge changed")
    parent_symbols = sp.symbols(" ".join(S.ACTIVE))
    parent = dict(zip(S.ACTIVE, parent_symbols, strict=True))
    active_symbols = sp.symbols(" ".join(ACTIVE))
    active = dict(zip(ACTIVE, active_symbols, strict=True))
    parent_indices = tuple(context.variable_names.index(name)
                           for name in S.ACTIVE)
    projected = {index: E.project(poly, context, parent_indices)
                 for index, _, poly in rows if poly}
    source_labels = {index: label for index, label, poly in rows if poly}
    source = {index: expression(poly, parent_symbols)
              for index, poly in projected.items()}
    substitution = {parent[name]: active[name] for name in ACTIVE}
    substitution[parent["d2"]] = active["d1"]
    retained = {index: primitive(poly.subs(substitution), active_symbols)
                for index, poly in source.items()}
    require(tuple(retained) == tuple(range(6, 22)),
            "literal source packet was pruned")

    a5, b5, d1 = active["a5"], active["b5"], active["d1"]
    V = sp.expand(2*a5*b5*d1-b5**2-2*b5+1)
    require(sp.expand(retained[8]-V) == 0 or
            sp.expand(retained[8]+V) == 0,
            "raw8 did not become the four-term residual")

    full_parent = E.project(full, context, parent_indices)
    full_expr = expression(full_parent, parent_symbols)
    localizer = primitive(full_expr.subs(substitution), active_symbols)
    # Retain multiplicity d1^2 inherited from original live d1*d2.
    require(sp.Poly(localizer, d1).degree() >= 2 and
            len(sp.Poly(localizer, *active_symbols).terms()) > 0,
            "original live multiplicity was lost")
    labelled = [(f"raw_{index}_{source_labels[index]}",
                 encode(retained[index], active_symbols))
                for index in retained]
    z = sp.symbols("z")
    labelled.append(("RAB_exact_original_live_delta0", encode(
        z*localizer-1, sp.symbols(" ".join(VARIABLES)))))
    INPUT.write_text(",".join(VARIABLES)+"\n0\n"+
                     ",\n".join(poly for _, poly in labelled)+"\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "raw_source_indices": list(retained),
        "branch_substitution": "d2=d1",
        "raw8_residual": encode(V, active_symbols),
        "exact_live_factorization": (
            "H_delta * (b3*b4*b5) * "
            "(a0*a1*a2*a3*a4*d1^2*d3*d4) * "
            "(1+a0)*(1+a1*d1)*(1+a2*d1)*"
            "(1+a3*d3)*(1+a4*d4)"),
    }, indent=2, sort_keys=True)+"\n")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.variables == VARIABLES and parsed.characteristic == 0 and
            len(parsed.polynomials) == 17,
            "strict char0 input interface changed")
    require(IO.polynomial_sha256("-"+labelled[0][1]) !=
            parsed.polynomial_sha256[0], "source mutation did not fire")
    require(IO.polynomial_sha256(labelled[-1][1].replace("-1", "+1")) !=
            parsed.polynomial_sha256[-1], "Rabinowitsch mutation did not fire")

    result = {
        "status": "UNAUDITED exact full-source k5 delta=0 char0 export PASS",
        "state": "0:63:31", "branch": "d1=d2",
        "variables": list(VARIABLES),
        "retained_raw_indices": list(retained),
        "retained_labels": [source_labels[index] for index in retained],
        "raw8_is_four_term_residual": True,
        "raw8_residual": encode(V, active_symbols),
        "row_profiles": [{"raw_index": index,
                          "label": source_labels[index],
                          "terms": len(sp.Poly(poly, *active_symbols).terms()),
                          "degree": int(sp.total_degree(poly))}
                         for index, poly in retained.items()],
        "localizer_terms": len(sp.Poly(localizer, *active_symbols).terms()),
        "localizer_degree": int(sp.total_degree(localizer)),
        "exact_live_factorization": json.loads(LABELS.read_text())[
            "exact_live_factorization"],
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "input_polynomial_sha256": list(parsed.polynomial_sha256),
        "source_sha256": sha256(STRUCT.read_bytes()).hexdigest(),
        "must_fire": ["raw8 four-term specialization",
                      "literal source sign mutation",
                      "Rabinowitsch constant mutation"],
        "scope_guard": ("Only d1=d2 inside k5 0:63:31 is exported. "
                        "The d1-d2!=0 branch is untouched."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("face06331 delta=0 char0 export: PASS")
    print("rows/localizer terms", len(retained), result["localizer_terms"])
    print("input", result["input_file_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
