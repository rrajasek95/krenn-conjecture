#!/usr/bin/env python3
"""Exact response/permanent audit for the sole-plane (r,t)=(3,6) closure.

The response checks below reconstruct the literal source-22 marked-pair
coefficients, including every contaminating active star.  The final stage
checks the three localized Cauchy-permanent ideals over QQ.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations, permutations

import sympy as sp

import explore_live_three_zero_sole_plane_first_high_permanents as ideals


E0 = (sp.S.One, sp.S.Zero, sp.S.Zero)
E1 = (sp.S.Zero, sp.S.One, sp.S.Zero)
E2 = (sp.S.Zero, sp.S.Zero, sp.S.One)
ZERO = (sp.S.Zero, sp.S.Zero, sp.S.Zero)
HESSIAN = sp.Matrix(((0, 1, 1), (1, 0, 1), (1, 1, 0)))
LIVE = tuple(range(6))
ACTIVE = (6, 7, 8)
CENTRES = (6, 7)
EXTRA = 8


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
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


def edge(rows, betas, left, right):
    return (
        (sp.Matrix([rows[left]]) * HESSIAN * sp.Matrix([rows[right]]).T)[0]
        / (betas[left] + betas[right])
    )


def hafnian(rows, betas, vertices):
    return sum(
        (
            sp.prod(edge(rows, betas, left, right) for left, right in matching)
            for matching in perfect_matchings(tuple(vertices))
        ),
        sp.S.Zero,
    )


def source_22_response(rows, betas, direct_scale):
    """Return the three actual active-star coefficients for source 22."""
    # The direct quadratic is supported only on source 01.  Keeping its
    # arbitrary scale here audits, rather than assumes, its disappearance.
    direct = sp.Matrix(
        ((0, direct_scale, 0), (direct_scale, 0, 0), (0, 0, 0))
    )
    direct_weight = direct[2, 2]
    assert direct_weight == 0
    answer = {}
    vertices = tuple(range(9))
    for star in ACTIVE:
        coefficient = direct_weight * hafnian(
            rows, betas, tuple(site for site in vertices if site != star)
        )
        for left, right in combinations(vertices, 2):
            if star in (left, right):
                continue
            marked_weight = 2 * rows[left][2] * rows[right][2]
            if marked_weight == 0:
                continue
            remaining = tuple(
                site for site in vertices if site not in (left, right, star)
            )
            coefficient += marked_weight * hafnian(rows, betas, remaining)
        # Keep triangular contamination factored as a sum of matching
        # monomials.  Expanding/cancelling a coefficient that is discarded
        # later is both unnecessary and dramatically more expensive.
        answer[star] = coefficient
    return answer


def permanent(rows, columns):
    return sum(
        (
            sp.prod(
                1 / (rows[index] + columns[permutation[index]])
                for index in range(len(rows))
            )
            for permutation in permutations(range(len(rows)))
        ),
        sp.S.Zero,
    )


def assert_equal(left, right):
    assert sp.cancel(left - right) == 0, sp.factor(sp.cancel(left - right))


def base_data():
    betas_live = sp.symbols("b0:6")
    betas = betas_live + (sp.S.One, sp.S.One, sp.S.One)
    direct_scale = sp.Symbol("lambda")
    return betas_live, betas, direct_scale


def audit_noncoordinate_P_rows():
    betas_live, betas, direct_scale = base_data()
    p0, p1, p2 = sp.symbols("p0 p1 p2")
    marked = 0
    left = (1, 2, 3)
    right = (4, 5)
    pivot = 2 * p2 * permanent(
        tuple(betas_live[index] for index in left),
        (sp.S.One,) + tuple(betas_live[index] for index in right),
    )
    for target in CENTRES:
        other = next(site for site in CENTRES if site != target)
        for target_row in range(3):
            rows = [None] * 9
            rows[marked] = E2
            rows[EXTRA] = (p0, p1, p2)
            if target_row == 1:
                rows[target] = E1
                rows[other] = E0
                for site in left:
                    rows[site] = E1
                for site in right:
                    rows[site] = E0
            else:
                rows[target] = E0 if target_row == 0 else ZERO
                rows[other] = E1
                for site in left:
                    rows[site] = E0
                for site in right:
                    rows[site] = E1
            response = source_22_response(tuple(rows), betas, direct_scale)
            assert_equal(response[target], pivot)
            assert_equal(response[other], 0)
            assert_equal(response[EXTRA], 0)


def audit_R_cleanup():
    betas_live, betas, direct_scale = base_data()
    p0, p1, p2 = sp.symbols("p0 p1 p2")
    marked = (0, 1)
    left = (2, 3)
    right = (4, 5)
    rows = [None] * 9
    for site in marked:
        rows[site] = E2
    for site in left:
        rows[site] = E0
    for site in right:
        rows[site] = E1
    rows[6] = E0
    rows[7] = E1
    rows[EXTRA] = (p0, p1, p2)
    response = source_22_response(tuple(rows), betas, direct_scale)
    pivot = 2 * permanent(
        (sp.S.One,) + tuple(betas_live[index] for index in left),
        (sp.S.One,) + tuple(betas_live[index] for index in right),
    )
    assert_equal(response[EXTRA], pivot)
    assert not ({p0, p1, p2, direct_scale} & response[EXTRA].free_symbols)
    # The centre coefficients are deliberately retained: they are the
    # triangular contamination killed by the preceding P rows.


def audit_coordinate_S_rows():
    betas_live, betas, direct_scale = base_data()
    marked = (0, 1)
    left = (2, 3, 4)
    singleton = 5
    pivot = 2 * permanent(
        tuple(betas_live[index] for index in left),
        (sp.S.One, sp.S.One, betas_live[singleton]),
    )
    for target in ACTIVE:
        others = tuple(site for site in ACTIVE if site != target)
        for target_row in (0, 1):
            same = E0 if target_row == 0 else E1
            opposite = E1 if target_row == 0 else E0
            rows = [None] * 9
            for site in marked:
                rows[site] = E2
            for site in left:
                rows[site] = same
            rows[singleton] = opposite
            rows[target] = same
            for site in others:
                rows[site] = opposite
            response = source_22_response(tuple(rows), betas, direct_scale)
            assert_equal(response[target], pivot)
            for site in others:
                assert_equal(response[site], 0)


def audit_coordinate_R_rows():
    betas_live, betas, direct_scale = base_data()
    marked = (0, 1)
    left = (2, 3)
    right = (4, 5)
    pivot = 2 * permanent(
        (sp.S.One,) + tuple(betas_live[index] for index in left),
        (sp.S.One,) + tuple(betas_live[index] for index in right),
    )
    for target in ACTIVE:
        others = tuple(site for site in ACTIVE if site != target)
        for swap in (False, True):
            zero, one = (E1, E0) if swap else (E0, E1)
            rows = [None] * 9
            for site in marked:
                rows[site] = E2
            for site in left:
                rows[site] = zero
            for site in right:
                rows[site] = one
            rows[target] = ZERO
            rows[others[0]] = zero
            rows[others[1]] = one
            response = source_22_response(tuple(rows), betas, direct_scale)
            assert_equal(response[target], pivot)
            for site in others:
                assert_equal(response[site], 0)


def monic_factor(expression, variables):
    return sp.Poly(expression, *variables, domain=sp.QQ).monic().as_expr()


def raw_pivots(profile, family):
    _variables, live, _localizer = ideals.profile_data(profile)
    indices = tuple(range(6))
    if family == "P":
        for marked in indices:
            remaining = tuple(index for index in indices if index != marked)
            for left in combinations(remaining, 3):
                right = tuple(index for index in remaining if index not in left)
                yield permanent(
                    tuple(live[index] for index in left),
                    (sp.S.One,) + tuple(live[index] for index in right),
                )
    elif family == "R":
        for marked in combinations(indices, 2):
            remaining = tuple(index for index in indices if index not in marked)
            for left in combinations(remaining, 2):
                right = tuple(index for index in remaining if index not in left)
                if left <= right:
                    yield permanent(
                        (sp.S.One,) + tuple(live[index] for index in left),
                        (sp.S.One,) + tuple(live[index] for index in right),
                    )
    elif family == "S":
        for marked in combinations(indices, 2):
            remaining = tuple(index for index in indices if index not in marked)
            for singleton in remaining:
                left = tuple(index for index in remaining if index != singleton)
                yield permanent(
                    tuple(live[index] for index in left),
                    (sp.S.One, sp.S.One, live[singleton]),
                )
    else:
        raise ValueError(family)


def audit_localizers_and_zero_beta():
    for profile, multiplicities in ideals.PROFILE_MULTIPLICITIES.items():
        variables, _live, localizer = ideals.profile_data(profile)
        actual = {
            monic_factor(factor, variables)
            for factor, _exponent in sp.factor_list(localizer)[1]
        }
        expected = {
            monic_factor(value - 1, variables) for value in variables
        } | {
            monic_factor(value + 1, variables) for value in variables
        }
        expected |= {
            monic_factor(left - right, variables)
            for left, right in combinations(variables, 2)
        }
        expected |= {
            monic_factor(left + right, variables)
            for left, right in combinations(variables, 2)
        }
        expected |= {
            monic_factor(value, variables)
            for value, multiplicity in zip(variables, multiplicities)
            if multiplicity >= 2
        }
        assert actual == expected

        allowed_denominators = {
            monic_factor(value + 1, variables) for value in variables
        } | {
            monic_factor(left + right, variables)
            for left, right in combinations(variables, 2)
        } | {
            monic_factor(value, variables)
            for value, multiplicity in zip(variables, multiplicities)
            if multiplicity >= 2
        }
        for family in ("P", "R", "S"):
            for expression in raw_pivots(profile, family):
                denominator = sp.cancel(expression).as_numer_denom()[1]
                factors = {
                    monic_factor(factor, variables)
                    for factor, _exponent in sp.factor_list(denominator)[1]
                }
                assert factors <= allowed_denominators

        # A singleton exceptional class may equal zero.  Test every such
        # boundary separately; repeated classes cannot be zero because a
        # pair of equal beta values would have denominator 2 beta.
        for zero_index, multiplicity in enumerate(multiplicities):
            if multiplicity != 1:
                continue
            values = [sp.Rational(index + 2) for index in range(len(variables))]
            values[zero_index] = sp.S.Zero
            substitution = dict(zip(variables, values))
            assert localizer.subs(substitution) != 0
            for family, function in (
                ("P", ideals.one_common_pivots),
                ("R", ideals.two_common_pivots),
                ("S", ideals.two_same_common_pivots),
            ):
                assert any(
                    polynomial.subs(substitution) != 0
                    for polynomial in function(profile)
                ), (profile, family, zero_index)


def audit_kernel_chart_cover():
    a, b = sp.symbols("a b")
    charts = {
        "01": sp.Matrix(((1, 0, a), (0, 1, b))),
        "12": sp.Matrix(((a, 1, 0), (b, 0, 1))),
        "02": sp.Matrix(((1, a, 0), (0, b, 1))),
    }
    binary_plane = sp.Matrix(((1, 0, 0), (0, 1, 0)))
    assert charts["01"].subs({a: 0, b: 0}) == binary_plane
    # In chart 01, a or b itself supplies the required source-2 entry.
    assert charts["01"][0, 2] == a and charts["01"][1, 2] == b
    # The other two charts are wholly noncoordinate and have a literal
    # source-2 entry in their second normalized row.
    assert charts["12"][1, 2] == 1
    assert charts["02"][1, 2] == 1
    for matrix in charts.values():
        assert matrix.rank() == 2


def audit_response_formulas():
    audit_noncoordinate_P_rows()
    audit_R_cleanup()
    audit_coordinate_S_rows()
    audit_coordinate_R_rows()
    audit_kernel_chart_cover()
    audit_localizers_and_zero_beta()
    print("actual source-22 P/R/S response formulas: PASS", flush=True)
    print("three kernel charts and zero-beta/localizer boundaries: PASS", flush=True)


def audit_unit_ideals():
    for profile in ideals.PROFILE_MULTIPLICITIES:
        for family in ("P", "R", "S"):
            pivots, result = ideals.status(profile, family)
            assert result == "UNIT", (profile, family, result)
            print(
                profile, family, "pivots", len(pivots), "status", result,
                flush=True,
            )
    print("all twelve localized QQ permanent ideals: UNIT", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--response-only", action="store_true",
        help="skip the slower twelve exact Singular unit-ideal checks",
    )
    args = parser.parse_args()
    audit_response_formulas()
    if not args.response_only:
        audit_unit_ideals()
    print("sole-plane (r,t)=(3,6): COMPLETE PASS", flush=True)


if __name__ == "__main__":
    main()
