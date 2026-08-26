#!/usr/bin/env python3
"""Exact fraction-free structural reduction of the 0:31:15 R=0 branch."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-face03115-modular-lead-2026-08-21"
SOURCE = PARENT / "export_face03115_base12_f4sat.py"
RESULTANT_SOURCE = PARENT / "derive_face03115_raw16_raw11_resultant.py"
OUT = HERE / "results_face03115_R_branch_reduction.json"
ACTIVE = ("a0", "a1", "a3", "a4", "a5", "b3", "b4", "b5",
          "d1", "d2", "d3")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face03115_R_parent_source", SOURCE)


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
    source = {index: expression(poly, parent_symbols)
              for index, poly in projected.items()}

    pivot = parent["a2"]
    P = sp.Poly(source[16], pivot)
    Q = sp.Poly(source[11], pivot)
    require(P.degree() == Q.degree() == 1,
            "frozen raw16/raw11 linear pair changed")
    A, B = map(sp.expand, P.all_coeffs())
    C, D = map(sp.expand, Q.all_coeffs())
    require(sp.expand(A-parent["b4"]*(parent["d2"]-1)) == 0,
            "pivot coefficient changed")
    R = sp.expand(A*D-B*C)
    factor_coefficient, factors = sp.factor_list(R)
    require(len(factors) == 1 and factors[0][1] == 1,
            "frozen irreducible R changed")

    substitution = {parent[name]: active[name] for name in ACTIVE}
    A0, B0 = sp.expand(A.subs(substitution)), sp.expand(B.subs(substitution))
    substitution[pivot] = -B0/A0
    R0 = primitive_numerator(R.subs(substitution), active_symbols)[0]
    require(len(sp.Poly(R0, *active_symbols).terms()) == 29 and
            sp.total_degree(R0) == 6,
            "R profile changed after dropping a2")
    require(sp.cancel(source[16].subs(substitution)) == 0,
            "raw16 did not vanish under its solve")
    q_num, q_den = primitive_numerator(source[11].subs(substitution),
                                       active_symbols)
    require(sp.expand(q_num-R0) == 0 or sp.expand(q_num+R0) == 0,
            "raw11 did not reduce to R")

    reduced = {}
    denominators = {}
    for index in range(6, 22):
        if index in (11, 16):
            continue
        numerator, denominator = primitive_numerator(
            source[index].subs(substitution), active_symbols)
        reduced[index] = numerator
        denominators[index] = denominator
        # Every denominator must be a power of the already-live A=b4(d2-1).
        quotient = sp.cancel(denominator / A0**sp.Poly(
            denominator, *active_symbols).total_degree())
        require(not denominator.has(parent["a2"]),
                "a2 survived a denominator")
        require(all(sp.expand(factor-active["b4"]) == 0 or
                    sp.expand(factor-(active["d2"]-1)) == 0
                    for factor, _ in sp.factor_list(denominator)[1]),
                ("non-A denominator", index, denominator, quotient))

    # The original a2 and (1+a2*d2) live factors become B and A-B*d2;
    # signs are immaterial for localization.  These help distinguish genuine
    # new factors from invertible source remnants.
    live_polynomials = {
        "b4": active["b4"], "d2-1": active["d2"]-1,
        "B(a2 numerator)": B0,
        "A-B*d2(c2 numerator)": sp.expand(A0-B0*active["d2"]),
        "a0": active["a0"], "a1": active["a1"], "a3": active["a3"],
        "a5": active["a5"], "b3": active["b3"],
        "d1": active["d1"], "d2": active["d2"], "d3": active["d3"],
        "1+a0": 1+active["a0"],
        "1+a1*d1": 1+active["a1"]*active["d1"],
        "1+a3*d3": 1+active["a3"]*active["d3"],
    }
    profiles = []
    for index, poly in reduced.items():
        coefficient, factor_list = sp.factor_list(poly)
        profiles.append({
            "raw_index": index, "label": labels[index],
            "terms": len(sp.Poly(poly, *active_symbols).terms()),
            "degree": int(sp.total_degree(poly)),
            "denominator": str(denominators[index]).replace("**", "^"),
            "factor_content": int(coefficient),
            "factors": [{"polynomial": encode(factor, active_symbols),
                         "terms": len(sp.Poly(factor, *active_symbols).terms()),
                         "degree": int(sp.total_degree(factor)),
                         "exponent": int(exponent),
                         "matches_declared_live": [name for name, live in
                            live_polynomials.items()
                            if sp.expand(factor-live) == 0 or
                               sp.expand(factor+live) == 0]}
                        for factor, exponent in factor_list],
        })
    profiles.sort(key=lambda row: (min(factor["terms"]
                                      for factor in row["factors"]),
                                   row["terms"], row["raw_index"]))

    # Select the shortest genuinely new irreducible factor.  This is a
    # source consequence on the open branch, not an ideal computation.
    candidates = []
    for row in profiles:
        for factor in row["factors"]:
            if not factor["matches_declared_live"]:
                candidates.append((factor["terms"], factor["degree"],
                                   row["raw_index"], factor))
    candidates.sort(key=lambda item: item[:3])
    best_terms, best_degree, best_index, best = candidates[0]
    best_row = next(row for row in profiles if row["raw_index"] == best_index)

    # The shortest equation has a particularly small sound split.  Since
    # a5,b3,b4,d3 are already live, J!=0 solves b5; J=0 leaves the four-term
    # U.  The second identity proves the closed-branch reduction without a
    # division by J.
    require(best_index == 9, "shortest source row changed")
    a3, a4, a5 = active["a3"], active["a4"], active["a5"]
    b3, b4, b5 = active["b3"], active["b4"], active["b5"]
    d3 = active["d3"]
    F = reduced[9]
    J = sp.expand(a4*b4*d3-b3)
    S = sp.expand(a3*a4*b4*d3+a3*b3+a4*b4+
                  a5**2*b3*b4**2*d3-2*a5*b3*b4)
    U = sp.expand(2*a3*d3+1+a5**2*b4**2*d3**2-2*a5*b4*d3)
    require(sp.expand(F-a5*b3*J*b5-S) == 0 and
            sp.expand(d3*S-b3*U-J*(a3*d3+1)) == 0,
            "raw9 J-split identities failed")
    require(len(sp.Poly(J, *active_symbols).terms()) == 2 and
            len(sp.Poly(U, *active_symbols).terms()) == 4,
            "J/U short profiles changed")

    # Exact factor-product replay and two mutations.
    rebuilt = sp.Integer(best_row["factor_content"])
    for factor in best_row["factors"]:
        decoded = sp.sympify(factor["polynomial"].replace("^", "**"),
                             locals=active)
        rebuilt *= decoded**factor["exponent"]
    require(sp.expand(rebuilt-reduced[best_index]) == 0,
            "shortest factorization replay failed")
    require(sp.expand(A0-active["b4"]*(active["d2"]+1)) != 0 and
            sp.expand(A0*D.subs(substitution)+B0*C.subs(substitution)-R0)
            != 0, "must-fire mutation failed")

    result = {
        "status": "UNAUDITED exact fraction-free R-branch reduction PASS",
        "state": "0:31:15", "branch": "d2-1 != 0, R=0",
        "variables": list(ACTIVE),
        "pivot": {"equation": "raw16=A*a2+B", "A": encode(A0, active_symbols),
                  "B": encode(B0, active_symbols), "a2": "-B/A"},
        "imposed_resultant": {"terms": 29, "degree": 6,
                              "polynomial": encode(R0, active_symbols)},
        "raw11_reduction": "primitive numerator is +/-R",
        "removed_as_identities_mod_R": [11, 16],
        "reduced_profiles": profiles,
        "declared_live_after_substitution": {
            name: encode(poly, active_symbols)
            for name, poly in live_polynomials.items()},
        "shortest_new_consistency_factor": {
            "source_raw_index": best_index,
            "source_label": labels[best_index],
            "source_numerator_terms": best_row["terms"],
            "factor_terms": best_terms, "factor_degree": best_degree,
            "factor": best["polynomial"],
            "complete_factorization": best_row["factors"],
        },
        "shortest_sound_factor_split": {
            "J": encode(J, active_symbols),
            "S": encode(S, active_symbols),
            "U": encode(U, active_symbols),
            "identity_1": "raw9=a5*b3*J*b5+S",
            "identity_2": "d3*S=b3*U+J*(a3*d3+1)",
            "open_J_branch": (
                "J!=0: live a5*b3 makes raw9 solve "
                "b5=-S/(a5*b3*J)"),
            "closed_J_branch": (
                "J=0: live b3,d3 make raw9=0 equivalent to U=0; "
                "U is the four-term residual"),
        },
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "resultant_source_sha256": sha256(
            RESULTANT_SOURCE.read_bytes()).hexdigest(),
        "must_fire": ["d2-1 changed to d2+1",
                      "resultant cross-term sign mutation"],
        "scope_guard": ("This is exact substitution, numerator clearing, "
                        "and factorization only. No GB/F4SAT/msolve was run, "
                        "and no emptiness or radical claim is made."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("face03115 R-branch reduction: PASS")
    print("shortest", best_index, best_terms, best_degree,
          best["polynomial"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
