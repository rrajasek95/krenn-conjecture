#!/usr/bin/env python3
"""Exact audits for the two-by-two checkerboard Hessian erasure.

The disjoint calculation has first-star exceptions {0,1} and second-star
exceptions {2,3}.  The overlap-one audit has exception sets {0,3} and
{1,3}; full injectivity is false there, while the finite specializations
below have zero kernel blocks on the three edges incident with common site 3.
"""

from __future__ import annotations

import itertools
from collections import Counter

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_two_k4_four_singular_matching_hessian_obstruction as hessian
import verify_two_k4_six_cycle_two_defect_obstruction as two_defect


SITES = hessian.SITES
COLORS = hessian.COLORS
EDGES = hessian.EDGES
WORDS = hessian.WORDS
DOMAIN = tuple(
    (edge, left, right)
    for edge in EDGES
    for left in COLORS
    for right in COLORS
)
EIGHT_CELLS = tuple(
    (x, y)
    for x, y in itertools.product(COLORS, repeat=2)
    if (x, y) != (0, 0)
)


def exact_rank(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).rank()


def edge_columns(edges) -> tuple[int, ...]:
    edges = frozenset(tuple(sorted(edge)) for edge in edges)
    return tuple(
        column
        for column, (edge, _left, _right) in enumerate(DOMAIN)
        if edge in edges
    )


def audit_disjoint_four_branches() -> None:
    """The four zero/nonzero branches have kernels 0, 9, 9, and 18."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    active = sp.diag(1, 0, 0)
    edge_01 = edge_columns(((0, 1),))
    edge_23 = edge_columns(((2, 3),))

    cases = (
        ((active, zero), (active, zero), ()),
        ((zero, zero), (active, zero), ((2, 3),)),
        ((active, zero), (zero, zero), ((0, 1),)),
        ((zero, zero), (zero, zero), ((0, 1), (2, 3))),
    )
    for (first_0, first_1), (second_2, second_3), residual in cases:
        matrix = hessian.erased_hessian_matrix(
            (first_0, first_1, identity, identity),
            (identity, identity, second_2, second_3),
            EIGHT_CELLS,
        )
        residual_columns = edge_columns(residual)
        other_columns = tuple(
            column
            for column in range(len(DOMAIN))
            if column not in residual_columns
        )
        assert matrix[:, residual_columns] == sp.zeros(
            matrix.rows, len(residual_columns)
        )
        assert exact_rank(matrix[:, other_columns]) == len(other_columns)
        assert exact_rank(matrix) == 54 - len(residual_columns)

    # The smallest active specialization has a unimodular maximal minor.
    minimal = hessian.erased_hessian_matrix(
        (active, zero, identity, identity),
        (identity, identity, active, zero),
        EIGHT_CELLS,
    )
    pivot_rows = hessian.modular_pivot_rows(minimal, 2)
    assert len(pivot_rows) == 54
    assert abs(int(minimal[pivot_rows, :].det(method="domain-ge"))) == 1

    assert len(edge_01) == len(edge_23) == 9


def audit_disjoint_normal_forms() -> None:
    """Exercise zero/rank-one/rank-two maps and relative incidences."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    defects = (
        zero,
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.diag(1, 1, 0),
        sp.Matrix([[0, 1, 2], [0, 2, 4], [0, 0, 0]]),
    )
    audited = 0
    for first_0, first_1, second_2, second_3 in itertools.product(
        defects, repeat=4
    ):
        matrix = hessian.erased_hessian_matrix(
            (first_0, first_1, identity, identity),
            (identity, identity, second_2, second_3),
            EIGHT_CELLS,
        )
        expected = 54
        if first_0 == zero and first_1 == zero:
            expected -= 9
        if second_2 == zero and second_3 == zero:
            expected -= 9
        assert exact_rank(matrix) == expected
        audited += 1
    assert audited == 625

    # None of the regular maps is the identity, and the four exceptional
    # maps have unrelated kernels and images.
    first = (
        sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]]),
        sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 2, 0]]),
        sp.Matrix([[1, 0, 1], [1, 2, 0], [0, 1, 1]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 2]]),
    )
    second = (
        sp.Matrix([[1, 1, 0], [1, 2, 1], [0, 1, 2]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
        sp.Matrix([[1, 0, 1], [0, 0, 0], [2, 0, 2]]),
        sp.Matrix([[0, 1, 2], [0, 2, 4], [0, 0, 0]]),
    )
    assert all(first[site].det() != 0 for site in (2, 3))
    assert all(second[site].det() != 0 for site in (0, 1))
    assert all(first[site].det() == 0 for site in (0, 1))
    assert all(second[site].det() == 0 for site in (2, 3))
    relative = hessian.erased_hessian_matrix(first, second, EIGHT_CELLS)
    assert exact_rank(relative) == 54


def audit_overlap_one_incidence_and_counterexample() -> None:
    """Full injectivity fails; audited common-site incident blocks vanish."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    defects = (
        zero,
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.diag(1, 1, 0),
        sp.Matrix([[0, 1, 2], [0, 2, 4], [0, 0, 0]]),
    )
    away_from_common = tuple(
        column
        for column, (edge, _left, _right) in enumerate(DOMAIN)
        if 3 not in edge
    )
    audited = 0
    for first_0, first_3, second_1, second_3 in itertools.product(
        defects, repeat=4
    ):
        matrix = hessian.erased_hessian_matrix(
            (first_0, identity, identity, first_3),
            (identity, second_1, identity, second_3),
            EIGHT_CELLS,
        )
        # ker(matrix) is contained in the 27 coordinates on triangle 012
        # iff adjoining the 27 site-3 columns raises rank by exactly 27.
        assert exact_rank(matrix) - exact_rank(matrix[:, away_from_common]) == 27
        audited += 1
    assert audited == 625

    # Exact rank-53 counterexample to the tempting overlap-one injectivity
    # extension.  All four displayed exceptional matrices are singular and
    # both exceptional pairs are nonzero.
    first = (
        sp.Matrix([[-1, 0, 2], [3, 2, -1], [-2, 0, 4]]),
        identity,
        identity,
        sp.Matrix([[2, 0, 0], [0, 0, 0], [2, 0, 0]]),
    )
    second = (
        identity,
        sp.Matrix([[0, 0, 0], [-2, -2, 2], [-4, -4, -6]]),
        identity,
        zero,
    )
    assert [first[site].rank() for site in (0, 3)] == [2, 1]
    assert [second[site].rank() for site in (1, 3)] == [2, 0]
    matrix = hessian.erased_hessian_matrix(first, second, EIGHT_CELLS)
    assert exact_rank(matrix) == 53

    vector = sp.zeros(54, 1)
    entries = {
        ((0, 1), 1, 1): -2,
        ((0, 1), 1, 2): 6,
        ((0, 1), 2, 1): -2,
        ((0, 1), 2, 2): -4,
        ((0, 2), 1, 2): 1,
        ((0, 2), 2, 1): -1,
        ((1, 2), 1, 1): 2,
        ((1, 2), 1, 2): 2,
        ((1, 2), 2, 1): -6,
        ((1, 2), 2, 2): 4,
    }
    for key, value in entries.items():
        vector[DOMAIN.index(key)] = value
    assert matrix * vector == sp.zeros(matrix.rows, 1)
    assert all(
        vector[column] == 0
        for column, (edge, _left, _right) in enumerate(DOMAIN)
        if 3 in edge
    )


def degrees(support, side: int) -> tuple[int, ...]:
    return tuple(
        sum(position[side] == vertex for position in support)
        for vertex in SITES
    )


def erased_by_separated_one_two(support) -> bool:
    """Lemma 6.1 of the exact-seven note, on either shore."""

    for transpose in (False, True):
        oriented = (
            frozenset((column, row) for row, column in support)
            if transpose
            else support
        )
        local_degrees = degrees(oriented, 0)
        for singleton in (
            vertex for vertex in SITES if local_degrees[vertex] == 1
        ):
            singleton_defect = next(
                column for row, column in oriented if row == singleton
            )
            for row in (
                vertex for vertex in SITES if local_degrees[vertex] == 2
            ):
                defects = {
                    column
                    for current, column in oriented
                    if current == row
                }
                if singleton_defect not in defects:
                    return True
    return False


C4_C4 = frozenset(
    ((0, 0), (0, 1), (1, 0), (1, 1),
     (2, 2), (2, 3), (3, 2), (3, 3))
)
C8 = frozenset(
    ((0, 0), (0, 1), (1, 0), (1, 2),
     (2, 1), (2, 3), (3, 2), (3, 3))
)
OVERLAP_ONE = frozenset(
    ((0, 0), (0, 1), (0, 2), (1, 0),
     (1, 3), (2, 1), (2, 3), (3, 3))
)


def audit_exact_eight_census() -> None:
    cells = tuple(itertools.product(SITES, repeat=2))
    after_seven = tuple(
        frozenset(support)
        for support in itertools.combinations(cells, 8)
        if two_defect.survives_pre_seven_rules(frozenset(support))
    )
    assert len(after_seven) == 4698

    frontier = tuple(
        support
        for support in after_seven
        if not erased_by_separated_one_two(support)
    )
    assert len(frontier) == 378
    orbits = Counter(
        two_defect.canonical_support(support) for support in frontier
    )
    assert orbits == Counter({
        tuple(sorted(C4_C4)): 18,
        tuple(sorted(C8)): 72,
        tuple(sorted(OVERLAP_ONE)): 288,
    })

    # The two 2-regular representatives have disjoint degree-two row pairs.
    for support, rows in ((C4_C4, (0, 2)), (C8, (0, 3))):
        exceptional = tuple(
            {column for current, column in support if current == row}
            for row in rows
        )
        assert len(exceptional[0]) == len(exceptional[1]) == 2
        assert exceptional[0].isdisjoint(exceptional[1])

    # The last representative has overlap-one pairs with common site 3.
    exceptional = tuple(
        {column for current, column in OVERLAP_ONE if current == row}
        for row in (1, 2)
    )
    assert exceptional == ({0, 3}, {1, 3})

    # In the all-literal-zero branch of either 2-regular mask, the two
    # complementary rows have zero sets covering every right site.  Hence
    # every two-column matrix Z_v in the two-edge-star normal form has rank
    # at most one, contradicting its forced rank-two centre.
    for support, complementary_rows in ((C4_C4, (1, 3)), (C8, (1, 2))):
        zero_sets = tuple(
            {column for current, column in support if current == row}
            for row in complementary_rows
        )
        assert zero_sets[0] | zero_sets[1] == set(SITES)


def audit_sector_identity(support, r: int, s: int) -> int:
    """Audit the actual two/four-cross pullback for one row pair."""

    blocks = two_defect.make_support_blocks(support)
    a, b = tuple(site for site in SITES if site not in (r, s))
    color = hessian.internal_color(a, b)
    assert color == hessian.internal_color(r, s)

    q_right = {}
    for u, v in EDGES:
        edge_color = hessian.internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][edge_color, edge_color] = 1
    pa = {site: blocks[a, site].row(color) for site in SITES}
    pb = {site: blocks[b, site].row(color) for site in SITES}
    q_effective = {
        (u, v): q_right[u, v] + pa[u].T * pb[v] + pb[u].T * pa[v]
        for u, v in EDGES
    }

    checked = 0
    for x, y in itertools.product(COLORS, repeat=2):
        left_word = [None] * 4
        left_word[a] = left_word[b] = color
        left_word[r], left_word[s] = x, y
        left_word = tuple(left_word)
        first = {site: blocks[r, site].row(x) for site in SITES}
        second = {site: blocks[s, site].row(y) for site in SITES}
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
                two_cross += hessian.permanent([
                    [
                        blocks[left, right][left_word[left], right_word[right]]
                        for right in remaining
                    ]
                    for left in (r, s)
                ])
            pulled_back = hessian.beta_coefficient(
                q_effective, first, second, right_word
            )
            assert sp.expand(pulled_back - four_cross - two_cross) == 0
            checked += 1
    assert checked == 729
    return checked


def audit_frontier_sector_identities() -> None:
    checked = 0
    checked += audit_sector_identity(C4_C4, 0, 2)
    checked += audit_sector_identity(C8, 0, 3)
    checked += audit_sector_identity(OVERLAP_ONE, 1, 2)
    assert checked == 2187


def main() -> None:
    audit_disjoint_four_branches()
    audit_disjoint_normal_forms()
    audit_overlap_one_incidence_and_counterexample()
    audit_exact_eight_census()
    audit_frontier_sector_identities()
    print("disjoint two-plus-two kernels: 0/9/9/18 exactly")
    print("minimal active disjoint minor: determinant 1")
    print("overlap-one injectivity: FALSE (exact rank-53 counterexample)")
    print("overlap-one common-site incident blocks: zero in all audited strata")
    print("exact-eight census: 4698 -> 378 = 18 + 72 + 288")
    print("exact-eight sector identities: 2187 exact coefficients")
    print("two-K4 exact-eight checkerboard Hessian audit: PASS")


if __name__ == "__main__":
    main()
