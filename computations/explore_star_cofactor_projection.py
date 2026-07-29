#!/usr/bin/env python3
"""Finite-field probe of the shared-cofactor projection on the star face.

This is an exploratory exhaustive calculation in three right-hand spaces of
dimension two over F_2.  For pair tensors R_34,R_35,R_45, let K be the space
of triples p=(p_3,p_4,p_5) satisfying

    p_3 R_45 + p_4 R_35 + p_5 R_34 = 0.

For two two-dimensional families P,Q in K, the six cross matchings define a
bilinear 2 by 2 coefficient matrix.  We measure the span of those matrices
as the remaining row and output indices vary.
"""

from __future__ import annotations

from itertools import product


def rank2(rows: list[int], width: int) -> int:
    rows = [row for row in rows if row]
    rank = 0
    for column in reversed(range(width)):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] >> column & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] >> column & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def kernel2(rows: list[int], width: int) -> list[int]:
    rows = rows[:]
    pivot_columns: list[int] = []
    rank = 0
    for column in range(width):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] >> column & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] >> column & 1:
                rows[i] ^= rows[rank]
        pivot_columns.append(column)
        rank += 1
    free = [column for column in range(width) if column not in pivot_columns]
    answer = []
    for free_column in free:
        vector = 1 << free_column
        for i, pivot_column in enumerate(pivot_columns):
            if rows[i] >> free_column & 1:
                vector |= 1 << pivot_column
        answer.append(vector)
    return answer


def bit(matrix: int, row: int, column: int) -> int:
    return matrix >> (2 * row + column) & 1


def build_map(r34: int, r35: int, r45: int) -> list[int]:
    # Eight output coordinates, six input coordinates ordered (site-3,
    # site-4, site-5), with two coordinates at each site.
    rows = []
    for i, j, k in product(range(2), repeat=3):
        row = 0
        if bit(r45, j, k):
            row |= 1 << i
        if bit(r35, i, k):
            row |= 1 << (2 + j)
        if bit(r34, i, j):
            row |= 1 << (4 + k)
        rows.append(row)
    return rows


def coordinate(vector: int, site: int, value: int) -> int:
    return vector >> (2 * (site - 3) + value) & 1


def cross_value(r: int, p: int, q: int, output: tuple[int, int, int]) -> int:
    values = dict(zip((3, 4, 5), output))
    answer = 0
    for r_site, p_site, q_site in (
        (3, 4, 5),
        (3, 5, 4),
        (4, 3, 5),
        (4, 5, 3),
        (5, 3, 4),
        (5, 4, 3),
    ):
        answer ^= (
            coordinate(r, r_site, values[r_site])
            & coordinate(p, p_site, values[p_site])
            & coordinate(q, q_site, values[q_site])
        )
    return answer


def cross_span(p_family: tuple[int, int], q_family: tuple[int, int]) -> int:
    coefficient_rows = []
    for r_coordinate in range(6):
        r = 1 << r_coordinate
        for output in product(range(2), repeat=3):
            row = 0
            for alpha, p in enumerate(p_family):
                for beta, q in enumerate(q_family):
                    row |= cross_value(r, p, q, output) << (2 * alpha + beta)
            coefficient_rows.append(row)
    return rank2(coefficient_rows, 4)


def main() -> None:
    counts: dict[tuple[int, int], int] = {}
    maximum = 0
    witness = None
    for r34, r35, r45 in product(range(16), repeat=3):
        kernel = kernel2(build_map(r34, r35, r45), 6)
        dimension = len(kernel)
        if dimension < 2:
            continue
        # It is enough for the first probe to use pairs from a kernel basis.
        for p_indices in product(range(dimension), repeat=2):
            for q_indices in product(range(dimension), repeat=2):
                p_family = tuple(kernel[index] for index in p_indices)
                q_family = tuple(kernel[index] for index in q_indices)
                span = cross_span(p_family, q_family)
                counts[dimension, span] = counts.get((dimension, span), 0) + 1
                if span > maximum:
                    maximum = span
                    witness = (r34, r35, r45, kernel, p_indices, q_indices)
    print("counts by (kernel dimension, cross span):", sorted(counts.items()))
    print("maximum cross span:", maximum)
    print("first witness:", witness)


if __name__ == "__main__":
    main()
