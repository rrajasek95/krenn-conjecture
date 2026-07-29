#!/usr/bin/env python3
"""Exact star-transport calculation for the six-site collision testbed."""

from __future__ import annotations

import itertools
from fractions import Fraction

from verify_color_collision_n_plus_two import perfect_matchings
from verify_four_vertex_collision_countermodel import (
    CORE,
    N,
    Q0,
    Q1,
    Q2,
    X,
    Y,
    Z,
    base_coefficient,
    direct_q2_cofactor,
    first_coefficient,
    second_coefficient,
)


VERTICES = tuple(range(N))
LABELS = (X, Y, Z)


def edge_value(table, u, v, a, b):
    """Read an endpoint-ordered cell from one of Q0,Q1,Q2."""
    if u < v:
        return Fraction(table.get((u, v, a, b), 0))
    return Fraction(table.get((v, u, b, a), 0))


def cofactor_coefficient(p, j, coloring, degree):
    r"""Coefficient of t^degree in H_{B\{p,j}}(q0+tQ1+t^2Q2)."""
    remaining = tuple(v for v in VERTICES if v not in (p, j))
    total = Fraction(0)
    for matching in perfect_matchings(remaining):
        polynomial = [Fraction(1), Fraction(0), Fraction(0)]
        for u, v in matching:
            cell = [
                edge_value(Q0, u, v, coloring[u], coloring[v]),
                edge_value(Q1, u, v, coloring[u], coloring[v]),
                edge_value(Q2, u, v, coloring[u], coloring[v]),
            ]
            product = [Fraction(0), Fraction(0), Fraction(0)]
            for first in range(3):
                for second in range(3 - first):
                    product[first + second] += polynomial[first] * cell[second]
            polynomial = product
        total += polynomial[degree]
    return total


def star_columns(p, z_degree):
    columns = []
    for j in VERTICES:
        if j == p:
            continue
        for a, b in itertools.product(LABELS, repeat=2):
            if int(a == Z) + int(b == Z) == z_degree:
                columns.append((j, a, b))
    return tuple(columns)


def star_map(p, column, jet_degree):
    """Sparse coordinate dictionary for F_jet_degree(column)."""
    j, a, b = column
    remaining = tuple(v for v in VERTICES if v not in (p, j))
    image = {}
    for labels in itertools.product(LABELS, repeat=len(remaining)):
        coloring = [None] * N
        coloring[p] = a
        coloring[j] = b
        for v, label in zip(remaining, labels):
            coloring[v] = label
        coloring = tuple(coloring)
        value = cofactor_coefficient(p, j, coloring, jet_degree)
        if value:
            image[coloring] = value
    return image


def add_scaled(target, source, scalar):
    for row, value in source.items():
        target[row] = target.get(row, Fraction(0)) + scalar * value
        if not target[row]:
            del target[row]


def exact_rank(rows):
    """Rank of a rational matrix supplied as a mutable list of dense rows."""
    if not rows:
        return 0
    matrix = [list(map(Fraction, row)) for row in rows]
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((r for r in range(row, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        scale = matrix[row][column]
        matrix[row] = [entry / scale for entry in matrix[row]]
        for r in range(len(matrix)):
            if r == row or not matrix[r][column]:
                continue
            scale = matrix[r][column]
            matrix[r] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(matrix[r], matrix[row])
            ]
        row += 1
        if row == len(matrix):
            break
    return row


def main():
    # Recheck the collision identities used by the transport example rather
    # than relying on the companion verifier's main routine.
    for coloring in itertools.product((X, Y), repeat=N):
        expected = 2 if coloring == (X,) * N else int(coloring == (Y,) * N)
        assert base_coefficient(coloring) == expected
    for z_site in VERTICES:
        for rest in itertools.product((X, Y), repeat=N - 1):
            coloring = list(rest)
            coloring.insert(z_site, Z)
            assert first_coefficient(tuple(coloring)) == 0
    for first, second in itertools.combinations(CORE, 2):
        remaining = tuple(v for v in VERTICES if v not in (first, second))
        for bits in itertools.product((X, Y), repeat=N - 2):
            coloring = [None] * N
            coloring[first] = coloring[second] = Z
            for vertex, bit in zip(remaining, bits):
                coloring[vertex] = bit
            expected = Fraction(1, 2) if bits == (X,) * (N - 2) else 0
            assert second_coefficient(tuple(coloring)) == expected
    tail_coloring = (Z, X, X, X, Z, X)
    assert direct_q2_cofactor(0, 4) == 0
    assert second_coefficient(tail_coloring) == 0

    circuit_data = {
        # p: (first star neighbor, second star neighbor, opposite core site,
        #     rank(F0 on D1), rank(coupled coefficient matrix))
        0: (1, 2, 3, 15, 20),
        1: (0, 3, 2, 19, 25),
        2: (3, 0, 1, 19, 25),
        3: (2, 1, 0, 15, 20),
    }
    rank_reports = []
    for p, (first_neighbor, second_neighbor, opposite, expected_first_rank,
            expected_coupled_rank) in circuit_data.items():
        degree_one_columns = star_columns(p, 1)
        degree_two_columns = star_columns(p, 2)
        assert len(degree_one_columns) == 20
        assert len(degree_two_columns) == 5

        f0_d1 = {column: star_map(p, column, 0) for column in degree_one_columns}
        f1_d1 = {column: star_map(p, column, 1) for column in degree_one_columns}
        f0_d2 = {column: star_map(p, column, 0) for column in degree_two_columns}

        # At each core site, the two incident switched-matching cells have
        # the same all-x derivative.  Their difference is therefore an exact
        # support-reducing star circuit.
        d0 = {
            (first_neighbor, X, X): Fraction(1),
            (second_neighbor, X, X): Fraction(-1),
        }
        f0_d0 = {}
        f1_d0 = {}
        f2_d0 = {}
        for column, scalar in d0.items():
            add_scaled(f0_d0, star_map(p, column, 0), scalar)
            add_scaled(f1_d0, star_map(p, column, 1), scalar)
            add_scaled(f2_d0, star_map(p, column, 2), scalar)
        assert not f0_d0

        # This single coordinate is a denominator-free certificate that the
        # first transport equation has no solution.  The forcing is -1,
        # whereas every possible one-z star correction has coefficient zero.
        obstruction = [X] * N
        obstruction[opposite] = Z
        obstruction = tuple(obstruction)
        assert f1_d0[obstruction] == -1
        assert all(not image.get(obstruction, 0) for image in f0_d1.values())

        first_rows = sorted(set(f1_d0).union(*(image for image in f0_d1.values())))
        first_matrix = [
            [f0_d1[column].get(row, 0) for column in degree_one_columns]
            for row in first_rows
        ]
        first_rhs = [-f1_d0.get(row, 0) for row in first_rows]
        first_rank = exact_rank(first_matrix)
        first_augmented_rank = exact_rank(
            [entries + [rhs] for entries, rhs in zip(first_matrix, first_rhs)]
        )

        # Form both lift equations at once, retaining every affine choice of
        # D1 and every degree-two star cell in D2.
        second_rows = sorted(
            set(f2_d0)
            .union(*(image for image in f1_d1.values()))
            .union(*(image for image in f0_d2.values()))
        )
        coupled_matrix = []
        coupled_rhs = []
        for entries, rhs in zip(first_matrix, first_rhs):
            coupled_matrix.append(entries + [Fraction(0)] * len(degree_two_columns))
            coupled_rhs.append(rhs)
        for row in second_rows:
            coupled_matrix.append(
                [f1_d1[column].get(row, 0) for column in degree_one_columns]
                + [f0_d2[column].get(row, 0) for column in degree_two_columns]
            )
            coupled_rhs.append(-f2_d0.get(row, 0))

        coupled_rank = exact_rank(coupled_matrix)
        coupled_augmented_rank = exact_rank(
            [entries + [rhs] for entries, rhs in zip(coupled_matrix, coupled_rhs)]
        )
        assert (first_rank, first_augmented_rank) == (
            expected_first_rank,
            expected_first_rank + 1,
        )
        assert (coupled_rank, coupled_augmented_rank) == (
            expected_coupled_rank,
            expected_coupled_rank + 1,
        )
        rank_reports.append(
            (p, first_rank, first_augmented_rank, coupled_rank, coupled_augmented_rank)
        )

    print("verified the base equation, full tangent equation, and six core pair equations")
    print("verified all four core D0 moves are exact support-reducing star circuits")
    print("verified each has an opposite-site coefficient -1 outside the full F0(D1) image")
    for p, first_rank, first_augmented_rank, coupled_rank, coupled_augmented_rank in rank_reports:
        print(
            f"p={p}: first lift ranks {first_rank}/{first_augmented_rank}; "
            f"coupled ranks {coupled_rank}/{coupled_augmented_rank}"
        )
    print("verified the omitted pair 04 has coefficient 0 instead of 1/2")


if __name__ == "__main__":
    main()
