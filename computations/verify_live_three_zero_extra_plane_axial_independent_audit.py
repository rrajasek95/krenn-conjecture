#!/usr/bin/env python3
"""Independent exact audit of the axial sole-extra-plane closure.

This file deliberately does not import the accompanying checker.  It builds
the marked response directly from contracted row vectors, and it retains
columns for the structurally zero exceptional stars so that the two cleanup
steps can be audited after the correct triangular quotient.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb, factorial

import sympy as sp


E0 = (sp.S.One, sp.S.Zero, sp.S.Zero)
E1 = (sp.S.Zero, sp.S.One, sp.S.Zero)
E2 = (sp.S.Zero, sp.S.Zero, sp.S.One)
ZERO = (sp.S.Zero, sp.S.Zero, sp.S.Zero)
KAPPA = sp.Rational(1, 2)


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in matchings(vertices[1:position] + vertices[position + 1 :])
    )


def h_pair(left, right):
    """The bilinear pairing for the normalized zero-diagonal H."""
    return (
        left[0] * (right[1] + right[2])
        + left[1] * (right[0] + right[2])
        + left[2] * (right[0] + right[1])
    )


def edge(rows, betas, left: int, right: int):
    return h_pair(rows[left], rows[right]) / (betas[left] + betas[right])


def hafnian(rows, betas, vertices):
    return sum(
        (
            sp.prod(edge(rows, betas, left, right) for left, right in matching)
            for matching in matchings(tuple(vertices))
        ),
        sp.S.Zero,
    )


def marked_pairs(rows, source: int):
    return tuple(
        (left, right)
        for left, right in combinations(range(len(rows)), 2)
        if sp.cancel(2 * rows[left][source] * rows[right][source]) != 0
    )


def star_contribution(rows, betas, source: int, pair, star: int):
    if star in pair:
        return sp.S.Zero
    left, right = pair
    remaining = tuple(
        site
        for site in range(len(rows))
        if site not in (left, right, star)
    )
    return sp.cancel(
        2
        * rows[left][source]
        * rows[right][source]
        * hafnian(rows, betas, remaining)
    )


def full_response(rows, betas, source: int):
    """Return coefficients at every possible star, including exceptional ones."""
    site_count = len(rows)
    answer = [sp.S.Zero] * site_count
    for left, right in combinations(range(site_count), 2):
        marked = 2 * rows[left][source] * rows[right][source]
        if marked == 0:
            continue
        for star in range(site_count):
            if star in (left, right):
                continue
            remaining = tuple(
                site
                for site in range(site_count)
                if site not in (left, right, star)
            )
            answer[star] += marked * hafnian(rows, betas, remaining)
    return tuple(sp.cancel(value) for value in answer)


def data(r: int, exceptional_betas):
    exceptional_betas = tuple(map(sp.sympify, exceptional_betas))
    t = len(exceptional_betas)
    exceptional = tuple(range(t))
    active_count = 2 * r + 2 - t
    active = tuple(range(t, t + active_count))
    extra = t + active_count
    betas = exceptional_betas + (sp.S.One,) * (active_count + 1)
    return exceptional, active, extra, betas


def subset_pivot(r: int, exceptional_betas, marked: int):
    exceptional_betas = tuple(map(sp.sympify, exceptional_betas))
    t = len(exceptional_betas)
    return sp.cancel(
        2
        * factorial(r)
        * sp.prod(
            1 / (exceptional_betas[index] + 1)
            for index in range(t)
            if index != marked
        )
        * KAPPA ** (r - t + 1)
    )


def endpoint_pivot(r: int, exceptional_betas, marked: int, opposite: int):
    exceptional_betas = tuple(map(sp.sympify, exceptional_betas))
    left = set(range(len(exceptional_betas))) - {marked, opposite}
    return sp.cancel(
        2
        * factorial(r - 1)
        * sp.prod(1 / (exceptional_betas[index] + 1) for index in left)
        * sum(
            (exceptional_betas[index] + 1)
            / (exceptional_betas[index] + exceptional_betas[opposite])
            for index in left
        )
    )


def audit_normal_form():
    u = sp.Symbol("u")
    matrix = sp.Matrix([[1, 0, 0], [0, u, 1], [0, 0, 0]])
    assert matrix.rank() == 2
    # Columns zero and two give the output plane even at u=0.
    assert sp.Matrix.hstack(matrix[:, 0], matrix[:, 2]).rank() == 2
    assert matrix[2, :] == sp.zeros(1, 3)
    source_binary = sp.Matrix.vstack(sp.Matrix([E0]), sp.Matrix([E1]))
    combined = sp.Matrix.vstack(matrix[:2, :], source_binary)
    assert combined.rank() == 3
    assert matrix.subs(u, 0).rank() == 2


def audit_subset_case(r: int, exceptional_betas, axial_parameter):
    exceptional, active, extra, betas = data(r, exceptional_betas)
    t = len(exceptional)
    assert 1 <= t <= r + 1
    marked = exceptional[0]
    size = r + 2 - t
    pivot = subset_pivot(r, exceptional_betas, marked)
    axial = (sp.S.Zero, sp.sympify(axial_parameter), sp.S.One)

    incidence = []
    for chosen_tuple in combinations(active, size):
        chosen = set(chosen_tuple)
        rows = [E1] * (extra + 1)
        for site in exceptional:
            rows[site] = E0
        rows[marked] = E2
        rows[extra] = axial
        for site in chosen:
            rows[site] = E0
        assert marked_pairs(rows, 2) == ((marked, extra),)
        response = full_response(rows, betas, 2)
        assert all(
            sp.cancel(response[site] - (pivot if site in chosen else 0)) == 0
            for site in active
        )
        assert response[extra] == 0
        incidence.append([int(site in chosen) for site in active])

        swapped = [E0] * (extra + 1)
        for site in exceptional:
            swapped[site] = E1
        swapped[marked] = E2
        swapped[extra] = axial
        for site in chosen:
            swapped[site] = E1
        assert marked_pairs(swapped, 2) == ((marked, extra),)
        response = full_response(swapped, betas, 2)
        assert all(
            sp.cancel(response[site] - (pivot if site in chosen else 0)) == 0
            for site in active
        )
        assert response[extra] == 0

    assert sp.Matrix(incidence).rank() == len(active)


def endpoint_rows(r, exceptional_betas, axial_parameter, marked, opposite, target):
    exceptional, active, extra, betas = data(r, exceptional_betas)
    left = set(exceptional) - {marked, opposite}
    rows = [E1] * (extra + 1)
    for site in left:
        rows[site] = E0
    rows[marked] = E2
    rows[opposite] = E1
    rows[target] = E0
    rows[extra] = (sp.S.Zero, sp.sympify(axial_parameter), sp.S.One)
    return rows, betas, exceptional, active, extra, left


def audit_endpoint_case(r: int, exceptional_betas, axial_parameter):
    assert len(exceptional_betas) == r + 2
    exceptional, active, _, _ = data(r, exceptional_betas)
    opposite = exceptional[0]
    pivots = []
    for marked in exceptional[1:]:
        pivot = endpoint_pivot(r, exceptional_betas, marked, opposite)
        pivots.append(pivot)
        for target in active:
            rows, betas, _, active_sites, extra, left = endpoint_rows(
                r,
                exceptional_betas,
                axial_parameter,
                marked,
                opposite,
                target,
            )
            assert marked_pairs(rows, 2) == ((marked, extra),)
            response = full_response(rows, betas, 2)
            assert sp.cancel(response[target] - pivot) == 0
            assert all(response[site] == 0 for site in active_sites if site != target)
            assert response[extra] == 0

            swapped = list(rows)
            for site in left:
                swapped[site] = E1
            swapped[opposite] = E0
            for site in active_sites:
                swapped[site] = E0
            swapped[target] = E1
            assert marked_pairs(swapped, 2) == ((marked, extra),)
            response = full_response(swapped, betas, 2)
            assert sp.cancel(response[target] - pivot) == 0
            assert all(response[site] == 0 for site in active_sites if site != target)
            assert response[extra] == 0
    assert any(sp.cancel(pivot) != 0 for pivot in pivots)


def audit_extra_cleanup(r: int, exceptional_betas):
    exceptional_betas = tuple(map(sp.sympify, exceptional_betas))
    exceptional, active, extra, betas = data(r, exceptional_betas)
    t = len(exceptional)
    a, b, c = sp.symbols("a b c")
    rows = [E1] * (extra + 1)
    rows[extra] = (a, b, c)
    if t >= 2:
        for site in exceptional:
            rows[site] = E0
        rows[exceptional[0]] = E2
        rows[exceptional[1]] = E2
        for site in active[: r + 2 - t]:
            rows[site] = E0
        source = 2
        expected = sp.cancel(
            2
            * factorial(r)
            * sp.prod(
                1 / (exceptional_betas[index] + 1)
                for index in range(2, t)
            )
            * KAPPA ** (r - t + 2)
        )
    else:
        rows[exceptional[0]] = E0
        for site in active[: r - 1]:
            rows[site] = E0
        source = 1
        expected = sp.cancel(
            2
            * comb(r + 2, 2)
            * factorial(r)
            / (exceptional_betas[0] + 1)
            * KAPPA ** (r - 1)
        )
    response = full_response(rows, betas, source)
    assert sp.cancel(response[extra] - expected) == 0
    pairs = marked_pairs(rows, source)
    pairs_away_from_extra = tuple(pair for pair in pairs if extra not in pair)
    assert sp.cancel(
        sum(
            star_contribution(rows, betas, source, pair, extra)
            for pair in pairs_away_from_extra
        )
        - expected
    ) == 0
    assert all(
        star_contribution(rows, betas, source, pair, extra) == 0
        for pair in pairs
        if extra in pair
    )
    # Every contaminating active coefficient is attached to a binary row;
    # exceptional stars are structurally zero, leaving only the extra block.
    assert all(rows[site] in (E0, E1) for site in active)
    killed = set(active) | set(exceptional)
    surviving = {
        site: value
        for site, value in enumerate(response)
        if site not in killed and value != 0
    }
    assert surviving == {extra: expected}


def audit_third_row_cleanup_subset(r: int, exceptional_betas, axial_parameter):
    exceptional, active, extra, betas = data(r, exceptional_betas)
    t = len(exceptional)
    marked = exceptional[0]
    size = r + 2 - t
    pivot = subset_pivot(r, exceptional_betas, marked)
    targets = [active[0], active[-1]]
    for target in targets:
        chosen = set(next(s for s in combinations(active, size) if target in s))
        rows = [E1] * (extra + 1)
        for site in exceptional:
            rows[site] = E0
        rows[marked] = E2
        for site in chosen:
            rows[site] = E0
        common_live_count = 2 * r - t
        rows[target] = E2 if target < t + common_live_count else ZERO
        rows[extra] = (sp.S.Zero, sp.sympify(axial_parameter), sp.S.One)
        pairs = marked_pairs(rows, 2)
        expected_pairs = {(marked, extra)}
        if rows[target] == E2:
            expected_pairs |= {(marked, target), (target, extra)}
        assert set(pairs) == expected_pairs
        assert sp.cancel(
            star_contribution(rows, betas, 2, (marked, extra), target)
            - pivot
        ) == 0
        assert all(
            star_contribution(rows, betas, 2, pair, target) == 0
            for pair in pairs
            if pair != (marked, extra)
        )
        response = full_response(rows, betas, 2)
        assert sp.cancel(response[target] - pivot) == 0
        assert all(rows[site] in (E0, E1) for site in active if site != target)
        killed = (set(active) - {target}) | set(exceptional) | {extra}
        surviving = {
            site: value
            for site, value in enumerate(response)
            if site not in killed and value != 0
        }
        assert surviving == {target: pivot}


def audit_third_row_cleanup_endpoint(r: int, exceptional_betas, axial_parameter):
    exceptional, active, _, _ = data(r, exceptional_betas)
    opposite = exceptional[0]
    pivots = {
        marked: endpoint_pivot(r, exceptional_betas, marked, opposite)
        for marked in exceptional[1:]
    }
    marked, pivot = next((site, value) for site, value in pivots.items() if value != 0)
    common_live_count = 2 * r - len(exceptional)
    for target in (active[0], active[-1]):
        rows, betas, exceptional_sites, active_sites, extra, _ = endpoint_rows(
            r,
            exceptional_betas,
            axial_parameter,
            marked,
            opposite,
            target,
        )
        rows[target] = E2 if target < len(exceptional) + common_live_count else ZERO
        pairs = marked_pairs(rows, 2)
        expected_pairs = {(marked, extra)}
        if rows[target] == E2:
            expected_pairs |= {(marked, target), (target, extra)}
        assert set(pairs) == expected_pairs
        assert sp.cancel(
            star_contribution(rows, betas, 2, (marked, extra), target)
            - pivot
        ) == 0
        assert all(
            star_contribution(rows, betas, 2, pair, target) == 0
            for pair in pairs
            if pair != (marked, extra)
        )
        response = full_response(rows, betas, 2)
        assert sp.cancel(response[target] - pivot) == 0
        assert all(
            rows[site] in (E0, E1) for site in active_sites if site != target
        )
        killed = (
            (set(active_sites) - {target}) | set(exceptional_sites) | {extra}
        )
        surviving = {
            site: value
            for site, value in enumerate(response)
            if site not in killed and value != 0
        }
        assert surviving == {target: pivot}


def audit_deletion_transform():
    for r in range(2, 13):
        transform = sp.ones(r + 1) - sp.eye(r + 1)
        assert transform.det() == (-1) ** r * r
        assert transform.eigenvals() == {sp.Integer(-1): r, sp.Integer(r): 1}


def main():
    u, nu = sp.symbols("u nu")
    audit_normal_form()

    audit_subset_case(2, [nu], u)
    audit_subset_case(2, [2, 2], 0)
    audit_subset_case(2, [2, 2, 3], 0)
    audit_subset_case(3, [2, 2, 3, 3], sp.Rational(-7, 5))

    values = sp.symbols("v0:4")
    audit_endpoint_case(2, values, u)
    audit_endpoint_case(2, [2, 2, 3, 3], 0)
    audit_endpoint_case(3, [2, 2, 3, 3, 4], sp.Rational(5, 7))

    audit_extra_cleanup(2, [nu])
    audit_extra_cleanup(2, [2, 2, 3])
    audit_extra_cleanup(2, [2, 2, 3, 3])
    audit_third_row_cleanup_subset(2, [nu], u)
    audit_third_row_cleanup_subset(2, [2, 2, 3], 0)
    audit_third_row_cleanup_endpoint(2, [2, 2, 3, 3], 0)
    audit_third_row_cleanup_endpoint(3, [2, 2, 3, 3, 4], sp.Rational(5, 7))
    audit_deletion_transform()

    print("Live three-zero extra-plane axial independent audit: PASS")
    print("normal form and forced marked pair: exact")
    print("subset balances and endpoint Cauchy permanents: exact")
    print("extra/third-row triangular contamination: retained")
    print("repeated beta, r=2, and u=0 cases: exact")
    print("J-I determinants through r=12: exact")


if __name__ == "__main__":
    main()
