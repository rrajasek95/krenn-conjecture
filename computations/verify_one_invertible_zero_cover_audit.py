#!/usr/bin/env python3
"""Independent exact audit of the local algebra in Lemma 6.6.

After using the invertible p-x block to set a_c=e_c, the six equations are

    e_c S_d^T + b_d P_c^T = lambda_cd A,       c != d.

The second star b_0,b_1,b_2 is completely arbitrary.  Right changes of
basis let us replace A by one canonical matrix for each of its column
spaces.  Scaling a nonzero b_d does not change row support, so finite-field
searches need only one representative for each projective b_d.

This file does not import the verifier accompanying the main note.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product


PAIR_ORDER = tuple(
    (c, d) for c in range(3) for d in range(3) if c != d
)
VARIABLE_COUNT = 24  # 9 P entries, 9 S entries, and 6 lambdas
RATIONAL_CERTIFICATE_PRIME = (1 << 61) - 1


def dot(left, right, modulus=None):
    value = sum(x * y for x, y in zip(left, right, strict=True))
    return value if modulus is None else value % modulus


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def determinant_of_columns(columns, modulus=None):
    first, second, third = columns
    value = dot(first, cross(second, third))
    return value if modulus is None else value % modulus


def finite_projective_representatives(modulus):
    representatives = [(0, 0, 0)]
    for vector in product(range(modulus), repeat=3):
        if not any(vector):
            continue
        first = next(index for index, entry in enumerate(vector) if entry)
        inverse = pow(vector[first], -1, modulus)
        normalized = tuple(entry * inverse % modulus for entry in vector)
        if normalized not in representatives:
            representatives.append(normalized)
    return tuple(representatives)


def bounded_rational_projective_representatives():
    """The zero vector and the 13 normalized {-1,0,1} projective vectors."""
    representatives = [(0, 0, 0)]
    for vector in product((-1, 0, 1), repeat=3):
        if not any(vector):
            continue
        first = next(index for index, entry in enumerate(vector) if entry)
        normalized = vector if vector[first] == 1 else tuple(-x for x in vector)
        if normalized not in representatives:
            representatives.append(normalized)
    assert len(representatives) == 14
    return tuple(representatives)


def canonical_blocks(projective_lines, *, modulus=None):
    """One right-equivalence representative for every selected image space."""
    blocks = [(0, ((0, 0, 0), (0, 0, 0), (0, 0, 0)))]

    for image_vector in projective_lines:
        block = tuple(
            tuple(image_vector[row] if column == 0 else 0 for column in range(3))
            for row in range(3)
        )
        blocks.append((1, block))

    values = range(modulus) if modulus is not None else (-1, 0, 1)
    for normal in projective_lines:
        kernel_vectors = [
            vector
            for vector in product(values, repeat=3)
            if any(vector) and dot(normal, vector, modulus) == 0
        ]
        first = kernel_vectors[0]
        if modulus is None:
            second = next(vector for vector in kernel_vectors if any(cross(first, vector)))
        else:
            second = next(
                vector
                for vector in kernel_vectors
                if any(entry % modulus for entry in cross(first, vector))
            )
        block = tuple(
            tuple((first[row], second[row], 0)[column] for column in range(3))
            for row in range(3)
        )
        blocks.append((2, block))

    return tuple(blocks)


def equation_matrix(second_star_columns, aggregate, modulus):
    """Build the 54 scalar equations, omitting identically zero rows."""
    equations = []
    for pair_index, (c, d) in enumerate(PAIR_ORDER):
        for left_row in range(3):
            for right_column in range(3):
                equation = [0] * VARIABLE_COUNT
                equation[3 * c + right_column] = (
                    second_star_columns[d][left_row] % modulus
                )
                if left_row == c:
                    equation[9 + 3 * d + right_column] = 1
                equation[18 + pair_index] = -aggregate[left_row][right_column] % modulus
                if any(equation):
                    equations.append(equation)
    return equations


def active_endpoint_rows(equations, modulus):
    """Return endpoint rows which are nonzero on some kernel vector.

    A homogeneous linear solution space over an infinite field contains a
    vector on which any prescribed finite collection of nonzero coordinate
    projections are simultaneously nonzero.  Thus bounding the union of
    active row projections is stronger than checking solutions one by one.
    """
    rows = [list(row) for row in equations]
    pivot_columns = []
    pivot_row = 0

    for column in range(VARIABLE_COUNT):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column] % modulus, -1, modulus)
        rows[pivot_row] = [entry * inverse % modulus for entry in rows[pivot_row]]
        normalized = rows[pivot_row]
        for row_index, row in enumerate(rows):
            if row_index == pivot_row:
                continue
            coefficient = row[column] % modulus
            if coefficient:
                rows[row_index] = [
                    (entry - coefficient * base) % modulus
                    for entry, base in zip(row, normalized, strict=True)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    pivot_to_row = {column: row for row, column in enumerate(pivot_columns)}
    free_columns = tuple(
        column
        for column in range(VARIABLE_COUNT)
        if column not in pivot_to_row
    )
    active_coordinates = []
    for coordinate in range(18):
        if coordinate in free_columns:
            active_coordinates.append(True)
            continue
        row = rows[pivot_to_row[coordinate]]
        active_coordinates.append(any(row[column] for column in free_columns))

    active_rows = tuple(
        any(active_coordinates[3 * row : 3 * row + 3]) for row in range(6)
    )
    return active_rows, len(pivot_columns)


def audit_complete_finite_field(modulus):
    representatives = finite_projective_representatives(modulus)
    lines = representatives[1:]
    blocks = canonical_blocks(lines, modulus=modulus)
    histogram_by_rank = defaultdict(Counter)
    checked = 0
    double_invertible_rank_two = 0

    for second_star in product(representatives, repeat=3):
        second_star_invertible = determinant_of_columns(second_star, modulus) != 0
        for aggregate_rank, aggregate in blocks:
            equations = equation_matrix(second_star, aggregate, modulus)
            active, _ = active_endpoint_rows(equations, modulus)
            active_count = sum(active)
            assert active_count <= 4, (
                modulus,
                second_star,
                aggregate,
                active,
            )
            histogram_by_rank[aggregate_rank][active_count] += 1
            if second_star_invertible and aggregate_rank == 2:
                assert not any(active), (modulus, second_star, aggregate, active)
                double_invertible_rank_two += 1
            checked += 1

    return {
        "checked": checked,
        "histogram_by_rank": {
            rank: dict(sorted(histogram.items()))
            for rank, histogram in sorted(histogram_by_rank.items())
        },
        "double_invertible_rank_two": double_invertible_rank_two,
    }


def audit_bounded_rational_data():
    """Exact rank audit for normalized {-1,0,1} rational data.

    Reduction modulo the 61-bit prime is rank-faithful here.  Every row of
    the integer coefficient matrix has Euclidean norm at most sqrt(3), so
    Hadamard bounds every square minor (including coordinate-row augmented
    minors) by 3^12 = 531441, far below the prime.  Consequently all ranks
    used to decide whether a coordinate vanishes on the rational kernel are
    exactly their modular ranks.
    """
    representatives = bounded_rational_projective_representatives()
    lines = representatives[1:]
    blocks = canonical_blocks(lines)
    histogram_by_rank = defaultdict(Counter)
    checked = 0
    double_invertible_rank_two = 0

    for second_star in product(representatives, repeat=3):
        second_star_invertible = determinant_of_columns(second_star) != 0
        for aggregate_rank, aggregate in blocks:
            equations = equation_matrix(
                second_star, aggregate, RATIONAL_CERTIFICATE_PRIME
            )
            active, _ = active_endpoint_rows(
                equations, RATIONAL_CERTIFICATE_PRIME
            )
            active_count = sum(active)
            assert active_count <= 4, (second_star, aggregate, active)
            histogram_by_rank[aggregate_rank][active_count] += 1
            if second_star_invertible and aggregate_rank == 2:
                assert not any(active), (second_star, aggregate, active)
                double_invertible_rank_two += 1
            checked += 1

    assert 3**12 < RATIONAL_CERTIFICATE_PRIME
    return {
        "checked": checked,
        "histogram_by_rank": {
            rank: dict(sorted(histogram.items()))
            for rank, histogram in sorted(histogram_by_rank.items())
        },
        "double_invertible_rank_two": double_invertible_rank_two,
        "prime": RATIONAL_CERTIFICATE_PRIME,
    }


def audit_sharp_rational_witness():
    """Check a rank-two example with exactly four nonzero endpoint rows."""
    second_star = ((0, 0, 0), (0, 0, 0), (1, 1, 0))
    aggregate = ((-1, -1, 0), (-1, 0, 0), (0, 0, 0))
    p_rows = ((1, 0, 0), (-1, -1, 0), (1, 1, 1))
    s_rows = ((0, 0, 0), (0, 0, 0), (0, 1, 0))
    lambdas = (0, -1, 0, 1, 0, 0)

    for pair_index, (c, d) in enumerate(PAIR_ORDER):
        left_side = tuple(
            tuple(
                (1 if row == c else 0) * s_rows[d][column]
                + second_star[d][row] * p_rows[c][column]
                for column in range(3)
            )
            for row in range(3)
        )
        right_side = tuple(
            tuple(lambdas[pair_index] * aggregate[row][column] for column in range(3))
            for row in range(3)
        )
        assert left_side == right_side

    support = tuple(any(row) for row in p_rows + s_rows)
    assert support == (True, True, True, False, False, True)
    assert any(cross(aggregate[0], aggregate[1]))
    assert determinant_of_columns(second_star) == 0
    return support


def main():
    field_two = audit_complete_finite_field(2)
    field_three = audit_complete_finite_field(3)
    rational = audit_bounded_rational_data()
    sharp_support = audit_sharp_rational_witness()

    print(f"F2 exhaustive audit: {field_two}")
    print(f"F3 exhaustive audit: {field_three}")
    print(f"bounded rational exact-rank audit: {rational}")
    print(f"sharp rank-two singular-second-star support: {sharp_support}")
    print("PASS: independent one-invertible zero-cover audit")


if __name__ == "__main__":
    main()
