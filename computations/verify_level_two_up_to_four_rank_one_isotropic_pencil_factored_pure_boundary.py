#!/usr/bin/env python3
"""Rank-55 factored-pure guards with up to four rank-one selected sites.

Activate any subset of roots 0,1,2,3 with rank-one matrices sharing the
isotropic input line e_0.  All pair-pencil numerators vanish.  Each active
root has two residual internal R2 witnesses with nonzero cofactors, while
inactive roots preserve.  The SHARP_M residual and separate factored-pure
assignments retain rank 55/53.  Standard library only; live under -O and
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
EDGES = BOUNDARY["EDGES"]
WORDS = BOUNDARY["WORDS"]
M = BOUNDARY["M"]
POTENTIALS = BOUNDARY["POTENTIALS"]
ZERO_MATRIX = ((0, 0), (0, 0))
ELIGIBLE = (0, 1, 2, 3)
OUTPUT_FACTORS = {
    0: (1, 2),
    1: (2, 3),
    2: (3, 5),
    3: (5, 7),
}
WITNESSES = {
    0: {0: 3, 1: 2},
    1: {0: 2, 1: 3},
    2: {0: 3, 1: 0},
    3: {0: 2, 1: 1},
}


def selected_family(active):
    selected = {site: ZERO_MATRIX for site in SITES}
    for site in active:
        h0, h1 = OUTPUT_FACTORS[site]
        selected[site] = ((h0, 0), (h1, 0))
    return selected


def audit_selected_equations(selected):
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
                ("isotropic-pencil generic-kernel identity failed", u, v, a, b),
            )
            tangent[u, v, a, b] = numerator
            checks += 1
    require(checks == 60, "isotropic-pencil scalar census changed")
    require(SHARP["apply_differential"](M, tangent) == [0] * 64,
            "an isotropic-pencil selected row survived")
    return checks


def with_selected(selected, function, *args):
    globals_dict = function.__globals__
    old_x = globals_dict["X"]
    try:
        globals_dict["X"] = selected
        return function(*args)
    finally:
        globals_dict["X"] = old_x


def audit_r2(active, selected):
    table = {}
    for root in SITES:
        preserves = selected[root] == ZERO_MATRIX
        if root in active:
            require(not preserves, ("an active isotropic root preserves", root))
            pure = {}
            for output, neighbour in WITNESSES[root].items():
                require(BOUNDARY["pure_column"](M, root, neighbour, output),
                        ("an isotropic-root pure witness vanished",
                         root, output, neighbour))
                complement = tuple(
                    site for site in SITES if site not in (root, neighbour)
                )
                nonzero = sum(
                    SHARP["hafnian"](M, complement, word) != 0
                    for word in WORDS
                )
                require(nonzero,
                        ("an isotropic-root cofactor vanished",
                         root, output, neighbour))
                pure[output] = (neighbour, nonzero)
            table[root] = (False, pure)
        else:
            require(preserves, ("an inactive isotropic root lost preservation", root))
            table[root] = (True, {})
    return table


def audit_subset(active):
    selected = selected_family(active)
    ranks = tuple(SHARP["rational_rank"](selected[site]) for site in SITES)
    require(sum(ranks) == len(active) and all(rank in (0, 1) for rank in ranks),
            ("isotropic-pencil endpoint ranks changed", active, ranks))
    generic = audit_selected_equations(selected)
    zero = with_selected(
        selected, BOUNDARY["audit_factored_three_slice_completion"], 0
    )
    one = with_selected(
        selected, BOUNDARY["audit_factored_three_slice_completion"], 1
    )
    r2 = audit_r2(active, selected)
    return ranks, generic, zero, one, r2


def main():
    _derivative, ranks, changed = BOUNDARY["audit_residual_rank_and_kernel"]()
    obstruction = BOUNDARY["audit_sharp_factor_obstruction_scope"]()
    counts = {size: 0 for size in range(5)}
    checks = 0
    calibrations = {}
    for size in range(5):
        for active in combinations(ELIGIBLE, size):
            result = audit_subset(active)
            counts[size] += 1
            checks += result[1] + result[2][0] + result[3][0]
            calibrations.setdefault(size, (active, result[0]))
    require(counts == {0: 1, 1: 4, 2: 6, 3: 4, 4: 1},
            ("isotropic-pencil subset census changed", counts))
    print("up-to-four rank-one isotropic-pencil boundary: all checks passed")
    print(f"  residual difference/ranks      : {changed}/60, {ranks}")
    print(f"  active-subset census            : {counts}")
    print(f"  rank-profile calibrations       : {calibrations}")
    print(f"  generic/literal checks          : {checks}")
    print(f"  simultaneous obstruction core  : {obstruction} edges")
    print("  conclusion                      : kR+(6-k)Z reaches rank 55 for k<=4")


if __name__ == "__main__":
    main()
