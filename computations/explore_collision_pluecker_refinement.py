#!/usr/bin/env python3
"""Exact probes of coupled collision-pair equations on nondiagonal bases.

This discovery script generalizes the dense-diagonal second-jet elimination
to an arbitrary first-kernel dimension.  Its initial test point is the
active rank-two binary gadget, rescaled to realize 2 X + Y.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

import verify_active_ranktwo_binary_gadget as gadget
import verify_dense_diagonal_collision_obstruction as dense


N = 6
EDGES = dense.EDGES
MATCHINGS = dense.MATCHINGS


def nondiagonal_base():
    q0 = {}
    for (u, v), matrix in gadget.MATRICES.items():
        for a in (dense.X, dense.Y):
            for b in (dense.X, dense.Y):
                value = Fraction(matrix[a][b])
                # A local x-coordinate scaling at vertex zero changes the
                # gadget's X+Y output to 2X+Y without creating mixed output.
                if u == 0 and a == dense.X:
                    value *= 2
                if value:
                    q0[(u, v, a, b)] = value
    return q0


def canonical_particular(q0, variables):
    """Half of the infinitesimal local change x -> x+t z."""
    answer = []
    for u, v, a, b in variables:
        value = Fraction(0)
        if a == dense.Z:
            value += q0.get((u, v, dense.X, b), 0) / 2
        if b == dense.Z:
            value += q0.get((u, v, a, dense.X), 0) / 2
        answer.append(value)
    return answer


def second_rows(q0, variables, particular, basis, pure_x=False):
    parameter_count = len(basis)
    parameter_pairs = tuple(
        itertools.combinations_with_replacement(range(parameter_count), 2)
    )
    pair_index = {pair: index for index, pair in enumerate(parameter_pairs)}
    variable_index = {key: index for index, key in enumerate(variables)}
    forms = [
        (particular[index], tuple(vector[index] for vector in basis))
        for index in range(len(variables))
    ]

    rows = []
    colorings = tuple(
        coloring
        for coloring in itertools.product((dense.X, dense.Y, dense.Z), repeat=N)
        if coloring.count(dense.Z) == 2
        and (not pure_x or dense.Y not in coloring)
    )
    for coloring in colorings:
        q2_part = [Fraction(0)] * len(EDGES)
        linear = [Fraction(0)] * parameter_count
        quadratic = [Fraction(0)] * len(parameter_pairs)
        constant = Fraction(-int(dense.Y not in coloring))

        for matching in MATCHINGS:
            for position, edge in enumerate(matching):
                u, v = edge
                if (coloring[u], coloring[v]) != (dense.Z, dense.Z):
                    continue
                coefficient = Fraction(1)
                for other, (a, b) in enumerate(matching):
                    if other != position:
                        coefficient *= q0.get(
                            (a, b, coloring[a], coloring[b]), 0
                        )
                q2_part[EDGES.index(edge)] += coefficient

            for first, second in itertools.combinations(range(3), 2):
                remaining = 3 - first - second
                a, b = matching[remaining]
                coefficient = q0.get((a, b, coloring[a], coloring[b]), 0)
                if not coefficient:
                    continue
                chosen = []
                for position in (first, second):
                    u, v = matching[position]
                    index = variable_index.get(
                        (u, v, coloring[u], coloring[v])
                    )
                    if index is None:
                        chosen = []
                        break
                    chosen.append(forms[index])
                if not chosen:
                    continue
                (left_constant, left), (right_constant, right) = chosen
                constant += coefficient * left_constant * right_constant
                for i in range(parameter_count):
                    linear[i] += coefficient * (
                        left_constant * right[i] + right_constant * left[i]
                    )
                    for j in range(i, parameter_count):
                        value = left[i] * right[j]
                        if i != j:
                            value += left[j] * right[i]
                        quadratic[pair_index[(i, j)]] += coefficient * value

        rows.append(q2_part + linear + quadratic + [constant])
    return parameter_pairs, rows


def polynomial_string(row, parameter_pairs):
    offset = len(EDGES)
    terms = []
    parameter_count = max(max(pair) for pair in parameter_pairs) + 1
    for i, coefficient in enumerate(row[offset : offset + parameter_count]):
        if coefficient:
            terms.append(f"({coefficient})t{i}")
    offset += parameter_count
    for pair, coefficient in zip(parameter_pairs, row[offset:-1]):
        if coefficient:
            terms.append(f"({coefficient})t{pair[0]}t{pair[1]}")
    if row[-1]:
        terms.append(f"({row[-1]})")
    return " + ".join(terms) or "0"


def z_site(vector, variables):
    support = set()
    for coefficient, (u, v, a, b) in zip(vector, variables):
        if coefficient:
            support.add(u if a == dense.Z else v)
    assert len(support) == 1
    return support.pop()


def pair_quotient_bilinear_ranks(q0, variables, basis):
    """Ranks after retaining every binary complement coefficient.

    For a pair i,j, use independent bases of the site tangent kernels K_i,
    K_j.  Each complement coloring gives a row in the direct-W coordinate,
    the d_i*d_j bilinear coordinates, and the target constant.  Eliminating
    W leaves affine bilinear equations.  Their matrix ranks diagnose whether
    a vertex-scalar tetrad t_i*t_j=c_ij is even available.
    """
    grouped = {vertex: [] for vertex in range(N)}
    for vector in basis:
        grouped[z_site(vector, variables)].append(vector)
    variable_index = {key: index for index, key in enumerate(variables)}
    output = {}
    for i, j in EDGES:
        left, right = grouped[i], grouped[j]
        rows = []
        remaining = tuple(v for v in range(N) if v not in (i, j))
        for tail in itertools.product((dense.X, dense.Y), repeat=N - 2):
            coloring = [None] * N
            coloring[i] = coloring[j] = dense.Z
            for vertex, color in zip(remaining, tail):
                coloring[vertex] = color
            direct = Fraction(0)
            bilinear = [Fraction(0)] * (len(left) * len(right))
            for matching in MATCHINGS:
                for position, edge in enumerate(matching):
                    if edge != (i, j):
                        continue
                    coefficient = Fraction(1)
                    for other, (u, v) in enumerate(matching):
                        if other != position:
                            coefficient *= q0.get(
                                (u, v, coloring[u], coloring[v]), 0
                            )
                    direct += coefficient
                for first, second in itertools.combinations(range(3), 2):
                    remaining_position = 3 - first - second
                    u, v = matching[remaining_position]
                    coefficient = q0.get(
                        (u, v, coloring[u], coloring[v]), 0
                    )
                    if not coefficient:
                        continue
                    selected = []
                    for position in (first, second):
                        a, b = matching[position]
                        index = variable_index.get(
                            (a, b, coloring[a], coloring[b])
                        )
                        if index is None:
                            selected = []
                            break
                        selected.append(index)
                    if not selected:
                        continue
                    first_index, second_index = selected
                    for a, left_vector in enumerate(left):
                        for b, right_vector in enumerate(right):
                            value = (
                                left_vector[first_index] * right_vector[second_index]
                                + left_vector[second_index] * right_vector[first_index]
                            )
                            bilinear[a * len(right) + b] += coefficient * value
            target = Fraction(1, 2) if dense.Y not in coloring else Fraction(0)
            rows.append([direct] + bilinear + [-target])
        reduced, _ = dense.rref(rows)
        eliminated = [row for row in reduced if not row[0]]
        ranks = []
        for row in eliminated:
            matrix = [
                row[1 + a * len(right) : 1 + (a + 1) * len(right)]
                for a in range(len(left))
            ]
            ranks.append(len(dense.rref(matrix)[1]) if matrix and matrix[0] else 0)
        output[(i, j)] = (len(left), len(right), tuple(ranks), len(eliminated))
    return output


def main():
    q0 = nondiagonal_base()
    for coloring in itertools.product((dense.X, dense.Y), repeat=N):
        target = 2 if coloring == (dense.X,) * N else int(
            coloring == (dense.Y,) * N
        )
        assert dense.output_coefficient(q0, coloring) == target

    variables, matrix, target = dense.first_system(N, q0)
    basis, pivots = dense.nullspace(matrix)
    particular = canonical_particular(q0, variables)
    assert all(
        sum(value * coordinate for value, coordinate in zip(row, particular))
        == rhs
        for row, rhs in zip(matrix, target)
    )
    parameter_pairs, rows = second_rows(q0, variables, particular, basis)
    reduced, second_pivots = dense.rref(rows)
    eliminated = [row for row in reduced if not any(row[: len(EDGES)])]
    print(
        f"first_rank={len(pivots)} first_nullity={len(basis)} "
        f"second_rank={len(reduced)} q2_rank="
        f"{sum(pivot < len(EDGES) for pivot in second_pivots)} "
        f"eliminated={len(eliminated)}"
    )
    for row in eliminated:
        print(polynomial_string(row, parameter_pairs))

    pure_pairs, pure_rows = second_rows(
        q0, variables, particular, basis, pure_x=True
    )
    pure_reduced, pure_pivots = dense.rref(pure_rows)
    pure_eliminated = [
        row for row in pure_reduced if not any(row[: len(EDGES)])
    ]
    print(
        f"pure-X second_rank={len(pure_reduced)} q2_rank="
        f"{sum(pivot < len(EDGES) for pivot in pure_pivots)} "
        f"eliminated={len(pure_eliminated)}"
    )
    for row in pure_eliminated:
        print("pure", polynomial_string(row, pure_pairs))

    print("pair quotient bilinear ranks:")
    for pair, datum in pair_quotient_bilinear_ranks(q0, variables, basis).items():
        print(pair, datum)


if __name__ == "__main__":
    main()
