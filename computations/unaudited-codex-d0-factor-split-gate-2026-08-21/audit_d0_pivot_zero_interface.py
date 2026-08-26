#!/usr/bin/env python3
"""Minimal exact interface for C0!=0 and the selected Cramer pivot zero.

Only the two selected literal rows are used.  No division by their coefficient
minor and no Groebner basis computation occurs.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SOURCE = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
          "probe_branch0_cycle_d0_c0_generic.py")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load():
    spec = importlib.util.spec_from_file_location("d0_pivot_zero_literal_source", SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    require(spec.loader is not None, "missing source loader")
    spec.loader.exec_module(module)
    return module


def encode(sp, value):
    return str(sp.expand(value)).replace("**", "^")


def digest_text(value):
    return sha256(value.encode()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def profile(sp, value, variables):
    poly = sp.Poly(value, *variables)
    return {"terms": len(poly.terms()), "total_degree": int(poly.total_degree()),
            "multidegree": [int(poly.degree(variable)) for variable in variables],
            "sha256": digest_text(encode(sp, poly.as_expr()))}


def primitive(sp, value, variables):
    return sp.primitive(sp.Poly(sp.expand(value), *variables))[1].as_expr()


def factor_records(sp, value, variables):
    content, factors = sp.factor_list(value)
    return {
        "content": int(content),
        "factors": [{"multiplicity": int(multiplicity),
                     "profile": profile(sp, factor, variables),
                     "polynomial": encode(sp, factor)}
                    for factor, multiplicity in factors],
    }


def main():
    P = load()
    sp = P.sp
    variables, residual, c0 = P.derive()
    b0, d1, d4, a0, a5 = variables
    variables3 = (b0, d1, d4)
    labels = [label for label, _ in residual]
    require(labels[1] == "t_013" and labels[4] == "cofactor_0_3",
            "selected literal row labels changed")
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    rows = [1, 4]
    pivot = primitive(sp, matrix[rows, :].det(), variables3)
    consistency_a0 = primitive(sp,
        sp.Matrix([[matrix[1, 0], rhs[1]],
                   [matrix[4, 0], rhs[4]]]).det(), variables3)
    consistency_a5 = primitive(sp,
        sp.Matrix([[matrix[1, 1], rhs[1]],
                   [matrix[4, 1], rhs[4]]]).det(), variables3)

    pivot_factors = factor_records(sp, pivot, variables3)
    require(len(pivot_factors["factors"]) == 8,
            "cleared selected-pivot factor count changed")
    # Declared Laurent/C0 factors are b0,d1,d4,C0.  Four further factors
    # remain on the honest C0!=0 pivot-zero face.
    residual_pivot_factors = []
    declared = {encode(sp, b0), encode(sp, d1), encode(sp, d4), encode(sp, c0)}
    for record in pivot_factors["factors"]:
        if record["polynomial"] not in declared:
            residual_pivot_factors.append(record)
    require(len(residual_pivot_factors) == 4,
            "wrong number of nonlive selected-pivot factors")

    candidates = [("a0_rhs_minor", consistency_a0),
                  ("a5_rhs_minor", consistency_a5)]
    candidates.sort(key=lambda item: len(sp.Poly(item[1], *variables3).terms()))
    smallest_label, smallest = candidates[0]
    common = sp.gcd(sp.Poly(consistency_a0, *variables3),
                    sp.Poly(consistency_a5, *variables3))
    pivot_common = sp.gcd(sp.Poly(pivot, *variables3), common)

    result = {
        "status": "exact D0 C0-open pivot-zero minimal interface PASS",
        "source": {"path": str(SOURCE),
                   "sha256": sha256(SOURCE.read_bytes()).hexdigest()},
        "endpoint_solve_scope": ("four upper cofactors, D0=0, and the two "
                                 "endpoint cofactors only; C0 is assumed nonzero"),
        "selected_rows": [{"index": 1, "label": labels[1]},
                          {"index": 4, "label": labels[4]}],
        "coefficient_pivot": {
            "profile": profile(sp, pivot, variables3),
            "factorization": pivot_factors,
            "C0_open_residual_factors": residual_pivot_factors,
        },
        "forced_consistency_minors": [
            {"label": label, "profile": profile(sp, value, variables3),
             "factorization": factor_records(sp, value, variables3),
             "polynomial": encode(sp, value)}
            for label, value in candidates],
        "smallest_forced_minor": smallest_label,
        "two_consistency_minor_gcd": {
            "profile": profile(sp, common.as_expr(), variables3),
            "polynomial": encode(sp, common.as_expr()),
        },
        "pivot_and_consistency_gcd": {
            "profile": profile(sp, pivot_common.as_expr(), variables3),
            "polynomial": encode(sp, pivot_common.as_expr()),
        },
        "logic": ("If the two selected affine-linear equations have a common "
                  "(a0,a5) solution and their coefficient determinant is zero, "
                  "both coefficient/RHS 2x2 minors must vanish.  These are "
                  "necessary literal consistency equations; no pivot division occurs."),
        "scope_guard": ("This is only a minimal residual interface, not an "
                        "emptiness result and not a claim that the two rows are sufficient."),
        "mutation_control": ("Deleting either RHS column changes its corresponding "
                             "forced determinant; identifying pivot=0 with C0=0 "
                             "drops four exact nonlive factors."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_interface.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero minimal interface PASS", result["logical_sha256"])
    print("smallest", smallest_label, profile(sp, smallest, variables3))
    print("consistency gcd", result["two_consistency_minor_gcd"]["profile"])


if __name__ == "__main__":
    main()
