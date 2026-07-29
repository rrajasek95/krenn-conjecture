#!/usr/bin/env python3
"""Discover exact response minors in the minimal three-extra chart.

This is a proof-discovery helper.  It keeps the shared-star zero rows at
the M={0} and M={1} extras, selects a sparse 19-row basis modulo a prime,
then reconstructs and factors that same maximal minor over Q(a,...,f).
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations, product
import random

import sympy as sp
from flint import fmpq, fmpq_mpoly_ctx, fmpz_mpoly_ctx


PRIME = 1_000_003
H_NUMERIC = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
I_NUMERIC = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
D_NUMERIC = ((1, 0, 0), (0, 1, 0), (0, 0, 0))
VERTICES = tuple(range(7))
COLUMNS = tuple(
    [(site, row) for site in range(5) for row in range(3)]
    + [(5, 1), (5, 2), (6, 0), (6, 2)]
)
COLUMN_INDEX = {column: index for index, column in enumerate(COLUMNS)}


def chart(kind, a, b):
    if kind == "01":
        return ((1, 0, a), (0, 1, b))
    if kind == "12":
        return ((a, 1, 0), (b, 0, 1))
    if kind == "02":
        return ((1, a, 0), (0, b, 1))
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
        for tail in matchings(vertices[1:position] + vertices[position + 1 :])
    )


def numeric_matrices(kinds, values):
    a, b, c, d, e, f = values
    return (
        I_NUMERIC,
        I_NUMERIC,
        D_NUMERIC,
        D_NUMERIC,
        embed((0, 1), chart(kinds[0], a, b)),
        embed((1, 2), chart(kinds[1], c, d)),
        embed((0, 2), chart(kinds[2], e, f)),
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
        (i, j): numeric_product(matrices[i], H_NUMERIC, matrices[j])
        for i, j in combinations(VERTICES, 2)
    }

    def edge(word, i, j):
        if i < j:
            return blocks[i, j][word[i]][word[j]]
        return blocks[j, i][word[j]][word[i]]

    def hafnian(word, vertices):
        answer = 0
        for matching in matchings(vertices):
            term = 1
            for i, j in matching:
                term = term * edge(word, i, j) % PRIME
            answer = (answer + term) % PRIME
        return answer

    def row(label):
        word, source_left, source_right = label
        answer = [0] * len(COLUMNS)
        for x, y in combinations(VERTICES, 2):
            marked = (
                matrices[x][word[x]][source_left]
                * matrices[y][word[y]][source_right]
                + matrices[x][word[x]][source_right]
                * matrices[y][word[y]][source_left]
            ) % PRIME
            if not marked:
                continue
            for star in VERTICES:
                column = (star, word[star])
                if star in (x, y) or column not in COLUMN_INDEX:
                    continue
                remaining = tuple(
                    site for site in VERTICES if site not in (x, y, star)
                )
                index = COLUMN_INDEX[column]
                answer[index] = (
                    answer[index] + marked * hafnian(word, remaining)
                ) % PRIME
        return answer

    return row


def select_labels(kinds, values, excluded_sources=(), tie_seed=None):
    row = numeric_row_engine(numeric_matrices(kinds, values))
    records = []
    for word in product(range(3), repeat=7):
        for source_left in range(3):
            for source_right in range(source_left, 3):
                if (source_left, source_right) in excluded_sources:
                    continue
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
            pivot = next(index for index, value in enumerate(reduced) if value)
            if pivot not in basis:
                inverse = pow(reduced[pivot], PRIME - 2, PRIME)
                basis[pivot] = [value * inverse % PRIME for value in reduced]
                selected.append((support, label))
                break
            scale = reduced[pivot]
            reduced = [
                (value - scale * basis_value) % PRIME
                for value, basis_value in zip(reduced, basis[pivot])
            ]
        if len(basis) == len(COLUMNS):
            break
    return selected


def symbolic_response_matrix(kinds, labels):
    parameters = sp.symbols("a b c d e f")
    a, b, c, d, e, f = parameters
    hessian = sp.Matrix(H_NUMERIC)
    identity = sp.eye(3)
    diagonal = sp.diag(1, 1, 0)

    def symbolic_embed(positions, rows):
        matrix = sp.zeros(3)
        for row, position in zip(rows, positions):
            matrix[position, :] = sp.Matrix(1, 3, row)
        return matrix

    matrices = (
        identity,
        identity,
        diagonal,
        diagonal,
        symbolic_embed((0, 1), chart(kinds[0], a, b)),
        symbolic_embed((1, 2), chart(kinds[1], c, d)),
        symbolic_embed((0, 2), chart(kinds[2], e, f)),
    )
    blocks = {
        (i, j): matrices[i] * hessian * matrices[j].T
        for i, j in combinations(VERTICES, 2)
    }

    def edge(word, i, j):
        if i < j:
            return blocks[i, j][word[i], word[j]]
        return blocks[j, i][word[j], word[i]]

    def hafnian(word, vertices):
        return sum(
            (
                sp.prod(edge(word, i, j) for i, j in matching)
                for matching in matchings(vertices)
            ),
            sp.S.Zero,
        )

    def row(label):
        word, source_left, source_right = label
        answer = [sp.S.Zero] * len(COLUMNS)
        for x, y in combinations(VERTICES, 2):
            marked = (
                matrices[x][word[x], source_left]
                * matrices[y][word[y], source_right]
                + matrices[x][word[x], source_right]
                * matrices[y][word[y], source_left]
            )
            if marked == 0:
                continue
            for star in VERTICES:
                column = (star, word[star])
                if star in (x, y) or column not in COLUMN_INDEX:
                    continue
                remaining = tuple(
                    site for site in VERTICES if site not in (x, y, star)
                )
                answer[COLUMN_INDEX[column]] += marked * hafnian(word, remaining)
        return answer

    return parameters, sp.Matrix([row(label) for label in labels])


def symbolic_determinant(kinds, labels):
    _, matrix = symbolic_response_matrix(kinds, labels)
    return sp.factor(matrix.det(method="domain-ge"))


def flint_determinant(kinds, labels):
    """Compute the same determinant by fraction-free FLINT elimination."""
    parameters, matrix = symbolic_response_matrix(kinds, labels)
    context = fmpz_mpoly_ctx.get(tuple(map(str, parameters)))

    def convert(expression):
        polynomial = sp.Poly(sp.expand(expression), *parameters, domain=sp.ZZ)
        return context.from_dict(
            {monomial: int(coefficient) for monomial, coefficient in polynomial.terms()}
        )

    entries = [
        [convert(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]
    sign = 1
    previous = context.constant(1)
    size = len(entries)
    for pivot_index in range(size - 1):
        if not entries[pivot_index][pivot_index]:
            swap_index = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if entries[row][pivot_index]
                ),
                None,
            )
            if swap_index is None:
                swap_column = next(
                    (
                        column
                        for column in range(pivot_index + 1, size)
                        if any(
                            entries[row][column]
                            for row in range(pivot_index, size)
                        )
                    ),
                    None,
                )
                if swap_column is None:
                    return context.constant(0)
                for row in range(size):
                    entries[row][pivot_index], entries[row][swap_column] = (
                        entries[row][swap_column], entries[row][pivot_index]
                    )
                sign = -sign
                swap_index = next(
                    row
                    for row in range(pivot_index, size)
                    if entries[row][pivot_index]
                )
            entries[pivot_index], entries[swap_index] = (
                entries[swap_index],
                entries[pivot_index],
            )
            if swap_index != pivot_index:
                sign = -sign
        pivot = entries[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    pivot * entries[row][column]
                    - entries[row][pivot_index] * entries[pivot_index][column]
                )
                entries[row][column] = (
                    numerator if pivot_index == 0 else numerator // previous
                )
            entries[row][pivot_index] = context.constant(0)
        previous = pivot
    return sign * entries[-1][-1]


def flint_restricted_determinant(kinds, labels, substitutions):
    """Compute a determinant after exact parameter specialization.

    The substitutions map any subset of the strings a,...,f to exact integer
    values. Eliminating specialized variables before fraction-free
    elimination is substantially faster on boundary strata.
    """
    parameters, matrix = symbolic_response_matrix(kinds, labels)
    parameter_by_name = {str(parameter): parameter for parameter in parameters}
    symbolic_substitutions = {
        parameter_by_name[name]: value for name, value in substitutions.items()
    }
    restricted = matrix.subs(symbolic_substitutions)
    free_parameters = tuple(
        parameter for parameter in parameters
        if str(parameter) not in substitutions
    )
    if not free_parameters:
        return sp.Integer(restricted.det(method="domain-ge"))

    rational_specialization = any(
        sp.denom(sp.Rational(value)) != 1 for value in substitutions.values()
    )
    context = (
        fmpq_mpoly_ctx.get(tuple(map(str, free_parameters)))
        if rational_specialization
        else fmpz_mpoly_ctx.get(tuple(map(str, free_parameters)))
    )

    def convert(expression):
        domain = sp.QQ if rational_specialization else sp.ZZ
        polynomial = sp.Poly(sp.expand(expression), *free_parameters, domain=domain)
        return context.from_dict(
            {
                monomial: (
                    fmpq(int(coefficient.p), int(coefficient.q))
                    if rational_specialization
                    else int(coefficient)
                )
                for monomial, coefficient in polynomial.terms()
            }
        )

    entries = [
        [convert(restricted[row, column]) for column in range(restricted.cols)]
        for row in range(restricted.rows)
    ]
    sign = 1
    previous = context.constant(1)
    size = len(entries)
    for pivot_index in range(size - 1):
        if not entries[pivot_index][pivot_index]:
            swap_index = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if entries[row][pivot_index]
                ),
                None,
            )
            if swap_index is None:
                swap_column = next(
                    (
                        column
                        for column in range(pivot_index + 1, size)
                        if any(
                            entries[row][column]
                            for row in range(pivot_index, size)
                        )
                    ),
                    None,
                )
                if swap_column is None:
                    return context.constant(0)
                for row in range(size):
                    entries[row][pivot_index], entries[row][swap_column] = (
                        entries[row][swap_column], entries[row][pivot_index]
                    )
                sign = -sign
                swap_index = next(
                    row
                    for row in range(pivot_index, size)
                    if entries[row][pivot_index]
                )
            entries[pivot_index], entries[swap_index] = (
                entries[swap_index],
                entries[pivot_index],
            )
            if swap_index != pivot_index:
                sign = -sign
        pivot = entries[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    pivot * entries[row][column]
                    - entries[row][pivot_index] * entries[pivot_index][column]
                )
                entries[row][column] = (
                    numerator if pivot_index == 0 else numerator // previous
                )
            entries[row][pivot_index] = context.constant(0)
        previous = pivot
    return sign * entries[-1][-1]


def flint_rational_restriction(
    kinds, labels, substitutions, free_parameter_names
):
    """Clear row denominators after a rational parameter substitution.

    Returns the determinant of the row-cleared matrix and the product of the
    row denominators.  The original restricted determinant is their quotient.
    """
    parameters, matrix = symbolic_response_matrix(kinds, labels)
    parameter_by_name = {str(parameter): parameter for parameter in parameters}
    symbolic_substitutions = {
        parameter_by_name[name]: value for name, value in substitutions.items()
    }
    restricted = matrix.subs(symbolic_substitutions).applyfunc(sp.cancel)
    free_parameters = tuple(
        parameter_by_name[name] for name in free_parameter_names
    )

    row_denominators = []
    cleared_rows = []
    for row_index in range(restricted.rows):
        row = list(restricted.row(row_index))
        row_denominator = sp.S.One
        for entry in row:
            row_denominator = sp.lcm(
                row_denominator, sp.cancel(entry).as_numer_denom()[1]
            )
        row_denominators.append(row_denominator)
        cleared_rows.append(
            [sp.cancel(row_denominator * entry) for entry in row]
        )
    cleared = sp.Matrix(cleared_rows)

    context = fmpq_mpoly_ctx.get(tuple(map(str, free_parameters)))

    def convert(expression):
        polynomial = sp.Poly(
            sp.expand(expression), *free_parameters, domain=sp.QQ
        )
        return context.from_dict(
            {
                monomial: fmpq(int(coefficient.p), int(coefficient.q))
                for monomial, coefficient in polynomial.terms()
            }
        )

    entries = [
        [convert(cleared[row, column]) for column in range(cleared.cols)]
        for row in range(cleared.rows)
    ]
    sign = 1
    previous = context.constant(1)
    size = len(entries)
    for pivot_index in range(size - 1):
        if not entries[pivot_index][pivot_index]:
            swap_index = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if entries[row][pivot_index]
                ),
                None,
            )
            if swap_index is None:
                swap_column = next(
                    (
                        column
                        for column in range(pivot_index + 1, size)
                        if any(
                            entries[row][column]
                            for row in range(pivot_index, size)
                        )
                    ),
                    None,
                )
                if swap_column is None:
                    return context.constant(0), sp.factor(
                        sp.prod(row_denominators)
                    )
                for row in range(size):
                    entries[row][pivot_index], entries[row][swap_column] = (
                        entries[row][swap_column], entries[row][pivot_index]
                    )
                sign = -sign
                swap_index = next(
                    row
                    for row in range(pivot_index, size)
                    if entries[row][pivot_index]
                )
            entries[pivot_index], entries[swap_index] = (
                entries[swap_index],
                entries[pivot_index],
            )
            if swap_index != pivot_index:
                sign = -sign
        pivot = entries[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    pivot * entries[row][column]
                    - entries[row][pivot_index] * entries[pivot_index][column]
                )
                entries[row][column] = (
                    numerator if pivot_index == 0 else numerator // previous
                )
            entries[row][pivot_index] = context.constant(0)
        previous = pivot
    determinant = sign * entries[-1][-1]
    multiplier = sp.factor(sp.prod(row_denominators))
    return determinant, multiplier


def symbolic_q_restriction(kinds, labels):
    """Return a denominator-cleared determinant on Q=0.

    In the central chart

        Q = ac + ae + ce + 3a + 3c + 3e + 6

    is linear in e.  On the open set a+c+3 != 0, solve Q=0 for e,
    clear the least common denominator in each response row, and compute
    the resulting polynomial determinant.  The returned multiplier is
    the product of those row denominators, so the identity being audited
    is exact in the localization Q[a,b,c,d,f,1/(a+c+3)].
    """
    parameters, matrix = symbolic_response_matrix(kinds, labels)
    a, _, c, _, e, _ = parameters
    denominator = a + c + 3
    numerator = -(a * c + 3 * a + 3 * c + 6)
    restricted = matrix.subs(e, numerator / denominator).applyfunc(sp.cancel)

    row_denominators = []
    cleared_rows = []
    for row_index in range(restricted.rows):
        row = list(restricted.row(row_index))
        row_denominator = sp.S.One
        for entry in row:
            row_denominator = sp.lcm(
                row_denominator, sp.cancel(entry).as_numer_denom()[1]
            )
        row_denominators.append(row_denominator)
        cleared_rows.append([sp.cancel(row_denominator * entry) for entry in row])

    cleared = sp.Matrix(cleared_rows)
    multiplier = sp.factor(sp.prod(row_denominators))
    determinant = sp.factor(cleared.det(method="domain-ge"))
    return determinant, multiplier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--charts", nargs=3, default=("01", "01", "01"))
    parser.add_argument("--values", nargs=6, type=int, default=(2, 3, 5, 7, 11, 13))
    parser.add_argument("--no-det", action="store_true")
    parser.add_argument("--restrict-q", action="store_true")
    parser.add_argument("--flint", action="store_true")
    args = parser.parse_args()
    selected = select_labels(tuple(args.charts), tuple(args.values))
    print("rank", len(selected))
    for support, label in selected:
        print(support, label)
    if len(selected) == len(COLUMNS) and not args.no_det:
        print("determinant")
        labels = [label for _, label in selected]
        if args.restrict_q:
            determinant, multiplier = symbolic_q_restriction(
                tuple(args.charts), labels
            )
            print("row-denominator multiplier")
            print(multiplier)
            print("cleared Q-restricted determinant")
            print(determinant)
        elif args.flint:
            print(flint_determinant(tuple(args.charts), labels).factor())
        else:
            print(symbolic_determinant(tuple(args.charts), labels))


if __name__ == "__main__":
    main()
