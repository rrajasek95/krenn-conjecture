#!/usr/bin/env python3
"""Export the full normalized 0:31:15 source on the d2=1 branch.

Raw16 becomes K*b4-N=0, where

    t=a5*(d1+1),  K=t+1,  N=t-1.

K=0 is incompatible with raw16 in characteristic zero, so the branch is
faithfully parametrized by b4=N/K.  Every one of the other fifteen literal
raw rows is retained after numerator clearing.  The Rabinowitsch product is
exactly the surviving original live factors, together with K solely as the
forced denominator guard.
"""

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
INPUT = HERE / "face03115_d2eq1_full_source_char0.msolve"
LABELS = HERE / "face03115_d2eq1_full_source_char0_labels.json"
RESULT = HERE / "results_face03115_d2eq1_char0_export.json"
ACTIVE = ("a0", "a1", "a2", "a3", "a4", "a5", "b3", "b5", "d1", "d3")
VARIABLES = ("z", *ACTIVE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face03115_d2eq1_parent_source", SOURCE)
IO = load("face03115_d2eq1_msolve_io", TOOLKIT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def parent_expression(poly, symbols):
    return sp.expand(sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(symbols, exponent, strict=True))
        for exponent, coefficient in poly.items())))


def primitive(poly, symbols):
    value = sp.Poly(sp.expand(poly), *symbols, domain=sp.QQ)
    denominator = math.lcm(*(int(coefficient.q)
                             for _, coefficient in value.terms()))
    integer = sp.Poly(value.as_expr()*denominator, *symbols, domain=sp.ZZ)
    content, primitive_poly = integer.primitive()
    require(content != 0 and primitive_poly.as_expr() != 0,
            "zero polynomial escaped source branch")
    if primitive_poly.LC() < 0:
        primitive_poly = -primitive_poly
    return primitive_poly.as_expr()


def numerator_after_substitution(poly, parent_symbols, active_symbols,
                                 substitutions, K):
    value = sp.cancel(poly.subs(substitutions))
    numerator, denominator = map(sp.expand, sp.fraction(value))
    require(not denominator.has(*[symbol for symbol in parent_symbols
                                  if symbol not in active_symbols]),
            "substituted denominator escaped active variables")
    factors = sp.factor_list(denominator)[1]
    require(all(sp.expand(factor-K) == 0 for factor, _ in factors),
            ("non-K denominator after b4 substitution", denominator))
    return primitive(numerator, active_symbols)


def encode(poly, symbols):
    terms = sp.Poly(sp.expand(poly), *symbols, domain=sp.ZZ).terms()
    pieces = []
    for position, (exponent, coefficient) in enumerate(terms):
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
    labels = {index: label for index, label, poly in rows if poly}
    source = {index: parent_expression(poly, parent_symbols)
              for index, poly in projected.items()}

    t = active["a5"]*(active["d1"]+1)
    K = sp.expand(t+1)
    N = sp.expand(t-1)
    substitutions = {parent[name]: active[name] for name in ACTIVE}
    substitutions[parent["d2"]] = 1
    substitutions[parent["b4"]] = N/K

    relation = sp.expand(source[16].subs(parent["d2"], 1))
    require(sp.expand(relation-(parent["b4"]*(
        parent["a5"]*(parent["d1"]+1)+1)-(
            parent["a5"]*(parent["d1"]+1)-1))) == 0,
            "raw16 short relation changed")
    require(sp.cancel(relation.subs(parent["b4"], N/K)) == 0,
            "raw16 parametrization changed")
    # If K=0 then t=-1, N=-2 and raw16=2, so K is forced live on raw16=0.
    Kp = parent["a5"]*(parent["d1"]+1)+1
    require(sp.expand(relation-Kp*(parent["b4"]-1)-2) == 0,
            "forced-denominator must-fire changed")

    retained = {}
    for index in range(6, 22):
        value = sp.cancel(source[index].subs(substitutions))
        if index == 16:
            require(value == 0, "raw16 did not vanish after its own solve")
            continue
        retained[index] = numerator_after_substitution(
            source[index], parent_symbols, active_symbols, substitutions, K)
    require(tuple(retained) == tuple(index for index in range(6, 22)
                                     if index != 16),
            "full literal source packet was pruned")

    h_parent = E.project(h, context, active_indices)
    h_expr = parent_expression(h_parent, parent_symbols)
    h_num = numerator_after_substitution(
        h_expr, parent_symbols, active_symbols, substitutions, K)
    original_live = [
        h_num, active["a5"], active["b3"], N,
        active["a0"], active["a1"], active["a2"], active["a3"],
        active["d1"], active["d3"], 1+active["a0"],
        1+active["a1"]*active["d1"], 1+active["a2"],
        1+active["a3"]*active["d3"],
    ]
    localizer = primitive(K*sp.prod(original_live), active_symbols)
    labelled = [(f"raw_{index}_{labels[index]}",
                 encode(retained[index], active_symbols))
                for index in retained]
    rab = sp.expand(sp.symbols("z")*localizer-1)
    labelled.append(("RAB_surviving_original_live_times_K", encode(
        rab, sp.symbols(" ".join(VARIABLES)))))
    INPUT.write_text(",".join(VARIABLES) + "\n0\n" +
                     ",\n".join(poly for _, poly in labelled) + "\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "raw_source_indices": list(retained),
        "eliminated_raw_index": 16,
        "substitution": {"d2": "1", "b4": "N/K",
                         "K": str(K), "N": str(N)},
        "localized_factors": ["K(forced denominator)", "H_numerator",
            "a5", "b3", "N(b4 numerator)", "a0", "a1", "a2", "a3",
            "d1", "d3", "1+a0", "1+a1*d1", "1+a2", "1+a3*d3"],
    }, indent=2, sort_keys=True) + "\n")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.variables == VARIABLES and parsed.characteristic == 0 and
            len(parsed.polynomials) == 16,
            "strict char0 input interface changed")
    mutated = list(labelled)
    mutated[0] = (mutated[0][0], "-" + mutated[0][1]
                  if not mutated[0][1].startswith("-") else
                  mutated[0][1][1:])
    require(IO.polynomial_sha256(mutated[0][1]) !=
            parsed.polynomial_sha256[0], "source mutation did not fire")
    require(IO.polynomial_sha256(labelled[-1][1].replace("-1", "+1")) !=
            parsed.polynomial_sha256[-1], "Rabinowitsch mutation did not fire")

    result = {
        "status": "UNAUDITED exact full-source d2=1 char0 export PASS",
        "state": "0:31:15", "branch": "d2=1",
        "variables": list(VARIABLES),
        "substitution": {"d2": "1", "t": str(t), "K": str(K),
                         "N": str(N), "b4": "N/K"},
        "forced_denominator_proof": "K=0 => t=-1,N=-2,raw16=2",
        "retained_raw_indices": list(retained),
        "retained_labels": [labels[index] for index in retained],
        "row_profiles": [{"raw_index": index, "label": labels[index],
                          "terms": len(sp.Poly(retained[index],
                                                *active_symbols).terms()),
                          "degree": int(sp.total_degree(retained[index]))}
                         for index in retained],
        "restored_previously_omitted": list(E.OMITTED),
        "localizer_terms": len(sp.Poly(localizer, *active_symbols).terms()),
        "localizer_degree": int(sp.total_degree(localizer)),
        "localized_factors": json.loads(LABELS.read_text())[
            "localized_factors"],
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "input_polynomial_sha256": list(parsed.polynomial_sha256),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "must_fire": ["raw16 relation solve", "K=0 gives raw16=2",
                      "source leading-sign mutation",
                      "Rabinowitsch constant mutation"],
        "scope_guard": ("Only the d2=1 branch is exported. K is localized "
                        "solely because it is the forced denominator of the "
                        "raw16 parametrization. The irreducible R=0 branch "
                        "is untouched."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03115 d2=1 full-source char0 export: PASS")
    print("rows/localizer terms", len(retained), result["localizer_terms"])
    print("input", result["input_file_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
