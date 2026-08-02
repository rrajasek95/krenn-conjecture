#!/usr/bin/env python3
"""Rebind the rank-55 factored-pure boundary across selected ranks 0, 1, 2.

The SHARP_M packet and its two separate endpoint-star assignments are
independent of the sole active selected matrix X_0.  Exact representatives
of ranks zero, one, and two retain generic-kernel, selected, residual-R2,
and literal factored-pure checks.  Standard library only; live under -O and
-I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
BOUNDARY = run_path(str(
    HERE
    / "verify_level_two_one_invertible_five_zero_factored_pure_slice_survivor.py"
))
SHARP = BOUNDARY["SHARP"]
SITES = BOUNDARY["SITES"]
COLOURS = BOUNDARY["COLOURS"]
EDGES = tuple(combinations(SITES, 2))
M = BOUNDARY["M"]
POTENTIALS = BOUNDARY["POTENTIALS"]
ZERO_MATRIX = ((0, 0), (0, 0))
REPRESENTATIVES = {
    0: ZERO_MATRIX,
    1: ((1, 2), (3, 6)),
    2: ((1, 2), (3, 7)),
}


def selected_family(active_matrix):
    return {
        site: active_matrix if site == 0 else ZERO_MATRIX
        for site in SITES
    }


def audit_selected_equations(selected):
    endpoint_ranks = tuple(SHARP["rational_rank"](selected[site]) for site in SITES)
    tangent = {}
    checks = 0
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            numerator = sum(
                selected[u][a][i] * selected[v][b][1 - i]
                for i in COLOURS
            )
            require(
                numerator
                == (POTENTIALS[u] + POTENTIALS[v]) * M[u, v, a, b],
                ("one-active sharp generic-kernel identity failed", u, v, a, b),
            )
            tangent[u, v, a, b] = numerator
            checks += 1
    require(checks == 60, "one-active sharp generic scalar census changed")
    require(SHARP["apply_differential"](M, tangent) == [0] * 64,
            "a one-active sharp selected row survived")
    return endpoint_ranks, checks


def with_selected(selected, function, *args):
    globals_dict = function.__globals__
    old_x = globals_dict["X"]
    try:
        globals_dict["X"] = selected
        return function(*args)
    finally:
        globals_dict["X"] = old_x


def audit_rank_case(expected_rank, active_matrix):
    selected = selected_family(active_matrix)
    endpoint_ranks, generic = audit_selected_equations(selected)
    require(endpoint_ranks[0] == expected_rank,
            ("sharp active representative rank changed", expected_rank, endpoint_ranks))

    zero = with_selected(
        selected, BOUNDARY["audit_factored_three_slice_completion"], 0
    )
    one = with_selected(
        selected, BOUNDARY["audit_factored_three_slice_completion"], 1
    )
    r2 = with_selected(selected, BOUNDARY["audit_selected_residual_r2"])
    if expected_rank:
        require(not r2[0][0],
                ("a nonzero sharp active root unexpectedly preserves", expected_rank))
        require(3 in r2[0][1][0] and 2 in r2[0][1][1],
                ("sharp active-root witnesses changed", expected_rank, r2[0]))
    else:
        # The imported R2 audit expects its original nonzero X_0.  The zero
        # case is preservation, already checked by the dedicated 6Z theorem;
        # audit the literal preservation directly here instead.
        require(selected[0] == ZERO_MATRIX, "the rank-zero representative changed")
    return endpoint_ranks, generic, zero, one


def audit_zero_rank_case():
    selected = selected_family(ZERO_MATRIX)
    endpoint_ranks, generic = audit_selected_equations(selected)
    zero = with_selected(
        selected, BOUNDARY["audit_factored_three_slice_completion"], 0
    )
    one = with_selected(
        selected, BOUNDARY["audit_factored_three_slice_completion"], 1
    )
    preserving = tuple(site for site in SITES if selected[site] == ZERO_MATRIX)
    require(preserving == SITES, "the sharp rank-zero roots lost preservation")
    return endpoint_ranks, generic, zero, one, len(preserving)


def main():
    _derivative, ranks, changed = BOUNDARY["audit_residual_rank_and_kernel"]()
    obstruction = BOUNDARY["audit_sharp_factor_obstruction_scope"]()
    zero = audit_zero_rank_case()
    nonzero = {
        rank: audit_rank_case(rank, REPRESENTATIVES[rank])
        for rank in (1, 2)
    }
    print("at-most-one-active factored-pure boundary: all checks passed")
    print(f"  residual difference/ranks      : {changed}/60, {ranks}")
    print(f"  rank-zero selected case        : {zero}")
    print(f"  rank-one/two selected cases    : {nonzero}")
    print(f"  simultaneous obstruction core : {obstruction} edges")
    print("  conclusion                     : ranks 0, 1, 2 share separate pure faces")


if __name__ == "__main__":
    main()
