#!/usr/bin/env python3
"""Exact response-local Artin jet at the nine-cell one-bad point.

The base point is the orbit-0 response point of commit e3fb47f.  We impose
the four full response tensors and require every six-site top coefficient
below the prospective pure-X2 leading order to vanish.  A source arc is
expanded through order four with all 135 endpoint-coloured cells available.

This is deliberately local: it proves a necessary finite-jet obstruction at
this response point, not a global statement about the whole one-bad ideal.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product

import sympy as sp


SITES = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    ((u, v), (a, b))
    for u, v in EDGES
    for a in COLOURS
    for b in COLOURS
)
CELL_INDEX = {source_cell: index for index, source_cell in enumerate(CELLS)}
RESPONSE_SETS = (
    (0, 1, 2, 4),
    (0, 1, 3, 5),
    (0, 1, 2, 5),
    (0, 1, 3, 4),
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def source_cell(u: int, v: int, a: int, b: int):
    if u > v:
        u, v, a, b = v, u, b, a
    return ((u, v), (a, b))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    u = vertices[0]
    return tuple(
        ((u, vertices[j]),) + rest
        for j in range(1, len(vertices))
        for rest in perfect_matchings(vertices[1:j] + vertices[j + 1 :])
    )


def matching_terms(vertices: tuple[int, ...], word: tuple[int, ...]):
    colour = dict(zip(vertices, word, strict=True))
    return tuple(
        tuple(
            CELL_INDEX[source_cell(u, v, colour[u], colour[v])]
            for u, v in matching
        )
        for matching in perfect_matchings(vertices)
    )


def base_point() -> dict[tuple[tuple[int, int], tuple[int, int]], sp.Integer]:
    # Exact nine-cell orbit-0 point from e3fb47f.
    return {
        source_cell(0, 1, 0, 1): sp.Integer(1),
        source_cell(0, 1, 1, 0): sp.Integer(1),
        source_cell(0, 2, 0, 0): sp.Integer(1),
        source_cell(0, 3, 1, 1): sp.Integer(1),
        source_cell(0, 4, 0, 0): sp.Integer(1),
        source_cell(0, 5, 1, 1): sp.Integer(1),
        source_cell(1, 3, 1, 1): sp.Integer(1),
        source_cell(1, 4, 0, 0): sp.Integer(1),
        source_cell(3, 4, 1, 0): sp.Integer(-1),
    }


def equation_terms():
    rows = []
    labels = []
    for vertices in RESPONSE_SETS:
        for word in product(COLOURS, repeat=4):
            rows.append(matching_terms(vertices, word))
            labels.append(("response", vertices, word))
    for word in product(COLOURS, repeat=6):
        rows.append(matching_terms(SITES, word))
        labels.append(("top", SITES, word))
    require(len(rows) == 1053, len(rows))
    return tuple(rows), tuple(labels)


def jacobian(rows, x0: sp.Matrix) -> sp.SparseMatrix:
    entries: defaultdict[tuple[int, int], sp.Expr] = defaultdict(lambda: 0)
    for row_index, row in enumerate(rows):
        for term in row:
            for position, variable in enumerate(term):
                coefficient = sp.prod(
                    x0[other]
                    for index, other in enumerate(term)
                    if index != position
                )
                if coefficient:
                    entries[row_index, variable] += coefficient
    return sp.SparseMatrix(len(rows), len(CELLS), dict(entries))


def symmetric_hasse_matrix(rows, x0, tangent):
    pairs = tuple((i, j) for i in range(10) for j in range(i, 10))
    entries: defaultdict[tuple[int, int], sp.Expr] = defaultdict(lambda: 0)
    for row_index, row in enumerate(rows):
        for term in row:
            for left in range(len(term)):
                for right in range(left + 1, len(term)):
                    base_factor = sp.prod(
                        x0[term[index]]
                        for index in range(len(term))
                        if index not in (left, right)
                    )
                    if not base_factor:
                        continue
                    u, v = term[left], term[right]
                    for column, (i, j) in enumerate(pairs):
                        coefficient = tangent[u, i] * tangent[v, j]
                        if i != j:
                            coefficient += tangent[u, j] * tangent[v, i]
                        if coefficient:
                            entries[row_index, column] += base_factor * coefficient
    return pairs, sp.SparseMatrix(len(rows), len(pairs), dict(entries))


def forcing_coefficient(rows, coefficients, order, selected_rows):
    """Coefficient of t^order excluding the linear x_order contribution."""
    forcing = []
    for row_index in selected_rows:
        value = 0
        for term in rows[row_index]:
            for orders in product(range(order), repeat=len(term)):
                if sum(orders) != order:
                    continue
                value += sp.prod(
                    coefficients[source_order][term[position]]
                    for position, source_order in enumerate(orders)
                )
        forcing.append(sp.expand(value))
    return sp.Matrix(forcing)


def quadratic_polynomial(row, pairs, parameters):
    return sp.factor(
        sum(
            row[column] * parameters[i] * parameters[j]
            for column, (i, j) in enumerate(pairs)
        )
    )


def main() -> None:
    rows, labels = equation_terms()
    q0 = base_point()
    require(len(q0) == 9, len(q0))
    x0 = sp.Matrix([q0.get(source, 0) for source in CELLS])
    differential = jacobian(rows, x0)
    require(differential.rank() == 125, differential.rank())
    tangent_basis = differential.nullspace()
    require(len(tangent_basis) == 10, len(tangent_basis))
    tangent = sp.Matrix.hstack(*tangent_basis)

    pure_22_indices = tuple(
        CELL_INDEX[source_cell(u, v, 2, 2)] for u, v in EDGES
    )
    require(
        all(tangent[index, column] == 0
            for index in pure_22_indices for column in range(10)),
        "a simultaneous response/top tangent acquired a pure-22 cell",
    )

    # A deterministic 125-by-125 implicit-function block.
    _, pivot_columns = differential.rref()
    require(len(pivot_columns) == 125, len(pivot_columns))
    pivot_matrix = differential[:, list(pivot_columns)]
    _, pivot_rows = pivot_matrix.T.rref()
    require(len(pivot_rows) == 125, len(pivot_rows))
    unit_block = pivot_matrix[list(pivot_rows), :]
    inverse = unit_block.inv()
    require(unit_block.det() in (1, -1), unit_block.det())
    pivot_position = {variable: index for index, variable in enumerate(pivot_columns)}
    require(all(index in pivot_position for index in pure_22_indices),
            "a pure-22 cell stopped being an implicit pivot")

    # The full second fundamental form has exactly two compatibility classes.
    pairs, second_hasse = symmetric_hasse_matrix(rows, x0, tangent)
    second_pivot = -inverse * second_hasse[list(pivot_rows), :]
    second_residual = pivot_matrix * second_pivot + second_hasse
    require((second_residual.rank(), second_residual.nnz()) == (2, 2),
            (second_residual.rank(), second_residual.nnz()))
    _, obstruction_rows = second_residual.T.rref()
    require(obstruction_rows == (217, 226), obstruction_rows)
    first_parameters = sp.symbols("a0:10")
    obstructions = tuple(
        quadratic_polynomial(second_residual[row, :], pairs, first_parameters)
        for row in obstruction_rows
    )
    require(obstructions == (-first_parameters[2] * first_parameters[9],
                             -first_parameters[5] * first_parameters[9]),
            obstructions)
    require(
        tuple(labels[row] for row in obstruction_rows)
        == (
            ("response", (0, 1, 2, 5), (2, 0, 0, 1)),
            ("response", (0, 1, 2, 5), (2, 1, 0, 1)),
        ),
        tuple(labels[row] for row in obstruction_rows),
    )

    # Necessary implicit Artin recursion.  At each order an arbitrary kernel
    # vector is retained, so this covers every branch, not a chosen slice.
    coefficients = [x0, tangent * sp.Matrix(first_parameters)]
    pure_counts = [
        sum(coefficients[1][index] != 0 for index in pure_22_indices)
    ]
    for order, names in ((2, "b0:10"), (3, "c0:10"), (4, "d0:10")):
        forcing = forcing_coefficient(rows, coefficients, order, pivot_rows)
        pivot_solution = -inverse * forcing
        correction = sp.zeros(len(CELLS), 1)
        for position, variable in enumerate(pivot_columns):
            correction[variable] = pivot_solution[position]
        correction += tangent * sp.Matrix(sp.symbols(names))
        require(
            differential[list(pivot_rows), :] * correction + forcing
            == sp.zeros(len(pivot_rows), 1),
            f"order-{order} implicit solve changed",
        )
        coefficients.append(correction)
        pure_count = sum(
            sp.expand(correction[index]) != 0 for index in pure_22_indices
        )
        pure_counts.append(pure_count)
    require(pure_counts == [0, 0, 0, 0], pure_counts)

    print("N=8 one-bad response-local Artin jet: PASS")
    print("combined response/top differential rank / kernel: 125 / 10")
    print("pure-22 tangent cells: 0 of 15")
    print("second compatibility rank / nonzeros: 2 / 2")
    print("quadratic obstructions: -a2*a9, -a5*a9")
    print("pure-22 source corrections at orders 1..4: 0,0,0,0")
    print("therefore the pure-X2 top coefficient has t-valuation at least 15")
    print("scope: necessary local jet at e3fb47f; no all-order/global exclusion")


if __name__ == "__main__":
    main()
