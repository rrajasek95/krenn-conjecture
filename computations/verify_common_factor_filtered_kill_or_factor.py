#!/usr/bin/env python3
"""Exact audit for the four-site colon guard in the companion note."""

from fractions import Fraction
from itertools import combinations, product


SITES = tuple(range(4))
COLOURS = tuple(range(3))
EMPTY = -1


def unit(site, colour):
    word = [EMPTY] * len(SITES)
    word[site] = colour
    return {tuple(word): Fraction(1)}


def add(left, right):
    out = dict(left)
    for word, coefficient in right.items():
        out[word] = out.get(word, Fraction(0)) + coefficient
        if not out[word]:
            del out[word]
    return out


def scale(poly, scalar):
    return {
        word: scalar * coefficient
        for word, coefficient in poly.items()
        if scalar * coefficient
    }


def multiply(left, right):
    out = {}
    for u, cu in left.items():
        for v, cv in right.items():
            word = list(u)
            for site, colour in enumerate(v):
                if colour == EMPTY:
                    continue
                if word[site] != EMPTY:
                    break
                word[site] = colour
            else:
                key = tuple(word)
                out[key] = out.get(key, Fraction(0)) + cu * cv
                if not out[key]:
                    del out[key]
    return out


def edge(i, j):
    return multiply(unit(i, 0), unit(j, 0))


def quadratic(vertices):
    out = {}
    for i, j in combinations(vertices, 2):
        out = add(out, edge(i, j))
    return out


def rank(matrix):
    matrix = [list(map(Fraction, row)) for row in matrix]
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def column_rank(columns):
    words = sorted({word for column in columns for word in column})
    matrix = [
        [column.get(word, Fraction(0)) for column in columns]
        for word in words
    ]
    return rank(matrix)


def audit_physical_span_support_ledger():
    """Audit the support implication in Theorem 3.1."""
    allowed = []
    row_sparse = 0
    for entries in product((0, 1), repeat=9):
        support = [
            {column for column in COLOURS if entries[3 * row + column]}
            for row in COLOURS
        ]
        if any(len(row_support) > 1 for row_support in support):
            continue
        row_sparse += 1
        selected = set().union(*support)
        if len(selected) <= 1:
            allowed.append(entries)

    # Four choices per row (zero or one of three columns), then the shared
    # complement factor leaves zero plus seven nonzero row patterns in each
    # of the three possible common columns.
    assert row_sparse == 4 ** 3
    assert len(allowed) == 1 + 3 * (2 ** 3 - 1)
    identity = tuple(int(row == column) for row in COLOURS for column in COLOURS)
    assert identity not in allowed
    return row_sparse, len(allowed)


def main():
    row_sparse, shared_factor = audit_physical_span_support_ledger()
    q = quadratic(SITES)
    q_second = scale(multiply(q, q), Fraction(1, 2))
    pure = tuple([0] * len(SITES))
    assert q_second == {pure: Fraction(3)}

    active_complements = 0
    for i, j in combinations(SITES, 2):
        complement = tuple(site for site in SITES if site not in (i, j))
        cofactor = quadratic(complement)
        assert cofactor == edge(*complement)
        assert multiply(edge(i, j), cofactor) == {pure: Fraction(1)}
        active_complements += 1
    assert active_complements == 6

    odd_sites = (0, 1, 2)
    z = quadratic(odd_sites)
    h = add(unit(0, 0), scale(unit(1, 0), -1))
    assert h
    assert not multiply(h, z)

    columns = [
        multiply(unit(site, colour), z)
        for site in odd_sites
        for colour in COLOURS
    ]
    one_hole_rank = column_rank(columns)
    assert len(columns) == 9
    assert one_hole_rank == 7

    print("four-site pair top: q^[2] = 3 X_0")
    print(
        "physical-span ledgers "
        f"(row-sparse, shared-complement)={row_sparse, shared_factor}"
    )
    print(f"active pair complements={active_complements}")
    print(f"one-hole multiplication rank={one_hole_rank}/9, nullity=2")
    print("common-factor filtered kill-or-factor guard: PASS")


if __name__ == "__main__":
    main()
