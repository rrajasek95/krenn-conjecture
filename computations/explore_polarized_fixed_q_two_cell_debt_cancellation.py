#!/usr/bin/env python3
"""Enumerate exact two-cell cancellations of the displayed polarized debt.

For q'=q+t*e+u*f, write X=1/t and Y=1/u.  After division by t*u,

    z*q'^[3]-Delta = 0

is the linear vector equation D_f*X + D_e*Y + D_ef = 0.  This discovery
script solves that system exactly over QQ for every unordered pair of cells
outside the sparse q and records every family with nonzero t,u.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations

from explore_polarized_fixed_q_two_extra_frontier import cross_debt
from verify_polarized_eight_site_single_invisible_cell_projective_closure_independent import (
    ALL_CELLS,
    BASE_Q,
    polarized_derivative,
)


def solve_two_variable(rows):
    """Solve A*X+B*Y=C; return (rank, one nonzero rational point) or None."""
    nonzero = [(Fraction(a), Fraction(b), Fraction(c))
               for a, b, c in rows if a or b or c]
    if not nonzero:
        return 0, (Fraction(1), Fraction(1))
    pivots = []
    for row in nonzero:
        a, b, c = row
        if not a and not b:
            return None
        if not pivots:
            pivots.append(row)
            continue
        a0, b0, c0 = pivots[0]
        determinant = a0 * b - a * b0
        if determinant:
            x = (c0 * b - c * b0) / determinant
            y = (a0 * c - a * c0) / determinant
            if not x or not y:
                return None
            if any(a1 * x + b1 * y != c1 for a1, b1, c1 in nonzero):
                return None
            return 2, (x, y)
        if a0 * c != a * c0 or b0 * c != b * c0:
            return None

    a, b, c = pivots[0]
    if b:
        for x in (Fraction(1), Fraction(2), Fraction(-1), Fraction(3)):
            y = (c - a * x) / b
            if x and y:
                return 1, (x, y)
        return None
    else:
        x = c / a
        if not x:
            return None
        return 1, (x, Fraction(1))


def main():
    extras = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
    assert len(extras) == 243
    debts = {cell: polarized_derivative(cell) for cell in extras}
    solutions = []
    ledger = Counter()
    for left, right in combinations(extras, 2):
        left_debt = debts[left]
        right_debt = debts[right]
        cross = cross_debt(left, right)
        words = set(left_debt) | set(right_debt) | set(cross)
        # D_f*X + D_e*Y = -D_ef.
        rows = [
            (right_debt[word], left_debt[word], -cross[word])
            for word in words
        ]
        answer = solve_two_variable(rows)
        if answer is None:
            continue
        rank, (x, y) = answer
        t, u = 1 / x, 1 / y
        assert t and u
        assert all(
            t * left_debt[word] + u * right_debt[word]
            + t * u * cross[word] == 0
            for word in words
        )
        visibility = (bool(left_debt), bool(right_debt))
        overlap = len(set(left[:2]) & set(right[:2]))
        ledger[rank, visibility, overlap] += 1
        solutions.append((left, right, rank, x, y))

    invisible_only = sum(
        count for (rank, visibility, _overlap), count in ledger.items()
        if visibility == (False, False)
    )
    visible = [row for row in solutions
               if debts[row[0]] or debts[row[1]]]
    print("two-cell polarized debt cancellation census: PASS")
    print("all unordered outside-cell pairs:", len(tuple(combinations(extras, 2))))
    print("solvable with t,u nonzero:", len(solutions))
    print("invisible-compatible / involving visible debt:",
          invisible_only, len(visible))
    print("ledger:")
    for key, count in sorted(ledger.items(), key=lambda item: repr(item[0])):
        print(key, count)
    print("visible-debt solutions:")
    for row in visible:
        print(row)


if __name__ == "__main__":
    main()
