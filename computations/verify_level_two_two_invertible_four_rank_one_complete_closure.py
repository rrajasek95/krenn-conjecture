#!/usr/bin/env python3
"""Audit the complete generic-kernel closure of the 2I+4R stratum.

The zero-multiplier graph on four rank-one sites is either one of four
no-isolated graphs (2K2, K1,3, K2,2, K4) or has an isolated vertex.  In the
latter case the other three rank-one sites form a coordinate shore, with
rank bounds 35, 42, 49, or 51.  The prior no-isolated support theorems have
bounds 48, 47, 53, and 52.  Thus rank(dPsi) <= 53 throughout 2I+4R.

Standard library only; ``require`` checks remain live under ``-O`` and the
checker also runs with isolated Python (``-I -S``).
"""

from collections import Counter
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent


def load_checker(stem):
    return run_path(str(HERE / f"{stem}.py"))


RANK_ONE = load_checker(
    "verify_level_two_two_invertible_three_rank_one_one_zero_closure"
)
BALANCED = load_checker(
    "verify_level_two_two_invertible_four_rank_one_balanced_k22_closure"
)
DISJOINT = load_checker(
    "verify_level_two_two_invertible_four_rank_one_disjoint_pair_closure"
)
STAR = load_checker(
    "verify_level_two_two_invertible_four_rank_one_k13_closure"
)
ALL_ZERO = load_checker(
    "verify_level_two_two_invertible_four_rank_one_all_zero_closure"
)

VERTICES = range(4)
FOUR_EDGES = tuple(combinations(VERTICES, 2))
NO_ISOLATED_TYPES = {
    (2, (1, 1, 1, 1)): "2K2",
    (3, (1, 1, 1, 3)): "K1,3",
    (4, (2, 2, 2, 2)): "K2,2",
    (6, (3, 3, 3, 3)): "K4",
}


def zero_sum_edges(potentials):
    return frozenset(
        (u, v) for u, v in FOUR_EDGES
        if potentials[u] + potentials[v] == 0
    )


def graph_signature(edges):
    degrees = tuple(sorted(
        sum(vertex in edge for edge in edges)
        for vertex in VERTICES
    ))
    return len(edges), degrees


def audit_four_vertex_graph_classification():
    # Four vertices use at most four nonzero sign-orbits.  Relabeling those
    # orbits by 1,...,4 embeds every abstract zero/opposition pattern in this
    # exhaustive 9^4 model.
    no_isolated = Counter()
    no_isolated_zero_counts = {
        graph_type: set() for graph_type in NO_ISOLATED_TYPES.values()
    }
    isolated_shores = Counter()
    for potentials in product(range(-4, 5), repeat=4):
        edges = zero_sum_edges(potentials)
        degrees = tuple(
            sum(vertex in edge for edge in edges)
            for vertex in VERTICES
        )
        if all(degrees):
            signature = graph_signature(edges)
            require(signature in NO_ISOLATED_TYPES,
                    ("unclassified no-isolated graph", potentials, edges))
            graph_type = NO_ISOLATED_TYPES[signature]
            no_isolated[graph_type] += 1
            no_isolated_zero_counts[graph_type].add(potentials.count(0))
        for isolated in VERTICES:
            if degrees[isolated]:
                continue
            shore_edges = sum(
                isolated not in edge for edge in edges
            )
            require(shore_edges in range(4),
                    ("bad three-site shore", potentials, isolated, edges))
            isolated_shores[shore_edges] += 1

    require(no_isolated == {
        "2K2": 192,
        "K1,3": 32,
        "K2,2": 24,
        "K4": 1,
    }, ("no-isolated enumeration changed", no_isolated))
    require(isolated_shores == {0: 13024, 1: 4704, 2: 672, 3: 32},
            ("isolated-shore enumeration changed", isolated_shores))
    require(no_isolated_zero_counts == {
        "2K2": {0, 2},
        "K1,3": {0},
        "K2,2": {0},
        "K4": {4},
    }, ("no-isolated zero counts changed", no_isolated_zero_counts))

    # The 2K2 support theorem must include both kinds of potential data:
    # two nonzero sign-orbits and a zero pair plus one nonzero opposite pair.
    expected_matching = frozenset(((0, 1), (2, 3)))
    for potentials in ((1, -1, 2, -2), (0, 0, 1, -1)):
        require(zero_sum_edges(potentials) == expected_matching,
                ("2K2 representative changed", potentials))
    return no_isolated, isolated_shores


def audit_isolated_triangle_constant_cross():
    # In a triangle shore all three potentials vanish and all source factors
    # can be written as one common b.  After a_s=e0, both an invertible inner
    # numerator and the isolated rank-one inner numerator are independent of
    # the shore label.  Their nonzero multipliers are nu_i and nu_r.
    constant = RANK_ONE["constant"]
    variable = RANK_ONE["variable"]
    add = RANK_ONE["add"]
    multiply = RANK_ONE["multiply"]
    matrix_product = RANK_ONE["matrix_product"]
    transpose = RANK_ONE["transpose"]
    outer = RANK_ONE["outer"]

    J = ((constant(0), constant(1)),
         (constant(1), constant(0)))
    e0 = (constant(1), constant(0))
    common_b = tuple(variable(f"b{row}") for row in range(2))
    isolated_a = tuple(variable(f"a{row}") for row in range(2))
    isolated_b = tuple(variable(f"c{row}") for row in range(2))
    invertible_x = tuple(
        tuple(variable(f"x{row}{column}") for column in range(2))
        for row in range(2)
    )
    shore_x = outer(e0, common_b)
    isolated_x = outer(isolated_a, isolated_b)

    invertible_actual = matrix_product(
        matrix_product(invertible_x, J), transpose(shore_x)
    )
    invertible_left = tuple(
        add(*(multiply(invertible_x[row][middle],
                       common_b[1 - middle])
              for middle in range(2)))
        for row in range(2)
    )
    invertible_expected = outer(invertible_left, e0)

    isolated_actual = matrix_product(
        matrix_product(isolated_x, J), transpose(shore_x)
    )
    pairing = add(
        multiply(isolated_b[0], common_b[1]),
        multiply(isolated_b[1], common_b[0]),
    )
    isolated_expected = tuple(
        tuple(multiply(pairing, isolated_a[row], e0[column])
              for column in range(2))
        for row in range(2)
    )

    checked = 0
    for _shore_label in range(3):
        require(invertible_actual == invertible_expected,
                "invertible triangle spoke stopped being constant")
        require(isolated_actual == isolated_expected,
                "rank-one triangle spoke stopped being constant")
        checked += 8
    return checked


def audit_isolated_vertex_bounds():
    require(RANK_ONE["audit_rank_one_generic_factors"]() == 8,
            "rank-one block factorization audit changed")
    require(RANK_ONE["audit_zero_sum_graph_classification"]() == {
        0: "empty",
        1: "one edge",
        2: "two-edge path",
        3: "triangle",
    }, "three-site graph classification changed")
    require(len(RANK_ONE["audit_triangle_common_isotropic_line"]()) == 2,
            "common-isotropic-line branch audit changed")
    require(audit_isolated_triangle_constant_cross() == 24,
            "constant-cross numerator audit changed")

    bounds, categories = RANK_ONE["audit_imported_shore_bounds"]()
    require(bounds == {
        "empty": 35,
        "one edge": 42,
        "two-edge path": 49,
        "triangle": 51,
    }, ("isolated-vertex shore bounds changed", bounds))
    require(max(bounds.values()) == 51,
            "isolated-vertex maximum bound changed")
    return bounds, categories


def audit_no_isolated_support_bounds():
    require(BALANCED["audit_formal_extra_kernel"]() == 128,
            "K2,2 formal kernel audit changed")
    require(BALANCED["audit_kernel_independence"]() == (5, 2, 7, 53),
            "K2,2 rank bound changed")

    require(DISJOINT["audit_matching_factorization"]() == 64,
            "2K2 matching factorization changed")
    disjoint_checks, disjoint_dimensions = (
        DISJOINT["audit_effective_kernel_and_dimensions"]()
    )
    require(disjoint_checks == 256, "2K2 kernel audit changed")
    require(disjoint_dimensions == (32, 24, 4, 20, 28, 48),
            "2K2 dimension count changed")

    require(STAR["audit_matching_factorization"]() == 64,
            "K1,3 matching factorization changed")
    star_checks, star_dimensions = (
        STAR["audit_effective_kernel_and_dimensions"]()
    )
    require(star_checks == 384, "K1,3 kernel audit changed")
    require(star_dimensions == (35, 28, 6, 22, 25, 47),
            "K1,3 dimension count changed")

    require(ALL_ZERO["audit_constant_spoke_factorization"]() == 64,
            "K4 constant-spoke factorization changed")
    require(ALL_ZERO["audit_formal_cancellation_kernel"]() == 256,
            "K4 formal kernel audit changed")
    require(ALL_ZERO["audit_kernel_dimension"]() == (5, 4, 8, 52),
            "K4 rank bound changed")

    bounds = {"2K2": 48, "K1,3": 47, "K2,2": 53, "K4": 52}
    require(max(bounds.values()) == 53,
            "no-isolated maximum bound changed")
    return bounds


def main():
    graph_counts, isolated_counts = audit_four_vertex_graph_classification()
    isolated_bounds, path_categories = audit_isolated_vertex_bounds()
    no_isolated_bounds = audit_no_isolated_support_bounds()
    universal_bound = max(
        max(isolated_bounds.values()), max(no_isolated_bounds.values())
    )
    require(universal_bound == 53, "universal 2I+4R bound changed")

    print("complete 2I+4R generic-kernel closure verified")
    print(f"  no-isolated graph counts   : {dict(graph_counts)}")
    print(f"  isolated shore counts      : {dict(isolated_counts)}")
    print(f"  isolated-vertex bounds     : {isolated_bounds}")
    print(f"  path matching categories   : {path_categories}")
    print(f"  no-isolated bounds         : {no_isolated_bounds}")
    print(f"  universal differential rank: <= {universal_bound}")


if __name__ == "__main__":
    main()
