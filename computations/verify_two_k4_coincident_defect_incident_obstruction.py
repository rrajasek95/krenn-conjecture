#!/usr/bin/env python3
"""Exact audits for the coincident-defect incident-erasure obstruction."""

from __future__ import annotations

import itertools
from collections import Counter

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

import verify_two_k4_exact_four_nonmatching_obstruction as one_defect
import verify_two_k4_four_singular_matching_hessian_obstruction as separated


SITES = separated.SITES
COLORS = separated.COLORS
EDGES = separated.EDGES
WORDS = separated.WORDS


def quadratic_domain():
    return [
        (edge, left, right)
        for edge in EDGES
        for left in COLORS
        for right in COLORS
    ]


def incident_selector(site: int) -> sp.Matrix:
    """Coordinate projection from R_2 to blocks incident with ``site``."""

    domain = quadratic_domain()
    incident = [
        column
        for column, (edge, _left, _right) in enumerate(domain)
        if site in edge
    ]
    selector = sp.zeros(len(incident), len(domain))
    for row, column in enumerate(incident):
        selector[row, column] = 1
    assert selector.shape == (27, 54)
    return selector


def assert_incident_erased(matrix: sp.Matrix, site: int) -> None:
    """Check ker(matrix) is contained in the zero-incident subspace."""

    selector = incident_selector(site)
    assert matrix.cols == selector.cols == 54
    assert matrix.rank() == matrix.col_join(selector).rank()


def audit_almost_star_annihilator() -> None:
    """Reuse the exact rank and generator audit behind equation (7)."""

    one_defect.audit_one_defect_annihilator()


def three_leg_matrix() -> sp.Matrix:
    """Map the three incident blocks to the three pair equations (14)."""

    good = (1, 2, 3)
    domain = [
        (site, h_color, site_color)
        for site in good
        for h_color in COLORS
        for site_color in COLORS
    ]
    rows = []
    for i, j in itertools.combinations(good, 2):
        for h_color, i_color, j_color in itertools.product(COLORS, repeat=3):
            row = []
            for site, left, right in domain:
                value = 0
                if (
                    site == i
                    and left == h_color
                    and right == i_color
                    and j_color == 0
                ):
                    value += 1
                if (
                    site == j
                    and left == h_color
                    and right == j_color
                    and i_color == 0
                ):
                    value += 1
                row.append(value)
            rows.append(row)
    return sp.Matrix(rows)


def audit_three_leg_cancellation() -> None:
    matrix = three_leg_matrix()
    assert matrix.shape == (81, 27)
    assert matrix.rank() == 27

    # The Smith form records exactly where characteristic != 2 is used:
    # 24 unit pivots and three pivots equal to two.
    smith = smith_normal_form(matrix, domain=sp.ZZ)
    invariants = [
        abs(int(smith[index, index]))
        for index in range(min(smith.shape))
        if smith[index, index]
    ]
    assert Counter(invariants) == Counter({1: 24, 2: 3})

    pivot_rows = separated.modular_pivot_rows(matrix, 3)
    assert len(pivot_rows) == 27
    assert abs(int(matrix[pivot_rows, :].det())) == 8


def audit_oriented_incident_erasure() -> None:
    """Exact six-cell ranks with a nonzero unrestricted defect."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    h = 0
    six_cells = tuple((x, y) for x in (1, 2) for y in COLORS)

    first_defects = (
        zero,
        sp.diag(1, 0, 0),  # kills the restricted two-plane
        sp.diag(0, 1, 0),
        sp.diag(1, 1, 0),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]]),
    )
    nonzero_second_defects = (
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.diag(1, 1, 0),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]]),
    )

    audited = 0
    for first_defect, second_defect in itertools.product(
        first_defects, nonzero_second_defects
    ):
        first = [identity] * 4
        second = [identity] * 4
        first[h] = first_defect
        second[h] = second_defect
        matrix = separated.erased_hessian_matrix(
            tuple(first), tuple(second), six_cells
        )
        assert_incident_erased(matrix, h)
        expected_rank = (
            53
            if first_defect[:, 1:3] == sp.zeros(3, 2)
            else 54
        )
        assert matrix.rank() == expected_rank
        audited += 1
    assert audited == 20


def audit_zero_zero_branch() -> None:
    """With both defects zero, precisely the regular triangle is invisible."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    h = 0
    six_cells = tuple((x, y) for x in (1, 2) for y in COLORS)
    first = [identity] * 4
    second = [identity] * 4
    first[h] = second[h] = zero
    matrix = separated.erased_hessian_matrix(
        tuple(first), tuple(second), six_cells
    )

    domain = quadratic_domain()
    regular = [
        column
        for column, (edge, _left, _right) in enumerate(domain)
        if h not in edge
    ]
    incident = [column for column in range(54) if column not in regular]
    assert len(regular) == len(incident) == 27
    assert matrix[:, regular] == sp.zeros(matrix.rows, len(regular))
    assert matrix[:, incident].rank() == 27
    assert matrix.rank() == 27
    assert_incident_erased(matrix, h)


def audit_unoriented_eight_cell_erasure() -> None:
    """Audit orientation by either star, including two zero defects."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    h = 0
    eight_cells = tuple(
        (x, y)
        for x, y in itertools.product(COLORS, repeat=2)
        if (x, y) != (0, 0)
    )
    defects = (
        zero,
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.diag(1, 1, 0),
    )

    ranks = Counter()
    for first_defect, second_defect in itertools.product(defects, repeat=2):
        first = [identity] * 4
        second = [identity] * 4
        first[h] = first_defect
        second[h] = second_defect
        matrix = separated.erased_hessian_matrix(
            tuple(first), tuple(second), eight_cells
        )
        assert_incident_erased(matrix, h)
        ranks[matrix.rank()] += 1

    # Coincident defects genuinely differ from separated defects: full
    # erasure can leave classes supported on the regular triangle.
    assert ranks == Counter({54: 12, 53: 3, 27: 1})

    # One relabelled-site audit prevents an accidental hard-coding of h=0.
    h = 2
    first = [identity] * 4
    second = [identity] * 4
    first[h] = zero
    second[h] = sp.diag(1, 0, 0)
    matrix = separated.erased_hessian_matrix(
        tuple(first), tuple(second), eight_cells
    )
    assert_incident_erased(matrix, h)

    # A nontrivial relative-basis chart at all three regular sites.
    h = 0
    first = (
        sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]]),
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[1, 0, 1], [1, 2, 0], [0, 1, 1]]),
    )
    second = (
        sp.Matrix([[1, 0, 0], [2, 1, 0], [3, 2, 0]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[1, 0, 1], [2, 1, 0], [0, 1, 1]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
    )
    assert all(first[site].det() != 0 for site in (1, 2, 3))
    assert all(second[site].det() != 0 for site in (1, 2, 3))
    matrix = separated.erased_hessian_matrix(first, second, eight_cells)
    assert matrix.rank() == 54
    assert_incident_erased(matrix, h)

    zero_first = list(first)
    zero_second = list(second)
    zero_first[h] = zero
    zero_second[h] = zero
    matrix = separated.erased_hessian_matrix(
        tuple(zero_first), tuple(zero_second), eight_cells
    )
    assert matrix.rank() == 27
    assert_incident_erased(matrix, h)


EXACT_SIX_SUPPORT = {
    (0, 0), (0, 1),
    (1, 0), (1, 3),
    (2, 2), (3, 2),
}


def make_exact_six_blocks(shared_zero: bool) -> dict[tuple[int, int], sp.Matrix]:
    blocks = {}
    for i, j in itertools.product(SITES, repeat=2):
        matrix = sp.Matrix([
            [i + 1, j + 1, 1],
            [0, i + j + 2, j + 2],
            [0, 0, i + 2],
        ])
        assert matrix.det() != 0
        blocks[i, j] = matrix

    for position in EXACT_SIX_SUPPORT:
        blocks[position][2, 2] = 0
        assert blocks[position].rank() == 2

    # Exercise both orientations of the proof and its all-zero branch.
    if shared_zero:
        blocks[2, 2] = sp.zeros(3)
        blocks[3, 2] = sp.zeros(3)
    else:
        blocks[2, 2] = sp.Matrix([[1, 2, 3], [0, 0, 0], [0, 0, 0]])
        blocks[3, 2] = sp.diag(1, 1, 0)

    actual_singular = {
        position for position, matrix in blocks.items() if matrix.det() == 0
    }
    assert actual_singular == EXACT_SIX_SUPPORT
    return blocks


def audit_two_k4_sector_identity() -> None:
    a, b, r, s = 0, 1, 2, 3
    h = 2
    c = separated.internal_color(a, b)
    assert c == 0 and separated.internal_color(r, s) == c

    q_right = {}
    for u, v in EDGES:
        color = separated.internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][color, color] = 1

    checked = 0
    for shared_zero in (False, True):
        blocks = make_exact_six_blocks(shared_zero)
        pa = {site: blocks[a, site].row(c) for site in SITES}
        pb = {site: blocks[b, site].row(c) for site in SITES}
        q_effective = {
            (u, v): (
                q_right[u, v]
                + pa[u].T * pb[v]
                + pb[u].T * pa[v]
            )
            for u, v in EDGES
        }

        for x, y in itertools.product(COLORS, repeat=2):
            left_word = [None] * 4
            left_word[a] = left_word[b] = c
            left_word[r], left_word[s] = x, y
            left_word = tuple(left_word)
            first = {site: blocks[r, site].row(x) for site in SITES}
            second = {site: blocks[s, site].row(y) for site in SITES}

            for right_word in WORDS:
                four_cross = separated.permanent([
                    [
                        blocks[left, right][left_word[left], right_word[right]]
                        for right in SITES
                    ]
                    for left in SITES
                ])
                two_cross = 0
                for u, v in EDGES:
                    color = separated.internal_color(u, v)
                    if (
                        right_word[u] != color
                        or right_word[v] != color
                    ):
                        continue
                    remaining = tuple(
                        site for site in SITES if site not in (u, v)
                    )
                    two_cross += separated.permanent([
                        [
                            blocks[left, right][left_word[left], right_word[right]]
                            for right in remaining
                        ]
                        for left in (r, s)
                    ])
                pulled_back = separated.beta_coefficient(
                    q_effective, first, second, right_word
                )
                assert sp.expand(
                    pulled_back - four_cross - two_cross
                ) == 0
                checked += 1

        assert all(
            blocks[r, site].det() != 0
            and blocks[s, site].det() != 0
            for site in SITES
            if site != h
        )

        endpoint_lines = [
            sp.eye(3)[:, separated.internal_color(h, other)]
            for other in SITES
            if other != h
        ]
        product_plane = sp.Matrix.hstack(pa[h].T, pb[h].T)
        assert sp.Matrix.hstack(*endpoint_lines).rank() == 3
        assert product_plane.rank() <= 2

    assert checked == 2 * 729


def audit_position_counts() -> None:
    cells = tuple(itertools.product(SITES, repeat=2))
    row_pattern = []
    shared_singletons = []
    shared_and_all_columns = []
    combined_survivors = []

    for support in itertools.combinations(cells, 6):
        row_degrees = tuple(
            sum(row == vertex for row, _column in support)
            for vertex in SITES
        )
        column_degrees = tuple(
            sum(column == vertex for _row, column in support)
            for vertex in SITES
        )
        if (
            sum(degree <= 1 for degree in row_degrees) <= 1
            and sum(degree <= 1 for degree in column_degrees) <= 1
        ):
            combined_survivors.append(support)

        if sorted(row_degrees) != [1, 1, 2, 2]:
            continue
        row_pattern.append(support)
        singleton_rows = tuple(
            row for row, degree in enumerate(row_degrees) if degree == 1
        )
        singleton_columns = tuple(
            next(column for row, column in support if row == singleton)
            for singleton in singleton_rows
        )
        if singleton_columns[0] != singleton_columns[1]:
            continue
        shared_singletons.append(support)
        if all(column_degrees):
            shared_and_all_columns.append(support)

    assert len(row_pattern) == 3456
    assert len(shared_singletons) == 864
    assert len(shared_and_all_columns) == 288
    assert tuple(sorted(EXACT_SIX_SUPPORT)) in shared_and_all_columns
    assert len(combined_survivors) == 96
    assert all(
        sorted(
            sum(position[side] == vertex for position in support)
            for vertex in SITES
        ) == [0, 2, 2, 2]
        for support in combined_survivors
        for side in (0, 1)
    )


def main() -> None:
    audit_almost_star_annihilator()
    audit_three_leg_cancellation()
    audit_oriented_incident_erasure()
    audit_zero_zero_branch()
    audit_unoriented_eight_cell_erasure()
    audit_two_k4_sector_identity()
    audit_position_counts()
    print("almost-star annihilator: dimensions 27,1,1,1")
    print("three-leg Smith invariants: 1^24, 2^3")
    print("coincident-defect incident erasure: exact normal forms PASS")
    print("exact-six effective-sector identities: 1458 coefficients")
    print("row pattern (2,2,1,1): 3456 supports, 864 shared-singleton")
    print("combined sparse-pair boundary: 8008 -> 96 six-cycles")
    print("coincident singleton-column obstruction: PASS")


if __name__ == "__main__":
    main()
