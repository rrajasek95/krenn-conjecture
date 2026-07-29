#!/usr/bin/env python3
"""Exact audit for the axial sole-extra-plane response.

The proof uses only diagonal source 11 and 22 rows, so the direct
coordinate-factor term vanishes identically.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb, factorial

import sympy as sp


H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
I = sp.eye(3)
D = sp.diag(1, 1, 0)
ZERO = sp.zeros(3)
KAPPA = sp.Rational(1, 2)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in perfect_matchings(
            vertices[1:position] + vertices[position + 1 :]
        )
    )


def permanent(matrix: sp.Matrix) -> sp.Expr:
    rows, columns = matrix.shape
    assert rows == columns
    if rows == 0:
        return sp.S.One
    return sum(
        matrix[0, column]
        * permanent(matrix.minor_submatrix(0, column))
        for column in range(columns)
    )


class AxialResponse:
    def __init__(self, r: int, exceptional_betas, axial_parameter):
        self.r = r
        self.exceptional_betas = tuple(map(sp.sympify, exceptional_betas))
        self.t = len(self.exceptional_betas)
        self.common_live_count = 2 * r - self.t
        assert self.common_live_count >= 0
        self.active_count = self.common_live_count + 2

        self.exceptional = tuple(range(self.t))
        self.active = tuple(
            range(self.t, self.t + self.active_count)
        )
        self.extra = self.t + self.active_count
        self.site_count = self.extra + 1

        extra = sp.Matrix(
            [[1, 0, 0], [0, axial_parameter, 1], [0, 0, 0]]
        )
        self.matrices = (
            (I,) * self.t
            + (I,) * self.common_live_count
            + (D, D)
            + (extra,)
        )
        self.betas = (
            self.exceptional_betas
            + (sp.S.One,) * (self.active_count + 1)
        )
        self.columns = tuple(
            (site, colour)
            for site in self.active + (self.extra,)
            for colour in range(3)
        )
        self.column_index = {
            column: index for index, column in enumerate(self.columns)
        }
        self.blocks = {
            (left, right): sp.simplify(
                self.matrices[left]
                * H
                * self.matrices[right].T
                / (self.betas[left] + self.betas[right])
            )
            for left, right in combinations(range(self.site_count), 2)
        }

    def edge(self, word, left: int, right: int):
        if left < right:
            return self.blocks[left, right][word[left], word[right]]
        return self.blocks[right, left][word[right], word[left]]

    def hafnian(self, word, vertices):
        return sum(
            (
                sp.prod(
                    self.edge(word, left, right)
                    for left, right in matching
                )
                for matching in perfect_matchings(tuple(vertices))
            ),
            sp.S.Zero,
        )

    def response(self, word, source: int):
        """Return the full active-plus-extra star row for diagonal source."""
        word = tuple(word)
        row = [sp.S.Zero] * len(self.columns)
        for left, right in combinations(range(self.site_count), 2):
            marked = (
                2
                * self.matrices[left][word[left], source]
                * self.matrices[right][word[right], source]
            )
            if marked == 0:
                continue
            for star in self.active + (self.extra,):
                if star in (left, right):
                    continue
                remaining = tuple(
                    site
                    for site in range(self.site_count)
                    if site not in (left, right, star)
                )
                row[self.column_index[star, word[star]]] += (
                    marked * self.hafnian(word, remaining)
                )
        return tuple(sp.cancel(entry) for entry in row)

    def entry(self, row, site: int, colour: int):
        return row[self.column_index[site, colour]]


def assert_supported_on(response, audit: AxialResponse, allowed):
    allowed = set(allowed)
    assert all(
        entry == 0 or column in allowed
        for column, entry in zip(audit.columns, response)
    )


def audit_subset_range(r: int, exceptional_betas, axial_parameter):
    audit = AxialResponse(r, exceptional_betas, axial_parameter)
    t = audit.t
    assert 1 <= t <= r + 1
    marked = audit.exceptional[0]
    subset_size = r + 2 - t
    lambdas = [
        1 / (1 + value) for value in audit.exceptional_betas[1:]
    ]
    pivot = (
        2
        * factorial(r)
        * sp.prod(lambdas)
        * KAPPA ** (r - t + 1)
    )

    incidence_rows = []
    for subset in combinations(audit.active, subset_size):
        subset = set(subset)
        word = [1] * audit.site_count
        for site in audit.exceptional:
            word[site] = 0
        word[marked] = 2
        word[audit.extra] = 1
        for site in subset:
            word[site] = 0
        response = audit.response(word, 2)
        for site in audit.active:
            expected = pivot if site in subset else 0
            assert sp.cancel(audit.entry(response, site, word[site]) - expected) == 0
        assert audit.entry(response, audit.extra, 1) == 0
        incidence_rows.append(
            [int(site in subset) for site in audit.active]
        )

        swapped_word = [
            2 if site == marked
            else 1 if site in audit.exceptional
            else 0
            for site in range(audit.site_count)
        ]
        swapped_word[audit.extra] = 1
        for site in subset:
            swapped_word[site] = 1
        response = audit.response(swapped_word, 2)
        for site in audit.active:
            expected = pivot if site in subset else 0
            assert sp.cancel(
                audit.entry(response, site, swapped_word[site]) - expected
            ) == 0
        assert audit.entry(response, audit.extra, 1) == 0

    assert sp.Matrix(incidence_rows).rank() == audit.active_count

    audit_extra_cleanup(audit)

    # The row-two step is triangular after binary active rows and the
    # entire extra block have vanished.
    for target in audit.active:
        subset = set(next(
            choice
            for choice in combinations(audit.active, subset_size)
            if target in choice
        ))
        word = [1] * audit.site_count
        for site in audit.exceptional:
            word[site] = 0
        word[marked] = 2
        word[audit.extra] = 1
        for site in subset:
            word[site] = 0
        word[target] = 2
        response = audit.response(word, 2)
        assert sp.cancel(audit.entry(response, target, 2) - pivot) == 0
        killed = {
            (site, colour)
            for site in audit.active
            for colour in (0, 1)
        } | {
            (audit.extra, colour) for colour in range(3)
        }
        assert_supported_on(response, audit, killed | {(target, 2)})


def audit_extra_cleanup(audit: AxialResponse):
    r, t = audit.r, audit.t
    if t >= 2:
        word = [1] * audit.site_count
        for site in audit.exceptional:
            word[site] = 0
        word[audit.exceptional[0]] = 2
        word[audit.exceptional[1]] = 2
        for site in audit.active[: r + 2 - t]:
            word[site] = 0
        expected = (
            2
            * factorial(r)
            * sp.prod(
                1 / (1 + audit.exceptional_betas[index])
                for index in range(2, t)
            )
            * KAPPA ** (r - t + 2)
        )
        source = 2
    else:
        word = [1] * audit.site_count
        word[audit.exceptional[0]] = 0
        for site in audit.active[: r - 1]:
            word[site] = 0
        expected = (
            2
            * comb(r + 2, 2)
            * factorial(r)
            / (1 + audit.exceptional_betas[0])
            * KAPPA ** (r - 1)
        )
        source = 1

    for extra_colour in range(3):
        word[audit.extra] = extra_colour
        response = audit.response(word, source)
        assert sp.cancel(
            audit.entry(response, audit.extra, extra_colour) - expected
        ) == 0
        allowed = {
            (site, word[site]) for site in audit.active
        } | {(audit.extra, extra_colour)}
        assert_supported_on(response, audit, allowed)


def endpoint_pivot(exceptional_betas, marked: int, opposite: int):
    labels = set(range(len(exceptional_betas)))
    left = sorted(labels - {marked, opposite})
    special_sum = sum(
        (exceptional_betas[index] + 1)
        / (exceptional_betas[index] + exceptional_betas[opposite])
        for index in left
    )
    return sp.cancel(
        2
        * factorial(len(left) - 1)
        * sp.prod(1 / (exceptional_betas[index] + 1) for index in left)
        * special_sum
    )


def audit_endpoint(r: int, exceptional_betas, axial_parameter):
    assert len(exceptional_betas) == r + 2
    audit = AxialResponse(r, exceptional_betas, axial_parameter)
    opposite = 0
    pivots = {}
    for marked in audit.exceptional:
        if marked == opposite:
            continue
        left = set(audit.exceptional) - {marked, opposite}
        pivot = endpoint_pivot(
            audit.exceptional_betas, marked, opposite
        )
        pivots[marked] = pivot
        for target in audit.active:
            word = [1] * audit.site_count
            for site in left:
                word[site] = 0
            word[opposite] = 1
            word[marked] = 2
            word[audit.extra] = 1
            word[target] = 0
            response = audit.response(word, 2)
            assert sp.cancel(audit.entry(response, target, 0) - pivot) == 0
            assert_supported_on(response, audit, {(target, 0)})

            swapped = list(word)
            for site in left:
                swapped[site] = 1
            swapped[opposite] = 0
            for site in audit.active:
                swapped[site] = 0
            swapped[target] = 1
            response = audit.response(swapped, 2)
            assert sp.cancel(audit.entry(response, target, 1) - pivot) == 0
            assert_supported_on(response, audit, {(target, 1)})

    assert any(sp.cancel(value) != 0 for value in pivots.values())
    audit_extra_cleanup(audit)

    # Select one nonzero pivot and audit the final triangular row-two step.
    marked, pivot = next(
        (site, value)
        for site, value in pivots.items()
        if sp.cancel(value) != 0
    )
    left = set(audit.exceptional) - {marked, opposite}
    for target in audit.active:
        word = [1] * audit.site_count
        for site in left:
            word[site] = 0
        word[opposite] = 1
        word[marked] = 2
        word[audit.extra] = 1
        word[target] = 2
        response = audit.response(word, 2)
        assert sp.cancel(audit.entry(response, target, 2) - pivot) == 0
        killed = {
            (site, colour)
            for site in audit.active
            for colour in (0, 1)
        } | {
            (audit.extra, colour) for colour in range(3)
        }
        assert_supported_on(response, audit, killed | {(target, 2)})


def audit_deletion_transform():
    for r in range(2, 11):
        matrix = sp.ones(r + 1) - sp.eye(r + 1)
        assert matrix.det() == (-1) ** r * r
        assert matrix.rank() == r + 1


def main():
    u = sp.Symbol("u")
    nu = sp.Symbol("nu")
    audit_subset_range(2, [nu], u)

    # The top cancellation-free layer, with repeated exceptional values.
    audit_subset_range(3, [2, 2, 3, 3], sp.Rational(-7, 5))

    # A fully symbolic endpoint at r=2, followed by a repeated-beta
    # endpoint one order higher.
    endpoint_values = sp.symbols("v0:4")
    audit_endpoint(2, endpoint_values, u)
    audit_subset_range(2, [2, 2, 3], 0)
    audit_endpoint(2, [2, 2, 3, 3], 0)
    audit_endpoint(3, [2, 2, 3, 3, 4], sp.Rational(5, 7))

    audit_deletion_transform()
    print("Live three-zero extra-plane axial: PASS")
    print("forced {exceptional, extra} marked pair: exact")
    print("subset and endpoint response rows: exact")
    print("arbitrary axial parameter and repeated betas: retained")
    print("r=2, u=0, repeated-beta t=3/4 boundary: exact")
    print("one-point deletion transforms through r=10: full rank")


if __name__ == "__main__":
    main()
