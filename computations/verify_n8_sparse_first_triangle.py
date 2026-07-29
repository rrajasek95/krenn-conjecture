#!/usr/bin/env python3
"""Cross-check the sparse first-unit-triangle finder exhaustively."""

from itertools import combinations, product
from random import Random

import search_n8_binomial_support_full_sat as full
import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric
import verify_n8_toric_orbit40_boundary as boundary


def difference(left, right, width):
    row = [0] * width
    for index in left:
        row[index] += 1
    for index in right:
        row[index] -= 1
    return row


def audit_result(rows, result, exhaustive):
    assert (result is None) == (not exhaustive)
    if result is None:
        return
    indices, signs = result
    assert len(indices) == len(set(indices)) == 3
    assert tuple(sorted(indices)) in exhaustive
    assert all(sign in (-1, 1) for sign in signs)
    assert sum(signs) & 1
    assert all(
        sum(
            sign * rows[index][column]
            for index, sign in zip(indices, signs)
        ) == 0
        for column in range(len(rows[0]))
    )


def random_audit():
    rng = Random(20260724)
    width = 18
    for trial in range(500):
        monomials = [
            frozenset(rng.sample(range(width), 4))
            for _ in range(14)
        ]
        rows = [
            difference(*rng.sample(monomials, 2), width)
            for _ in range(rng.randrange(3, 18))
        ]
        if trial % 2 == 0:
            first, second, third = rng.sample(monomials, 3)
            rows.extend((
                difference(first, second, width),
                difference(second, third, width),
                difference(third, first, width),
            ))
        exhaustive = toric.unit_triangle_circuits(rows)
        audit_result(
            rows, full.first_unit_triangle_circuit(rows), exhaustive
        )


def orbit40_boundary_audit():
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(signed.N), 2)
        for a, b in product(range(signed.Q), repeat=2)
    )
    cell_index = {cell: index for index, cell in enumerate(cells)}
    matchings = tuple(
        signed.core.perfect_matchings(tuple(range(signed.N)))
    )
    fibres = signed.core.exact_fibres(
        signed.N, boundary.boundary_support(), matchings
    )
    mixed = [
        (coloring, terms)
        for coloring, terms in sorted(fibres.items())
        if len(set(coloring)) > 1
    ]
    rows = [
        signed.core.exponent_row(
            terms[0][1], terms[1][1], cell_index, len(cells)
        )
        for _coloring, terms in mixed
    ]
    exhaustive = toric.unit_triangle_circuits(rows)
    assert len(exhaustive) == 48
    result = full.first_unit_triangle_circuit(rows)
    audit_result(rows, result, exhaustive)
    indices, _signs = result
    guard = {
        cell
        for index in indices
        for _matching_number, decorated in mixed[index][1]
        for cell in decorated
    }
    assert len(guard) == 10


def main():
    random_audit()
    orbit40_boundary_audit()
    print(
        "PASS sparse first-triangle finder: 500 random exact comparisons "
        "and the 48-circuit orbit-40 boundary"
    )


if __name__ == "__main__":
    main()
