#!/usr/bin/env python3
"""Exact response discovery for the first two-extra rescue frontier.

The configuration is

    (M_e2, M_e0) = ({2}, {0}),   (r,t) = (2,0).

All seven nonzero residual sites are retained in every cofactor.  The
shared-star theorem removes only output row 0 from the e0 star, leaving
20 response columns.  Row selection is direct-free (source 01 is omitted).
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations, product
import random

import sympy as sp
from flint import fmpz_mpoly_ctx


PRIME = 1_000_003
HESSIAN = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
TYPE_10 = ((1, 0, 0), (0, 1, 0), (0, 0, 0))
VERTICES = tuple(range(7))

# Sites are (u0,u1,u2,c,d,e2,e0).  The e0->z0 block has image in
# <e1,e2>, but e0 itself is not deleted from marked pairs or cofactors.
COLUMNS = tuple(
    [(site, row) for site in range(6) for row in range(3)]
    + [(6, 1), (6, 2)]
)
COLUMN_INDEX = {column: index for index, column in enumerate(COLUMNS)}
SOURCE_PAIRS = ((0, 0), (0, 2), (1, 1), (1, 2), (2, 2))


def chart(kind, first, second):
    if kind == "01":
        return ((1, 0, first), (0, 1, second))
    if kind == "12":
        return ((first, 1, 0), (second, 0, 1))
    if kind == "02":
        return ((1, first, 0), (0, second, 1))
    raise ValueError(kind)


def embed(positions, rows):
    matrix = [[0] * 3 for _ in range(3)]
    for row, position in zip(rows, positions):
        matrix[position] = list(row)
    return tuple(tuple(row) for row in matrix)


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in matchings(
            vertices[1:position] + vertices[position + 1 :]
        )
    )


def numeric_matrices(kinds, values):
    a, b, c, d = values
    return (
        IDENTITY,
        IDENTITY,
        IDENTITY,
        TYPE_10,
        TYPE_10,
        embed((0, 1), chart(kinds[0], a, b)),
        embed((1, 2), chart(kinds[1], c, d)),
    )


def numeric_product(left, middle, right):
    return tuple(
        tuple(
            sum(
                left[i][a] * middle[a][b] * right[j][b]
                for a in range(3)
                for b in range(3)
            )
            % PRIME
            for j in range(3)
        )
        for i in range(3)
    )


def numeric_row_engine(matrices):
    blocks = {
        (i, j): numeric_product(matrices[i], HESSIAN, matrices[j])
        for i, j in combinations(VERTICES, 2)
    }

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left]][word[right]]
        return blocks[right, left][word[right]][word[left]]

    @lru_cache(maxsize=None)
    def hafnian(word, vertices):
        answer = 0
        for matching in matchings(vertices):
            term = 1
            for left, right in matching:
                term = term * edge(word, left, right) % PRIME
            answer = (answer + term) % PRIME
        return answer

    def row(label):
        word, source_left, source_right = label
        answer = [0] * len(COLUMNS)
        for marked_left, marked_right in combinations(VERTICES, 2):
            marked = (
                matrices[marked_left][word[marked_left]][source_left]
                * matrices[marked_right][word[marked_right]][source_right]
                + matrices[marked_left][word[marked_left]][source_right]
                * matrices[marked_right][word[marked_right]][source_left]
            ) % PRIME
            if not marked:
                continue
            for star in VERTICES:
                column = (star, word[star])
                if (
                    star in (marked_left, marked_right)
                    or column not in COLUMN_INDEX
                ):
                    continue
                remaining = tuple(
                    site for site in VERTICES
                    if site not in (marked_left, marked_right, star)
                )
                answer[COLUMN_INDEX[column]] = (
                    answer[COLUMN_INDEX[column]]
                    + marked * hafnian(word, remaining)
                ) % PRIME
        return answer

    return row


def select_labels(kinds, values, tie_seed=None):
    row = numeric_row_engine(numeric_matrices(kinds, values))
    records = []
    for word in product(range(3), repeat=7):
        for source_left, source_right in SOURCE_PAIRS:
            label = (word, source_left, source_right)
            values_row = row(label)
            support = sum(bool(value) for value in values_row)
            if support:
                records.append((support, label, values_row))
    if tie_seed is not None:
        random.Random(tie_seed).shuffle(records)
    records.sort(key=lambda item: item[0])

    basis = {}
    selected = []
    for support, label, original in records:
        reduced = original[:]
        while any(reduced):
            pivot = next(
                index for index, value in enumerate(reduced) if value
            )
            if pivot not in basis:
                inverse = pow(reduced[pivot], PRIME - 2, PRIME)
                basis[pivot] = [
                    value * inverse % PRIME for value in reduced
                ]
                selected.append((support, label))
                break
            scale = reduced[pivot]
            reduced = [
                (value - scale*basis_value) % PRIME
                for value, basis_value in zip(reduced, basis[pivot])
            ]
        if len(basis) == len(COLUMNS):
            break
    return tuple(selected)


def symbolic_response_matrix(kinds, labels):
    parameters = sp.symbols("a b c d")
    a, b, c, d = parameters
    hessian = sp.Matrix(HESSIAN)
    identity = sp.eye(3)
    type_10 = sp.diag(1, 1, 0)

    def symbolic_embed(positions, rows):
        matrix = sp.zeros(3)
        for row, position in zip(rows, positions):
            matrix[position, :] = sp.Matrix(1, 3, row)
        return matrix

    matrices = (
        identity,
        identity,
        identity,
        type_10,
        type_10,
        symbolic_embed((0, 1), chart(kinds[0], a, b)),
        symbolic_embed((1, 2), chart(kinds[1], c, d)),
    )
    blocks = {
        (i, j): matrices[i]*hessian*matrices[j].T
        for i, j in combinations(VERTICES, 2)
    }

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left], word[right]]
        return blocks[right, left][word[right], word[left]]

    def hafnian(word, vertices):
        return sum(
            (
                sp.prod(
                    edge(word, left, right)
                    for left, right in matching
                )
                for matching in matchings(vertices)
            ),
            sp.S.Zero,
        )

    def row(label):
        word, source_left, source_right = label
        answer = [sp.S.Zero] * len(COLUMNS)
        for marked_left, marked_right in combinations(VERTICES, 2):
            marked = (
                matrices[marked_left][word[marked_left], source_left]
                * matrices[marked_right][word[marked_right], source_right]
                + matrices[marked_left][word[marked_left], source_right]
                * matrices[marked_right][word[marked_right], source_left]
            )
            if marked == 0:
                continue
            for star in VERTICES:
                column = (star, word[star])
                if (
                    star in (marked_left, marked_right)
                    or column not in COLUMN_INDEX
                ):
                    continue
                remaining = tuple(
                    site for site in VERTICES
                    if site not in (marked_left, marked_right, star)
                )
                answer[COLUMN_INDEX[column]] += (
                    marked * hafnian(word, remaining)
                )
        return answer

    return parameters, sp.Matrix([row(label) for label in labels])


def flint_determinant(kinds, labels):
    """Reconstruct one selected maximal minor over ZZ[a,b,c,d]."""
    parameters, matrix = symbolic_response_matrix(kinds, labels)
    context = fmpz_mpoly_ctx.get(tuple(map(str, parameters)))

    def convert(expression):
        polynomial = sp.Poly(
            sp.expand(expression), *parameters, domain=sp.ZZ
        )
        return context.from_dict(
            {
                monomial: int(coefficient)
                for monomial, coefficient in polynomial.terms()
            }
        )

    entries = [
        [
            convert(matrix[row, column])
            for column in range(matrix.cols)
        ]
        for row in range(matrix.rows)
    ]
    sign = 1
    previous = context.constant(1)
    for pivot_index in range(len(entries)-1):
        if not entries[pivot_index][pivot_index]:
            swap_index = next(
                (
                    row for row in range(pivot_index+1, len(entries))
                    if entries[row][pivot_index]
                ),
                None,
            )
            if swap_index is None:
                swap_column = next(
                    (
                        column
                        for column in range(pivot_index+1, len(entries))
                        if any(
                            entries[row][column]
                            for row in range(pivot_index, len(entries))
                        )
                    ),
                    None,
                )
                if swap_column is None:
                    return context.constant(0)
                for row in range(len(entries)):
                    entries[row][pivot_index], entries[row][swap_column] = (
                        entries[row][swap_column],
                        entries[row][pivot_index],
                    )
                sign = -sign
                swap_index = next(
                    row for row in range(pivot_index, len(entries))
                    if entries[row][pivot_index]
                )
            entries[pivot_index], entries[swap_index] = (
                entries[swap_index], entries[pivot_index]
            )
            if swap_index != pivot_index:
                sign = -sign
        pivot = entries[pivot_index][pivot_index]
        for row in range(pivot_index+1, len(entries)):
            for column in range(pivot_index+1, len(entries)):
                numerator = (
                    pivot*entries[row][column]
                    - entries[row][pivot_index]
                    * entries[pivot_index][column]
                )
                entries[row][column] = (
                    numerator
                    if pivot_index == 0
                    else numerator // previous
                )
            entries[row][pivot_index] = context.constant(0)
        previous = pivot
    return sign*entries[-1][-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--charts", nargs=2, default=("01", "01"))
    parser.add_argument(
        "--values", nargs=4, type=int, default=(2, 3, 5, 7)
    )
    parser.add_argument("--all-charts", action="store_true")
    parser.add_argument("--determinant", action="store_true")
    args = parser.parse_args()

    chart_products = (
        tuple(product(("01", "12", "02"), repeat=2))
        if args.all_charts
        else (tuple(args.charts),)
    )
    for kinds in chart_products:
        selected = select_labels(kinds, tuple(args.values))
        print("".join(kinds), "rank", len(selected), "/", len(COLUMNS))
        if not args.all_charts:
            for support, label in selected:
                print(support, label)
        if args.determinant:
            assert len(selected) == len(COLUMNS)
            print(flint_determinant(
                kinds, tuple(label for _support, label in selected)
            ).factor())


if __name__ == "__main__":
    main()
