#!/usr/bin/env python3
"""Exact frontier census and residual audit for nine singular two-K4 blocks.

The proof uses the exact-eight disjoint and overlap-one erased-Hessian
lemmas.  This checker independently enumerates all nine position orbits,
audits the actual two-/four-cross pullback on the eight locally closed
orbits, exhausts every literal-zero branch of the disjoint orbit, verifies
its final two-block polynomial contradiction, and exhibits the precise
local barrier on the remaining K3,3 singular square.
"""

from __future__ import annotations

import itertools
from collections import Counter

import sympy as sp

import verify_two_k4_exact_eight_checkerboard_hessian as exact_eight
import verify_two_k4_four_singular_matching_hessian_obstruction as hessian
import verify_two_k4_six_cycle_two_defect_obstruction as two_defect


SITES = hessian.SITES
COLORS = hessian.COLORS
EDGES = hessian.EDGES
WORDS = hessian.WORDS
CELLS = tuple(itertools.product(SITES, repeat=2))


def row_support(*rows: str) -> frozenset[tuple[int, int]]:
    return frozenset(
        (row, int(column))
        for row, columns in enumerate(rows)
        for column in columns
    )


# Canonical singular-position representatives after the pre-seven and
# separated-one-plus-two rules.  The final entry is the number of perfect
# matchings in the nonsingular complement.
FRONTIER_ORBITS = (
    (row_support("0123", "01", "02", "0"), 288, 0),
    (row_support("012", "012", "012", ""), 16, 0),
    (row_support("012", "012", "03", "3"), 288, 0),
    (row_support("012", "013", "023", ""), 192, 1),
    (row_support("012", "013", "02", "2"), 576, 1),
    (row_support("012", "01", "03", "23"), 576, 1),
    (row_support("012", "013", "23", "2"), 576, 2),
    (row_support("012", "01", "23", "23"), 144, 2),
    (row_support("012", "03", "13", "23"), 96, 2),
)

A = FRONTIER_ORBITS[6][0]
B = FRONTIER_ORBITS[7][0]
C = FRONTIER_ORBITS[8][0]
K33 = FRONTIER_ORBITS[1][0]


# (orbit index, transpose first, star rows, padded exception pairs, common
# exceptional site).  A padded component is invertible, which is allowed:
# the overlap lemma assumes that selected components are arbitrary and only
# requires the two unselected components of each star to be invertible.
OVERLAP_CASES = (
    (0, False, 1, 2, frozenset((0, 1)), frozenset((0, 2)), 0),
    (2, False, 2, 3, frozenset((0, 3)), frozenset((1, 3)), 3),
    (3, True, 1, 2, frozenset((0, 1)), frozenset((0, 2)), 0),
    (4, False, 2, 3, frozenset((0, 2)), frozenset((1, 2)), 2),
    (5, False, 1, 2, frozenset((0, 1)), frozenset((0, 3)), 0),
    (6, False, 2, 3, frozenset((2, 3)), frozenset((0, 2)), 2),
    (8, False, 1, 2, frozenset((0, 3)), frozenset((1, 3)), 3),
)


def transpose(support) -> frozenset[tuple[int, int]]:
    return frozenset((column, row) for row, column in support)


def exceptional_set(support, row: int) -> frozenset[int]:
    return frozenset(column for current, column in support if current == row)


def nonsingular_perfect_matchings(support) -> int:
    nonsingular = frozenset(CELLS) - frozenset(support)
    return sum(
        all((row, permutation[row]) in nonsingular for row in SITES)
        for permutation in itertools.permutations(SITES)
    )


def audit_frontier_census() -> None:
    survivors = tuple(
        frozenset(support)
        for support in itertools.combinations(CELLS, 9)
        if two_defect.survives_pre_seven_rules(frozenset(support))
        and not exact_eight.erased_by_separated_one_two(
            frozenset(support)
        )
    )
    assert len(survivors) == 2752

    observed = Counter(
        two_defect.canonical_support(support) for support in survivors
    )
    expected = Counter(
        {tuple(sorted(support)): orbit_size for support, orbit_size, _ in FRONTIER_ORBITS}
    )
    assert observed == expected

    for support, _orbit_size, matching_count in FRONTIER_ORBITS:
        assert two_defect.canonical_support(support) == tuple(sorted(support))
        assert nonsingular_perfect_matchings(support) == matching_count

    # This is diagnostic only.  A singular block need not be zero, so the
    # low-/unique-matching theorems cannot be applied to the nonsingular
    # complement without an additional zero-propagation theorem.
    by_matching_count = Counter()
    for support, orbit_size, matching_count in FRONTIER_ORBITS:
        by_matching_count[matching_count] += orbit_size
    assert by_matching_count == Counter({0: 592, 1: 1344, 2: 816})
    assert sum(
        orbit_size
        for _support, orbit_size, matching_count in FRONTIER_ORBITS
        if matching_count >= 2
    ) == 576 + 144 + 96


def assert_overlap_one(
    support,
    first: int,
    second: int,
    first_set: frozenset[int],
    second_set: frozenset[int],
    common: int,
) -> None:
    # All actual singular components lie among the selected arbitrary
    # components.  Every unselected component is therefore invertible.
    assert exceptional_set(support, first) <= first_set
    assert exceptional_set(support, second) <= second_set
    assert len(first_set) == len(second_set) == 2
    assert first_set & second_set == {common}

    complement = tuple(site for site in SITES if site not in (first, second))
    assert hessian.internal_color(first, second) == hessian.internal_color(
        *complement
    )
    assert {
        hessian.internal_color(common, other)
        for other in SITES
        if other != common
    } == set(COLORS)


def assert_disjoint(support, first: int, second: int) -> None:
    first_set = exceptional_set(support, first)
    second_set = exceptional_set(support, second)
    assert len(first_set) == len(second_set) == 2
    assert first_set.isdisjoint(second_set)
    complement = tuple(site for site in SITES if site not in (first, second))
    assert hessian.internal_color(first, second) == hessian.internal_color(
        *complement
    )


def audit_local_incidence_patterns() -> None:
    for (
        orbit_index,
        use_transpose,
        first,
        second,
        first_set,
        second_set,
        common,
    ) in OVERLAP_CASES:
        support = FRONTIER_ORBITS[orbit_index][0]
        if use_transpose:
            support = transpose(support)
        assert_overlap_one(
            support,
            first,
            second,
            first_set,
            second_set,
            common,
        )

    # B supplies two disjoint choices on the original shore and two more
    # after transposition, exactly the choices used in the zero audit.
    assert_disjoint(B, 1, 2)
    assert_disjoint(B, 1, 3)
    transposed_b = transpose(B)
    assert_disjoint(transposed_b, 0, 3)
    assert_disjoint(transposed_b, 1, 3)

    # K3,3 has three degree-three stars and one regular star on either
    # shore.  No two distinct stars can have all singular components inside
    # padded two-element exception sets.
    for support in (K33, transpose(K33)):
        eligible = tuple(
            row
            for row in SITES
            if len(exceptional_set(support, row)) <= 2
        )
        assert eligible == (3,)


def audit_weighted_sector_identity(
    support,
    first_row: int,
    second_row: int,
    label: str,
) -> int:
    """Audit the pullback with independent symbolic internal weights.

    The older exact-eight spot check sets all internal weights to one.  Here
    the selected left-edge weight and all six right-edge weights remain
    algebraically independent, so the exact-nine argument cannot silently
    use a unit-weight normalization.
    """

    blocks = two_defect.make_support_blocks(support)
    complementary = tuple(
        site for site in SITES if site not in (first_row, second_row)
    )
    left_a, left_b = complementary
    color = hessian.internal_color(left_a, left_b)
    assert color == hessian.internal_color(first_row, second_row)

    left_weight = sp.Symbol(f"lambda_{label}", nonzero=True)
    right_weights = {
        edge: sp.Symbol(f"rho_{label}_{edge[0]}{edge[1]}", nonzero=True)
        for edge in EDGES
    }
    q_right = {}
    for edge in EDGES:
        edge_color = hessian.internal_color(*edge)
        q_right[edge] = sp.zeros(3)
        q_right[edge][edge_color, edge_color] = right_weights[edge]

    first_complementary_star = {
        site: blocks[left_a, site].row(color) for site in SITES
    }
    second_complementary_star = {
        site: blocks[left_b, site].row(color) for site in SITES
    }
    q_effective = {
        (u, v): (
            left_weight * q_right[u, v]
            + first_complementary_star[u].T
            * second_complementary_star[v]
            + second_complementary_star[u].T
            * first_complementary_star[v]
        )
        for u, v in EDGES
    }

    checked = 0
    for x, y in itertools.product(COLORS, repeat=2):
        left_word = [None] * 4
        left_word[left_a] = left_word[left_b] = color
        left_word[first_row], left_word[second_row] = x, y
        left_word = tuple(left_word)
        first_star = {
            site: blocks[first_row, site].row(x) for site in SITES
        }
        second_star = {
            site: blocks[second_row, site].row(y) for site in SITES
        }

        for right_word in WORDS:
            four_cross = hessian.permanent([
                [
                    blocks[left, right][left_word[left], right_word[right]]
                    for right in SITES
                ]
                for left in SITES
            ])
            two_cross = 0
            for u, v in EDGES:
                edge_color = hessian.internal_color(u, v)
                if (
                    right_word[u] != edge_color
                    or right_word[v] != edge_color
                ):
                    continue
                remaining = tuple(
                    site for site in SITES if site not in (u, v)
                )
                two_cross += (
                    left_weight
                    * right_weights[u, v]
                    * hessian.permanent([
                        [
                            blocks[left, right][
                                left_word[left], right_word[right]
                            ]
                            for right in remaining
                        ]
                        for left in (first_row, second_row)
                    ])
                )
            pulled_back = hessian.beta_coefficient(
                q_effective,
                first_star,
                second_star,
                right_word,
            )
            assert sp.expand(pulled_back - four_cross - two_cross) == 0
            checked += 1
    assert checked == 729
    return checked


def audit_sector_identities() -> None:
    checked = 0
    for case_index, (
        orbit_index,
        use_transpose,
        first,
        second,
        *_rest,
    ) in enumerate(OVERLAP_CASES):
        support = FRONTIER_ORBITS[orbit_index][0]
        if use_transpose:
            support = transpose(support)
        checked += audit_weighted_sector_identity(
            support,
            first,
            second,
            f"H{orbit_index}_{case_index}",
        )
    checked += audit_weighted_sector_identity(B, 1, 2, "H7")
    assert checked == 8 * 729


def audit_literal_zero_reduction() -> None:
    """Every B branch not already erased is supported only at B_02."""

    # A disjoint pair kills the branch unless all four exceptional blocks
    # in that pair are literal zero.  The last two sets come from applying
    # the same statement after transposition.
    disjoint_unions = (
        frozenset(((1, 0), (1, 1), (2, 2), (2, 3))),
        frozenset(((1, 0), (1, 1), (3, 2), (3, 3))),
        frozenset(((0, 0), (1, 0), (2, 3), (3, 3))),
        frozenset(((0, 1), (1, 1), (2, 3), (3, 3))),
    )
    assert all(union <= B for union in disjoint_unions)

    surviving_nonzero_sets = set()
    ordered = tuple(sorted(B))
    for mask in range(1 << len(ordered)):
        nonzero = frozenset(
            position
            for index, position in enumerate(ordered)
            if mask & (1 << index)
        )
        if all(not (nonzero & union) for union in disjoint_unions):
            surviving_nonzero_sets.add(nonzero)

    assert surviving_nonzero_sets == {
        frozenset(),
        frozenset(((0, 2),)),
    }


def audit_sharp_residual_contradiction() -> None:
    """The two cross-edge zeros put one row on two coordinate lines."""

    left_weight, rho_02, rho_12 = sp.symbols(
        "lambda_left rho_02 rho_12",
        nonzero=True,
    )
    alpha = left_weight * rho_02
    beta = left_weight * rho_12
    u0 = sp.Matrix(sp.symbols("u0_0:3"))
    u1 = sp.Matrix(sp.symbols("u1_0:3"))
    v = sp.Matrix(sp.symbols("v0:3"))
    e0, e1, e2 = (sp.eye(3)[:, color] for color in COLORS)

    # With a=0, b=3, r=1, s=2, the common internal colour is 2.
    assert hessian.internal_color(1, 2) == 2
    assert hessian.internal_color(0, 3) == 2
    assert hessian.internal_color(0, 2) == 1
    assert hessian.internal_color(1, 2) == 2

    pa = (
        sp.zeros(3, 1),
        sp.zeros(3, 1),
        v,
        sp.Matrix(sp.symbols("a3_0:3")),
    )
    pb = (u0, u1, sp.zeros(3, 1), sp.zeros(3, 1))

    def effective_block(
        left: int,
        right: int,
        right_weight: sp.Expr,
    ) -> sp.Matrix:
        color = hessian.internal_color(left, right)
        coordinate = (e0, e1, e2)[color]
        return (
            left_weight * right_weight * coordinate * coordinate.T
            + pa[left] * pb[right].T
            + pb[left] * pa[right].T
        )

    block_02 = effective_block(0, 2, rho_02)
    block_12 = effective_block(1, 2, rho_12)
    assert block_02 == alpha * e1 * e1.T + u0 * v.T
    assert block_12 == beta * e2 * e2.T + u1 * v.T

    # If both blocks vanish, these three entries vanish.  The displayed
    # combination is a division-free certificate alpha*beta=0.
    f_11 = block_02[1, 1]
    f_12 = block_02[1, 2]
    g_22 = block_12[2, 2]
    certificate = sp.expand(
        beta * f_11
        - v[1] * (u0[1] * g_22 - u1[2] * f_12)
    )
    assert certificate == alpha * beta


def audit_k33_local_barrier() -> None:
    """The three-plus-three erasure does not force common-site incidence."""

    identity = sp.eye(3)
    rank_one = sp.diag(1, 0, 0)
    first = (rank_one, rank_one, rank_one, identity)
    second = (rank_one, rank_one, rank_one, identity)
    matrix = hessian.erased_hessian_matrix(
        first,
        second,
        exact_eight.EIGHT_CELLS,
    )
    incident_with_regular_site = exact_eight.edge_columns(
        ((0, 3), (1, 3), (2, 3))
    )
    assert matrix[:, incident_with_regular_site] == sp.zeros(
        matrix.rows,
        len(incident_with_regular_site),
    )
    assert exact_eight.exact_rank(matrix) == 19
    assert len(incident_with_regular_site) == 27


def main() -> None:
    audit_frontier_census()
    audit_local_incidence_patterns()
    audit_sector_identities()
    audit_literal_zero_reduction()
    audit_sharp_residual_contradiction()
    audit_k33_local_barrier()
    print("exact-nine census: 2752 supports in 9 position orbits")
    print("nonsingular-complement PM histogram: 592 / 1344 / 816 (diagnostic only)")
    print("seven overlap-one orbits: common-site endpoint contradiction")
    print("disjoint orbit B: 512 literal-zero branches -> {zero, B_02}")
    print("sharp B residual: weighted alpha*beta polynomial certificate")
    print("K3,3 residual: rank-one local kernel has 27 invisible incident columns")
    print("two-K4 exact-nine frontier reduction: PASS")


if __name__ == "__main__":
    main()
