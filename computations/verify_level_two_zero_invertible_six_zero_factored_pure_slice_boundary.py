#!/usr/bin/env python3
"""Rebind the sharp factored-pure boundary to the 6Z selected chart.

Set all six selected endpoint matrices and all six potentials to zero while
retaining the exact SHARP_M residual packet and the two separate binary
endpoint-star assignments from the 1I+5Z factored-pure theorem.  The
generic-kernel and selected rows vanish, every residual root preserves the
binary pair, and each pure L0 target is still realized separately.

This does not assert a simultaneous four-slice completion.  Standard library
only; checks remain live under -O and -I -S.
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

SITES = BOUNDARY["SITES"]
COLOURS = BOUNDARY["COLOURS"]
ENDPOINTS = BOUNDARY["ENDPOINTS"]
EDGES = tuple(combinations(SITES, 2))
M = BOUNDARY["M"]
ZERO_MATRIX = ((0, 0), (0, 0))
X_ZERO = {site: ZERO_MATRIX for site in SITES}
POTENTIALS = (0,) * 6


def audit_zero_selected_block():
    ranks = tuple(
        BOUNDARY["SHARP"]["rational_rank"](X_ZERO[site])
        for site in SITES
    )
    require(ranks == (0, 0, 0, 0, 0, 0),
            ("six-zero endpoint ranks changed", ranks))

    checks = 0
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            numerator = sum(
                X_ZERO[u][a][i] * X_ZERO[v][b][1 - i]
                for i in COLOURS
            )
            require(
                numerator
                == (POTENTIALS[u] + POTENTIALS[v]) * M[u, v, a, b],
                ("six-zero generic-kernel identity failed", u, v, a, b),
            )
            checks += 1
    require(checks == 60, "six-zero generic scalar census changed")

    tangent = {
        (u, v, a, b): 0
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }
    require(
        BOUNDARY["SHARP"]["apply_differential"](M, tangent) == [0] * 64,
        "a six-zero selected row survived",
    )
    require(-sum(POTENTIALS) == 0,
            "the six-zero direct selected value is nonzero")
    return ranks, checks


def audit_factored_binary_slices():
    # The imported functions share one module-global dictionary. Rebinding
    # X affects only the selected rare/rare audit; the 512 literal binary
    # slices use M and the two endpoint-star assignments unchanged.
    function = BOUNDARY["audit_factored_three_slice_completion"]
    globals_dict = function.__globals__
    require(globals_dict is BOUNDARY["eight_site_value"].__globals__,
            "the imported factored functions lost shared globals")
    old_x = globals_dict["X"]
    try:
        globals_dict["X"] = X_ZERO
        zero = function(0)
        one = function(1)
    finally:
        globals_dict["X"] = old_x
    require(zero == (256, (0, 1, 0, 0))
            and one == (256, (4, 5, 1, 1)),
            ("six-zero factored slices changed", zero, one))
    return zero, one


def audit_residual_r2_preservation():
    # The binary endpoint-star assignments do not create a rare column.
    # With every selected rare column zero, every residual root preserves
    # the residual binary pair.
    roots = {}
    for root in SITES:
        rare_values = [
            X_ZERO[root][row][column]
            for row in COLOURS
            for column in COLOURS
        ]
        require(not any(rare_values),
                ("a six-zero root lost preservation", root, rare_values))
        roots[root] = "preserves binary pair"
    require(len(roots) == 6, "six-zero R2 root census changed")
    return roots


def main():
    _derivative, incidence, changed = (
        BOUNDARY["audit_residual_rank_and_kernel"]()
    )
    ranks, generic = audit_zero_selected_block()
    slices = audit_factored_binary_slices()
    r2 = audit_residual_r2_preservation()
    obstruction = BOUNDARY["audit_sharp_factor_obstruction_scope"]()

    print("zero-invertible six-zero factored-pure boundary: all checks passed")
    print(f"  endpoint ranks                : {ranks}")
    print(f"  generic-kernel scalars        : {generic}/60")
    print("  selected level-two rows       : 64/64")
    print(f"  selected residual R2 roots    : {len(r2)}/6")
    print(f"  differential incidence ranks  : {incidence}")
    print(f"  separate factored pure slices : {slices}")
    print(f"  sharp/old residual difference : {changed}/60 cells")
    print(f"  simultaneous obstruction core : {obstruction} edges")
    print("  scope                          : separate pure assignments only")


if __name__ == "__main__":
    main()
