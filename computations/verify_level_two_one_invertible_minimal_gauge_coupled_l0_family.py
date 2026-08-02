#!/usr/bin/env python3
"""Exact rank-38 obstruction for a minimal gauge-coupled 1I+5Z family.

The canonical residual packet couples the two localized pure endpoint-star
assignments: both mixed tangents are vertex gauges, so one shared endpoint
assignment realizes all four L0 slices.  With X_2=I it also has literal
selected residual R2.  Its differential rank is only 38.

Independent nonzero diagonal changes at all six residual sites preserve the
four-slice completion, R2, and differential rank.  Thus the whole natural
12-parameter diagonal-torus family misses rank 55.  Standard library only;
checks stay live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
CORE = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

SITES = tuple(range(6))
ENDPOINTS = (6, 7)
COLOURS = (0, 1)
RARE = 2
EDGES = tuple(combinations(SITES, 2))
CELLS = CORE["CELLS"]
WORDS = CORE["WORDS"]
MATCHINGS8 = CORE["MATCHINGS8"]
ZERO = ((0, 0), (0, 0))
E00 = ((1, 0), (0, 0))
E01 = ((0, 1), (0, 0))
E11 = ((0, 0), (0, 1))

BLOCKS = {edge: ZERO for edge in EDGES}
BLOCKS.update({
    (0, 2): E11,
    (1, 3): E11,
    (2, 3): E00,
    (4, 5): E00,
    (0, 4): E01,
    (0, 5): E01,
    (1, 4): E01,
    (1, 5): E01,
})
M = {
    (u, v, a, b): BLOCKS[u, v][a][b]
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
}
X = {
    site: ((1, 0), (0, 1)) if site == 2 else ((0, 0), (0, 0))
    for site in SITES
}
GAUGE = (1, -1, -1, 1, 0, 0)


def canonical_stars():
    u = {
        (s, r, a): Q(0)
        for s in COLOURS for r in SITES for a in COLOURS
    }
    v = dict(u)
    u[0, 0, 0] = Q(1)
    u[0, 1, 0] = Q(-1)
    v[0, 0, 0] = Q(-1, 2)
    v[0, 1, 0] = Q(1, 2)
    u[1, 4, 1] = Q(1, 2)
    u[1, 5, 1] = Q(1, 2)
    v[1, 4, 1] = Q(1)
    v[1, 5, 1] = Q(1)
    return u, v


def factored_tangent(u_star, v_star, s, t):
    return {
        (r, u, a, b): (
            u_star[s, r, a] * v_star[t, u, b]
            + v_star[t, r, a] * u_star[s, u, b]
        )
        for r, u in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def gauge_tangent(packet, weights):
    return {
        (r, u, a, b): (weights[r] + weights[u]) * packet[r, u, a, b]
        for r, u, a, b in CELLS
    }


def ranks_over_fields(matrix):
    return (
        CORE["rational_rank"](matrix),
        CORE["modular_rank"](matrix, 101),
        CORE["modular_rank"](matrix, 32_003),
        CORE["modular_rank"](matrix, 1_000_003),
    )


def audit_canonical_four_slice_completion():
    u_star, v_star = canonical_stars()
    tangents = {
        (s, t): factored_tangent(u_star, v_star, s, t)
        for s, t in product(COLOURS, repeat=2)
    }
    gauge = gauge_tangent(M, GAUGE)
    require(tangents[0, 1] == gauge,
            "the first mixed tangent is not the planned gauge")
    require(all(
        tangents[1, 0][cell] == Q(-1, 4) * gauge[cell]
        for cell in CELLS
    ), "the second mixed tangent is not minus one quarter of the gauge")
    require(not any(CORE["apply_differential"](M, gauge)),
            "the planned vertex gauge left the differential kernel")

    expected_support = {
        (0, 0): ((0, 1, 0, 0),),
        (0, 1): (
            (0, 4, 0, 1), (0, 5, 0, 1),
            (1, 4, 0, 1), (1, 5, 0, 1),
        ),
        (1, 0): (
            (0, 4, 0, 1), (0, 5, 0, 1),
            (1, 4, 0, 1), (1, 5, 0, 1),
        ),
        (1, 1): ((4, 5, 1, 1),),
    }
    for key, tangent in tangents.items():
        support = tuple(cell for cell in CELLS if tangent[cell])
        require(support == expected_support[key],
                ("a factored tangent support changed", key, support))

    outputs = {
        key: CORE["apply_differential"](M, tangent)
        for key, tangent in tangents.items()
    }
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    require(outputs == {
        (0, 0): pure_zero,
        (0, 1): [0] * 64,
        (1, 0): [0] * 64,
        (1, 1): pure_one,
    }, "the canonical four L0 outputs changed")
    return u_star, v_star, tangents, outputs


def audit_rank_ceiling():
    derivative = CORE["differential_matrix"](M)
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
    }
    require(ranks == {
        "D": (38, 38, 38, 38),
        "D_mixed": (36, 36, 36, 36),
    }, ("the minimal coupled ranks changed", ranks))
    return derivative, ranks


def transform_packet(packet, diagonal):
    return {
        (r, u, a, b): (
            diagonal[r][a] * packet[r, u, a, b] * diagonal[u][b]
        )
        for r, u, a, b in CELLS
    }


def transform_stars(u_star, v_star, diagonal):
    zero_scale = Q(1)
    one_scale = Q(1)
    for site in SITES:
        zero_scale *= diagonal[site][0]
        one_scale *= diagonal[site][1]
    transformed_u = {}
    transformed_v = {}
    for s in COLOURS:
        normalization = Q(1, zero_scale if s == 0 else one_scale)
        for r in SITES:
            for a in COLOURS:
                transformed_u[s, r, a] = (
                    normalization * diagonal[r][a] * u_star[s, r, a]
                )
                transformed_v[s, r, a] = (
                    diagonal[r][a] * v_star[s, r, a]
                )
    return transformed_u, transformed_v, (zero_scale, one_scale)


def audit_formal_covariance_support():
    """Check the diagonal exponent identity on every live derivative term."""

    checked = 0
    for word in WORDS:
        expected = [0] * 12
        for site in SITES:
            expected[2 * site + word[site]] += 1
        for r, u in EDGES:
            complement = tuple(
                site for site in SITES if site not in (r, u)
            )
            for matching in CORE["MATCHINGS"][complement]:
                term = 1
                exponent = [0] * 12
                exponent[2 * r + word[r]] += 1
                exponent[2 * u + word[u]] += 1
                for left, right in matching:
                    term *= M[left, right, word[left], word[right]]
                    exponent[2 * left + word[left]] += 1
                    exponent[2 * right + word[right]] += 1
                if not term:
                    continue
                require(exponent == expected,
                        ("a live derivative monomial has the wrong weight",
                         word, r, u, matching))
                checked += 1
    require(checked == 56,
            ("the live covariance-monomial census changed", checked))
    return checked


def audit_diagonal_covariance(derivative, u_star, v_star):
    diagonal = {
        site: pair for site, pair in enumerate((
            (2, 17), (3, 19), (5, 23),
            (7, 29), (11, 31), (13, 37),
        ))
    }
    require(all(value for pair in diagonal.values() for value in pair),
            "a diagonal family parameter vanished")
    transformed_m = transform_packet(M, diagonal)
    transformed_d = CORE["differential_matrix"](transformed_m)

    row_scales = {
        word: Q(1) for word in WORDS
    }
    for word in WORDS:
        for site in SITES:
            row_scales[word] *= diagonal[site][word[site]]
    column_scales = {
        (r, u, a, b): Q(diagonal[r][a] * diagonal[u][b])
        for r, u, a, b in CELLS
    }
    checked = 0
    for row, word in enumerate(WORDS):
        for column, cell in enumerate(CELLS):
            require(
                transformed_d[row][column] * column_scales[cell]
                == row_scales[word] * derivative[row][column],
                ("diagonal differential covariance failed", word, cell),
            )
            checked += 1
    require(checked == 64 * 60,
            "the differential covariance census changed")

    transformed_u, transformed_v, target_scales = transform_stars(
        u_star, v_star, diagonal
    )
    transformed_tangents = {
        (s, t): factored_tangent(transformed_u, transformed_v, s, t)
        for s, t in product(COLOURS, repeat=2)
    }
    transformed_outputs = {
        key: CORE["apply_differential"](transformed_m, tangent)
        for key, tangent in transformed_tangents.items()
    }
    require(transformed_outputs == {
        (0, 0): [int(word == (0,) * 6) for word in WORDS],
        (0, 1): [0] * 64,
        (1, 0): [0] * 64,
        (1, 1): [int(word == (1,) * 6) for word in WORDS],
    }, "a nontrivial diagonal family member lost the four L0 slices")

    transformed_gauge = gauge_tangent(transformed_m, GAUGE)
    zero_scale, one_scale = target_scales
    require(all(
        transformed_tangents[0, 1][cell]
        == Q(1, zero_scale) * transformed_gauge[cell]
        for cell in CELLS
    ), "the transformed first mixed gauge coefficient changed")
    require(all(
        transformed_tangents[1, 0][cell]
        == Q(-1, 4 * one_scale) * transformed_gauge[cell]
        for cell in CELLS
    ), "the transformed second mixed gauge coefficient changed")
    return transformed_m, transformed_u, transformed_v, checked


def full_edge_value(packet, u_star, v_star, edge, colours):
    r, u = edge
    a, b = colours
    if u < ENDPOINTS[0]:
        return packet[r, u, a, b]
    if u == ENDPOINTS[0] and r < ENDPOINTS[0]:
        if b in COLOURS:
            return u_star[b, r, a]
        if b == RARE:
            return Q(X[r][a][0])
        return Q(0)
    if u == ENDPOINTS[1] and r < ENDPOINTS[0]:
        if b in COLOURS:
            return v_star[b, r, a]
        if b == RARE:
            return Q(X[r][a][1])
        return Q(0)
    if (r, u) == ENDPOINTS:
        return Q(0)
    raise RuntimeError(("unclassified eight-site edge", edge, colours))


def eight_site_value(packet, u_star, v_star, word):
    total = Q(0)
    for matching in MATCHINGS8:
        term = Q(1)
        for edge in matching:
            term *= full_edge_value(
                packet, u_star, v_star, edge,
                (word[edge[0]], word[edge[1]]),
            )
        total += term
    return total


def audit_literal_eight_site_slices(packet, u_star, v_star):
    checked = 0
    for s, t in product(COLOURS, repeat=2):
        literal = [
            eight_site_value(packet, u_star, v_star, word + (s, t))
            for word in WORDS
        ]
        expected = [
            int((s, t) == (0, 0) and word == (0,) * 6)
            + int((s, t) == (1, 1) and word == (1,) * 6)
            for word in WORDS
        ]
        require(literal == expected,
                ("a literal eight-site L0 slice changed", s, t))
        checked += 64
    selected = [
        eight_site_value(packet, u_star, v_star, word + (RARE, RARE))
        for word in WORDS
    ]
    require(selected == [0] * 64,
            "the selected rare/rare endpoint slice is nonzero")
    return checked


def oriented_value(packet, root, neighbour, root_colour, neighbour_colour):
    if root < neighbour:
        return packet.get(
            (root, neighbour, root_colour, neighbour_colour), Q(0)
        )
    return packet.get(
        (neighbour, root, neighbour_colour, root_colour), Q(0)
    )


def pure_internal_column(packet, root, neighbour, output):
    return (
        any(oriented_value(packet, root, neighbour, row, output)
            for row in COLOURS)
        and all(
            oriented_value(packet, root, neighbour, row, column) == 0
            for row in COLOURS
            for column in COLOURS
            if column != output
        )
    )


def audit_selected_block_and_r2(packet):
    endpoint_ranks = tuple(CORE["rational_rank"](X[site]) for site in SITES)
    require(endpoint_ranks == (0, 0, 2, 0, 0, 0),
            ("one-invertible endpoint ranks changed", endpoint_ranks))

    selected_tangent = {}
    checked = 0
    for r, u in EDGES:
        for a, b in product(COLOURS, repeat=2):
            numerator = sum(
                X[r][a][i] * X[u][b][1 - i]
                for i in COLOURS
            )
            require(numerator == 0,
                    ("a generic-kernel numerator survived", r, u, a, b))
            selected_tangent[r, u, a, b] = numerator
            checked += 1
    require(checked == 60, "generic-kernel scalar census changed")
    require(CORE["apply_differential"](packet, selected_tangent) == [0] * 64,
            "a selected level-two row survived")

    require(pure_internal_column(packet, 2, 3, 0),
            "the root-2 pure-zero residual witness vanished")
    require(pure_internal_column(packet, 2, 0, 1),
            "the root-2 pure-one residual witness vanished")
    for neighbour in (3, 0):
        complement = tuple(
            site for site in SITES if site not in (2, neighbour)
        )
        require(any(
            CORE["hafnian"](packet, complement, word) != 0
            for word in WORDS
        ), ("a root-2 residual witness has zero cofactor", neighbour))

    preserving = tuple(site for site in SITES if site != 2)
    require(all(
        X[site] == ((0, 0), (0, 0)) for site in preserving
    ), "a nominally preserving root has a selected rare column")
    return endpoint_ranks, checked, preserving


def main():
    u_star, v_star, _tangents, _outputs = (
        audit_canonical_four_slice_completion()
    )
    derivative, ranks = audit_rank_ceiling()
    formal_covariance = audit_formal_covariance_support()
    transformed_m, transformed_u, transformed_v, covariance = (
        audit_diagonal_covariance(derivative, u_star, v_star)
    )
    literal = audit_literal_eight_site_slices(
        transformed_m, transformed_u, transformed_v
    )
    endpoint_ranks, generic, preserving = audit_selected_block_and_r2(
        transformed_m
    )
    print("one-invertible minimal gauge-coupled L0 family: all checks passed")
    print(f"  canonical differential ranks : {ranks}")
    print(f"  formal covariance monomials  : {formal_covariance}/56")
    print(f"  diagonal covariance entries  : {covariance}/3840")
    print(f"  literal transformed L0 slices: {literal}/256")
    print(f"  endpoint ranks               : {endpoint_ranks}")
    print(f"  generic-kernel scalars       : {generic}/60")
    print(f"  selected R2 preserving roots : {len(preserving)}/5")
    print("  active R2 root               : 2, internal witnesses 23/0 and 20/1")
    print("  family conclusion            : full factored L0 + R2, rank identically 38")


if __name__ == "__main__":
    main()
