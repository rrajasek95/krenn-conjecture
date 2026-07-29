#!/usr/bin/env python3
"""Exact audits for notes/rank-two-singular-fixed-line-obstruction.md."""

from __future__ import annotations

import itertools

import sympy as sp


def audit_symbolic_compressions() -> None:
    x, y, z, w = sp.symbols("x y z w")
    alpha, beta, gamma, delta = sp.symbols(
        "alpha beta gamma delta", nonzero=True
    )

    matching = sp.Matrix(
        [[0, alpha * x, y],
         [z, 0, beta * x],
         [gamma * x, w, 0]]
    )
    coordinate_quotients = [
        sp.Matrix([[int(row == index) for index in range(3)]
                   for row in range(3) if row != omitted])
        for omitted in range(3)
    ]
    expected_matching = [
        sp.Matrix([[0, beta * x], [w, 0]]),
        sp.Matrix([[0, y], [gamma * x, 0]]),
        sp.Matrix([[0, alpha * x], [z, 0]]),
    ]
    for quotient, expected in zip(coordinate_quotients, expected_matching):
        assert (quotient * matching * quotient.T).equals(expected)

    two_plus_two = sp.Matrix(
        [[0, alpha * x, beta * x],
         [gamma * y, 0, z],
         [delta * y, w, 0]]
    )
    quotient_v = sp.Matrix([[1, 0, 0], [0, delta, -gamma]])
    quotient_u = sp.Matrix([[1, 0, 0], [0, beta, -alpha]])
    expected_two_plus_two = sp.Matrix(
        [[0, 0], [0, -alpha * delta * z - beta * gamma * w]]
    )
    assert (quotient_v * two_plus_two * quotient_u.T).equals(
        expected_two_plus_two
    )

    three_plus_one = sp.Matrix(
        [[0, alpha * x + beta * y, x],
         [0, 0, z],
         [w, y, 0]]
    )
    quotient_e2 = coordinate_quotients[2]
    assert (quotient_e2 * three_plus_one * quotient_e2.T).equals(
        sp.Matrix([[0, alpha * x + beta * y], [0, 0]])
    )


def audit_crossed_kernel_cancellation() -> None:
    z00, z01, z10, z11 = sp.symbols("z00 z01 z10 z11")
    # Coordinates relative to the bases (a1,a,a2) and (b1,b,b2) in (29).
    U = sp.Matrix([[0, 1], [1, 0], [0, 0]])
    X = sp.Matrix([[0, 0], [1, 0], [0, 1]])
    Y = sp.Matrix([[0, 1], [1, 0], [0, 0]])
    V = sp.Matrix([[0, 0], [-1, 0], [0, 1]])
    Z = sp.Matrix([[z00, z01], [z10, z11]])
    physical = sp.expand(U * Z * Y.T + X * Z.T * V.T)
    expected = sp.Matrix(
        [[z11, z10, 0], [z01, 0, z10], [0, -z01, z11]]
    )
    assert physical == expected
    assert sp.expand(physical.det()) == 0


def projective_points(prime: int) -> tuple[tuple[int, int, int], ...]:
    points = []
    for vector in itertools.product(range(prime), repeat=3):
        if vector == (0, 0, 0):
            continue
        pivot = next(value for value in vector if value)
        inverse = pow(pivot, -1, prime)
        normalized = tuple(value * inverse % prime for value in vector)
        if normalized not in points:
            points.append(normalized)
    return tuple(points)


def projectivize(vector: tuple[int, int, int], prime: int) -> tuple[int, int, int]:
    pivot = next(value for value in vector if value % prime)
    inverse = pow(pivot, -1, prime)
    return tuple(value * inverse % prime for value in vector)


def cross_matrix(vector: tuple[int, int, int], prime: int) -> tuple[tuple[int, ...], ...]:
    first, second, third = vector
    return (
        (0, -third % prime, second % prime),
        (third % prime, 0, -first % prime),
        (-second % prime, first % prime, 0),
    )


def multiply(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column]
                for middle in range(len(right))) % prime
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def transpose(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(zip(*matrix))


def matrix_rank(matrix: list[list[int]], prime: int) -> int:
    reduced = [[entry % prime for entry in row] for row in matrix]
    row_count = len(reduced)
    column_count = len(reduced[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if reduced[row][column]),
            None,
        )
        if pivot is None:
            continue
        reduced[rank], reduced[pivot] = reduced[pivot], reduced[rank]
        inverse = pow(reduced[rank][column], -1, prime)
        reduced[rank] = [entry * inverse % prime for entry in reduced[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            coefficient = reduced[row][column]
            reduced[row] = [
                (entry - coefficient * pivot_entry) % prime
                for entry, pivot_entry in zip(reduced[row], reduced[rank])
            ]
        rank += 1
    return rank


def compression_span_rank(
    basis: tuple[tuple[tuple[int, ...], ...], ...],
    u: tuple[int, int, int],
    v: tuple[int, int, int],
    prime: int,
) -> int:
    left = cross_matrix(v, prime)
    right_transpose = transpose(cross_matrix(u, prime))
    columns = []
    for matrix in basis:
        compressed = multiply(multiply(left, matrix, prime), right_transpose, prime)
        columns.append(tuple(entry for row in compressed for entry in row))
    coefficient_matrix = [list(row) for row in zip(*columns)]
    return matrix_rank(coefficient_matrix, prime)


def matrix_from_entries(
    entries: tuple[tuple[int, int, int], ...], prime: int
) -> tuple[tuple[int, ...], ...]:
    matrix = [[0] * 3 for _ in range(3)]
    for row, column, value in entries:
        matrix[row][column] = value % prime
    return tuple(tuple(row) for row in matrix)


def matching_basis(
    coefficients: tuple[int, int, int], prime: int
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    alpha, beta, gamma = coefficients
    return (
        matrix_from_entries(((0, 1, alpha), (1, 2, beta), (2, 0, gamma)), prime),
        matrix_from_entries(((0, 2, 1),), prime),
        matrix_from_entries(((1, 0, 1),), prime),
        matrix_from_entries(((2, 1, 1),), prime),
    )


def two_plus_two_basis(
    coefficients: tuple[int, int, int, int], prime: int
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    alpha, beta, gamma, delta = coefficients
    return (
        matrix_from_entries(((0, 1, alpha), (0, 2, beta)), prime),
        matrix_from_entries(((1, 0, gamma), (2, 0, delta)), prime),
        matrix_from_entries(((1, 2, 1),), prime),
        matrix_from_entries(((2, 1, 1),), prime),
    )


def three_plus_one_basis(
    coefficients: tuple[int, int], prime: int
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    alpha, beta = coefficients
    return (
        matrix_from_entries(((0, 1, alpha), (0, 2, 1)), prime),
        matrix_from_entries(((0, 1, beta), (2, 1, 1)), prime),
        matrix_from_entries(((1, 2, 1),), prime),
        matrix_from_entries(((2, 0, 1),), prime),
    )


def one_line_pairs(
    basis: tuple[tuple[tuple[int, ...], ...], ...],
    points: tuple[tuple[int, int, int], ...],
    prime: int,
) -> set[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    return {
        (u, v)
        for u in points
        for v in points
        if compression_span_rank(basis, u, v, prime) == 1
    }


def audit_exact_finite_field_classification() -> None:
    # This is an exact audit of every coefficient degeneration over F_5.
    # Lemma 4.1 supplies the characteristic-zero proof.
    prime = 5
    points = projective_points(prime)
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)

    relation_directions = tuple(
        point for point in points if sum(value != 0 for value in point) >= 2
    )
    for alpha, beta, gamma in relation_directions:
        expected = set()
        if beta == 0:
            expected.add((e0, e0))
        if gamma == 0:
            expected.add((e1, e1))
        if alpha == 0:
            expected.add((e2, e2))
        actual = one_line_pairs(
            matching_basis((alpha, beta, gamma), prime), points, prime
        )
        assert actual == expected

    for beta in range(1, prime):
        for delta in range(1, prime):
            coefficients = (1, beta, 1, delta)
            expected_u = projectivize((0, 1, beta), prime)
            expected_v = projectivize((0, 1, delta), prime)
            actual = one_line_pairs(two_plus_two_basis(coefficients, prime), points, prime)
            assert actual == {(expected_u, expected_v)}

    for alpha in range(1, prime):
        for beta in range(1, prime):
            actual = one_line_pairs(
                three_plus_one_basis((alpha, beta), prime), points, prime
            )
            assert actual == {(e2, e2)}


def main() -> None:
    audit_symbolic_compressions()
    audit_crossed_kernel_cancellation()
    audit_exact_finite_field_classification()
    print("rank-two singular fixed-line obstruction: PASS")


if __name__ == "__main__":
    main()
