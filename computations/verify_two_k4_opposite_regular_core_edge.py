#!/usr/bin/env python3
"""Exact audits for the opposite-regular/common-core Hessian boundary.

The local pattern has two common exceptional sites 0,1, an invertible
second-star component at site 2, and an invertible first-star component at
site 3.  The candidate invariant statement is that eight-cell erasure forces
the quadratic block q_01 to vanish.  The finite normal-form audit below is
evidence for that statement, not a substitute for its missing invariant
coefficient proof.  The literal-zero kernel and all sector identities checked
here are complete exact statements.
"""

from __future__ import annotations

import itertools
from collections import Counter

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_two_k4_exact_eight_checkerboard_hessian as exact_eight
import verify_two_k4_four_singular_matching_hessian_obstruction as hessian
import verify_two_k4_four_singular_row_obstruction as sector


SITES = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
WORDS = tuple(itertools.product(COLORS, repeat=4))
DOMAIN = exact_eight.DOMAIN
EIGHT_CELLS = exact_eight.EIGHT_CELLS


def exact_rank(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).rank()


def columns_on(edge: tuple[int, int]) -> tuple[int, ...]:
    return tuple(
        column
        for column, (current, _left, _right) in enumerate(DOMAIN)
        if current == edge
    )


CORE_COLUMNS = columns_on((0, 1))
AWAY_COLUMNS = tuple(
    column for column in range(len(DOMAIN)) if column not in CORE_COLUMNS
)


def opposite_regular_matrix(
    maps: tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    """Return the eight-cell map for P0,P1,P2,S0,S1,S3."""

    p0, p1, p2, s0, s1, s3 = maps
    identity = sp.eye(3)
    return hessian.erased_hessian_matrix(
        (p0, p1, p2, identity),
        (s0, s1, identity, s3),
        EIGHT_CELLS,
    )


def core_projection_dimension(matrix: sp.Matrix) -> int:
    """Dimension of the kernel projection to the q_01 coordinates."""

    # This is dim ker(M|away quotient), equivalently the rank increment when
    # the nine core columns are adjoined.
    return exact_rank(matrix) - exact_rank(matrix[:, AWAY_COLUMNS])


def audit_literal_zero_kernel() -> None:
    """With all six exceptional maps zero, only q_01 is visible."""

    zero = sp.zeros(3)
    matrix = opposite_regular_matrix((zero,) * 6)
    assert exact_rank(matrix) == 9
    assert exact_rank(matrix[:, CORE_COLUMNS]) == 9
    assert matrix[:, AWAY_COLUMNS] == sp.zeros(matrix.rows, len(AWAY_COLUMNS))
    assert core_projection_dimension(matrix) == 9


def audit_rank_normal_forms() -> Counter[int]:
    """Audit all 3^6 simultaneous zero/rank-one/rank-two diagonal forms."""

    forms = (
        sp.zeros(3),
        sp.diag(1, 0, 0),
        sp.diag(1, 1, 0),
    )
    ranks: Counter[int] = Counter()
    audited = 0
    for indices in itertools.product(range(3), repeat=6):
        matrix = opposite_regular_matrix(tuple(forms[index] for index in indices))
        rank = exact_rank(matrix)
        assert rank - exact_rank(matrix[:, AWAY_COLUMNS]) == 9
        ranks[rank] += 1
        audited += 1
    assert audited == 729
    return ranks


def audit_relative_bases() -> None:
    """Exercise unrelated kernels, images, and non-diagonal rank profiles."""

    zero = sp.zeros(3)
    forms = (
        zero,
        sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]]),
        sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 2, 0]]),
        sp.Matrix([[1, 0, 1], [0, 0, 0], [2, 0, 2]]),
        sp.Matrix([[0, 1, 2], [0, 2, 4], [1, 0, 1]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 3, 1]]),
    )
    assert all(matrix.det() == 0 for matrix in forms)
    for shift in range(18):
        maps = tuple(forms[(shift + 2 * index) % len(forms)] for index in range(6))
        matrix = opposite_regular_matrix(maps)
        assert core_projection_dimension(matrix) == 9


def representative_blocks() -> dict[tuple[int, int], sp.Matrix]:
    """A rank-two/invertible realization of the displayed ten-position mask."""

    singular = {
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 3),
        (2, 2), (2, 3),
        (3, 2), (3, 3),
    }
    blocks: dict[tuple[int, int], sp.Matrix] = {}
    for row, column in itertools.product(SITES, repeat=2):
        matrix = sp.Matrix(
            [
                [row + 1, column + 1, 1],
                [0, row + column + 2, column + 2],
                [0, 0, row + 2],
            ]
        )
        if (row, column) in singular:
            matrix[2, 2] = 0
            assert matrix.rank() == 2
        else:
            assert matrix.det() != 0
        blocks[row, column] = matrix
    return blocks


def standard_quadratic() -> dict[tuple[int, int], sp.Matrix]:
    result = {}
    for edge in EDGES:
        color = sector.internal_color(*edge)
        result[edge] = sp.zeros(3)
        result[edge][color, color] = 1
    return result


def effective_quadratic_from_rows(
    blocks: dict[tuple[int, int], sp.Matrix],
    first: int,
    second: int,
    color: int,
) -> dict[tuple[int, int], sp.Matrix]:
    q_standard = standard_quadratic()
    first_star = {site: blocks[first, site].row(color) for site in SITES}
    second_star = {site: blocks[second, site].row(color) for site in SITES}
    return {
        (u, v): q_standard[u, v]
        + first_star[u].T * second_star[v]
        + second_star[u].T * first_star[v]
        for u, v in EDGES
    }


def audit_sector_identity() -> None:
    """Check the exact 2/4-cross pullback for rows 0,1 of the mask."""

    blocks = representative_blocks()
    variable_rows = (0, 1)
    fixed_rows = (2, 3)
    color = sector.internal_color(*fixed_rows)
    q_effective = effective_quadratic_from_rows(
        blocks, fixed_rows[0], fixed_rows[1], color
    )

    checked = 0
    for x, y in itertools.product(COLORS, repeat=2):
        left_word = (x, y, color, color)
        first_star = {site: blocks[0, site].row(x) for site in SITES}
        second_star = {site: blocks[1, site].row(y) for site in SITES}
        for right_word in WORDS:
            four_cross = sector.permanent(
                [
                    [blocks[row, column][left_word[row], right_word[column]]
                     for column in SITES]
                    for row in SITES
                ]
            )
            two_cross = 0
            for u, v in EDGES:
                edge_color = sector.internal_color(u, v)
                if right_word[u] != edge_color or right_word[v] != edge_color:
                    continue
                remaining = tuple(site for site in SITES if site not in (u, v))
                two_cross += sector.permanent(
                    [
                        [blocks[row, site][left_word[row], right_word[site]]
                         for site in remaining]
                        for row in variable_rows
                    ]
                )
            pulled_back = sector.beta_coefficient(
                q_effective, first_star, second_star, right_word
            )
            assert sp.expand(pulled_back - two_cross - four_cross) == 0
            checked += 1
    assert checked == 729


def literal_zero_blocks() -> dict[tuple[int, int], sp.Matrix]:
    """Six invertible blocks and ten literal zeros in the displayed mask."""

    blocks = {
        position: sp.zeros(3)
        for position in itertools.product(SITES, repeat=2)
    }
    identity = sp.eye(3)
    blocks[0, 3] = identity
    blocks[1, 2] = identity
    blocks[2, 0] = identity
    blocks[2, 1] = identity
    blocks[3, 0] = identity
    blocks[3, 1] = -2 * identity
    return blocks


def audit_sharp_sector_countermodel() -> None:
    """The core equations on both shores admit the literal-zero mask."""

    blocks = literal_zero_blocks()
    color = sector.internal_color(2, 3)
    assert color == sector.internal_color(0, 1)

    q_right = effective_quadratic_from_rows(blocks, 2, 3, color)
    assert q_right[0, 1] == sp.zeros(3)
    for x, y in itertools.product(COLORS, repeat=2):
        first_star = {site: blocks[0, site].row(x) for site in SITES}
        second_star = {site: blocks[1, site].row(y) for site in SITES}
        for word in WORDS:
            assert sector.beta_coefficient(
                q_right, first_star, second_star, word
            ) == 0

    # Transpose the construction.  Columns 0,1 are fixed to the same color;
    # columns 2,3 are the two opposite-regular variable stars.
    transposed = {
        (row, column): blocks[column, row].T
        for row, column in itertools.product(SITES, repeat=2)
    }
    q_left = effective_quadratic_from_rows(transposed, 0, 1, color)
    assert q_left[2, 3] == sp.zeros(3)
    for x, y in itertools.product(COLORS, repeat=2):
        first_star = {site: transposed[2, site].row(x) for site in SITES}
        second_star = {site: transposed[3, site].row(y) for site in SITES}
        for word in WORDS:
            assert sector.beta_coefficient(
                q_left, first_star, second_star, word
            ) == 0


def main() -> None:
    audit_literal_zero_kernel()
    ranks = audit_rank_normal_forms()
    audit_relative_bases()
    audit_sector_identity()
    audit_sharp_sector_countermodel()
    print("opposite-regular literal-zero kernel: rank 9, residual dimension 45")
    print(
        "opposite-regular normal forms: 729 core projections of dimension 9; "
        f"full ranks {dict(sorted(ranks.items()))}"
    )
    print("opposite-regular unrelated-basis audits: 18 exact cases")
    print("displayed ten-position 2/4-cross sector identity: 729 coefficients")
    print("literal-zero two-shore core-sector countermodel: PASS")


if __name__ == "__main__":
    main()
