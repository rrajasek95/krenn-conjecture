#!/usr/bin/env python3
"""Verify generic rank 84 of the full Jacobian on the rank-53 GHZ8 chart.

The 26-parameter Laurent chart has 26 evident tangent directions.  This
checker constructs two further kernel vectors over the Laurent polynomial
ring, supported on 24 and 17 cells respectively.  Together they force every
85-minor of the 256-by-112 GHZ Jacobian to vanish identically on the chart.
The rational seed has rank 84, so the Laurent-function-field rank is exactly
84 and the rank is constantly 84 on a Zariski neighbourhood of that seed.

This does not claim rank 84 at every specialization of the chart: the rank
may drop on the closed set where all 84-minors vanish.

Standard-library arithmetic only; assertions remain live under ``python3
-O`` and ``python3 -I -S``.
"""

from fractions import Fraction as Q
from pathlib import Path
import runpy


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


TANGENT_PATH = Path(__file__).with_name(
    "verify_binary_ghz8_rank53_two_cell_tangent_isolation.py"
)
TANGENT = runpy.run_path(str(TANGENT_PATH))
SOURCE = TANGENT["SOURCE"]
LaurentPolynomial = SOURCE["LaurentPolynomial"]
DEFAULT_PARAMETERS = SOURCE["DEFAULT_PARAMETERS"]
named_cell = SOURCE["named_cell"]
parameterized_source = SOURCE["parameterized_source"]
source = SOURCE["source"]
field_rank = SOURCE["field_rank"]
ALL_CELLS = TANGENT["ALL_CELLS"]
CELL_INDEX = {cell: index for index, cell in enumerate(ALL_CELLS)}
full_jacobian = TANGENT["full_jacobian"]


# These are the supports found by exact kernel reduction at the rational
# seed.  The elimination below proves that they persist over the Laurent
# chart; their order is part of the certificate.
FIRST_SUPPORT = (
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 3, 1, 1),
    (0, 4, 0, 0),
    (1, 2, 0, 0),
    (1, 2, 0, 1),
    (1, 4, 0, 1),
    (1, 5, 0, 0),
    (1, 6, 0, 0),
    (1, 6, 1, 1),
    (1, 7, 0, 0),
    (2, 4, 1, 1),
    (0, 2, 0, 0),
    (0, 2, 1, 0),
    (0, 4, 0, 1),
    (0, 4, 1, 1),
    (1, 2, 1, 0),
    (1, 4, 1, 1),
    (2, 5, 0, 0),
    (2, 7, 0, 0),
    (2, 7, 0, 1),
    (4, 5, 1, 0),
    (4, 7, 1, 0),
    (4, 7, 1, 1),
)

SECOND_SUPPORT = (
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 3, 1, 1),
    (0, 4, 0, 0),
    (1, 2, 0, 0),
    (1, 2, 0, 1),
    (1, 4, 0, 1),
    (1, 5, 0, 0),
    (1, 6, 0, 0),
    (1, 6, 1, 1),
    (1, 7, 0, 0),
    (2, 4, 1, 1),
    (1, 2, 1, 1),
    (1, 6, 1, 0),
    (2, 5, 1, 0),
    (2, 6, 1, 0),
    (5, 6, 0, 0),
)


def formal_chart():
    names = tuple(sorted(DEFAULT_PARAMETERS))
    parameters = {
        name: LaurentPolynomial.variable(index, len(names))
        for index, name in enumerate(names)
    }
    return names, parameterized_source(parameters)


def as_laurent(value, variable_count):
    if isinstance(value, LaurentPolynomial):
        return value
    return LaurentPolynomial.constant(value, variable_count)


def restricted_jacobian(jacobian, support, variable_count):
    columns = tuple(CELL_INDEX[cell] for cell in support)
    return [
        [as_laurent(row[column], variable_count) for column in columns]
        for row in jacobian
    ]


def monomial_reduce(matrix, pivot_columns):
    """RREF the stated columns, using only Laurent-monomial units."""

    rows = [list(row) for row in matrix]
    for rank, column in enumerate(pivot_columns):
        pivot = next(
            (
                row
                for row in range(rank, len(rows))
                if rows[row][column] and len(rows[row][column].terms) == 1
            ),
            None,
        )
        require(pivot is not None, f"no monomial pivot in column {column}")
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
    return rows


def first_extra_kernel(matrix, zero, one):
    """Construct the 24-cell syzygy with x1600 as free coordinate."""

    free = 8
    pivots = tuple(range(8)) + tuple(range(9, len(FIRST_SUPPORT)))
    reduced = monomial_reduce(matrix, pivots)
    require(
        all(not any(row) for row in reduced[len(pivots) :]),
        "the first Laurent reduction gained a residual equation",
    )

    vector = [zero] * len(FIRST_SUPPORT)
    vector[free] = one
    for row, pivot in enumerate(pivots):
        vector[pivot] = -reduced[row][free]
    require(
        vector[FIRST_SUPPORT.index((4, 7, 1, 1))],
        "the first extra kernel lost its distinguishing missing cell",
    )
    return vector


def second_extra_kernel(matrix, zero):
    """Construct the 17-cell syzygy from its last two-column relation."""

    free = (8, 16)
    pivots = tuple(range(8)) + tuple(range(9, 16))
    reduced = monomial_reduce(matrix, pivots)
    residual = [row for row in reduced[len(pivots) :] if any(row)]
    require(len(residual) == 1, "second Laurent residual is not one equation")
    relation = residual[0]
    require(
        tuple(index for index, entry in enumerate(relation) if entry) == free,
        "second Laurent residual changed support",
    )
    require(
        all(len(relation[index].terms) == 2 for index in free),
        "second Laurent residual lost its two-term form",
    )

    # If the last relation is a*x1600 + b*x5600 = 0, take (b,-a).
    vector = [zero] * len(SECOND_SUPPORT)
    vector[free[0]] = relation[free[1]]
    vector[free[1]] = -relation[free[0]]
    for row, pivot in enumerate(pivots):
        vector[pivot] = -sum(
            (reduced[row][index] * vector[index] for index in free), zero
        )
    require(
        vector[SECOND_SUPPORT.index((5, 6, 0, 0))],
        "the second extra kernel lost its distinguishing missing cell",
    )
    return vector


def verify_kernel(matrix, vector, zero, label):
    for row, equation in enumerate(matrix):
        value = sum(
            (entry * coordinate for entry, coordinate in zip(equation, vector)),
            zero,
        )
        require(not value, f"{label} failed at Jacobian row {row}")


def laurent_derivative(polynomial, variable, variable_count):
    polynomial = as_laurent(polynomial, variable_count)
    terms = {}
    for exponent, coefficient in polynomial.terms.items():
        power = exponent[variable]
        if not power:
            continue
        derivative_exponent = list(exponent)
        derivative_exponent[variable] -= 1
        derivative_exponent = tuple(derivative_exponent)
        terms[derivative_exponent] = (
            terms.get(derivative_exponent, Q(0)) + coefficient * power
        )
    return LaurentPolynomial(terms, variable_count)


def evaluate_laurent(polynomial, names, values):
    return sum(
        coefficient
        * product(values[name] ** power for name, power in zip(names, exponent))
        for exponent, coefficient in polynomial.terms.items()
    )


def product(factors):
    answer = Q(1)
    for factor in factors:
        answer *= factor
    return answer


def verify_chart_tangents(names, cells, jacobian, zero, one):
    """Verify the 26 chart derivatives and their identity coordinate block."""

    parameter_cells = tuple(named_cell(name) for name in names)
    for variable in range(len(parameter_cells)):
        vector = [zero] * len(ALL_CELLS)
        for cell, value in cells.items():
            vector[CELL_INDEX[cell]] = laurent_derivative(
                value, variable, len(names)
            )
        require(
            tuple(vector[CELL_INDEX[cell]] for cell in parameter_cells)
            == tuple(
                one if index == variable else zero
                for index in range(len(names))
            ),
            f"chart tangent {variable} lost its identity coordinate block",
        )
        for row, equation in enumerate(jacobian):
            value = sum(
                (
                    as_laurent(entry, len(names)) * coordinate
                    for entry, coordinate in zip(equation, vector)
                ),
                zero,
            )
            require(not value, f"chart tangent {variable} failed at row {row}")


def main():
    names, cells = formal_chart()
    zero = LaurentPolynomial.constant(0, len(names))
    one = LaurentPolynomial.constant(1, len(names))
    jacobian = full_jacobian(cells)

    first_matrix = restricted_jacobian(
        jacobian, FIRST_SUPPORT, len(names)
    )
    second_matrix = restricted_jacobian(
        jacobian, SECOND_SUPPORT, len(names)
    )
    first = first_extra_kernel(first_matrix, zero, one)
    second = second_extra_kernel(second_matrix, zero)
    verify_kernel(first_matrix, first, zero, "first extra kernel")
    verify_kernel(second_matrix, second, zero, "second extra kernel")
    verify_chart_tangents(names, cells, jacobian, zero, one)

    # The two distinguishing missing cells make the extra vectors independent
    # modulo the 26 chart tangents, whose support is contained in `cells`.
    require((4, 7, 1, 1) not in cells, "first missing cell became active")
    require((5, 6, 0, 0) not in cells, "second missing cell became active")
    require(
        (4, 7, 1, 1) not in SECOND_SUPPORT,
        "second kernel gained the first distinguishing cell",
    )
    require(
        (5, 6, 0, 0) not in FIRST_SUPPORT,
        "first kernel gained the second distinguishing cell",
    )
    require(
        evaluate_laurent(
            first[FIRST_SUPPORT.index((4, 7, 1, 1))],
            names,
            DEFAULT_PARAMETERS,
        ),
        "first distinguishing coordinate vanished at the rational seed",
    )
    require(
        evaluate_laurent(
            second[SECOND_SUPPORT.index((5, 6, 0, 0))],
            names,
            DEFAULT_PARAMETERS,
        ),
        "second distinguishing coordinate vanished at the rational seed",
    )

    rational_rank = field_rank(full_jacobian(source()))
    require(rational_rank == 84, "rational-seed Jacobian rank changed")

    print("verified 26 independent Laurent chart tangents")
    print("verified two independent extra Laurent kernel vectors")
    print("verified all full-Jacobian 85-minors vanish identically on the chart")
    print("verified Laurent-function-field rank 84 from the rational seed")
    print("scope: rank 84 locally near the seed; special chart ranks may drop")


if __name__ == "__main__":
    main()
