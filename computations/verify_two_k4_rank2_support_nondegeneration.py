#!/usr/bin/env python3
"""Exact counter-audit to rank-two support degeneration in the two-K4 chart.

One cross block has rank exactly two, with a coordinate zero row and zero
column.  The other fifteen blocks are full-support invertible matrices.  The
script proves that cell support and the usual no-singleton conditions do not
force a low-matching or unique-perfect-matching contraction:

* every coordinate word has at least 18 supported cross-sector monomials;
* all off-diagonal block constants have supported corrections;
* either kernel contraction leaves K_{4,4} minus one edge, with 18 perfect
  matchings; and
* at least six edge deletions are needed to reach a unique-perfect-matching
  subgraph of K_{4,4}, while at least four are needed to destroy all perfect
  matchings.

This is a strict limitation theorem, not a candidate weighted realization.
"""

from __future__ import annotations

from collections import Counter
import itertools


COLORS = tuple(range(3))
LOCAL_VERTICES = tuple(range(4))
GLOBAL_VERTICES = tuple(range(8))
FACTORS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
EDGE_COLOR = {
    tuple(sorted(edge)): color
    for color, factor in enumerate(FACTORS)
    for edge in factor
}


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(GLOBAL_VERTICES))
BIPARTITE_PERMUTATIONS = tuple(itertools.permutations(LOCAL_VERTICES))


def determinant_3(matrix: tuple[tuple[int, ...], ...]) -> int:
    return sum(
        (-1) ** sum(
            permutation[i] > permutation[j]
            for i in COLORS
            for j in COLORS
            if i < j
        )
        * matrix[0][permutation[0]]
        * matrix[1][permutation[1]]
        * matrix[2][permutation[2]]
        for permutation in itertools.permutations(COLORS)
    )


def matrix_vector_product(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in COLORS)
        for row in COLORS
    )


def bilinear(left, matrix, right):
    product = matrix_vector_product(matrix, right)
    return sum(left[row] * product[row] for row in COLORS)


def rank_two_block(zero_row: int, zero_column: int):
    rows = tuple(color for color in COLORS if color != zero_row)
    columns = tuple(color for color in COLORS if color != zero_column)
    matrix = [[0] * 3 for _ in COLORS]
    values = ((1, 1), (1, 2))
    for row_number, row in enumerate(rows):
        for column_number, column in enumerate(columns):
            matrix[row][column] = values[row_number][column_number]
    return tuple(tuple(row) for row in matrix)


FULL_INVERTIBLE_BLOCK = (
    (2, 1, 1),
    (1, 2, 1),
    (1, 1, 2),
)


def compatible_cross_terms(coloring: tuple[int, ...]):
    answer = []
    for matching in MATCHINGS:
        cross_cells = []
        compatible = True
        for u, v in matching:
            if u < 4 <= v:
                cross_cells.append((u, v - 4, coloring[u], coloring[v]))
            else:
                color = (
                    EDGE_COLOR[u, v]
                    if v < 4
                    else EDGE_COLOR[u - 4, v - 4]
                )
                if coloring[u] != color or coloring[v] != color:
                    compatible = False
                    break
        if compatible and cross_cells:
            answer.append(tuple(cross_cells))
    return tuple(answer)


def support_active(cell, zero_row: int, zero_column: int) -> bool:
    left, right, left_color, right_color = cell
    return not (
        left == 0
        and right == 0
        and (left_color == zero_row or right_color == zero_column)
    )


def matching_count(edges: frozenset[tuple[int, int]]) -> int:
    return sum(
        all((left, permutation[left]) in edges for left in LOCAL_VERTICES)
        for permutation in BIPARTITE_PERMUTATIONS
    )


def audit_numeric_ranks_and_kernel_contractions() -> None:
    assert determinant_3(FULL_INVERTIBLE_BLOCK) == 4
    all_ones = (1, 1, 1)
    basis = tuple(
        tuple(int(row == color) for row in COLORS) for color in COLORS
    )

    for zero_row, zero_column in itertools.product(COLORS, repeat=2):
        singular = rank_two_block(zero_row, zero_column)
        assert determinant_3(singular) == 0
        remaining_rows = tuple(color for color in COLORS if color != zero_row)
        remaining_columns = tuple(
            color for color in COLORS if color != zero_column
        )
        minor = (
            tuple(singular[row][column] for column in remaining_columns)
            for row in remaining_rows
        )
        minor = tuple(minor)
        assert minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0] == 1
        assert matrix_vector_product(singular, basis[zero_column]) == (0, 0, 0)
        assert all(
            singular[zero_row][column] == 0 for column in COLORS
        )

        # Contract L_0 by the left kernel and R_0 by the right kernel.  Use
        # all-ones vectors elsewhere.  Exactly the scalar edge (0,0) dies.
        left_vectors = (basis[zero_row],) + (all_ones,) * 3
        right_vectors = (basis[zero_column],) + (all_ones,) * 3
        scalar_edges = set()
        for left, right in itertools.product(LOCAL_VERTICES, repeat=2):
            block = singular if (left, right) == (0, 0) else FULL_INVERTIBLE_BLOCK
            value = bilinear(left_vectors[left], block, right_vectors[right])
            if value:
                scalar_edges.add((left, right))
        assert scalar_edges == {
            (left, right)
            for left, right in itertools.product(LOCAL_VERTICES, repeat=2)
            if (left, right) != (0, 0)
        }
        assert matching_count(frozenset(scalar_edges)) == 18

        # Either one-sided kernel contraction has the same exact support.
        for left_zero, right_zero in ((True, False), (False, True)):
            left_vectors = (
                (basis[zero_row],) + (all_ones,) * 3
                if left_zero
                else (all_ones,) * 4
            )
            right_vectors = (
                (basis[zero_column],) + (all_ones,) * 3
                if right_zero
                else (all_ones,) * 4
            )
            scalar_edges = {
                (left, right)
                for left, right in itertools.product(LOCAL_VERTICES, repeat=2)
                if bilinear(
                    left_vectors[left],
                    singular
                    if (left, right) == (0, 0)
                    else FULL_INVERTIBLE_BLOCK,
                    right_vectors[right],
                )
            }
            assert len(scalar_edges) == 15
            assert (0, 0) not in scalar_edges
            assert matching_count(frozenset(scalar_edges)) == 18


def audit_coordinate_fibres() -> None:
    colorings = tuple(itertools.product(COLORS, repeat=8))
    terms = {
        coloring: compatible_cross_terms(coloring) for coloring in colorings
    }
    off_diagonal_constants = {
        (left_color,) * 4 + (right_color,) * 4
        for left_color, right_color in itertools.product(COLORS, repeat=2)
        if left_color != right_color
    }

    expected_histogram = {
        18: 2200,
        19: 320,
        20: 960,
        21: 80,
        22: 80,
        24: 1760,
        25: 5,
        26: 1024,
        28: 128,
        32: 4,
    }
    for zero_row, zero_column in itertools.product(COLORS, repeat=2):
        counts = {
            coloring: sum(
                all(
                    support_active(cell, zero_row, zero_column)
                    for cell in term
                )
                for term in terms[coloring]
            )
            for coloring in colorings
        }
        assert min(counts.values()) == 18
        assert Counter(counts.values()) == expected_histogram
        assert all(counts[coloring] > 0 for coloring in off_diagonal_constants)
        assert all(
            count != 1
            for coloring, count in counts.items()
            if coloring not in off_diagonal_constants
        )

        # The four-cross scalar support graph is K4,4 or K4,4-e_00 in every
        # coordinate word, so it alone supplies respectively 24 or 18 terms.
        for coloring in colorings:
            missing = coloring[0] == zero_row or coloring[4] == zero_column
            assert sum(
                len(term) == 4
                and all(
                    support_active(cell, zero_row, zero_column)
                    for cell in term
                )
                for term in terms[coloring]
            ) == (18 if missing else 24)


def audit_deletion_thresholds() -> None:
    complete_edges = tuple(itertools.product(LOCAL_VERTICES, repeat=2))
    histogram = Counter()
    maximum_unique_edges = 0
    minimum_no_matching_deletions = 16
    for mask in range(1 << len(complete_edges)):
        edges = frozenset(
            edge
            for bit, edge in enumerate(complete_edges)
            if mask >> bit & 1
        )
        count = matching_count(edges)
        histogram[count] += 1
        if count == 1:
            maximum_unique_edges = max(maximum_unique_edges, len(edges))
        elif count == 0:
            minimum_no_matching_deletions = min(
                minimum_no_matching_deletions, 16 - len(edges)
            )
    assert maximum_unique_edges == 10
    assert minimum_no_matching_deletions == 4
    assert histogram[24] == 1


def main() -> None:
    assert len(MATCHINGS) == 105
    audit_numeric_ranks_and_kernel_contractions()
    audit_coordinate_fibres()
    audit_deletion_thresholds()
    print(
        "PASS: rank2 dense support has fibre minimum 18; "
        "kernel contractions have 18 PMs; unique/no-PM deletion thresholds=6/4"
    )


if __name__ == "__main__":
    main()
