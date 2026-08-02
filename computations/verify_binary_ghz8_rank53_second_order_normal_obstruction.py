#!/usr/bin/env python3
"""Exact second-order obstruction to the two non-chart GHZ8 tangents.

At the rational rank-53 seed, the full GHZ8 Jacobian has a 28-dimensional
kernel.  The exact rational chart supplies 26 directions; the quotient has
two further tangent classes.  This checker proves that no tangent with a
nonzero component in those two classes lifts through second order.

The statement is local at this seed and concerns the first derivative of a
formal arc.  It does not exclude an arc tangent to the chart to first order
and leaving it only at a higher order, a distant component, or a rank-54/55
source elsewhere.

Standard-library Fraction arithmetic only; live under ``python3 -O`` and
``python3 -I -S``.
"""

from fractions import Fraction as Q
from itertools import combinations_with_replacement
from pathlib import Path
import runpy


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


TANGENT_PATH = Path(__file__).with_name(
    "verify_binary_ghz8_rank53_two_cell_tangent_isolation.py"
)
TANGENT = runpy.run_path(str(TANGENT_PATH))
ALL_CELLS = TANGENT["ALL_CELLS"]
CELL_INDEX = {cell: index for index, cell in enumerate(ALL_CELLS)}
full_jacobian = TANGENT["full_jacobian"]
reduce_active_columns = TANGENT["reduce_active_columns"]
source = TANGENT["source"]
SOURCE = TANGENT["SOURCE"]
VERTICES = SOURCE["VERTICES"]
WORDS8 = SOURCE["WORDS8"]
MATCHINGS = SOURCE["MATCHINGS"][VERTICES]


def rref(matrix):
    rows = [list(row) for row in matrix]
    width = len(rows[0]) if rows else 0
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(rows))
             if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            multiple = rows[index][column]
            rows[index] = [
                left - multiple * right
                for left, right in zip(rows[index], rows[rank])
            ]
        pivots.append(column)
        rank += 1
    return rank, tuple(pivots), rows


def nullspace_from_rref(width, pivots, reduced):
    free = tuple(column for column in range(width) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(vector)
    return free, basis


def tangent_bases(cells, jacobian):
    active = tuple(
        index for index, cell in enumerate(ALL_CELLS) if cell in cells
    )
    missing = tuple(
        index for index, cell in enumerate(ALL_CELLS) if cell not in cells
    )
    order = active + missing
    reordered = [[row[index] for index in order] for row in jacobian]
    active_rank, active_pivots, reduced = reduce_active_columns(
        reordered, len(active)
    )
    require(active_rank == 19, "active Jacobian rank changed")

    active_free = tuple(
        column for column in range(len(active))
        if column not in active_pivots
    )
    chart_basis = []
    for free_column in active_free:
        active_vector = [Q(0)] * len(active)
        active_vector[free_column] = Q(1)
        for row, pivot in enumerate(active_pivots):
            active_vector[pivot] = -reduced[row][free_column]
        full = [Q(0)] * len(ALL_CELLS)
        for offset, index in enumerate(active):
            full[index] = active_vector[offset]
        chart_basis.append(full)
    require(len(chart_basis) == 26, "chart tangent dimension changed")

    quotient = [
        row[len(active):]
        for row in reduced[active_rank:]
    ]
    quotient_rank, quotient_pivots, quotient_reduced = rref(quotient)
    require(quotient_rank == 65, "missing-cell quotient rank changed")
    missing_free, missing_nullspace = nullspace_from_rref(
        len(missing), quotient_pivots, quotient_reduced
    )
    require(
        tuple(ALL_CELLS[missing[index]] for index in missing_free)
        == ((4, 7, 1, 1), (5, 6, 0, 0)),
        "normal tangent coordinates changed",
    )

    normal_basis = []
    for missing_vector in missing_nullspace:
        active_rhs = [
            sum(
                reduced[row][len(active) + offset]
                * missing_vector[offset]
                for offset in range(len(missing))
            )
            for row in range(active_rank)
        ]
        active_vector = [Q(0)] * len(active)
        for row, pivot in enumerate(active_pivots):
            active_vector[pivot] = -active_rhs[row]

        full = [Q(0)] * len(ALL_CELLS)
        for offset, index in enumerate(active):
            full[index] = active_vector[offset]
        for offset, index in enumerate(missing):
            full[index] = missing_vector[offset]
        normal_basis.append(full)
    require(len(normal_basis) == 2, "normal tangent dimension changed")
    return chart_basis, normal_basis


# Three sparse left-cokernel functionals obtained by exact row reduction of
# the full 256-by-112 Jacobian.  Keys are binary-word row indices.
FUNCTIONALS = (
    {72: Q(-1175, 258), 200: Q(1)},
    {104: Q(-1175, 258), 232: Q(1)},
    {96: Q(1)},
)


def apply_functional(functional, vector):
    return sum(weight * vector[row] for row, weight in functional.items())


def second_coefficient_at(cells, word_index, left, right, same=False):
    """Coefficient of st (or s^2 when same) in the matching tensor."""

    word = WORDS8[word_index]
    answer = Q(0)
    for matching in MATCHINGS:
        indices = tuple(
            CELL_INDEX[u, v, word[u], word[v]]
            for u, v in matching
        )
        base = tuple(cells.get(ALL_CELLS[index], 0) for index in indices)
        for first in range(4):
            for second in range(first + 1, 4):
                complement = Q(1)
                for position in range(4):
                    if position not in (first, second):
                        complement *= base[position]
                if same:
                    answer += (
                        left[indices[first]] * left[indices[second]]
                        * complement
                    )
                else:
                    answer += (
                        left[indices[first]] * right[indices[second]]
                        + right[indices[first]] * left[indices[second]]
                    ) * complement
    return answer


def functional_second_coefficient(
    cells, functional, left, right, same=False
):
    return sum(
        weight * second_coefficient_at(
            cells, word_index, left, right, same=same
        )
        for word_index, weight in functional.items()
    )


def verify_tangent_vectors(jacobian, vectors):
    for number, vector in enumerate(vectors):
        for row, equation in enumerate(jacobian):
            require(
                sum(entry * coordinate
                    for entry, coordinate in zip(equation, vector)) == 0,
                f"tangent {number} failed at row {row}",
            )


def main():
    cells = source()
    jacobian = full_jacobian(cells)
    chart_basis, normal_basis = tangent_bases(cells, jacobian)
    verify_tangent_vectors(jacobian, chart_basis + normal_basis)

    for number, functional in enumerate(FUNCTIONALS):
        for column in range(len(ALL_CELLS)):
            require(
                sum(
                    weight * jacobian[row][column]
                    for row, weight in functional.items()
                ) == 0,
                f"functional {number} left the Jacobian cokernel",
            )

    t0, t1 = normal_basis
    normal_quadratics = (
        (t0, t0, True),
        (t0, t1, False),
        (t1, t1, True),
    )
    obstruction_matrix = [
        [
            functional_second_coefficient(
                cells, functional, left, right, same=same
            )
            for left, right, same in normal_quadratics
        ]
        for functional in FUNCTIONALS
    ]
    require(
        obstruction_matrix == [
            [Q(1566568103750000, 145242430893), Q(0), Q(0)],
            [Q(0), Q(631124000000, 21744264209), Q(0)],
            [Q(0), Q(0), Q(-6048000, 27732773)],
        ],
        "normal quadratic obstruction matrix changed",
    )

    chart_pairs = 0
    for first, second in combinations_with_replacement(
        range(len(chart_basis)), 2
    ):
        chart_pairs += 1
        for functional in FUNCTIONALS:
            require(
                functional_second_coefficient(
                    cells,
                    functional,
                    chart_basis[first],
                    chart_basis[second],
                    same=first == second,
                ) == 0,
                "a chart-chart quadratic gained a cokernel component",
            )
    require(chart_pairs == 351, "chart-pair census changed")

    cross_terms = 0
    for normal in normal_basis:
        for chart in chart_basis:
            cross_terms += 1
            for functional in FUNCTIONALS:
                require(
                    functional_second_coefficient(
                        cells, functional, normal, chart
                    ) == 0,
                    "a chart-normal quadratic gained a cokernel component",
                )
    require(cross_terms == 52, "chart-normal census changed")

    print("verified tangent kernel = 26 chart + 2 normal directions")
    print("verified three exact Jacobian-cokernel functionals")
    print("verified 351 chart-chart and 52 chart-normal quadratic reductions")
    print("verified normal obstruction diagonal in a^2, ab, b^2")
    print("scope: no second-order lift with first-order normal component")


if __name__ == "__main__":
    main()
