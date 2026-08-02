#!/usr/bin/env python3
"""Exact one-/two-cell tangent census at the rational rank-53 GHZ8 seed.

This is an infinitesimal statement at one point.  It does not exclude a
higher-order branch through that point, a distant component with enlarged
support, or a rank-54/55 source elsewhere in the binary GHZ8 fibre.

Let C be the 45-cell support of the exact rational source.  The Jacobian of
the 256 GHZ8 equations restricted to C has rank 19.  This checker proves that
adjoining any one of the 67 missing cells raises the rank to 20, and adjoining
any two raises it to 21.  Equivalently, every tangent vector supported on C
plus at most two missing cells has zero coordinate on every added cell.

The source is loaded from the companion exact checker.  Everything here uses
only standard-library exact Fraction arithmetic and remains live under
``python3 -O`` and ``python3 -I -S``.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import runpy


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SOURCE_PATH = Path(__file__).with_name(
    "verify_binary_ghz8_exact_rank53_source.py"
)
SOURCE = runpy.run_path(str(SOURCE_PATH))
VERTICES = SOURCE["VERTICES"]
EDGES = SOURCE["EDGES"]
WORDS8 = SOURCE["WORDS8"]
coefficient = SOURCE["coefficient"]
source = SOURCE["source"]
field_rank = SOURCE["field_rank"]

ALL_CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product((0, 1), repeat=2)
)


def full_jacobian(cells):
    """Return the exact 256-by-112 Jacobian of the GHZ8 coefficient map."""

    matrix = []
    for word in WORDS8:
        row = []
        for u, v, a, b in ALL_CELLS:
            if (word[u], word[v]) != (a, b):
                row.append(Q(0))
                continue
            remaining = tuple(
                vertex for vertex in VERTICES if vertex not in (u, v)
            )
            remaining_word = tuple(word[vertex] for vertex in remaining)
            row.append(coefficient(cells, remaining, remaining_word))
        matrix.append(row)
    return matrix


def reduce_active_columns(matrix, active_count):
    """Row-reduce only the active columns, applying operations globally."""

    rows = [list(row) for row in matrix]
    rank = 0
    pivots = []
    for column in range(active_count):
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


def proportional(left, right):
    """Whether two exact nonzero vectors span the same line."""

    ratio = None
    for first, second in zip(left, right):
        if not first and not second:
            continue
        if not first or not second:
            return False
        current = first / second
        if ratio is None:
            ratio = current
        elif current != ratio:
            return False
    return ratio is not None


def main():
    cells = source()
    active_indices = tuple(
        index for index, cell in enumerate(ALL_CELLS) if cell in cells
    )
    missing_indices = tuple(
        index for index, cell in enumerate(ALL_CELLS) if cell not in cells
    )
    require(len(active_indices) == 45, "active support size changed")
    require(len(missing_indices) == 67, "missing support size changed")

    order = active_indices + missing_indices
    jacobian = full_jacobian(cells)
    reordered = [[row[index] for index in order] for row in jacobian]
    active_rank, pivots, reduced = reduce_active_columns(
        reordered, len(active_indices)
    )
    require(active_rank == 19, "active-support Jacobian rank changed")
    require(
        pivots == (0, 1, 2, 3, 4, 5, 6, 7, 18, 19, 20, 21, 22,
                   23, 24, 26, 28, 29, 32),
        "active-support pivot profile changed",
    )

    # After the active columns are in reduced form, their column span consists
    # precisely of vectors supported in the first active_rank rows.  The tails
    # below those rows are therefore exact coordinates in the quotient by the
    # active column span.
    quotient_columns = tuple(
        tuple(
            reduced[row][len(active_indices) + offset]
            for row in range(active_rank, len(reduced))
        )
        for offset in range(len(missing_indices))
    )

    zero_quotient_columns = tuple(
        offset for offset, column in enumerate(quotient_columns)
        if not any(column)
    )
    require(
        not zero_quotient_columns,
        f"one-cell tangent openings appeared: {zero_quotient_columns}",
    )

    dependent_pairs = []
    checked_pairs = 0
    for first in range(len(quotient_columns)):
        for second in range(first + 1, len(quotient_columns)):
            checked_pairs += 1
            if proportional(quotient_columns[first], quotient_columns[second]):
                dependent_pairs.append((first, second))
    require(checked_pairs == 2211, "two-cell census size changed")
    require(
        not dependent_pairs,
        f"two-cell tangent openings appeared: {dependent_pairs}",
    )

    quotient_matrix = [list(row) for row in zip(*quotient_columns)]
    quotient_rank = field_rank(quotient_matrix)
    require(quotient_rank == 65, "missing-cell quotient rank changed")

    print("verified exact active-support GHZ8 Jacobian rank 19")
    print("verified all 67 one-cell augmentations have rank 20")
    print("verified all 2,211 two-cell augmentations have rank 21")
    print("verified missing-cell quotient rank 65 (full rank 84)")
    print("scope: first-order isolation at the rational rank-53 seed only")


if __name__ == "__main__":
    main()
