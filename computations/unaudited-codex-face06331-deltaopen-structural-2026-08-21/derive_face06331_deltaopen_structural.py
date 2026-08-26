#!/usr/bin/env python3
"""Structural reduction of k5 interior 0:63:31 on d1-d2 != 0."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
STRUCT_DIR = HERE.parent / "unaudited-codex-face06331-structural-2026-08-21"
STRUCT = STRUCT_DIR / "export_face06331_structural.py"
OUT = HERE / "results_face06331_deltaopen_structural.json"
ACTIVE = ("a0", "a2", "a3", "a4", "a5", "b3", "b4", "b5",
          "d1", "d2", "d3", "d4")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


S = load("face06331_deltaopen_parent", STRUCT)
E = S.E


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
    return "".join(pieces)


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
    labels = {index: label for index, label, poly in rows if poly}
    source = {index: expression(poly, parent_symbols)
              for index, poly in projected.items()}

    pivot = parent["a1"]
    raw8 = sp.Poly(source[8], pivot)
    require(raw8.degree() == 1, "raw8 stopped being linear in a1")
    coefficient, constant = map(sp.expand, raw8.all_coeffs())
    substitution = {parent[name]: active[name] for name in ACTIVE}
    delta = sp.expand(coefficient.subs(substitution))
    K = sp.expand(constant.subs(substitution))
    require(sp.expand(delta-(active["d1"]-active["d2"])) == 0,
            "delta pivot changed")
    substitution[pivot] = -K/delta
    require(sp.cancel(source[8].subs(substitution)) == 0,
            "raw8 did not vanish after solve")

    reduced = {}
    denominators = {}
    for index in range(6, 22):
        if index == 8:
            continue
        numerator, denominator = primitive_numerator(
            source[index].subs(substitution), active_symbols)
        reduced[index] = numerator
        denominators[index] = denominator
        require(all(sp.expand(factor-delta) == 0
                    for factor, _ in sp.factor_list(denominator)[1]),
                ("non-delta denominator", index, denominator))
    require(tuple(reduced) == tuple(index for index in range(6, 22)
                                    if index != 8),
            "literal source packet was pruned")

    # Original a1 and 1+a1*d1 liveness become K and delta-K*d1.
    C1 = sp.expand(delta-K*active["d1"])
    full_parent = expression(E.project(full, context, parent_indices),
                             parent_symbols)
    live_numerator = primitive_numerator(
        full_parent.subs(substitution), active_symbols)[0]
    localizer = sp.expand(delta*live_numerator)
    require(sp.rem(sp.Poly(live_numerator, *active_symbols),
                   sp.Poly(K, *active_symbols)) == 0 and
            sp.rem(sp.Poly(live_numerator, *active_symbols),
                   sp.Poly(C1, *active_symbols)) == 0,
            "transformed a1/c1 live numerators were lost")

    profiles = []
    candidates = []
    for index, poly in reduced.items():
        content, factors = sp.factor_list(poly)
        row = {"raw_index": index, "label": labels[index],
               "terms": len(sp.Poly(poly, *active_symbols).terms()),
               "degree": int(sp.total_degree(poly)),
               "denominator": str(denominators[index]).replace("**", "^"),
               "factor_content": int(content), "factors": []}
        for factor, exponent in factors:
            factor_record = {
                "polynomial": encode(factor, active_symbols),
                "terms": len(sp.Poly(factor, *active_symbols).terms()),
                "degree": int(sp.total_degree(factor)),
                "exponent": int(exponent),
                "matches_transformed_live": [name for name, live in
                    (("K(a1 numerator)", K), ("delta-K*d1(c1 numerator)", C1),
                     ("delta", delta))
                    if sp.expand(factor-live) == 0 or
                       sp.expand(factor+live) == 0],
            }
            row["factors"].append(factor_record)
            if not factor_record["matches_transformed_live"]:
                candidates.append((factor_record["terms"],
                                   factor_record["degree"], index,
                                   factor_record))
        profiles.append(row)
    profiles.sort(key=lambda row: (min(f["terms"] for f in row["factors"]),
                                   row["terms"], row["raw_index"]))
    candidates.sort(key=lambda value: value[:3])
    terms, degree, best_index, best = candidates[0]

    # Literal reconstruction of the best factor product.
    best_row = next(row for row in profiles if row["raw_index"] == best_index)
    rebuilt = sp.Integer(best_row["factor_content"])
    for factor in best_row["factors"]:
        decoded = sp.sympify(factor["polynomial"].replace("^", "**"),
                             locals=active)
        rebuilt *= decoded**factor["exponent"]
    require(sp.expand(rebuilt-reduced[best_index]) == 0,
            "shortest factor replay failed")
    require(best_index == 9, "shortest source row changed")
    a3, a4, a5 = active["a3"], active["a4"], active["a5"]
    b3, b4, b5 = active["b3"], active["b4"], active["b5"]
    d3, d4 = active["d3"], active["d4"]
    F = reduced[9]
    Pminor = sp.expand(b3*d4-b4*d3)
    Qminor = sp.expand(b3*d4+b4*d3)
    W = sp.expand(b3**2*b5**2+2*b3*b4*b5-b4**2)
    closed = sp.expand(-2*a5*b3*b4**2*b5*d3+W)
    require(sp.expand(F-Pminor*(a3*b4+a4*b3*b5**2)+
                      a5*b3*b4*b5*Qminor-W) == 0 and
            sp.expand(Qminor-2*b4*d3-Pminor) == 0,
            "raw9 minor split identities failed")

    result = {
        "status": "UNAUDITED exact delta-open structural reduction PASS",
        "state": "0:63:31", "branch": "d1-d2!=0",
        "variables": list(ACTIVE),
        "pivot": {"raw_index": 8, "variable": "a1",
                  "delta": encode(delta, active_symbols),
                  "K": encode(K, active_symbols), "a1": "-K/delta"},
        "retained_raw_indices": list(reduced),
        "reduced_profiles": profiles,
        "transformed_live": {"delta(branch guard)": encode(delta,
                                                               active_symbols),
                             "K(a1 numerator)": encode(K, active_symbols),
                             "delta-K*d1(c1 numerator)": encode(C1,
                                                                 active_symbols)},
        "localizer_terms": len(sp.Poly(localizer, *active_symbols).terms()),
        "localizer_degree": int(sp.total_degree(localizer)),
        "shortest_new_consistency_factor": {
            "source_raw_index": best_index, "source_label": labels[best_index],
            "factor_terms": terms, "factor_degree": degree,
            "factor": best["polynomial"],
            "complete_factorization": best_row["factors"],
        },
        "shortest_sound_minor_split": {
            "P": encode(Pminor, active_symbols),
            "Q": encode(Qminor, active_symbols),
            "W": encode(W, active_symbols),
            "identity": (
                "raw9=P*(a3*b4+a4*b3*b5^2)-"
                "a5*b3*b4*b5*Q+W"),
            "relation": "Q=2*b4*d3+P",
            "P_nonzero": "live b4 makes raw9 solve a3",
            "P_zero_residual": encode(closed, active_symbols),
            "P_zero_residual_terms": 4,
        },
        "source_sha256": sha256(STRUCT.read_bytes()).hexdigest(),
        "must_fire": ["raw8 pivot solve", "delta-only denominators",
                      "K and delta-K*d1 retained in live product",
                      "shortest factor product replay"],
        "scope_guard": ("Structural export only. No solver was launched. "
                        "The d1=d2 branch is excluded."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("face06331 delta-open structural: PASS")
    print("rows/localizer", len(reduced), result["localizer_terms"])
    print("shortest", best_index, terms, degree, best["polynomial"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
