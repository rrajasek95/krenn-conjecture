#!/usr/bin/env python3
"""Independent exact audit of the n=8 toric binomial lattice engine.

This checker deliberately derives consistency from a Smith decomposition of
the *unaugmented* exponent matrix, rather than from the augmented row-HNF used
by ``search_n8_toric_binomial_lazy_cegar.py``.  It exhausts small integer
matrices, reconstructs rational phases for every consistent case, and checks
the resulting root-of-unity equations exactly.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import lcm
import random

from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

import search_n8_toric_binomial_lazy_cegar as search


def integer_entries(matrix):
    return [
        [int(matrix[i, j].element) for j in range(matrix.shape[1])]
        for i in range(matrix.shape[0])
    ]


def independent_smith_consistency(rows, columns):
    """Test whether ``D theta = 1/2`` in ``(Q/Z)^r`` using only SNF."""

    if not rows:
        return True
    matrix = DomainMatrix.from_list([list(row) for row in rows], ZZ)
    diagonal, left, _right = smith_normal_decomp(matrix)
    s = integer_entries(diagonal)
    u = integer_entries(left)
    transformed_twice_rhs = [sum(row) for row in u]
    for i in range(len(rows)):
        diagonal_entry = s[i][i] if i < min(len(rows), columns) else 0
        if diagonal_entry == 0 and transformed_twice_rhs[i] % 2:
            return False
    return True


def audit_matrix(rows, columns):
    hnf_consistent, _lattice = search.toric.signed_quotient_lattice(
        rows, columns
    )
    smith_consistent = independent_smith_consistency(rows, columns)
    assert hnf_consistent == smith_consistent, (rows, hnf_consistent)
    if not hnf_consistent:
        return

    phases = search.rational_phase_solution(rows, columns)
    assert len(phases) == columns
    order = 1
    for phase in phases:
        order = lcm(order, phase.denominator)
    order = lcm(order, 2)
    exponents = [int(phase * order) % order for phase in phases]
    for row in rows:
        assert (
            sum(coefficient * exponent
                for coefficient, exponent in zip(row, exponents))
            % order
            == order // 2
        ), (rows, order, exponents)


def main():
    checked = 0

    # Exhaust all matrices with entries in {-1,0,1}, through four equations
    # in two variables.  These include zero rows, duplicate/opposite rows,
    # nonsaturated row lattices, and every small odd-dependency pattern.
    for columns in (1, 2):
        for number_rows in range(0, 5):
            for flat in product((-1, 0, 1), repeat=columns * number_rows):
                rows = [
                    list(flat[columns * i:columns * (i + 1)])
                    for i in range(number_rows)
                ]
                audit_matrix(rows, columns)
                checked += 1

    # Exercise wider rectangular matrices and larger invariant factors.
    rng = random.Random(0xC0FFEE)
    for _ in range(5000):
        columns = rng.randrange(1, 8)
        number_rows = rng.randrange(0, 10)
        rows = [
            [rng.randrange(-4, 5) for _ in range(columns)]
            for _ in range(number_rows)
        ]
        audit_matrix(rows, columns)
        checked += 1

    triangle_instances = 0
    for _ in range(500):
        columns = rng.randrange(1, 8)
        number_rows = rng.randrange(3, 10)
        rows = [
            [rng.randrange(-2, 3) for _ in range(columns)]
            for _ in range(number_rows)
        ]
        found = set(search.unit_triangle_circuits(rows))
        brute = {
            indices
            for indices in combinations(range(number_rows), 3)
            if not search.toric.signed_quotient_lattice(
                [rows[index] for index in indices], columns
            )[0]
            and any(
                all(
                    sum(signs[i] * rows[index][column]
                        for i, index in enumerate(indices)) == 0
                    for column in range(columns)
                )
                for signs in product((-1, 1), repeat=3)
            )
        }
        assert found == brute, (rows, found, brute)
        triangle_instances += 1

    print(
        f"PASS: {checked} HNF/Smith instances and exact phases; "
        f"{triangle_instances} triangle-cut instances"
    )


if __name__ == "__main__":
    main()
